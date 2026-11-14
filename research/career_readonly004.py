"""Private stable-save snapshots and conservative public reader coverage.

No UI, native host, process memory reading of FM or calendar executor exists here.
"""
from collections import Counter
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from hashlib import file_digest, sha256
import importlib.metadata
import json
from pathlib import Path
import re
import shutil

PROBES = ('open','managed_clubs','clubs','players','training','tactics','selections',
          'set_pieces','staff','staff_lists','injuries','fixtures')
SHA = re.compile(r'[0-9a-f]{64}\Z')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with Path(path).open('rb') as stream:
        return file_digest(stream,'sha256').hexdigest()


def write(path, value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2,default=str)+'\n',encoding='utf8')


def snapshot(source, target, approved_basename, max_bytes=512*1024**2):
    """Never overwrite; preserve a partial/different copy after a failed invariant."""
    source,target=Path(source),Path(target)
    require(source.name==approved_basename and source.suffix.lower()=='.fm','Source is not the approved save')
    before=source.stat()
    require(0<before.st_size<=max_bytes,'Save size outside technical contract')
    source_hash=digest(source)
    target.parent.mkdir(parents=True,exist_ok=True)
    with source.open('rb') as incoming,target.open('xb') as outgoing:
        shutil.copyfileobj(incoming,outgoing,1024*1024)
    copy_hash=digest(target);after_hash=digest(source);after=source.stat()
    receipt=dict(source_sha256_before=source_hash,source_sha256_after_copy=after_hash,
                 snapshot_sha256=copy_hash,bytes=before.st_size,
                 size_unchanged=before.st_size==after.st_size,
                 mtime_unchanged=before.st_mtime_ns==after.st_mtime_ns,
                 stable=source_hash==copy_hash==after_hash and
                        before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns)
    return receipt


def source_inventory():
    d=importlib.metadata.distribution('fmsave');package=Path(d.locate_file('fmsave'))
    names=('_save.py','_container.py','_version.py','_context.py','models/meta.py',
           'models/training.py','models/players.py','models/tactics.py','models/staff.py',
           'models/injuries.py','readers/training.py','readers/tactics.py','readers/players.py')
    return dict(package='fmsave',version=d.version,files={n:digest(package/n) for n in names})


def safe_build(value):
    require(isinstance(value,str) and re.fullmatch(r'\d+\.\d+\.\d+\+\d+',value),'Unrecognized build string')
    return value


def section_summary(info):
    require(info.game=='FM27','Approved audit requires an FM27 save')
    require(all(re.fullmatch(r'[A-Za-z0-9_]{1,64}',s.name) for s in info.sections),
            'Unexpected section code: keep raw name private')
    return dict(game=info.game,save_build=safe_build(info.build),known_build=bool(info.known_build),
        game_date_claim=info.game_date.isoformat() if info.game_date else None,
        game_date_semantics_verified=False,time_slot_raw=info.time_slot,
        sections=[dict(code=s.name,schema=s.schema,compressed_bytes=s.compressed_size,
                       decompressed_bytes=s.decompressed_size) for s in info.sections])


def _enum_code(value):
    number=getattr(value,'raw',getattr(value,'value',value))
    require(type(number) is int,'Training session is not a raw integer')
    return number


def _field_inventory(rows):
    if not rows:return []
    value=rows[0]
    return sorted(value.__dataclass_fields__) if is_dataclass(value) else []


def summarize_probe(name, value, context, info):
    """Own whitelist; never serializes record repr, names, identities or source paths."""
    rows=list(value);result=dict(rows=len(rows),record_fields=_field_inventory(rows),semantics_verified=False)
    if name=='managed_clubs':
        context['managed_uid']=rows[0].club_uid if len(rows)==1 else None
        result.update(single_managed_club=len(rows)==1,
                      manager_identity_resolved=sum(r.manager_staff_uid is not None for r in rows))
    elif name=='clubs':
        own=[r for r in rows if r.uid==context.get('managed_uid')]
        context['team_ids']=[t.team_id for r in own for t in r.teams]
        result['managed_team_capacity']=len(context['team_ids']) if own else None
    elif name=='players':
        # Counts only; no new raw/display mapping and no player identities exported.
        team_ids=set(context.get('team_ids',[]))
        own=[r for r in rows if getattr(r,'team_id',None) in team_ids]
        result['managed_squad_records']=len(own) if team_ids else None
        context['managed_players']={r.uid for r in own}
        result['attribute_pair_coverage']={}
        for field in ('acceleration','pace','agility','stamina'):
            pairs=[(getattr(r.raw_attributes,field),getattr(r.attributes,field)) for r in own
                   if getattr(r.raw_attributes,field,None) is not None and getattr(r.attributes,field,None) is not None]
            result['attribute_pair_coverage'][field]=dict(pairs=len(pairs),
                raw_range=[min(a for a,b in pairs),max(a for a,b in pairs)] if pairs else None,
                display_range=[min(b for a,b in pairs),max(b for a,b in pairs)] if pairs else None,
                parser_derived_only=True,fm_ui_calibrated=False)
    elif name=='training':
        teams=[]
        for i,r in enumerate(rows):
            codes=Counter(_enum_code(s) for w in r.weeks for d in w.days for s in d.sessions)
            dated=[w for w in r.weeks if w.week_start is not None]
            teams.append(dict(team_code=f'T{i:02d}',weeks=len(r.weeks),dated_weeks=len(dated),
                days=sum(len(w.days) for w in r.weeks),
                raw_session_counts={str(k):v for k,v in sorted(codes.items())},
                first_week=min((w.week_start for w in dated),default=None),
                last_week=max((w.week_start for w in dated),default=None)))
        result.update(teams=teams,individual_participation=None,coach_assignment=None,
                      focus_assignment=None,intensity_assignment=None)
    elif name=='injuries':
        own=[r for r in rows if getattr(r,'club_uid',None)==context.get('managed_uid')]
        result.update(managed_injury_records=len(own),
            record_kinds=dict(Counter(getattr(getattr(r,'kind',None),'name','unknown') for r in own)),
            observed_injury_intervals=None)
    elif name=='tactics':
        result.update(selected_tactic_identified=False,tactical_effectiveness=None,
                      role_semantics_verified=False,ip_oop_engine_binding_verified=False)
    elif name in ('staff','staff_lists'):
        result.update(individual_session_coach_assignment=None)
    elif name=='fixtures':
        result['authoritative_career_calendar_verified']=False
    return result


def public_report(events, snapshot_receipt, inventory, resources, final_hash):
    """Generate only fixed own keys, preserving failure/missing/not-started states."""
    require(all(SHA.fullmatch(snapshot_receipt[k]) for k in
                ('source_sha256_before','source_sha256_after_copy','snapshot_sha256')),'Bad snapshot hashes')
    indexed={}
    for e in events:
        require(e['probe'] in PROBES,'Unknown probe')
        indexed[e['probe']]=e
    probes=[]
    for name in PROBES:
        e=indexed.get(name)
        if not e:probes.append(dict(probe=name,status='not_started'));continue
        row=dict(probe=name,status='started_unresolved' if e['status']=='started' else e['status'])
        if e['status']=='ok':
            row['coverage']=e['coverage']
            row['warning_types']=e.get('warning_types',[])
        elif e['status']=='failed':row['error_type']=e['error_type']
        probes.append(row)
    stable=snapshot_receipt['stable'] and final_hash==snapshot_receipt['source_sha256_before']
    return dict(experiment_id='VALID-004-CAREER-R0',kind='single_save_readonly_coverage',
        snapshot={**snapshot_receipt,'source_sha256_after_reader':final_hash,'stable_through_reader':stable},
        reader=inventory,resources=resources,probes=probes,
        native_released=False,career_advance_released=False,replay_released=False,
        source_semantics_verified=False,ui_to_save_binding_verified=False,
        career_rng_independence_verified=False,individual_participation_verified=False,
        native_starts=0,calendar_advances=0,seeds_reserved=0,
        missing=['independent_ui_field_validation','career_rng_stream_provenance',
                 'individual_actual_session_participation','session_coach_focus_intensity_binding',
                 'observed_injury_intervals','passive_native_tactical_effectiveness',
                 'calendar_executor_validation'])

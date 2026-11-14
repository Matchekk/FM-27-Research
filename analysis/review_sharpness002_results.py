"""Independent, read-only sharpness input/raw-result auditor; never a runner.

No save, engine, host, registry-write or allocation API is used. JSON/JSONL,
frozen source and already-existing FM27CFG1 inputs are the only file evidence.
Missing evidence fails closed. Successful software checks do not authorize native
execution; actual release, publication CI and director admission remain separate.
"""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
EXPERIMENT='MECH-002-SHARPNESS-P0'
CONTEXTS=('high_press','deep_block')
ARMS=('S70-P0','S100-P0','S70-P1','S100-P1')
HOST='58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
STAGES=('prepared','first_advance','finished')
STAT_KEYS=('xg','shots','shots_on_target','passes','completed_passes','possession','possession_ticks')
RAW_FIELDS=('condition_raw','sharpness_raw','sharpness_secondary_raw','fatigue_raw',
            'condition_accumulator_raw','sharpness_penalty_raw')
DESCRIPTIVE=tuple(f'{s}_{v}_mean' for s in ('prepared','first','finished')
    for v in ('condition_cache89','sharpness_cache8a'))+(
    'prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00',
    'finished_tf33_distinct_hashes',*(f'finished_{k}_mean' for k in RAW_FIELDS))
HASH=re.compile('[0-9a-f]{64}\\Z')


def need(condition,message):
    if not condition:raise ValueError(message)


def canonical(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def file_sha(path,normalized=False):
    path=Path(path)
    need(path.suffix.lower() in ('.json','.jsonl','.bin','.py','.md','.txt','.h','.patch','.stdout'),
         'Only approved evidence extensions may be read')
    raw=path.read_bytes()
    return sha256(raw.replace(b'\r\n',b'\n') if normalized else raw).hexdigest()


def read(path):
    path=Path(path);need(path.suffix in ('.json','.jsonl'),'Only JSON evidence allowed')
    def pairs(items):
        output={}
        for key,value in items:
            need(key not in output,'Duplicate JSON field');output[key]=value
        return output
    def constant(_):raise ValueError('Nonfinite JSON constant')
    decode=lambda raw:json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)
    if path.suffix=='.jsonl':
        with path.open(encoding='utf8') as stream:return [decode(line) for line in stream if line.strip()]
    return decode(path.read_text(encoding='utf8'))


def utc(value):
    need(type(value) is str,'UTC timestamp required');parsed=datetime.fromisoformat(value)
    need(parsed.utcoffset()==timedelta(0),'Timestamp must be UTC');return parsed


def number(value):return type(value) in (int,float) and math.isfinite(value)


def integer(value,low=0,high=0xffffffff):
    need(type(value) is int and low<=value<=high,'Exact bounded integer required')


def records(payload):
    need(type(payload) is bytes and payload[:8]==b'FM27CFG1' and len(payload)>=12,'Configuration header differs')
    count=struct.unpack_from('<I',payload,8)[0]
    need(count==5557 and len(payload)==12+20*count,'Configuration record count/length differs')
    rows=list(struct.iter_unpack('<5I',payload[12:]))
    need(not any(r[0]==61 for r in rows),'Execution records forbidden');return rows


def seed_values(value,active=False):
    output=set()
    if type(value) is dict:
        for key,child in value.items():
            output.update(seed_values(child,active or key in ('seed','seeds','validation_seeds','effective_seed')))
    elif type(value) is list:
        for child in value:output.update(seed_values(child,active))
    elif active and type(value) is int:output.add(value)
    return output


def reconstruct_exclusions(central):
    """Reconstruct the frozen exclusion commitment without changing a registry."""
    central=Path(central);used={0};sources=0
    roots=[p for p in (central/'data').iterdir() if p.is_dir() and p.name!='mech-002-sharpness-p0']
    roots += [p for p in (central/'local').iterdir() if p.is_dir() and p.name!='mech-002-sharpness-p0'
        and p.name.startswith(('valid','tact-','attr-','mech-','night-','platform-smoke'))]
    paths=[p for root in roots for p in root.rglob('*.json*') if p.suffix in ('.json','.jsonl')]
    paths += [p for p in (central/'local/registry').glob('*.json') if p.name!=EXPERIMENT+'.reserved.json']
    for path in paths:
        used.update(seed_values(read(path)));sources+=1
    return used,sources


def deterministic_candidates(namespace,count,excluded):
    # Pure independent reconstruction, no use of core.allocate or registry API.
    selected=[];counter=0;taken=set(excluded)|{0}
    while len(selected)<count:
        candidate=int.from_bytes(sha256((namespace+'/'+str(counter)).encode()).digest()[:4],'little');counter+=1
        if candidate not in taken:selected.append(candidate);taken.add(candidate)
    return selected


def audit_seed_plan(plan,excluded):
    need(plan['experiment_id']==EXPERIMENT and plan['namespace']==EXPERIMENT+'/main-v1' and
         plan['technical_namespace']==EXPERIMENT+'/technical-v1','Seed namespace differs')
    main,tech,total=[plan[k] for k in ('main_seeds','technical_seeds','seeds')]
    need(type(main) is list and type(tech) is list and type(total) is list and
         len(main)==64 and len(tech)==4 and len(total)==len(set(total))==68 and total==main+tech,'Exact ordered64+4 seed inventory required')
    for value in total:integer(value,1)
    need(not set(total)&excluded and plan['excluded_seed_count']==len(excluded) and
         plan['excluded_seed_set_sha256']==canonical(sorted(excluded)),'Seed exclusion commitment differs')
    need(main==deterministic_candidates(plan['namespace'],64,excluded) and
         tech==deterministic_candidates(plan['technical_namespace'],4,excluded|set(main)),
         'Independent deterministic seed reconstruction differs')
    return dict(main_seeds=64,technical_seeds=4,distinct_seeds=68,excluded_seed_count=len(excluded),
                excluded_seed_set_sha256=canonical(sorted(excluded)),seed_plan_canonical_sha256=canonical(plan))


def expected_jobs(seedplan,receipt=None):
    if receipt is None:
        jobs=[dict(key=f'tech-{h}-s{s}-{a}-r{r}',job_id=f'tech-{h}-s{s}-{a}-r{r}',scenario=h,context=h,
            side=s,team_side=s,arm=a,seed=seedplan['technical_seeds'][i],repeat=r,kind='full')
            for i,(h,s) in enumerate(product(CONTEXTS,(0,1))) for a,r in product(ARMS,(0,1))]
        return jobs+[dict(key='negative-malformed',job_id='negative-malformed',kind='negative',seed=None)]
    c=receipt['config'];need(receipt['seeds']==seedplan['main_seeds'] and receipt['config_sha256']==canonical(c),'Manifest seed/config differs')
    jobs=[]
    for h,context in enumerate(CONTEXTS):
        for seed,side,arm in product(seedplan['main_seeds'][h*32:(h+1)*32],(0,1),ARMS):
            key=f'{context}-{seed}-{side}-{arm}'
            jobs.append(dict(key=key,scenario=context,seed=seed,side=side,arm=arm,
                setup_sha256=c['design']['setups'][context][str(side)][arm],config_sha256=canonical(c),identity=c['identity']))
    return sorted(jobs,key=lambda job:sha256(job['key'].encode()).digest())


def expected_input(base,side,arm):
    need(type(side) is int and side in (0,1) and arm in ARMS,'Unknown intervention cell')
    source=records(base);lineup={(s,a):v for k,s,a,b,v in source if k==11 and b==0}
    need(len([r for r in source if r[0]==11 and r[3]==0])==22 and
         set(lineup)==set(product((0,1),range(11))) and
         all(len({lineup[s,i] for i in range(11)})==11 for s in (0,1)),'Absolute lineup differs')
    attributes=[r for r in source if r[0]==1];profiles=[r for r in source if r[0]==15]
    need(len(attributes)==3174 and {r[1:4] for r in attributes}==set(product((0,1),range(23),range(69))) and
         len(profiles)==1058 and {r[1:4] for r in profiles}==set(product((0,1),range(23),range(23))),
         'Full active input inventory differs')
    need([r[4] for r in attributes if r[3]==52]==[60]*46,'Original active stamina must all be60')
    need(all(r[4]==10000 for r in profiles if r[3] in (16,17)),'Original two-field start package differs')
    targets={lineup[side,i] for i in range(1,11)};low=arm.startswith('S70-');press=arm.endswith('P1')
    output=[]
    for k,s,a,b,v in source:
        if low and k==15 and s==side and a in targets and b in (16,17):need(v==10000,'Baseline sharpness differs');v=7000
        if press and (k,s,a,b)==(2,side,10,0):need(v==1313689463,'Baseline pressing differs');v=2000905329
        output.append((k,s,a,b,v))
    need(sum(x!=y for x,y in zip(source,output))==20*low+press,'Input mutation count differs')
    return base[:12]+b''.join(struct.pack('<5I',*r) for r in output),lineup


def audit_prepared(central):
    central=Path(central);public=central/'data/mech-002-sharpness-p0';local=central/'local/mech-002-sharpness-p0'
    frozen=read(public/'inputs.json');plan=read(public/'seed-plan.json');contract=read(public/'contract.json')
    excluded,count=reconstruct_exclusions(central);seeds=audit_seed_plan(plan,excluded)
    need(plan==read(local/'seed-plan.json')==read(central/'local/registry'/f'{EXPERIMENT}.reserved.json'),'Private/public seed plan differs')
    need(frozen['experiment_id']==EXPERIMENT and frozen['observer_host_sha256']==HOST and
         frozen['seed_plan_sha256']==file_sha(public/'seed-plan.json',True),'Frozen input identity differs')
    need(canonical(read(local/'configs.json'))==frozen['configs_sha256'],'Frozen baseline configuration differs')
    sourcefiles={}
    for name,wanted in frozen['code_sha256'].items():
        path=(central/name).resolve();need(central.resolve() in path.parents,'Source path escapes archive')
        need(file_sha(path,True)==wanted,'Frozen source hash differs');sourcefiles[name]=wanted
    old=read(central/'data/valid-005-observer-v1/inputs.json');prior=read(central/'data/mech-003-stamina/inputs.json')
    need(frozen['identity']==old['identity']==prior['identity'] and frozen['configs_sha256']==old['configs_sha256'],
         'Original input/config identities differ')
    proofs=[]
    for h,s in product(CONTEXTS,(0,1)):
        label=f'{h}-{s}';base=(central/f'local/valid005-observer-v1/inputs/{label}.bin').read_bytes()
        carrier=(central/f'local/mech-003-stamina/inputs/{label}-R01.bin').read_bytes()
        need(sha256(base).hexdigest()==old['setups'][label] and sha256(carrier).hexdigest()==prior['setups'][h][str(s)]['R01'],
             'Original published configuration hash differs')
        _,lineup=expected_input(base,s,'S100-P0');targets={lineup[s,i] for i in range(1,11)}
        restore=[r for r in records(carrier) if r[0]==1 and r[1]==s and r[2] in targets and r[3]==52 and r[4]==40]
        need(len(restore)==10,'Exactly ten original R01 stamina40 values required')
        restored=[(k,a,b,c,60) if (k,a,b,c,v) in restore else (k,a,b,c,v) for k,a,b,c,v in records(carrier)]
        need([(x,y) for x,y in zip(records(base),restored) if x!=y]==[
            ((2,s,10,0,1313689463),(2,s,10,0,2000905329))],'Original R01 restoration differs')
        original=frozen['original_inputs'][label];gold=central/'local/valid005-observer-v1/technical'/(label+'-observer_on.jsonl')
        need(original==dict(d00_sha256=sha256(base).hexdigest(),original_r01_sha256=sha256(carrier).hexdigest(),gold_sha256=file_sha(gold)),
             'Original source/hash manifest differs')
        controls={}
        for row in read(gold):
            if row.get('event')!='native_passive_state' or row['stage'] not in ('prepared','first_advance'):continue
            need(row['stage'] not in controls,'Duplicate frozen initial snapshot')
            actors=bind_snapshot(row);fields=('id','side','roster_index','condition_raw','fatigue_raw',
                'condition_accumulator_raw','sharpness_penalty_raw','effectiveness_region_hex')
            controls[row['stage']]=canonical([{k:p[k] for k in fields} for p in sorted(actors.values(),key=lambda p:p['id'])])
        need(set(controls)=={'prepared','first_advance'} and controls==frozen['frozen_controls'][label],
             'Frozen initial raw/control hashes differ from actual historical snapshots')
        for arm in ARMS:
            expected,_=expected_input(base,s,arm);actual=(local/'inputs'/f'{label}-{arm}.bin').read_bytes()
            need(actual==expected and sha256(actual).hexdigest()==frozen['setups'][h][str(s)][arm],
                 'Prepared input is not the independent intended record sequence')
            proofs.append(dict(context=h,side=s,arm=arm,sha256=sha256(actual).hexdigest()))
    from analysis.sharpness002_design import validate_design
    validate_design(contract)
    need(contract['design']['setups']==frozen['setups'] and contract['execution']['code_sha256']==sourcefiles and
         contract['execution']['input_manifest_sha256']==file_sha(public/'inputs.json',True) and
         contract['execution']['seed_plan_sha256']==file_sha(public/'seed-plan.json',True),'Concrete contract does not bind frozen inputs')
    release=read(central/'data/mech-002-startpolicy-tech/release-gate.json')
    selected={k:release[k] for k in ('experiment_id','passed','independently_released','release_commit','ci_run','summary_sha256','review_sha256')}
    need(selected==frozen['tech17_release']==contract['gates']['tech17'] and selected['passed'] is True and
         selected['independently_released'] is True and
         file_sha(central/'data/mech-002-startpolicy-tech/release-gate.json',True)==frozen['tech17_release_file_sha256'] and
         file_sha(central/'data/mech-002-startpolicy-tech/technical-summary.json',True)==selected['summary_sha256'] and
         file_sha(central/'docs/night-001/STARTPOLICY-002-RESULTS-REVIEW.md',True)==selected['review_sha256'],
         'Actual independently published TECH17 evidence binding differs')
    return dict(prepared_input_evidence_verified=True,native_start_authorized=False,seed_audit=seeds,
        seed_source_files_read=count,inputs_sha256=file_sha(public/'inputs.json',True),
        source_files_verified=len(sourcefiles),input_cells=proofs,tech17_release_binding=selected,
        own_native_budget_exists=(local/'budget.json').exists(),reviewer_native_starts=0)


def one(evidence,name):
    found=[r for r in evidence if r.get('event')==name];need(len(found)==1,'Missing/duplicate raw event: '+name);return found[0]


def outcome(evidence,seed):
    actual=one(evidence,'native_input_seed');need(actual['override'] is True and actual['effective_seed']==seed,'Actual controlled seed differs')
    finish=one(evidence,'natural_match_finished');stats=one(evidence,'native_match_statistics')
    need(finish['full_match_completed'] is True and stats['source']=='original_team_statistics','Natural endpoint missing')
    integer(finish['tick'],1,47995);integer(finish['clock'],0,0x7fffffff)
    need(type(finish['score']) is list and len(finish['score'])==2,'Two actual scores required')
    for v in finish['score']:integer(v,0,100)
    need([r['side'] for r in stats['teams']]==[0,1],'Actual team sides differ')
    teams=[{k:r[k] for k in STAT_KEYS} for r in stats['teams']]
    need(all(number(v) for row in teams for v in row.values()),'Nonfinite actual statistic')
    need(all(r['xg']>=0 and 0<=r['shots_on_target']<=r['shots'] and
        0<=r['completed_passes']<=r['passes'] and 0<=r['possession']<=1 for r in teams) and
        abs(sum(r['possession'] for r in teams)-1)<1e-6,'Implausible actual statistic')
    return dict(score=finish['score'],tick=finish['tick'],clock=finish['clock'],team_statistics=teams)


def bind_snapshot(row):
    need(row['event']=='native_passive_state' and row['schema']=='fm27.passive-observer.v1','Snapshot schema differs')
    bound={};identities=set()
    for p in row['players']:
        integer(p['side'],0,1);integer(p['roster_index'],0,22);integer(p['id'],1)
        key=(p['side'],p['roster_index']);need(key not in bound and p['id'] not in identities,'Duplicate actor identity/slot')
        for field in RAW_FIELDS:integer(p[field],0,0xffffffff if field=='condition_accumulator_raw' else 65535)
        for field,size in (('effectiveness_region_hex',33),('statistics_cache_region_hex',16)):
            raw=p[field]
            if field=='statistics_cache_region_hex' and raw is None:continue
            need(type(raw) is str and len(raw)==size*2 and re.fullmatch('[0-9a-f]+',raw),'Raw region shape differs')
        bound[key]=p;identities.add(p['id'])
    need(set(bound)==set(product((0,1),range(23))),'Exactly46 active snapshot actors required');return bound


def audit_readbacks(evidence,dump,binary,config,catalog,oop_map):
    source=records(binary);need(one(evidence,'native_scenario_readback_verified')['records']==5557 and
        one(evidence,'native_scenario_readback_verified')['after_original_preparation'] is True and
        one(evidence,'native_profile_bindings_verified')['fields']==1058 and
        one(evidence,'native_player_tactic_bindings_verified')['players']==22 and
        one(evidence,'native_player_tactic_bindings_verified')['phases']==2,'Native readback receipt differs')
    phases=[r for r in evidence if r.get('event')=='native_phase_configuration']
    need(len(phases)==4 and {(r['side'],r['phase']) for r in phases}==set(product((0,1),(0,1))),'Both native phases required')
    need(len(dump['teams'])==2,'Two native input teams required');attrs=profiles=phasecells=pi_groups=0
    for side,team in enumerate(dump['teams']):
        need(type(team['side']) is int and team['side']==side and team['count']==len(team['players'])==23,'Native input roster differs')
        for slot,p in enumerate(team['players']):
            need(p['index']==slot and p['id']==config['teams'][side]['players'][slot]['native_id'],'Native actor identity differs')
    offsets={0:(0x6c,4),1:(0x79,1),9:(0xbb8,4),10:(0xbbc,4),19:(0x70,1),20:(0xca8,1),21:(0xca2,1),22:(0xca3,1)}
    offsets.update({i:(0x72+i-2,1) for i in range(2,9)})
    offsets.update({i:(off,2) for i,off in enumerate((0xc98,0xc8c,0xc96,0xc78,0xc8a,0xc90,0xc7a,0xc84),11)})
    for k,side,slot,field,value in source:
        if k not in (1,15):continue
        p=dump['teams'][side]['players'][slot]
        if k==1:
            need(type(p['attributes'][field]) is int and p['attributes'][field]==value,'Raw native attribute differs');attrs+=1
        else:
            offset,length=offsets[field];raw=bytes.fromhex(p['prefix_hex'] if offset<0x80 else p['input_tail_hex'])
            at=offset if offset<0x80 else offset-0x4c5;actual=raw[at:at+length]
            wanted=struct.pack('<f',value/100) if field==0 else value.to_bytes(length,'little')
            need(actual==wanted,'Raw native profile value differs');profiles+=1
    roles={r['id']:int(r['flags']) for r in catalog['roles']};positions={r['id']:r['mask'] for r in catalog['positions']}
    for side,team in enumerate(config['teams']):
        got=dump['teams'][side];creator=bytes.fromhex(got['creator_hex']);bits=int.from_bytes(creator[:16],'little')
        need(creator[0x25]==team['mentality'],'Native mentality differs')
        for group in catalog['team_instructions']:
            selected=next(o['native_bit'] for o in group['options'] if o['id']==team['instructions'][str(group['id'])])
            need({o['native_bit'] for o in group['options'] if o['native_bit'] and bits>>o['native_bit']&1}==
                 ({selected} if selected else set()),'Native team instruction bits differ')
        for phase,cells in enumerate(team['phases']):
            need(len(cells)==11,'Eleven native tactic cells required')
            for i,cell in enumerate(cells):
                index=oop_map[side][i] if phase else i;raw=bytes.fromhex(got['tactical_slots'][phase][index])
                need(struct.unpack_from('<I',raw)[0]==positions[cell['position']] and
                    struct.unpack_from('<Q',raw,64)[0]==(roles[cell['role']]|int(cell['duty'])),'Native position/role differs')
                pi=got['personal_instructions'][phase][index]
                need(pi['target_player']==cell['target_player'] and pi['target_position']==cell['target_position'],'Native PI target differs')
                for group in catalog['player_instructions']:
                    selected=cell['instructions'][str(group['id'])]
                    need({o['id'] for o in group['options'] if o['id'] and int(pi['flags'])>>o['id']&1}==
                         ({selected} if selected else set()),'Native PI bits differ');pi_groups+=1
                phasecells+=1
    need((attrs,profiles,phasecells,pi_groups)==(3174,1058,44,748),'Complete native audit coverage required')
    need(all(p['attributes'][52]==60 for t in dump['teams'] for p in t['players']),'Active Stamina60 differs')
    return dict(attribute_values_verified=attrs,profile_fields_verified=profiles,phase_cells_verified=phasecells,pi_groups_verified=pi_groups)


def audit_raw_match(evidence,dump,job,binary,config,catalog,oop_map,frozen_controls):
    need(one(evidence,'native_image_fingerprint')['sha256']==job['identity']['engine_sha256'] and
         one(evidence,'native_engine_compatibility')['compatible'] is True and
         one(evidence,'windows_load_returned')['success'] is True,'Actual engine/loader identity differs')
    forbidden={'native_passive_observer_rejected','experimental_engine_version','native_execution_context_bound','native_execution_probe'}
    need(not any(r.get('event') in forbidden for r in evidence),'Forbidden native execution/rejection event')
    audit=audit_readbacks(evidence,dump,binary,config,catalog,oop_map);result=outcome(evidence,job['seed'])
    snapshots=[r for r in evidence if r.get('event')=='native_passive_state']
    need([r['stage'] for r in snapshots]==list(STAGES),'Three ordered native snapshots required')
    prepared,first,finish=snapshots
    need(prepared['advance_ordinal']==0 and prepared['tick']==prepared['tick_before']==prepared['requested_target'] and
        first['advance_ordinal']==1 and first['tick_before']==prepared['tick'] and
        first['requested_target']==first['tick_before']+1 and first['tick']>first['tick_before'] and
        finish['advance_ordinal']>=first['advance_ordinal'] and finish['tick']==result['tick']>=first['tick'] and
        finish['clock']==result['clock'],'First actual advance/natural finish binding differs')
    need(evidence.index(one(evidence,'native_input_seed'))<evidence.index(one(evidence,'native_scenario_readback_verified'))<
        evidence.index(prepared)<evidence.index(first)<evidence.index(finish)<evidence.index(one(evidence,'natural_match_finished')),
        'Native input/snapshot/finish ordering differs')
    lineup={(s,a):v for k,s,a,b,v in records(binary) if k==11 and b==0};side=job['side']
    targets={lineup[side,i] for i in range(1,11)};starters={(s,lineup[s,i]) for s,i in product((0,1),range(11))}
    level=7000 if job['arm'].startswith('S70-') else 10000;bit=66 if job['arm'].endswith('P1') else 0
    allstates=[];description={};missing={};controls={};identities=None
    dumped={(s,p['index']):p for s,t in enumerate(dump['teams']) for p in t['players']}
    for row in snapshots:
        need(type(row['seed']) is int and row['seed']==job['seed'] and row['match_version_raw']==0x1b000000,'Snapshot seed/version differs')
        bound=bind_snapshot(row);mapping={key:p['id'] for key,p in bound.items()}
        need(mapping=={key:p['id'] for key,p in dumped.items()} and (identities is None or identities==mapping),'Cross-stage actor identity differs');identities=mapping
        initial=row['stage']!='finished';chosen=[p for key,p in bound.items() if key[0]==side and key[1] in targets]
        need(len(chosen)==10,'Ten tested outfield actors required')
        for key,p in bound.items():
            if row['stage']=='prepared':
                tail=bytes.fromhex(dumped[key]['input_tail_hex'])
                for field,offset in (('condition_raw',0xc8a),('sharpness_raw',0xc90),('sharpness_secondary_raw',0xc7a),('fatigue_raw',0xc84)):
                    need(p[field]==struct.unpack_from('<H',tail,offset-0x4c5)[0],'Prepared snapshot not native dump-bound')
                need(bytes.fromhex(p['effectiveness_region_hex'])==tail[0xcba-0x4c5:0xcba-0x4c5+33],'Prepared raw33 not dump-bound')
            if initial:
                rawlevel=level if key[0]==side and key[1] in targets else 10000
                need(p['sharpness_raw']==p['sharpness_secondary_raw']==rawlevel and p['condition_raw']==10000 and
                    p['fatigue_raw']==p['sharpness_penalty_raw']==0 and p['condition_accumulator_raw']==1000000,'Initial raw treatment/control differs')
                if key in starters:
                    need(p['statistics_cache_region_hex'] is not None and bytes.fromhex(p['statistics_cache_region_hex'])[9:11]==
                        bytes((100,rawlevel//100)),'Actual starting actor cache transfer differs')
        prefix='first' if row['stage']=='first_advance' else row['stage']
        for offset,name in ((9,'condition_cache89'),(10,'sharpness_cache8a')):
            key=f'{prefix}_{name}_mean';values=[bytes.fromhex(p['statistics_cache_region_hex'])[offset]
                for p in chosen if p['statistics_cache_region_hex'] is not None]
            description[key]=sum(values)/10 if len(values)==10 else None
            if len(values)!=10:missing[key]='incomplete_identity_bound_runtime_cache'
        selected=[{k:p[k] for k in ('id','side','roster_index',*RAW_FIELDS,'effectiveness_region_hex')}|
            {'cache89_8a':None if p['statistics_cache_region_hex'] is None else bytes.fromhex(p['statistics_cache_region_hex'])[9:11].hex()}
            for p in sorted(bound.values(),key=lambda p:p['id'])]
        allstates.append({k:row[k] for k in ('stage','advance_ordinal','tick_before','requested_target','tick','clock','seed','match_version_raw')}|
                         {'players':selected})
        if initial:
            fields=('id','side','roster_index','condition_raw','fatigue_raw','condition_accumulator_raw','sharpness_penalty_raw','effectiveness_region_hex')
            controls[row['stage']]=canonical([{k:p[k] for k in fields} for p in sorted(bound.values(),key=lambda p:p['id'])])
        else:
            description.update({f'finished_{k}_mean':sum(p[k] for p in chosen)/10 for k in RAW_FIELDS})
            description['finished_tf33_distinct_hashes']=len({sha256(bytes.fromhex(p['effectiveness_region_hex'])).hexdigest() for p in chosen})
    need(controls==frozen_controls,'Initial nonsharpness/raw33 frozen controls differ')
    description.update(prepared_tf33_matches_frozen_d00=True,first_tf33_matches_frozen_d00=True)
    need(set(description)==set(DESCRIPTIVE),'Independent descriptive field inventory differs')
    audit.update(input_verified=True,seed_verified=True,sharpness_start_verified=True,stamina60_verified=True,
                 pressing_verified=True,controls_verified=True,sharpness_raw=level,pressing_bit=bit)
    compatible=deepcopy(allstates)
    for stage in compatible:
        for player in stage['players']:
            raw=player['cache89_8a'];player['cache89_8a']=None if raw is None else list(bytes.fromhex(raw))
    return dict(result=result,native_audit=audit,descriptive=description,descriptive_missing_reasons=missing,
                aa_signature_sha256=canonical(dict(result=result,states=allstates)),
                published_raw_state_sha256=canonical(compatible),published_result_sha256=canonical(dict(seed=job['seed'],**result)),
                snapshots_verified=3,actor_stage_observations=138)


def audit_cleanup(proof,process):
    need(proof['schema']==process['schema']=='fm27.contained-call.v1' and proof['cleanup_confirmed'] is True and
         proof['capsule_exit_confirmed'] is True and type(proof['kernel_active_processes']) is int and proof['kernel_active_processes']==0 and
         proof['host_start_permission_sent'] is True and process['membership_verified_before_go'] is True,
         'Kernel-zero/GO/membership receipt missing')
    for value in (proof,process):
        p=value['job_policy'];need(type(p['active_process_limit']) is int and p['active_process_limit']==3 and
            p['limit_flags']==0x2008 and p['kill_on_close'] is True and p['breakaway_allowed'] is False,'Exact Job3 policy required')
    need(proof.get('error_type') is None and number(proof['elapsed_seconds']) and proof['elapsed_seconds']>0,'Contained process error/time unknown')


def audit_concurrency(events,keys):
    claimed=set();completed=set();active=0;peak=0;stopped=False
    for event in events:
        key=event['job_id'];kind=event['event'];utc(event['utc'])
        if kind=='claimed':
            need(not stopped and key in keys and key not in claimed,'Claim after stop/unknown/repeated job');claimed.add(key);active+=1;peak=max(peak,active)
        elif kind=='completed':need(key in claimed and key not in completed,'Unclaimed/repeated completion');completed.add(key);active-=1
        elif kind=='stop':need(not stopped,'Repeated stop event');stopped=True
        else:raise ValueError('Unknown concurrency event')
        need(type(event['active_claims']) is int and event['active_claims']==active and event['peak_claims']==peak and 0<=active<=4,
             'Concurrency claim accounting differs')
    need(not stopped and active==0 and claimed==completed==set(keys),'Incomplete/stopped dispatch')
    return dict(claimed=len(claimed),completed=len(completed),peak_inflight_claims=peak,engine_pid_peak_measured=False)


def audit_budget(state,proof,snapshot_sha,phase,plans):
    phases=['technical'] if phase=='technical' else ['technical','main']
    need(state['experiment']==EXPERIMENT and state['limits']=={'technical':33,'main':512} and state['limit_seconds']==900 and
         state['wall_limit_seconds']==3600 and state['halted'] is False and state['active'] is None and
         not state.get('cleanup_unconfirmed') and not state.get('global_native_lease_retained'),'Own budget state/caps differ')
    ops=state['operations'];need([o['name'] for o in ops]==phases,'Missing/repeated phase operation')
    start=utc(state['wall_start_utc']);deadline=utc(state['wall_deadline_utc']);finish=utc(proof['completed_utc'])
    need(deadline-start==timedelta(seconds=3600) and start<finish<=deadline and finish<=utc('2026-11-14T23:00:00+00:00'),
         'Fixed3600UTC/NIGHT deadline exceeded')
    need(proof['experiment_id']==EXPERIMENT and proof['phase']==phase and proof['budget_sha256']==snapshot_sha,'Parent final budget binding differs')
    reserved={};charged=0.
    for op in ops:
        keys=[j['key'] for j in plans[op['name']]];begin=utc(op['start_utc']);end=utc(op['child_deadline_utc'])
        need(op['kind']==op['name'] and op['keys']==keys and len(set(keys))==len(keys) and type(op['returncode']) is int and
             op['returncode']==0 and op['timed_out'] is False and number(op['elapsed_seconds']) and op['elapsed_seconds']>0 and
             start<=begin<end<=deadline and (end-begin).total_seconds()<=900 and
             (finish-begin).total_seconds()>=op['elapsed_seconds'],'Unsuccessful/unreconciled phase operation')
        charged+=op['elapsed_seconds'];reserved.update({key:op['kind'] for key in keys})
    need(number(state['charged_seconds']) and state['charged_seconds']==charged<=900 and state['reserved']==reserved and
         Counter(reserved.values())==({'technical':33} if phase=='technical' else {'technical':33,'main':512}),'Refunded or exceeded own attempt/time budget')
    return dict(charged_seconds=charged,wall_start_utc=start.isoformat(),wall_deadline_utc=deadline.isoformat(),
                completed_utc=finish.isoformat(),snapshot_sha256=snapshot_sha)


def audit_outer_budget(outer,phase,plans,inner):
    need(outer['experiment']=='NIGHT-001' and outer['limit_seconds']==1800 and outer['active'] is None and
         outer['halted'] is False and outer['absolute_deadline_utc']=='2026-11-14T23:00:00+00:00',
         'Outer NIGHT budget is incomplete/halted or differs')
    need(outer['charged_seconds']==sum(o['elapsed_seconds'] for o in outer['operations'])<=1800,
         'Outer child charge refunded/exceeded')
    need(all(number(o['elapsed_seconds']) and o['elapsed_seconds']>=0 for o in outer['operations']),
         'Outer history contains unknown/negative charge')
    phases=['technical'] if phase=='technical' else ['technical','main'];matched=[]
    for name in phases:
        found=[o for o in outer['operations'] if o['name']==EXPERIMENT+'/'+name]
        need(len(found)==1,'Missing/repeated outer scientific phase');op=found[0]
        keys=[EXPERIMENT+':'+j['key'] for j in plans[name]]
        own=next(o for o in inner['operations'] if o['name']==name)
        need(op['kind']==name and op['keys']==keys and op['returncode']==0 and type(op['returncode']) is int and
             op['timed_out'] is False and number(op['elapsed_seconds']) and op['elapsed_seconds']>=own['elapsed_seconds']>0 and
             all(outer['reserved'].get(k)==name for k in keys) and
             utc(op['start_utc'])<=utc(own['start_utc'])<utc(op['child_deadline_utc'])<=utc(outer['absolute_deadline_utc']),
             'Outer phase reservation/time/return differs')
        matched.append(dict(name=name,elapsed_seconds=op['elapsed_seconds']))
    return dict(global_charged_seconds=outer['charged_seconds'],matched_operations=matched)


def audit_first_main_admission(evidence,inner,outer):
    checked=utc(evidence['checked_utc']);own=next(o for o in inner['operations'] if o['name']=='main')
    i=next(i for i,o in enumerate(outer['operations']) if o['name']==EXPERIMENT+'/main');op=outer['operations'][i]
    prior_own=sum(o['elapsed_seconds'] for o in inner['operations'] if o['name']=='technical')
    prior_global=sum(o['elapsed_seconds'] for o in outer['operations'][:i])
    need(utc(own['start_utc'])<=checked<utc(own['child_deadline_utc']),'First-call check outside main operation')
    remaining=min(900-prior_own,(utc(inner['wall_deadline_utc'])-checked).total_seconds(),
        (utc(op['child_deadline_utc'])-checked).total_seconds(),(utc('2026-11-14T23:00:00+00:00')-checked).total_seconds(),
        1800-prior_global-(checked-utc(op['start_utc'])).total_seconds(),
        (utc(own['child_deadline_utc'])-checked).total_seconds())-5
    need(number(evidence['remaining_seconds']) and evidence['remaining_seconds']>=600 and remaining>=600 and
         abs(evidence['remaining_seconds']-remaining)<1,'First-call own/global600s evidence differs')
    return dict(checked_utc=checked.isoformat(),independently_reconstructed_seconds=remaining)


def safe_public_row(row,job,frozen,receipt):
    allowed={'job_id','seed','status','native_invocation_started','experiment_id','context','team_side','arm','config_sha256',
        'setup_sha256','identity','observer_host_sha256','result','native_audit','descriptive','descriptive_missing_reasons',
        'returncode','native_elapsed_seconds','stdout_sha256','raw_log_sha256','input_dump_sha256','containment_receipt_sha256'}
    need(type(row) is dict and set(row)<=allowed and row['job_id']==job['key'] and row['seed']==job.get('seed') and
         row['native_invocation_started'] is True,'Unknown/private public field or attempt identity')
    need(type(row['returncode']) is int and number(row['native_elapsed_seconds']) and row['native_elapsed_seconds']>0,
         'Native attempt lacks return/time')
    for key in ('stdout_sha256','raw_log_sha256','containment_receipt_sha256'):
        need(type(row[key]) is str and HASH.fullmatch(row[key]),'Public artifact hash malformed')
    if job.get('kind')=='negative':
        need(row['status']=='expected_rejection' and row['returncode']==108 and 'result' not in row,'Negative result/exit differs')
        return
    need(type(row['seed']) is int and type(row['team_side']) is int and
         row['status']=='ok' and row['returncode']==0 and row['experiment_id']==EXPERIMENT and
         row['identity']==frozen['identity'] and row['observer_host_sha256']==HOST and row['context']==job['scenario'] and
         row['team_side']==job['side'] and row['arm']==job['arm'] and
         row['config_sha256']==receipt['config_sha256'] and
         row['setup_sha256']==frozen['setups'][job['scenario']][str(job['side'])][job['arm']],
         'Public fullmatch provenance differs')
    need(set(row['result'])=={'score','tick','clock','team_statistics'} and
         all(set(t)==set(STAT_KEYS) for t in row['result']['team_statistics']), 'Unexpected public result fields')
    result=row['result'];need(len(result['score'])==len(result['team_statistics'])==2,'Public endpoints require two teams')
    for score in result['score']:integer(score,0,100)
    integer(result['tick'],1,47995);integer(result['clock'],0,0x7fffffff)
    for stats in result['team_statistics']:
        need(all(number(v) for v in stats.values()) and stats['xg']>=0 and 0<=stats['shots_on_target']<=stats['shots'] and
             0<=stats['completed_passes']<=stats['passes'] and 0<=stats['possession']<=1,'Malformed public endpoint')
    need(abs(sum(s['possession'] for s in result['team_statistics'])-1)<1e-6,'Public possession sum differs')
    need(set(row['native_audit'])=={'input_verified','seed_verified','sharpness_start_verified','stamina60_verified',
        'pressing_verified','controls_verified','attribute_values_verified','profile_fields_verified',
        'phase_cells_verified','pi_groups_verified','sharpness_raw','pressing_bit'},'Unexpected public audit fields')
    need(set(row['descriptive'])==set(DESCRIPTIVE) and type(row['descriptive_missing_reasons']) is dict,
         'Unexpected public descriptive fields')
    desc=row['descriptive'];missing={k for k,v in desc.items() if v is None}
    need(missing<={'finished_condition_cache89_mean','finished_sharpness_cache8a_mean'} and
         set(row['descriptive_missing_reasons'])==missing and
         all(type(v) is str and v for v in row['descriptive_missing_reasons'].values()),'Public missing observation has no explicit reason')
    for key,value in desc.items():
        if value is None:continue
        if key in ('prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00'):need(value is True,'Public initial raw33 control failed')
        elif key=='finished_tf33_distinct_hashes':integer(value,1,10)
        else:need(number(value),'Nonfinite public descriptive observation')
    need(type(row['input_dump_sha256']) is str and HASH.fullmatch(row['input_dump_sha256']),'Public dump hash malformed')


def audit_phase(central,phase):
    """Requires actual complete private evidence; no autor-summary pass is trusted."""
    need(phase in ('technical','main'),'Explicit actual phase required')
    central=Path(central);public=central/'data/mech-002-sharpness-p0';local=central/'local/mech-002-sharpness-p0'
    prepared=audit_prepared(central)
    frozen=read(public/'inputs.json');seedplan=read(public/'seed-plan.json');receipt=read(public/'manifest.json')
    need(receipt==read(local/'manifest.json'),'Public/private registration differs')
    from analysis.sharpness002_design import validate_design
    validate_design(receipt['config'],executable=True)
    plans={'technical':expected_jobs(seedplan),'main':expected_jobs(seedplan,receipt)}
    for name,jobs in plans.items():need(jobs==read(public/(name+'-job-plan.json')),'Independent phase plan differs')
    plan=plans[phase];directory=local/phase/'dispatch';ledger=read(directory/'ledger.jsonl')
    need(len(ledger)==len(plan)==(33 if phase=='technical' else 512) and len({r['job_id'] for r in ledger})==len(plan),
         'Incomplete/repeated phase: technical status only')
    indexed={r['job_id']:r for r in ledger};need(set(indexed)=={j['key'] for j in plan},'Unknown/missing actual attempt')
    concurrency=audit_concurrency(read(directory/'concurrency.jsonl'),set(indexed))
    need(concurrency['peak_inflight_claims']==4 if phase=='technical' else concurrency['peak_inflight_claims']<=4,
         'Required four-claim technique absent')
    need(not list((local/phase/'jobs').glob('*/pending.json')) and
         not list(directory.glob('*.failure.json')) and not list(directory.glob('*.admission-failure.json')),
         'Unresolved/failed native attempt retained')
    configs=read(local/'configs.json');catalog=read(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json')
    need(file_sha(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json')==frozen['catalog_sha256'],'Native catalog drift')
    artifacts={};signatures={};aa_provenance={};reconstructed=[];projection=[];negative=0
    for job in plan:
        key=job['key'];row=indexed[key];safe_public_row(row,job,frozen,receipt);jobdir=local/phase/'jobs'/key
        paths={'stdout_sha256':jobdir/'native.stdout','raw_log_sha256':jobdir/'native.jsonl',
               'containment_receipt_sha256':jobdir/'native.containment.json'}
        for field,path in paths.items():need(file_sha(path)==row[field],'Actual artifact hash differs')
        cleanup=read(paths['containment_receipt_sha256']);process=read(jobdir/'native.process.json');audit_cleanup(cleanup,process)
        started=read(directory/(key+'.started.json'));admitted=read(directory/(key+'.admitted.json'))
        need(started['job_id']==admitted['job_id']==key and started['seed']==job.get('seed') and
             started['native_invocation_started'] is False and
             utc(started['claimed_utc'])<=utc(process['started_utc'])<=utc(admitted['admitted_utc']),
             'Actual claim/start/GO marker binding differs')
        need(read(jobdir/'native-exit.json')=={k:row[k] for k in ('returncode','native_elapsed_seconds','stdout_sha256',
            'raw_log_sha256','input_dump_sha256','containment_receipt_sha256')},'Actual exit receipt differs')
        artifacts[key]={p.name:file_sha(p) for p in (*paths.values(),jobdir/'native.process.json',jobdir/'native-exit.json')}
        projected=dict(job_id=key,kind='negative' if job.get('kind')=='negative' else 'full',seed=job.get('seed'),
            context=job.get('scenario'),team_side=job.get('side'),arm=job.get('arm'),repeat=job.get('repeat'),
            status=row['status'],returncode=row['returncode'],native_elapsed_seconds=row['native_elapsed_seconds'],
            native_invocation_started=True,claimed_utc=started['claimed_utc'],admitted_utc=admitted['admitted_utc'],
            raw_log_sha256=row['raw_log_sha256'],input_dump_sha256=row.get('input_dump_sha256'),stdout_sha256=row['stdout_sha256'],
            containment_sha256=row['containment_receipt_sha256'],process_receipt_sha256=file_sha(jobdir/'native.process.json'),
            kernel_active_processes=0,cleanup_confirmed=True,process_limit=3,membership_verified_before_go=True)
        evidence=read(paths['raw_log_sha256'])
        if job.get('kind')=='negative':
            rejected=one(evidence,'scenario_rejected')
            need(rejected['stage']=='initial' and not any(r.get('event') in ('native_passive_state','natural_match_finished') for r in evidence),
                 'Negative rejection not initial or generated a match')
            need(file_sha(jobdir/'malformed.bin')==sha256(b'SHARPNESS INVALID HEADER').hexdigest(),'Actual malformed input differs')
            projected.update(input_setup_sha256=file_sha(jobdir/'malformed.bin'),negative_initial_rejection=True,
                scenario_rejected_count=1,natural_finish_count=0,passive_snapshot_count=0)
            projection.append(projected);negative+=1;continue
        dump_path=jobdir/'input.json';need(file_sha(dump_path)==row['input_dump_sha256'],'Native input dump hash differs')
        artifacts[key]['input.json']=file_sha(dump_path);binary=(local/'inputs'/f"{job['scenario']}-{job['side']}-{job['arm']}.bin").read_bytes()
        need(sha256(binary).hexdigest()==row['setup_sha256'],'Actual configuration input differs')
        actual_job=dict(job,identity=frozen['identity']);config=deepcopy(configs[f"{job['scenario']}-{job['side']}"])
        config['teams'][job['side']]['instructions']['10']=2000905329 if job['arm'].endswith('P1') else 1313689463
        actual=audit_raw_match(evidence,read(dump_path),actual_job,binary,config,catalog,frozen['oop_map'],
                               frozen['frozen_controls'][f"{job['scenario']}-{job['side']}"])
        for field in ('result','native_audit','descriptive','descriptive_missing_reasons'):
            need(row[field]==actual[field],'Published measurement differs from independent native reconstruction')
        projected.update(input_setup_sha256=row['setup_sha256'],native_audit=actual['native_audit'],
            stamina_values_verified=46,result=actual['result'],passive_snapshot_count=3,
            raw_state_aa_signature_sha256=actual['aa_signature_sha256'])
        projection.append(projected)
        signatures[key]=actual['aa_signature_sha256'];aa_provenance[key]=actual;reconstructed.append(row)
    aa=0
    if phase=='technical':
        for h,s,a in product(CONTEXTS,(0,1),ARMS):
            prefix=f'tech-{h}-s{s}-{a}-r';need(signatures[prefix+'0']==signatures[prefix+'1'],'Actual raw-state/result A/A differs');aa+=1
        need(aa==16 and negative==1,'Technical A/A/negative coverage differs')
    state=read(local/(phase+'-budget.snapshot.json'));proof=read(local/(phase+'-reconciled.json'))
    own=audit_budget(state,proof,file_sha(local/(phase+'-budget.snapshot.json')),phase,plans)
    outer_state=read(central/'local/night-001/program-budget.json');outer=audit_outer_budget(outer_state,phase,plans,state)
    need(not (central/'local/global-native/native-execution.lease.json').exists(),'Global native lease still retained/active')
    publicrows=read(public/('technical.jsonl' if phase=='technical' else 'main.jsonl'))
    need(publicrows==[r for r in ledger if r['status']=='ok'],'Published allowed measurement subset differs')
    accounting=read(public/(phase+'-job-accounting.jsonl'))
    need(len(accounting)==len(plan) and all(r==dict(job_id=j['key'],seed=j.get('seed'),
        status='expected_rejection' if j.get('kind')=='negative' else 'ok',admission_error_type=None)
        for r,j in zip(accounting,plan,strict=True)),'Incomplete/changed public failure accounting')
    summary=read(public/(phase+'-summary.json'));public_budget=read(public/(phase+'-budget.json'))
    need(summary['passed'] is True and summary['budget_reconciled'] is True and summary['complete'] is True and
         summary['full_matches']==len(reconstructed) and summary['negative_rejections']==negative and
         summary['peak_inflight_claims']==concurrency['peak_inflight_claims'] and summary['engine_pid_peak_measured'] is False and
         summary['dispatch_summary_sha256']==file_sha(directory/'dispatch-summary.json') and
         summary['concurrency_ledger_sha256']==file_sha(directory/'concurrency.jsonl'),
         'Published summary disagrees with independently reconstructed raw evidence')
    need(public_budget['passed'] is True and public_budget['charged_seconds']==own['charged_seconds'] and
         public_budget['budget_sha256']==own['snapshot_sha256'] and public_budget['limits']=={'technical':33,'main':512} and
         public_budget['limit_seconds']==900 and public_budget['wall_limit_seconds']==3600,'Public/private budget differs')
    if phase=='technical':
        expected_aa=[]
        for h,s,a in product(CONTEXTS,(0,1),ARMS):
            proof=aa_provenance[f'tech-{h}-s{s}-{a}-r0']
            expected_aa.append(dict(context=h,side=s,arm=a,exact_outcomes_and_identified_fields_equal=True,
                raw_state_sha256=proof['published_raw_state_sha256'],result_sha256=proof['published_result_sha256']))
        need(sorted(summary['aa_pairs'],key=lambda r:(r['context'],r['side'],r['arm']))==
             sorted(expected_aa,key=lambda r:(r['context'],r['side'],r['arm'])),'Published A/A provenance differs from independent raw states')
    admission=None
    if phase=='main':admission=audit_first_main_admission(read(local/'main-summary.json')['first_main_admission'],state,outer_state)
    return dict(phase=phase,actual_raw_evidence_verified=True,native_start_authorized=False,
        inputs_sha256=prepared['inputs_sha256'],
        full_matches=len(reconstructed),negative_rejections=negative,aa_pairs=aa,
        snapshots=3*len(reconstructed),actor_stage_observations=138*len(reconstructed),
        attribute_values_verified=3174*len(reconstructed),profile_values_verified=1058*len(reconstructed),
        phase_cells_verified=44*len(reconstructed),pi_groups_verified=748*len(reconstructed),
        concurrency=concurrency,budget=own,outer_budget=outer,first_main_admission=admission,
        private_artifact_manifest_sha256=canonical(artifacts),
        technical_evidence_projection=projection if phase=='technical' else None,reviewer_native_starts=0)


def audit_public(central,phase):
    """Portable QA only; cannot prove private native readbacks or parent budgets."""
    need(phase in ('technical','main'),'Explicit public phase required')
    public=Path(central)/'data/mech-002-sharpness-p0';frozen=read(public/'inputs.json')
    seedplan=read(public/'seed-plan.json');receipt=read(public/'manifest.json');plan=expected_jobs(seedplan,None if phase=='technical' else receipt)
    need(read(public/(phase+'-job-plan.json'))==plan,'Public independently reconstructed job plan differs')
    data=read(public/('technical.jsonl' if phase=='technical' else 'main.jsonl'))
    expected={j['key']:j for j in plan if j.get('kind')!='negative'}
    need(len(data)==len(expected)==(32 if phase=='technical' else 512) and
         len({r['job_id'] for r in data})==len(data) and {r['job_id'] for r in data}==set(expected),
         'Public incomplete/repeated seed blocks: no effect estimates')
    for row in data:
        safe_public_row(row,expected[row['job_id']],frozen,receipt)
        audit=row['native_audit'];level=7000 if row['arm'].startswith('S70-') else 10000;bit=66 if row['arm'].endswith('P1') else 0
        need(all(audit[k] is True for k in ('input_verified','seed_verified','sharpness_start_verified','stamina60_verified','pressing_verified','controls_verified')) and
            all(type(audit[k]) is int and audit[k]==v for k,v in (('attribute_values_verified',3174),('profile_fields_verified',1058),
            ('phase_cells_verified',44),('pi_groups_verified',748),('sharpness_raw',level),('pressing_bit',bit))),
            'Public declared native audit missing/wrong')
    result=dict(public_subset_verified=True,private_raw_evidence_verified=False,
        native_start_authorized=False,phase=phase,match_rows=len(data),reviewer_native_starts=0)
    if phase=='technical':
        result['independent_33_job_projection']=audit_public_projection(
            read(public/'technical-evidence-review.json'),data,plan,file_sha(public/'inputs.json',True))
    if phase=='main':
        result.update(verify_stored_analysis(data,receipt,read(public/'effects.json'),read(public/'seed-contrasts.jsonl')))
        provenance=read(public/'analysis-provenance.json')
        need(provenance['experiment_id']==EXPERIMENT and provenance['native_starts_by_analysis']==0 and
             provenance['analysis']=='analysis/analyse_sharpness002.py','Analysis provenance identity differs')
        need(set(provenance['source_and_input_sha256'])=={'analysis/analyse_sharpness002.py',
            'data/mech-002-sharpness-p0/main.jsonl','data/mech-002-sharpness-p0/manifest.json',
            'data/mech-002-sharpness-p0/main-summary.json'} and
            file_sha(Path(central)/'analysis/analyse_sharpness002.py',True)==receipt['config']['preregistration']['analysis_sha256'],
            'Complete original registered analysis source binding required')
        for name,wanted in provenance['source_and_input_sha256'].items():
            need(name in ('analysis/analyse_sharpness002.py','data/mech-002-sharpness-p0/main.jsonl',
                'data/mech-002-sharpness-p0/manifest.json','data/mech-002-sharpness-p0/main-summary.json') and
                file_sha(Path(central)/name,True)==wanted,'Analysis input/source provenance hash differs')
        need(set(provenance['output_sha256'])=={'effects.json','seed-contrasts.jsonl'} and
             all(file_sha(public/name,True)==wanted for name,wanted in provenance['output_sha256'].items()),
             'Stored analysis output hash differs')
        result['stored_analysis_provenance_verified']=True
    return result


def compare_numbers(got,wanted,label):
    if type(wanted) is bool:need(got is wanted,'Stored Boolean differs: '+label)
    elif type(wanted) in (list,tuple):
        need(type(got) in (list,tuple) and len(got)==len(wanted),'Stored analysis list differs: '+label)
        for a,b in zip(got,wanted):compare_numbers(a,b,label)
    elif wanted is None:need(got is None,'Stored undefined statistic differs: '+label)
    else:need(number(got) and number(wanted) and math.isclose(got,wanted,rel_tol=1e-10,abs_tol=1e-12),
              'Stored analysis value differs: '+label)


def independent_planning(sd):
    """Independent linear integer search, not the author's binary-search planner."""
    from scipy.stats import chi2,nct,t
    need(len(sd)==2 and all(number(s) and s>=0 for s in sd),'Two finite planning SDs required')
    result={}
    for key,factor in (('observed',1.),('simultaneous95_sd_upper',math.sqrt(31/chi2.ppf(.025,31)))):
        values=[s*factor for s in sd];plans=[]
        for effect in (.2,.3):
            for n in range(2,10000001):
                parts=[s*s/(4*n) for s in values];variance=sum(parts)
                if variance==0:width=0.;power=1.
                else:
                    se=math.sqrt(variance);df=variance**2/sum(p*p/(n-1) for p in parts)
                    cut=t.ppf(.975,df);width=2*cut*se;shift=effect/se
                    power=float(nct.cdf(-cut,df,shift)+nct.sf(cut,df,shift))
                if power>=.9:break
            else:raise ValueError('Independent conditional planning exceeds search budget')
            plans.append(dict(effect=effect,seeds_per_context=n,independent_blocks=2*n,matches=16*n,
                              full_width=float(width),power=power))
        result[key]=dict(sd=values,power90=plans)
    return result


def verify_stored_analysis(data,receipt,effects,blocks):
    """Recompute all stored effects/blocks from raw scores/xG, without analyse()."""
    from statistics import fmean,variance
    from scipy.stats import chi2
    from analysis.review_sharpness002_science import independently_group,independently_summarize,independently_holm,FAMILY,raw_metrics,BOOT_SEED
    need(len(data)==512 and effects['experiment_id']==EXPERIMENT and effects['n_matches']==512 and
         effects['independent_seed_blocks']==64 and effects['primary_contrast']=='SHARPNESS' and
         set(effects['secondary'])==set(FAMILY),'Stored result endpoints/sample differs')
    need(effects['bootstrap']==dict(seed=BOOT_SEED,resamples=20000) and effects['practical_reference']==.3 and
         effects['desired_full_ci_width']==.5 and effects['exploratory_context_and_side_only'] is True and
         all(effects[k] is False for k in ('ui_scale_calibrated','consumer_semantics_validated','mediation_identified',
             'career_transfer_confirmed','winner_selected')),'Stored interpretation/preregistered settings drift')
    grouped=independently_group(data,receipt)
    independent={key:independently_summarize(grouped[key]) for key in ('SHARPNESS:xgd',*FAMILY)}
    published={'SHARPNESS:xgd':effects['primary'],**effects['secondary']}
    holm=independently_holm({key:independent[key]['p'] for key in FAMILY})
    expected_blocks=[]
    for key,wanted in independent.items():
        got=published[key];name,endpoint=key.split(':')
        for field in ('mean','se','df','p','ci','bootstrap_ci'):compare_numbers(got[field],wanted[field],key+'/'+field)
        need(got['n_seed_blocks']==64 and got['n_scenarios']==2 and got['alpha']==.05,'Stored uncertainty sample/alpha differs')
        compare_numbers(got['leave_one_out']['range'],wanted['loo_range'],key+'/LOO range')
        compare_numbers(got['leave_one_out']['max_change'],wanted['loo_change'],key+'/LOO change')
        for h,context in enumerate(CONTEXTS):
            own=grouped[key][h];values=own['blocks'];a,b=own['sides'];actual=got['context'][context]
            context_expected=dict(mean=fmean(values),sd=math.sqrt(variance(values)),
                sd_upper95_normal_model=math.sqrt(variance(values))*math.sqrt(31/chi2.ppf(.05,31)),
                side0_mean=fmean(a),side1_mean=fmean(b),side0_sd=math.sqrt(variance(a)),side1_sd=math.sqrt(variance(b)),
                side_covariance=wanted['side_covariance'][h])
            for field,value in context_expected.items():compare_numbers(actual[field],value,key+'/'+context+'/'+field)
            for i,value in enumerate(values):expected_blocks.append(dict(context=context,seed=receipt['seeds'][h*32+i],contrast=name,endpoint=endpoint,value=value))
        if key in FAMILY:
            compare_numbers(got['p_holm'],holm[key],key+'/Holm')
            need(got['reject_holm'] is (holm[key]<=.05),'Stored Holm decision differs')
    need(len(blocks)==len(expected_blocks)==512,'Stored derived block count differs')
    for actual,wanted in zip(blocks,expected_blocks,strict=True):
        need(set(actual)==set(wanted) and all(actual[k]==wanted[k] for k in ('context','seed','contrast','endpoint')),
             'Stored derived block identity/order differs')
        compare_numbers(actual['value'],wanted['value'],'derived seed contrast')
    planning=independent_planning(independent['SHARPNESS:xgd']['context_sd'])
    for key,value in planning.items():
        compare_numbers(effects['planning'][key]['sd'],value['sd'],'planning/'+key+'/SD')
        need(len(effects['planning'][key]['power90'])==2,'Stored planning effect family differs')
        for actual,wanted in zip(effects['planning'][key]['power90'],value['power90'],strict=True):
            for field in ('effect','full_width','power'):compare_numbers(actual[field],wanted[field],'planning/'+field)
            need(all(type(actual[k]) is int and actual[k]==wanted[k] for k in ('seeds_per_context','independent_blocks','matches')),
                 'Stored independent confirmation block/match cost differs')
    for context,arm in product(CONTEXTS,ARMS):
        selected=[r for r in data if r['context']==context and r['arm']==arm];need(len(selected)==64,'Stored arm descriptive denominator differs')
        metrics=[raw_metrics(r) for r in selected]
        for endpoint in metrics[0]:compare_numbers(effects['arm_means'][context][arm][endpoint],fmean(m[endpoint] for m in metrics),context+'/'+arm+'/'+endpoint)
        for field in DESCRIPTIVE:
            observed=[r['descriptive'][field] for r in selected if r['descriptive'][field] is not None]
            missing=Counter(r['descriptive_missing_reasons'][field] for r in selected if r['descriptive'][field] is None)
            got=effects['descriptive']['by_context_arm'][context][arm][field]
            need(got['observed']==len(observed) and got['missing']==sum(missing.values()) and got['missing_reasons']==dict(missing),
                 'Stored descriptive observation/missing accounting differs')
            for name,value in (('mean',fmean(observed) if observed else None),('min',min(observed) if observed else None),('max',max(observed) if observed else None)):
                compare_numbers(got[name],value,'descriptive/'+field+'/'+name)
    return dict(independent_seed_blocks=64,stored_effects_and_512_derived_blocks_verified=True,
        independent_contrasts=independent,independent_secondary_holm=holm,independent_conditional_planning=planning,
        interpretation='Independent raw-score/xG reconstruction; total two-field package effect in this fixed synthetic context only. No new execution.')


def audit_public_projection(evidence,measurements,plan,inputs_sha256):
    """Public consistency/negative-control QA; no substitute for private raw proof."""
    need(evidence['schema']=='fm27.sharpness002.independent-technical-evidence.v1' and evidence['experiment_id']==EXPERIMENT and
         evidence['summary']['inputs_sha256']==inputs_sha256 and len(evidence['jobs'])==33,'Public independent projection identity/count differs')
    rows={r['job_id']:r for r in measurements};need(len(rows)==32,'Exactly32 public success rows required')
    common={'job_id','kind','seed','context','team_side','arm','repeat','status','returncode','native_elapsed_seconds',
        'native_invocation_started','claimed_utc','admitted_utc','raw_log_sha256','input_dump_sha256','stdout_sha256',
        'containment_sha256','process_receipt_sha256','kernel_active_processes','cleanup_confirmed','process_limit',
        'membership_verified_before_go','input_setup_sha256'}
    signatures={};negative=0
    for job,actual in zip(plan,evidence['jobs'],strict=True):
        full=job.get('kind')!='negative';extra={'native_audit','stamina_values_verified','result','passive_snapshot_count','raw_state_aa_signature_sha256'} if full else {
            'negative_initial_rejection','scenario_rejected_count','natural_finish_count','passive_snapshot_count'}
        need(set(actual)==common|extra and actual['job_id']==job['key'] and actual['seed']==job.get('seed') and
             actual['context']==job.get('scenario') and actual['team_side']==job.get('side') and actual['arm']==job.get('arm') and
             actual['repeat']==job.get('repeat') and actual['kind']==('full' if full else 'negative'),
             'Unexpected/private public projection field or job identity')
        for key in ('raw_log_sha256','stdout_sha256','containment_sha256','process_receipt_sha256','input_setup_sha256'):
            need(type(actual[key]) is str and HASH.fullmatch(actual[key]),'Malformed public projection hash')
        need(actual['native_invocation_started'] is True and actual['membership_verified_before_go'] is True and
             actual['cleanup_confirmed'] is True and type(actual['kernel_active_processes']) is int and actual['kernel_active_processes']==0 and
             type(actual['process_limit']) is int and actual['process_limit']==3 and utc(actual['claimed_utc'])<=utc(actual['admitted_utc']) and
             number(actual['native_elapsed_seconds']) and actual['native_elapsed_seconds']>0,'Public process/claim/cleanup proof differs')
        if not full:
            need(actual['status']=='expected_rejection' and type(actual['returncode']) is int and actual['returncode']==108 and
                 actual['negative_initial_rejection'] is True and actual['scenario_rejected_count']==1 and
                 actual['natural_finish_count']==actual['passive_snapshot_count']==0 and actual['input_dump_sha256'] is None and
                 actual['input_setup_sha256']==sha256(b'SHARPNESS INVALID HEADER').hexdigest(),'Public negative108/no-match proof differs')
            negative+=1;continue
        row=rows[job['key']]
        need(actual['status']=='ok' and type(actual['returncode']) is int and actual['returncode']==0 and actual['stamina_values_verified']==46 and
             actual['passive_snapshot_count']==3 and actual['result']==row['result'] and actual['native_audit']==row['native_audit'] and
             actual['input_dump_sha256']==row['input_dump_sha256'] and actual['input_setup_sha256']==row['setup_sha256'] and
             actual['containment_sha256']==row['containment_receipt_sha256'] and actual['raw_log_sha256']==row['raw_log_sha256'] and
             actual['stdout_sha256']==row['stdout_sha256'],'Public success/projection cross-binding differs')
        need(type(actual['raw_state_aa_signature_sha256']) is str and HASH.fullmatch(actual['raw_state_aa_signature_sha256']),
             'Malformed public A/A signature')
        signatures[job['key']]=actual['raw_state_aa_signature_sha256']
    for h,s,a in product(CONTEXTS,(0,1),ARMS):
        key=f'tech-{h}-s{s}-{a}-r';need(signatures[key+'0']==signatures[key+'1'],'Public paired A/A signature differs')
    need(negative==1,'Public negative not accounted')
    return dict(jobs_verified=33,full_matches=32,negative_initial108=1,aa_pairs=16,
                private_raw_evidence_verified_by_this_public_check=False)


def audit_resource_plan(central):
    central=Path(central);public=central/'data/mech-002-sharpness-p0';local=central/'local/mech-002-sharpness-p0'
    plan=read(public/'resource-admission-plan.json');jobs=read(public/'technical-job-plan.json')
    events=read(local/'technical/dispatch/concurrency.jsonl');data=read(public/'technical.jsonl');budget=read(local/'technical-budget.snapshot.json')
    blocks=[]
    for context,side in product(CONTEXTS,(0,1)):
        keys={j['key'] for j in jobs if j.get('scenario')==context and j.get('side')==side}
        selected=[e for e in events if e['job_id'] in keys]
        begin=min(utc(e['utc']) for e in selected if e['event']=='claimed')
        end=max(utc(e['utc']) for e in selected if e['event']=='completed')
        need(len(keys)==8 and len(selected)==16,'Runtime planning lacks complete raw eight-job blocks')
        blocks.append(dict(context=context,team_side=side,full_jobs=8,elapsed_seconds=(end-begin).total_seconds()))
    dispatch=(max(utc(e['utc']) for e in events if e['event']=='completed')-
              min(utc(e['utc']) for e in events if e['event']=='claimed')).total_seconds()
    overhead=budget['charged_seconds']-dispatch;cold=max(r['native_elapsed_seconds'] for r in data)
    prediction=64*max(b['elapsed_seconds'] for b in blocks)+overhead+cold+90
    need(plan['experiment_id']==EXPERIMENT and plan['kind']=='administrative_runtime_projection_only' and
        plan['observed_technical_blocks']==blocks and plan['main_blocks']==64 and plan['own_cumulative_limit_seconds']==900 and
        plan['fixed_main_minimum_seconds']==600 and plan['contingency_seconds']==90 and
        plan['own_wall_deadline_utc']==budget['wall_deadline_utc'] and plan['night_wall_deadline_utc']=='2026-11-14T23:00:00+00:00',
        'Runtime projection scope, raw block sources or unchanged limits differ')
    for field,value in (('technical_dispatcher_seconds',dispatch),('technical_own_charge_seconds',budget['charged_seconds']),
        ('source_and_phase_overhead_seconds',overhead),('first_main_serial_call_allowance_seconds',cold),
        ('projected_main_seconds',prediction),('own_remaining_after_technical_seconds',900-budget['charged_seconds'])):
        need(number(plan[field]) and math.isclose(plan[field],value,rel_tol=1e-12,abs_tol=1e-9),'Runtime projection arithmetic differs')
    for name,digest in plan['evidence_sha256'].items():
        need(name in ('technical.jsonl','technical-budget.json','technical-summary.json') and file_sha(public/name,True)==digest,
             'Runtime projection evidence hash differs')
    return dict(projected_main_seconds=prediction,own_remaining_seconds=900-budget['charged_seconds'],
        stricter_utc_deadline=min(utc(plan['own_wall_deadline_utc']),utc(plan['night_wall_deadline_utc'])).isoformat(),
        guaranteed_upper_bound=False,unchanged_minimum_admission_seconds=600,
        source_sha256=file_sha(public/'resource-admission-plan.json',True))


def verify_publication(central,commit,ci,paths):
    """Only git/gh read requests, no engine/native process API."""
    need(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit) and type(ci) is int and ci>0,'Exact commit/CI run required')
    central=Path(central)
    for name in paths:
        path=(central/name).resolve();need(central.resolve() in path.parents,'Publication path escaped archive')
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=central)
        need(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==file_sha(path,True),'Published source/artifact differs')
    run=json.loads(subprocess.check_output(['gh','api',f'repos/Matchekk/FM-27-Research/actions/runs/{ci}'],cwd=central,text=True))
    need(run['head_sha']==commit and run['status']=='completed' and run['conclusion']=='success','Actual exact publication CI not successful')
    return dict(publication_commit=commit,ci_run=ci,ci_verified=True,
                ci_completed_utc=utc(run['updated_at']).isoformat(),source_blobs_verified=len(paths))


def technical_evidence(central):
    central=Path(central);public=central/'data/mech-002-sharpness-p0'
    result=audit_phase(central,'technical');jobs=result.pop('technical_evidence_projection')
    proof=read(central/'local/mech-002-sharpness-p0/technical-reconciled.json');frozen=read(public/'inputs.json')
    paths=[*frozen['code_sha256'],'docs/night-001/SHARPNESS-REVIEW.md',*[f'data/mech-002-sharpness-p0/{n}'
        for n in ('contract.json','inputs.json','seed-plan.json','review-gate.json','manifest.json','main-job-plan.json','technical-job-plan.json')]]
    publication=verify_publication(central,proof['publication_commit'],proof['ci_run'],paths)
    need(utc(publication['ci_completed_utc'])<min(utc(j['claimed_utc']) for j in jobs),
         'Exact successful publication CI did not precede every technical claim')
    output=dict(schema='fm27.sharpness002.independent-technical-evidence.v1',experiment_id=EXPERIMENT,
        publication=publication,summary=result,resource_plan_review=audit_resource_plan(central),jobs=jobs)
    audit_public_projection(output,read(public/'technical.jsonl'),read(public/'technical-job-plan.json'),result['inputs_sha256'])
    return output


def main_evidence(central):
    """Final evidence only; never grants execution or creates a new study."""
    central=Path(central);public=central/'data/mech-002-sharpness-p0';local=central/'local/mech-002-sharpness-p0'
    raw=audit_phase(central,'main');raw.pop('technical_evidence_projection')
    analysis=audit_public(central,'main');frozen=read(public/'inputs.json');proof=read(local/'main-reconciled.json')
    release=read(public/'technical-release.json')
    need(release['approved_for_main'] is True and release['experiment_id']==EXPERIMENT and
        release['summary_sha256']==file_sha(public/'technical-summary.json',True) and
        release['review_sha256']==file_sha(central/'docs/night-001/SHARPNESS-TECHNICAL-REVIEW.md',True) and
        release['evidence_projection_sha256']==file_sha(public/'technical-evidence-review.json',True) and
        release['resource_admission_plan_sha256']==file_sha(public/'resource-admission-plan.json',True) and
        release['duplicate_preflight_sha256']==file_sha(public/'duplicate-preflight.json',True) and
        release['duplicate_review_sha256']==file_sha(central/'docs/night-001/SHARPNESS-DUPLICATE-REVIEW.md',True),
        'Actual main release/preflight bindings differ')
    paths=[*frozen['code_sha256'],*[f'data/mech-002-sharpness-p0/{name}' for name in (
        'contract.json','inputs.json','seed-plan.json','review-gate.json','manifest.json','main-job-plan.json','technical-job-plan.json',
        'technical-release.json','technical-summary.json','technical-budget.json','technical-job-accounting.jsonl',
        'technical-evidence-review.json','resource-admission-plan.json','duplicate-preflight.json')],
        *[f'docs/night-001/{name}' for name in ('SHARPNESS-REVIEW.md','SHARPNESS-TECHNICAL-REVIEW.md',
            'SHARPNESS-DUPLICATE-PREFLIGHT.md','SHARPNESS-DUPLICATE-REVIEW.md')]]
    publication=verify_publication(central,proof['publication_commit'],proof['ci_run'],paths)
    state=read(local/'main-budget.snapshot.json');main_start=next(o['start_utc'] for o in state['operations'] if o['name']=='main')
    need(utc(publication['ci_completed_utc'])<utc(main_start),'Successful exact CI did not precede main phase')
    complete=read(public/'complete-job-accounting.jsonl');expected=[]
    for phase in ('technical','main'):
        expected.extend(dict(phase=phase,**row) for row in read(public/(phase+'-job-accounting.jsonl')))
    # The director's harmless aggregate may order the added phase field anywhere.
    need(complete==expected and len(complete)==545 and Counter(r['status'] for r in complete)==
         {'ok':544,'expected_rejection':1},'Complete545 failure accounting differs')
    return dict(schema='fm27.sharpness002.independent-main-evidence.v1',experiment_id=EXPERIMENT,
        publication=publication,raw_evidence=raw,independent_public_analysis=analysis,
        complete_job_accounting_sha256=file_sha(public/'complete-job-accounting.jsonl',True),
        total_planned_jobs=545,successful_full_matches=544,expected_rejections=1,unexpected_failures=0,unbegun=0,
        native_execution_authorized=False,new_study_authorized=False,reviewer_native_starts=0)


def main():
    from argparse import ArgumentParser
    parser=ArgumentParser(description=__doc__);parser.add_argument('stage',choices=('seeds','inputs','technical','main','technical-evidence','main-evidence','public-technical','public-main'))
    parser.add_argument('--central',type=Path,default=ROOT);args=parser.parse_args();central=args.central.resolve()
    if args.stage=='seeds':
        excluded,count=reconstruct_exclusions(central);result=audit_seed_plan(read(central/'local/registry'/f'{EXPERIMENT}.reserved.json'),excluded)
        result.update(seed_source_files_read=count,reviewer_native_starts=0,native_start_authorized=False)
    elif args.stage=='inputs':result=audit_prepared(central)
    elif args.stage=='technical-evidence':result=technical_evidence(central)
    elif args.stage=='main-evidence':result=main_evidence(central)
    elif args.stage.startswith('public-'):result=audit_public(central,args.stage.removeprefix('public-'))
    else:result=audit_phase(central,args.stage)
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__=='__main__':main()

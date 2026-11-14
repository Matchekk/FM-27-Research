"""Two explicit read-only reader profiles and a Windows hard memory job.

Importing this module never imports fmsave or opens any game data.
"""
from dataclasses import is_dataclass
from hashlib import sha256
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import sys

from .career_readonly004 import PROBES, section_summary, summarize_probe

VERSION='career-readonly-profiles-v1'
MEMORY_BYTES=3*1024**3
WALL_SECONDS=180
EXPECTED_SNAPSHOT='1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d'
WHEEL_SHA='2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa'
RELEASE_COMMIT='e0704bc5d7e6bf687fecf85cd48b28c497bdef68'
PROFILE_V10='fm27-save-2486695-2503222-v10'
PROFILES=('R1','R2')
SAFE_CODE=re.compile(r'[A-Za-z0-9_:.+-]{1,100}\Z')


def require(ok,message):
    if not ok:raise ValueError(message)


def file_hash(path, normalized=False):
    raw=Path(path).read_bytes()
    return sha256(raw.replace(b'\r\n',b'\n') if normalized else raw).hexdigest()


def tree_hashes(directory):
    directory=Path(directory)
    return {p.relative_to(directory).as_posix():file_hash(p)
            for p in sorted(directory.rglob('*.py'))}


def public_checks(check):
    if check is None:return None
    require(SAFE_CODE.fullmatch(check.reader),'Unsafe reader code')
    require(type(check.record_count) is int and check.record_count>=0,'Invalid record count')
    gates=[]
    for g in check.gates:
        require(SAFE_CODE.fullmatch(g.name),'Unsafe gate code')
        values={k:getattr(g,k) for k in ('observed','minimum','maximum')}
        require(all(v is None or type(v) in (int,float) and math.isfinite(v) for v in values.values()),'Nonnumeric gate')
        gates.append(dict(code=g.name,**values,passed=bool(g.passed),applied=bool(g.applied),
                          advisory=bool(getattr(g,'advisory',False))))
    require(all(SAFE_CODE.fullmatch(k) and type(v) is int for k,v in check.anomalies.items()),'Unsafe anomaly')
    return dict(reader=check.reader,record_count=check.record_count,gates=gates,
                anomalies=dict(check.anomalies),native_semantics_verified=False)


def current_checks(save, name, error=None):
    if error is not None:
        return [public_checks(c) for c in getattr(error,'checks',())]
    check=save._reader_check(name)
    return [] if check is None else [public_checks(check)]


def layout_claim(save,name):
    getter=getattr(save,'_reader_layout',None)
    value=getter(name) if getter else None
    if value is None:return None
    # Pinned0.12.4's private diagnostic record, not a raw offset proof.
    return dict(region=value.region,source_build=value.build,source_schema=value.schema,
                save_schema=value.save_schema)


def load_profile(profile,runtime_source,isolated_site):
    require(profile in PROFILES,'Unknown reader profile')
    require(not any(k=='fmsave' or k.startswith('fmsave.') for k in sys.modules),
            'Reader profiles require a fresh interpreter')
    trace=dict(summary_calls=0,draft_fallback_calls=0,draft_fallback_accepted=0,
               draft_fallback_exceptions=0)
    if profile=='R1':
        runtime_source=Path(runtime_source)
        sys.path.insert(0,str(runtime_source));sys.path.insert(0,str(runtime_source/'vendor'))
        draft=importlib.import_module('desktop_save_draft')
        original=draft.read_summary
        def observed_draft(container):
            trace['draft_fallback_calls']+=1
            try:value=original(container)
            except Exception:
                trace['draft_fallback_exceptions']+=1;raise
            trace['draft_fallback_accepted']+=int(value is not None)
            return value
        draft.read_summary=observed_draft
        compat=importlib.import_module('desktop_save_compat')
        require(compat.PROFILE==PROFILE_V10,'Runtime compatibility profile drift')
        compat.install()
        module=importlib.import_module('fmsave')
        version=importlib.import_module('fmsave._version')
        summary=version.read_summary_facts
        def observed_summary(container):
            trace['summary_calls']+=1
            return summary(container)
        version.read_summary_facts=observed_summary
    else:
        sys.path.insert(0,str(isolated_site))
        module=importlib.import_module('fmsave')
        require(module.__version__=='0.12.4','Isolated reader version drift')
        require(Path(module.__file__).resolve().is_relative_to(Path(isolated_site).resolve()),
                'R2 imported the base reader')
    require(not any(k in sys.modules for k in ('fm27_tactics_server','desktop_engine','desktop_host')),
            'Unexpected native runtime import')
    return module,trace


def coverage(name,value,context,info):
    result=section_summary(info) if name=='open' else summarize_probe(name,value,context,info)
    if name=='injuries':
        rows=list(value);uid=context.get('managed_uid');cohort=context.get('managed_players')
        result.pop('managed_injury_records',None);result.pop('record_kinds',None)
        result['historical_managed_club_records']=sum(
            getattr(getattr(r,'kind',None),'name',None)=='HISTORY' and r.club_uid==uid
            for r in rows) if uid is not None else None
        result['typed_current_cohort_records']=sum(
            getattr(getattr(r,'kind',None),'name',None)=='TYPED' and r.player_uid in cohort
            for r in rows) if cohort is not None else None
    result['native_semantics_verified']=False
    return result


def compare_reports(first,second,first_bindings,second_bindings):
    require(first['snapshot_sha256']==second['snapshot_sha256']==EXPECTED_SNAPSHOT,
            'Cross-reader reports are not bound to the same immutable snapshot')
    require(first['profile']=='R1' and second['profile']=='R2','Cross-reader profile order differs')
    require(first.get('snapshot_stable') is True and second.get('snapshot_stable') is True,
            'Unstable or unverified snapshot cannot enter cross-reader comparison')
    a={r['probe']:r for r in first['probes']};b={r['probe']:r for r in second['probes']}
    fields={'open':('game','save_build','game_date_claim','time_slot_raw','sections'),
            'managed_clubs':('rows','single_managed_club','manager_identity_resolved'),
            'clubs':('rows','managed_team_capacity'),
            'players':('rows','managed_squad_records','attribute_pair_coverage'),
            'training':('rows','teams'),
            'injuries':('rows','historical_managed_club_records','typed_current_cohort_records')}
    comparisons=[]
    for name in PROBES:
        for key in fields.get(name,('rows',)):
            observed=lambda row:row.get('status') in ('observed','observed_with_warnings')
            av=a[name].get('coverage',{}).get(key);bv=b[name].get('coverage',{}).get(key)
            available=observed(a[name]) and observed(b[name]) and av is not None and bv is not None
            comparisons.append(dict(field=f'{name}.{key}',
                status='same_parsed_value' if available and av==bv else
                       'different_parsed_value' if available else 'not_comparable_unavailable',
                first=av if available else None,second=bv if available else None,
                native_verified=False))
    bindings={}
    for key in ('managed_uid','team_ids','managed_players'):
        av=first_bindings.get(key);bv=second_bindings.get(key)
        bindings[key]='same_private_binding' if av is not None and bv is not None and av==bv else \
                      'different_private_binding' if av is not None and bv is not None else 'unavailable'
    return dict(kind='same_bytes_cross_reader_diagnostic_not_independent_replicates',
        snapshot_sha256=EXPECTED_SNAPSHOT,fields=comparisons,private_binding_comparison=bindings,
        source_snapshots=1,independent_treatment_replicates_verified=None,
        native_semantics_verified=False,career_advance_released=False)


def field_contract():
    return {
      'open.save_build':dict(unit='last_writer_build_string',source='fmsave._version.find_game_version',native_verified=False),
      'open.game_date_claim':dict(unit='parser_claimed_ISO_date',source='fmsave._version.read_save_info;R1 summary fallback trace',native_verified=False),
      'open.sections':dict(unit='schema_and_byte_counts',source='fmsave._container.read_index;fmsave._version.section_schema',native_verified=False),
      'coverage.rows':dict(unit='decoded_records',source='len(fmsave.Table)',native_verified=False),
      'coverage.record_fields':dict(unit='parser_model_field_names',source='dataclass field inventory, no field values',native_verified=False),
      'managed_clubs':dict(unit='decoded_record_count_and_resolution_count',source='ManagedClub.club_uid/manager_staff_uid; IDs private',native_verified=False),
      'players.managed_squad_records':dict(unit='decoded_records_joined_by_stored_team_id',source='Player.team_id joined to Club.teams.team_id; IDs private',native_verified=False),
      'players.attribute_pair_coverage':dict(unit='parser_raw_and_parser_display_range',source='fmsave.models.players.Player raw_attributes/attributes',native_verified=False),
      'training.raw_session_counts':dict(unit='stored_raw_session_code_count',source='TrainingWeek.days.TrainingDay.sessions.CodedValue.raw',native_verified=False),
      'managed_team_capacity':dict(unit='stored_team_list_length',source='Club.teams joined to ManagedClub.club_uid',native_verified=False),
      'training.teams':dict(unit='stored_weeks_days_and_parser_claimed_week_dates',source='TeamTraining.weeks/TrainingWeek.week_start/days; team codes anonymized',native_verified=False),
      'injuries.historical_managed_club_records':dict(unit='HISTORY_records_joined_by_stored_club_uid',source='Injury.kind/club_uid; null club is not managed identity',native_verified=False),
      'injuries.typed_current_cohort_records':dict(unit='TYPED_records_joined_to_current_parsed_cohort',source='Injury.kind/player_uid joined to parsed managed squad; no duration claim',native_verified=False),
      'tactics':dict(unit='decoded_records_only',source='Save.tactics; active tactic/IP/OOP/effectiveness not established',native_verified=False),
      'fixtures':dict(unit='decoded_records_only',source='Save.fixtures; authoritative calendar not established',native_verified=False),
      'staff':dict(unit='decoded_records_only',source='Save.staff/staff_lists; session coach assignment not established',native_verified=False),
      'checks':dict(unit='upstream_structural_counts_bounds_and_rates',source='Save._reader_check and GateCheckError.checks',native_verified=False),
      'borrowed_layout':dict(unit='upstream_layout_selection_claim',source='Save._reader_layout in0.12.4',native_verified=False),
      'trace':dict(unit='call_count',source='own passive wrappers;return values unchanged',native_verified=False),
      'individual_participation':dict(unit=None,source=None,status='not_available'),
      'career_rng_independence':dict(unit=None,source=None,status='not_available')}


def ledger(events,profile,resources,stable):
    indexed={}
    for row in events:
        require(row['probe'] in PROBES,'Unknown probe in retained ledger')
        indexed[row['probe']]=row
    result=[]
    for name in PROBES:
        old=indexed.get(name)
        if old is None:result.append(dict(probe=name,status='not_started'));continue
        row={k:old[k] for k in ('probe','status','coverage','checks','borrowed_layout','warning_types','warning_count','error_type') if k in old}
        if row['status']=='started':row['status']='started_unresolved'
        result.append(row)
    return dict(profile=profile,version=VERSION,resources=resources,snapshot_stable=stable,
        probes=result,field_contract=field_contract(),
        warnings_require_review=True,unverified_build_is_not_validation=True,
        raw_offset_binding_independently_verified=False,native_semantics_verified=False,
        ui_to_save_binding_verified=False,career_rng_independence_verified=False,
        individual_participation_verified=False,native_released=False,career_advance_released=False,
        replay_released=False,native_starts=0,calendar_advances=0,seeds_reserved=0)


class HardReaderJob:
    """One Windows job with kernel process+job private-memory caps and kill-on-close."""
    def __init__(self,limit=MEMORY_BYTES):
        require(os.name=='nt','Windows hard memory job is required')
        require(type(limit) is int and limit>0,'Invalid memory cap')
        import ctypes
        from ctypes import wintypes
        self.ctypes,self.wintypes=ctypes,wintypes
        class Basic(ctypes.Structure):
            _fields_=[('ProcessTime',ctypes.c_int64),('JobTime',ctypes.c_int64),
                ('Flags',wintypes.DWORD),('MinWorkingSet',ctypes.c_size_t),('MaxWorkingSet',ctypes.c_size_t),
                ('ActiveProcesses',wintypes.DWORD),('Affinity',ctypes.c_size_t),
                ('Priority',wintypes.DWORD),('Scheduling',wintypes.DWORD)]
        class IO(ctypes.Structure):
            _fields_=[(x,ctypes.c_ulonglong) for x in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
        class Extended(ctypes.Structure):
            _fields_=[('Basic',Basic),('IO',IO),('ProcessMemory',ctypes.c_size_t),
                ('JobMemory',ctypes.c_size_t),('PeakProcessMemory',ctypes.c_size_t),('PeakJobMemory',ctypes.c_size_t)]
        self.Extended=Extended
        k=ctypes.WinDLL('kernel32',use_last_error=True);self.kernel=k
        k.CreateJobObjectW.argtypes=[ctypes.c_void_p,wintypes.LPCWSTR];k.CreateJobObjectW.restype=wintypes.HANDLE
        k.SetInformationJobObject.argtypes=[wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD];k.SetInformationJobObject.restype=wintypes.BOOL
        k.AssignProcessToJobObject.argtypes=[wintypes.HANDLE,wintypes.HANDLE];k.AssignProcessToJobObject.restype=wintypes.BOOL
        k.QueryInformationJobObject.argtypes=[wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD,ctypes.c_void_p];k.QueryInformationJobObject.restype=wintypes.BOOL
        k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
        self.handle=k.CreateJobObjectW(None,None)
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        self.limit=limit
        info=Extended();info.Basic.Flags=0x2000|0x100|0x200|0x8
        info.Basic.ActiveProcesses=1;info.ProcessMemory=limit;info.JobMemory=limit
        if not k.SetInformationJobObject(self.handle,9,ctypes.byref(info),ctypes.sizeof(info)):
            error=ctypes.WinError(ctypes.get_last_error());self.close();raise error

    def assign(self,process):
        if not self.kernel.AssignProcessToJobObject(self.handle,int(process._handle)):
            raise self.ctypes.WinError(self.ctypes.get_last_error())
        proof=self.info()
        require(proof['process_memory_limit']==self.limit and proof['job_memory_limit']==self.limit,
                'Kernel memory policy readback differs')
        require(proof['limit_flags']&0x2308==0x2308 and proof['active_process_limit']==1,
                'Kernel process-count/kill policy readback differs')
        return proof

    def info(self):
        data=self.Extended()
        if not self.kernel.QueryInformationJobObject(self.handle,9,self.ctypes.byref(data),self.ctypes.sizeof(data),None):
            raise self.ctypes.WinError(self.ctypes.get_last_error())
        return dict(process_memory_limit=int(data.ProcessMemory),job_memory_limit=int(data.JobMemory),
            limit_flags=int(data.Basic.Flags),active_process_limit=int(data.Basic.ActiveProcesses),
            peak_process_private_bytes=int(data.PeakProcessMemory),peak_job_private_bytes=int(data.PeakJobMemory))

    def close(self):
        if getattr(self,'handle',None):
            self.kernel.CloseHandle(self.handle);self.handle=None

    def __enter__(self):return self
    def __exit__(self,*args):self.close()

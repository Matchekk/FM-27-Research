"""Cold-only sharpness audit and bounded four-thread dispatch, no server import."""
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from threading import Event, Lock

from analysis import run_observer005 as observer
from analysis.startpolicy002_gate import audit_start_state, lineup_slots, repeat_equivalence
from research.native import event, require
from research.passive_observer import audit_trace, canonical_hash, match_result, snapshot

EXPERIMENT = 'MECH-002-SHARPNESS-P0'
OBSERVER_HOST = '58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
CONTEXTS = ('high_press', 'deep_block')
ARMS = ('S70-P0', 'S100-P0', 'S70-P1', 'S100-P1')


class FirstMainCall:
    """No other cold call may overtake the immediate first-call600s recheck."""
    def __init__(self):
        self.lock=Lock();self.attempted=False;self.evidence=None

    def invoke(self,operation,check,allowance):
        with self.lock:
            if not self.attempted:
                limit=allowance()  # Admission/IO occurs after waiting, before the final600s check.
                remaining=check()
                require(type(remaining) in (int,float) and math.isfinite(remaining) and remaining>=600,
                        'Immediate first-main allowance below600s')
                self.evidence=dict(remaining_seconds=remaining,checked_utc=datetime.now(timezone.utc).isoformat())
                self.attempted=True
                return operation(min(limit,remaining))  # First call alone; then normal four-thread dispatch.
        return operation(allowance())


class ReadLeases:
    """Own Windows read handles: share reads only; no foreign Python import."""
    def __init__(self):
        import ctypes
        from ctypes import wintypes
        import os
        require(os.name=='nt','Windows read leases required')
        self.ctypes=ctypes;self.handles=[];self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        self.kernel.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,
                                         wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]
        self.kernel.CreateFileW.restype=wintypes.HANDLE
        self.kernel.CloseHandle.argtypes=[wintypes.HANDLE];self.kernel.CloseHandle.restype=wintypes.BOOL

    def lease(self,path):
        value=self.kernel.CreateFileW(str(Path(path).resolve()),0x80000000,1,None,3,0x80,None)
        if value==self.ctypes.c_void_p(-1).value:raise self.ctypes.WinError(self.ctypes.get_last_error())
        self.handles.append(value)

    def close_leases(self):
        while self.handles:
            if not self.kernel.CloseHandle(self.handles[-1]):raise self.ctypes.WinError(self.ctypes.get_last_error())
            self.handles.pop()


def treatment(arm):
    require(arm in ARMS, 'Unknown arm')
    return (7000 if arm.startswith('S70-') else 10000, 66 if arm.endswith('P1') else 0)


def initial_controls(evidence):
    result = {}
    for row in evidence:
        if row.get('event') != 'native_passive_state' or row['stage'] not in ('prepared', 'first_advance'):
            continue
        players = snapshot(row)
        fields = ('id', 'side', 'roster_index', 'condition_raw', 'fatigue_raw',
                  'condition_accumulator_raw', 'sharpness_penalty_raw', 'effectiveness_region_hex')
        result[row['stage']] = canonical_hash([{k:p[k] for k in fields} for _,p in sorted(players.items())])
    require(set(result) == {'prepared', 'first_advance'}, 'Missing initial control stage')
    return result


def descriptive(evidence, binary, side):
    slots = lineup_slots(binary); targets = {slots[side,i] for i in range(1,11)}
    stages = {r['stage']:snapshot(r) for r in evidence if r.get('event') == 'native_passive_state'}
    require(set(stages) == {'prepared','first_advance','finished'}, 'Descriptive snapshots incomplete')
    output, missing = {}, {}
    for stage, bound in stages.items():
        players = [p for p in bound.values() if p['side'] == side and p['roster_index'] in targets]
        require(len(players) == 10, 'Ten identity-bound outfield starters required')
        prefix = 'first' if stage == 'first_advance' else stage
        for offset, name in ((9,'condition_cache89'),(10,'sharpness_cache8a')):
            key = prefix+'_'+name+'_mean'
            values = [bytes.fromhex(p['statistics_cache_region_hex'])[offset]
                      for p in players if p['statistics_cache_region_hex'] is not None]
            output[key] = sum(values)/10 if len(values) == 10 else None
            if len(values) != 10: missing[key] = 'incomplete_identity_bound_runtime_cache'
        if stage == 'finished':
            for field in ('condition_raw','sharpness_raw','sharpness_secondary_raw','fatigue_raw',
                          'condition_accumulator_raw','sharpness_penalty_raw'):
                output['finished_'+field+'_mean'] = sum(p[field] for p in players)/10
            # Includes the all-zero pattern; ten all-zero regions means one hash.
            output['finished_tf33_distinct_hashes'] = len({sha256(bytes.fromhex(p['effectiveness_region_hex'])).hexdigest()
                                                          for p in players})
    output.update(prepared_tf33_matches_frozen_d00=True, first_tf33_matches_frozen_d00=True)
    return output, missing


def audit_job(evidence, dump, job, binary, config, catalog, oop_map, frozen_controls, observer_sha256):
    require(observer_sha256 == OBSERVER_HOST, 'Observer binary drift')
    require(event(evidence,'native_image_fingerprint')['sha256'] == job['identity']['engine_sha256'], 'Loaded engine drift')
    require(event(evidence,'native_engine_compatibility')['compatible'] is True and
            event(evidence,'windows_load_returned')['success'] is True, 'Native loader gate failed')
    phases = [r for r in evidence if r.get('event') == 'native_phase_configuration']
    require(len(phases) == 4 and {(r['side'],r['phase']) for r in phases} == {(s,p) for s in (0,1) for p in (0,1)},
            'Native phase receipts incomplete')
    checked = observer.audit_input(evidence,dump,config,binary,catalog,oop_map)
    audit_trace(evidence,dump,job['seed'])
    raw, bit = treatment(job['arm'])
    audit_start_state(evidence,binary,job['side'],raw)
    require(all(type(p['attributes'][52]) is int and p['attributes'][52] == 60
                for team in dump['teams'] for p in team['players']), 'Stamina60 changed')
    selected = config['teams'][job['side']]['instructions']['10']
    require(selected == (2000905329 if bit else 1313689463), 'Declared pressing ID drift')
    require(initial_controls(evidence) == frozen_controls, 'Initial nonsharpness/rawTF33 controls changed')
    values, missing = descriptive(evidence,binary,job['side'])
    return dict(job_id=job['key'],experiment_id=EXPERIMENT,context=job['scenario'],team_side=job['side'],
        seed=job['seed'],arm=job['arm'],status='ok',config_sha256=job['config_sha256'],
        setup_sha256=job['setup_sha256'],identity=job['identity'],observer_host_sha256=observer_sha256,
        result={k:v for k,v in match_result(evidence,job['seed']).items() if k != 'seed'},
        native_audit=dict(input_verified=True,seed_verified=True,
            sharpness_start_verified=True,stamina60_verified=True,pressing_verified=True,controls_verified=True,
            attribute_values_verified=checked['attribute_values_verified'],profile_fields_verified=checked['profile_fields_verified'],
            phase_cells_verified=checked['phase_cells_verified'],pi_groups_verified=checked['pi_groups_verified'],
            sharpness_raw=raw,pressing_bit=bit), descriptive=values,descriptive_missing_reasons=missing)


def write_exclusive(path, value):
    import os
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(value,stream,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())


class ColdScheduler:
    """One phase, four claims maximum. Claimed jobs precede any Popen/GO.

    A shared locked stop prevents subsequent claims and blocks. Already claimed
    calls finish within their existing kernel containment/deadlines and remain
    accounted. This counts admitted in-flight calls, not unseen engine PIDs.
    """
    def __init__(self, directory, invoke, admission, audit_block=None):
        self.directory = Path(directory); self.directory.mkdir(parents=True,exist_ok=False)
        self.invoke,self.admission,self.audit_block = invoke,admission,audit_block
        self.stop = Event(); self.lock = Lock(); self.claims = 0; self.peak = 0
        self.started = set(); self.results = {}; self.counter_events = []

    def _counter(self, event_name, key):
        import os
        value = dict(event=event_name,job_id=key,active_claims=self.claims,peak_claims=self.peak,
                     utc=datetime.now(timezone.utc).isoformat())
        with (self.directory/'concurrency.jsonl').open('a',encoding='utf8') as stream:
            stream.write(json.dumps(value)+'\n');stream.flush();os.fsync(stream.fileno())
        self.counter_events.append(value)

    def _halt(self,key):
        # Caller holds the same lock used to claim jobs.
        if not self.stop.is_set():
            self.stop.set();self._counter('stop',key)

    def _one(self, job):
        key = job['key']; require(re.fullmatch('[A-Za-z0-9_-]{1,180}',key), 'Unsafe job key')
        with self.lock:
            if self.stop.is_set(): return None
            try:
                self.admission(job)
                require(key not in self.started, 'Duplicate claimed job')
                write_exclusive(self.directory/(key+'.started.json'),dict(job_id=key,seed=job.get('seed'),
                    claimed_utc=datetime.now(timezone.utc).isoformat(),native_invocation_started=False))
                self.started.add(key);self.claims += 1;self.peak = max(self.peak,self.claims)
                require(self.claims <= 4, 'Global cold-call limit exceeded')
                self._counter('claimed',key)
            except BaseException as error:
                self._halt(key)
                write_exclusive(self.directory/(key+'.admission-failure.json'),
                                dict(error_type=type(error).__name__,detail=str(error)))
                raise
        row = dict(job_id=key,seed=job.get('seed'),status='started',native_invocation_started=False)
        def on_start():
            with self.lock:
                row['native_invocation_started'] = True
                write_exclusive(self.directory/(key+'.admitted.json'),dict(job_id=key,
                    admitted_utc=datetime.now(timezone.utc).isoformat()))
        try:
            result = self.invoke(job,on_start)
            require(type(result) is dict and result.get('status') in ('ok','expected_rejection'), 'Invalid cold result')
            row.update(result)
        except BaseException as error:
            with self.lock:self._halt(key)
            row.update(status='failed',error_type=type(error).__name__)
            if type(getattr(error,'native_evidence',None)) is dict:
                row['native_failure_evidence']=error.native_evidence
            write_exclusive(self.directory/(key+'.failure.json'),dict(detail=str(error)))
        finally:
            import os
            with self.lock:
                self.claims -= 1
                self.results[key] = row
                self._counter('completed',key)
                with (self.directory/'ledger.jsonl').open('a',encoding='utf8') as stream:
                    stream.write(json.dumps(row,allow_nan=False)+'\n');stream.flush();os.fsync(stream.fileno())
        return row

    def run(self, blocks):
        all_jobs = [job for block in blocks for job in block]
        require(len({j['key'] for j in all_jobs}) == len(all_jobs), 'Duplicate phase plan')
        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                for block in blocks:
                    if self.stop.is_set():break
                    pending = iter(block); futures = set()
                    for _ in range(min(4,len(block))): futures.add(pool.submit(self._one,next(pending)))
                    while futures:
                        done,futures = wait(futures,return_when=FIRST_COMPLETED)
                        for future in done:
                            try: future.result()
                            except BaseException:
                                with self.lock:self._halt('dispatch')
                        if not self.stop.is_set():
                            for _ in done:
                                job = next(pending,None)
                                if job is not None:futures.add(pool.submit(self._one,job))
                    if not self.stop.is_set() and self.audit_block:
                        try:self.audit_block(block)
                        except BaseException as error:
                            with self.lock:self._halt('block-audit')
                            write_exclusive(self.directory/'block-audit.failure.json',
                                dict(job_ids=[j['key'] for j in block],error_type=type(error).__name__,detail=str(error)))
                            raise
        finally:
            write_exclusive(self.directory/'dispatch-summary.json',dict(
                planned=len(all_jobs),claimed=len(self.started),resolved=len(self.results),
                unbegun=[j['key'] for j in all_jobs if j['key'] not in self.started],
                started_unresolved=sorted(self.started-set(self.results)),stop=self.stop.is_set(),
                peak_inflight_claims=self.peak,active_claims=self.claims,
                engine_process_upper_bound=self.peak,engine_pid_peak_measured=False,
                engine_bound_basis='At most four independent Job3 calls; unchanged native host allows one engine child per call'))
        require(not self.stop.is_set() and len(self.results) == len(all_jobs) and
                all(r['status'] in ('ok','expected_rejection') for r in self.results.values()),
                'Incomplete/failed phase: technical status only')
        return [self.results[j['key']] for j in all_jobs]


def block_jobs(jobs, *, technical=False):
    """Eight full jobs per independent seed block; technical negative is last."""
    grouped = {}; negative = []
    for job in jobs:
        if job.get('kind') == 'negative': negative.append(job);continue
        # Technical seeds belong to a context+side cell, main seeds span both sides.
        key = (job['scenario'],job['seed'],job['side']) if technical else (job['scenario'],job['seed'])
        grouped.setdefault(key,[]).append(job)
    require(all(len(block) == 8 for block in grouped.values()), 'Eight complete jobs per block required')
    require(len(negative) == (1 if technical else 0), 'Unexpected negative count')
    return [grouped[key] for key in sorted(grouped)] + ([negative] if negative else [])

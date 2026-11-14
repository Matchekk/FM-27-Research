"""One-time reviewed administrative continuation for an independent study only.

Reads existing private evidence. Never starts a host, resumes the failed study,
changes its own ledger or refunds any mission time, job or seed reservation.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.pycache_prefix = str(ROOT/'local/night-002/reconcile-cache'/uuid4().hex)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from research.budget import atomic
from research.native import read, rows, require
from research.native_process005 import confirmed_cleanup
from research.night002_control import (DEADLINE, FAILED_GLOBAL_SHA256, TERMINAL_STUDY,
    INDEPENDENT_STUDY, assert_artifact_limit, reconcile_terminal_state)

PUBLIC = 'data/night-002-split004/'
REVIEW = 'docs/night-002/SPLIT004-TERMINATION-REVIEW.md'
PUBLISHED_PATHS = ('research/night002_control.py','analysis/night002_supervise.py',
    'analysis/reconcile_night002.py','tests/test_night002_control.py',REVIEW,
    PUBLIC+'termination.json',PUBLIC+'termination-review.json',PUBLIC+'native-call-time.json')


def digest(path, normalized=False):
    data = Path(path).read_bytes()
    return sha256(data.replace(b'\r\n',b'\n') if normalized else data).hexdigest()


def publication(commit, ci):
    require(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit) and type(ci) is int and ci>0,
            'Full publication commit and positive CI run required')
    result = json.loads(subprocess.check_output(['gh','run','view',str(ci),'--repo','Matchekk/FM-27-Research',
        '--json','headSha,status,conclusion'],cwd=ROOT,text=True))
    require(result == dict(headSha=commit,status='completed',conclusion='success'), 'Exact publication CI not successful')
    remote = subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]
    for target in ('HEAD',remote):
        subprocess.run(['git','merge-base','--is-ancestor',commit,target],cwd=ROOT,check=True,capture_output=True)
    for name in PUBLISHED_PATHS:
        blob = subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(blob == (ROOT/name).read_bytes().replace(b'\r\n',b'\n'), 'Published reconciliation artifact changed: '+name)


def private_cleanup(proof, calls):
    local = ROOT/'local/night-002/split004';own_path = local/'budget.json';own = read(own_path)
    require(digest(own_path) == proof['study_budget_sha256'] and own['active'] is None and own['halted'] is True and
            own['charged_seconds'] == proof['study_charged_seconds'] == 528.8133745000014,
            'Terminal own-study ledger changed or resumed')
    require(not list(local.rglob('pending.json')) and not (ROOT/'local/global-native/native-execution.lease.json').exists(),
            'Native cleanup pending or global lease retained')
    require(calls['experiment_id'] == TERMINAL_STUDY and calls['terminal_closed'] is True and
            calls['scientific_series_complete'] is False and calls['complete_accounting'] is True and
            calls['calls'] == 257 and calls['planned_jobs'] == 545 and
            digest(ROOT/(PUBLIC+'native-call-time.json'),True) == proof['native_call_time_sha256'],
            'Terminal native call inventory differs')
    total = 0.;count = 0
    for phase, expected in (('technical',33),('main',224)):
        ledger_path = local/phase/'dispatch/ledger.jsonl';data = rows(ledger_path)
        native = [row for row in data if row.get('native_invocation_started') is True]
        require(len(native) == expected and len(data) == (33 if phase=='technical' else 225), 'Native ledger coverage differs')
        projection = [dict(job_id=r['job_id'],status=r['status'],native_elapsed_seconds=r['native_elapsed_seconds']) for r in native]
        recorded = calls['phases'][phase]
        require(recorded['jobs'] == projection and recorded['ledger_sha256'] == digest(ledger_path),
                'Public native call accounting differs from immutable ledger')
        if phase=='main':
            failed = [r for r in data if r['status']=='failed']
            require(len(failed)==1 and failed[0]['native_invocation_started'] is False and
                    not list((local/phase/'jobs'/failed[0]['job_id']).glob('*')),
                    'Failed job may have launched a native process')
            require(digest(ledger_path)==proof['main_dispatch_ledger_sha256'], 'Terminal main ledger changed')
        for row in native:
            directory = local/phase/'jobs'/row['job_id']
            require(confirmed_cleanup(directory/'native.stdout',expected_limit=3), 'Kernel-zero cleanup not proved')
            for name,field in (('native.stdout','stdout_sha256'),('native.jsonl','raw_log_sha256'),
                    ('native.containment.json','containment_receipt_sha256'),('input.json','input_dump_sha256')):
                if row.get(field):require(digest(directory/name)==row[field], 'Private raw evidence hash changed')
            require(row['status'] in ('ok','expected_rejection') and type(row['native_elapsed_seconds']) in (int,float) and
                    row['native_elapsed_seconds']>0, 'Unknown/failed native charge')
            total += row['native_elapsed_seconds'];count += 1
        require(sum(r['native_elapsed_seconds'] for r in native) == recorded['sum_native_elapsed_seconds'],
                'Phase native time was refunded/changed')
    # Preserve the original order of phase summation used in the public ledger.
    require(count==257 and sum(calls['phases'][p]['sum_native_elapsed_seconds'] for p in ('technical','main')) ==
            calls['sum_native_elapsed_seconds'], 'Terminal native time total differs')
    archive = local/'main/completed-archives/batch-0000.zip';journal_path = archive.with_suffix('.json');journal = read(journal_path)
    require(digest(archive)==proof['archive_zip_sha256']==journal['archive_sha256'] and
            digest(journal_path)==proof['archive_journal_sha256'] and len(journal['entries'])==1024,
            'Restored archive/journal commitment differs')
    with zipfile.ZipFile(archive) as stream:
        require(stream.testzip() is None and set(stream.namelist())==set(journal['entries']), 'Archive CRC/inventory failed')
        for name,wanted in journal['entries'].items():
            path = (local/'main'/name).resolve()
            require(path.is_relative_to((local/'main').resolve()) and digest(path)==wanted==sha256(stream.read(name)).hexdigest(),
                    'Archive restoration is incomplete or changed')
    return dict(native_calls=257,all_native_cleanup_confirmed=True,archive_entries_restored=1024,
                summed_native_call_seconds=calls['sum_native_elapsed_seconds'])


def checked_transition(commit,ci):
    public = ROOT/PUBLIC;proof = read(public/'termination.json');review = read(public/'termination-review.json')
    binding = dict(termination_sha256=digest(public/'termination.json',True),
        review_sha256=digest(ROOT/REVIEW,True),review_gate_sha256=digest(public/'termination-review.json',True),
        publication_commit=commit,ci_run=ci,checked_utc=datetime.now(timezone.utc).isoformat())
    path = ROOT/'local/night-002/program-budget.json';before = path.read_bytes()
    require(sha256(before).hexdigest()==FAILED_GLOBAL_SHA256, 'Only the exact retained failed global budget is admissible')
    next_state = reconcile_terminal_state(before,FAILED_GLOBAL_SHA256,proof,review,binding)
    report = private_cleanup(proof,read(public/'native-call-time.json'))
    assert_artifact_limit(ROOT)
    require(datetime.now(timezone.utc)<datetime.fromisoformat(DEADLINE), 'NIGHT-002 absolute deadline passed')
    require(path.read_bytes()==before, 'Concurrent mission budget change; no reconciliation')
    return path,before,next_state,report


def apply_transition(commit,ci):
    publication(commit,ci)
    path = ROOT/'local/night-002/program-budget.json';lock = path.with_suffix('.lock');lock.touch(exist_ok=False)
    try:
        path,before,next_state,report = checked_transition(commit,ci)
        directory = path.parent/'reconciliations';directory.mkdir(exist_ok=True)
        snapshot = directory/'MECH004-failed-budget.json';receipt_path = directory/'MECH004-to-TACT003.json'
        require(not snapshot.exists() and not receipt_path.exists(), 'Reconciliation already attempted; no retry')
        after = (json.dumps(next_state,allow_nan=False,indent=2)+'\n').encode()
        receipt = dict(schema_version=1,terminal_study=TERMINAL_STUDY,independent_study_only=INDEPENDENT_STUDY,
            before_budget_sha256=sha256(before).hexdigest(),after_budget_sha256=sha256(after).hexdigest(),
            charges_and_reservations_preserved=True,failed_own_ledger_unchanged=True,
            binding=next_state['reconciliations'][0],cleanup=report)
        # Receipt precedes the state change. A crash before replacement leaves
        # the mission halted and the one-shot receipt blocks automatic retry.
        with snapshot.open('xb') as stream:stream.write(before);stream.flush();os.fsync(stream.fileno())
        with receipt_path.open('x',encoding='utf8',newline='\n') as stream:
            stream.write(json.dumps(receipt,allow_nan=False,indent=2)+'\n');stream.flush();os.fsync(stream.fileno())
        require(path.read_bytes()==before, 'Mission budget changed before atomic reconciliation')
        atomic(path,next_state)
        require(digest(path)==receipt['after_budget_sha256'], 'Atomic reconciliation hash mismatch')
        return receipt
    finally:lock.unlink()


if __name__=='__main__':
    parser = ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('command',choices=('check','reconcile-failed-study'))
    parser.add_argument('--publication');parser.add_argument('--ci-run',type=int);args=parser.parse_args()
    if args.command=='check':
        _,_,_,report = checked_transition(args.publication,args.ci_run)
        print(json.dumps(dict(read_only=True,**report),indent=2))
    else:print(json.dumps(apply_transition(args.publication,args.ci_run),indent=2))

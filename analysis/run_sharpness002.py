"""Draft cold-CLI sharpness pilot supervisor. All releases are external gates.

No NativeLab/server/warm-runner import, seed allocation or career operation.
Only a centrally admitted phase can reach the unchanged readonly observer host.
"""
from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from analysis import run_observer005 as observer
from analysis.run_startpolicy002 import audit_malformed
from analysis.sharpness002_runner import (EXPERIMENT,OBSERVER_HOST,ARMS,CONTEXTS,ColdScheduler,ReadLeases,
    audit_job,block_jobs,initial_controls,repeat_equivalence,treatment,write_exclusive)
from research.budget import atomic,supervisor_alive
from research.coordination import NativeLease
from research.core import config_hash,historical_seeds,schedule
from research.native import digest,read,require,rows,write
from research.night_control import assert_night_admission,DEADLINE
from research.study_budget import DeadlineBudget

LOCAL=ROOT/'local/mech-002-sharpness-p0'
PUBLIC=ROOT/'data/mech-002-sharpness-p0'
REGISTRY=ROOT/'local/registry'
RUNTIME=ROOT/'local/runtime-v1114.6'
TECH17=ROOT/'data/mech-002-startpolicy-tech'
TECH17_REVIEW='docs/night-001/STARTPOLICY-002-RESULTS-REVIEW.md'
REVIEW='docs/night-001/SHARPNESS-REVIEW.md'
MAIN_REVIEW='docs/night-001/SHARPNESS-TECHNICAL-REVIEW.md'
DOCUMENT='experiments/MECH-002-sharpness-pilot.md'
CODE=('analysis/run_sharpness002.py','analysis/sharpness002_runner.py','tests/test_sharpness002_runner.py',
    'docs/night-001/SHARPNESS-RUNNER.md','analysis/sharpness002_design.py','analysis/analyse_sharpness002.py',DOCUMENT,
    'analysis/run_observer005.py','analysis/run_startpolicy002.py','analysis/startpolicy002_gate.py',
    'analysis/startpolicy002_budget.py','analysis/night_supervise.py','research/startpolicy.py',
    'research/passive_observer.py','research/native_process005.py','research/core.py','research/native.py',
    'research/coordination.py','research/budget.py','research/study_budget.py','research/night_control.py',
    'research/stats.py','requirements.txt','requirements-lock.txt',
    'adapters/passive_observer_v1.h','adapters/passive-observer-v1.patch')
source_hash=observer.source_hash


def design():
    return importlib.import_module('analysis.sharpness002_design')


def software():
    return dict(python=sys.version,numpy=importlib.metadata.version('numpy'),scipy=importlib.metadata.version('scipy'),
                capsule_base_python_sha256=digest(Path(getattr(sys,'_base_executable',sys.executable))))


def sha_commit(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{40}',value),'Full published commit required')


def published(commit,ci,paths):
    sha_commit(commit);require(type(ci) is int and ci>0,'Exact successful CI required')
    observer.successful_ci(commit,ci)
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]
    for target in ('HEAD',remote):
        subprocess.run(['git','merge-base','--is-ancestor',commit,target],cwd=ROOT,check=True,capture_output=True)
    for name in paths:
        require(subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)==
                (ROOT/name).read_bytes().replace(b'\r\n',b'\n'),'Published artifact changed: '+name)


def verify_tech17():
    release=read(TECH17/'release-gate.json');summary=read(TECH17/'technical-summary.json')
    require(release['experiment_id']=='MECH-002-STARTPOLICY-TECH-V1' and release['passed'] is True and
            release['independently_released'] is True and summary['passed'] is True and
            summary['full_matches']==16 and summary['negative_rejections']==1 and
            summary['budget_gate']['passed'] is True,'TECH17 transfer is not independently released')
    require(release['summary_sha256']==source_hash(TECH17/'technical-summary.json') and
            release['review_sha256']==source_hash(ROOT/TECH17_REVIEW),'TECH17 release evidence drift')
    published(release['release_commit'],release['ci_run'],
              ['data/mech-002-startpolicy-tech/technical-summary.json',TECH17_REVIEW])
    # The old master belongs to its historical epoch, not this new route.
    registration=read(TECH17/'registration.json');inputs=read(TECH17/'inputs.json')
    old=registration['preregistration_commit'];sha_commit(old)
    require(registration['inputs_sha256']==source_hash(TECH17/'inputs.json'),'TECH17 original registration drift')
    for name,value in inputs['code_sha256'].items():
        blob=subprocess.check_output(['git','show',old+':'+name],cwd=ROOT)
        require(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==value,'TECH17 archived source blob mismatch')
    return {k:release[k] for k in ('experiment_id','passed','independently_released','release_commit',
                                  'ci_run','summary_sha256','review_sha256')}


def previous_seeds():
    used={0}
    for path in (ROOT/'data').iterdir():
        if path.is_dir() and path!=PUBLIC:used.update(historical_seeds(path))
    for path in REGISTRY.glob('*.json'):
        if path.name!=EXPERIMENT+'.reserved.json':
            used.update(historical_seeds(path));used.update(read(path).get('seeds',[]))
    for path in (ROOT/'local').iterdir():
        if path.is_dir() and path!=LOCAL and path.name.startswith(('valid','tact-','attr-','mech-','night-','platform-smoke')):
            used.update(historical_seeds(path))
    return used


def seed_plan():
    plan=read(REGISTRY/(EXPERIMENT+'.reserved.json'))
    require(plan['experiment_id']==EXPERIMENT and plan['namespace']==EXPERIMENT+'/main-v1','Wrong external seed namespace')
    main,technical,all_seeds=(plan[k] for k in ('main_seeds','technical_seeds','seeds'))
    require(type(main) is list and type(technical) is list and type(all_seeds) is list and
            len(main)==64 and len(technical)==4 and len(all_seeds)==len(set(all_seeds))==68 and
            set(all_seeds)==set(main+technical) and
            all(type(s) is int and 0<s<=0xffffffff for s in all_seeds+main+technical),'Exactly64main+4technical new uint32 seeds')
    require(not set(all_seeds)&previous_seeds(),'Historical/reserved seed overlap')
    return plan


def prepare():
    require(not (PUBLIC/'inputs.json').exists() and not LOCAL.exists(),'Prepared experiment retained; no retry/reseed')
    release=verify_tech17();plan=seed_plan();module=design()
    prior=read(ROOT/'data/valid-005-observer-v1/inputs.json');private=read(ROOT/'local/valid005-observer-v1/private-host.json')
    host=Path(private['observer_host']);build=read(private['build_manifest'])
    require(digest(host)==OBSERVER_HOST==prior['observer_host_sha256'] and
            digest(private['build_manifest'])==prior['build_manifest_sha256'] and
            digest(host.parent/'desktop_host.cpp')==build['modified_host_source_sha256'] and
            digest(host.parent/'passive_observer_v1.h')==build['observer_header_sha256'],'Unchanged observer build required')
    require(observer.fingerprint()==prior['identity']['resource_fingerprint'] and
            digest(RUNTIME/'engine/fm27_native/fixtures/match.pkm')==prior['identity']['fixture_sha256'],'Engine/resources/fixture drift')
    old=read(ROOT/'data/mech-003-stamina/inputs.json');configs=read(ROOT/'local/valid005-observer-v1/configs.json')
    require(old['identity']==prior['identity'] and config_hash(configs)==prior['configs_sha256'],'Baseline identity/config drift')
    setups={}; controls={}; originals={}; factory_hashes={}
    for context in CONTEXTS:
        setups[context]={}
        for side in (0,1):
            label=f'{context}-{side}'
            d00=ROOT/'local/valid005-observer-v1/inputs'/(label+'.bin')
            more=ROOT/'local/mech-003-stamina/inputs'/(label+'-R01.bin')
            require(digest(d00)==prior['setups'][label] and digest(more)==old['setups'][context][str(side)]['R01'],
                    'D00/originalStamina40More input hash mismatch')
            payloads=module.build_inputs(d00.read_bytes(),more.read_bytes(),side)
            require(set(payloads)==set(ARMS),'Factory arm mismatch')
            setups[context][str(side)]={}
            for arm,payload in payloads.items():
                path=LOCAL/'inputs'/f'{label}-{arm}.bin';path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as stream:stream.write(payload)
                setups[context][str(side)][arm]=digest(path)
            gold=ROOT/'local/valid005-observer-v1/technical'/(label+'-observer_on.jsonl')
            controls[label]=initial_controls(rows(gold))
            originals[label]=dict(d00_sha256=digest(d00),original_r01_sha256=digest(more),gold_sha256=digest(gold))
            factory_hashes[label]=config_hash(setups[context][str(side)])
    write_exclusive(LOCAL/'configs.json',configs);write_exclusive(LOCAL/'private-host.json',private)
    write_exclusive(PUBLIC/'seed-plan.json',plan);write_exclusive(LOCAL/'seed-plan.json',plan)
    inputs=dict(experiment_id=EXPERIMENT,identity=prior['identity'],observer_host_sha256=OBSERVER_HOST,software=software(),
        build_manifest_sha256=prior['build_manifest_sha256'],catalog_sha256=prior['catalog_sha256'],oop_map=prior['oop_map'],
        runtime_source_sha256=prior['runtime_source_sha256'],lease_module_sha256=prior['lease_module_sha256'],
        setups=setups,original_inputs=originals,frozen_controls=controls,configs_sha256=config_hash(configs),
        factory_sha256=factory_hashes,tech17_release=release,tech17_release_file_sha256=source_hash(TECH17/'release-gate.json'),
        code_sha256={name:source_hash(ROOT/name) for name in CODE},seed_plan_sha256=source_hash(PUBLIC/'seed-plan.json'))
    write_exclusive(PUBLIC/'inputs.json',inputs)
    contract=module.contract_definition(identity=prior['identity'],setups=setups)
    contract['gates']['tech17']=release
    contract['execution']=dict(runner='analysis/run_sharpness002.py',kind='cold_direct_cli',workers=4,max_processes_per_job=3,
        code_sha256=inputs['code_sha256'],input_manifest_sha256=source_hash(PUBLIC/'inputs.json'),
        seed_plan_sha256=source_hash(PUBLIC/'seed-plan.json'))
    module.validate_design(contract)
    write_exclusive(PUBLIC/'contract.json',contract)
    write_exclusive(LOCAL/'technical-keys.json',[j['key'] for j in module.technical_jobs(plan['technical_seeds'])])
    print('Offline inputs prepared; zero native calls, zero seed allocations.',flush=True)


def verify_frozen():
    value=read(PUBLIC/'inputs.json')
    require(value['experiment_id']==EXPERIMENT and value['observer_host_sha256']==OBSERVER_HOST,'Input identity changed')
    require(value['software']==software(),'Python/capsule/analysis dependency drift')
    require(all(source_hash(ROOT/n)==h for n,h in value['code_sha256'].items()),'Frozen code changed')
    require(source_hash(PUBLIC/'seed-plan.json')==value['seed_plan_sha256'] and read(PUBLIC/'seed-plan.json')==seed_plan(),'Seed plan drift')
    require(verify_tech17()==value['tech17_release'] and source_hash(TECH17/'release-gate.json')==value['tech17_release_file_sha256'],
            'Prior technical release changed')
    require(config_hash(read(LOCAL/'configs.json'))==value['configs_sha256'],'D00 config drift')
    for context in CONTEXTS:
        for side in (0,1):
            for arm in ARMS:
                require(digest(LOCAL/'inputs'/f'{context}-{side}-{arm}.bin')==value['setups'][context][str(side)][arm],'Input binary drift')
    return value


def register(commit,ci):
    frozen=verify_frozen();gate=read(PUBLIC/'review-gate.json')
    require(gate['experiment_id']==EXPERIMENT and gate['approved_for_technical'] is True and
            gate['inputs_sha256']==source_hash(PUBLIC/'inputs.json') and gate['review_sha256']==source_hash(ROOT/REVIEW),
            'Independent prepared-input review missing')
    paths=[*CODE,REVIEW,*[f'data/mech-002-sharpness-p0/{n}' for n in ('contract.json','inputs.json','seed-plan.json','review-gate.json')]]
    published(commit,ci,paths)
    config=deepcopy(read(PUBLIC/'contract.json'));config['status']='registered'
    config['preregistration']=dict(commit=commit,document=DOCUMENT,document_sha256=source_hash(ROOT/DOCUMENT),
        analysis='analysis/analyse_sharpness002.py',analysis_sha256=source_hash(ROOT/'analysis/analyse_sharpness002.py'))
    design().validate_design(config,executable=True)
    receipt=dict(config=config,config_sha256=config_hash(config),seeds=read(PUBLIC/'seed-plan.json')['main_seeds'],
        input_review_sha256=source_hash(ROOT/REVIEW),input_review_gate_sha256=source_hash(PUBLIC/'review-gate.json'))
    write_exclusive(LOCAL/'manifest.json',receipt);write_exclusive(PUBLIC/'manifest.json',receipt)
    write_exclusive(PUBLIC/'main-job-plan.json',schedule(receipt))
    write_exclusive(PUBLIC/'technical-job-plan.json',design().technical_jobs(read(PUBLIC/'seed-plan.json')['technical_seeds']))
    write_exclusive(LOCAL/'main-keys.json',[j['key'] for j in schedule(receipt)])


def publication_gate(commit,ci,phase):
    frozen=verify_frozen();receipt=read(LOCAL/'manifest.json');design().validate_design(receipt['config'],executable=True)
    require(receipt==read(PUBLIC/'manifest.json') and receipt['config_sha256']==config_hash(receipt['config']) and
            receipt['input_review_sha256']==source_hash(ROOT/REVIEW) and
            receipt['input_review_gate_sha256']==source_hash(PUBLIC/'review-gate.json'),'Registered intent/review drift')
    expected=deepcopy(read(PUBLIC/'contract.json'));expected['status']='registered'
    expected['preregistration']=receipt['config']['preregistration']
    require(expected==receipt['config'] and receipt['seeds']==seed_plan()['main_seeds'] and
            receipt['config']['design']['setups']==frozen['setups'] and
            receipt['config']['execution']['code_sha256']==frozen['code_sha256'] and
            receipt['config']['execution']['input_manifest_sha256']==source_hash(PUBLIC/'inputs.json') and
            receipt['config']['execution']['seed_plan_sha256']==source_hash(PUBLIC/'seed-plan.json'),
            'Registered contract no longer matches frozen concrete intent')
    names=('contract.json','inputs.json','seed-plan.json','review-gate.json','manifest.json','main-job-plan.json','technical-job-plan.json')
    paths=[*CODE,REVIEW,*[f'data/mech-002-sharpness-p0/{n}' for n in names]]
    if phase=='main':
        release=read(PUBLIC/'technical-release.json');summary=read(PUBLIC/'technical-summary.json')
        require(release['experiment_id']==EXPERIMENT and release['approved_for_main'] is True and summary['passed'] is True and
                summary['budget_reconciled'] is True and summary['complete'] is True and summary['full_matches']==32 and
                summary['negative_rejections']==1 and len(summary['aa_pairs'])==16 and summary['peak_inflight_claims']==4 and
                release['summary_sha256']==source_hash(PUBLIC/'technical-summary.json') and
                release['review_sha256']==source_hash(ROOT/MAIN_REVIEW),'New cold four-worker technical release missing')
        snapshot=LOCAL/'technical-budget.snapshot.json';proof=read(LOCAL/'technical-reconciled.json')
        require(phase_budget_gate('technical',read(snapshot),proof,digest(snapshot),
            {'technical':[j['key'] for j in read(PUBLIC/'technical-job-plan.json')]}),'Private cold technical accounting failed')
        paths.extend([MAIN_REVIEW,*[f'data/mech-002-sharpness-p0/{n}' for n in
            ('technical-release.json','technical-summary.json','technical-budget.json','technical-job-accounting.jsonl')]])
    published(commit,ci,paths)
    return receipt


def main_remaining(inner,night,now):
    require(inner['experiment']==EXPERIMENT and inner['limits']=={'technical':33,'main':512} and
            inner['limit_seconds']==900 and inner['wall_limit_seconds']==3600 and inner['halted'] is False,
            'Own study budget differs/halted')
    active=night['active'];require(active and active['name']==EXPERIMENT+'/main','No outer main admission')
    options=[900-inner['charged_seconds'],(datetime.fromisoformat(inner['wall_deadline_utc'])-now).total_seconds(),
        (datetime.fromisoformat(active['child_deadline_utc'])-now).total_seconds(),
        (datetime.fromisoformat(DEADLINE)-now).total_seconds(),
        1800-night['charged_seconds']-(now-datetime.fromisoformat(active['start_utc'])).total_seconds()]
    if inner['active'] is not None:
        options.append((datetime.fromisoformat(inner['active']['child_deadline_utc'])-now).total_seconds())
    remaining=min(options)-5
    require(remaining>=600,'At least600s remaining own/global allowance required before first main command')
    return remaining


def admission(phase,keys):
    assert_night_admission(ROOT,EXPERIMENT,phase,keys)
    state=read(LOCAL/'budget.json');active=state['active']
    require(state['limits']=={'technical':33,'main':512} and state['limit_seconds']==900 and state['wall_limit_seconds']==3600 and
            not state['halted'] and active and active['name']==phase and active['kind']==phase and active['keys']==keys and
            supervisor_alive(active['supervisor_pid']) and active['token_sha256']==
            sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN','').encode()).hexdigest(),'No authenticated inner phase')
    lease=read(ROOT/'local/global-native/native-execution.lease.json')
    require(lease['owner_pid']==active['supervisor_pid'] and lease['experiment']==EXPERIMENT and lease['workers']==4,'NativeLease4 missing')
    now=datetime.now(timezone.utc)
    seconds=min((datetime.fromisoformat(active['child_deadline_utc'])-now).total_seconds(),
                (datetime.fromisoformat(state['wall_deadline_utc'])-now).total_seconds(),
                (datetime.fromisoformat(DEADLINE)-now).total_seconds())-5
    require(seconds>0,'No bounded native allowance')
    require(sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file())<2*1024**3 and
            shutil.disk_usage(LOCAL).free>20*1024**3,'Private artifact/disk limit')
    return seconds


def native_job(job,phase,keys,frozen,on_start):
    from research.native_process005 import contained_call,confirmed_cleanup,CleanupUnconfirmed
    directory=LOCAL/phase/'jobs'/job['key'];directory.mkdir(parents=True,exist_ok=False)
    pending=directory/'pending.json';write_exclusive(pending,dict(job_id=job['key']))
    private=read(LOCAL/'private-host.json');host=Path(private['observer_host'])
    log=directory/'native.jsonl';dump=directory/'input.json';out=directory/'native.stdout'
    if job.get('kind')=='negative':
        binary=directory/'malformed.bin'
        with binary.open('xb') as stream:stream.write(b'SHARPNESS INVALID HEADER')
    else:
        binary=LOCAL/'inputs'/f"{job['scenario']}-{job['side']}-{job['arm']}.bin"
        require(digest(binary)==job['setup_sha256'],'Frozen input mismatch')
    command=[str(host),'--fixture',str(RUNTIME/'engine/fm27_native/fixtures/match.pkm'),
        '--scenario-file',str(binary),'--dump-input',str(dump),'--output',str(log),'--tick-step','1']
    if job.get('seed') is not None:command.extend(('--seed',str(job['seed'])))
    env={k:v for k,v in os.environ.items() if not k.startswith('FM27_')}
    env.update(FM27_ENGINE_ROOT=str(RUNTIME/'engine'),FM27_GAME_ROOT=str(observer.GAME),
               FM27_EXPECTED_DLL_SHA256=frozen['identity']['engine_sha256'],FM27_PASSIVE_OBSERVER_V1='1')
    try:
        code,elapsed=contained_call(command,env,log,out,timeout=90,on_start=on_start,max_processes=3,
                                    total_timeout=admission(phase,keys))
    except BaseException as error:
        if not confirmed_cleanup(out,expected_limit=3):raise CleanupUnconfirmed(dict(job_id=job['key'])) from error
        pending.unlink();raise
    if not confirmed_cleanup(out,expected_limit=3):raise CleanupUnconfirmed(dict(job_id=job['key']))
    pending.unlink()
    native=dict(returncode=code,native_elapsed_seconds=elapsed,stdout_sha256=digest(out),
        raw_log_sha256=digest(log) if log.exists() else None,input_dump_sha256=digest(dump) if dump.exists() else None,
        containment_receipt_sha256=digest(out.with_suffix('.containment.json')))
    write_exclusive(directory/'native-exit.json',native)
    try:
        require(code==(108 if job.get('kind')=='negative' else 0),'Cold native command returned unexpected exit code')
        evidence=rows(log)
        if job.get('kind')=='negative':
            audit_malformed(evidence,code);value=dict(job_id=job['key'],status='expected_rejection')
        else:
            require(dump.exists(),'Cold input dump missing')
            config=deepcopy(read(LOCAL/'configs.json')[f"{job['scenario']}-{job['side']}"])
            config['teams'][job['side']]['instructions']['10']=2000905329 if treatment(job['arm'])[1] else 1313689463
            value=audit_job(evidence,read(dump),job,binary.read_bytes(),config,
                read(RUNTIME/'source/tactics_ui/catalog.json'),frozen['oop_map'],
                frozen['frozen_controls'][f"{job['scenario']}-{job['side']}"],digest(host))
    except BaseException as error:
        error.native_evidence=native;raise
    value.update(native)
    return value


def execute(phase,publication,ci):
    receipt=publication_gate(publication,ci,phase);frozen=verify_frozen()
    plan=read(PUBLIC/(phase+'-job-plan.json'))
    expected=schedule(receipt) if phase=='main' else design().technical_jobs(read(PUBLIC/'seed-plan.json')['technical_seeds'])
    require(plan==expected,'Published schedule drift')
    keys=[j['key'] for j in plan];admission(phase,keys)
    # Own readonly Windows handles; no foreign Python module is imported.
    leases=ReadLeases()
    private=read(LOCAL/'private-host.json');host=Path(private['observer_host']);fixture=RUNTIME/'engine/fm27_native/fixtures/match.pkm'
    try:
        for path in [*observer.resource_paths().values(),host,fixture,LOCAL/'configs.json',Path(private['build_manifest']),
                     host.parent/'desktop_host.cpp',host.parent/'passive_observer_v1.h',RUNTIME/'source/tactics_ui/catalog.json',*LOCAL.glob('inputs/*.bin')]:
            leases.lease(path)
        require(digest(host)==OBSERVER_HOST and digest(fixture)==frozen['identity']['fixture_sha256'] and
                observer.fingerprint()==frozen['identity']['resource_fingerprint'] and
                digest(private['build_manifest'])==frozen['build_manifest_sha256'],'Locked native identity drift')
        build=read(private['build_manifest'])
        require(digest(host.parent/'desktop_host.cpp')==build['modified_host_source_sha256'] and
                digest(host.parent/'passive_observer_v1.h')==build['observer_header_sha256'] and
                source_hash(host.parent/'passive_observer_v1.h')==source_hash(ROOT/'adapters/passive_observer_v1.h'),
                'Locked observer source/header drift')
        require(source_hash(RUNTIME/'source/desktop_engine.py')==frozen['lease_module_sha256'] and
                all(source_hash(RUNTIME/'source'/n)==h for n,h in frozen['runtime_source_sha256'].items()) and
                digest(RUNTIME/'source/tactics_ui/catalog.json')==frozen['catalog_sha256'],'Runtime/catalog drift')
        require(config_hash(read(LOCAL/'configs.json'))==frozen['configs_sha256'],'Locked configs drift')
        for context in CONTEXTS:
            for side in (0,1):
                for arm in ARMS:
                    require(digest(LOCAL/'inputs'/f'{context}-{side}-{arm}.bin')==frozen['setups'][context][str(side)][arm],'Locked input drift')
        for job in plan:
            if job.get('kind')!='negative':
                job.update(identity=frozen['identity'],config_sha256=receipt['config_sha256'],
                           setup_sha256=frozen['setups'][job['scenario']][str(job['side'])][job['arm']])
        aa=[]
        def check_block(block):
            if phase!='technical' or block[0].get('kind')=='negative':return
            for arm in ARMS:
                pair=sorted((j for j in block if j['arm']==arm),key=lambda j:j['repeat'])
                require(len(pair)==2,'A/A pair incomplete')
                logs=[rows(LOCAL/phase/'jobs'/j['key']/'native.jsonl') for j in pair]
                aa.append(dict(context=pair[0]['scenario'],side=pair[0]['side'],arm=arm,
                               **repeat_equivalence(logs[0],logs[1],pair[0]['seed'])))
        if phase=='main':main_remaining(read(LOCAL/'budget.json'),read(ROOT/'local/night-001/program-budget.json'),datetime.now(timezone.utc))
        scheduler=ColdScheduler(LOCAL/phase/'dispatch',lambda j,on:native_job(j,phase,keys,frozen,on),
                                lambda j:admission(phase,keys),check_block)
        data=scheduler.run(block_jobs(plan,technical=phase=='technical'))
        require(len(data)==(33 if phase=='technical' else 512),'Complete phase required')
        require(scheduler.peak<=4 and (phase!='technical' or scheduler.peak==4 and len(aa)==16),
                'Cold four-worker A/A coverage missing')
        write_exclusive(LOCAL/(phase+'-summary.json'),dict(passed=True,phase=phase,
            full_matches=32 if phase=='technical' else 512,negative_rejections=1 if phase=='technical' else 0,
            aa_pairs=aa,peak_inflight_claims=scheduler.peak,engine_pid_peak_measured=False,
            dispatch_summary_sha256=digest(LOCAL/phase/'dispatch/dispatch-summary.json'),
            concurrency_ledger_sha256=digest(LOCAL/phase/'dispatch/concurrency.jsonl'),
            scientific_analysis_allowed=phase=='main',career_released=False))
    finally:leases.close_leases()


def supervise(phase,publication,ci):
    receipt=publication_gate(publication,ci,phase)
    plan=read(PUBLIC/(phase+'-job-plan.json'));keys=[j['key'] for j in plan]
    if phase=='main':require((LOCAL/'budget.json').exists(),'Technical study window must already exist')
    budget=DeadlineBudget(LOCAL/'budget.json',experiment=EXPERIMENT,seconds=900,
                          caps={'technical':33,'main':512},wall_seconds=3600)
    state=budget.load()
    require(not (LOCAL/(phase+'.stdout')).exists() and not (LOCAL/(phase+'.lease.json')).exists(),'Retained phase: no retry')
    if phase=='main':main_remaining(state,read(ROOT/'local/night-001/program-budget.json'),datetime.now(timezone.utc))
    lease=NativeLease(ROOT/'local/global-native',EXPERIMENT,workers=4).acquire()
    try:
        owner=lease.assert_owned();write_exclusive(LOCAL/(phase+'.lease.json'),
            {k:owner[k] for k in ('schema','experiment','workers','owner_pid','acquired_utc')})
        command=[sys.executable,str(Path(__file__).resolve()),phase,'--child','--publication',publication,'--ci-run',str(ci)]
        budget.run(phase,phase,keys,command,ROOT,LOCAL/(phase+'.stdout'))
    finally:
        state=budget.load()
        if state['active'] or list((LOCAL/phase/'jobs').glob('*/pending.json')):
            state.update(halted=True,cleanup_unconfirmed=True,global_native_lease_retained=True);atomic(budget.path,state)
        else:lease.release()
    require(state['halted'] is False and state['active'] is None,'Phase did not reconcile successfully')
    snapshot=LOCAL/(phase+'-budget.snapshot.json')
    with snapshot.open('xb') as stream:stream.write(budget.path.read_bytes());stream.flush();os.fsync(stream.fileno())
    write_exclusive(LOCAL/(phase+'-reconciled.json'),dict(experiment_id=EXPERIMENT,phase=phase,
        completed_utc=datetime.now(timezone.utc).isoformat(),budget_sha256=digest(snapshot),
        publication_commit=publication,ci_run=ci))


def phase_budget_gate(phase,state,reconciliation,snapshot_sha,expected_keys):
    """Success needs complete parent accounting and actual UTC completion."""
    try:
        expected_phases=['technical'] if phase=='technical' else ['technical','main']
        require(state['experiment']==EXPERIMENT and state['limits']=={'technical':33,'main':512} and
                state['limit_seconds']==900 and state['wall_limit_seconds']==3600 and state['halted'] is False and
                state['active'] is None and not state.get('cleanup_unconfirmed') and
                not state.get('global_native_lease_retained'),'Phase budget not reconciled')
        operations=state['operations'];require([o['name'] for o in operations]==expected_phases,'Missing/duplicate operation')
        require(all(o['kind']==o['name'] and type(o['returncode']) is int and o['returncode']==0 and o['timed_out'] is False and
                    type(o['elapsed_seconds']) in (int,float) and 0<o['elapsed_seconds']<=900 for o in operations),'Failed/unknown operation')
        require(type(state['charged_seconds']) in (int,float) and
                state['charged_seconds']==sum(o['elapsed_seconds'] for o in operations)<=900,'Refunded/exceeded child time')
        require(all(o['keys']==expected_keys[o['name']] and len(set(o['keys']))==len(o['keys']) for o in operations),
                'Reserved phase keys differ from the complete published plan')
        reserved={key:o['kind'] for o in operations for key in o['keys']}
        require(state['reserved']==reserved and sum(v=='technical' for v in reserved.values())==33 and
                sum(v=='main' for v in reserved.values())==(512 if phase=='main' else 0),'Reservation count/refund mismatch')
        start=datetime.fromisoformat(state['wall_start_utc']);end=datetime.fromisoformat(state['wall_deadline_utc'])
        finish=datetime.fromisoformat(reconciliation['completed_utc'])
        require(all(value.utcoffset()==timedelta(0) for value in (start,end,finish)),'UTC time evidence missing')
        require(end-start==timedelta(seconds=3600) and start<finish<=end and finish<=datetime.fromisoformat(DEADLINE),
                'Actual fixed UTC window exceeded')
        require(reconciliation['experiment_id']==EXPERIMENT and reconciliation['phase']==phase and
                reconciliation['budget_sha256']==snapshot_sha,'Final reconciliation mismatch')
        for op in operations:
            begin=datetime.fromisoformat(op['start_utc']);deadline=datetime.fromisoformat(op['child_deadline_utc'])
            require(begin.utcoffset()==deadline.utcoffset()==timedelta(0) and start<=begin<deadline<=end and
                    (deadline-begin).total_seconds()<=900 and (finish-begin).total_seconds()>=op['elapsed_seconds'],
                    'Operation actual/deadline timing evidence invalid')
        return True
    except (KeyError,TypeError,ValueError,OverflowError):return False


def optional(path):
    try:return read(path)
    except (OSError,ValueError):return None


def safe_budget(state,known_keys):
    """Unknown duration is null; retain raw recorded charges, never private fields."""
    def numeric(value):
        try:return value if type(value) in (int,float) and math.isfinite(value) else None
        except OverflowError:return None
    def utc(value):
        try:
            parsed=datetime.fromisoformat(value)
            return parsed.isoformat() if parsed.utcoffset()==timedelta(0) else None
        except (TypeError,ValueError):return None
    def operation(value):
        if type(value) is not dict:return None
        keys=value.get('keys')
        return dict(name=value.get('name') if value.get('name') in ('technical','main') else None,
            kind=value.get('kind') if value.get('kind') in ('technical','main') else None,
            keys=[k for k in keys if type(k) is str and k in known_keys] if type(keys) is list else None,
            start_utc=utc(value.get('start_utc')),child_deadline_utc=utc(value.get('child_deadline_utc')),
            elapsed_seconds=numeric(value.get('elapsed_seconds')),
            returncode=value.get('returncode') if type(value.get('returncode')) is int else None,
            timed_out=value.get('timed_out') if type(value.get('timed_out')) is bool else None)
    if type(state) is not dict:state={}
    return dict(recorded_charged_seconds=numeric(state.get('charged_seconds')),
        active=operation(state.get('active')),halted=state.get('halted') if type(state.get('halted')) is bool else None,
        operations=[operation(o) for o in state['operations']] if type(state.get('operations')) is list else None,
        wall_start_utc=utc(state.get('wall_start_utc')),wall_deadline_utc=utc(state.get('wall_deadline_utc')))


def export(phase):
    require(phase in ('technical','main'),'Explicit phase required')
    plan=read(PUBLIC/(phase+'-job-plan.json'));directory=LOCAL/phase/'dispatch'
    data=rows(directory/'ledger.jsonl') if (directory/'ledger.jsonl').exists() else []
    actual={r['job_id']:r for r in data};require(len(actual)==len(data),'Duplicate ledger attempts')
    require(not set(actual)-{j['key'] for j in plan},'Unexpected ledger attempt')
    accounting=[]
    for job in plan:
        row=actual.get(job['key']);status=row['status'] if row else 'started_unresolved' if (directory/(job['key']+'.started.json')).exists() else 'not_started'
        admission_failure=directory/(job['key']+'.admission-failure.json')
        accounting.append(dict(job_id=job['key'],seed=job.get('seed'),status=status,
            admission_error_type=read(admission_failure).get('error_type') if admission_failure.exists() else None))
        if row and row.get('raw_log_sha256'):
            raw=LOCAL/phase/'jobs'/job['key']
            require(digest(raw/'native.jsonl')==row['raw_log_sha256'],'Raw native evidence changed')
            require(digest((raw/'native.stdout').with_suffix('.containment.json'))==row['containment_receipt_sha256'],'Cleanup receipt changed')
            if row.get('input_dump_sha256'):require(digest(raw/'input.json')==row['input_dump_sha256'],'Input dump changed')
    summary=read(LOCAL/(phase+'-summary.json')) if (LOCAL/(phase+'-summary.json')).exists() else dict(passed=False)
    snapshot=LOCAL/(phase+'-budget.snapshot.json');proof=LOCAL/(phase+'-reconciled.json')
    state=optional(snapshot);reconciliation=optional(proof)
    expected_keys={name:[j['key'] for j in read(PUBLIC/(name+'-job-plan.json'))]
                   for name in (('technical',) if phase=='technical' else ('technical','main'))}
    good=bool(state and reconciliation and phase_budget_gate(phase,state,reconciliation,digest(snapshot),expected_keys))
    complete=(len(data)==len(plan)==(33 if phase=='technical' else 512) and
              all(actual[j['key']]['status']==('expected_rejection' if j.get('kind')=='negative' else 'ok') for j in plan))
    if summary.get('passed') is True:
        require(digest(directory/'dispatch-summary.json')==summary['dispatch_summary_sha256'] and
                digest(directory/'concurrency.jsonl')==summary['concurrency_ledger_sha256'],'Concurrency evidence changed')
    passed=summary.get('passed') is True and good and complete and not list((LOCAL/phase/'jobs').glob('*/pending.json'))
    summary.update(passed=passed,budget_reconciled=good,complete=complete,scientific_analysis_allowed=phase=='main' and passed,
                   career_released=False)
    PUBLIC.mkdir(parents=True,exist_ok=True)
    (PUBLIC/(phase+'-job-accounting.jsonl')).write_text(''.join(json.dumps(r)+'\n' for r in accounting),encoding='utf8')
    if summary['passed']:
        text=''.join(json.dumps(r,allow_nan=False)+'\n' for r in data if r['status']=='ok')
        target=PUBLIC/('main.jsonl' if phase=='main' else 'technical.jsonl')
        if target.exists():require(target.read_text(encoding='utf8')==text,'Published raw rows changed')
        else:target.write_text(text,encoding='utf8')
    write(PUBLIC/(phase+'-summary.json'),summary)
    safe=safe_budget(state if state is not None else optional(LOCAL/'budget.json'),
                     {j['key'] for name in expected_keys for j in read(PUBLIC/(name+'-job-plan.json'))})
    safe.update(passed=good,charged_seconds=state['charged_seconds'] if good else None,charged_seconds_incomplete=not good,
        limits={'technical':33,'main':512},
        limit_seconds=900,wall_limit_seconds=3600,budget_sha256=digest(snapshot) if snapshot.exists() else None,
        completed_utc=reconciliation.get('completed_utc') if good else None)
    write(PUBLIC/(phase+'-budget.json'),safe)


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare','register','technical','main','export'))
    parser.add_argument('--publication');parser.add_argument('--ci-run',type=int);parser.add_argument('--child',action='store_true')
    parser.add_argument('--export-phase',choices=('technical','main'));args=parser.parse_args()
    require((ROOT/'.git').is_dir(),'Central checkout execution only')
    if args.phase=='register':register(args.publication,args.ci_run);return
    if args.phase=='export':export(args.export_phase);return
    keys=[] if args.phase=='prepare' else [j['key'] for j in read(PUBLIC/(args.phase+'-job-plan.json'))]
    assert_night_admission(ROOT,EXPERIMENT,args.phase,keys)
    if args.phase=='prepare':require(not args.child,'No prepare child');prepare();return
    if args.child:execute(args.phase,args.publication,args.ci_run)
    else:supervise(args.phase,args.publication,args.ci_run)


if __name__=='__main__':main()

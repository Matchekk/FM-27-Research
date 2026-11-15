"""Fixed NIGHT-003 two-player positional sharpness study; reuse released codecs and containment.

No historical budget is modified. No native setter, warm host or career import.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.pycache_prefix = str(ROOT/'local/night-003/import-cache'/uuid.uuid4().hex)
sys.dont_write_bytecode = True
from analysis import run_observer005 as observer
from analysis.stless003_design import build_inputs, validate_cells
from analysis.startpolicy002_gate import compile_cell, lineup_slots, cache_bytes, repeat_equivalence
from research.passive_observer import snapshot
from analysis.sharpness002_runner import ColdScheduler, ReadLeases, initial_controls, descriptive, write_exclusive
from analysis.run_startpolicy002 import audit_malformed
from research.budget import supervisor_alive, atomic
from research.coordination import NativeLease
from research.core import allocate, historical_seeds, config_hash
from research.native import read, rows, digest, require, event
from research.passive_observer import audit_trace, match_result
from research.study_budget import DeadlineBudget

ID = 'N3-SHARPPOS-C1'
PUB = ROOT/'data/night-003-sharppos'
LOC = ROOT/'local/night-003/sharppos'
RUNTIME = ROOT/'local/runtime-v1114.6'
ARMS = ('ATTACK_LOW','DEFENCE_LOW')
CONTEXTS = ('high_press','deep_block')
N = 512
HOST = '58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
CAPS = {'technical':17,'main':4096}
CHILD_SECONDS = 7200
WALL_SECONDS = 10800
CODE = ('analysis/night003_pos.py','analysis/analyse_night003_pos.py','tests/test_night003_pos.py',
        'experiments/N3-SHARPPOS-C1.md','docs/night-003/LITERATURE_POS.md',
        'analysis/stless003_design.py','analysis/startpolicy002_gate.py',
        'analysis/sharpness002_runner.py','analysis/run_observer005.py',
        'analysis/run_startpolicy002.py','research/native_process005.py',
        'research/startpolicy.py','research/passive_observer.py','research/coordination.py',
        'research/budget.py','research/study_budget.py','research/core.py','research/native.py','research/stats.py')

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    write_exclusive(path, value)

def target_slots(arm):
    require(arm in ARMS,'Unknown arm')
    return (8,10) if arm=='ATTACK_LOW' else (2,3)

def jobs(phase, seeds):
    if phase == 'technical':
        out = [dict(key=f'tech-{h}-{s}-{a}-{r}',scenario=h,side=s,arm=a,repeat=r,seed=seeds[i],kind='full')
               for i,(h,s) in enumerate(product(CONTEXTS,(0,1))) for a,r in product(ARMS,(0,1))]
        return out+[dict(key='negative-malformed',kind='negative',seed=None)]
    require(phase=='main' and len(seeds)==2*N,'Main seed count')
    out = [dict(key=f'{h}-{seed}-{s}-{a}',scenario=h,side=s,arm=a,seed=seed,kind='full')
           for i,h in enumerate(CONTEXTS) for seed in seeds[i*N:(i+1)*N] for s,a in product((0,1),ARMS)]
    # Shuffle complete blocks only; both sides and both arms remain together.
    import random
    blocks=group_jobs(out); random.Random(2026111504).shuffle(blocks)
    return [j for b in blocks for j in b]

def group_jobs(plan,technical=False):
    grouped={};negative=[]
    for j in plan:
        if j['kind']=='negative':negative.append(j);continue
        key=(j['scenario'],j['seed'],j['side']) if technical else (j['scenario'],j['seed'])
        grouped.setdefault(key,[]).append(j)
    require(all(len(b)==4 for b in grouped.values()),'Four complete calls per block')
    return list(grouped.values())+([negative] if negative else [])

def audit_positional_start(evidence,binary,side,arm):
    slots=lineup_slots(binary);targets={slots[side,i] for i in target_slots(arm)}
    starters={(s,slots[s,i]) for s in (0,1) for i in range(11)}
    captures=[r for r in evidence if r.get('event')=='native_passive_state']
    require([r['stage'] for r in captures]==['prepared','first_advance','finished'],'Three captures required')
    for r in captures[:2]:
        players=snapshot(r)
        require({(p['side'],p['roster_index']) for p in players.values()}=={(s,i) for s in (0,1) for i in range(23)},'All46actors required')
        count=0
        for p in players.values():
            affected=p['side']==side and p['roster_index'] in targets
            expected=7000 if affected else 10000
            require(p['sharpness_raw']==p['sharpness_secondary_raw']==expected,'Wrong positional raw sharpness')
            require(p['condition_raw']==10000 and p['fatigue_raw']==0 and p['condition_accumulator_raw']==1000000 and
                    p['sharpness_penalty_raw']==0,'Other start state changed')
            if (p['side'],p['roster_index']) in starters:
                require(cache_bytes(p)==(100,70 if affected else 100),'Wrong identity-bound starter cache')
            count+=affected
        require(count==2,'Exactly two declared positional actors required')

def prepare():
    require(not LOC.exists() and not (PUB/'inputs.json').exists(),'Retained study; no reset')
    prior=read(ROOT/'data/valid-005-observer-v1/inputs.json')
    private=read(ROOT/'local/valid005-observer-v1/private-host.json')
    require(digest(private['observer_host'])==HOST,'Host drift')
    require(observer.fingerprint()==prior['identity']['resource_fingerprint'],'Resource/build drift')
    require(digest(RUNTIME/'engine/fm27_native/fixtures/match.pkm')==prior['identity']['fixture_sha256'],'Fixture drift')
    require(digest(RUNTIME/'source/tactics_ui/catalog.json')==prior['catalog_sha256'],'Catalog drift')
    require(all(observer.source_hash(RUNTIME/'source'/n)==v for n,v in prior['runtime_source_sha256'].items()),'Runtime source drift')
    catalog=read(RUNTIME/'source/tactics_ui/catalog.json')
    baseline=read(ROOT/'local/valid005-observer-v1/configs.json')
    require(config_hash(baseline)==prior['configs_sha256'],'Baseline drift')
    configs={}; setups={}; controls={}; diffs={}
    from research.startpolicy import decode_records
    for h,s in product(CONTEXTS,(0,1)):
        label=f'{h}-{s}'; original=ROOT/'local/valid005-observer-v1/inputs'/(label+'.bin')
        require(digest(original)==prior['setups'][label],'D00 drift')
        raw=original.read_bytes()
        # Reuse the released baseline and full ten-player compiler; select only
        # the two declared existing profile bindings before preparation.
        build_inputs(raw,s,baseline[label],catalog,prior['oop_map'])
        configs[label]={a:deepcopy(baseline[label]) for a in ARMS}
        controls[label]=initial_controls(rows(ROOT/'local/valid005-observer-v1/technical'/(label+'-observer_on.jsonl')))
        setups[label]={}; diffs[label]={}
        from research.startpolicy import encode_records
        from analysis.startpolicy002_gate import lineup_slots
        slots=lineup_slots(raw)
        low,_=compile_cell(raw,s,7000)
        for a in ARMS:
            targets={slots[s,i] for i in target_slots(a)}
            records=tuple(after if before[0]==15 and before[1]==s and before[2] in targets and before[3] in (16,17)
                          else before for before,after in zip(decode_records(raw),decode_records(low),strict=True))
            payload=encode_records(records)
            delta=[(x,y) for x,y in zip(decode_records(raw),records,strict=True) if x!=y]
            require(len(delta)==4 and all(x[:4]==y[:4] and x[0]==15 and x[1]==s and x[2] in targets and
                        x[3] in (16,17) and x[4]==10000 and y[4]==7000 for x,y in delta),'Undeclared positional sharpness delta')
            require([(configs[label][a]['teams'][s]['phases'][0][i]['position']) for i in target_slots(a)]==
                    (['AMC','ST'] if a=='ATTACK_LOW' else ['DCR','DCL']),'Declared position group drift')
            path=LOC/'inputs'/f'{label}-{a}.bin';path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(payload)
            setups[label][a]=digest(path);diffs[label][a]=dict(changed_records=4,target_start_slots=list(target_slots(a)),level_raw=7000)
    # The shared registry includes terminal, failed and never-run reservations.
    used={0}
    for directory in (ROOT/'data').iterdir():
        if directory.is_dir() and directory!=PUB: used.update(historical_seeds(directory))
    for path in (ROOT/'local/registry').glob('*.json'):
        used.update(read(path).get('seeds',[]))
        # Historical reservation schemas may nest seed arrays.
    used.update(historical_seeds(ROOT/'local/registry'))
    for directory in (ROOT/'local').iterdir():
        if directory.is_dir() and directory.name!='night-003' and directory.name.startswith(('valid','tact-','attr-','mech-','night-','platform-smoke')):
            # Avoid massive raw evidence: only immutable seed plans/manifests are needed.
            for path in directory.rglob('*seed*.json'):
                def collect(v, flag=False):
                    if isinstance(v,dict):
                        for k,x in v.items():collect(x,flag or 'seed' in k)
                    elif isinstance(v,list):
                        for x in v:collect(x,flag)
                    elif flag and type(v) is int:used.add(v)
                collect(read(path))
    seeds=allocate(ID+'/main-v1',2*N+4,used)
    plan=dict(experiment_id=ID,namespace=ID+'/main-v1',main_seeds=seeds[:2*N],technical_seeds=seeds[2*N:],seeds=seeds,
              prior_unique_seeds=len(used),overlap=0)
    reservation=ROOT/'local/registry'/(ID+'.reserved.json');write(reservation,plan)
    write(LOC/'configs.json',configs);write(LOC/'private-host.json',private)
    write(PUB/'seed-plan.json',plan)
    frozen=dict(experiment_id=ID,identity=prior['identity'],observer_host_sha256=HOST,oop_map=prior['oop_map'],
        build_manifest_sha256=prior['build_manifest_sha256'],catalog_sha256=prior['catalog_sha256'],
        runtime_source_sha256=prior['runtime_source_sha256'],setups=setups,controls=controls,
        configs_sha256=config_hash(configs),diffs=diffs,code_sha256={n:observer.source_hash(ROOT/n) for n in CODE},
        seed_plan_sha256=observer.source_hash(PUB/'seed-plan.json'),
        mission_deadline_utc=read(ROOT/'local/night-003/sharpstruct/budget.json')['wall_deadline_utc'],
        limits=dict(caps=CAPS,child_seconds=CHILD_SECONDS,wall_seconds=WALL_SECONDS,raw_bytes=16*1024**3,disk_reserve_bytes=20*1024**3,
                    absolute_call_timeout=30,processes_per_call=3,workers=4))
    write(PUB/'inputs.json',frozen)
    for phase in ('technical','main'):write(PUB/(phase+'-plan.json'),jobs(phase,plan[phase+'_seeds']))
    print('Prepared positional inputs and reserved 1028 new seeds; no native calls.',flush=True)

def verify():
    f=read(PUB/'inputs.json');p=read(LOC/'private-host.json');host=Path(p['observer_host']);build=read(p['build_manifest'])
    require(all(observer.source_hash(ROOT/n)==h for n,h in f['code_sha256'].items()),'Frozen code drift')
    require(observer.source_hash(PUB/'seed-plan.json')==f['seed_plan_sha256'],'Seed plan drift')
    require(read(PUB/'seed-plan.json')==read(ROOT/'local/registry'/(ID+'.reserved.json')),'Registry drift')
    require(digest(host)==HOST and digest(p['build_manifest'])==f['build_manifest_sha256'],'Host/build drift')
    require(digest(host.parent/'desktop_host.cpp')==build['modified_host_source_sha256'] and
            digest(host.parent/'passive_observer_v1.h')==build['observer_header_sha256'],'Host source drift')
    require(observer.fingerprint()==f['identity']['resource_fingerprint'] and
            digest(RUNTIME/'engine/fm27_native/fixtures/match.pkm')==f['identity']['fixture_sha256'],'Resource drift')
    require(config_hash(read(LOC/'configs.json'))==f['configs_sha256'],'Config drift')
    require(digest(RUNTIME/'source/tactics_ui/catalog.json')==f['catalog_sha256'] and
            all(observer.source_hash(RUNTIME/'source'/n)==v for n,v in f['runtime_source_sha256'].items()),'Runtime drift')
    for label,arms in f['setups'].items():
        for a,h in arms.items():require(digest(LOC/'inputs'/f'{label}-{a}.bin')==h,'Binary drift')
    return f

def publication(commit,ci):
    observer.successful_ci(commit,ci)
    for name in (*CODE,'data/night-003-sharppos/inputs.json','data/night-003-sharppos/seed-plan.json',
        'data/night-003-sharppos/technical-plan.json','data/night-003-sharppos/main-plan.json'):
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(blob.replace(b'\r\n',b'\n')==(ROOT/name).read_bytes().replace(b'\r\n',b'\n'),'Publication drift '+name)
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/codex/night-003'],cwd=ROOT,text=True).split()[0]
    subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=ROOT,check=True)

def admission(phase):
    state=read(LOC/'budget.json');active=state['active'];now=datetime.now(timezone.utc)
    require(not state['halted'] and active and active['name']==phase and supervisor_alive(active['supervisor_pid']) and
        active['token_sha256']==sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN','').encode()).hexdigest(),'Supervisor missing')
    lease=read(ROOT/'local/global-native/native-execution.lease.json')
    require(lease['owner_pid']==active['supervisor_pid'] and lease['experiment']==ID and lease['workers']==4,'Lease missing')
    mission_deadline=read(ROOT/'local/night-003/sharpstruct/budget.json')['wall_deadline_utc']
    require(mission_deadline==read(PUB/'inputs.json')['mission_deadline_utc'],'Fixed mission deadline changed')
    remaining=min((datetime.fromisoformat(mission_deadline)-now).total_seconds(),
                  (datetime.fromisoformat(active['child_deadline_utc'])-now).total_seconds(),
                  (datetime.fromisoformat(state['wall_deadline_utc'])-now).total_seconds())-5
    require(remaining>=40,'No call envelope remaining')
    require(shutil.disk_usage(LOC).free>20*1024**3,'Disk reserve')
    return min(30,remaining-10)

def audit(evidence,dump,job,binary,config,f):
    require(event(evidence,'native_image_fingerprint')['sha256']==f['identity']['engine_sha256'],'Loaded engine drift')
    require(event(evidence,'native_engine_compatibility')['compatible'] is True and
            event(evidence,'windows_load_returned')['success'] is True,'Loader failed')
    require(not any(r.get('event') in ('invalid_role_context','scenario_rejected') for r in evidence),'Native legality failed')
    require(len([r for r in evidence if r.get('event')=='native_phase_configuration'])==4,'Phase receipts missing')
    validate_cells(config,job['side'],read(RUNTIME/'source/tactics_ui/catalog.json'))
    counts=observer.audit_input(evidence,dump,config,binary,read(RUNTIME/'source/tactics_ui/catalog.json'),f['oop_map'])
    audit_trace(evidence,dump,job['seed']);audit_positional_start(evidence,binary,job['side'],job['arm'])
    require(initial_controls(evidence)==f['controls'][f"{job['scenario']}-{job['side']}"],'Nonsharpness controls drift')
    require(all(p['attributes'][52]==60 for team in dump['teams'] for p in team['players']),'Stamina drift')
    require(config['teams'][job['side']]['instructions']['10']==1313689463,'Pressing drift')
    values,missing=descriptive(evidence,binary,job['side'])
    return dict(experiment_id=ID,job_id=job['key'],context=job['scenario'],seed=job['seed'],team_side=job['side'],arm=job['arm'],
        status='ok',identity=f['identity'],observer_host_sha256=HOST,setup_sha256=job['setup_sha256'],
        config_sha256=f['configs_sha256'],result={k:v for k,v in match_result(evidence,job['seed']).items() if k!='seed'},
        native_audit=dict(input_verified=True,start_state_verified=True,controls_verified=True,game_rules_verified=True,target_start_slots=list(target_slots(job['arm'])),**counts),
        descriptive=values,descriptive_missing_reasons=missing)

def native_job(job,phase,f,on_start):
    from research.native_process005 import contained_call,confirmed_cleanup,CleanupUnconfirmed
    directory=LOC/phase/'jobs'/job['key'];directory.mkdir(parents=True,exist_ok=False)
    pending=directory/'pending.json';write(pending,dict(job_id=job['key']))
    private=read(LOC/'private-host.json');log=directory/'native.jsonl';out=directory/'native.stdout';dump=directory/'input.json'
    negative=job['kind']=='negative'
    binary=directory/'malformed.bin' if negative else LOC/'inputs'/f"{job['scenario']}-{job['side']}-{job['arm']}.bin"
    if negative:binary.write_bytes(b'NIGHT003 INVALID HEADER')
    else:require(digest(binary)==job['setup_sha256'],'Input drift')
    command=[private['observer_host'],'--fixture',str(RUNTIME/'engine/fm27_native/fixtures/match.pkm'),
             '--scenario-file',str(binary),'--dump-input',str(dump),'--output',str(log),'--tick-step','1']
    if not negative:command.extend(('--seed',str(job['seed'])))
    env={k:v for k,v in os.environ.items() if not k.startswith('FM27_')}
    env.update(FM27_ENGINE_ROOT=str(RUNTIME/'engine'),FM27_GAME_ROOT=str(observer.GAME),
               FM27_EXPECTED_DLL_SHA256=f['identity']['engine_sha256'],FM27_PASSIVE_OBSERVER_V1='1')
    try:code,elapsed=contained_call(command,env,log,out,timeout=90,on_start=on_start,max_processes=3,total_timeout=admission(phase))
    except BaseException:
        if not confirmed_cleanup(out,expected_limit=3):raise CleanupUnconfirmed(dict(job_id=job['key']))
        pending.unlink();raise
    require(confirmed_cleanup(out,expected_limit=3),'Cleanup unconfirmed')
    pending.unlink()
    native=dict(returncode=code,native_elapsed_seconds=elapsed,raw_log_sha256=digest(log) if log.exists() else None,
                input_dump_sha256=digest(dump) if dump.exists() else None,
                containment_receipt_sha256=digest(out.with_suffix('.containment.json')))
    write(directory/'native-exit.json',native)
    require(code==(108 if negative else 0),'Unexpected native exit')
    evidence=rows(log)
    if negative:audit_malformed(evidence,code);value=dict(job_id=job['key'],status='expected_rejection')
    else:value=audit(evidence,read(dump),job,binary.read_bytes(),read(LOC/'configs.json')[f"{job['scenario']}-{job['side']}"][job['arm']],f)
    value.update(native);return value

def execute(phase):
    f=verify();plan=read(PUB/(phase+'-plan.json'));p=read(PUB/'seed-plan.json')
    require(plan==jobs(phase,p[phase+'_seeds']),'Plan drift')
    if phase=='main':require(read(PUB/'technical-release.json')['passed'] is True,'Technical release missing')
    private=read(LOC/'private-host.json');host=Path(private['observer_host']);leases=ReadLeases();aa=[];raw_size=0
    try:
        for path in [*observer.resource_paths().values(),host,Path(private['build_manifest']),host.parent/'desktop_host.cpp',
                     host.parent/'passive_observer_v1.h',RUNTIME/'engine/fm27_native/fixtures/match.pkm',
                     RUNTIME/'source/tactics_ui/catalog.json',LOC/'configs.json',*LOC.glob('inputs/*.bin')]:leases.lease(path)
        verify();admission(phase)
        for job in plan:
            if job['kind']!='negative':job['setup_sha256']=f['setups'][f"{job['scenario']}-{job['side']}"][job['arm']]
        def check(block):
            nonlocal raw_size
            if phase=='technical' and block[0]['kind']!='negative':
                for a in ARMS:
                    pair=sorted([j for j in block if j['arm']==a],key=lambda j:j['repeat'])
                    aa.append(dict(context=pair[0]['scenario'],side=pair[0]['side'],arm=a,
                        **repeat_equivalence(*[rows(LOC/phase/'jobs'/j['key']/'native.jsonl') for j in pair],pair[0]['seed'])))
            raw_size+=sum(p.stat().st_size for j in block for p in (LOC/phase/'jobs'/j['key']).iterdir() if p.is_file())
            require(raw_size<16*1024**3,'Raw artifact cap')
            print(json.dumps(dict(phase=phase,completed=len(scheduler.results),planned=len(plan),raw_bytes=raw_size,
                                  utc=datetime.now(timezone.utc).isoformat())),flush=True)
        scheduler=ColdScheduler(LOC/phase/'dispatch',lambda j,on:native_job(j,phase,f,on),lambda j:admission(phase),check)
        result=scheduler.run(group_jobs(plan,technical=phase=='technical'))
        require(len(result)==CAPS[phase] and (phase!='technical' or len(aa)==8),'Incomplete phase')
        write(LOC/(phase+'-summary.json'),dict(passed=True,planned=len(plan),completed=len(result),aa_pairs=aa,
            peak_inflight_claims=scheduler.peak,utc=datetime.now(timezone.utc).isoformat()))
    finally:leases.close_leases()

def supervise(phase,commit,ci):
    publication(commit,ci);verify()
    require(read(ROOT/'data/night-003-sharpstruct/main-summary.json')['passed'] is True and
            read(ROOT/'data/night-003-sharpstruct/effects.json')['n_matches']==4096 and
            read(ROOT/'data/night-003-sharpstruct/independent-recalculation.json')['passed'] is True,
            'First scientific study must be complete and analysed before another native phase')
    require(not (LOC/(phase+'.stdout')).exists(),'No phase retry')
    if phase=='main':
        deadline=read(PUB/'inputs.json')['mission_deadline_utc']
        require((datetime.fromisoformat(deadline)-datetime.now(timezone.utc)).total_seconds()>=4200,
                'Need4200s remaining mission window before4096 main matches')
        release=read(PUB/'technical-release.json')
        require(release['passed'] is True and release['summary_sha256']==observer.source_hash(PUB/'technical-summary.json'),'Technical release drift')
    budget=DeadlineBudget(LOC/'budget.json',ID,CHILD_SECONDS,CAPS,WALL_SECONDS)
    lease=NativeLease(ROOT/'local/global-native',ID,workers=4).acquire()
    try:
        plan=read(PUB/(phase+'-plan.json'))
        budget.run(phase,phase,[j['key'] for j in plan],
            [sys.executable,'-B',str(Path(__file__).resolve()),phase,'--child'],ROOT,LOC/(phase+'.stdout'))
    finally:
        state=budget.load()
        if state['active'] or list((LOC/phase/'jobs').glob('*/pending.json')):
            state.update(halted=True,cleanup_unconfirmed=True,global_native_lease_retained=True);atomic(budget.path,state)
        else:lease.release()
    require(not state['halted'],'Failed phase remains terminal')
    ledger=rows(LOC/phase/'dispatch/ledger.jsonl')
    # Second pass after all processes are gone: original immutable raw evidence,
    # not a check of only the exported success flags.
    f=verify();configs=read(LOC/'configs.json')
    indexed={r['job_id']:r for r in ledger}
    for job in read(PUB/(phase+'-plan.json')):
        d=LOC/phase/'jobs'/job['key'];row=indexed[job['key']]
        require(digest(d/'native.jsonl')==row['raw_log_sha256'],'Raw evidence hash mismatch')
        if job['kind']=='negative':audit_malformed(rows(d/'native.jsonl'),row['returncode']);continue
        label=f"{job['scenario']}-{job['side']}";binary=LOC/'inputs'/f"{label}-{job['arm']}.bin"
        job['setup_sha256']=f['setups'][label][job['arm']]
        require(digest(d/'input.json')==row['input_dump_sha256'],'Input evidence hash mismatch')
        rechecked=audit(rows(d/'native.jsonl'),read(d/'input.json'),job,binary.read_bytes(),configs[label][job['arm']],f)
        require(all(row[k]==v for k,v in rechecked.items()),'Second raw pass differs')
    with (PUB/(phase+'.jsonl')).open('x',encoding='utf8') as stream:
        for row in ledger:stream.write(json.dumps(row,allow_nan=False)+'\n')
    summary=read(LOC/(phase+'-summary.json'))
    summary.update(publication_commit=commit,ci_run=ci,charged_seconds=state['charged_seconds'],
                   budget_passed=True,all_cleanup_confirmed=True,ledger_sha256=digest(PUB/(phase+'.jsonl')))
    write(PUB/(phase+'-summary.json'),summary)
    if phase=='technical':write(PUB/'technical-release.json',dict(passed=True,summary_sha256=observer.source_hash(PUB/'technical-summary.json'),
        method='Full native readback and exactly two declared positional actors per call;8 exact A/A pairs and malformed exit108; independently re-audited from raw files before main.'))
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=('prepare','technical','main'))
    parser.add_argument('--child',action='store_true');parser.add_argument('--publication');parser.add_argument('--ci',type=int)
    args=parser.parse_args()
    if args.phase=='prepare':prepare()
    elif args.child:execute(args.phase)
    else:supervise(args.phase,args.publication,args.ci)

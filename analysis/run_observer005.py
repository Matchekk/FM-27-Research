"""Central, admitted, one-worker technical validation of the passive observer.

No old runner/host is patched in place. Preparation is static. Only the single
technical phase may execute the twenty preregistered native CLI probes.
"""
from argparse import ArgumentParser
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from itertools import product
import importlib.util
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.budget import supervisor_alive
from research.coordination import NativeLease
from research.core import allocate, config_hash, historical_seeds
from research.native import read, write, rows, require, digest, event
from research.night_control import assert_night_admission
from research.passive_observer import audit_trace, equivalence, match_result
from research.study_budget import DeadlineBudget

EXPERIMENT='VALID-005-OBSERVER-V1'
LOCAL=ROOT/'local/valid005-observer-v1'
PUBLIC=ROOT/'data/valid-005-observer-v1'
REGISTRY=ROOT/'local/registry'
RUNTIME=ROOT/'local/runtime-v1114.6'
GAME=Path('D:/steam/steamapps/common/Football Manager 27')
MODES=('reference','observer_off','observer_on','observer_on_repeat')
CONTEXTS=('high_press','deep_block')
DOCUMENT='experiments/VALID-005-passive-observer.md'
REVIEW_DOCUMENT='docs/night-001/OBSERVER-RUNNER-REVIEW.md'
CODE=('analysis/run_observer005.py','analysis/night_supervise.py','research/passive_observer.py',
      'research/night_control.py','research/budget.py','research/study_budget.py','research/core.py',
      'research/native.py','research/coordination.py','adapters/passive_observer_v1.h',
      'adapters/passive-observer-v1.patch',DOCUMENT,REVIEW_DOCUMENT)


def source_hash(path):
    return sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def resource_paths():
    plugins=GAME/'fm_Data/Plugins/x86_64'
    result={'game_plugin.dll':plugins/'game_plugin.dll','icudt65l.dat':GAME/'icudt65l.dat',
            'shared/data/simatch.fmf':GAME/'shared/data/simatch.fmf',
            'shared/data/simatchshared.fmf':GAME/'shared/data/simatchshared.fmf'}
    for name in ('icuuc65.dll','icuin65.dll','icudt65.dll','EOSSDK-Win64-Shipping.dll',
                 'PartyWin.dll','PlayFabMultiplayerWin.dll','steam_api64.dll'):
        result['libs/'+name]=plugins/name
    return result


def fingerprint():
    return config_hash([dict(path=name,sha256=digest(path)) for name,path in sorted(resource_paths().items())])


def jobs(seeds):
    require(type(seeds) is list and len(seeds)==len(set(seeds))==4,'Exactly four technical seeds')
    plan=[dict(key='image-'+mode,kind='image',mode=mode,seed=None) for mode in ('reference','observer_off')]
    for i,(context,side) in enumerate(product(CONTEXTS,(0,1))):
        for mode in MODES:
            plan.append(dict(key=f'{context}-{side}-{mode}',kind='full',context=context,
                             side=side,mode=mode,seed=seeds[i]))
    plan.extend((dict(key='negative-opt-in',kind='negative',mode='invalid_opt_in',seed=seeds[0]),
                 dict(key='negative-binary',kind='negative',mode='invalid_binary',seed=None)))
    return plan


def all_previous_seeds():
    used={0}
    for path in (ROOT/'data').iterdir():
        if path.is_dir() and path!=PUBLIC:
            used.update(historical_seeds(path))
    for path in REGISTRY.glob('*.json'):
        if not path.name.startswith(EXPERIMENT):
            used.update(historical_seeds(path));used.update(read(path).get('seeds',[]))
    for path in (ROOT/'local').iterdir():
        if path.is_dir() and path!=LOCAL and path.name.startswith(('valid','tact-','attr-','mech-','platform-smoke')):
            used.update(historical_seeds(path))
    return used


def prepare(host,manifest):
    require(not (LOCAL/'seed-plan.json').exists(),'Prepared study retained; no reseeding')
    code_hashes={name:source_hash(ROOT/name) for name in CODE}
    validation=read(ROOT/'data/valid-002/validation-summary.json')
    identity=validation['identity'];require(validation['passed'],'VALID-002 not released')
    original=RUNTIME/'engine/fm27_native/FM27Simulator.exe'
    build=read(manifest);published=read(ROOT/'data/night-001-observer/build-report.json')
    require(build['build_status']=='compiled_not_executed' and
            digest(host)==build['observer_host_sha256']==published['observer_host_sha256'],
            'Private observer build identity differs')
    require(digest(original)==identity['adapter_host_sha256'] and
            digest(resource_paths()['game_plugin.dll'])==identity['engine_sha256'] and
            fingerprint()==identity['resource_fingerprint'],'Original host/engine/resources changed')
    fixture=RUNTIME/'engine/fm27_native/fixtures/match.pkm'
    require(digest(fixture)==identity['fixture_sha256'],'Fixture drift')
    require(source_hash(host.parent/'passive_observer_v1.h')==source_hash(ROOT/'adapters/passive_observer_v1.h') and
            digest(host.parent/'passive_observer_v1.h')==build['observer_header_sha256'],
            'Compiled observer header differs from reviewed source')
    require(digest(host.parent/'desktop_host.cpp')==build['modified_host_source_sha256'],
            'Private modified source differs from compile receipt')
    inputs=read(ROOT/'data/tact-001-p1b/inputs.json')
    require(inputs['identity']==identity and digest(RUNTIME/'source/tactics_ui/catalog.json')==inputs['catalog_sha256'],
            'D00 identity/catalog drift')
    require(all(source_hash(RUNTIME/'source'/n)==h for n,h in inputs['runtime_source_sha256'].items()),
            'Frozen runtime source drift')
    old=read(ROOT/'local/tact-001-p1b/configs.json');configs={};setups={}
    for context,side in product(CONTEXTS,(0,1)):
        label=f'{context}-{side}';config=old[f'{label}-D00']
        require(config['rules']=='game' and config['fixture']=='bundled_match_pkm' and
                'experimental_execution' not in config and 'away_tactic_pool' not in config,'Forbidden D00 normalization')
        before=ROOT/'local/tact-002-r0/inputs'/f'{label}-R00.bin'
        require(digest(before)==inputs['setups'][context][str(side)]['D00'],'D00 bytes changed')
        target=LOCAL/'inputs'/(label+'.bin');target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream:stream.write(before.read_bytes())
        configs[label]=config;setups[label]=digest(target)
    write(LOCAL/'configs.json',configs)
    snapshot=read(RUNTIME/'engine/fm27_native/editor_manual_default.json')
    maps=[]
    for team in snapshot['teams']:
        raw=bytes.fromhex(team['manager_tactical_hex']);start=0x1fb4-0x2e0
        mapping=[i if v==255 else v for i,v in enumerate(raw[start:start+11])]
        require(sorted(mapping)==list(range(11)),'OOP permutation invalid');maps.append(mapping)
    lock=REGISTRY/'.allocation.lock';lock.touch(exist_ok=False)
    try:
        excluded=all_previous_seeds();seeds=allocate(EXPERIMENT+'/technical-v1',4,excluded)
        plan=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+'/technical-v1',seeds=seeds,
                  excluded_seed_count=len(excluded),excluded_seed_set_sha256=config_hash(sorted(excluded)))
        with (REGISTRY/(EXPERIMENT+'.reserved.json')).open('x',encoding='utf8') as stream:
            json.dump(plan,stream,indent=2);stream.flush();os.fsync(stream.fileno())
    finally:lock.unlink()
    write(LOCAL/'seed-plan.json',plan);write(PUBLIC/'seed-plan.json',plan)
    write(PUBLIC/'excluded-seeds.json',sorted(excluded));write(PUBLIC/'job-plan.json',jobs(seeds))
    write(LOCAL/'technical-keys.json',[j['key'] for j in jobs(seeds)])
    write(LOCAL/'private-host.json',dict(observer_host=str(host.resolve()),build_manifest=str(manifest.resolve())))
    write(PUBLIC/'inputs.json',dict(schema='valid005.inputs.v1',experiment_id=EXPERIMENT,
        identity=identity,observer_host_sha256=digest(host),build_manifest_sha256=digest(manifest),
        setups=setups,configs_sha256=config_hash(configs),oop_map=maps,catalog_sha256=inputs['catalog_sha256'],
        runtime_source_sha256=inputs['runtime_source_sha256'],code_sha256=code_hashes,
        lease_module_sha256=source_hash(RUNTIME/'source/desktop_engine.py'),
        document=DOCUMENT,document_sha256=source_hash(ROOT/DOCUMENT),
        technical_attempts=20,full_matches=16,loader_checks=2,negative_probes=2,
        seed_plan_sha256=source_hash(PUBLIC/'seed-plan.json'),job_plan_sha256=source_hash(PUBLIC/'job-plan.json'),
        max_workers=1,progress_timeout_seconds=90,child_seconds=180,study_window_seconds=900))
    print('Prepared four unchanged D00 cells/four fresh seeds; zero native invocations.',flush=True)


def verify_frozen():
    value=read(PUBLIC/'inputs.json')
    require(all(source_hash(ROOT/n)==h for n,h in value['code_sha256'].items()),'Frozen observer code changed')
    require(source_hash(PUBLIC/'seed-plan.json')==value['seed_plan_sha256'] and
            source_hash(PUBLIC/'job-plan.json')==value['job_plan_sha256'],'Frozen plan changed')
    require(config_hash(read(LOCAL/'configs.json'))==value['configs_sha256'],'Private configurations changed')
    require(all(digest(LOCAL/'inputs'/(label+'.bin'))==h for label,h in value['setups'].items()),'Binary input drift')
    return value


def successful_ci(commit,run):
    value=json.loads(subprocess.check_output(['gh','run','view',str(run),'--json','status,conclusion,headSha'],cwd=ROOT,text=True))
    require(value['status']=='completed' and value['conclusion']=='success' and value['headSha']==commit,
            'Successful CI for the exact published observer commit required')


def register(commit,ci_run):
    import re
    require(type(commit) is str and re.fullmatch('[0-9a-f]{40}',commit),'Full published commit required')
    frozen=verify_frozen()
    require(type(ci_run) is int and ci_run>0,'Exact successful CI identifier required')
    successful_ci(commit,ci_run)
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]
    for target in ('HEAD',remote):
        subprocess.run(['git','merge-base','--is-ancestor',commit,target],cwd=ROOT,check=True,capture_output=True)
    for name in (*CODE,'data/valid-005-observer-v1/inputs.json','data/valid-005-observer-v1/seed-plan.json',
                 'data/valid-005-observer-v1/job-plan.json'):
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(blob==(ROOT/name).read_bytes().replace(b'\r\n',b'\n'),'Published observer artifact differs: '+name)
    plan=read(LOCAL/'seed-plan.json');require(not set(plan['seeds'])&all_previous_seeds(),'Seed collision after reservation')
    receipt=dict(experiment_id=EXPERIMENT,preregistration_commit=commit,ci_run=ci_run,
                 independent_review_document=REVIEW_DOCUMENT,independent_review_sha256=source_hash(ROOT/REVIEW_DOCUMENT),
                 inputs_sha256=source_hash(PUBLIC/'inputs.json'),
                 code_sha256=frozen['code_sha256'],seeds=plan['seeds'])
    with (LOCAL/'registration.json').open('x',encoding='utf8') as stream:json.dump(receipt,stream,indent=2)
    write(PUBLIC/'registration.json',receipt)


def clean_environment(mode):
    env={k:v for k,v in os.environ.items() if not k.startswith('FM27_')}
    env.update(FM27_ENGINE_ROOT=str(RUNTIME/'engine'),FM27_GAME_ROOT=str(GAME),
               FM27_EXPECTED_DLL_SHA256=read(PUBLIC/'inputs.json')['identity']['engine_sha256'])
    if mode in ('observer_on','observer_on_repeat'):env['FM27_PASSIVE_OBSERVER_V1']='1'
    if mode=='invalid_opt_in':env['FM27_PASSIVE_OBSERVER_V1']='2'
    return env


def native_call(command,env,log,output,timeout=90,on_start=None):
    began=time.monotonic();progress=began;signature=None
    with output.open('xb') as stream:
        process=subprocess.Popen(command,cwd=RUNTIME/'engine',env=env,stdout=stream,stderr=subprocess.STDOUT,
                                 creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if on_start:on_start()
        write(output.with_suffix('.process.json'),dict(pid=process.pid,started_utc=datetime.now(timezone.utc).isoformat()))
        while process.poll() is None:
            current=(log.stat().st_size,log.stat().st_mtime_ns) if log.exists() else None
            if current is not None and current!=signature:signature=current;progress=time.monotonic()
            if time.monotonic()-progress>timeout:
                subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=4)
                process.wait(timeout=4);raise TimeoutError('Native progress timeout; retained original attempt')
            time.sleep(.1)
    return process.returncode,time.monotonic()-began


def audit_input(evidence,dump,config,binary,catalog,oop_map):
    require(event(evidence,'native_scenario_readback_verified')['after_original_preparation'] is True and
            event(evidence,'native_scenario_readback_verified')['records']==5557,'Original preparation readback missing')
    require(event(evidence,'native_profile_bindings_verified')['fields']==1058,'Profile receipt incomplete')
    require(event(evidence,'native_player_tactic_bindings_verified')['players']==22,'Actor binding incomplete')
    require(event(evidence,'native_player_tactic_bindings_verified')['phases']==2,'Both actor phases required')
    roles={r['id']:int(r['flags']) for r in catalog['roles']};positions={p['id']:p['mask'] for p in catalog['positions']}
    pis={g['id']:g for g in catalog['player_instructions']}
    for side,team in enumerate(config['teams']):
        got=dump['teams'][side]
        require(got['side']==side and got['count']==23 and
                [(p['id'],p['attributes']) for p in got['players']]==
                [(p['native_id'],p['attributes']) for p in team['players'][:23]],'Roster/attribute mismatch')
        require(bytes.fromhex(got['creator_hex'])[0x25]==team['mentality'],'Mentality mismatch')
        bits=int.from_bytes(bytes.fromhex(got['creator_hex'])[:16],'little')
        for group in catalog['team_instructions']:
            choice=team['instructions'][str(group['id'])]
            selected=next(o['native_bit'] for o in group['options'] if o['id']==choice)
            active={o['native_bit'] for o in group['options'] if o['native_bit'] and bits>>o['native_bit']&1}
            require(active==({selected} if selected else set()),'Team instruction mismatch')
        for phase,cells in enumerate(team['phases']):
            for i,cell in enumerate(cells):
                slot=oop_map[side][i] if phase else i
                raw=bytes.fromhex(got['tactical_slots'][phase][slot])
                require(struct.unpack_from('<I',raw)[0]==positions[cell['position']] and
                        struct.unpack_from('<Q',raw,64)[0]==roles[cell['role']]|int(cell['duty']),'Phase/role mismatch')
                pi=got['personal_instructions'][phase][slot]
                require(pi['target_player']==cell['target_player'] and pi['target_position']==cell['target_position'],'PI target mismatch')
                for group,definition in pis.items():
                    active={o['id'] for o in definition['options'] if o['id'] and int(pi['flags'])>>o['id']&1}
                    selected=cell['instructions'][str(group)]
                    require(active==({selected} if selected else set()),'PI group mismatch')
    offsets={9:(0xbb8,4),10:(0xbbc,4),19:(0x70,1),20:(0xca8,1),21:(0xca2,1),22:(0xca3,1),1:(0x79,1)}
    offsets.update({f:(a,2) for f,a in enumerate((0xc98,0xc8c,0xc96,0xc78,0xc8a,0xc90,0xc7a,0xc84),11)})
    offsets.update({f:(0x72+f-2,1) for f in range(2,9)})
    profile_count=0
    for kind,side,slot,field,value in struct.iter_unpack('<5I',binary[12:]):
        if kind!=15:continue
        player=dump['teams'][side]['players'][slot]
        if field==0:
            require(bytes.fromhex(player['prefix_hex'])[0x6c:0x70]==struct.pack('<f',value/100),'Height mismatch')
        else:
            offset,length=offsets[field]
            blob=bytes.fromhex(player['prefix_hex'] if offset<0x80 else player['input_tail_hex'])
            start=offset if offset<0x80 else offset-0x4c5
            require(int.from_bytes(blob[start:start+length],'little')==value,'Profile field mismatch')
        profile_count+=1
    require(profile_count==1058,'Full profile coverage missing')
    return dict(attribute_values_verified=3174,profile_fields_verified=profile_count,
                phase_cells_verified=44,pi_groups_verified=748)


def technical():
    frozen=verify_frozen();registration=read(LOCAL/'registration.json')
    require(registration['inputs_sha256']==source_hash(PUBLIC/'inputs.json'),'Registration drift')
    successful_ci(registration['preregistration_commit'],registration['ci_run'])
    require(source_hash(ROOT/REVIEW_DOCUMENT)==registration['independent_review_sha256'],
            'Independent review changed after publication')
    for name in (*CODE,'data/valid-005-observer-v1/inputs.json','data/valid-005-observer-v1/seed-plan.json',
                 'data/valid-005-observer-v1/job-plan.json'):
        require(subprocess.check_output(['git','show',registration['preregistration_commit']+':'+name],cwd=ROOT)==
                (ROOT/name).read_bytes().replace(b'\r\n',b'\n'),'Published observer code/plan changed')
    original=RUNTIME/'engine/fm27_native/FM27Simulator.exe';private=read(LOCAL/'private-host.json')
    observer=Path(private['observer_host'])
    require(digest(original)==frozen['identity']['adapter_host_sha256'] and digest(observer)==frozen['observer_host_sha256'],
            'Host changed')
    require(fingerprint()==frozen['identity']['resource_fingerprint'],'Engine resources changed')
    require(source_hash(RUNTIME/'source/desktop_engine.py')==frozen['lease_module_sha256'] and
            all(source_hash(RUNTIME/'source'/n)==h for n,h in frozen['runtime_source_sha256'].items()),
            'Runtime source changed after preparation')
    # The upstream module only defines file-lease helpers at import. No initialize()
    # or server import is called. Hold resource/host/input handles against writes.
    spec=importlib.util.spec_from_file_location('night_file_leases',RUNTIME/'source/desktop_engine.py')
    leases=importlib.util.module_from_spec(spec);spec.loader.exec_module(leases)
    fixture=RUNTIME/'engine/fm27_native/fixtures/match.pkm'
    for path in [*resource_paths().values(),original,observer,fixture,*((LOCAL/'inputs').glob('*.bin'))]:leases.lease(path)
    try:
        require(fingerprint()==frozen['identity']['resource_fingerprint'],'Resource drift during lock acquisition')
        configs=read(LOCAL/'configs.json');catalog=read(RUNTIME/'source/tactics_ui/catalog.json')
        require(digest(RUNTIME/'source/tactics_ui/catalog.json')==frozen['catalog_sha256'],'Catalog drift')
        planned=read(PUBLIC/'job-plan.json');trace={};results=[]
        for job in planned:
            assert_night_admission(ROOT,EXPERIMENT,'technical',[j['key'] for j in planned])
            require(sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file())<512*1024**2 and
                    shutil.disk_usage(LOCAL).free>20*1024**3,'Private artifact/disk bound')
            key=job['key'];directory=LOCAL/'technical';directory.mkdir(exist_ok=True)
            log=directory/(key+'.jsonl');dump=directory/(key+'.input.json');stdout=directory/(key+'.stdout')
            require(not log.exists() and not dump.exists() and not stdout.exists(),'Retained native attempt: no retry')
            host=original if job['mode']=='reference' else observer
            row=dict(job,status='started',native_invocation_started=False,host_sha256=digest(host),engine_sha256=frozen['identity']['engine_sha256'])
            write(directory/(key+'.started.json'),row)
            try:
                if job['kind']=='image':
                    command=[str(host),'--check-image',str(resource_paths()['game_plugin.dll'])]
                else:
                    label=f"{job.get('context',CONTEXTS[0])}-{job.get('side',0)}"
                    binary=LOCAL/'inputs'/(label+'.bin')
                    if job['mode']=='invalid_binary':
                        binary=LOCAL/'invalid.bin'
                        with binary.open('xb') as stream:stream.write(b'VALID005 INVALID INPUT')
                    command=[str(host),'--fixture',str(fixture),'--scenario-file',str(binary),
                             '--dump-input',str(dump),'--output',str(log),'--tick-step','1']
                    if job['seed'] is not None:command.extend(('--seed',str(job['seed'])))
                mode='observer_on' if job['mode']=='invalid_binary' else job['mode']
                code,elapsed=native_call(command,clean_environment(mode),log,stdout,30 if job['kind']=='image' else 90,
                                         on_start=lambda:row.update(native_invocation_started=True))
                row.update(returncode=code,elapsed_seconds=elapsed)
                if job['kind']=='image':
                    check=event(rows(stdout),'native_engine_compatibility')
                    require(code==0 and check['compatible'] is True,'Image compatibility failed')
                    row.update(status='ok',stdout_sha256=digest(stdout))
                elif job['kind']=='negative':
                    expected=252 if job['mode']=='invalid_opt_in' else 108
                    evidence=rows(log) if log.exists() else []
                    require(code==expected and not any(r.get('event')=='natural_match_finished' for r in evidence),'Negative probe failed')
                    row.update(status='expected_rejection',raw_log_sha256=digest(log) if log.exists() else None,
                               stdout_sha256=digest(stdout))
                else:
                    require(code==0 and log.exists() and dump.exists(),'Native full match failed')
                    evidence=rows(log);native_dump=read(dump)
                    row.update(audit_input(evidence,native_dump,configs[label],binary.read_bytes(),catalog,frozen['oop_map']))
                    row.update(status='ok',result=match_result(evidence,job['seed']),
                               raw_log_sha256=digest(log),input_dump_sha256=digest(dump),setup_sha256=digest(binary))
                    if job['mode'] in ('observer_on','observer_on_repeat'):
                        row['passive_audit']=audit_trace(evidence,native_dump,job['seed'])
                    else:
                        require(not any(r.get('event')=='native_passive_state' for r in evidence),'Observer off emitted snapshots')
                    trace.setdefault((job['context'],job['side']),{})[job['mode']]=evidence
            except Exception as error:
                row.update(status='failed',error_type=type(error).__name__)
                write(directory/(key+'.failure.json'),dict(detail=str(error)))
                raise
            finally:
                with (LOCAL/'ledger.jsonl').open('a',encoding='utf8') as stream:
                    stream.write(json.dumps(row,allow_nan=False)+'\n');stream.flush();os.fsync(stream.fileno())
            results.append(row);print(f"{len(results)}/20 {key}: {row['status']}",flush=True)
        comparisons=[dict(context=h,side=s,**equivalence(trace[h,s],read(LOCAL/'seed-plan.json')['seeds'][i]))
                     for i,(h,s) in enumerate(product(CONTEXTS,(0,1)))]
        write(LOCAL/'technical-summary.json',dict(passed=True,full_matches=16,loader_checks=2,
            negative_rejections=2,equivalence=comparisons,passive_consumer_semantics_validated=False,
            ui_scale_calibrated=False,startpolicy_released=False,career_released=False))
    finally:leases.close_leases()


def export():
    budget=read(LOCAL/'budget.json');require(budget['active'] is None,'Unreconciled native operation retained')
    data=rows(LOCAL/'ledger.jsonl') if (LOCAL/'ledger.jsonl').exists() else []
    actual={r['key']:r for r in data};require(len(actual)==len(data),'Duplicate probe ledger')
    if (PUBLIC/'job-plan.json').exists():plan=read(PUBLIC/'job-plan.json')
    elif (LOCAL/'seed-plan.json').exists():plan=jobs(read(LOCAL/'seed-plan.json')['seeds'])
    else:plan=[dict(j,seed=None) for j in jobs([1,2,3,4])]
    accounting=[]
    for job in plan:
        key=job['key'];row=actual.get(key)
        status=row['status'] if row else 'started_unresolved' if (LOCAL/'technical'/(key+'.started.json')).exists() else 'not_started'
        accounting.append(dict(job,status=status,reserved=key in budget['reserved']))
        if row and row['kind']=='full' and row['status']=='ok':
            require(digest(LOCAL/'technical'/(key+'.jsonl'))==row['raw_log_sha256'] and
                    digest(LOCAL/'technical'/(key+'.input.json'))==row['input_dump_sha256'],'Private evidence changed')
    (PUBLIC/'measurements.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in data),encoding='utf8')
    (PUBLIC/'job-accounting.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in accounting),encoding='utf8')
    summary=read(LOCAL/'technical-summary.json') if (LOCAL/'technical-summary.json').exists() else dict(passed=False)
    write(PUBLIC/'technical-summary.json',summary)
    operations=[{k:o[k] for k in ('name','kind','keys','start_utc','child_deadline_utc','elapsed_seconds','returncode','timed_out')} for o in budget['operations']]
    public={k:budget[k] for k in ('experiment','limits','limit_seconds','charged_seconds','reserved','halted','wall_start_utc','wall_deadline_utc','wall_limit_seconds')}
    public.update(active=None,operations=operations)
    if operations:
        end=max(datetime.fromisoformat(o['start_utc'])+timedelta(seconds=o['elapsed_seconds']) for o in operations)
        public['elapsed_study_window_seconds']=(end-datetime.fromisoformat(budget['wall_start_utc'])).total_seconds()
        public['within_fixed_deadline']=end<=datetime.fromisoformat(budget['wall_deadline_utc'])
    write(PUBLIC/'budget.json',public)
    print(json.dumps(dict(probes=len(data),full_matches=sum(r['kind']=='full' and r['status']=='ok' for r in data),
                          passed=summary['passed'],charged_seconds=budget['charged_seconds'])))


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare','register','technical','export','status'))
    parser.add_argument('--observer-host',type=Path);parser.add_argument('--build-manifest',type=Path)
    parser.add_argument('--commit');parser.add_argument('--ci-run',type=int)
    parser.add_argument('--child',action='store_true');args=parser.parse_args()
    require((ROOT/'.git').is_dir(),'Observer execution only from central checkout')
    if args.phase=='register':register(args.commit,args.ci_run);return
    if args.phase=='export':export();return
    if args.phase=='status':print(json.dumps(read(LOCAL/'budget.json'),indent=2));return
    keys=[] if args.phase=='prepare' else [j['key'] for j in read(PUBLIC/'job-plan.json')]
    assert_night_admission(ROOT,EXPERIMENT,args.phase,keys)
    if args.child:
        active=read(LOCAL/'budget.json')['active']
        require(active and active['name']==args.phase and supervisor_alive(active['supervisor_pid']) and
                active['token_sha256']==sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN','').encode()).hexdigest(),'No live inner supervisor')
        lease=read(ROOT/'local/global-native/native-execution.lease.json')
        require(lease['owner_pid']==active['supervisor_pid'] and lease['experiment']==EXPERIMENT and lease['workers']==1,'Lease identity mismatch')
        if args.phase=='prepare':
            require(args.observer_host and args.build_manifest,'Explicit reviewed private build paths required')
            prepare(args.observer_host,args.build_manifest)
        else:technical()
        return
    budget=DeadlineBudget(LOCAL/'budget.json',experiment=EXPERIMENT,seconds=180,caps={'technical':20,'main':0},wall_seconds=900)
    state=budget.load();proof=LOCAL/(args.phase+'.lease.json')
    require(not state['active'] and not state['halted'] and args.phase not in {o['name'] for o in state['operations']} and
            not proof.exists() and not (LOCAL/(args.phase+'.stdout')).exists(),
            'Attempt retained; no retry or provenance overwrite')
    command=[sys.executable,str(Path(__file__).resolve()),args.phase,'--child']
    if args.observer_host:command.extend(('--observer-host',str(args.observer_host.resolve())))
    if args.build_manifest:command.extend(('--build-manifest',str(args.build_manifest.resolve())))
    with NativeLease(ROOT/'local/global-native',EXPERIMENT,workers=1) as lease:
        owned=lease.assert_owned()
        with proof.open('x',encoding='utf8') as stream:
            json.dump({k:owned[k] for k in ('schema','experiment','workers','owner_pid','acquired_utc')},stream,indent=2)
            stream.flush();os.fsync(stream.fileno())
        budget.run(args.phase,'technical',keys,command,ROOT,LOCAL/(args.phase+'.stdout'))
    print((LOCAL/(args.phase+'.stdout')).read_text(encoding='utf8',errors='replace')[-3000:])


if __name__=='__main__':main()

"""Central-only ATTR-009 supervisor; no retries, no worktree native starts."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json, os, random, shutil, struct, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.attr009 import (EXPERIMENT,ARMS,CONTEXTS,SECONDARY,COEFFICIENTS,matrix,
                             apply_arm,audit_binary,raw_readback,capability_report)
from research.native import NativeLab,digest,event,read,rows,write,require
from research.core import allocate,check_identity,config_hash,historical_seeds,schedule,validate
from research.cli import published_registration
from research.study_budget import DeadlineBudget
from research.budget import supervisor_alive
from research.coordination import NativeLease
from analyse_attr009 import SCHEDULER_SEED,validate_design

LOCAL=ROOT/'local/attr-009-bridge';PUBLIC=ROOT/'data/attr-009-bridge'
SPEC=PUBLIC/'contract.json';REGISTRY=ROOT/'local/registry'
BASE_COMMIT='7767d859e3a66a9aedcf9c1574f3e48dc8dc841f'
CODE=('research/attr009.py','analysis/run_attr009.py','analysis/analyse_attr009.py',
      'analysis/export_attr009.py','analysis/verify_attr009.py','research/native.py','research/stats.py','research/core.py',
      'research/cli.py','research/budget.py','research/study_budget.py','research/coordination.py',
      'research/validation003.py')


def source_hash(path):return sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def historical(exclude_own=False):
    used={0}
    for path in (ROOT/'data').iterdir():
        if path.is_dir() and not(exclude_own and path==PUBLIC):used.update(historical_seeds(path))
    for path in REGISTRY.glob('*.json'):
        if not(exclude_own and path.name.startswith(EXPERIMENT)):
            used.update(historical_seeds(path));used.update(read(path).get('seeds',[]))
    for path in (ROOT/'local').iterdir():
        if path.is_dir() and path!=LOCAL and path.name.startswith(('valid','tact-','mech-','attr-','platform-smoke')):
            used.update(historical_seeds(path))
    return used


def prepare(lab):
    require(not(LOCAL/'seed-plan.json').exists(),'Already prepared: no reseeding')
    check_identity(read(ROOT/'data/valid-002/validation-summary.json')['identity'],lab.identity,read(ROOT/'data/valid-002/validation-summary.json'))
    old_inputs=read(ROOT/'data/tact-001-p1b/inputs.json');require(lab.identity==old_inputs['identity'],'D00 identity drift')
    catalog=lab.runtime/'source/tactics_ui/catalog.json';require(digest(catalog)==old_inputs['catalog_sha256'],'Catalog drift')
    require(all(source_hash(lab.runtime/'source'/n)==v for n,v in old_inputs['runtime_source_sha256'].items()),'Runtime source drift')
    old=read(ROOT/'local/tact-001-p1b/configs.json');configs={};setups={};audits=[];manifest={};negative=[]
    for h,side in product(CONTEXTS,(0,1)):
        base=old[f'{h}-{side}-D00'];blob=lab.server.encode_scenario(base,absolute=True)
        require(sha256(blob).hexdigest()==old_inputs['setups'][h][str(side)]['D00'],'D00 changed')
        for arm in ARMS:
            name=f'{h}-{side}-{arm}';config,bound,changes=apply_arm(base,side,arm,lab.server.OOP_MAP)
            normalized=lab.server.validate_scenario(config);require(normalized==config,'Normalizer changed mask/dose/context')
            binary=LOCAL/'inputs'/(name+'.bin');setup=lab.encode(config,binary)
            audited=audit_binary(blob,binary.read_bytes(),changes)
            configs[name]=config;setups.setdefault(h,{}).setdefault(str(side),{})[arm]=setup
            manifest[name]=dict(bindings=bound,changes=changes)
            audits.append(dict(context=h,side=side,arm=arm,**audited))
        for kind,index,value in [('position_range',2,21),('ability_range',54,101),('bool',49,True)]:
            bad=deepcopy(base);bad['teams'][side]['players'][1]['attributes'][index]=value
            try:lab.server.validate_scenario(bad)
            except ValueError:negative.append(dict(context=h,side=side,kind=kind,rejected=True))
            else:raise ValueError('Invalid attribute accepted')
    write(LOCAL/'configs.json',configs);write(PUBLIC/'mask-manifest.json',manifest)
    write(PUBLIC/'binary-diff-audit.json',dict(passed=True,cells=24,audits=audits))
    write(PUBLIC/'offline-negative-controls.json',dict(passed=True,probes=negative))
    write(PUBLIC/'design-matrix.json',dict(matrix=matrix(),matrix_sha256=config_hash(matrix())))
    write(PUBLIC/'capabilities.json',capability_report())
    REGISTRY.mkdir(exist_ok=True);lock=REGISTRY/'.allocation.lock';lock.touch(exist_ok=False)
    try:
        used=historical();tech=allocate(EXPERIMENT+'/technical-v1',2,used);main=allocate(EXPERIMENT+'/main-v1',32,used|set(tech))
        plan=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+'/main-v1',seeds=tech+main,technical_seeds=tech,main_seeds=main,
                  excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
        with(REGISTRY/(EXPERIMENT+'.reserved.json')).open('x',encoding='utf8')as f:json.dump(plan,f,indent=2);f.flush();os.fsync(f.fileno())
    finally:lock.unlink()
    write(LOCAL/'seed-plan.json',plan);write(PUBLIC/'seed-plan.json',plan);write(PUBLIC/'excluded-seeds.json',sorted(used))
    code={n:source_hash(ROOT/n)for n in CODE}
    write(PUBLIC/'inputs.json',dict(identity=lab.identity,catalog_sha256=digest(catalog),oop_map=lab.server.OOP_MAP,
          source_p1b_inputs_sha256=source_hash(ROOT/'data/tact-001-p1b/inputs.json'),setups=setups,
          fixed_contexts=old_inputs['fixed_contexts'],synthetic_profiles=old_inputs['synthetic_profiles'],
          runtime_source_sha256=old_inputs['runtime_source_sha256'],code_sha256=code,
          passive_effectiveness='unavailable; mechanism unidentified; no kind61',raw_dose='60->80; no FM display claim'))
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE_COMMIT,'--','analysis','data','experiments','research','tests','docs/program-2026-11-14','docs/round2'],cwd=ROOT,text=True).splitlines()
    write(PUBLIC/'historical-archive.json',dict(base_commit=BASE_COMMIT,sha256={n:source_hash(ROOT/n)for n in names}))
    c=deepcopy(read(ROOT/'research/specs/TACT-002-R0.json'))
    c.update(experiment_id=EXPERIMENT,module='ATTR',status='draft',seed_namespace=EXPERIMENT+'/main-v1',identity=lab.identity,
       hypothesis='Unused position specialization modifies relative raw Jumping Reach versus Acceleration/Pace benefit.',
       control='Omni unused ratings20; each attribute arm raw60->80; D00 tactics fixed',
       intervention='Specialized unused field ratings1; active IP/OOP families20; same raw60->80 dose; no baseline arm',
       conditions='D00 IP4231/OOP4411, known discovery opponents, identical nonintervened profiles, benchmark management, no experimental_execution or pool')
    c['metrics']=dict(primary='xgd',secondary=list(SECONDARY),plausibility=[])
    c['design']=dict(unit='seed_block',n_blocks=16,sides=[0,1],control_arm='OJ',matrix=matrix(),matrix_sha256=config_hash(matrix()),setups=setups,
        arms=[dict(id=a,setup_sha256=config_hash({h:{s:v[a]for s,v in by.items()}for h,by in setups.items()}))for a in ARMS],
        scenarios=[dict(id=h,opponent=h,strength='same fixed synthetic roster; only declared mask/dose differs',split='discovery')for h in CONTEXTS])
    c['science']=dict(alpha=.05,power=.9,min_effect=.3,multiple_testing='holm',family_size=5,contrast_coefficients=list(COEFFICIENTS),secondary_endpoints=list(SECONDARY),
        analysis='One primary xGD contrast S[J-(A+P)/2]-O[J-(A+P)/2]; side means per seed; equal contexts; Welch95 and20000stratified block bootstrap; Holm5 secondary only.',
        exclusions='None; incomplete blocks technical status only; no replacement seeds/retries.',
        negative_controls=['24cells once+8frozen A/A repeats=32fullmatches','invalid binary expected108','invalid position/ability/bool offline'],
        readback_fields=['all69 attributes and23profile fields for46players after original preparation','44roles/positions/PI748groups','effective seed/identity/natural finish','raw60/80 comparison among technical siblingarms','OOP player bindings'],
        stopping_rule='384main,32technical+1negative;600child sec/1200immutableUTC;max4workers/90s;first gate error stops.',
        selection_rule='No global attribute ranking or tactic selection; total native raw-dose interaction only; passive mediation unidentified.',
        power_basis='Variance pilot, unknown contrast SD; practical .30xGD,desired full95CIwidth.50; no guaranteed90%power; plan future .20/.30 from observed and upper SD.',
        context_weights=[.5,.5],side_weights=[.5,.5],bootstrap_resamples=20000)
    c['budget']=dict(max_matches=384,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=600,absolute_study_wall_seconds=1200,raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3)
    files=('inputs.json','seed-plan.json','design-matrix.json','mask-manifest.json','offline-negative-controls.json','binary-diff-audit.json','capabilities.json')
    c['execution']=dict(code_sha256=code,artifacts={n:source_hash(PUBLIC/n)for n in files})
    c['preregistration']=dict(commit=None,document='experiments/ATTR-009-preregistration.md',document_sha256=None,analysis='analysis/analyse_attr009.py',analysis_sha256=None)
    validate(c);validate_design(c);write(SPEC,c)
    print('Prepared24cells/34newseeds; no full match.',flush=True)


def verify_code(c):
    require(all(source_hash(ROOT/n)==v for n,v in c['execution']['code_sha256'].items()),'Frozen code drift')
    require(all(source_hash(PUBLIC/n)==v for n,v in c['execution']['artifacts'].items()),'Frozen input drift')
    validate_design(c)


def register(commit):
    c=read(SPEC);c['status']='registered';p=c['preregistration'];p['commit']=commit
    for field in ('document','analysis'):p[field+'_sha256']=sha256(subprocess.check_output(['git','show',commit+':'+p[field]],cwd=ROOT)).hexdigest()
    validate(c,executable=True);published_registration(c,SPEC);verify_code(c)
    plan=read(LOCAL/'seed-plan.json');require(not set(plan['seeds'])&historical(True),'Seed collision')
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=plan['main_seeds']);require(len(schedule(receipt))==384,'Schedule drift')
    for path in (LOCAL/'receipt.json',REGISTRY/(EXPERIMENT+'.json')):
        with path.open('x',encoding='utf8')as f:json.dump(receipt,f,indent=2)
    write(PUBLIC/'manifest.json',receipt)


def ordered_main(r):
    jobs=schedule(r);random.Random(SCHEDULER_SEED).shuffle(jobs);return jobs


def technical_jobs():
    seeds=read(LOCAL/'seed-plan.json')['technical_seeds']
    jobs=[dict(key=f'tech-{h}-{s}-{a}-r0',scenario=h,side=s,arm=a,seed=seeds[CONTEXTS.index(h)])for h,s,a in product(CONTEXTS,(0,1),ARMS)]
    jobs += [dict(key=f'tech-{h}-{s}-{a}-r1',scenario=h,side=s,arm=a,seed=seeds[CONTEXTS.index(h)])for h,s,a in product(CONTEXTS,(0,1),('OJ','SJ'))]
    random.Random(SCHEDULER_SEED+1).shuffle(jobs);return jobs


def collect(kind,r):
    expected={j['key']:j for j in(ordered_main(r)if kind=='main'else technical_jobs())};data=[]
    for p in sorted((LOCAL/kind).glob('part-*/ledger.jsonl')):
        for row in rows(p):
            require(row['key']in expected,'Unexpected key');row.update(scenario=expected[row['key']]['scenario'],config_sha256=r['config_sha256']);data.append(row)
    return data


def audit_contract(lab,row,job,task,log):
    evidence=rows(log);require(event(evidence,'native_profile_bindings_verified')['fields']==1058,'Incomplete profiles')
    binding=event(evidence,'native_player_tactic_bindings_verified')
    require(binding['players']==22 and binding['phases']==2,'Actual-player IP/OOP binding missing')
    require(not any(r.get('event') in('native_execution_probe','experimental_engine_version')for r in evidence),'Experimental execution forbidden')
    dump=read(task['dump']);config=job['config'];role_cells=pi_cells=pi_groups=0
    for side,team in enumerate(config['teams']):
        flags=int.from_bytes(bytes.fromhex(dump['teams'][side]['creator_hex'])[:16],'little')
        for group,choice in team['instructions'].items():
            options=lab.server.GROUPS[int(group)]['options'];bit=next(o['native_bit']for o in options if o['id']==choice)
            active={o['native_bit']for o in options if o['native_bit']and flags>>o['native_bit']&1};require(active==({bit}if bit else set()),'Team instruction drift')
        for phase,cells in enumerate(team['phases']):
            for i,cell in enumerate(cells):
                slot=lab.server.OOP_MAP[side][i]if phase else i;raw=bytes.fromhex(dump['teams'][side]['tactical_slots'][phase][slot])
                require(struct.unpack_from('<I',raw)[0]==lab.server.POSITIONS[cell['position']]['mask'],'Phase position drift')
                require(struct.unpack_from('<Q',raw,64)[0]==int(lab.server.ROLES[cell['role']]['flags'])|int(cell['duty']),'Role/duty drift');role_cells+=1
                pi=dump['teams'][side]['personal_instructions'][phase][slot]
                require(pi['target_player']==cell['target_player']and pi['target_position']==cell['target_position'],'PI target drift')
                require(set(cell['instructions'])=={str(k)for k in lab.server.PIS},'Missing PI groups')
                for group,definition in lab.server.PIS.items():
                    options={o['id']for o in definition['options']if o['id']};active={v for v in options if int(pi['flags'])>>v&1};choice=cell['instructions'][str(group)]
                    require(active==({choice}if choice else set()),'PI drift');pi_groups+=1
                pi_cells+=1
    # All native attributes and IDs were also independently compared by NativeLab.
    require(role_cells==44 and pi_cells==44 and pi_groups==748,'Coverage incomplete')
    manifest=read(PUBLIC/'mask-manifest.json')[f"{job['scenario']}-{job['side']}-{job['arm']}"]
    for change in manifest['changes']:
        require(dump['teams'][change['side']]['players'][change['roster_slot']]['attributes'][change['attribute']]==change['after'],'Raw/mask not native')
    return dict(input_contract_verified=True,profile_fields_verified=1058,native_roles_verified=44,native_pi_cells_verified=44,native_pi_groups_verified=748,
                native_raw_dose_verified=True,design_matrix_sha256=config_hash(matrix()))


def check_technical_publication():
    gate=read(PUBLIC/'technical-gate.json');require(gate.get('passed')is True and type(gate.get('ci_run'))is int,'Technical gate absent')
    ci=json.loads(subprocess.check_output(['gh','run','view',str(gate['ci_run']),'--json','status,conclusion,headSha'],cwd=ROOT,text=True))
    require(ci['status']=='completed'and ci['conclusion']=='success'and ci['headSha']==gate['published_commit'],'Technical CI mismatch')
    subprocess.run(['git','merge-base','--is-ancestor',gate['published_commit'],subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]],cwd=ROOT,check=True)
    require(subprocess.check_output(['git','show',gate['published_commit']+':data/attr-009-bridge/technical-summary.json'],cwd=ROOT)==(PUBLIC/'technical-summary.json').read_bytes().replace(b'\r\n',b'\n'),'Technical report drift')
    return gate


def execute(lab,kind):
    r=read(LOCAL/'receipt.json');published_registration(r['config'],SPEC);verify_code(r['config'])
    check_identity(r['config']['identity'],lab.identity,read(ROOT/'data/valid-002/validation-summary.json'))
    frozen=read(PUBLIC/'inputs.json');require(lab.server.OOP_MAP==frozen['oop_map'],'OOP map drift')
    require(digest(lab.runtime/'source/tactics_ui/catalog.json')==frozen['catalog_sha256'],'Catalog drift')
    require(all(source_hash(lab.runtime/'source'/n)==v for n,v in frozen['runtime_source_sha256'].items()),'Runtime drift')
    if kind=='main':require(read(LOCAL/'technical-summary.json')['passed'],'Private tech gate absent');check_technical_publication()
    jobs=ordered_main(r)if kind=='main'else technical_jobs();configs=read(LOCAL/'configs.json')
    for j in jobs:
        name=f"{j['scenario']}-{j['side']}-{j['arm']}";j.update(config=configs[name],binary=LOCAL/'inputs'/(name+'.bin'))
    for i in range(0,len(jobs),32):
        require(sum(p.stat().st_size for p in LOCAL.rglob('*')if p.is_file())<2*1024**3,'Artifact cap')
        require(shutil.disk_usage(LOCAL).free>20*1024**3,'Disk reserve')
        lab.run(jobs[i:i+32],LOCAL/kind/f'part-{i//32:03d}',workers=4,audit=lambda *a:audit_contract(lab,*a))
    data=collect(kind,r);require(len(data)==len(jobs)and len({x['key']for x in data})==len(jobs),'Incomplete phase')
    if kind=='technical':
        groups={};compared=[];calibration=[]
        for row in data:groups.setdefault((row['scenario'],row['tested_side'],row['arm']),[]).append(row)
        for key,pair in groups.items():
            if len(pair)==2:
                require(all(pair[0][f]==pair[1][f]for f in('score','finish_tick','team_statistics','setup_sha256','seed')),'A/A differs');compared.append(dict(context=key[0],side=key[1],arm=key[2],exact=True))
        require(len(groups)==24 and len(compared)==8,'Technical coverage differs')
        for h,s,a in product(CONTEXTS,(0,1),ARMS):
            # A sibling attribute arm supplies the native60 before-value with
            # identical mask/context/seed/side, without an extra baseline match.
            sibling=a[0]+('A'if a[1]=='J'else'J')
            before=read(LOCAL/'technical/part-000'/f'tech-{h}-{s}-{sibling}-r0.input.json')
            after=read(LOCAL/'technical/part-000'/f'tech-{h}-{s}-{a}-r0.input.json')
            bound=read(PUBLIC/'mask-manifest.json')[f'{h}-{s}-{a}']['bindings']
            calibration.append(dict(context=h,side=s,arm=a,**raw_readback(before,after,configs[f'{h}-{s}-{a}'],s,a,bound)))
        invalid=LOCAL/'invalid.bin';invalid.write_bytes(b'ATTR-009 INVALID');log=LOCAL/'negative.jsonl'
        write(LOCAL/'negative-attempt.json',dict(status='started',expected_returncode=108))
        try:result=subprocess.run([str(lab.server.native_host()),'--scenario-file',str(invalid),'--output',str(log)],cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as error:write(LOCAL/'negative-attempt.json',dict(status='failed',error_type=type(error).__name__));raise
        accepted=any(x.get('event')=='natural_match_finished'for x in rows(log))if log.exists()else False
        negative=dict(status='expected_rejection'if result.returncode==108 and log.exists()and not accepted else'failed',returncode=result.returncode,natural_match_finished=accepted,raw_log_sha256=digest(log)if log.exists()else None)
        write(LOCAL/'negative-attempt.json',negative);require(negative['status']=='expected_rejection','Invalid binary accepted')
        write(LOCAL/'technical-summary.json',dict(passed=True,matches=32,readback_cells=24,repeats=compared,negative=negative,raw_calibration=calibration,
              native_identity=lab.identity,matrix_sha256=config_hash(matrix()),passive_effectiveness='unavailable; mechanism unidentified',fm_in_game_display_calibrated=False))


def run_supervised_phase(budget,phase,keys,command):
    state=budget.load();require(not state['active']and not state['halted'],'Interrupted/failed phase retained')
    require(phase not in{o['name']for o in state['operations']},'Phase attempted: no retry')
    proof_path=LOCAL/(phase+'.lease.json');require(not proof_path.exists(),'Lease proof retained')
    with NativeLease(ROOT/'local/global-native',EXPERIMENT,workers=4)as lease:
        proof=lease.assert_owned()
        with proof_path.open('x',encoding='utf8',newline='\n')as f:json.dump({k:proof[k]for k in('schema','experiment','workers','owner_pid','acquired_utc')},f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        budget.run(phase,'main'if phase=='main'else'technical',keys,command,ROOT,LOCAL/(phase+'.stdout'))


def main():
    p=ArgumentParser(description=__doc__);p.add_argument('phase',choices=('prepare','register','technical','main','status'));p.add_argument('--commit')
    p.add_argument('--runtime',type=Path,default=ROOT/'local/runtime-v1114.6');p.add_argument('--game',type=Path,default=Path('D:/steam/steamapps/common/Football Manager 27'));p.add_argument('--child',action='store_true');a=p.parse_args()
    require((ROOT/'.git').is_dir(),'Central checkout only; worktrees cannot prepare/register/start')
    if a.phase=='register':register(a.commit);return
    if a.phase=='status':print(json.dumps(read(LOCAL/'budget.json'),indent=2));return
    if a.child:
        active=read(LOCAL/'budget.json')['active'];require(active and active['name']==a.phase and supervisor_alive(active['supervisor_pid'])and active['token_sha256']==sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN','').encode()).hexdigest(),'No authenticated supervisor')
        lease=read(ROOT/'local/global-native/native-execution.lease.json');require(lease['owner_pid']==active['supervisor_pid']and lease['experiment']==EXPERIMENT and lease['workers']==4,'Lease mismatch')
        lab=NativeLab(a.runtime,a.game,LOCAL);prepare(lab)if a.phase=='prepare'else execute(lab,a.phase);return
    budget=DeadlineBudget(LOCAL/'budget.json',experiment=EXPERIMENT,seconds=600,caps={'technical':33,'main':384},wall_seconds=1200)
    keys=[]if a.phase=='prepare'else[j['key']for j in technical_jobs()]+['negative-binary']if a.phase=='technical'else[j['key']for j in ordered_main(read(LOCAL/'receipt.json'))]
    if a.phase=='main':require(read(LOCAL/'technical-summary.json')['passed'],'Tech gate absent');check_technical_publication()
    cmd=[sys.executable,str(Path(__file__).resolve()),a.phase,'--child','--runtime',str(a.runtime.resolve()),'--game',str(a.game.resolve())]
    run_supervised_phase(budget,a.phase,keys,cmd)
    print((LOCAL/(a.phase+'.stdout')).read_text(encoding='utf8',errors='replace')[-3000:])
    print('Charged seconds',budget.load()['charged_seconds'],'/600;UTCdeadline',budget.load()['wall_deadline_utc'])


if __name__=='__main__':main()

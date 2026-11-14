"""Central MECH-003 supervisor. Root alone may admit it through NIGHT-001."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json, os, random, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.stamina003 import (EXPERIMENT,ARMS,CONTEXTS,SECONDARY,SECONDARY_PAIRS,COEFFICIENTS,
                                 STAMINA_INDEX,PRESS_GROUP,PRESS_IDS,PRESS_BITS,matrix,treatment,apply_arm,audit_binary,audit_contract)
from research.native import NativeLab,digest,event,read,rows,write,require
from research.core import allocate,check_identity,config_hash,historical_seeds,schedule,validate
from research.cli import published_registration
from research.study_budget import DeadlineBudget
from research.budget import supervisor_alive
from research.coordination import NativeLease
from analyse_mech003 import SCHEDULER_SEED,validate_design
LOCAL=ROOT/'local/mech-003-stamina';PUBLIC=ROOT/'data/mech-003-stamina'
SPEC=PUBLIC/'contract.json';REGISTRY=ROOT/'local/registry'
BASE_COMMIT='adb708e99c6cb284b493fb7cee1c60ae9361546b'
CODE=('research/stamina003.py','analysis/run_mech003.py','analysis/analyse_mech003.py',
      'analysis/export_mech003.py','analysis/verify_mech003.py','research/native.py','research/stats.py',
      'research/core.py','research/cli.py','research/budget.py','research/study_budget.py',
      'research/coordination.py','research/validation003.py','research/night_control.py','analysis/night_supervise.py')


def assert_master(phase,keys):
    # Root supplies this interface before code freeze; importing this module is inert.
    from research.night_control import assert_night_admission
    assert_night_admission(ROOT,EXPERIMENT,phase,keys)


def source_hash(path):
    return sha256(Path(path).read_bytes().replace(b"\r\n",b"\n")).hexdigest()

def historical(exclude_own=False):
    used={0}
    for path in (ROOT/"data").iterdir():
        if path.is_dir() and not (exclude_own and path==PUBLIC):used.update(historical_seeds(path))
    for path in REGISTRY.glob("*.json"):
        if not (exclude_own and path.name.startswith(EXPERIMENT)):
            used.update(historical_seeds(path));used.update(read(path).get("seeds",[]))
    for path in (ROOT/"local").iterdir():
        if path.is_dir() and path!=LOCAL and path.name.startswith(("valid","tact-","mech-","attr-","night-","platform-smoke")):
            used.update(historical_seeds(path))
    return used

def contract_definition(identity=None,setups=None):
    c=deepcopy(read(ROOT/'research/specs/TACT-002-R0.json'))
    c.update(experiment_id=EXPERIMENT,module='MECH',status='draft',seed_namespace=EXPERIMENT+'/main-v1',identity=identity,
        hypothesis='Higher native Stamina improves average xGD over the two frozen pressing levels in the fixed D00 synthetic context.',
        control='R00: ten starting outfield players Stamina52 raw40, Standard pressing; not the original raw60 attribute baseline.',
        intervention='Full2x2 Stamina52 raw40/80 and TriggerPress Standard/MoreOften; only tested-side ten starting outfield ability values and one team instruction differ.',
        conditions='D00 IP4231/OOP4411, same known opponents, phases, roles, PI, positions, profiles, management and all nonintervened abilities; no experimental execution, pool or observer.')
    c['metrics']=dict(primary='xgd',secondary=list(SECONDARY),plausibility=[])
    c['design']=dict(unit='seed_block',n_blocks=32,sides=[0,1],control_arm='R00',matrix=matrix(),matrix_sha256=config_hash(matrix()),setups=setups,
        arms=[dict(id=a,setup_sha256=config_hash({h:{s:v[a] for s,v in by.items()} for h,by in setups.items()}) if setups is not None else None) for a in ARMS],
        scenarios=[dict(id=h,opponent=h,strength='fixed identical synthetic nonintervened profiles; only declared Stamina/pressing treatment differs',split='discovery') for h in CONTEXTS])
    c['science']=dict(alpha=.05,power=.9,min_effect=.3,multiple_testing='holm',family_size=7,primary_contrast='STAMINA',
        contrast_coefficients={k:list(v) for k,v in COEFFICIENTS.items()},secondary_contrasts=[list(x) for x in SECONDARY_PAIRS],
        analysis='Stamina marginal raw80-minus40 on xGD primary. Side means per seed, context weights1/2; Welch95 and20000 full-block stratified bootstrap. Exactly Holm7 secondary.',
        exclusions='None; incomplete blocks technical status only. No replacement seed, retry, winner selection or raw60 baseline inference.',
        negative_controls=['16cells twice=32technical full matches/16exactA/A pairs','invalid binary expected exit108','Stamina0/101/bool and unknown pressing ID rejected offline'],
        readback_fields=['all69attribute values and23profile fields for46active players after original preparation','actual22player IP/OOP bindings;44roles/positions/PI cells;748PIgroups','Stamina ten40/80 and pressing native0/66; every other input unchanged','effective seed and natural score/endtick'],
        stopping_rule='512main,32technical+1negative;600supervised child sec/1200immutableUTC;NightMaster1800sec/23UTC also mandatory;max4workers90s;first gate error stops.',
        selection_rule='No final candidate or attribute ranking; estimate controlled total effects only, no fatigue mediation or career transfer.',
        power_basis='Unknown new Stamina contrast SD; practical .30xGD, desired full95width .50; no90%power guarantee. Future new-seed planning for .20/.30 from observed and simultaneous normal-model SD upper bounds.',
        context_weights=[.5,.5],side_weights=[.5,.5],desired_full_ci_width=.5,bootstrap_resamples=20000)
    c['budget']=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=600,
                     absolute_study_wall_seconds=1200,raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3)
    c['execution']=None
    c['preregistration']=dict(commit=None,document='experiments/MECH-003-stamina-preregistration.md',document_sha256=None,
                              analysis='analysis/analyse_mech003.py',analysis_sha256=None)
    validate(c);validate_design(c)
    return c


def prepare(lab):
    require(not (LOCAL/'seed-plan.json').exists(), 'Already prepared; no reseeding')
    require(read(PUBLIC/'contract-draft.json')==contract_definition(),'Published draft/scientific design drift')
    validation=read(ROOT/'data/valid-002/validation-summary.json')
    check_identity(validation['identity'],lab.identity,validation)
    source=read(ROOT/'data/tact-001-p1b/inputs.json')
    require(lab.identity==source['identity'],'D00 engine/host/fixture identity drift')
    catalog_path=lab.runtime/'source/tactics_ui/catalog.json';catalog=read(catalog_path)
    require(digest(catalog_path)==source['catalog_sha256'],'Catalog drift')
    require(catalog['attributes'][STAMINA_INDEX]['id']==STAMINA_INDEX and catalog['attributes'][STAMINA_INDEX]['name']=='Stamina', 'Stamina semantic catalog drift')
    group=lab.server.GROUPS[PRESS_GROUP]
    require(group['name']=='TriggerPress' and all(any(o['id']==identifier and o['native_bit']==bit for o in group['options'])
            for identifier,bit in zip(PRESS_IDS,PRESS_BITS,strict=True)), 'Pressing native catalog drift')
    require(all(source_hash(lab.runtime/'source'/n)==v for n,v in source['runtime_source_sha256'].items()),'Runtime source drift')
    old=read(ROOT/'local/tact-001-p1b/configs.json')
    configs={};setups={};manifest={};audits=[];negative=[]
    for h,side in product(CONTEXTS,(0,1)):
        base=old[f'{h}-{side}-D00'];blob=lab.server.encode_scenario(base,absolute=True)
        require(sha256(blob).hexdigest()==source['setups'][h][str(side)]['D00'],'Original D00 changed')
        for arm in ARMS:
            name=f'{h}-{side}-{arm}';config,changes=apply_arm(base,side,arm)
            normalized=lab.server.validate_scenario(config)
            require(normalized==config,'Normalizer changed a nondeclared input')
            reset=deepcopy(config)
            for change in changes:reset['teams'][side]['players'][change['roster_slot']]['attributes'][STAMINA_INDEX]=60
            reset['teams'][side]['instructions'][str(PRESS_GROUP)]=PRESS_IDS[0]
            require(reset==base,'Non-Stamina/non-pressing input changed')
            binary=LOCAL/'inputs'/(name+'.bin');setup=lab.encode(config,binary)
            audited=audit_binary(blob,binary.read_bytes(),side,arm,changes)
            configs[name]=config;setups.setdefault(h,{}).setdefault(str(side),{})[arm]=setup
            manifest[name]=dict(treatment=treatment(arm),starting_outfield_roster_slots=base['teams'][side]['lineup'][1:],
                                changes=changes,setup_sha256=setup)
            audits.append(dict(context=h,side=side,arm=arm,**audited))
        for kind,value in (('below_range',0),('above_range',101),('bool',True)):
            bad=deepcopy(base);bad['teams'][side]['players'][base['teams'][side]['lineup'][1]]['attributes'][STAMINA_INDEX]=value
            try:lab.server.validate_scenario(bad)
            except ValueError:negative.append(dict(context=h,side=side,kind=kind,rejected=True))
            else:raise ValueError('Invalid Stamina input accepted')
        bad=deepcopy(base);bad['teams'][side]['instructions'][str(PRESS_GROUP)]=0
        try:lab.server.validate_scenario(bad)
        except ValueError:negative.append(dict(context=h,side=side,kind='unknown_pressing_id',rejected=True))
        else:raise ValueError('Invalid pressing ID accepted')
    write(LOCAL/'configs.json',configs)
    write(PUBLIC/'intervention-manifest.json',manifest)
    write(PUBLIC/'binary-diff-audit.json',dict(passed=True,cells=16,audits=audits))
    write(PUBLIC/'offline-negative-controls.json',dict(passed=True,probes=negative))
    write(PUBLIC/'design-matrix.json',dict(matrix=matrix(),matrix_sha256=config_hash(matrix())))
    REGISTRY.mkdir(exist_ok=True);lock=REGISTRY/'.allocation.lock';lock.touch(exist_ok=False)
    try:
        used=historical();tech=allocate(EXPERIMENT+'/technical-v1',2,used);main=allocate(EXPERIMENT+'/main-v1',64,used|set(tech))
        plan=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+'/main-v1',seeds=tech+main,technical_seeds=tech,main_seeds=main,
                  excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
        with (REGISTRY/(EXPERIMENT+'.reserved.json')).open('x',encoding='utf8') as stream:
            json.dump(plan,stream,indent=2);stream.flush();os.fsync(stream.fileno())
    finally:lock.unlink()
    write(LOCAL/'seed-plan.json',plan);write(PUBLIC/'seed-plan.json',plan);write(PUBLIC/'excluded-seeds.json',sorted(used))
    code={n:source_hash(ROOT/n) for n in CODE}
    write(PUBLIC/'inputs.json',dict(identity=lab.identity,catalog_sha256=digest(catalog_path),oop_map=lab.server.OOP_MAP,
          source_p1b_inputs_sha256=source_hash(ROOT/'data/tact-001-p1b/inputs.json'),setups=setups,
          fixed_contexts=source['fixed_contexts'],synthetic_profiles=source['synthetic_profiles'],
          runtime_source_sha256=source['runtime_source_sha256'],code_sha256=code,
          observer_used=False,mechanism_decomposition_identified=False,fm_ui_scale_calibrated=False,
          intervention='Stamina52 raw40/80 at ten starting outfield players; TriggerPress Standard/MoreOften only'))
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE_COMMIT,'--','analysis','data','experiments','research','tests','docs/program-2026-11-14','docs/round2','docs/round3','docs/night-001'],cwd=ROOT,text=True).splitlines()
    write(PUBLIC/'historical-archive.json',dict(base_commit=BASE_COMMIT,sha256={n:source_hash(ROOT/n) for n in paths}))
    c=contract_definition(lab.identity,setups)
    artifacts=('contract-draft.json','inputs.json','seed-plan.json','design-matrix.json','intervention-manifest.json','offline-negative-controls.json','binary-diff-audit.json')
    c['execution']=dict(code_sha256=code,artifacts={n:source_hash(PUBLIC/n) for n in artifacts})
    c['preregistration']=dict(commit=None,document='experiments/MECH-003-stamina-preregistration.md',document_sha256=None,
                              analysis='analysis/analyse_mech003.py',analysis_sha256=None)
    validate(c);validate_design(c);write(SPEC,c)
    print('Prepared16cells/66newseeds; zero full matches.',flush=True)


def verify_code(c):
    require(all(source_hash(ROOT/n)==v for n,v in c['execution']['code_sha256'].items()),'Frozen MECH003 code drift')
    require(all(source_hash(PUBLIC/n)==v for n,v in c['execution']['artifacts'].items()),'Frozen MECH003 artifact drift')
    validate_design(c)


def register(commit):
    c=read(SPEC);c['status']='registered';p=c['preregistration'];p['commit']=commit
    for field in ('document','analysis'):p[field+'_sha256']=sha256(subprocess.check_output(['git','show',commit+':'+p[field]],cwd=ROOT)).hexdigest()
    validate(c,executable=True);published_registration(c,SPEC);verify_code(c)
    plan=read(LOCAL/'seed-plan.json');require(not set(plan['seeds'])&historical(True),'Seed collision')
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=plan['main_seeds']);require(len(schedule(receipt))==512,'Schedule drift')
    for path in (LOCAL/'receipt.json',REGISTRY/(EXPERIMENT+'.json')):
        with path.open('x',encoding='utf8') as stream:json.dump(receipt,stream,indent=2)
    write(PUBLIC/'manifest.json',receipt)


def ordered_main(receipt):
    jobs=schedule(receipt);random.Random(SCHEDULER_SEED).shuffle(jobs)
    return jobs

def technical_jobs():
    seeds=read(LOCAL/"seed-plan.json")["technical_seeds"]
    jobs=[dict(key=f"tech-{h}-{side}-{arm}-r0",scenario=h,side=side,arm=arm,seed=seeds[CONTEXTS.index(h)]) for h,side,arm in product(CONTEXTS,(0,1),ARMS)]
    jobs.extend(dict(key=f"tech-{h}-{side}-{arm}-r1",scenario=h,side=side,arm=arm,seed=seeds[CONTEXTS.index(h)]) for h,side,arm in product(CONTEXTS,(0,1),ARMS))
    random.Random(SCHEDULER_SEED+1).shuffle(jobs)
    return jobs

def collect(kind,receipt):
    expected={j["key"]:j for j in (ordered_main(receipt) if kind=="main" else technical_jobs())};data=[]
    for path in sorted((LOCAL/kind).glob("part-*/ledger.jsonl")):
        for row in rows(path):
            require(row["key"] in expected,"Unexpected ledger key")
            row.update(experiment_id=EXPERIMENT,scenario=expected[row["key"]]["scenario"],config_sha256=receipt["config_sha256"])
            data.append(row)
    return data

def check_technical_publication():
    gate=read(PUBLIC/'technical-gate.json')
    require(gate.get('passed') is True and type(gate.get('ci_run')) is int,'Missing published MECH003 technical/CI gate')
    ci=json.loads(subprocess.check_output(['gh','run','view',str(gate['ci_run']),'--json','status,conclusion,headSha'],cwd=ROOT,text=True))
    require(ci['status']=='completed' and ci['conclusion']=='success' and ci['headSha']==gate['published_commit'],'Technical publication CI not successful for exact gate commit')
    subprocess.run(['git','merge-base','--is-ancestor',gate['published_commit'],subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]],cwd=ROOT,check=True)
    require(subprocess.check_output(['git','show',gate['published_commit']+':data/mech-003-stamina/technical-summary.json'],cwd=ROOT)==(PUBLIC/'technical-summary.json').read_bytes().replace(b'\r\n',b'\n'),'Published technical summary drift')
    review=gate.get('independent_review_document');review_path=(ROOT/review).resolve() if isinstance(review,str) else None
    require(review_path is not None and ROOT.resolve() in review_path.parents and source_hash(review_path)==gate.get('independent_review_sha256'),
            'Independent technical review document/hash missing')
    require(subprocess.check_output(['git','show',gate['published_commit']+':'+review],cwd=ROOT)==review_path.read_bytes().replace(b'\r\n',b'\n'),
            'Independent technical review not in the successful release commit')
    return gate


def execute(lab,kind):
    receipt=read(LOCAL/'receipt.json');published_registration(receipt['config'],SPEC);verify_code(receipt['config'])
    check_identity(receipt['config']['identity'],lab.identity,read(ROOT/'data/valid-002/validation-summary.json'))
    frozen=read(PUBLIC/'inputs.json')
    require(lab.server.OOP_MAP==frozen['oop_map'],'OOP map drift')
    require(digest(lab.runtime/'source/tactics_ui/catalog.json')==frozen['catalog_sha256'],'Catalog drift')
    require(all(source_hash(lab.runtime/'source'/n)==v for n,v in frozen['runtime_source_sha256'].items()),'Runtime source drift')
    if kind=='main':
        require(read(LOCAL/'technical-summary.json')['passed'],'Private technical gate absent')
        check_technical_publication()
    jobs=ordered_main(receipt) if kind=='main' else technical_jobs();configs=read(LOCAL/'configs.json')
    for job in jobs:
        name=f"{job['scenario']}-{job['side']}-{job['arm']}"
        job.update(config=configs[name],binary=LOCAL/'inputs'/(name+'.bin'))
    for offset in range(0,len(jobs),32):
        require(sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file())<2*1024**3,'Private artifact cap')
        require(shutil.disk_usage(LOCAL).free>20*1024**3,'Disk reserve exhausted')
        lab.run(jobs[offset:offset+32],LOCAL/kind/f'part-{offset//32:03d}',workers=4,
                audit=lambda *args:audit_contract(lab,*args))
    data=collect(kind,receipt)
    require(len(data)==len(jobs) and len({r['key'] for r in data})==len(jobs),'Incomplete native phase')
    if kind=='technical':
        groups={};repeats=[];dose=[]
        for row in data:groups.setdefault((row['scenario'],row['tested_side'],row['arm']),[]).append(row)
        require(len(groups)==16,'Wrong technical cell coverage')
        for key,pair in groups.items():
            require(len(pair)==2 and all(pair[0][field]==pair[1][field] for field in
                    ('score','finish_tick','team_statistics','setup_sha256','seed','native_stamina_values','native_pressing_bit')),
                    'A/A repeat differs')
            repeats.append(dict(context=key[0],side=key[1],arm=key[2],exact=True))
        for h,side,(low_arm,high_arm) in product(CONTEXTS,(0,1),(('R00','R10'),('R01','R11'))):
            low=read(LOCAL/'technical/part-000'/f'tech-{h}-{side}-{low_arm}-r0.input.json')
            high=read(LOCAL/'technical/part-000'/f'tech-{h}-{side}-{high_arm}-r0.input.json')
            lineup=configs[f'{h}-{side}-{low_arm}']['teams'][side]['lineup'][1:]
            for index in lineup:
                a,b=low['teams'][side]['players'][index],high['teams'][side]['players'][index]
                require(a['id']==b['id'] and a['attributes'][STAMINA_INDEX]==40 and b['attributes'][STAMINA_INDEX]==80,
                        'Native raw40/80 dose contrast differs')
            dose.append(dict(context=h,side=side,pressing_bit=treatment(low_arm)['pressing_bit'],
                             ten_native_raw_pairs_verified=True,low=40,high=80,fm_ui_scale_calibrated=False))
        invalid=LOCAL/'invalid.bin';invalid.write_bytes(b'MECH003 INTENTIONALLY INVALID');log=LOCAL/'negative.jsonl'
        write(LOCAL/'negative-attempt.json',dict(status='started',expected_returncode=108))
        try:
            result=subprocess.run([str(lab.server.native_host()),'--scenario-file',str(invalid),'--output',str(log)],
                cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as error:
            write(LOCAL/'negative-attempt.json',dict(status='failed',error_type=type(error).__name__));raise
        accepted=any(r.get('event')=='natural_match_finished' for r in rows(log)) if log.exists() else False
        negative=dict(status='expected_rejection' if result.returncode==108 and log.exists() and not accepted else 'failed',
                      returncode=result.returncode,natural_match_finished=accepted,raw_log_sha256=digest(log) if log.exists() else None)
        write(LOCAL/'negative-attempt.json',negative)
        require(negative['status']=='expected_rejection','Negative input did not reject correctly')
        write(LOCAL/'technical-summary.json',dict(passed=True,matches=32,readback_cells=16,repeats=repeats,
              native_identity=lab.identity,matrix_sha256=config_hash(matrix()),raw_dose_comparisons=dose,
              negative=negative,observer_used=False,mechanism_decomposition_identified=False,fm_ui_scale_calibrated=False))


def run_supervised_phase(budget,phase,keys,command):
    """Never replace the provenance of a completed, retained or crashed phase."""
    state=budget.load()
    require(not state['active'] and not state['halted'],'Interrupted/failed operation: retain original provenance')
    require(phase not in {o['name'] for o in state['operations']},'Phase already attempted: retain original provenance')
    proof_path=LOCAL/(phase+'.lease.json')
    require(not proof_path.exists(),'Retained phase lease proof exists: no retry or overwrite')
    assert_master(phase,keys)
    with NativeLease(ROOT/'local/global-native',EXPERIMENT,workers=4) as lease:
        proof=lease.assert_owned()
        # Exclusive creation also closes the precheck/open race. A failed or partial
        # write remains blocking; no retry can silently repair or replace it.
        with proof_path.open('x',encoding='utf8',newline='\n') as stream:
            json.dump({k:proof[k] for k in ('schema','experiment','workers','owner_pid','acquired_utc')},stream,indent=2)
            stream.write('\n');stream.flush();os.fsync(stream.fileno())
        budget.run(phase,'main' if phase=='main' else 'technical',keys,command,ROOT,LOCAL/(phase+'.stdout'))


def phase_keys(phase):
    if phase=='prepare':return []
    if phase=='technical':return [j['key'] for j in technical_jobs()]+['negative-binary']
    require(phase=='main','Unknown native phase')
    return [j['key'] for j in ordered_main(read(LOCAL/'receipt.json'))]


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare','register','technical','main','status'));parser.add_argument('--commit')
    parser.add_argument('--runtime',type=Path,default=ROOT/'local/runtime-v1114.6')
    parser.add_argument('--game',type=Path,default=Path('D:/steam/steamapps/common/Football Manager 27'))
    parser.add_argument('--child',action='store_true');args=parser.parse_args()
    require((ROOT/'.git').is_dir(),'Central checkout only; no worktree prepare/register/native start')
    if args.phase=='register':register(args.commit);return
    if args.phase=='status':print(json.dumps(read(LOCAL/'budget.json'),indent=2));return
    keys=phase_keys(args.phase)
    assert_master(args.phase,keys)  # Before budget creation or NativeLab/check-image.
    if args.child:
        active=read(LOCAL/'budget.json')['active']
        require(active and active['name']==args.phase and supervisor_alive(active['supervisor_pid']) and
                active['token_sha256']==sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN','').encode()).hexdigest(),
                'No authenticated live inner supervisor')
        lease=read(ROOT/'local/global-native/native-execution.lease.json')
        require(lease['owner_pid']==active['supervisor_pid'] and lease['experiment']==EXPERIMENT and lease['workers']==4,'Central lease mismatch')
        lab=NativeLab(args.runtime,args.game,LOCAL)
        prepare(lab) if args.phase=='prepare' else execute(lab,args.phase)
        return
    if args.phase=='main':
        require(read(LOCAL/'technical-summary.json')['passed'],'Technical gate missing')
        check_technical_publication()
    budget=DeadlineBudget(LOCAL/'budget.json',experiment=EXPERIMENT,seconds=600,
                          caps={'technical':33,'main':512},wall_seconds=1200)
    command=[sys.executable,str(Path(__file__).resolve()),args.phase,'--child','--runtime',str(args.runtime.resolve()),'--game',str(args.game.resolve())]
    run_supervised_phase(budget,args.phase,keys,command)
    print((LOCAL/(args.phase+'.stdout')).read_text(encoding='utf8',errors='replace')[-3000:])
    print('Charged seconds',budget.load()['charged_seconds'],'/600; UTCdeadline',budget.load()['wall_deadline_utc'])


if __name__=='__main__':main()

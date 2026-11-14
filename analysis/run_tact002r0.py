"""One preregistered R0 study, two native phases, one persistent study deadline."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import random
import shutil
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.budget import supervisor_alive
from research.study_budget import DeadlineBudget
from research.coordination import NativeLease
from research.cli import published_registration
from research.core import allocate, check_identity, config_hash, historical_seeds, schedule, validate
from research.discovery import validate_4231
from research.native import NativeLab, digest, event, read, require, rows, write
from analyse_tact002r0 import (ARMS,CONTEXTS,FACTORS,METRICS,SECONDARY,PLAUSIBILITY,
                              SCHEDULER_SEED,matrix,validate_design,wanted_flags,SECONDARY_PAIRS)

EXPERIMENT="TACT-002-R0"
LOCAL=ROOT/"local/tact-002-r0"
PUBLIC=ROOT/"data/tact-002-r0"
SPEC=ROOT/"research/specs/TACT-002-R0.json"
REGISTRY=ROOT/"local/registry"
BASE_COMMIT="790727f3ef830209baf55f2dde36b6dca1299685"
CODE=("analysis/verify_tact002r0.py","analysis/run_tact002r0.py","analysis/analyse_tact002r0.py","analysis/export_tact002r0.py",
      "analysis/run_tact001p1b.py","analysis/analyse_tact001p1b.py","research/discovery.py","research/study_budget.py","research/budget.py","research/core.py",
      "research/native.py","research/stats.py","research/cli.py","research/coordination.py")


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
        if path.is_dir() and path!=LOCAL and path.name.startswith(("valid","tact-","platform-smoke")):
            used.update(historical_seeds(path))
    return used


def binary_audit(before,after,side,levels,slots):
    require(before[:12]==after[:12] and len(before)==len(after),"Binary header/count changed")
    a=list(struct.iter_unpack("<5I",before[12:]));b=list(struct.iter_unpack("<5I",after[12:]))
    changed=[dict(before=list(x),after=list(y)) for x,y in zip(a,b,strict=True) if x!=y]
    expected={((4,side,slots[f["code"]],f["low_flags"]>>32,f["low_flags"]&0xffffffff),
               (4,side,slots[f["code"]],f["high_flags"]>>32,f["high_flags"]&0xffffffff)) for f in FACTORS if levels[f["code"]]==1}
    require({(tuple(x["before"]),tuple(x["after"])) for x in changed}==expected,"Undeclared binary change or wrong role encoding")
    return changed


def apply_roles(base,side,levels,catalog):
    require(base.get("rules")=="game" and base.get("fixture")=="bundled_match_pkm","Unvalidated rules/fixture")
    config=deepcopy(base);roles={r['id']:r for r in catalog['roles']};positions={p['id']:p for p in catalog['positions']}
    cells=config['teams'][side]['phases'][0]
    cb=sum(bool(positions[c['position']]['mask']&16) for c in cells);dm=sum(bool(positions[c['position']]['mask']&0x80) for c in cells)
    key=f'{3 if cb>=3 else 0}:{int(dm==1)}';slots={}
    for f in FACTORS:
        matches=[i for i,c in enumerate(cells) if c['position']==f['position']]
        require(len(matches)==1,'Factor position not unique');i=matches[0];slots[f['code']]=i
        require(cells[i]['role']==f['low_role'] and int(cells[i]['duty'])==0 and all(v==0 for v in cells[i]['instructions'].values()),'D00 role/duty/PI changed')
        for label in ('low','high'):
            role=f[label+'_role']
            require(role in catalog['role_eligibility_context'][key][f['position']][0] and roles[role]['phase']==0 and int(roles[role]['flags'])==f[label+'_flags'],'Role catalog/eligibility drift')
        cells[i]['role']=f['high_role'] if levels[f['code']]==1 else f['low_role']
    return config,slots


def prepare(lab):
    require(not (LOCAL/"seed-plan.json").exists(),"R0 already prepared; no reseeding")
    validation=read(ROOT/"data/valid-002/validation-summary.json")
    check_identity(validation["identity"],lab.identity,validation)
    source=read(ROOT/"data/tact-001-p1b/inputs.json");require(lab.identity==source["identity"],"P1B identity drift")
    catalog_path=lab.runtime/"source/tactics_ui/catalog.json";catalog=read(catalog_path)
    require(digest(catalog_path)==source["catalog_sha256"],"Catalog drift")
    for name,value in source["runtime_source_sha256"].items():require(source_hash(lab.runtime/"source"/name)==value,"Runtime source drift")
    old=read(ROOT/"local/tact-001-p1b/configs.json");configs={};setups={};audits=[];overrides={};role_manifest={}
    negative=[]
    for h,side in product(CONTEXTS,(0,1)):
        base=old[f"{h}-{side}-D00"]
        require(sha256(lab.server.encode_scenario(base,absolute=True)).hexdigest()==source['setups'][h][str(side)]['D00'],'Original D00 drift')
        for cell in matrix():
            arm=cell['id'];levels=cell['levels'];label=f'{h}-{side}-{arm}'
            config,slots=apply_roles(base,side,levels,catalog);config=validate_4231(config,lab.server,side)
            # No normalizer changes except the two declared role IDs are permitted.
            reset=deepcopy(config)
            for f in FACTORS:reset['teams'][side]['phases'][0][slots[f['code']]]['role']=f['low_role']
            require(reset==base,'Normalizer changed a non-role input')
            binary=LOCAL/'inputs'/(label+'.bin');value=lab.encode(config,binary)
            setups.setdefault(h,{}).setdefault(str(side),{})[arm]=value;configs[label]=config
            changes=binary_audit(lab.server.encode_scenario(base,absolute=True),binary.read_bytes(),side,levels,slots)
            audits.append(dict(context=h,side=side,design_id=arm,changed_records=changes,undeclared_changes=0))
            overrides[label]=dict(levels=levels,role_flags=wanted_flags(arm),slots=slots,duty=0,explicit_PI='all17groups0 in both phases; targets unchanged',setup_sha256=value)
            role_manifest[label]=[dict(side=s,phases=[[dict(slot=i,position=c['position'],role=c['role'],flags=int(lab.server.ROLES[c['role']]['flags']),duty=int(c['duty']),instructions=c['instructions'],target_player=c['target_player'],target_position=c['target_position']) for i,c in enumerate(ph)] for ph in team['phases']]) for s,team in enumerate(config['teams'])]
        require(setups[h][str(side)]['R00']==source['setups'][h][str(side)]['D00'],'R00 not byte-identical D00')
        for kind in ('unknown_role','wrong_phase','invalid_pi'):
            bad=deepcopy(base);cell=bad['teams'][side]['phases'][0][10]
            if kind=='unknown_role':cell['role']='TACT002_INVALID_ROLE'
            elif kind=='wrong_phase':cell['role']='OPCentreForward'
            else:cell['instructions']['0']=999
            try:lab.server.validate_scenario(bad)
            except ValueError:negative.append(dict(context=h,side=side,probe=kind,rejected=True))
            else:raise ValueError('Offline invalid role/phase/PI accepted')
    write(LOCAL/'configs.json',configs)
    REGISTRY.mkdir(exist_ok=True);lock=REGISTRY/'.allocation.lock';lock.touch(exist_ok=False)
    try:
        used=historical();write(PUBLIC/'excluded-seeds.json',sorted(used));tech=allocate(EXPERIMENT+'/technical-v1',3,used);main=allocate(EXPERIMENT+'/main-v1',64,used|set(tech))
        reservation=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+'/main-v1',seeds=[*tech,*main],technical_seeds=tech,main_seeds=main,excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
        with (REGISTRY/(EXPERIMENT+'.reserved.json')).open('x',encoding='utf8') as stream:
            json.dump(reservation,stream,indent=2);stream.flush();os.fsync(stream.fileno())
    finally:lock.unlink()
    write(LOCAL/'seed-plan.json',reservation);write(PUBLIC/'seed-plan.json',reservation)
    code={p:source_hash(ROOT/p) for p in CODE}
    write(PUBLIC/'design-matrix.json',dict(matrix=matrix(),matrix_sha256=config_hash(matrix()),design='full2x2 ST/AMC roles; R00=D00'))
    write(PUBLIC/'binary-diff-audit.json',dict(passed=True,cells=16,audits=audits))
    write(PUBLIC/'offline-negative-controls.json',dict(passed=True,probes=negative))
    write(PUBLIC/'role-manifest.json',dict(catalog_sha256=digest(catalog_path),factors=list(FACTORS),cells=role_manifest))
    write(PUBLIC/'inputs.json',dict(identity=lab.identity,catalog_sha256=digest(catalog_path),factors=list(FACTORS),fixed_contexts=source['fixed_contexts'],cell_overrides=overrides,setups=setups,synthetic_profiles=source['synthetic_profiles'],source_p1b_inputs_sha256=source_hash(ROOT/'data/tact-001-p1b/inputs.json'),holdout_profiles_unchanged_not_executed=source['holdout_profiles_unchanged_not_executed'],runtime_source_sha256=source['runtime_source_sha256'],code_sha256=code))
    names=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE_COMMIT,'--','analysis','data','experiments','research/specs','docs/program-2026-11-14'],cwd=ROOT,text=True).splitlines()
    write(PUBLIC/'historical-archive.json',dict(base_commit=BASE_COMMIT,sha256={n:source_hash(ROOT/n) for n in names}))
    contract=deepcopy(read(ROOT/'research/specs/TACT-001-P1B.json'))
    contract.update(experiment_id=EXPERIMENT,seed_namespace=EXPERIMENT+'/main-v1',identity=lab.identity,status='draft',hypothesis='Marginal ST role effect DLF-minus-CF on xGD averaged over the two AMC roles and equally weighted known synthetic opponents.',control='R00 byte-identical D00; CF/AttackingMidfielder, existing IP4231/OOP4411',intervention='Full2x2 CF/DLF x AttackingMidfielder/SecondStriker, only tested-side IP ST/AMC roles change')
    contract['metrics']=dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(PLAUSIBILITY))
    contract['design']=dict(unit='seed_block',n_blocks=32,sides=[0,1],control_arm='R00',matrix=matrix(),matrix_sha256=config_hash(matrix()),factors=list(FACTORS),setups=setups,
        arms=[dict(id=arm,setup_sha256=config_hash({h:{s:by[arm] for s,by in sides.items()} for h,sides in setups.items()})) for arm in ARMS],scenarios=[dict(id=h,opponent=h,strength='identical_synthetic_profiles',split='discovery') for h in CONTEXTS])
    contract['science']=dict(alpha=.05,power=.9,min_effect=.3,multiple_testing='none',family_size=1,primary_contrast='ST',secondary_contrasts=[list(p) for p in SECONDARY_PAIRS],secondary_family_size=7,
        analysis='analysis/analyse_tact002r0.py: ST(-.5,+.5,-.5,+.5), AMC(-.5,-.5,+.5,+.5), DoD(1,-1,-1,1); side mean then equal context weights; Welch95 and20000 stratified full-block bootstrap; Holm7 secondary.',
        exclusions='None. Incomplete blocks permit technical status only; no replacement seeds, retries, or winner selection.',negative_controls=['16input cells twice:32technical full matches and16A/A pairs','invalid binary exit108','unknown role/wrong phase/invalid PI offline'],readback_fields=['all coded records after original preparation','both phases/positions/role64/duty/17PIgroups','69attributes/1058profiles','both teams all instructions','effective seed','natural finish'],
        stopping_rule='512main/33technical attempts,900s cumulative supervised child time,1800s immutable UTC window,max4workers,90s progress timeout; error stops; no expansion.',selection_rule='No winner or new candidate selected; estimate ST primary, seven frozen secondary contrasts and pilot variance only.',power_basis='Unknown role contrastSD. Equal-stratum SD.8/1.2/1.8 imply full95width.400/.600/.900 and power.840/.504/.259 for.30 at64blocks. Not guaranteed90%-powered; future independent planning at effects.20/.30.',context_weights=[.5,.5],side_weights=[.5,.5],desired_full_ci_width=.5,bootstrap_resamples=20000,scheduler_rng=SCHEDULER_SEED)
    contract['budget']=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,absolute_study_wall_seconds=1800,raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3)
    contract['execution']=dict(code_sha256=code,public_inputs_sha256=source_hash(PUBLIC/'inputs.json'),seed_plan_sha256=source_hash(PUBLIC/'seed-plan.json'),matrix_file_sha256=source_hash(PUBLIC/'design-matrix.json'),role_manifest_sha256=source_hash(PUBLIC/'role-manifest.json'),offline_negative_sha256=source_hash(PUBLIC/'offline-negative-controls.json'),binary_audit_sha256=source_hash(PUBLIC/'binary-diff-audit.json'))
    contract['preregistration']=dict(commit=None,document='experiments/TACT-002-R0-preregistration.md',document_sha256=None,analysis='analysis/analyse_tact002r0.py',analysis_sha256=None)
    validate(contract);validate_design(contract);write(SPEC,contract);print('Prepared16rolecells and67newseeds; no full match executed.',flush=True)


def verify_code(config):
    require(all(source_hash(ROOT/p)==v for p,v in config["execution"]["code_sha256"].items()),"Frozen R0 implementation changed")
    for name,key in (("inputs.json","public_inputs_sha256"),("seed-plan.json","seed_plan_sha256"),("design-matrix.json","matrix_file_sha256"),("role-manifest.json","role_manifest_sha256"),("offline-negative-controls.json","offline_negative_sha256"),("binary-diff-audit.json","binary_audit_sha256")):
        require(source_hash(PUBLIC/name)==config["execution"][key],"Frozen R0 artifact changed")
    validate_design(config)


def register(commit):
    config=read(SPEC);config["status"]="registered";p=config["preregistration"];p["commit"]=commit
    for field in ("document","analysis"):
        p[field+"_sha256"]=sha256(subprocess.check_output(["git","show",commit+":"+p[field]],cwd=ROOT)).hexdigest()
    validate(config,executable=True);published_registration(config,SPEC);verify_code(config)
    plan=read(LOCAL/"seed-plan.json")
    require(not set(plan["seeds"])&historical(exclude_own=True),"Seed collision after reservation")
    receipt=dict(config=config,config_sha256=config_hash(config),seeds=plan["main_seeds"])
    require(len(schedule(receipt))==512,"Wrong main schedule")
    for path in (LOCAL/"receipt.json",REGISTRY/(EXPERIMENT+".json")):
        with path.open("x",encoding="utf8") as stream:json.dump(receipt,stream,indent=2)
    write(PUBLIC/"manifest.json",receipt)


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
            row.update(scenario=expected[row["key"]]["scenario"],config_sha256=receipt["config_sha256"])
            data.append(row)
    return data


def audit_contract(lab,row,job,task,log):
    require(event(rows(log),'native_profile_bindings_verified')['fields']==1058,'Incomplete native profiles')
    dump=read(task['dump']);config=job['config'];pi_cells=0;pi_groups=0;role_cells=0;observed={}
    for side,team in enumerate(config['teams']):
        flags=int.from_bytes(bytes.fromhex(dump['teams'][side]['creator_hex'])[:16],'little')
        for group,choice in team['instructions'].items():
            options=lab.server.GROUPS[int(group)]['options'];bit=next(o['native_bit'] for o in options if o['id']==choice)
            active={o['native_bit'] for o in options if o['native_bit'] and flags>>o['native_bit']&1};require(active==({bit} if bit else set()),'Native team instruction mismatch')
        for phase,cells in enumerate(team['phases']):
            for index,cell in enumerate(cells):
                slot=lab.server.OOP_MAP[side][index] if phase else index
                raw=bytes.fromhex(dump['teams'][side]['tactical_slots'][phase][slot]);expected=int(lab.server.ROLES[cell['role']]['flags'])|int(cell['duty'])
                require(struct.unpack_from('<Q',raw,64)[0]==expected,'Native role/duty mismatch');role_cells+=1
                pi=dump['teams'][side]['personal_instructions'][phase][slot]
                require(pi['target_player']==cell['target_player'] and pi['target_position']==cell['target_position'],'Native PI target mismatch')
                require(set(cell['instructions'])=={str(k) for k in lab.server.PIS},'Incomplete PI groups')
                for group,definition in lab.server.PIS.items():
                    options={o['id'] for o in definition['options'] if o['id']}
                    active={v for v in options if int(pi['flags'])>>v&1};choice=cell['instructions'][str(group)]
                    require(active==({choice} if choice else set()),'Native PI group mismatch');pi_groups+=1
                pi_cells+=1
                if side==job['side'] and phase==0:
                    for f in FACTORS:
                        if cell['position']==f['position']:observed[f['code']]=struct.unpack_from('<Q',raw,64)[0]
    require(role_cells==44 and pi_cells==44 and pi_groups==748 and observed==wanted_flags(job['arm']),'Role/PI coverage incomplete')
    return dict(input_contract_verified=True,profile_fields_verified=1058,native_roles_verified=role_cells,native_pi_cells_verified=pi_cells,native_pi_groups_verified=pi_groups,
        factor_levels=matrix()[ARMS.index(job['arm'])]['levels'],native_role_flags=observed,design_matrix_sha256=config_hash(matrix()))


def check_technical_publication():
    gate=read(PUBLIC/'technical-gate.json')
    require(gate.get('passed') is True and type(gate.get('ci_run')) is int,'Missing published technical/CI gate')
    ci=json.loads(subprocess.check_output(['gh','run','view',str(gate['ci_run']),'--json','status,conclusion,headSha'],cwd=ROOT,text=True))
    require(ci['status']=='completed' and ci['conclusion']=='success' and ci['headSha']==gate['published_commit'],'Technical publication CI not successful for exact gate commit')
    return gate


def execute(lab,kind):
    receipt=read(LOCAL/"receipt.json");published_registration(receipt["config"],SPEC);verify_code(receipt["config"])
    check_identity(receipt["config"]["identity"],lab.identity,read(ROOT/"data/valid-002/validation-summary.json"))
    frozen=read(PUBLIC/"inputs.json")
    require(digest(lab.runtime/"source/tactics_ui/catalog.json")==frozen["catalog_sha256"],"Catalog drift")
    require(all(source_hash(lab.runtime/"source"/n)==v for n,v in frozen["runtime_source_sha256"].items()),"Runtime source drift")
    if kind=="main":
        gate=check_technical_publication()
        require(read(LOCAL/"technical-summary.json")["passed"] and gate["passed"],"Missing technical gate")
        subprocess.run(["git","merge-base","--is-ancestor",gate["published_commit"],subprocess.check_output(["git","ls-remote","origin","refs/heads/main"],cwd=ROOT,text=True).split()[0]],cwd=ROOT,check=True)
        require(subprocess.check_output(["git","show",gate["published_commit"]+":data/tact-002-r0/technical-summary.json"],cwd=ROOT)==(PUBLIC/"technical-summary.json").read_bytes().replace(b"\r\n",b"\n"),"Technical report changed since publication")
    jobs=ordered_main(receipt) if kind=="main" else technical_jobs();configs=read(LOCAL/"configs.json")
    for j in jobs:
        label=f"{j['scenario']}-{j['side']}-{j['arm']}";j.update(config=configs[label],binary=LOCAL/"inputs"/(label+".bin"))
    for i in range(0,len(jobs),64):
        require(sum(p.stat().st_size for p in LOCAL.rglob("*") if p.is_file())<2*1024**3,"Raw artifact cap exceeded")
        require(shutil.disk_usage(LOCAL).free>20*1024**3,"Native disk reserve exhausted")
        lab.run(jobs[i:i+64],LOCAL/kind/f"part-{i//64:03d}",workers=4,audit=lambda *a:audit_contract(lab,*a))
    data=collect(kind,receipt)
    require(len(data)==len(jobs) and len({r["key"] for r in data})==len(jobs),"Incomplete native phase")
    if kind=="technical":
        groups={};compared=[]
        for row in data:groups.setdefault((row["scenario"],row["tested_side"],row["arm"]),[]).append(row)
        for key,pair in groups.items():
            if len(pair)==2:
                require(all(pair[0][f]==pair[1][f] for f in ("score","finish_tick","team_statistics","setup_sha256","seed")),"A/A repeat mismatch")
                compared.append(dict(context=key[0],side=key[1],design_id=key[2],exact=True))
        require(len(groups)==16 and len(compared)==16,"Readback/repeat coverage incomplete")
        invalid=LOCAL/"invalid.bin";invalid.write_bytes(b"TACT-002-R0 INTENTIONALLY INVALID")
        log=LOCAL/"negative.jsonl"
        write(LOCAL/'negative-attempt.json',dict(status='started',expected_returncode=108))
        try:
            result=subprocess.run([str(lab.server.native_host()),"--scenario-file",str(invalid),"--output",str(log)],cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        except Exception as error:
            write(LOCAL/'negative-attempt.json',dict(status='failed',error_type=type(error).__name__,expected_returncode=108));raise
        accepted=any(r.get('event')=='natural_match_finished' for r in rows(log)) if log.exists() else False
        negative=dict(status='expected_rejection' if result.returncode==108 and log.exists() and not accepted else 'failed',returncode=result.returncode,natural_match_finished=accepted,raw_log_sha256=digest(log) if log.exists() else None)
        write(LOCAL/'negative-attempt.json',negative)
        require(negative['status']=='expected_rejection','Negative binary did not reject as expected')
        write(LOCAL/"technical-summary.json",dict(passed=True,matches=32,readback_cells=16,repeats=compared,negative=dict(returncode=108,raw_log_sha256=digest(log)),native_identity=lab.identity,
            matrix_sha256=config_hash(matrix()),all_frozen_inputs_native_validated=True))
    print(kind,"complete",len(data),flush=True)


def main():
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("phase",choices=("prepare","register","technical","main","status"));parser.add_argument("--commit")
    parser.add_argument("--runtime",type=Path,default=ROOT/"local/runtime-v1114.6")
    parser.add_argument("--game",type=Path,default=Path("D:/steam/steamapps/common/Football Manager 27"))
    parser.add_argument("--child",action="store_true");args=parser.parse_args()
    if args.phase=="register":register(args.commit);return
    if args.phase=="status":print(json.dumps(read(LOCAL/"budget.json"),indent=2));return
    if args.child:
        state=read(LOCAL/"budget.json");active=state["active"]
        require(active and active["name"]==args.phase and supervisor_alive(active["supervisor_pid"]) and
                active["token_sha256"]==sha256(os.environ.get("TACT_P0_SUPERVISOR_TOKEN","").encode()).hexdigest(),"No authenticated live study supervisor")
        lease=read(ROOT/'local/global-native/native-execution.lease.json')
        require(lease['owner_pid']==active['supervisor_pid'] and lease['experiment']==EXPERIMENT and lease['workers']==4,'Missing central native lease')
        lab=NativeLab(args.runtime,args.game,LOCAL)
        prepare(lab) if args.phase=="prepare" else execute(lab,args.phase)
        return
    require((ROOT/".git").is_dir(),"Native phases only from central checkout, never worktrees")
    budget=DeadlineBudget(LOCAL/"budget.json",experiment=EXPERIMENT,seconds=900,caps={"technical":33,"main":512},wall_seconds=1800)
    keys=[] if args.phase=="prepare" else [j["key"] for j in technical_jobs()]+["negative-binary"] if args.phase=="technical" else [j["key"] for j in ordered_main(read(LOCAL/"receipt.json"))]
    if args.phase=="main":
        require(read(LOCAL/"technical-summary.json")["passed"],"Technical gate not passed");check_technical_publication()
    cmd=[sys.executable,str(Path(__file__).resolve()),args.phase,"--child","--runtime",str(args.runtime.resolve()),"--game",str(args.game.resolve())]
    with NativeLease(ROOT/"local/global-native",EXPERIMENT,workers=4) as lease:
        proof=lease.assert_owned()
        write(LOCAL/(args.phase+'.lease.json'),{k:proof[k] for k in ('schema','experiment','workers','owner_pid','acquired_utc')})
        budget.run(args.phase,"main" if args.phase=="main" else "technical",keys,cmd,ROOT,LOCAL/(args.phase+".stdout"))
    print((LOCAL/(args.phase+".stdout")).read_text(encoding="utf8",errors="replace")[-3000:])
    print("Charged seconds:",budget.load()["charged_seconds"],"/900; fixed UTC deadline:",budget.load()["wall_deadline_utc"])


if __name__=="__main__":main()

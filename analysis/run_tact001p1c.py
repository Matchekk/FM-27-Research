"""One preregistered P1C study, two native phases, one persistent study deadline."""
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
from research.cli import published_registration
from research.core import allocate, check_identity, config_hash, historical_seeds, schedule, validate
from research.discovery import validate_4231
from research.native import NativeLab, digest, event, read, require, rows, write
from analyse_tact001p1c import (ARMS,CONTEXTS,FACTORS,METRICS,SECONDARY,PLAUSIBILITY,
                              SCHEDULER_SEED,matrix,validate_design)

EXPERIMENT="TACT-001-P1C"
LOCAL=ROOT/"local/tact-001-p1c"
PUBLIC=ROOT/"data/tact-001-p1c"
SPEC=ROOT/"research/specs/TACT-001-P1C.json"
REGISTRY=ROOT/"local/registry"
BASE_COMMIT="317dec75d37eeef4199c4e6082a9da87b6396fc7"
CODE=("analysis/verify_tact001p1c.py","analysis/run_tact001p1c.py","analysis/analyse_tact001p1c.py","analysis/export_tact001p1c.py",
      "analysis/run_tact001p1b.py","analysis/analyse_tact001p1b.py","research/discovery.py","research/study_budget.py","research/budget.py","research/core.py",
      "research/native.py","research/stats.py","research/cli.py")


def source_hash(path):
    return sha256(Path(path).read_bytes().replace(b"\r\n",b"\n")).hexdigest()


def historical(exclude_own=False):
    used={0}
    for path in (ROOT/"data").iterdir():
        if path.is_dir() and not (exclude_own and path==PUBLIC):
            used.update(historical_seeds(path))
    for path in REGISTRY.glob("*.json"):
        if not (exclude_own and path.name.startswith(EXPERIMENT)):
            used.update(historical_seeds(path));used.update(read(path).get("seeds",[]))
    for name in ("valid002","valid002-run1","platform-smoke-001","tact-001-p0","tact-001-p1b"):
        used.update(historical_seeds(ROOT/"local"/name))
    return used


def binary_audit(before,after,side,levels):
    require(before[:12]==after[:12] and len(before)==len(after),"Binary header/count changed")
    a=list(struct.iter_unpack("<5I",before[12:]));b=list(struct.iter_unpack("<5I",after[12:]))
    changed=[dict(before=list(x),after=list(y)) for x,y in zip(a,b,strict=True) if x!=y]
    expected={((2,side,f["group_id"],0,f["low_id"]),(2,side,f["group_id"],0,f["high_id"]))
              for f in FACTORS if levels[f["code"]]==1}
    require({(tuple(x["before"]),tuple(x["after"])) for x in changed}==expected,"Undeclared binary change or wrong factor encoding")
    return changed


def prepare(lab):
    require(not (LOCAL/"seed-plan.json").exists(),"P1C already prepared; no reseeding")
    validation=read(ROOT/"data/valid-002/validation-summary.json")
    check_identity(validation["identity"],lab.identity,validation)
    source=read(ROOT/"data/tact-001-p1b/inputs.json")
    require(lab.identity==source["identity"],"P1B identity drift")
    catalog=lab.runtime/"source/tactics_ui/catalog.json"
    require(digest(catalog)==source["catalog_sha256"],"Catalog drift")
    for name,value in source["runtime_source_sha256"].items():
        require(source_hash(lab.runtime/"source"/name)==value,"Runtime source drift")
    old=read(ROOT/"local/tact-001-p1b/configs.json")
    configs={};setups={};audits=[];overrides={}
    for h,side,arm in product(CONTEXTS,(0,1),ARMS):
        label=f"{h}-{side}-{arm}";config=validate_4231(deepcopy(old[label]),lab.server,side)
        binary=LOCAL/"inputs"/(label+".bin")
        value=lab.encode(config,binary)
        require(value==source["setups"][h][str(side)][arm],"Frozen P1B candidate input changed")
        setups.setdefault(h,{}).setdefault(str(side),{})[arm]=value
        configs[label]=config
        base=old[f"{h}-{side}-D00"]
        changes=binary_audit(lab.server.encode_scenario(base,absolute=True),binary.read_bytes(),side,matrix()[ARMS.index(arm)]["levels"])
        audits.append(dict(context=h,side=side,design_id=arm,changed_records=changes,undeclared_changes=0))
        overrides[label]=source["cell_overrides"][label]
    write(LOCAL/"configs.json",configs)
    # All public/private historical, failed and still reserved seed values excluded.
    used=historical();write(PUBLIC/"excluded-seeds.json",sorted(used));tech=allocate(EXPERIMENT+"/technical-v1",3,used)
    main=allocate(EXPERIMENT+"/main-v1",128,used|set(tech))
    reservation=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+"/main-v1",seeds=[*tech,*main],technical_seeds=tech,main_seeds=main,
        excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
    REGISTRY.mkdir(exist_ok=True)
    with (REGISTRY/(EXPERIMENT+".reserved.json")).open("x",encoding="utf8") as stream:json.dump(reservation,stream,indent=2)
    write(LOCAL/"seed-plan.json",reservation);write(PUBLIC/"seed-plan.json",reservation)
    code={p:source_hash(ROOT/p) for p in CODE}
    write(PUBLIC/"design-matrix.json",dict(matrix=matrix(),matrix_sha256=config_hash(matrix()),design="frozen direct two-arm package comparison, not a half-fraction"))
    write(PUBLIC/"binary-diff-audit.json",dict(passed=True,cells=8,audits=audits))
    write(PUBLIC/"inputs.json",dict(identity=lab.identity,catalog_sha256=digest(catalog),factors=list(FACTORS),fixed_contexts=source["fixed_contexts"],
        cell_overrides=overrides,setups=setups,synthetic_profiles=source["synthetic_profiles"],source_p1b_inputs_sha256=source_hash(ROOT/"data/tact-001-p1b/inputs.json"),
        holdout_profiles_unchanged_not_executed=source["holdout_profiles_unchanged_not_executed"],runtime_source_sha256=source["runtime_source_sha256"],code_sha256=code))
    contract=deepcopy(read(ROOT/"research/specs/TACT-001-P1B.json"))
    contract.update(experiment_id=EXPERIMENT,seed_namespace=EXPERIMENT+"/main-v1",identity=lab.identity,status="draft",
        hypothesis="Frozen D15 improves actual points per match over D00 at equal weights of the two existing synthetic discovery contexts.",
        control="D00 unchanged original own IP4231/OOP4411",intervention="Frozen D15: more pressing, higher line, higher tempo, shorter passing; standard width")
    contract["metrics"]=dict(primary="points",secondary=list(SECONDARY),plausibility=list(PLAUSIBILITY))
    contract["design"]=dict(unit="seed_block",n_blocks=64,sides=[0,1],control_arm="D00",matrix=matrix(),matrix_sha256=config_hash(matrix()),factors=list(FACTORS),setups=setups,
        arms=[dict(id=arm,setup_sha256=config_hash({h:{s:by[arm] for s,by in sides.items()} for h,sides in setups.items()})) for arm in ARMS],
        scenarios=[dict(id=h,opponent=h,strength="identical_synthetic_profiles",split="discovery") for h in CONTEXTS])
    contract["science"]=dict(alpha=.05,power=.9,min_effect=.15,multiple_testing="none",family_size=1,
        analysis="analysis/analyse_tact001p1c.py: D15-D00 points; side means within seed; fixed contexts 1/2; Welch95 and 20000 stratified seed-block bootstrap; Holm5 secondary.",
        exclusions="None. Incomplete blocks allow technical status only. No replacement seeds or retries.",
        negative_controls=["8 input cells twice: 16 complete audits and 8 exact A/A repeats","invalid binary exit108"],
        readback_fields=["both phases","roles/duties/PI","69 attributes","1058 profile fields","all team instruction bits","effective seed","natural finish"],
        stopping_rule="512 main, 17 technical attempts; child wall cap900s; immutable UTC window1800s; max4 workers timeout90; stop identity/input error; no effect stopping.",
        selection_rule="D15 only, D09 archived. Adequate pilot signal requires mean>=.15 points, CI95 lower>0, width<=.30 and positive means in both contexts. Otherwise recommend new roles/OOP factors rather than indefinite retesting. No automatic follow-up.",
        power_basis="Precision pilot, not guaranteed90%-powered; P1B selected-pair SD planning is conditional. New future power at effects .10/.15/.20, widths .20/.30 using observed and simultaneous-normal-model SD upper bounds; bounded SD3 sensitivity.",
        context_weights=[.5,.5],side_weights=[.5,.5],secondary_family_size=5,bootstrap_resamples=20000,scheduler_rng=SCHEDULER_SEED,
        desired_full_ci_width=.30,future_effects=[.10,.15,.20],future_widths=[.20,.30])
    contract["budget"]=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=17,total_native_wall_seconds=900,absolute_study_wall_seconds=1800,
        raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3)
    contract["execution"]=dict(code_sha256=code,public_inputs_sha256=source_hash(PUBLIC/"inputs.json"),seed_plan_sha256=source_hash(PUBLIC/"seed-plan.json"),matrix_file_sha256=source_hash(PUBLIC/"design-matrix.json"))
    contract["preregistration"]=dict(commit=None,document="experiments/TACT-001-P1C-preregistration.md",document_sha256=None,analysis="analysis/analyse_tact001p1c.py",analysis_sha256=None)
    validate(contract);validate_design(contract);write(SPEC,contract)
    print("Prepared 8 unchanged P1B inputs and 131 new reserved seeds.",flush=True)


def verify_code(config):
    require(all(source_hash(ROOT/p)==v for p,v in config["execution"]["code_sha256"].items()),"Frozen P1C implementation changed")
    for name,key in (("inputs.json","public_inputs_sha256"),("seed-plan.json","seed_plan_sha256"),("design-matrix.json","matrix_file_sha256")):
        require(source_hash(PUBLIC/name)==config["execution"][key],"Frozen P1C artifact changed")
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
    profiles=event(rows(log),"native_profile_bindings_verified")
    require(profiles["fields"]==1058,"Incomplete native profiles")
    dump=read(task["dump"]);config=job["config"]
    for side,team in enumerate(config["teams"]):
        flags=int.from_bytes(bytes.fromhex(dump["teams"][side]["creator_hex"])[:16],"little")
        for group,choice in team["instructions"].items():
            options=lab.server.GROUPS[int(group)]["options"]
            bit=next(o["native_bit"] for o in options if o["id"]==choice)
            active={o["native_bit"] for o in options if o["native_bit"] and flags>>o["native_bit"]&1}
            require(active==({bit} if bit else set()),"Native team instruction mismatch")
    levels=matrix()[ARMS.index(job["arm"])]["levels"]
    flags=int.from_bytes(bytes.fromhex(dump["teams"][job["side"]]["creator_hex"])[:16],"little")
    bits={f["code"]:f["high_bit"] if flags>>f["high_bit"]&1 else 0 for f in FACTORS}
    require(bits=={f["code"]:f["high_bit"] if levels[f["code"]]==1 else 0 for f in FACTORS},"Native input does not match negative-half design")
    return dict(input_contract_verified=True,profile_fields_verified=1058,factor_levels=levels,native_factor_bits=bits,design_matrix_sha256=config_hash(matrix()))


def execute(lab,kind):
    receipt=read(LOCAL/"receipt.json");published_registration(receipt["config"],SPEC);verify_code(receipt["config"])
    check_identity(receipt["config"]["identity"],lab.identity,read(ROOT/"data/valid-002/validation-summary.json"))
    frozen=read(PUBLIC/"inputs.json")
    require(digest(lab.runtime/"source/tactics_ui/catalog.json")==frozen["catalog_sha256"],"Catalog drift")
    require(all(source_hash(lab.runtime/"source"/n)==v for n,v in frozen["runtime_source_sha256"].items()),"Runtime source drift")
    if kind=="main":
        gate=read(PUBLIC/"technical-gate.json")
        require(read(LOCAL/"technical-summary.json")["passed"] and gate["passed"],"Missing technical gate")
        subprocess.run(["git","merge-base","--is-ancestor",gate["published_commit"],subprocess.check_output(["git","ls-remote","origin","refs/heads/main"],cwd=ROOT,text=True).split()[0]],cwd=ROOT,check=True)
        require(subprocess.check_output(["git","show",gate["published_commit"]+":data/tact-001-p1c/technical-summary.json"],cwd=ROOT)==(PUBLIC/"technical-summary.json").read_bytes().replace(b"\r\n",b"\n"),"Technical report changed since publication")
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
        require(len(groups)==8 and len(compared)==8,"Readback/repeat coverage incomplete")
        invalid=LOCAL/"invalid.bin";invalid.write_bytes(b"TACT-001-P1C INTENTIONALLY INVALID")
        log=LOCAL/"negative.jsonl"
        result=subprocess.run([str(lab.server.native_host()),"--scenario-file",str(invalid),"--output",str(log)],cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        require(result.returncode==108 and not any(r.get("event")=="natural_match_finished" for r in rows(log)),"Negative binary was accepted")
        write(LOCAL/"technical-summary.json",dict(passed=True,matches=16,readback_cells=8,repeats=compared,negative=dict(returncode=108,raw_log_sha256=digest(log)),native_identity=lab.identity,
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
        lab=NativeLab(args.runtime,args.game,LOCAL)
        prepare(lab) if args.phase=="prepare" else execute(lab,args.phase)
        return
    budget=DeadlineBudget(LOCAL/"budget.json",experiment=EXPERIMENT,seconds=900,caps={"technical":17,"main":512},wall_seconds=1800)
    keys=[] if args.phase=="prepare" else [j["key"] for j in technical_jobs()]+["negative-binary"] if args.phase=="technical" else [j["key"] for j in ordered_main(read(LOCAL/"receipt.json"))]
    if args.phase=="main":require(read(LOCAL/"technical-summary.json")["passed"],"Technical gate not passed")
    cmd=[sys.executable,str(Path(__file__).resolve()),args.phase,"--child","--runtime",str(args.runtime.resolve()),"--game",str(args.game.resolve())]
    budget.run(args.phase,"main" if args.phase=="main" else "technical",keys,cmd,ROOT,LOCAL/(args.phase+".stdout"))
    print((LOCAL/(args.phase+".stdout")).read_text(encoding="utf8",errors="replace")[-3000:])
    print("Charged seconds:",budget.load()["charged_seconds"],"/900; fixed UTC deadline:",budget.load()["wall_deadline_utc"])


if __name__=="__main__":main()

"""One preregistered P1B study, two native phases, one persistent study deadline."""
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
from analyse_tact001p1b import (ARMS,CONTEXTS,FACTORS,METRICS,SECONDARY,PLAUSIBILITY,
                              SCHEDULER_SEED,matrix,validate_design)

EXPERIMENT="TACT-001-P1B"
LOCAL=ROOT/"local/tact-001-p1b"
PUBLIC=ROOT/"data/tact-001-p1b"
SPEC=ROOT/"research/specs/TACT-001-P1B.json"
REGISTRY=ROOT/"local/registry"
BASE_COMMIT="e1a9ecafcd16c783e96c2a7478389c69ac8afbfa"
CODE=("analysis/run_tact001p1b.py","analysis/analyse_tact001p1b.py","analysis/export_tact001p1b.py",
      "research/discovery.py","research/study_budget.py","research/budget.py","research/core.py",
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
    for name in ("valid002","valid002-run1","platform-smoke-001"):
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
    require(not (LOCAL/"seed-plan.json").exists(),"P1B already prepared; no reseeding")
    validation=read(ROOT/"data/valid-002/validation-summary.json")
    check_identity(validation["identity"],lab.identity,validation)
    catalog=lab.runtime/"source/tactics_ui/catalog.json"
    require(digest(catalog)=="c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c","Catalog drift; stop before selecting new levels")
    old=read(ROOT/"local/tact-001-p0/configs.json")
    p0=read(ROOT/"data/tact-001-p0/inputs.json")
    configs={};setups={};audits=[];fixed={};overrides={}
    for h,side in product(CONTEXTS,(0,1)):
        key=f"{h}-{side}"
        base=old[key+"-baseline"]
        expected=p0["setups"][h][str(side)]["baseline"]
        require(sha256(lab.server.encode_scenario(base,absolute=True)).hexdigest()==expected,"P0 baseline changed")
        fixed[key]=p0["descriptors"][key+"-baseline"]
        for row in matrix():
            arm=row["id"];levels=row["levels"];config=deepcopy(base)
            for f in FACTORS:
                g=lab.server.GROUPS[f["group_id"]]
                require(g["name"]==f["group"] and any(o["id"]==f["high_id"] and o["native_bit"]==f["high_bit"] for o in g["options"])
                        and any(o["id"]==f["low_id"] and o["native_bit"]==0 for o in g["options"]),"Native catalog factor mismatch")
                config["teams"][side]["instructions"][str(f["group_id"])]=f["high_id"] if levels[f["code"]]==1 else f["low_id"]
            config=validate_4231(config,lab.server,side)
            label=key+"-"+arm;binary=LOCAL/"inputs"/(label+".bin")
            setups.setdefault(h,{}).setdefault(str(side),{})[arm]=lab.encode(config,binary)
            configs[label]=config
            changes=binary_audit(lab.server.encode_scenario(base,absolute=True),binary.read_bytes(),side,levels)
            unchanged=deepcopy(config)
            for f in FACTORS:
                group=str(f["group_id"])
                unchanged["teams"][side]["instructions"][group]=base["teams"][side]["instructions"][group]
            require(unchanged==base,"Non-factor input changed")
            audits.append(dict(context=h,side=side,design_id=arm,changed_records=changes,undeclared_changes=0))
            overrides[label]=dict(levels=levels,tested_side=side,instructions=config["teams"][side]["instructions"],setup_sha256=setups[h][str(side)][arm])
        require(setups[h][str(side)]["D00"]==expected,"D00 is not the original all-standard baseline")
    write(LOCAL/"configs.json",configs)
    used=historical();tech=allocate(EXPERIMENT+"/technical-v1",3,used)
    main=allocate(EXPERIMENT+"/main-v1",64,used|set(tech))
    reservation=dict(experiment_id=EXPERIMENT,namespace=EXPERIMENT+"/main-v1",seeds=[*tech,*main],technical_seeds=tech,main_seeds=main,
                     excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
    REGISTRY.mkdir(exist_ok=True)
    with (REGISTRY/(EXPERIMENT+".reserved.json")).open("x",encoding="utf8") as stream:json.dump(reservation,stream,indent=2)
    write(LOCAL/"seed-plan.json",reservation);write(PUBLIC/"seed-plan.json",reservation)
    code={p:source_hash(ROOT/p) for p in CODE}
    write(PUBLIC/"design-matrix.json",dict(fraction=-1,generator="E=-A*B*C*D",defining_relation="I=-ABCDE",matrix=matrix(),matrix_sha256=config_hash(matrix())))
    write(PUBLIC/"binary-diff-audit.json",dict(passed=True,cells=64,audits=audits))
    write(PUBLIC/"inputs.json",dict(identity=lab.identity,catalog_sha256=digest(catalog),factors=list(FACTORS),
        fixed_contexts=fixed,cell_overrides=overrides,setups=setups,synthetic_profiles=p0["synthetic_profiles"],
        source_p0_inputs_sha256=source_hash(ROOT/"data/tact-001-p0/inputs.json"),
        holdout_profiles_unchanged_not_executed=["holdout_midblock","holdout_direct_counter"],
        runtime_source_sha256={p.name:source_hash(p) for p in (lab.runtime/"source").glob("*.py")},code_sha256=code))
    contract=deepcopy(read(ROOT/"research/specs/TACT-001-P0.json"))
    contract.update(experiment_id=EXPERIMENT,seed_namespace=EXPERIMENT+"/main-v1",identity=lab.identity,
        hypothesis="Five high-minus-standard xGD main contrasts in the negative resolution-V half-fraction; two equally weighted frozen contexts.",
        control="D00 all-standard own IP4231/OOP4411; identical P0 profiles and management",
        intervention="A more pressing, B higher line, C higher tempo, D shorter passing, E wider attacking width; E=-ABCD",status="draft")
    contract["metrics"]=dict(primary="xgd",secondary=list(SECONDARY),plausibility=list(PLAUSIBILITY))
    contract["design"]=dict(unit="seed_block",n_blocks=32,sides=[0,1],control_arm="D00",fraction=-1,generator="E=-A*B*C*D",
        matrix=matrix(),matrix_sha256=config_hash(matrix()),factors=list(FACTORS),setups=setups,
        arms=[dict(id=arm,setup_sha256=config_hash({h:{s:by[arm] for s,by in sides.items()} for h,sides in setups.items()}),setup_sha256_type="cell-map") for arm in ARMS],
        scenarios=[dict(id=h,opponent=h,strength="identical_synthetic_profiles",split="discovery") for h in CONTEXTS])
    contract["science"]=dict(alpha=.05,power=.9,min_effect=.2,multiple_testing="holm",family_size=5,
        analysis="analysis/analyse_tact001p1b.py: mains coefficient X/8; physical pair DoDs XiXj/4; side mean then context weight 1/2; Welch and 20000 stratified complete-block bootstrap; Holm5/10/25 separate families.",
        exclusions="No result exclusions, replacement seeds or retries; any incomplete block permits technical status only.",
        negative_controls=["64 complete input cell readbacks","8 exact repeats: both contexts/sides, D00/D01","invalid binary exit108"],
        readback_fields=["both phases","roles/duties/PI","69 attributes","23 profile fields per player","all team instruction bits including C/D/E","effective seed","natural finish"],
        stopping_rule="2048 main and 73 technical attempt caps; fixed 2400s child time and 40min UTC study deadline; max4 workers, timeout90; no retries or effect stopping.",
        selection_rule="At most two measured cells with positive xGD gain over D00 in both contexts, sorted by worst context gain then equally weighted gain then design ID. No confirmation or holdout execution.",
        power_basis="P1A conditional transfer model: SE .0464, marginal95 halfwidth .0929, per-main Bonferroni alpha .01 power .9457 for .20. Unknown new factor variances; no joint90-power claim.",
        context_weights=[.5,.5],side_weights=[.5,.5],secondary_family_size=25,interaction_family_size=10,
        bootstrap_resamples=20000,scheduler_rng=SCHEDULER_SEED)
    contract["budget"]=dict(max_matches=2048,max_workers=4,timeout_seconds=90,max_technical_attempts=73,total_native_wall_seconds=2400,absolute_study_wall_seconds=2400,
                            raw_artifact_limit_bytes=4*1024**3,disk_reserve_bytes=20*1024**3)
    contract["execution"]=dict(code_sha256=code,public_inputs_sha256=source_hash(PUBLIC/"inputs.json"),seed_plan_sha256=source_hash(PUBLIC/"seed-plan.json"),matrix_file_sha256=source_hash(PUBLIC/"design-matrix.json"))
    contract["preregistration"]=dict(commit=None,document="experiments/TACT-001-P1B-preregistration.md",document_sha256=None,analysis="analysis/analyse_tact001p1b.py",analysis_sha256=None)
    validate(contract);validate_design(contract);write(SPEC,contract)
    print("Prepared 64 cells with negative half-fraction, original D00 inputs and 67 new reserved seeds.",flush=True)


def verify_code(config):
    require(all(source_hash(ROOT/p)==v for p,v in config["execution"]["code_sha256"].items()),"Frozen P1B implementation changed")
    for name,key in (("inputs.json","public_inputs_sha256"),("seed-plan.json","seed_plan_sha256"),("design-matrix.json","matrix_file_sha256")):
        require(source_hash(PUBLIC/name)==config["execution"][key],"Frozen P1B artifact changed")
    validate_design(config)


def register(commit):
    config=read(SPEC);config["status"]="registered";p=config["preregistration"];p["commit"]=commit
    for field in ("document","analysis"):
        p[field+"_sha256"]=sha256(subprocess.check_output(["git","show",commit+":"+p[field]],cwd=ROOT)).hexdigest()
    validate(config,executable=True);published_registration(config,SPEC);verify_code(config)
    plan=read(LOCAL/"seed-plan.json")
    require(not set(plan["seeds"])&historical(exclude_own=True),"Seed collision after reservation")
    receipt=dict(config=config,config_sha256=config_hash(config),seeds=plan["main_seeds"])
    require(len(schedule(receipt))==2048,"Wrong main schedule")
    for path in (LOCAL/"receipt.json",REGISTRY/(EXPERIMENT+".json")):
        with path.open("x",encoding="utf8") as stream:json.dump(receipt,stream,indent=2)
    write(PUBLIC/"manifest.json",receipt)


def ordered_main(receipt):
    jobs=schedule(receipt);random.Random(SCHEDULER_SEED).shuffle(jobs)
    return jobs


def technical_jobs():
    seeds=read(LOCAL/"seed-plan.json")["technical_seeds"]
    jobs=[dict(key=f"tech-{h}-{side}-{arm}-r0",scenario=h,side=side,arm=arm,seed=seeds[CONTEXTS.index(h)]) for h,side,arm in product(CONTEXTS,(0,1),ARMS)]
    jobs.extend(dict(key=f"tech-{h}-{side}-{arm}-r1",scenario=h,side=side,arm=arm,seed=seeds[CONTEXTS.index(h)]) for h,side,arm in product(CONTEXTS,(0,1),("D00","D01")))
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
    if kind=="main":
        gate=read(PUBLIC/"technical-gate.json")
        require(read(LOCAL/"technical-summary.json")["passed"] and gate["passed"],"Missing technical gate")
        subprocess.run(["git","merge-base","--is-ancestor",gate["published_commit"],subprocess.check_output(["git","ls-remote","origin","refs/heads/main"],cwd=ROOT,text=True).split()[0]],cwd=ROOT,check=True)
        require(subprocess.check_output(["git","show",gate["published_commit"]+":data/tact-001-p1b/technical-summary.json"],cwd=ROOT)==(PUBLIC/"technical-summary.json").read_bytes().replace(b"\r\n",b"\n"),"Technical report changed since publication")
    jobs=ordered_main(receipt) if kind=="main" else technical_jobs();configs=read(LOCAL/"configs.json")
    for j in jobs:
        label=f"{j['scenario']}-{j['side']}-{j['arm']}";j.update(config=configs[label],binary=LOCAL/"inputs"/(label+".bin"))
    for i in range(0,len(jobs),64):
        require(sum(p.stat().st_size for p in LOCAL.rglob("*") if p.is_file())<4*1024**3,"Raw artifact cap exceeded")
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
        require(len(groups)==64 and len(compared)==8,"Readback/repeat coverage incomplete")
        invalid=LOCAL/"invalid.bin";invalid.write_bytes(b"TACT-001-P1B INTENTIONALLY INVALID")
        log=LOCAL/"negative.jsonl"
        result=subprocess.run([str(lab.server.native_host()),"--scenario-file",str(invalid),"--output",str(log)],cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        require(result.returncode==108 and not any(r.get("event")=="natural_match_finished" for r in rows(log)),"Negative binary was accepted")
        write(LOCAL/"technical-summary.json",dict(passed=True,matches=72,readback_cells=64,repeats=compared,negative=dict(returncode=108,raw_log_sha256=digest(log)),native_identity=lab.identity,
            matrix_sha256=config_hash(matrix()),new_CDE_native_validated=True))
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
    budget=DeadlineBudget(LOCAL/"budget.json")
    keys=[] if args.phase=="prepare" else [j["key"] for j in technical_jobs()]+["negative-binary"] if args.phase=="technical" else [j["key"] for j in ordered_main(read(LOCAL/"receipt.json"))]
    if args.phase=="main":require(read(LOCAL/"technical-summary.json")["passed"],"Technical gate not passed")
    cmd=[sys.executable,str(Path(__file__).resolve()),args.phase,"--child","--runtime",str(args.runtime.resolve()),"--game",str(args.game.resolve())]
    budget.run(args.phase,"main" if args.phase=="main" else "technical",keys,cmd,ROOT,LOCAL/(args.phase+".stdout"))
    print((LOCAL/(args.phase+".stdout")).read_text(encoding="utf8",errors="replace")[-3000:])
    print("Charged seconds:",budget.load()["charged_seconds"],"/2400; fixed UTC deadline:",budget.load()["wall_deadline_utc"])


if __name__=="__main__":main()

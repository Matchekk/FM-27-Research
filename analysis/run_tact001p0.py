"""One bounded TACT-001-P0 pilot. Supervised children share one durable budget."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.budget import NativeBudget, atomic, supervisor_alive
from research.cli import published_registration
from research.core import allocate, canonical, check_identity, config_hash, historical_seeds, schedule, validate
from research.discovery import validate_4231
from research.native import NativeLab, digest, event, read, require, rows, write
from analyse_tact001p0 import ARMS, SCENARIOS, SECONDARY, analyse

LOCAL=ROOT/"local/tact-001-p0"
PUBLIC=ROOT/"data/tact-001-p0"
SPEC=ROOT/"research/specs/TACT-001-P0.json"
REGISTRY=ROOT/"local/registry"
EXPERIMENT="TACT-001-P0"
CODE=("analysis/run_tact001p0.py","analysis/analyse_tact001p0.py","research/budget.py",
      "research/native.py","research/core.py","research/stats.py","research/cli.py")
MAIN_NAMESPACE=EXPERIMENT+"/main-v1"


def source_hash(path):
    return sha256(Path(path).read_bytes().replace(b"\r\n",b"\n")).hexdigest()


def historical(exclude_own=False):
    used=historical_seeds(ROOT/"data")
    for path in REGISTRY.glob("*.json"):
        if exclude_own and path.name.startswith(EXPERIMENT):
            continue
        used.update(read(path)["seeds"])
    for name in ("valid002","valid002-run1","platform-smoke-001"):
        used.update(historical_seeds(ROOT/"local"/name))
    return used


def instruction(server,team,name,bit):
    group=next(g for g in server.GROUPS.values() if g["name"]==name)
    option=next(o for o in group["options"] if o["native_bit"]==bit)
    team["instructions"][str(group["id"])]=option["id"]
    return dict(group_id=group["id"],option_id=option["id"],native_bit=bit)


def own_team(lab):
    s=lab.server
    team=deepcopy(s.DEFAULT["teams"][1])
    team.update(name="Synthetic control",tactic_name="Own 4231 - P0",mentality=4,roster_size=23,native_extra_team_bits="0")
    for g in s.GROUPS.values():
        neutral=next((o for o in g["options"] if o["native_bit"]==0),g["options"][len(g["options"])//2])
        team["instructions"][str(g["id"])]=neutral["id"]
    profile=dict(height_cm=180,age=25,professionalism=12,loyalty=12,sportsmanship=12,temperament=12,
                 pressure=12,ambition=12,adaptability=12,traits_low=0,traits_high=0,current_ability=120,
                 home_reputation=5000,current_reputation=5000,world_reputation=5000,weight_kg=75,
                 condition=10000,sharpness=10000,sharpness_secondary=10000,fatigue_raw=0,
                 team_cohesion=80,club_cohesion=100,morale=20)
    for i,p in enumerate(team["players"]):
        keeper=i in (0,11)
        p["name"]=f"Synthetic {i:02d}"
        p["attributes"]=[20 if keeper and a==0 or not keeper and 2<=a<15 else 0 if a<15 else 60 for a in range(69)]
        p["native_profile"]=dict(profile)
        p.pop("source_uid",None)
    team["lineup"]=list(range(11))
    team["captains"]=[2,3]
    team["takers"]={k:[8,7,9] for k in s.TAKER_KEYS}
    neutral=s.unpack_oi(0x80000)
    team["opposition"]["players"]=[dict(neutral) for _ in team["opposition"]["players"]]
    team["opposition"]["positions"]={k:dict(neutral) for k in team["opposition"]["positions"]}
    ip_roles=("Goalkeeper","FullBack","CentreBack","CentreBack","FullBack","DefensiveMidfielder",
              "DeepLyingPlaymaker","Winger","AttackingMidfielder","Winger","CentreForward")
    oop_positions=("GK","DR","DCR","DCL","DL","MCR","MCL","MR","AMC","ML","ST")
    oop_roles=("OPGoalkeeper","OPFullBack","OPCentreBack","OPCentreBack","OPFullBack","OPCentralMidfielder",
               "OPCentralMidfielder","OPWideMidfielder","OPAttackingMidfielder","OPWideMidfielder","OPCentreForward")
    for phase,cells in enumerate(team["phases"]):
        for i,cell in enumerate(cells):
            cell.update(role=(ip_roles if phase==0 else oop_roles)[i],duty="0",target_player=255,target_position=0,
                        instructions={str(g):0 for g in s.PIS})
            if phase:
                cell["position"]=oop_positions[i]
    return team


def setup(lab):
    s=lab.server
    team=own_team(lab)
    opponent={}
    styles={"high_press":{"TriggerPress":65,"DefensiveLine":57,"LineOfEngagement":61,"DefensiveTransition":70},
            "deep_block":{"TriggerPress":67,"DefensiveLine":58,"LineOfEngagement":63,"DefensiveTransition":71},
            "holdout_midblock":{"TriggerPress":0,"DefensiveLine":0,"LineOfEngagement":62,"DefensiveTransition":0},
            "holdout_direct_counter":{"TriggerPress":0,"DefensiveLine":58,"LineOfEngagement":62,
                                      "AttackingTransition":54,"PassingDirectness":2,"Tempo":47}}
    for name,changes in styles.items():
        opponent[name]=deepcopy(team)
        opponent[name]["name"]=name
        for key,bit in changes.items():
            instruction(s,opponent[name],key,bit)
    configs,setups={},{}
    choices={}
    for scenario,side,arm in product(SCENARIOS,(0,1),ARMS):
        own=deepcopy(team)
        p=arm in ("press","combined")
        l=arm in ("line","combined")
        choices["press_high" if p else "press_standard"]=instruction(s,own,"TriggerPress",66 if p else 0)
        choices["line_high" if l else "line_standard"]=instruction(s,own,"DefensiveLine",57 if l else 0)
        config=dict(deepcopy(s.DEFAULT),rules="game",teams=[None,None])
        config["teams"][side]=s.transplant_team(own,side)
        config["teams"][1-side]=s.transplant_team(opponent[scenario],1-side)
        config=validate_4231(config,s,side)
        key=f"{scenario}-{side}-{arm}"
        binary=LOCAL/"inputs"/(key+".bin")
        hashed=lab.encode(config,binary)
        configs[key]=config
        setups.setdefault(scenario,{}).setdefault(str(side),{})[arm]=hashed
    holdouts={name:dict(profile_sha256=config_hash(value),instructions=value["instructions"],
                       phases=value["phases"],simulated=False) for name,value in opponent.items() if name.startswith("holdout")}
    write(LOCAL/"configs.json",configs)
    descriptors={k:dict(rules=v["rules"],teams=[dict(name=t["name"],mentality=t["mentality"],instructions=t["instructions"],
                    native_extra_team_bits=t["native_extra_team_bits"],phases=t["phases"],lineup=t["lineup"],
                    roster_size=t["roster_size"],active_profile_sha256=config_hash([dict(attributes=p["attributes"],profile=p["native_profile"]) for p in t["players"][:23]])) for t in v["teams"]]) for k,v in configs.items()}
    return configs,setups,choices,holdouts,descriptors,team


def prepare(lab):
    require(not (LOCAL/"seed-plan.json").exists(),"Pilot already prepared")
    expected=read(ROOT/"data/valid-002/validation-summary.json")
    check_identity(expected["identity"],lab.identity,expected)
    configs,setups,choices,holdouts,descriptors,team=setup(lab)
    # Assert all arms differ only in the two assigned instruction records.
    for scenario,side in product(SCENARIOS,(0,1)):
        baseline=configs[f"{scenario}-{side}-baseline"]
        for arm in ARMS:
            changed=deepcopy(configs[f"{scenario}-{side}-{arm}"])
            for group in ("9","10"):
                changed["teams"][side]["instructions"][group]=baseline["teams"][side]["instructions"][group]
            require(changed==baseline,"Arm has undeclared changes")
    used=historical()
    technical=allocate(EXPERIMENT+"/technical-v1",3,used)
    main=allocate(MAIN_NAMESPACE,16,used|set(technical))
    reservation=dict(experiment_id=EXPERIMENT,seeds=[*technical,*main],technical_seeds=technical,main_seeds=main,
                     namespace=MAIN_NAMESPACE,excluded_seed_count=len(used),excluded_seed_set_sha256=config_hash(sorted(used)))
    REGISTRY.mkdir(exist_ok=True)
    with (REGISTRY/(EXPERIMENT+".reserved.json")).open("x",encoding="utf8") as stream:
        json.dump(reservation,stream,indent=2)
    write(LOCAL/"seed-plan.json",reservation)
    PUBLIC.mkdir(parents=True,exist_ok=True)
    write(PUBLIC/"seed-plan.json",reservation)
    code={p:source_hash(ROOT/p) for p in CODE}
    public_inputs=dict(identity=lab.identity,choices=choices,setups=setups,holdouts=holdouts,descriptors=descriptors,
       synthetic_profiles=dict(attribute_rule="GK at roster slots 0,11: GK 20, other position values 0; outfield GK/Sweeper 0, positions 2..14 20; every ability index 15..68 raw 60",native_profile=team["players"][0]["native_profile"],
                               same_for_both_teams=True),runtime_source_sha256={p.name:source_hash(p) for p in (lab.runtime/"source").glob("*.py")},code_sha256=code)
    write(PUBLIC/"inputs.json",public_inputs)
    contract=dict(schema_version=1,experiment_id=EXPERIMENT,module="TACT",kind="native",stage="discovery",status="draft",
       hypothesis="Pressing and defensive-line changes interact on xGD within the frozen own IP-4231.",
       control="Standard trigger press, standard defensive line",intervention="2x2: trigger press standard/more often and defensive line standard/higher",
       conditions="Synthetic equal strength, controlled profiles, own IP4231/OOP4411, fixed native benchmark management, no injected live changes; two opponent styles, both sides.",
       seed_namespace=MAIN_NAMESPACE,identity=lab.identity,metrics=dict(primary="xgd",secondary=list(SECONDARY)),
       design=dict(unit="seed_block",n_blocks=8,sides=[0,1],arms=[dict(id=arm,setup_sha256=config_hash({sc:{si:by_arm[arm] for si,by_arm in by_side.items()} for sc,by_side in setups.items()}),setup_sha256_type="cell-map") for arm in ARMS],
                   scenarios=[dict(id=sc,opponent=sc,strength="identical_synthetic_profiles",split="discovery") for sc in SCENARIOS],setups=setups),
       science=dict(alpha=.05,power=.9,min_effect=.10,multiple_testing="none",family_size=1,
                    analysis="analysis/analyse_tact001p0.py: paired DID, side mean, two equally weighted contexts; 20000 stratified bootstrap resamples; ten-secondary Holm family.",
                    exclusions="No replacement seeds/outcome exclusions; failed or incomplete blocks block scientific reporting.",
                    negative_controls=["7 identical-input repeats/A-A","invalid binary rejected with 108"],
                    readback_fields=["69 attributes","23 profile fields","roles and duties","both phases","all encoded instructions","effective seed"],
                    stopping_rule="128 main jobs, at most 24 technical attempts, four workers, durable 900-second cumulative supervised wall-time cap, no retries.",
                    selection_rule="No winner selection, no optimization and no holdout simulation.",
                    power_basis="Variance pilot; .9 is target for subsequent planning, not achieved pilot power. Effects .10/.15/.20 xGD DID; one-sided SD upper bounds under normality."),
       budget=dict(max_matches=128,max_workers=4,timeout_seconds=90,max_technical_attempts=24,total_native_wall_seconds=900),
       execution=dict(code_sha256=code,public_inputs_sha256=source_hash(PUBLIC/"inputs.json"),seed_plan_sha256=source_hash(PUBLIC/"seed-plan.json")),
       preregistration=dict(commit=None,document="experiments/TACT-001-P0-preregistration.md",document_sha256=None,analysis="analysis/analyse_tact001p0.py",analysis_sha256=None))
    validate(contract)
    write(SPEC,contract)
    print("Prepared 16 frozen input cells, two held-out profiles and 19 disjoint seeds",flush=True)


def verify_code(config):
    require(all(source_hash(ROOT/name)==value for name,value in config["execution"]["code_sha256"].items()),"Frozen execution/analysis code changed")
    require(source_hash(PUBLIC/"inputs.json")==config["execution"]["public_inputs_sha256"] and
            source_hash(PUBLIC/"seed-plan.json")==config["execution"]["seed_plan_sha256"],"Frozen input descriptor/seed reservation changed")


def register(commit):
    config=read(SPEC)
    config["status"]="registered"
    prereg=config["preregistration"]
    prereg["commit"]=commit
    for field in ("document","analysis"):
        blob=subprocess.check_output(["git","show",f"{commit}:{prereg[field]}"],cwd=ROOT)
        prereg[field+"_sha256"]=sha256(blob).hexdigest()
    validate(config,executable=True)
    published_registration(config,SPEC)
    verify_code(config)
    plan=read(LOCAL/"seed-plan.json")
    # Own already-published reservation is excluded from the collision audit only here.
    used=set()
    for path in (ROOT/"data").iterdir():
        if path.is_dir() and path!=PUBLIC:
            used.update(historical_seeds(path))
    for path in REGISTRY.glob("*.json"):
        if not path.name.startswith(EXPERIMENT):
            used.update(read(path)["seeds"])
    require(not set(plan["seeds"])&used,"Reserved seeds now collide")
    receipt=dict(config=config,config_sha256=config_hash(config),seeds=plan["main_seeds"])
    require(len(schedule(receipt))==128,"Invalid pilot schedule")
    for path in (LOCAL/"receipt.json",REGISTRY/(EXPERIMENT+".json")):
        require(not path.exists(),"Pilot already registered")
        with path.open("x",encoding="utf8") as stream:
            json.dump(receipt,stream,allow_nan=False,indent=2)
    write(PUBLIC/"manifest.json",receipt)
    print("Registered published pilot",commit,flush=True)


def technical_jobs():
    plan=read(LOCAL/"seed-plan.json")
    jobs=[]
    for sc,side,arm in product(SCENARIOS,(0,1),ARMS):
        jobs.append(dict(key=f"tech-{sc}-{side}-{arm}-r0",scenario=sc,side=side,arm=arm,
                         seed=plan["technical_seeds"][SCENARIOS.index(sc)],repeat=0))
    for sc,side,arms in (("high_press",0,ARMS),("deep_block",1,ARMS[:3])):
        for arm in arms:
            jobs.append(dict(key=f"tech-{sc}-{side}-{arm}-r1",scenario=sc,side=side,arm=arm,
                             seed=plan["technical_seeds"][SCENARIOS.index(sc)],repeat=1))
    return sorted(jobs,key=lambda j:sha256(j["key"].encode()).digest())


def audit_contract(row,job,task,log):
    evidence=rows(log)
    profiles=event(evidence,"native_profile_bindings_verified")
    require(profiles["fields"]==46*23,"Native profile field coverage differs")
    dump=read(task["dump"])
    # Full native player profiles are already verified record by record by the host.
    # Additionally compare all creator instruction bits with named catalog options.
    config=job["config"]
    for side,team in enumerate(config["teams"]):
        raw=bytes.fromhex(dump["teams"][side]["creator_hex"])
        flags=int.from_bytes(raw[:16],"little")
        for group,choice in team["instructions"].items():
            options=LAB_SERVER.GROUPS[int(group)]["options"]
            selected=next(o["native_bit"] for o in options if o["id"]==choice)
            active={o["native_bit"] for o in options if o["native_bit"] and flags>>o["native_bit"]&1}
            require(active==({selected} if selected else set()),"Native team instruction differs")
    return dict(input_contract_verified=True,profile_fields_verified=profiles["fields"])


def attach(jobs,receipt=None):
    configs=read(LOCAL/"configs.json")
    for job in jobs:
        label=f"{job['scenario']}-{job['side']}-{job['arm']}"
        job.update(config=configs[label],binary=LOCAL/"inputs"/(label+".bin"))
    return jobs


def collect(kind,receipt):
    observed=[]
    main_jobs={j["key"]:j for j in schedule(receipt)}
    tech_jobs={j["key"]:j for j in technical_jobs()}
    expected=main_jobs if kind=="main" else tech_jobs
    for path in sorted((LOCAL/kind).glob("part-*/ledger.jsonl")):
        for row in rows(path):
            job=expected[row["key"]]
            row.update(scenario=job["scenario"],config_sha256=receipt["config_sha256"])
            observed.append(row)
    return observed


def execute(lab,kind):
    global LAB_SERVER
    LAB_SERVER=lab.server
    receipt=read(LOCAL/"receipt.json")
    published_registration(receipt["config"],SPEC)
    verify_code(receipt["config"])
    check_identity(receipt["config"]["identity"],lab.identity,read(ROOT/"data/valid-002/validation-summary.json"))
    if kind=="main":
        require(read(LOCAL/"technical-summary.json")["passed"],"Technical gate not passed")
        jobs=schedule(receipt)
    else:
        jobs=technical_jobs()
    jobs=attach(jobs)
    for i in range(0,len(jobs),16):
        lab.run(jobs[i:i+16],LOCAL/kind/f"part-{i//16:02d}",workers=4,bounded_validation=True,audit=audit_contract)
    observed=collect(kind,receipt)
    if kind=="technical":
        grouped={}
        for row in observed:
            grouped.setdefault((row["scenario"],row["tested_side"],row["arm"]),[]).append(row)
        compared=[]
        for key,pair in grouped.items():
            if len(pair)==2:
                exact=all(pair[0][field]==pair[1][field] for field in ("setup_sha256","score","finish_tick","team_statistics"))
                require(exact,"Technical A/A repeat mismatch")
                compared.append(dict(scenario=key[0],side=key[1],arm=key[2],exact=True))
        require(len(compared)==7 and len(observed)==23,"Technical coverage incomplete")
        invalid=LOCAL/"invalid.bin"
        invalid.write_bytes(b"TACT-001-P0 INTENTIONALLY INVALID")
        log=LOCAL/"negative.jsonl"
        result=subprocess.run([str(lab.server.native_host()),"--scenario-file",str(invalid),"--output",str(log)],
                              cwd=lab.root,capture_output=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
        require(result.returncode==108 and not any(r.get("event")=="natural_match_finished" for r in rows(log)),"Negative binary accepted")
        write(LOCAL/"technical-summary.json",dict(passed=True,matches=23,repeats=compared,
              negative=dict(returncode=108,raw_log_sha256=digest(log)),native_identity=lab.identity))
    else:
        require(len(observed)==128,"Main ledger incomplete")
    print(kind,"complete",len(observed),flush=True)


def child(args):
    lab=NativeLab(args.runtime,args.game,LOCAL)
    if args.phase=="prepare":
        prepare(lab)
    else:
        execute(lab,args.phase)


def main():
    p=ArgumentParser(description=__doc__)
    p.add_argument("phase",choices=("prepare","register","technical","main","status"))
    p.add_argument("--runtime",type=Path,default=ROOT/"local/runtime-v1114.6")
    p.add_argument("--game",type=Path,default=Path("D:/steam/steamapps/common/Football Manager 27"))
    p.add_argument("--commit")
    p.add_argument("--child",action="store_true",help="Internal supervised operation")
    args=p.parse_args()
    if args.child:
        # A child must be tied to a live durable supervisor reservation.
        state=read(LOCAL/"budget.json")
        require(state["active"] and state["active"]["name"].startswith(args.phase) and
                supervisor_alive(state["active"]["supervisor_pid"]) and
                state["active"]["token_sha256"]==sha256(os.environ.get("TACT_P0_SUPERVISOR_TOKEN","").encode()).hexdigest(),
                "No live authenticated supervisor reservation")
        write(LOCAL/(args.phase+"-native-entry.json"),dict(supervised=True))
        child(args)
        return
    if args.phase=="status":
        print(json.dumps(read(LOCAL/"budget.json"),indent=2))
        return
    if args.phase=="register":
        require(args.commit,"Published preregistration commit required")
        register(args.commit)
        return
    budget=NativeBudget(LOCAL/"budget.json")
    if args.phase=="prepare":
        keys=[];kind="technical"
    elif args.phase=="technical":
        keys=[j["key"] for j in technical_jobs()]+["negative-binary"];kind="technical"
    else:
        require(read(LOCAL/"technical-summary.json")["passed"],"Technical gate missing")
        keys=[j["key"] for j in schedule(read(LOCAL/"receipt.json"))];kind="main"
    command=[sys.executable,str(Path(__file__).resolve()),args.phase,"--child","--runtime",str(args.runtime.resolve()),"--game",str(args.game.resolve())]
    operation=args.phase
    if args.phase=="prepare" and budget.load().get("pre_native_auth_repair"):
        operation="prepare-after-auth-fix"
    budget.run(operation,kind,keys,command,ROOT,LOCAL/(operation+".stdout"))
    print((LOCAL/(operation+".stdout")).read_text(encoding="utf8",errors="replace")[-6000:])
    print("Charged supervised native wall time",round(budget.load()["charged_seconds"],3),"/ 900 seconds")


if __name__=="__main__":
    main()

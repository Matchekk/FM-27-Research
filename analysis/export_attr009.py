"""Recheck private evidence, export only allowed fields and complete job accounting."""
from collections import Counter
from datetime import datetime,timedelta
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read,rows,write,require,digest
from run_attr009 import LOCAL,PUBLIC,collect,technical_jobs,ordered_main,verify_code
from analyse_attr009 import analyse
from research.attr009 import ARMS, CONTEXTS
from itertools import product

FIELDS=("build","engine_sha256","adapter_host_sha256","adapter_version","lab_version","lab_commit",
        "fixture_sha256","resource_fingerprint","key","seed","arm","tested_side","setup_sha256",
        "config_sha256","scenario","status","engine_readback","score","finish_tick","team_statistics",
        "raw_log_sha256","input_dump_sha256","startup_receipt_sha256","native_elapsed_seconds",
        "worker_job_index","events_verified","input_contract_verified","profile_fields_verified","error_type",
        "native_raw_dose_verified","design_matrix_sha256","native_roles_verified","native_pi_cells_verified","native_pi_groups_verified")


def export_kind(kind,receipt):
    data=collect(kind,receipt);public=[]
    require(len({r["key"] for r in data})==len(data),"Duplicate ledger entries")
    for row in data:
        if row["status"]=="ok":
            logs=list((LOCAL/kind).glob("part-*/"+row["key"]+".jsonl"));require(len(logs)==1,"Ambiguous/missing raw log")
            log=logs[0]
            require(digest(log)==row["raw_log_sha256"] and digest(log.with_suffix(".input.json"))==row["input_dump_sha256"],"Private raw/input evidence changed")
            require(any(digest(p)==row["startup_receipt_sha256"] for p in log.parent.rglob("startup_receipt.json")),"Startup proof changed")
        public.append({k:row[k] for k in FIELDS if k in row})
    (PUBLIC/(kind+".jsonl")).write_text("".join(json.dumps(r,allow_nan=False)+"\n" for r in public),encoding="utf8")
    return public


def export():
    if not (LOCAL/"receipt.json").exists():
        # Preparation may stop before any seed plan or registration exists.
        # Publish technical accounting without manufacturing a main schedule.
        budget=read(LOCAL/"budget.json")
        require(budget["active"] is None,"Unreconciled active preparation retained")
        require(not budget['reserved'] and all(o['name']=='prepare' for o in budget['operations']),
                'Missing receipt with retained match reservations: reconcile original evidence')
        require(not any((LOCAL/name).exists() for name in ('technical','main','negative-attempt.json','negative.jsonl')),
                'Native match evidence without registration: retain and reconcile')
        plan=read(LOCAL/'seed-plan.json') if (LOCAL/'seed-plan.json').exists() else None
        if plan:
            require(len(plan['main_seeds'])==32 and len(plan['technical_seeds'])==2,
                    'Incomplete retained seed plan')
            seeds=plan['main_seeds']+plan['technical_seeds']
            require(len(set(seeds))==34 and all(type(s) is int and 0<s<=0xffffffff for s in seeds),
                    'Invalid retained seed plan')
        accounting=[]
        for h,s,a in product(CONTEXTS,(0,1),ARMS):
            for repeat in range(2 if a in ('OJ','SJ') else 1):
                accounting.append(dict(key=f'tech-{h}-{s}-{a}-r{repeat}',kind='technical',
                    seed=plan['technical_seeds'][CONTEXTS.index(h)] if plan else None,
                    scenario=h,side=s,design_id=a,status='not_started',registered=False,
                    reserved=False,native_log_present=False))
        accounting.append(dict(key='negative-binary',kind='technical',seed=None,status='not_started',
                               registered=False,reserved=False,native_log_present=False))
        for h,i,s,a in product(CONTEXTS,range(16),(0,1),ARMS):
            seed=plan['main_seeds'][CONTEXTS.index(h)*16+i] if plan else None
            key=f'{h}-{seed}-{s}-{a}' if plan else f'planned-{h}-block{i:02d}-{s}-{a}'
            accounting.append(dict(key=key,kind='main',seed=seed,scenario=h,block_slot=i,
                side=s,design_id=a,status='not_started',registered=False,reserved=False,native_log_present=False))
        PUBLIC.mkdir(parents=True,exist_ok=True)
        (PUBLIC/'job-accounting.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in accounting),encoding='utf8')
        fields=("name","kind","keys","start_utc","child_deadline_utc","elapsed_seconds","returncode","timed_out")
        operations=[{k:o[k] for k in fields if k in o} for o in budget["operations"]]
        public={k:budget[k] for k in ("experiment","limits","limit_seconds","charged_seconds","reserved","halted","wall_start_utc","wall_deadline_utc","wall_limit_seconds")}
        public.update(active=None,operations=operations,charge_scope="all supervised preparation walltime; no reset/retry")
        write(PUBLIC/"budget.json",public)
        write(PUBLIC/"run-summary.json",dict(experiment_id="ATTR-009-Bridge",scientific_series_complete=False,
            technical_gate_passed=False,registration_completed=False,counts=dict(technical={"not_started":33},main={"not_started":384}),
            charged_native_wall_seconds=budget["charged_seconds"],limit_seconds=600,excluded_matches=0,retries=0,holdout_matches=0))
        write(PUBLIC/"preparation-status.json",dict(status="blocked_before_registration",operations=operations,
            seed_reservation_present=(LOCAL/"seed-plan.json").exists(),native_full_matches_claimed=0,
            scientific_effects_published=False))
        return
    receipt=read(LOCAL/"receipt.json");verify_code(receipt["config"])
    budget=read(LOCAL/"budget.json");require(budget["active"] is None,"Unreconciled active operation: retain private state")
    tech=export_kind("technical",receipt);main=export_kind("main",receipt)
    control=read(LOCAL/"technical-summary.json") if (LOCAL/"technical-summary.json").exists() else dict(passed=False)
    write(PUBLIC/"technical-summary.json",control)
    operations=[{k:o[k] for k in ("name","kind","keys","start_utc","child_deadline_utc","elapsed_seconds","returncode","timed_out")} for o in budget["operations"]]
    public_budget={k:budget[k] for k in ("experiment","limits","limit_seconds","charged_seconds","reserved","halted","wall_start_utc","wall_deadline_utc","wall_limit_seconds")}
    end=max(datetime.fromisoformat(o["start_utc"])+timedelta(seconds=o["elapsed_seconds"]) for o in operations)
    elapsed=(end-datetime.fromisoformat(budget["wall_start_utc"])).total_seconds()
    within=end<=datetime.fromisoformat(budget["wall_deadline_utc"])
    public_budget.update(operations=operations,coordination_leases=[dict(phase=o["name"],**read(LOCAL/(o["name"]+".lease.json"))) for o in operations],active=None,elapsed_study_window_seconds=elapsed,within_fixed_deadline=within,
                         charge_scope="entire supervised child wall time incl. prep/audits; immutable study-wide UTC deadline also includes time between phases")
    write(PUBLIC/"budget.json",public_budget)
    actual={r["key"]:r for r in [*tech,*main]};accounting=[]
    for kind,jobs in (("technical",technical_jobs()),("main",ordered_main(receipt))):
        for j in jobs:
            key=j["key"];logs=list((LOCAL/kind).glob("part-*/"+key+".jsonl"))
            status=actual[key]["status"] if key in actual else "started_unresolved" if logs else "not_started"
            accounting.append(dict(key=key,kind=kind,seed=j["seed"],scenario=j["scenario"],side=j["side"],design_id=j["arm"],
                status=status,reserved=key in budget["reserved"],native_log_present=bool(logs)))
    negative=read(LOCAL/"negative-attempt.json") if (LOCAL/"negative-attempt.json").exists() else control.get("negative")
    if negative and negative.get("raw_log_sha256"):require(digest(LOCAL/"negative.jsonl")==negative["raw_log_sha256"],"Negative proof changed")
    write(PUBLIC/"negative-control.json",negative or dict(status="not_started"))
    accounting.append(dict(key="negative-binary",kind="technical",seed=None,status=negative["status"] if negative and negative.get("status") in ("failed","expected_rejection") else
        "started_unresolved" if (LOCAL/"negative.jsonl").exists() else "not_started",reserved="negative-binary" in budget["reserved"],native_log_present=(LOCAL/"negative.jsonl").exists()))
    (PUBLIC/"job-accounting.jsonl").write_text("".join(json.dumps(r)+"\n" for r in accounting),encoding="utf8")
    counts={kind:dict(Counter(r["status"] for r in accounting if r["kind"]==kind)) for kind in ("technical","main")}
    complete=len(main)==384 and all(r["status"]=="ok" for r in main) and control["passed"] and not budget["halted"] and within
    if complete:
        results,blocks=analyse(main,receipt)
        write(PUBLIC/"effects.json",results)
        (PUBLIC/"block-contrasts.jsonl").write_text("".join(json.dumps(r)+"\n" for r in blocks),encoding="utf8")
    summary=dict(experiment_id="ATTR-009-Bridge",scientific_series_complete=complete,technical_gate_passed=control["passed"],counts=counts,
        charged_native_wall_seconds=budget["charged_seconds"],limit_seconds=600,elapsed_study_window_seconds=elapsed,
        fixed_utc_deadline=budget["wall_deadline_utc"],within_fixed_deadline=within,independent_main_seed_blocks=32 if complete else None,
        excluded_matches=0,retries=0,holdout_matches=0,winner_confirmed=False,preregistration_commit=receipt["config"]["preregistration"]["commit"])
    write(PUBLIC/"run-summary.json",summary);print(json.dumps(summary))


if __name__=="__main__":export()

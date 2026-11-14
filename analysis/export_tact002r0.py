"""Recheck private evidence, export only allowed fields and complete job accounting."""
from collections import Counter
from datetime import datetime,timedelta
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read,rows,write,require,digest
from run_tact002r0 import LOCAL,PUBLIC,collect,technical_jobs,ordered_main,verify_code
from analyse_tact002r0 import analyse

FIELDS=("build","engine_sha256","adapter_host_sha256","adapter_version","lab_version","lab_commit",
        "fixture_sha256","resource_fingerprint","key","seed","arm","tested_side","setup_sha256",
        "config_sha256","scenario","status","engine_readback","score","finish_tick","team_statistics",
        "raw_log_sha256","input_dump_sha256","startup_receipt_sha256","native_elapsed_seconds",
        "worker_job_index","events_verified","input_contract_verified","profile_fields_verified","error_type",
        "factor_levels","native_role_flags","design_matrix_sha256","native_roles_verified","native_pi_cells_verified","native_pi_groups_verified")


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
    complete=len(main)==512 and all(r["status"]=="ok" for r in main) and control["passed"] and not budget["halted"] and within
    if complete:
        results,blocks=analyse(main,receipt)
        write(PUBLIC/"effects.json",results)
        (PUBLIC/"block-contrasts.jsonl").write_text("".join(json.dumps(r)+"\n" for r in blocks),encoding="utf8")
    summary=dict(experiment_id="TACT-002-R0",scientific_series_complete=complete,technical_gate_passed=control["passed"],counts=counts,
        charged_native_wall_seconds=budget["charged_seconds"],limit_seconds=900,elapsed_study_window_seconds=elapsed,
        fixed_utc_deadline=budget["wall_deadline_utc"],within_fixed_deadline=within,independent_main_seed_blocks=64 if complete else None,
        excluded_matches=0,retries=0,holdout_matches=0,winner_confirmed=False,preregistration_commit=receipt["config"]["preregistration"]["commit"])
    write(PUBLIC/"run-summary.json",summary);print(json.dumps(summary))


if __name__=="__main__":export()

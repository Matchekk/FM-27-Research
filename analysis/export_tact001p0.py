"""Verify local pilot evidence and publish only enumerated numeric fields."""
from collections import Counter
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.core import schedule
from research.native import digest, read, require, rows, write
from analyse_tact001p0 import analyse, ARMS, SCENARIOS
from run_tact001p0 import LOCAL, PUBLIC, collect, technical_jobs, verify_code

FIELDS=("build","engine_sha256","adapter_host_sha256","adapter_version","lab_version","lab_commit",
        "fixture_sha256","resource_fingerprint","key","seed","arm","tested_side","setup_sha256",
        "config_sha256","scenario","status","engine_readback","score","finish_tick","team_statistics",
        "raw_log_sha256","input_dump_sha256","startup_receipt_sha256","native_elapsed_seconds",
        "worker_job_index","events_verified","input_contract_verified","profile_fields_verified","error_type")


def export_kind(kind,receipt):
    data=collect(kind,receipt)
    require(len({r["key"] for r in data})==len(data),"Duplicate attempt ledger")
    public=[]
    for row in data:
        if row["status"]=="ok":
            paths=list((LOCAL/kind).glob("part-*/"+row["key"]+".jsonl"))
            require(len(paths)==1,"Missing/ambiguous native log")
            path=paths[0]
            require(digest(path)==row["raw_log_sha256"] and
                    digest(path.with_suffix(".input.json"))==row["input_dump_sha256"],"Raw input/result proof changed")
            require(any(digest(p)==row["startup_receipt_sha256"] for p in path.parent.rglob("startup_receipt.json")),"Startup proof changed")
        public.append({k:row[k] for k in FIELDS if k in row})
    (PUBLIC/(kind+".jsonl")).write_text("".join(json.dumps(r,allow_nan=False)+"\n" for r in public),encoding="utf8")
    return public


def export():
    receipt=read(LOCAL/"receipt.json")
    verify_code(receipt["config"])
    budget=read(LOCAL/"budget.json")
    require(budget["active"] is None,"Do not publish an unsettled native operation")
    tech=export_kind("technical",receipt)
    main=export_kind("main",receipt)
    control=read(LOCAL/"technical-summary.json") if (LOCAL/"technical-summary.json").exists() else dict(passed=False)
    write(PUBLIC/"technical-summary.json",control)
    operations=[{k:o[k] for k in ("name","kind","keys","start_utc","child_deadline_utc","elapsed_seconds","returncode","timed_out")} for o in budget["operations"]]
    public_budget={k:budget[k] for k in ("experiment","limits","limit_seconds","charged_seconds","reserved","halted")}
    public_budget.update(operations=operations,active=None,pre_native_auth_repair=budget.get("pre_native_auth_repair"),
                         charge_scope="entire supervised child wall time, including preflight/Python audits; never reset or refunded")
    write(PUBLIC/"budget.json",public_budget)
    actual={r["key"]:r for r in [*tech,*main]}
    accounting=[]
    for kind,jobs in (("technical",technical_jobs()),("main",schedule(receipt))):
        for job in jobs:
            key=job["key"]
            logs=list((LOCAL/kind).glob("part-*/"+key+".jsonl"))
            status=actual[key]["status"] if key in actual else "started_unresolved" if logs else "not_started"
            accounting.append(dict(key=key,kind=kind,seed=job["seed"],status=status,reserved=key in budget["reserved"],
                                   native_log_present=bool(logs)))
    negative=control.get("negative")
    if negative:
        require(digest(LOCAL/"negative.jsonl")==negative["raw_log_sha256"],"Negative proof changed")
    accounting.append(dict(key="negative-binary",kind="technical",seed=None,
                           status="expected_rejection" if negative else "not_started",reserved="negative-binary" in budget["reserved"],
                           native_log_present=(LOCAL/"negative.jsonl").exists()))
    (PUBLIC/"job-accounting.jsonl").write_text("".join(json.dumps(r)+"\n" for r in accounting),encoding="utf8")
    counts={kind:dict(Counter(r["status"] for r in accounting if r["kind"]==kind)) for kind in ("technical","main")}
    complete=len(main)==128 and all(r["status"]=="ok" for r in main) and control["passed"] and not budget["halted"]
    summary=dict(experiment_id="TACT-001-P0",scientific_series_complete=complete,technical_gate_passed=control["passed"],
                 counts=counts,charged_native_wall_seconds=budget["charged_seconds"],limit_seconds=900,
                 independent_main_seed_blocks=16 if complete else None,excluded_matches=0,retries=0,
                 holdout_matches=0,winner_selected=False,preregistration_commit=receipt["config"]["preregistration"]["commit"])
    write(PUBLIC/"run-summary.json",summary)
    if complete:
        results=analyse(main,receipt)
        write(PUBLIC/"effects.json",results)
    print(json.dumps(summary))


if __name__=="__main__":
    export()

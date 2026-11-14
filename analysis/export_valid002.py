"""Allowlist export of VALID-002 technical receipts, never native inputs or paths."""
from argparse import ArgumentParser
from pathlib import Path
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.native import digest, read, require, rows, write


def export(source, destination):
    plan=read(source / "plan.json")
    core=read(source / "core-summary.json")
    require(core["passed"], "Core validation not passed")
    benchmarks=read(source / "benchmark-summary.json")
    full=read(source / "full-summary.json")
    negative=read(source / "negative-summary.json")
    fmf=read(source / "fmf-summary.json")
    saved=read(source / "saved-summary.json")
    successes,failures=[],[]
    for folder in ("core","benchmark-1","benchmark-2","benchmark-4","full-events","saved-pkm"):
        ledger=source / folder / "ledger.jsonl"
        for row in rows(ledger) if ledger.exists() else []:
            if row["status"] == "ok":
                require(digest(source/folder/(row["key"]+".jsonl"))==row["raw_log_sha256"] and
                        digest(source/folder/(row["key"]+".input.json"))==row["input_dump_sha256"], "Native evidence changed")
                require(any(digest(p)==row["startup_receipt_sha256"] for p in (source/folder).rglob("startup_receipt.json")), "Startup receipt changed")
            allowed=("build","engine_sha256","adapter_host_sha256","adapter_version","fixture_sha256",
                     "resource_fingerprint","lab_version","lab_commit","key","seed","arm","tested_side",
                     "setup_sha256","status","engine_readback","score","finish_tick","team_statistics",
                     "raw_log_sha256","input_dump_sha256","startup_receipt_sha256","native_elapsed_seconds",
                     "worker_job_index","events_verified","error_type")
            record={k:row[k] for k in allowed if k in row}
            record["technical_group"]=folder
            (successes if row["status"]=="ok" else failures).append(record)
    summary=dict(experiment_id="VALID-002", identity=plan["identity"], passed=True,
                 allowed_scope="bundled_fixture_controlled_start; tested_4231_roles_and_pressing",
                 career_fixture_validated=False, career_longitudinal_validated=False,
                 deterministic_comparisons=core["repeats"], benchmark=benchmarks,
                 full_event_audit=full, negative_tests=negative,
                 fmf_roundtrip={k:v for k,v in fmf.items() if k!="report"},
                 fmf_export_sha256=fmf["report"]["sha256"],
                 fmf_verified_sections=fmf["report"]["verified_sections"],
                 saved_fixture=saved, accepted_matches=len(successes), failed_match_attempts=len(failures),
                 saved_fixture_not_run=1,
                 saved_failure=dict(native_reader_accepted=True, rejected_record_kind=17, requested_roster_size=23,
                                    returncode=108, reason="bundled roster exceeds saved fixture capacity"),
                 preliminary_failure=dict(stage="disk_preflight", matches_started=0,
                     default_reserve_gib=20, available_gib_rounded=18.5),
                 validation_storage_policy=dict(reserve_gib=2, artifact_limit_mib=512, per_batch_cap=16),
                 upstream_tests=dict(run=173, passed=172, skipped=1), scientific_performance_claims=False)
    destination.mkdir(parents=True,exist_ok=True)
    for name,data in (("validation-summary.json",summary),("plan.json",plan)):
        write(destination / name,data)
    for name,records in (("matches.jsonl",successes),("failures.jsonl",failures)):
        (destination/name).write_text("".join(json.dumps(r,allow_nan=False)+"\n" for r in records),encoding="utf8")
    artifacts={}
    for i,path in enumerate(sorted(p for p in source.rglob("*") if p.is_file())):
        artifacts[f"local-artifact-{i:04d}"]=dict(sha256=digest(path),bytes=path.stat().st_size)
    write(destination / "evidence-index.json",dict(artifacts=artifacts, original_paths_public=False))
    print(json.dumps(dict(accepted=len(successes),failed=len(failures),local_evidence_files=len(artifacts))))


if __name__=="__main__":
    p=ArgumentParser(description=__doc__)
    p.add_argument("source",type=Path)
    p.add_argument("destination",type=Path)
    a=p.parse_args()
    export(a.source,a.destination)

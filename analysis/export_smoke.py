"""Export the verified technical platform smoke using public fields only."""
from argparse import ArgumentParser
from pathlib import Path
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.core import config_hash, schedule
from research.native import digest, read, require, write
from research.report import experiment_report


def export(source,destination):
    receipt=read(source/"receipt.json")
    result=read(source/"results.json")
    summary=read(source/"summary.json")
    require(summary["passed"] and summary["technical_only"] and summary["matches"]==len(result)==4, "Invalid smoke")
    require(receipt["config_sha256"]==config_hash(receipt["config"]), "Registration changed")
    jobs=schedule(receipt)
    for row in result:
        require(digest(source/"matches"/(row["key"]+".jsonl"))==row["raw_log_sha256"] and
                digest(source/"matches"/(row["key"]+".input.json"))==row["input_dump_sha256"], "Smoke evidence changed")
        require(any(digest(p)==row["startup_receipt_sha256"] for p in (source/"matches").rglob("startup_receipt.json")), "Smoke startup receipt changed")
    fields=("build","engine_sha256","adapter_host_sha256","adapter_version","lab_version","lab_commit",
            "fixture_sha256","resource_fingerprint","key","seed","arm","tested_side","setup_sha256",
            "config_sha256","scenario","status","engine_readback","score","finish_tick","team_statistics",
            "raw_log_sha256","input_dump_sha256","startup_receipt_sha256","native_elapsed_seconds",
            "worker_job_index","events_verified")
    public=[{k:r[k] for k in fields} for r in result]
    destination.mkdir(parents=True,exist_ok=True)
    write(destination/"manifest.json",receipt)
    write(destination/"summary.json",summary)
    (destination/"matches.jsonl").write_text("".join(json.dumps(r,allow_nan=False)+"\n" for r in public),encoding="utf8")
    experiment_report(receipt,jobs,public,destination/"report.md")
    print(json.dumps(dict(accepted=4,seed_blocks=2,aa_exact=summary["all_aa_exact"])))


if __name__=="__main__":
    p=ArgumentParser(description=__doc__)
    p.add_argument("source",type=Path)
    p.add_argument("destination",type=Path)
    args=p.parse_args()
    export(args.source,args.destination)

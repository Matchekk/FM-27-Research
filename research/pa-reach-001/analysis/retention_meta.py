"""Measure April-to-June CA and pinned app Meta changes on the retention branch."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sqlite3

from observed_meta import read_scan, score_pairs


RETENTION_CHECKPOINTS = {
    "2027-04-30": "d2b2feabde2c324993d3584ae0b6f51649fa81b9a40ef36c598d110147a591b9",
    "2027-06-30": "040140911df6862dcc21bd20e0ba5b1acfeb616af7a66052bebbcd4ac1932088",
}
INTAKE_SHA256 = "1dcc8637e4d8047872e16607df854393702d3fa3c9396522c7186ab2048b5973"


def intake_results(start, end, intake, issues, model):
    members = {(row["id"], row["birth"]) for row in intake}
    if len(intake) != 16 or len(members) != 16:
        raise ValueError("Expected 16 distinct, previously bound intake identities")
    lookups = [{k[:2]: k for k in snapshot} for snapshot in (start, end)]
    selected = {}
    excluded = Counter()
    for member in sorted(members):
        first, last = (lookup.get(member) for lookup in lookups)
        if first is None:
            excluded["baseline_" + issues[0].get(member, "missing_identity")] += 1
        elif start[first][1] == "GK":
            excluded["baseline_goalkeeper"] += 1
        elif last is None:
            excluded["followup_" + issues[1].get(member, "missing_identity")] += 1
        elif end[last][1] == "GK":
            excluded["followup_goalkeeper"] += 1
        elif first != last:
            excluded["different_name_check"] += 1
        else:
            selected[first] = start[first]
    output = score_pairs(selected, end, model, extended=True)
    output["meta_delta"].pop("byPosition")
    return {"baseline_n": len(members), "excluded_before_scoring": dict(excluded), **output}


def load_snapshot(day, inputs, expected_hash):
    panel, tag, scan, before, after = inputs
    absent = {}
    with sqlite3.connect(Path(panel).resolve().as_uri()+"?mode=ro", uri=True) as conn:
        snapshot, audit = read_scan(conn, day, *map(Path, (scan, before, after)), tag=tag, exclusions=absent)
    if audit["hashes"]["loaded_copy"] != expected_hash:
        raise ValueError(f"Expected the frozen retention checkpoint for {day}")
    return snapshot, audit, absent


def load_intake(path):
    intake_raw = path.read_bytes()
    intake_digest = hashlib.sha256(intake_raw).hexdigest()
    if intake_digest != INTAKE_SHA256:
        raise ValueError("Expected the frozen youth intake identity list")
    return json.loads(intake_raw), intake_digest


def compare(args):
    april, june = RETENTION_CHECKPOINTS
    start, first_audit, first_issues = load_snapshot(april, args.april, RETENTION_CHECKPOINTS[april])
    end, last_audit, last_issues = load_snapshot(june, args.june, RETENTION_CHECKPOINTS[june])
    intake, intake_digest = load_intake(args.intake)
    global_end = {k: v for k, v in end.items() if v[1] and v[1] != "GK"}
    return {"schema": "pa-reach-retention-meta/v1", "independent_career_roots": 1,
            "calendar_days": 61, "snapshots": {april: first_audit, june: last_audit},
            "intake_identity_manifest_sha256": intake_digest,
            "intake": intake_results(start, end, intake, (first_issues, last_issues), args.model),
            "global_outfield_under_28": score_pairs(start, global_end, args.model, extended=True)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("intake", type=Path)
    for name in ("april", "june"):
        parser.add_argument("--"+name, nargs=5, required=True,
                            metavar=("PANEL", "TAG", "SCAN", "BEFORE", "AFTER"))
    print(json.dumps(compare(parser.parse_args()), indent=2))

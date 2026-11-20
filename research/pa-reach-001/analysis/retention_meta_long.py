"""Compare verified long-term RET snapshots with the frozen March and April Meta baselines."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

from observed_meta import score_pairs
from retention_meta import RETENTION_CHECKPOINTS, intake_results, load_intake, load_snapshot


MARCH, APRIL = "2027-03-30", "2027-04-30"
ROOT_HASH = "631a2c000d854fd46d98f0efcce55a5b179367167e8d57b99ad2d7844e4329e4"
TARGET_DAYS = ("2027-12-30", "2028-03-30", "2029-03-30")


def global_results(start, end, excluded, model):
    outfield_end = {k: v for k, v in end.items() if v[1] and v[1] != "GK"}
    identity_end = {k[:2]: k for k in end}
    counts = Counter()
    for key, (age, pos, _, _) in start.items():
        if age >= 28 or not pos or pos == "GK" or key in outfield_end:
            continue
        identity = key[:2]
        if key in end:
            counts["followup_goalkeeper_or_no_position"] += 1
        elif identity in identity_end:
            counts["different_name_check"] += 1
        else:
            counts[excluded.get(identity, "no_structural_followup_identity")] += 1
    result = score_pairs(start, outfield_end, model, extended=True)
    if sum(counts.values()) != result["missing_followup_identity_or_attributes"]:
        raise ValueError("Follow-up exclusions do not account for all lost pairs")
    return {"followup_exclusions": counts, **result}


def compare(args):
    target = args.through
    if not args.followup[1].startswith("ZD-RET-") or args.march[1] != "ZD-ROOT-01":
        raise ValueError("Expected March origin and retention follow-up tags")
    march, march_audit, _ = load_snapshot(MARCH, args.march, ROOT_HASH)
    april, april_audit, april_issues = load_snapshot(APRIL, args.april, RETENTION_CHECKPOINTS[APRIL])
    end, end_audit, end_issues = load_snapshot(target, args.followup, args.save_sha256)
    intake, intake_digest = load_intake(args.intake)
    day = date.fromisoformat(target)
    return {"schema": "pa-reach-retention-meta-long/v1", "independent_career_roots": 1,
            "snapshots": {MARCH: march_audit, APRIL: april_audit, target: end_audit},
            "intake_identity_manifest_sha256": intake_digest,
            "global_calendar_days": (day - date.fromisoformat(MARCH)).days,
            "intake_calendar_days": (day - date.fromisoformat(APRIL)).days,
            "global_outfield_under_28": global_results(march, end, end_issues, args.model),
            "intake": intake_results(april, end, intake, (april_issues, end_issues), args.model)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path)
    parser.add_argument("intake", type=Path)
    parser.add_argument("through", choices=TARGET_DAYS)
    parser.add_argument("--save-sha256", required=True)
    for name in ("march", "april", "followup"):
        parser.add_argument("--"+name, nargs=5, required=True,
                            metavar=("PANEL", "TAG", "SCAN", "BEFORE", "AFTER"))
    print(json.dumps(compare(parser.parse_args()), indent=2))

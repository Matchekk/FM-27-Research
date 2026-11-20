"""Compare identity-confirmed private native/save factor measurements on one branch."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def index_rows(document):
    rows = {}
    for record in document["rows"]:
        key = (record["uid"], record["birth"])
        if key in rows:
            raise ValueError("Duplicate identity")
        rows[key] = record
    return rows


def compare(earlier, later):
    start, end = read(earlier), read(later)
    days = (date.fromisoformat(end["game_date"]) - date.fromisoformat(start["game_date"])).days
    if days <= 0:
        raise ValueError("Expected a strictly later checkpoint")
    first, last = index_rows(start), index_rows(end)
    transitions, ca_diff, pa_diff, score_diff, mismatches = Counter(), Counter(), Counter(), Counter(), Counter()
    for key in first.keys() & last.keys():
        a, b = first[key], last[key]
        if a["native_factor"] != a["saved_factor"] or b["native_factor"] != b["saved_factor"]:
            mismatches[a["saved_factor"], a["native_factor"], b["saved_factor"], b["native_factor"]] += 1
            continue
        transitions[a["native_factor"], b["native_factor"]] += 1
        ca_diff[b["ca"] - a["ca"]] += 1
        pa_diff[b["pa"] - a["pa"]] += 1
        score_diff[b["native_recalculation_score"] - a["native_recalculation_score"]] += 1
    return {
        "schema": "pa-reach-named-factor-followup/v1",
        "baseline": {k: start[k] for k in ("game_date", "save_sha256", "private_receipt_sha256")},
        "followup": {k: end[k] for k in ("game_date", "save_sha256", "private_receipt_sha256")},
        "days": days, "baseline_n": len(first), "followup_n": len(last),
        "paired_uid_dob": len(first.keys() & last.keys()), "paired_save_native_equal_both_dates": transitions.total(),
        "missing_followup": len(first.keys() - last.keys()),
        "unresolved_pair_count": mismatches.total(),
        "unresolved_pairs": [{"baseline_save": a, "baseline_native": b, "final_save": c,
                              "final_native": d, "n": n} for (a,b,c,d),n in sorted(mismatches.items())],
        "changed_native_and_saved_factor": sum(v for (a,b),v in transitions.items() if a!=b),
        "factor_pairs": [{"start": a, "end": b, "n": n} for (a,b),n in sorted(transitions.items())],
        "ca_change_frequency": dict(sorted(ca_diff.items())), "pa_change_frequency": dict(sorted(pa_diff.items())),
        "native_recalculation_score_change_frequency": dict(sorted(score_diff.items())),
        "causal_attribution": "UNRESOLVED", "independent_careers": 1,
    }


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("earlier", type=Path)
    argp.add_argument("later", type=Path)
    print(json.dumps(compare(**vars(argp.parse_args())), indent=2))

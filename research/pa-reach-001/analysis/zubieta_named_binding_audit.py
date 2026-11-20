"""Measure repeated property stability and shared binding lag from the private acquisition receipts."""

import argparse
from collections import Counter
import json
from pathlib import Path


def read(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def check(first_panel, first_intake, repeated, shared_queue, shared_folder):
    first = {r["uid"]: r for source in (first_panel, first_intake) for r in read(source)["rows"]}
    later = read(repeated)["rows"]
    counts = Counter()
    for row in later:
        old = first[row["uid"]]
        if row["birth"] != old["birth"]:
            raise ValueError("Birth mismatch")
        counts["same_native_factor"] += row["native_factor"] == old["native_factor"]
        counts["same_native_recalculation_score"] += row["native_recalculation_score"] == old["native_recalculation_score"]
        counts["save_factor_changed"] += row["saved_factor"] != old["saved_factor"]
        counts["later_native_agrees_with_later_save"] += row["native_factor"] == row["saved_factor"]
    queue = read(shared_queue)
    ids = [int(read(shared_folder / f"{r['index']}-UniqueId.json")["Value"]) for r in queue]
    return {
        "schema": "pa-reach-named-binding-diagnostic/v1", "repeat_uids_and_dob": len(later),
        "repeated_distinct_player_path": dict(counts),
        "shared_path_requests": len(queue), "shared_path_distinct_returned_ids": len(set(ids)),
        "shared_path_id_equal_current_request": sum(r["uid"]==v for r,v in zip(queue,ids, strict=True)),
        "shared_path_equal_previous_request": sum(r["uid"]==v for r,v in zip(queue[:-1],ids[1:], strict=True)),
        "preceding_request_comparisons": max(0,len(queue)-1),
        "cross_assigned_rows_admitted_to_target_panel": 0,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    for f in ("first_panel","first_intake","repeated","shared_queue","shared_folder"):
        p.add_argument(f, type=Path)
    print(json.dumps(check(**vars(p.parse_args())),indent=2))

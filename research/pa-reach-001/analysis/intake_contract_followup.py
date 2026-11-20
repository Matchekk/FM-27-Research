"""Track a submitted youth intake against dated club inventories without emitting identities."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path


def summarize(queue, inventory, expected_hash):
    if inventory["source_sha256"] != expected_hash:
        raise ValueError("Unexpected follow-up source")
    day = date.fromisoformat(inventory["game_date"])
    identities = [(p["id"], p["birth"]) for p in queue]
    if not queue or len(identities) != len(set(identities)):
        raise ValueError("Missing or duplicated intake identities")
    states, starts, ends, kinds = Counter(), Counter(), Counter(), Counter()
    futures = 0
    for member, key in zip(queue, identities, strict=True):
        if member["offer_status"] != "TERMS_SUBMITTED" or date.fromisoformat(member["offer_date"]) >= day:
            raise ValueError("A submitted offer before the follow-up is required")
        rows = [r for r in inventory["members"] if (r["id"], r["birth"]) == key]
        if len(rows) != 1 or not rows[0]["stable"] or member["name"] != rows[0]["name"]:
            states["not_uniquely_matched_in_inventory"] += 1
            continue
        r = rows[0]
        if not r["contract_owner"]:
            states["current_ownership_not_confirmed"] += 1
            continue
        if not r["contract_end"] or r["scan_agrees_end"] is not True:
            states["current_end_not_independently_verified"] += 1
            continue
        if not r["contract_start"] or not (member["offer_date"] <= r["contract_start"]
                                           <= day.isoformat() <= r["contract_end"]):
            states["fixed_end_start_not_verified_in_window"] += 1
            continue
        states["current_same_club_contract_with_confirmed_end_after_offer"] += 1
        starts[r["contract_start"]] += 1
        ends[r["contract_end"]] += 1
        kinds[r["contract_kind"]] += 1
        futures += any(f["same_club"] and f["has_terms"] and f["start"] > day.isoformat()
                       for f in r["future_spells"])
    return {"schema": "pa-reach-intake-contracts/v1", "date": day.isoformat(),
            "build": inventory["build"], "save_sha256": expected_hash, "submitted": len(queue),
            "outcomes": states, "observed_kind": kinds, "observed_start_dates": starts,
            "independently_confirmed_end_dates": ends, "with_additional_future_same_club_terms": futures}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for label in ("matched_offer_queue", "verified_inventory"):
        parser.add_argument(label, type=Path)
    parser.add_argument("save_sha256")
    args = parser.parse_args()
    print(json.dumps(summarize(json.loads(args.matched_offer_queue.read_bytes()),
                               json.loads(args.verified_inventory.read_bytes()), args.save_sha256), indent=2))

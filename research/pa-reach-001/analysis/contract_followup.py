"""Compare two private club inventories on a declared branch, export only grouped counts."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path


def identity(row):
    if row["stable"] and row["id"] is not None and row["birth"]:
        return row["id"], row["birth"]
    return None


def outcome(before, after, start, end):
    if after is None:
        return "not_located_in_followup_club_inventory"
    if after["owner_missing"]:
        return "contract_ownership_unresolved"
    if not after["contract_owner"]:
        return "no_longer_owned_at_followup"
    previous_end, current_end = before["contract_end"], after["contract_end"]
    if previous_end is None or current_end is None:
        return "contract_end_missing"
    new_start = after["contract_start"]
    if current_end > previous_end:
        if before["scan_agrees_end"] is not True or after["scan_agrees_end"] is not True:
            return "later_end_without_independent_end_confirmation"
        if new_start and start < new_start <= end and new_start != before["contract_start"]:
            return "later_end_confirmed_new_start_observed"
        return "later_end_confirmed_start_not_established"
    if any(e["same_club"] and e["has_terms"] and e["start"] and e["start"] > end
           and e["end"] and e["end"] > previous_end for e in after["future_spells"]):
        return "future_same_club_terms_observed_not_started"
    if current_end < previous_end:
        return "earlier_contract_end"
    return "same_current_end"


def compare(first, last, baseline_hash, checkpoint_hash, branch):
    if (first["build"] != last["build"] or first["deadline"] != last["deadline"]
            or first["source_sha256"] != baseline_hash or last["source_sha256"] != checkpoint_hash):
        raise ValueError("Different build/cutoff or snapshots outside declared branch")
    start, end = first["game_date"], last["game_date"]
    if date.fromisoformat(start) >= date.fromisoformat(end):
        raise ValueError("Two chronological dates required")
    base = [r for r in first["members"] if r["contract_owner"]]
    base_keys = Counter(identity(r) for r in base)
    final_keys = Counter(identity(r) for r in last["members"])
    final = {identity(r): r for r in last["members"] if identity(r) is not None}
    all_outcomes, due_outcomes = Counter(), Counter()
    for row in base:
        key = identity(row)
        if key is None or base_keys[key] != 1 or final_keys[key] > 1:
            status = "identity_unresolved"
        else:
            status = outcome(row, final.get(key), start, end)
        all_outcomes[status] += 1
        if row["expires_by_cutoff"] is True:
            due_outcomes[status] += 1
    incoming = [r for key,r in final.items() if final_keys[key] == 1 and key not in base_keys
                and r["contract_owner"]]
    return dict(branch=branch, build=first["build"], start=start, end=end, deadline=first["deadline"],
                baseline_sha256=baseline_hash, checkpoint_sha256=checkpoint_hash,
                baseline_owned=len(base), all_baseline_outcomes=all_outcomes,
                baseline_due=sum(due_outcomes.values()), baseline_due_outcomes=due_outcomes,
                newly_observed_owned=len(incoming),
                newly_observed_owned_without_fixed_end=sum(not r["contract_end"] for r in incoming),
                candidate_status_requires_separate_intake_evidence=True,
                offer_counts_require_separate_event_ledger=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("baseline", "checkpoint"):
        parser.add_argument(name, type=Path)
    for name in ("baseline_hash", "checkpoint_hash", "branch"):
        parser.add_argument(name)
    a = parser.parse_args()
    print(json.dumps(compare(json.loads(a.baseline.read_bytes()), json.loads(a.checkpoint.read_bytes()),
                             a.baseline_hash, a.checkpoint_hash, a.branch), indent=2))

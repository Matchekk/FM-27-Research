"""Compare two hash-bound, same-day save checkpoints around delegated renewals."""

import argparse
from collections import Counter
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

import fmsave

from facilities_and_pa import manifest, sha256 as file_hash


STAGES = (("ZD-RET-MAR31", "zubieta-contracts-retention-0331.json"),
          ("ZD-RET-MAR31-RENEWALS", "zubieta-contracts-retention-0331-renewals.json"))


def read(path):
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def tag_name(name):
    return sha256(name.strip().casefold().encode()).digest() if name else None


def verify_aliases(save_path, expected_hash, needed):
    if fmsave.__version__ != "0.14.1" or file_hash(save_path) != expected_hash:
        raise ValueError("Wrong immutable source or decoder")
    result = Counter()
    with fmsave.open(save_path, strict=True) as save:
        for player in save.players():
            if player.unique_id not in needed:
                continue
            birth, display, full = needed[player.unique_id]
            if (player.birth_date is not None and player.birth_date.isoformat() == birth
                    and tag_name(player.name) == tag_name(display) and tag_name(player.full_name) == full):
                result[player.unique_id] += 1
    if set(result) != set(needed) or any(n != 1 for n in result.values()):
        raise ValueError("Display name and stored full name do not map to one record")


def index(rows, field):
    by_id = {r[field]: r for r in rows}
    if len(by_id) != len(rows) or None in by_id:
        raise ValueError("Ambiguous membership")
    return by_id


def compile_group(rows):
    factors = Counter((a[4], b[4]) for a, b in rows)
    matrix = [[factors[i, j] for j in range(1, 6)] for i in range(1, 6)]
    outside = [{"before": i, "after": j, "n": n} for (i, j), n in factors.items()
               if i not in range(1, 6) or j not in range(1, 6)]
    return {"n": len(rows), "matrix_before_rows_after_columns_1_to_5": matrix,
            "zero_or_missing_transitions": outside,
            "null_at_either_end": sum(n for (i, j), n in factors.items() if i is None or j is None),
            "changed_factor": sum(n for (i, j), n in factors.items() if i != j),
            "delta_CA_counts": dict(sorted(Counter(b[2]-a[2] for a, b in rows).items())),
            "delta_PA_counts": dict(sorted(Counter(b[3]-a[3] for a, b in rows).items()))}


def audit(panel, before_save, after_save, before_contracts, after_contracts, queue, intake):
    baseline = index(read(queue)["baseline_rows"], "player_id")
    candidates = index(read(intake), "id")
    groups = {uid: "due" if r["due_by_june"] else "later" for uid, r in baseline.items()}
    if set(groups) & set(candidates):
        raise ValueError("Overlapping baseline and intake")
    groups.update(dict.fromkeys(candidates, "intake"))
    counts = Counter(groups.values())
    if counts != {"due": 29, "later": 54, "intake": 16}:
        raise ValueError("Unexpected pre-defined cohorts")
    snapshots, contracts, aliases, hashes = [], [], [], []
    with closing(sqlite3.connect(panel.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        for (tag, source), save, contract_file in zip(
                STAGES, (before_save, after_save), (before_contracts, after_contracts), strict=True):
            expected = manifest(source)
            ledger = read(contract_file)
            digest = expected["save_sha256"]
            meta = db.execute("SELECT sha256,game_date,build,reader FROM capture WHERE tag=?", (tag,)).fetchone()
            if (meta != (digest, "2027-03-31", "27.1.0+2505117", "0.14.1")
                    or ledger["source_sha256"] != digest or ledger["game_date"] != meta[1]
                    or ledger["build"] != meta[2]):
                raise ValueError("Snapshot or contract ledger differs from manifest")
            club = index(ledger["members"], "id")
            records = {r[0]: r[1:] for r in db.execute(
                "SELECT uid,birth,name_check,ca,pa,candidate FROM player WHERE tag=?", (tag,))}
            mismatches = {}
            for uid, group in groups.items():
                row = candidates[uid] if group == "intake" else baseline[uid]
                birth, check = records[uid][:2]
                if not (club[uid]["stable"] and birth == club[uid]["birth"] == row["birth"]
                        and tag_name(row["name"]) == tag_name(club[uid]["name"]) and check):
                    raise ValueError("Missing or unstable candidate identity")
                if tag_name(row["name"]) != check:
                    mismatches[uid] = (birth, row["name"], check)
            verify_aliases(save, digest, mismatches)
            aliases.append(len(mismatches))
            contracts.append(club)
            hashes.append(digest)
            snapshots.append(records)
    a, b = snapshots
    cohort = {uid: (v, b[uid]) for uid, v in a.items()
              if uid in b and v[0] and v[1] and v[:2] == b[uid][:2]}
    if not set(groups).issubset(cohort):
        raise ValueError("Incomplete intervention pairing")
    personal = [set(c) for c in contracts]
    if personal[0] != personal[1]:
        raise ValueError("Changing registered/contracted player inventory")
    ca, cb = contracts
    changed = {uid for uid in personal[0] if ca[uid]["contract_end"] and cb[uid]["contract_end"]
               and cb[uid]["contract_end"] > ca[uid]["contract_end"]}
    same_day_start = {uid for uid in changed if ca[uid]["contract_start"] != cb[uid]["contract_start"]
                      and cb[uid]["contract_start"] == "2027-03-31"}
    if changed != same_day_start:
        raise ValueError("Extension and changed same-day start disagree")
    primary = {g: {uid for uid, label in groups.items() if label == g} for g in counts}
    selections = dict(primary, due_with_later_end_and_new_same_day_start=changed & primary["due"],
                      remaining_club_inventory=personal[0] - groups.keys(),
                      outside_observed_club_inventory=cohort.keys() - personal[0])
    results = {g: compile_group([cohort[uid] for uid in ids if uid in cohort]) for g, ids in selections.items()}
    return {"build": "27.1.0+2505117", "game_date_both": "2027-03-31", "save_hash_before_after": hashes,
            "save_extractor": "fmsave 0.14.1", "separate_native_full_population_on_either_checkpoint": False,
            "population_before_after": [len(a), len(b)], "stable_uid_birth_full_name_pairs": len(cohort),
            "ledger_display_and_full_names_reconciled_before_after": aliases,
            "exact_display_name_matches_to_full_name_at_baseline": sum(counts.values()) - aliases[0],
            "extensions_by_primary_group": {g: len(ids & changed) for g, ids in primary.items()},
            "groups": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("panel", "before_save", "after_save", "before_contracts", "after_contracts", "queue", "intake"):
        parser.add_argument(arg, type=Path)
    print(json.dumps(audit(**vars(parser.parse_args())), indent=2))

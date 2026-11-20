"""Reconcile a control-arm repeat and two club inventories without publishing identities."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3

from zubieta_readback import iso_birth, quoted_database


def audit(private_panel, native, replica, before_contracts, end_contracts, end_scout):
    previous = json.loads(before_contracts.read_bytes())
    current = json.loads(end_contracts.read_bytes())
    day = current["game_date"]
    old = {(row["id"], row["birth"]) for row in previous["members"] if row["stable"]}
    newcomers = [row for row in current["members"]
                 if row["stable"] and (row["id"],row["birth"]) not in old and row["contract_owner"]
                 and row["contract_end"] is None]
    data = json.loads(end_scout.read_bytes().decode("utf-8-sig"))["players"]
    multiplicity = Counter(p["id"] for p in data)
    scan = {p["id"]: p for p in data if multiplicity[p["id"]] == 1}
    result = Counter(first_seen_at_club_without_contract_end=len(newcomers), present_in_strict_native_pairs=0)
    with sqlite3.connect(quoted_database(private_panel), uri=True) as db:
        db.execute("ATTACH ? AS n", (quoted_database(native),))
        db.execute("ATTACH ? AS replica", (quoted_database(replica),))
        differences = {}
        for table in ("snapshot","observation"):
            for lhs,rhs in (("n","replica"),("replica","n")):
                differences[f"{lhs}_minus_{rhs}_{table}"] = db.execute(
                    f"SELECT count(*) FROM (SELECT * FROM {lhs}.{table} EXCEPT SELECT * FROM {rhs}.{table})"
                ).fetchone()[0]
        if any(differences.values()):
            raise ValueError("Control readback or source accounting changed")
        tag, = db.execute("SELECT tag FROM capture WHERE game_date=? AND sha256=?",
                          (day,current["source_sha256"])).fetchone()
        for person in newcomers:
            uid = person["id"]
            saved = db.execute("SELECT birth,ca,pa FROM player WHERE uid=? AND tag=?", (uid,tag)).fetchone()
            if saved is None or saved[0] != person["birth"]:
                continue
            scout = scan.get(uid)
            if scout and saved == (iso_birth(scout),scout["ca"],scout["pa"]):
                result["independent_scout_and_save_ability_agree"] += 1
                if scout.get("expires") is None:
                    result["also_missing_scout_expiry"] += 1
            if db.execute("SELECT 1 FROM n.observation WHERE uid=? AND birth=? AND day=?",
                          (uid,saved[0],day)).fetchone():
                result["present_in_strict_native_pairs"] += 1
    return dict(branch="ZD-CONTROL-01",source_sha256=previous["source_sha256"],
                endpoint_sha256=current["source_sha256"],day=day,repeat_row_differences=differences,
                new_undated_club_members=dict(result),
                verified_youth_candidate_screen_count=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("private_panel", "native", "replica", "before_contracts", "end_contracts", "end_scout"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(**vars(args)),indent=2,sort_keys=True))

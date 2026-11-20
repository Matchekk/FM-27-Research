"""Aggregate the three private Zubieta copies, their native readbacks and a dated Scout export."""

import argparse
from collections import Counter
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import sqlite3

import fmsave


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def quoted_database(path):
    return path.resolve().as_uri() + "?mode=ro"


def iso_birth(player):
    year, ordinal = player.get("birthYear"), player.get("birthDoy")
    if type(year) is not int or type(ordinal) is not int or not 1 <= ordinal <= 366:
        return None
    if not 1850 <= year <= 2200:
        return None
    birth = date(year, 1, 1) + timedelta(days=ordinal - 1)
    return birth.isoformat() if birth.year == year else None


def audit(panel, native, repeat, root_save, scout_path, history_path, training_panel, training_save):
    with sqlite3.connect(quoted_database(panel), uri=True) as db:
        captures = db.execute("SELECT tag,sha256,game_date,build,reader,managed,accounting FROM capture ORDER BY game_date").fetchall()
        managed = [json.loads(row[5]) for row in captures]
        snapshots = [dict(tag=t, sha256=h, game_date=d, build=b, reader=r, accounting=json.loads(a))
                     for t, h, d, b, r, _, a in captures]
        field_counts = {k: len(json.loads(v)) for k, v in db.execute("SELECT name,labels FROM field_order")}
        january = {uid: (birth, pa) for uid, birth, pa in db.execute(
            "SELECT uid,birth,pa FROM player WHERE tag='ZD-HIST-02' AND uid>=2000000000"
        )}
    with sqlite3.connect(quoted_database(native), uri=True) as db:
        db.execute("ATTACH DATABASE ? AS replay", (quoted_database(repeat),))
        differences = {}
        for table in ("snapshot", "observation"):
            for lhs, rhs in (("main", "replay"), ("replay", "main")):
                differences[f"{lhs}_minus_{rhs}_{table}"] = db.execute(
                    f"SELECT count(*) FROM (SELECT * FROM {lhs}.{table} EXCEPT SELECT * FROM {rhs}.{table})"
                ).fetchone()[0]
        if any(differences.values()):
            raise ValueError("Readback repetition mismatch")
        selected = {}
        for day in ("2027-01-31", "2027-03-30"):
            selected[day] = {uid: (birth, ca, pa) for uid, birth, ca, pa in db.execute(
                "SELECT uid,birth,ca,pa FROM observation WHERE day=? AND career='ZD-ROOT-01'", (day,)
            )}
    scout = json.loads(scout_path.read_bytes().decode("utf-8-sig"))
    hist = json.loads(history_path.read_bytes().decode("utf-8-sig"))
    meta = scout["meta"]
    with fmsave.open(root_save) as save:
        if digest(root_save) not in {s["sha256"] for s in snapshots}:
            raise ValueError("Root save was not captured")
        managers = list(save.managed_clubs())
        ob = managers[0] if len(managers) == 1 else None
    with fmsave.open(training_save) as save:
        trainer = [(m.manager_staff_uid, m.club_uid) for m in save.managed_clubs()]
    with sqlite3.connect(quoted_database(training_panel), uri=True) as db:
        early = list(db.execute("SELECT uid,birth,pa FROM observation WHERE career='TRAIN005-A' AND day='2027-01-16' AND uid>=2000000000 AND age<18"))
        expected = db.execute("SELECT save_hash FROM snapshot WHERE career='TRAIN005-A' AND day='2027-01-16'").fetchone()
        if not expected or digest(training_save) != expected[0]:
            raise ValueError("Unbound TRAIN-005 reference")
    if meta["gameDate"] != "2027-03-17" or meta["game"] != "FM27":
        raise ValueError("Unexpected dated export")
    day = meta["gameDate"]
    ledger = Counter(export_rows=len(scout["players"]))
    frequencies = Counter(p["id"] for p in scout["players"])
    explicit = {}
    for p in scout["players"]:
        uid, ca, pa = p["id"], p["ca"], p["pa"]
        birth = iso_birth(p)
        if frequencies[uid] != 1 or not birth or type(ca) is not int or type(pa) is not int or not (1 <= ca <= 200 and 1 <= pa <= 200):
            ledger["export_rows_ambiguous_or_invalid"] += 1
            continue
        explicit[uid] = (ca, pa)
        at_dates = []
        for label, archive in selected.items():
            other = archive.get(uid)
            matched = other is not None and other[0] == birth
            ledger["uid_and_birth_match_" + label] += int(matched)
            at_dates.append(other if matched else None)
        if all(at_dates):
            left, right = at_dates
            ledger["uid_and_birth_match_both_dates"] += 1
            ledger["same_pa_all_three"] += int(left[2] == pa == right[2])
            ledger["ca_differs_from_january"] += int(left[1] != ca)
            ledger["ca_differs_from_march30"] += int(right[1] != ca)
    dates = sorted(hist["dates"])
    explicit_counts = Counter()
    history_match = Counter()
    for uid, points in hist["players"].items():
        for d in points:
            explicit_counts[d] += 1
        if day in points:
            pair = explicit.get(int(uid))
            if pair is None:
                history_match["no_export_key"] += 1
            elif tuple(points[day][:2]) == pair:
                history_match["both_values_agree"] += 1
            else:
                history_match["value_mismatch"] += 1
    return dict(
        as_of="2026-11-20", origin="ZUBIETA", snapshots=snapshots,
        one_matching_filled_manager_staff_uid_and_club_uid=(
            len(managed) == 3 and all(len(m) == 1 and all(v is not None for v in m[0]) for m in managed)
            and all(m == managed[0] for m in managed)
        ),
        private_capture_field_orders=field_counts,
        train005_overlap=dict(
            same_manager_and_own_club=(ob is not None and trainer == [(ob.manager_staff_uid, ob.club_uid)]),
            baseline_under18_uid_at_least_2_billion=len(early),
            january_uid_birth_pa_matches=sum(january.get(uid) == (birth, pa) for uid, birth, pa in early),
            independent_career_validation_allowed=False,
        ),
        independent_repeat=differences,
        auxiliary_scout=dict(
            sha256=digest(scout_path), source=meta["source"], game=meta["game"],
            version=meta["gameVersion"], date=day, date_source=meta["gameDateSource"],
            agrees_manager_name=bool(ob and ob.manager_name and meta.get("manager") == ob.manager_name),
            agrees_managed_club=bool(ob and meta.get("myClub") in (ob.club_name, ob.club_short_name)),
            counters=dict(ledger), same_day_independent_save=False,
        ),
        delta_history=dict(
            sha256=digest(history_path), dates=dates, uid_keys=len(hist["players"]),
            explicit_point_counts=dict(explicit_counts), explicit_march17_against_scout=dict(history_match),
            complete_dob_build_or_branch_at_each_date=False,
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("panel", "native", "repeat", "root_save", "scout_export", "delta_history", "training_panel", "training_save"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    print(json.dumps(audit(args.panel, args.native, args.repeat, args.root_save,
                           args.scout_export, args.delta_history, args.training_panel,
                           args.training_save), indent=2, sort_keys=True))

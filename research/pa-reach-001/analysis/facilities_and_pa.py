"""Audit facility coverage and paired PA changes. Public output contains aggregate counts only."""

import argparse
from collections import Counter
from contextlib import closing
from hashlib import file_digest
import json
from pathlib import Path
import sqlite3
import subprocess


MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"
SCOUT_REVISION = "7fb12175f59b4d41b4418bf0378c3855a5bab4bd"


def sha256(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def manifest(name):
    return json.loads((MANIFESTS / name).read_bytes())


def pair_audit(database, design):
    start, end = sorted(design["snapshots"])
    career = design["career_id"]
    result = {}
    witnessed = []
    with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        for day in (start, end):
            capture = design["snapshots"][day]
            record = db.execute(
                "SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                (career, day),
            ).fetchone()
            if record != (design["engine_build"], capture["save_sha256"], capture["native_sha256"]):
                raise ValueError("Native panel and capture manifest differ")
        for group, baseline in (("all", "1"), ("outfield_under28", "a.age < 28 AND a.position <> 'GK'")):
            sizes = [db.execute(
                "SELECT count(*) FROM observation a WHERE a.career=? AND a.day=? AND " + baseline,
                (career, day),
            ).fetchone()[0] for day in (start, end)]
            pairs = db.execute(f"""
                SELECT a.pa,b.pa,a.club,b.club,a.ca,a.candidate,b.candidate
                FROM observation a JOIN observation b USING(career,uid,birth)
                WHERE a.career=? AND a.day=? AND b.day=? AND {baseline}
            """, (career, start, end))
            delta = Counter()
            for pa, later, club, later_club, ca, factor, later_factor in pairs:
                if not 1 <= pa <= 200 or not 1 <= later <= 200:
                    raise ValueError("Outside native PA scale")
                delta[later - pa] += 1
                if group == "outfield_under28" and club is not None and club == later_club:
                    witnessed.append((club, ca, pa, later, factor, later_factor))
            result[group] = {
                "eligible_baseline": sizes[0],
                "eligible_at_end_using_end_age_and_position": sizes[1],
                "matched_by_baseline_eligibility": sum(delta.values()),
                "baseline_without_identity_pair_at_end": sizes[0] - sum(delta.values()),
                "endpoint_PA_difference_counts": dict(sorted(delta.items())),
            }
    return result, witnessed


def club_ratings(cli, save, expected):
    if sha256(save) != expected:
        raise ValueError("Save differs from frozen input")
    with subprocess.Popen([str(cli), "clubs", str(save)], stdout=subprocess.PIPE) as process:
        rows = json.load(process.stdout)
        if process.wait() != 0:
            raise ValueError("Club reader failed")
    ratings = {row["uid"]: row["training_facilities"] for row in rows}
    if len(ratings) != len(rows) or any(type(v) is not int or not 1 <= v <= 20
                                       for v in ratings.values() if v is not None):
        raise ValueError("Duplicate clubs or invalid training facility ratings")
    return ratings


def coverage(clubs, pairs):
    a, b = clubs
    stable = {uid: value for uid, value in a.items() if value is not None and b.get(uid) == value}
    cap = {1: 70, 2: 75, 3: 85, 4: 95}
    groups = {}
    for label, rows in (
        ("same_observed_club", pairs),
        ("same_observed_club_and_stable_pa_factor_1_4_above_cap_plus_two",
         [r for r in pairs if r[2] == r[3] and r[4] == r[5] and r[4] in cap
          and 100 * r[1] > cap[r[4]] * r[2] + 200]),
    ):
        matched = Counter(stable[club] for club, *_ in rows if club in stable)
        groups[label] = dict(players=len(rows), with_stable_decoded_rating=sum(matched.values()),
                             at_decoded_16=matched[16], at_decoded_17=matched[17])
    return {
        "club_rows_by_day": [len(day) for day in clubs],
        "nonmissing_decoded_by_day": [sum(v is not None for v in day.values()) for day in clubs],
        "same_nonmissing_value_both_dates": len(stable),
        "stable_clubs_at_16": sum(v == 16 for v in stable.values()),
        "stable_clubs_at_17": sum(v == 17 for v in stable.values()),
        "baseline_outfield_under28": groups,
        "held_out_exact_integer_reference": None,
        "verified_facility_boundary_effect": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("history_panel", "control_panel", "pinned_reader_cli", "march_save", "april_save"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    history = manifest("zubieta-native-input.json")
    control = manifest("zubieta-control-native-input.json")
    historical, _ = pair_audit(args.history_panel, history)
    prospective, pairs = pair_audit(args.control_panel, control)
    version = subprocess.check_output([str(args.pinned_reader_cli), "--version"], text=True).strip()
    if version != "fm27scout 1.6.1":
        raise ValueError("Unexpected club reader version")
    clubs = [club_ratings(args.pinned_reader_cli, path, control["snapshots"][day]["save_sha256"])
             for day, path in zip(sorted(control["snapshots"]), (args.march_save, args.april_save), strict=True)]
    print(json.dumps(dict(build=control["engine_build"], external_reader_revision=SCOUT_REVISION,
                          external_reader_version=version, local_executable_sha256=sha256(args.pinned_reader_cli),
                          historical=historical, control=prospective, control_facilities=coverage(clubs, pairs)),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

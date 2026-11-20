"""Reproduce age/PA-gap, world-coverage and endpoint aggregates from dated private panels."""
import argparse
from collections import Counter, defaultdict
from contextlib import closing
from datetime import date
import json
from pathlib import Path
import sqlite3
from statistics import pstdev
import sys

from player_endpoints import endpoint

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))
from pa_reach_summary import age_band, gap_band, growth


def intervals(conn, career, start, end, end_tag):
    counts = Counter()
    groups = defaultdict(list)
    rows = conn.execute("""
        SELECT a.age,a.position,a.ca,a.pa,a.candidate,b.ca,b.pa,b.candidate,s.uid IS NOT NULL
        FROM observation a
        LEFT JOIN observation b ON a.career=b.career AND a.uid=b.uid AND a.birth=b.birth AND b.day=?
        LEFT JOIN structural.player s ON a.uid=s.uid AND a.birth=s.birth AND s.tag=?
        WHERE a.career=? AND a.day=?
    """, (end, end_tag, career, start))
    for age, position, ca, pa, factor, final_ca, final_pa, final_factor, in_save in rows:
        counts["all_observed_start"] += 1
        eligible = age < 28 and position not in (None, "", "GK")
        counts["eligible_start"] += eligible
        if final_ca is None:
            counts["all_start_only"] += 1
            counts["absent_native_but_same_identity_in_save"] += in_save
            counts["absent_native_and_save"] += not in_save
            counts["eligible_missing"] += eligible
            continue
        counts["all_paired"] += 1
        counts["ca_changed"] += ca != final_ca
        counts["pa_changed"] += pa != final_pa
        counts["factor_changed"] += factor != final_factor
        if eligible:
            counts["eligible_paired"] += 1
            groups[age_band(age), gap_band(pa-ca)].append(final_ca-ca)
    counts["all_observed_end"], = conn.execute(
        "SELECT count(*) FROM observation WHERE career=? AND day=?", (career, end)
    ).fetchone()
    counts["all_end_only"] = counts["all_observed_end"] - counts["all_paired"]
    return {"days": (date.fromisoformat(end) - date.fromisoformat(start)).days,
            **counts, "age_gap": {f"{age}/{gap}": {**growth(values), "empirical_sd": round(pstdev(values), 4)}
                                  for (age, gap), values in sorted(groups.items())}}


def landmarks(conn, career, first, last):
    conn.row_factory = sqlite3.Row
    histories = defaultdict(list)
    for row in conn.execute("""
        SELECT b.day,b.age,b.position,b.ca,b.pa,b.birth,b.uid
        FROM observation a JOIN observation b USING(career,uid,birth)
        WHERE a.career=? AND a.day=? AND b.day BETWEEN ? AND ? ORDER BY b.day
    """, (career, first, first, last)):
        histories[row["uid"], row["birth"]].append(row)
    counts = Counter()
    targets = defaultdict(Counter)
    gains = defaultdict(list)
    for history in histories.values():
        row = endpoint(history)
        if row is None:
            continue
        counts["endpoint_eligible"] += 1
        counts["has_exact_quarter"] += bool(row["exact_quarter_windows"])
        counts["has_12_month_ca"] += row["ca_at_exact_month"]["12"] is not None
        counts["has_24_month_ca"] += row["ca_at_exact_month"]["24"] is not None
        qualifying = row["last_observed_quarter_gain_at_least_3_ca"]
        counts["has_observed_quarter_gain_3"] += bool(qualifying)
        if qualifying:
            gains[age_band(history[0]["age"])].append(qualifying["delta_ca"])
        for threshold, result in row["targets"].items():
            targets[threshold][result["status"]] += 1
    return dict(landmark_availability=counts, baseline_under28_field_player_endpoints=targets,
                last_qualified_quarter_gain_by_baseline_age={a: growth(v) for a, v in sorted(gains.items())})


def analyze(native, structural, manifest, end, end_tag):
    career, build = manifest["career_id"], manifest["engine_build"]
    snapshots = {day: source for day, source in manifest["snapshots"].items() if day <= end}
    if end not in snapshots or len(snapshots) < 2:
        raise ValueError("A manifest with the requested end date and a prior observation is required")
    with closing(sqlite3.connect(native.resolve().as_uri() + "?mode=ro", uri=True)) as conn:
        conn.execute("ATTACH DATABASE ? AS structural", (structural.resolve().as_uri() + "?mode=ro",))
        actual = conn.execute("SELECT day,build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day<=? ORDER BY day",
                              (career, end)).fetchall()
        expected = [(day, build, source["save_sha256"], source["native_sha256"])
                    for day, source in sorted(snapshots.items())]
        if actual != expected:
            raise ValueError("Manifest disagrees with native panel dates, build or hashes")
        actual_structural = conn.execute("SELECT game_date,build,sha256 FROM structural.capture WHERE tag=?",
                                         (end_tag,)).fetchone()
        if actual_structural != (end, build, snapshots[end]["save_sha256"]):
            raise ValueError("End tag does not identify the same dated structural save")
        age_gap = {f"{day}:{end}": intervals(conn, career, day, end, end_tag)
                   for day in sorted(snapshots) if day != end}
        return {"engine_build": build, "end": end, "age_gap_intervals": age_gap,
                **landmarks(conn, career, min(snapshots), end)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("native_panel", type=Path)
    parser.add_argument("structural_panel", type=Path)
    parser.add_argument("native_input_manifest", type=Path)
    parser.add_argument("end", type=lambda value: date.fromisoformat(value).isoformat())
    parser.add_argument("end_tag")
    args = parser.parse_args()
    print(json.dumps(analyze(args.native_panel, args.structural_panel,
                             json.loads(args.native_input_manifest.read_bytes()), args.end, args.end_tag),
                     indent=2, sort_keys=True))

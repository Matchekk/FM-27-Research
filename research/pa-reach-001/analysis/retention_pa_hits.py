"""Aggregate observed fixed-PA hits for the March RET baseline up to an exact checkpoint."""

import argparse
from collections import Counter, defaultdict
from datetime import date
from itertools import groupby
import json
from pathlib import Path
import sqlite3

from player_endpoints import ability_targets, birthday_28
from prospective_ca61 import BRANCH, BUILD, MANIFESTS


BASELINE = "2027-03-30"


def counts():
    return {"n": 0, "followup": Counter(), "birthday_coverage": Counter(),
            "goals": defaultdict(Counter), "first_seen_by_date": defaultdict(Counter)}


def measure(db, through):
    dates = db.execute("SELECT day,build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day BETWEEN ? AND ? ORDER BY day",
                       (BRANCH, BASELINE, through)).fetchall()
    if len(dates) < 2 or dates[0][0] != BASELINE or dates[-1][0] != through:
        raise ValueError("Expected the fixed March baseline and exact final checkpoint")
    baseline = json.loads((MANIFESTS / "zubieta-retention-native-input-0430.json").read_bytes())["snapshots"][BASELINE]
    if any(build != BUILD or not save or not inv for _, build, save, inv in dates) or dates[0][2:] != (
            baseline["save_sha256"], baseline["native_sha256"]):
        raise ValueError("Missing or differing snapshot provenance")
    rows = db.execute("""
        SELECT a.uid,a.birth,a.age,a.ca,a.pa,b.day,b.ca,b.pa
        FROM observation a JOIN observation b USING(career,uid,birth)
        WHERE a.career=? AND a.day=? AND b.day BETWEEN a.day AND ?
          AND a.position<>'' AND a.position<>'GK' AND a.age<28 AND a.ca<a.pa
        ORDER BY a.uid,a.birth,b.day
    """, (BRANCH, BASELINE, through))
    grouped = defaultdict(counts)
    for (_, birth), series in groupby(rows, key=lambda r: r[:2]):
        history = list(series)
        _, _, age, ca, pa, _, _, _ = history[0]
        horizon = birthday_28(date.fromisoformat(birth)).isoformat()
        if BASELINE >= horizon:
            raise ValueError("Age disagrees with the birthday horizon")
        age_group = "U18" if age < 18 else "18–20" if age < 21 else "21–23" if age < 24 else "24–27"
        gap = pa - ca
        gap_group = next(label for limit, label in ((2,"1–2"), (5,"3–5"), (10,"6–10"),
                         (20,"11–20"), (30,"21–30"), (200,">30")) if gap <= limit)
        followup = [(day, value) for _, _, _, _, _, day, value, _ in history[1:] if day <= horizon]
        last = history[-1][5]
        coverage = "before_horizon" if last < horizon else (
            "exact_birthday_observed" if any(day == horizon for day, _ in followup)
            else "crossed_without_birthday_observation")
        for key in ("all", "age:"+age_group, "gap:"+gap_group, f"{age_group}|{gap_group}"):
            group = grouped[key]
            group["n"] += 1
            group["followup"]["observed_before_or_at_horizon" if followup else "missing_before_or_at_horizon"] += 1
            group["birthday_coverage"][coverage] += 1
            for name, level in ability_targets(pa).items():
                first_hit = next((day for day, value in followup if value >= level), None)
                if ca >= level:
                    status = "already_at_baseline"
                elif first_hit:
                    status = "first_observed_after_baseline"
                    group["first_seen_by_date"][name][first_hit] += 1
                elif not followup:
                    status = "missing_eligible_followup"
                elif coverage == "before_horizon":
                    status = "right_censored_before_horizon"
                else:
                    status = "no_observed_hit_birthday_interval_coverage_open"
                group["goals"][name][status] += 1
    at_full, = db.execute("""
        SELECT count(*) FROM observation WHERE career=? AND day=?
          AND position NOT IN ('','GK') AND age<28 AND ca>=pa
    """, (BRANCH, BASELINE)).fetchone()
    return {"schema": "pa-reach-retention-fixed-pa-hits/v1", "baseline_day": BASELINE, "last_checkpoint": through,
            "branch": BRANCH, "build": BUILD, "independent_careers": 1,
            "outside_risk_cohort_already_at_full_pa": at_full,
            "snapshots": {day: {"save_sha256": s, "native_sha256": inv} for day, _, s, inv in dates},
            "groups": grouped}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_native_panel", type=Path)
    parser.add_argument("through", type=date.fromisoformat)
    args = parser.parse_args()
    with sqlite3.connect(args.private_native_panel.resolve().as_uri()+"?mode=ro", uri=True) as connection:
        print(json.dumps(measure(connection, args.through.isoformat()), indent=2, sort_keys=True))

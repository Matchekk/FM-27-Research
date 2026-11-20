"""Follow the 2027 youth intake by its independently confirmed first positive factor."""
import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3
from statistics import mean, median


BASE = "2027-04-07"
BRANCH = "ZD-RETENTION-01"
BUILD = "27.1.0+2505117"
INTAKE_HASH = "1dcc8637e4d8047872e16607df854393702d3fa3c9396522c7186ab2048b5973"


def measure(database, roster, target):
    raw = roster.read_bytes()
    if hashlib.sha256(raw).hexdigest() != INTAKE_HASH or target <= date.fromisoformat(BASE):
        raise ValueError("Expected the frozen 2027 intake and a later endpoint")
    sources = {}
    outcomes = defaultdict(list)
    counts = Counter()
    with sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as db:
        for day in (BASE, target.isoformat()):
            source = db.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                                (BRANCH, day)).fetchone()
            if not source or source[0] != BUILD:
                raise ValueError(f"Missing verified checkpoint on {day}")
            sources[day] = {"save_sha256": source[1], "inventory_sha256": source[2]}
        for member in json.loads(raw):
            identity = (BRANCH, member["id"], member["birth"])
            start = db.execute("""
                SELECT o.position,o.ca,o.pa,o.candidate,f.native_factor FROM observation o
                LEFT JOIN factor_check f USING(career,day,uid,birth)
                WHERE o.career=? AND o.uid=? AND o.birth=? AND o.day=?
            """, (*identity, BASE)).fetchone()
            if not start or start[3] not in range(1, 6) or start[3] != start[4]:
                counts["missing_confirmed_starting_factor"] += 1
                continue
            position, ca, pa, tier, _ = start
            if not position or position == "GK":
                counts["excluded_position"] += 1
                continue
            end = db.execute("SELECT ca,pa,candidate FROM observation WHERE career=? AND uid=? AND birth=? AND day=?",
                             (*identity, target.isoformat())).fetchone()
            if end is None:
                counts["missing_target"] += 1
                continue
            counts["paired"] += 1
            outcomes[tier].append((end[0]-ca, pa-ca, end[1] != pa, end[2] != tier))
    summary = {}
    for tier, group in sorted(outcomes.items()):
        growth, gap, pa_changed, factor_changed = zip(*group)
        summary[tier] = {"n": len(group), "baseline_gap_mean": mean(gap),
                         "growth_mean": mean(growth), "growth_median": median(growth),
                         "growth_total": sum(growth), "end_pa_changed": sum(pa_changed),
                         "stored_factor_different_at_end": sum(factor_changed)}
    return {"schema": "pa-reach-intake-tier-growth/v1", "build": BUILD, "independent_roots": 1,
            "baseline": BASE, "target": target.isoformat(), "calendar_days": (target-date.fromisoformat(BASE)).days,
            "intake_sha256": INTAKE_HASH, "intake_size": len(json.loads(raw)), "checkpoints": sources,
            "accounting": counts, "outfield_by_verified_baseline_tier": summary}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("roster", type=Path)
    parser.add_argument("target_date", type=date.fromisoformat)
    args = parser.parse_args()
    print(json.dumps(measure(args.database, args.roster, args.target_date), indent=2))

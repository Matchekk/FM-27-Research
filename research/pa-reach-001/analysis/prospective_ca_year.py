"""Freeze an exact-date annual CA benchmark before the RET target is available."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path
import sqlite3

from prospective_ca61 import BUILD, BRANCH, MANIFESTS, sha


PREVIOUS, ORIGIN, TARGET = "2027-01-31", "2027-03-30", "2028-03-30"
ROOT = "ZD-ROOT-01"
BASE_DAYS = (date.fromisoformat(ORIGIN) - date.fromisoformat(PREVIOUS)).days
FORECAST_DAYS = (date.fromisoformat(TARGET) - date.fromisoformat(ORIGIN)).days


def freeze(history, retention, output):
    manifest = json.loads((MANIFESTS / "zubieta-native-input.json").read_bytes())
    sources = manifest["snapshots"]
    uri = lambda path: path.resolve().as_uri() + "?mode=ro"
    counts = Counter()
    with sqlite3.connect(uri(history), uri=True) as db:
        db.execute("ATTACH DATABASE ? AS ret", (uri(retention),))
        for schema, career, day in (("main", ROOT, PREVIOUS), ("main", ROOT, ORIGIN), ("ret", BRANCH, ORIGIN)):
            item = sources[day]
            row = db.execute(f"SELECT build,save_hash,inventory_hash FROM {schema}.snapshot WHERE career=? AND day=?",
                             (career, day)).fetchone()
            if row != (BUILD, item["save_sha256"], item["native_sha256"]):
                raise ValueError(f"Unverified {career} checkpoint {day}")
        if db.execute("SELECT 1 FROM ret.snapshot WHERE career=? AND day>=?", (BRANCH, TARGET)).fetchone():
            raise ValueError("Target already present in retention panel")
        rows = db.execute("""
            SELECT m.uid,m.birth,m.age,m.pa-m.ca,m.ca,j.ca FROM ret.observation m
            JOIN main.observation j USING(uid,birth)
            WHERE m.career=? AND m.day=? AND j.career=? AND j.day=?
              AND m.age<28 AND m.position<>'' AND m.position<>'GK'
              AND m.ca BETWEEN 1 AND 200 AND m.pa BETWEEN 1 AND 200 AND j.ca BETWEEN 1 AND 200
            ORDER BY m.uid,m.birth
        """, (BRANCH, ORIGIN, ROOT, PREVIOUS))
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            for uid, birth, age, gap, ca, previous_ca in rows:
                age_group = "U18" if age < 18 else "18–20" if age < 21 else "21–23" if age < 24 else "24–27"
                gap_group = "<0" if gap < 0 else "0–10" if gap <= 10 else "11–30" if gap <= 30 else ">30"
                trend = ca * BASE_DAYS + FORECAST_DAYS * (ca - previous_ca)
                trend = max(BASE_DAYS, min(200 * BASE_DAYS, trend))
                counts[f"{age_group}|{gap_group}"] += 1
                stream.write(json.dumps([uid, birth, age_group, gap_group, ca, trend], separators=(",", ":")) + "\n")
    if not counts:
        raise ValueError("No eligible pairs")
    return {"schema": "pa-reach-frozen-annual-ca/v1", "engine_build": BUILD, "target_branch": BRANCH,
            "previous": PREVIOUS, "origin": ORIGIN, "target": TARGET, "history_days": BASE_DAYS,
            "forecast_days": FORECAST_DAYS, "predictor_sources": sources, "private_columns":
            ["uid", "birth", "age_group", "gap_group", "carry_forward_ca", "trend_numerator"],
            "forecast_file_sha256": sha(output), "frozen_counts": counts, "frozen_total": sum(counts.values()),
            "independent_test_careers": 0, "target_observed_at_freeze": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("history", "retention", "private_output"):
        parser.add_argument(flag, type=Path)
    args = parser.parse_args()
    print(json.dumps(freeze(args.history, args.retention, args.private_output), indent=2, sort_keys=True))

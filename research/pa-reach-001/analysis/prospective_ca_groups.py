"""Freeze or score a leave-one-player-out CA growth table for the retention branch."""

import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sqlite3

from prospective_ca61 import BRANCH, BUILD, MANIFESTS, metrics, sha
from prospective_ca_year import TARGET


MARCH, SEPTEMBER = "2027-03-30", "2027-09-30"
FIT_DAYS = (date.fromisoformat(SEPTEMBER) - date.fromisoformat(MARCH)).days
TEST_DAYS = (date.fromisoformat(TARGET) - date.fromisoformat(SEPTEMBER)).days
RECEIPT = MANIFESTS / "prospective-ca-groups-0930.json"
SOURCES = {
    MARCH: ("631a2c000d854fd46d98f0efcce55a5b179367167e8d57b99ad2d7844e4329e4",
            "d8fd3cb42df998b97fb6f61628732dc9a66ae1f33e31b789ab9a96eebf4a2f14"),
    SEPTEMBER: ("a06b6e5f0aa32eeec1a7365b03afc5b0c9d6be303ef728fa6166b1c5f6591456",
                "6a3ecfd1a8b7564c0e303ea06a2cc119caaac44918ecb2298e2bc350601691b8"),
}


def check_snapshot(db, day, save_hash, native_hash):
    row = db.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                     (BRANCH, day)).fetchone()
    if (not all(len(key) == 64 and all(c in "0123456789abcdef" for c in key) for key in (save_hash, native_hash))
            or row != (BUILD, save_hash, native_hash)):
        raise ValueError(f"Unverified retention checkpoint {day}")


def cell(age, ca, pa):
    age_group = "U18" if age < 18 else "18–20" if age < 21 else "21–23" if age < 24 else "24–27"
    gap = pa - ca
    gap_group = "0–10" if gap <= 10 else "11–30" if gap <= 30 else ">30"
    return f"{age_group}|{gap_group}"


def eligible(db, day):
    return {(uid, birth): (age, ca, pa) for uid, birth, age, ca, pa in db.execute("""
        SELECT uid,birth,age,ca,pa FROM observation WHERE career=? AND day=?
          AND age<28 AND position NOT IN ('','GK') AND ca BETWEEN 1 AND 200 AND pa BETWEEN ca AND 200
        ORDER BY uid,birth
    """, (BRANCH, day))}


def freeze(db, output):
    for day, hashes in SOURCES.items():
        check_snapshot(db, day, *hashes)
    if db.execute("SELECT 1 FROM snapshot WHERE career=? AND day>=?", (BRANCH, TARGET)).fetchone():
        raise ValueError("Target already present in retention panel")
    march, september = (eligible(db, day) for day in SOURCES)
    sept_ca = {(u, b): ca for u, b, ca in db.execute("""
        SELECT uid,birth,ca FROM observation WHERE career=? AND day=? AND ca BETWEEN 1 AND 200
    """, (BRANCH, SEPTEMBER))}
    fit_n, fit_delta, contribution = Counter(), Counter(), {}
    for identity, profile in march.items():
        if identity in sept_ca:
            group, change = cell(*profile), sept_ca[identity] - profile[1]
            fit_n[group] += 1
            fit_delta[group] += change
            contribution[identity] = (group, change)
    forecast_n, excluded_self = Counter(), Counter()
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        for identity, profile in september.items():
            group, ca = cell(*profile), profile[1]
            n, delta = fit_n[group], fit_delta[group]
            if identity in contribution and contribution[identity][0] == group:
                n -= 1
                delta -= contribution[identity][1]
                excluded_self[group] += 1
            denominator = FIT_DAYS * n
            if not denominator:
                raise ValueError(f"No valid group history remaining in {group}")
            numerator = max(denominator, min(200*denominator, ca*denominator + TEST_DAYS*delta))
            forecast_n[group] += 1
            stream.write(json.dumps([*identity, group, ca, numerator, denominator], separators=(",", ":")) + "\n")
    return {"schema": "pa-reach-frozen-ca-groups/v1", "branch": BRANCH, "build": BUILD, "target": TARGET,
            "fit_days": FIT_DAYS, "target_days": TEST_DAYS, "sources": {
                day: {"save_sha256": s, "native_sha256": n} for day, (s, n) in SOURCES.items()},
            "march_eligible": len(march), "march_missing_sept_ca": len(march)-sum(fit_n.values()),
            "september_without_march_fit_contribution": len(september.keys()-contribution.keys()),
            "fit_count_by_group": fit_n, "fit_sum_delta_by_group": fit_delta, "self_removed_by_group": excluded_self,
            "forecast_count_by_group": forecast_n, "forecast_total": len(september), "forecast_sha256": sha(output),
            "target_viewed": False, "independent_test_careers": 0}


def score(db, forecast, save_hash, native_hash):
    check_snapshot(db, TARGET, save_hash, native_hash)
    receipt = json.loads(RECEIPT.read_bytes())
    if (receipt["forecast_sha256"], receipt["target"], receipt["branch"], receipt["build"],
        receipt["fit_days"], receipt["target_days"]) != (sha(forecast), TARGET, BRANCH, BUILD, FIT_DAYS, TEST_DAYS):
        raise ValueError("Forecast or timeline differs from the sealed receipt")
    actual = {(u, b): ca for u, b, ca in db.execute("""
        SELECT uid,birth,ca FROM observation WHERE career=? AND day=? AND ca BETWEEN 1 AND 200
    """, (BRANCH, TARGET))}
    frozen, errors = Counter(), defaultdict(lambda: ([], []))
    with forecast.open(encoding="utf-8") as stream:
        for line in stream:
            uid, birth, group, ca, num, den = json.loads(line)
            frozen[group] += 1
            observed = actual.get((uid, birth))
            if observed is not None:
                for name in ("all", group):
                    base, growth = errors[name]
                    base.append(ca-observed)
                    growth.append(num/den-observed)
    if frozen != receipt["forecast_count_by_group"] or sum(frozen.values()) != receipt["forecast_total"]:
        raise ValueError("Forecast counts differ from the sealed receipt")
    groups = {}
    for name, n in {"all": sum(frozen.values()), **frozen}.items():
        base, growth = map(metrics, errors[name])
        groups[name] = {"frozen": n, "missing": n-base["n"], "carry_forward": base, "group_growth": growth,
                        "mae_difference_growth_minus_carry_forward": growth["mae_ca"]-base["mae_ca"] if base["n"] else None}
    return {"schema": "pa-reach-scored-ca-groups/v1", "build": BUILD, "target": TARGET,
            "save_sha256": save_hash, "native_sha256": native_hash, "receipt_sha256": sha(RECEIPT), "groups": groups,
            "independent_test_careers": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    for command in ("freeze", "score"):
        entry = sub.add_parser(command)
        entry.add_argument("retention", type=Path)
        entry.add_argument("forecast", type=Path)
        if command == "score":
            entry.add_argument("--save-sha256", required=True)
            entry.add_argument("--native-sha256", required=True)
    args = parser.parse_args()
    with sqlite3.connect(args.retention.resolve().as_uri()+"?mode=ro", uri=True) as db:
        result = (freeze(db, args.forecast) if args.operation == "freeze" else
                  score(db, args.forecast, args.save_sha256, args.native_sha256))
    print(json.dumps(result, indent=2, sort_keys=True))

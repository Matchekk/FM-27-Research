"""Freeze and score a distribution reference for five exact observed CA checkpoints."""

import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sqlite3
from statistics import median

from player_endpoints import birthday_28
from prospective_ca61 import BRANCH, BUILD, MANIFESTS, metrics, sha
from prospective_ca_groups import cell, check_snapshot, eligible


LEARN = ("2027-03-30", "2027-06-30", "2027-09-30", "2027-12-30", "2028-03-30")
TEST = ("2028-03-30", "2028-06-30", "2028-09-30", "2028-12-30", "2029-03-30")
RECEIPT = MANIFESTS / "prospective-peak-ca-20290330.json"


def observations(db, days):
    return {day: {(u, b): ca for u, b, ca in db.execute("""
        SELECT uid,birth,ca FROM observation WHERE career=? AND day=? AND ca BETWEEN 1 AND 200
    """, (BRANCH, day))} for day in days}


def population(db, start, end):
    end_day = date.fromisoformat(end)
    return {key: profile for key, profile in eligible(db, start).items()
            if end_day <= birthday_28(date.fromisoformat(key[1]))}


def empirical_quantiles(histogram, excluded):
    """Return inverse ECDF P10/P50/P90 after removing the optional own record."""
    total = sum(histogram.values()) - (excluded is not None)
    if total <= 0:
        raise ValueError("No eligible learning history in the target cell")
    ranks = [(p * total + 99) // 100 for p in (10, 50, 90)]
    quantiles, count = [], 0
    for value, frequency in sorted(histogram.items()):
        count += frequency - (value == excluded)
        while len(quantiles) < len(ranks) and ranks[len(quantiles)] <= count:
            quantiles.append(value)
    return quantiles


def freeze(db, output, sources):
    if set(sources) != set(LEARN):
        raise ValueError("Expected exactly the five declared learning snapshots")
    for day in LEARN:
        check_snapshot(db, day, *sources[day])
    if db.execute("SELECT 1 FROM snapshot WHERE career=? AND day>?", (BRANCH, TEST[0])).fetchone():
        raise ValueError("Future-season checkpoints already present in the panel")
    training = population(db, LEARN[0], LEARN[-1])
    targets = population(db, TEST[0], TEST[-1])
    history = observations(db, LEARN[1:])
    histogram, own = defaultdict(Counter), {}
    missing, missing_patterns, predicted, removed = (Counter() for _ in range(4))
    for key, profile in training.items():
        gap = tuple(day for day, series in history.items() if key not in series)
        if gap:
            missing.update(gap)
            missing_patterns["/".join(gap)] += 1
            continue
        group, ca = cell(*profile), profile[1]
        delta = max(ca, *(series[key] for series in history.values())) - ca
        histogram[group][delta] += 1
        own[key] = (group, delta)
    # A cache permits separate exact leave-one-out estimates for each group and historical value.
    cache = {}
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        for key, profile in targets.items():
            group, ca = cell(*profile), profile[1]
            previous_group, delta = own.get(key, (None, None))
            excluded = delta if previous_group == group else None
            if excluded is not None:
                removed[group] += 1
            if (group, excluded) not in cache:
                cache[group, excluded] = empirical_quantiles(histogram[group], excluded)
            forecast = [min(200, ca + extra) for extra in cache[group, excluded]]
            predicted[group] += 1
            stream.write(json.dumps([*key, group, ca, *forecast], separators=(",", ":")) + "\n")
    return {"schema": "pa-reach-frozen-five-observation-peak-ca/v1", "branch": BRANCH, "build": BUILD,
            "learning_days": LEARN, "target_days": TEST, "learning_sources": sources,
            "learning_eligible": len(training), "learning_complete": len(own), "learning_missing_by_day": missing,
            "learning_missing_patterns": missing_patterns, "learning_count_by_cell": {
                group: sum(hist.values()) for group, hist in histogram.items()},
            "forecast_total": len(targets), "forecast_count_by_cell": predicted, "self_removed_by_cell": removed,
            "forecast_sha256": sha(output), "future_outcomes_seen": False, "independent_test_careers": 0}


def score(db, forecasts, sources):
    receipt = json.loads(RECEIPT.read_bytes())
    if (receipt["forecast_sha256"], tuple(receipt["target_days"]), receipt["branch"], receipt["build"]) != (
            sha(forecasts), TEST, BRANCH, BUILD):
        raise ValueError("Unexpected sealed forecast or timeline")
    if set(sources) != set(TEST) or tuple(sources[TEST[0]]) != tuple(receipt["learning_sources"][TEST[0]]):
        raise ValueError("Expected exactly the five registered target snapshots")
    for day in TEST:
        check_snapshot(db, day, *sources[day])
    values = observations(db, TEST)
    cells = defaultdict(lambda: {"frozen": 0, "missing_by_day": Counter(), "missing_patterns": Counter(),
                                "median_errors": [], "baseline_errors": [], "width": 0, "inside": 0})
    with forecasts.open(encoding="utf-8") as stream:
        for line in stream:
            uid, birth, group, base, lower, midpoint, upper = json.loads(line)
            key = uid, birth
            if not 1 <= base <= lower <= midpoint <= upper <= 200 or values[TEST[0]].get(key) != base:
                raise ValueError("Invalid forecast or mismatched baseline CA")
            missing = tuple(day for day, series in values.items() if key not in series)
            for name in ("all", group):
                result = cells[name]
                result["frozen"] += 1
                if missing:
                    result["missing_by_day"].update(missing)
                    result["missing_patterns"]["/".join(missing)] += 1
                    continue
                peak = max(series[key] for series in values.values())
                result["median_errors"].append(midpoint-peak)
                result["baseline_errors"].append(base-peak)
                result["width"] += upper-lower
                result["inside"] += lower <= peak <= upper
    if cells["all"]["frozen"] != receipt["forecast_total"] or {
        k: v["frozen"] for k, v in cells.items() if k != "all"} != receipt["forecast_count_by_cell"]:
        raise ValueError("Frozen group counts differ")
    summary = {}
    for group, result in cells.items():
        n = len(result["median_errors"])
        stratified_errors = result["median_errors"]
        baseline_errors = result["baseline_errors"]
        summary[group] = {"frozen": result["frozen"], "complete": n, "missing": result["frozen"]-n,
                          "missing_by_day": result["missing_by_day"], "missing_patterns": result["missing_patterns"],
                          "stratified": {"coverage": result["inside"]/n if n else None,
                                         "mean_interval_width": result["width"]/n if n else None,
                                         "median_prediction_errors": metrics(stratified_errors),
                                         "median_absolute_error": median(map(abs, stratified_errors)) if n else None},
                          "no_growth": {"coverage": baseline_errors.count(0)/n if n else None,
                                        "mean_interval_width": 0 if n else None,
                                        "median_prediction_errors": metrics(baseline_errors),
                                        "median_absolute_error": median(map(abs, baseline_errors)) if n else None}}
    return {"schema": "pa-reach-scored-five-observation-peak-ca/v1", "branch": BRANCH, "build": BUILD,
            "target_sources": sources, "receipt_sha256": sha(RECEIPT), "groups": summary,
            "independent_test_careers": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    for mode in ("freeze", "score"):
        cmd = sub.add_parser(mode)
        cmd.add_argument("panel", type=Path)
        cmd.add_argument("forecasts", type=Path)
        cmd.add_argument("source_hashes", type=Path, help="Exact date keys mapped to [save SHA-256, inventory SHA-256]")
    args = parser.parse_args()
    snapshots = json.loads(args.source_hashes.read_bytes())
    with sqlite3.connect(args.panel.resolve().as_uri()+"?mode=ro", uri=True) as db:
        result = (freeze if args.operation == "freeze" else score)(db, args.forecasts, snapshots)
    print(json.dumps(result, indent=2, sort_keys=True))

"""Freeze an exact-date annual CA benchmark before the RET target is available."""

import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sqlite3
import sys

from prospective_ca61 import BUILD, BRANCH, MANIFESTS, metrics, sha


PREVIOUS, ORIGIN, TARGET = "2027-01-31", "2027-03-30", "2028-03-30"
ROOT = "ZD-ROOT-01"
BASE_DAYS = (date.fromisoformat(ORIGIN) - date.fromisoformat(PREVIOUS)).days
FORECAST_DAYS = (date.fromisoformat(TARGET) - date.fromisoformat(ORIGIN)).days
RECEIPT = MANIFESTS / "prospective-ca-20280330.json"


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


def score(db, forecasts, expected_save_hash, expected_native_hash, *, receipt=RECEIPT):
    saved = json.loads(receipt.read_bytes())
    if (saved["target"], saved["target_branch"], saved["engine_build"], saved["history_days"],
            saved["forecast_days"], saved["forecast_file_sha256"]) != (
            TARGET, BRANCH, BUILD, BASE_DAYS, FORECAST_DAYS, sha(forecasts)):
        raise ValueError("Frozen forecast receipt differs")
    source = db.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                        (BRANCH, TARGET)).fetchone()
    if (not all(len(value) == 64 and all(c in '0123456789abcdef' for c in value)
                for value in (expected_save_hash, expected_native_hash)) or
            source != (BUILD, expected_save_hash, expected_native_hash)):
        raise ValueError("Expected exact target checkpoint with matching build and both source hashes")
    actual = {(u, b): ca for u, b, ca in db.execute(
        "SELECT uid,birth,ca FROM observation WHERE career=? AND day=? AND ca BETWEEN 1 AND 200", (BRANCH, TARGET))}
    errors = defaultdict(lambda: {"carry_forward": [], "previous_rate": []})
    frozen = Counter()
    seen = set()
    with forecasts.open(encoding="utf-8") as stream:
        for line in stream:
            uid, birth, age, gap, ca, trend = json.loads(line)
            cell = f"{age}|{gap}"
            if (uid, birth) in seen or not 1 <= ca <= 200 or not BASE_DAYS <= trend <= 200 * BASE_DAYS:
                raise ValueError("Invalid identity or value in frozen predictions")
            seen.add((uid, birth))
            frozen[cell] += 1
            observed = actual.get((uid, birth))
            if observed is not None:
                for group in ("all", cell):
                    errors[group]["carry_forward"].append(ca-observed)
                    errors[group]["previous_rate"].append(trend/BASE_DAYS-observed)
    if frozen != saved["frozen_counts"] or len(seen) != saved["frozen_total"]:
        raise ValueError("Frozen cohort differs")
    groups = {}
    for group, n in {"all": len(seen), **frozen}.items():
        measured = {name: metrics(values) for name, values in errors[group].items()}
        base, trend = measured["carry_forward"], measured["previous_rate"]
        groups[group] = {"frozen": n, "observed": base["n"], "missing": n-base["n"], **measured,
                         "mae_difference_previous_rate_minus_carry_forward":
                         trend["mae_ca"]-base["mae_ca"] if base["n"] else None}
    return {"schema": "pa-reach-scored-annual-ca/v1", "target": TARGET, "target_branch": BRANCH,
            "build": BUILD, "save_sha256": source[1], "native_sha256": source[2],
            "receipt_sha256": sha(receipt), "independent_test_careers": 0, "groups": groups}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation", required=True)
    freeze_cli = sub.add_parser("freeze")
    for flag in ("history", "retention", "private_output"):
        freeze_cli.add_argument(flag, type=Path)
    score_cli = sub.add_parser("score")
    score_cli.add_argument("retention", type=Path)
    score_cli.add_argument("forecasts", type=Path)
    score_cli.add_argument("--save-sha256", required=True)
    score_cli.add_argument("--native-sha256", required=True)
    argv = sys.argv[1:]
    if argv and argv[0] not in {"freeze", "score", "-h", "--help"}:
        argv = ["freeze", *argv]
    args = parser.parse_args(argv)
    if args.operation == "freeze":
        result = freeze(args.history, args.retention, args.private_output)
    else:
        with sqlite3.connect(args.retention.resolve().as_uri()+"?mode=ro", uri=True) as db:
            result = score(db, args.forecasts, args.save_sha256, args.native_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))

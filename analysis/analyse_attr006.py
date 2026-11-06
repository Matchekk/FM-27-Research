"""Preregistered paired confirmation of forward JumpingReach in ATTR-006."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
import json
from math import isfinite
from pathlib import Path

import numpy as np

from analyse_attr004 import METRICS, estimate, holm, require
from analyse_attr005 import IDENTITY_FIELDS, SCENARIO, seed_plan as attr005_seeds
from verify_matches import DATA, match_metrics, read, read_rows


EXPERIMENT = "ATTR-006"
ARMS = ("baseline", "FW-JumpingReach")
N = 300
MARGIN = 0.10
PRIOR = read(DATA / "attr-005/manifest.json")


def seed_plan():
    validation, main = attr005_seeds()
    require(PRIOR["validation_seeds"] == validation and PRIOR["seeds"] == main,
            "ATTR-005 seed provenance differs")
    earlier = read(DATA / "attr-004/manifest.json")
    historic = read(DATA / "matches/manifest.json")["seeds"].values()
    legacy = [study["seeds"] for study in read(DATA / "historical/audit.json")["studies"]]
    used = {0}.union(validation, main, earlier["validation_seeds"], *earlier["seeds"].values(),
                     *historic, *legacy)

    def allocate(phase, n):
        seeds = []
        counter = 0
        while len(seeds) < n:
            token = f"{EXPERIMENT}/{phase}/{counter}".encode("ascii")
            seed = int.from_bytes(sha256(token).digest()[:4], "little")
            counter += 1
            if seed not in used:
                seeds.append(seed)
                used.add(seed)
        return seeds

    return allocate("validation", 2), allocate("main", N)


def checked_rows(rows, manifest):
    validation, seeds = seed_plan()
    require(manifest["validation_seeds"] == validation and manifest["seeds"] == seeds, "Seed plan differs")
    require(all(manifest[k] == PRIOR[k] for k in (*IDENTITY_FIELDS, "resource_fingerprint")),
            "Unregistered native identity")
    setups = manifest["scenarios"][SCENARIO]["setups"]
    require(setups == {a: PRIOR["scenarios"][SCENARIO]["setups"][a] for a in ARMS},
            "Setups differ from ATTR-005")
    expected = set(product(seeds, ARMS))
    indexed = {}
    for row in rows:
        seed, arm = key = row["seed"], row["arm"]
        require(key in expected and key not in indexed and type(seed) is int, f"Invalid match key: {key}")
        require(row["status"] == "ok" and row["engine_readback"] is True and 0 < row["finish_tick"] < 47996
                and row["scenario"] == SCENARIO and row["tested_side"] == row["repeat"] == 0
                and row["pair_id"] == f"{EXPERIMENT}/{SCENARIO}/{seed}/0", f"Invalid match: {key}")
        require(all(row[k] == manifest[k] for k in IDENTITY_FIELDS)
                and row["setup_sha256"] == setups[arm] and row["baseline_setup_sha256"] == setups["baseline"],
                f"Provenance mismatch: {key}")
        for field in ("setup_sha256", "raw_log_sha256", "startup_receipt_sha256", "input_dump_sha256"):
            digest = row[field]
            require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                    f"Invalid proof hash {field}: {key}")
        require(len(row["score"]) == len(row["team_statistics"]) == 2
                and all(type(g) is int and g >= 0 for g in row["score"])
                and all(isfinite(team["xg"]) for team in row["team_statistics"]), f"Invalid statistics: {key}")
        indexed[key] = match_metrics(row)
    require(indexed.keys() == expected, f"Incomplete series: {len(indexed)}/{len(expected)} matches")
    return indexed


def decision(result):
    lower = float(result["ci95"][0])
    return dict(positive_confirmed=result["p"] < 0.05 and lower > 0, above_practical_margin=lower > MARGIN)


def summary(values):
    return dict(n=len(values), sd=float(values.std(ddof=1)), **estimate([values], [1]))


def sensitivity(values, full_decision):
    rng = np.random.default_rng(int.from_bytes(sha256(b"ATTR-006/bootstrap").digest()[:8], "little"))
    indices = rng.integers(len(values), size=(20_000, len(values)))
    boot = np.quantile(values[indices].mean(axis=1), [0.025, 0.975]).tolist()
    omitted = [summary(np.delete(values, i)) for i in range(len(values))]

    def bounds(numbers):
        return [min(numbers), max(numbers)]

    return dict(bootstrap_ci95=boot, leave_one_pair_out=dict(
        n_runs=len(omitted), mean_range=bounds([x["mean"] for x in omitted]),
        p_range=bounds([x["p"] for x in omitted]), lower_ci95_range=bounds([x["ci95"][0] for x in omitted]),
        decision_changes={k: sum(decision(x)[k] != value for x in omitted) for k, value in full_decision.items()}))


def analyse(indexed, seeds):
    results = {}
    for metric in METRICS:
        values = np.asarray([indexed[seed, ARMS[1]][metric] - indexed[seed, ARMS[0]][metric] for seed in seeds])
        results[metric] = summary(values)
        if metric == "xgd":
            primary = results[metric]
            primary.update(decision(primary))
            checks = sensitivity(values, decision(primary))
    primary = results.pop("xgd")
    holm(results)
    prior = read(DATA / "attr-005/effects.json")["primary"]["FW/JumpingReach-baseline/xgd"]
    comparison = {k: prior[k] for k in ("n", "mean", "sd", "ci95", "p_holm")}
    return dict(n_matches=len(indexed), n_pairs=len(seeds), primary=primary, sensitivity=checks,
                secondary=results, attr005_screening=comparison)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA / "attr-006")
    parser.add_argument("--seed-plan", action="store_true")
    args = parser.parse_args()
    validation, seeds = seed_plan()
    if args.seed_plan:
        print(json.dumps(dict(validation=validation, main=seeds), indent=2))
        return
    indexed = checked_rows(read_rows(args.data / "matches.jsonl"), read(args.data / "manifest.json"))
    print(json.dumps(analyse(indexed, seeds), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

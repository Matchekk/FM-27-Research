"""Frozen analysis of the ATTR-005 position screening."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations, product
import json
from math import isfinite, sqrt
from pathlib import Path

import numpy as np
from scipy.stats import chi2, nct, t

from analyse_attr004 import METRICS, estimate, holm, require, seed_plan as previous_seed_plan
from verify_matches import DATA, match_metrics, read, read_rows


GROUPS = {
    "CB": ("DCR", "DCL"),
    "FB": ("DR", "DL"),
    "CM": ("DMC", "MCR", "MCL"),
    "FW": ("AMR", "AML", "ST"),
}
ATTRIBUTES = ("JumpingReach", "Acceleration")
ARMS = ("baseline", *(f"{group}-{attr}" for group, attr in product(GROUPS, ATTRIBUTES)))
N = 100
SCENARIO = "standard"
IDENTITY_FIELDS = ("build", "engine_sha256", "adapter_version", "adapter_host_sha256", "fixture_sha256")


def seed_plan():
    previous = read(DATA / "attr-004/manifest.json")
    verified, main = previous_seed_plan()
    require(previous["seeds"] == main and previous["validation_seeds"] == verified,
            "ATTR-004 seed provenance differs")
    history = read(DATA / "matches/manifest.json")["seeds"].values()
    legacy = [s["seeds"] for s in read(DATA / "historical/audit.json")["studies"]]
    used = {0}.union(verified, *main.values(), *history, *legacy)

    def allocate(phase, n):
        seeds = []
        counter = 0
        while len(seeds) < n:
            digest = sha256(f"ATTR-005/{phase}/{counter}".encode("ascii")).digest()
            seed = int.from_bytes(digest[:4], "little")
            counter += 1
            if seed not in used:
                seeds.append(seed)
                used.add(seed)
        return seeds

    return allocate("validation", 2), allocate("main", N)


def checked_rows(rows, manifest):
    validation, main = seed_plan()
    require(manifest["seeds"] == main and manifest["validation_seeds"] == validation,
            "Seed plan differs from preregistration")
    prior = read(DATA / "attr-004/manifest.json")
    require(all(manifest[k] == prior[k] for k in (*IDENTITY_FIELDS, "resource_fingerprint")),
            "Unregistered build, host or fixture")
    setups = manifest["scenarios"][SCENARIO]["setups"]
    require(set(setups) == set(ARMS) and len(set(setups.values())) == len(ARMS), "Invalid arm setups")
    expected = {(seed, arm) for seed in main for arm in ARMS}
    indexed = {}
    for row in rows:
        seed, arm = key = row["seed"], row["arm"]
        require(key in expected and key not in indexed and type(seed) is int, f"Unexpected or duplicate key {key}")
        require(row["status"] == "ok" and row["engine_readback"] is True and 0 < row["finish_tick"] < 47996,
                f"Unvalidated match {key}")
        require(row["scenario"] == SCENARIO and row["repeat"] == row["tested_side"] == 0
                and row["pair_id"] == f"ATTR-005/{SCENARIO}/{seed}/0", f"Invalid seed block {key}")
        require(all(row[k] == manifest[k] for k in IDENTITY_FIELDS)
                and row["setup_sha256"] == setups[arm] and row["baseline_setup_sha256"] == setups["baseline"],
                f"Provenance or input mismatch {key}")
        for field in ("setup_sha256", "raw_log_sha256", "startup_receipt_sha256", "input_dump_sha256"):
            digest = row[field]
            require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                    f"Invalid proof hash {field} {key}")
        require(len(row["score"]) == len(row["team_statistics"]) == 2
                and all(type(g) is int and g >= 0 for g in row["score"])
                and all(isfinite(team["xg"]) for team in row["team_statistics"]), f"Invalid result {key}")
        indexed[key] = match_metrics(row)
    require(indexed.keys() == expected, f"Incomplete seed blocks, {len(indexed)}/{len(expected)} matches")
    return indexed


def power(n, effect, sd, alpha):
    cutoff = t.isf(alpha / 2, n - 1)
    nc = sqrt(n) * effect / sd
    return nct.cdf(-cutoff, n - 1, nc) + nct.sf(cutoff, n - 1, nc)


def required_n(effect, sd, alpha, target):
    if sd == 0:
        return 2
    lo, hi = 1, 2
    while power(hi, effect, sd, alpha) < target:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if power(mid, effect, sd, alpha) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def planning(result):
    sd = result["sd"]
    df = result["n"] - 1
    upper = sd * sqrt(df / chi2.ppf(0.05, df))
    return dict(sd=sd, sd_upper95=upper, scenarios=[
        dict(effect=effect, alpha=alpha, power=target,
             n_seeds=required_n(effect, sd, alpha, target),
             n_seeds_upper_sd=required_n(effect, upper, alpha, target))
        for effect, alpha, target in product((0.10, 0.15, 0.20), (0.05, 0.0125), (0.8, 0.9))
    ])


def analyse(indexed, seeds):
    primary, secondary, variance_planning = {}, {}, {}
    rng = np.random.default_rng(int.from_bytes(sha256(b"ATTR-005/bootstrap").digest()[:8], "little"))
    indices = rng.integers(len(seeds), size=(20_000, len(seeds)))
    directs = {}

    def evaluate(values):
        return dict(n=len(values), variance=float(values.var(ddof=1)), sd=float(values.std(ddof=1)),
                    **estimate([values], [1]))

    for metric in METRICS:
        for group in GROUPS:
            baseline = np.asarray([indexed[seed, "baseline"][metric] for seed in seeds])
            jumping, acceleration = [
                np.asarray([indexed[seed, f"{group}-{attr}"][metric] for seed in seeds])
                for attr in ATTRIBUTES
            ]
            contrasts = (("JumpingReach-baseline", jumping - baseline),
                         ("Acceleration-baseline", acceleration - baseline),
                         ("JumpingReach-Acceleration", jumping - acceleration))
            for label, values in contrasts:
                key = f"{group}/{label}/{metric}"
                result = evaluate(values)
                if metric == "xgd":
                    result["bootstrap_ci95"] = np.quantile(values[indices].mean(axis=1), [0.025, 0.975]).tolist()
                    primary[key] = result
                    variance_planning[key] = planning(result)
                else:
                    secondary[key] = result
            if metric == "xgd":
                directs[group] = jumping - acceleration

    for a, b in combinations(GROUPS, 2):
        key = f"{a}-{b}/JumpingReach-Acceleration/xgd"
        result = evaluate(directs[a] - directs[b])
        secondary[key] = result
        variance_planning[key] = planning(result)
    require(len(primary) == 12 and len(secondary) == 66, "Wrong test family sizes")
    holm(primary)
    holm(secondary)
    return dict(n_matches=len(indexed), n_seed_blocks=len(seeds), primary=primary, secondary=secondary,
                confirmation_planning=variance_planning)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA / "attr-005")
    parser.add_argument("--seed-plan", action="store_true")
    args = parser.parse_args()
    validation, seeds = seed_plan()
    if args.seed_plan:
        print(json.dumps(dict(validation=validation, main=seeds), indent=2))
        return
    manifest = read(args.data / "manifest.json")
    indexed = checked_rows(read_rows(args.data / "matches.jsonl"), manifest)
    print(json.dumps(analyse(indexed, seeds), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

"""Preregistered block analysis of the ATTR-007 forward factorial."""
from argparse import ArgumentParser
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import isfinite, sqrt
from pathlib import Path

import numpy as np
from scipy.stats import chi2

from analyse_attr004 import METRICS, estimate, holm, require
from analyse_attr005 import IDENTITY_FIELDS, SCENARIO, required_n
from analyse_attr006 import seed_plan as attr006_seeds
from verify_matches import DATA, match_metrics, read, read_rows


EXPERIMENT = "ATTR-007"
POSITIONS = ("AMR", "AML", "ST")
ARM_BITS = dict(zip(("baseline", "AMR", "AML", "ST", "AMR+AML", "AMR+ST", "AML+ST", "ALL"),
                    (0, 1, 2, 4, 3, 5, 6, 7), strict=True))
PRIOR = read(DATA / "attr-006/manifest.json")
N = 200


def seed_plan():
    validation, main = attr006_seeds()
    require(PRIOR["validation_seeds"] == validation and PRIOR["seeds"] == main, "ATTR-006 seed provenance differs")
    used = {0, *validation, *main}
    for folder in ("matches", "historical", "attr-004", "attr-005", "attr-006"):
        for path in (DATA / folder).glob("*.jsonl"):
            used.update(row["seed"] for row in read_rows(path) if "seed" in row)

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
    prior_setups = PRIOR["scenarios"][SCENARIO]["setups"]
    setups = manifest["scenarios"][SCENARIO]["setups"]
    require(set(setups) == set(ARM_BITS) and len(set(setups.values())) == len(ARM_BITS)
            and setups["baseline"] == prior_setups["baseline"] and setups["ALL"] == prior_setups["FW-JumpingReach"],
            "Incorrect factorial setups")
    expected = set(product(seeds, ARM_BITS))
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


def coefficients():
    """Return integer contrast numerators in ARM_BITS order and a common divisor per contrast."""
    primary, factorial = {}, {}
    for i, position in enumerate(POSITIONS):
        bit = 1 << i
        primary[f"isolated/{position}"] = (np.array([int(s == bit) - int(s == 0) for s in ARM_BITS.values()]), 1)
        weights = [(1 if s & bit else -1) * (2, 1, 2)[(s & ~bit).bit_count()] for s in ARM_BITS.values()]
        primary[f"shapley/{position}"] = (np.array(weights), 6)
    r, l, st = (primary[f"shapley/{p}"][0] for p in POSITIONS)
    primary["shapley/ST-minus-wing-mean"] = (2 * st - r - l, 12)
    total = np.array([int(s == 7) - int(s == 0) for s in ARM_BITS.values()])
    require(np.array_equal(r + l + st, 6 * total), "Invalid Shapley efficiency identity")
    for size in (1, 2, 3):
        for indices in combinations(range(3), size):
            key = ("main/" if size == 1 else "interaction/") + "*".join(POSITIONS[i] for i in indices)
            mask = sum(1 << i for i in indices)
            weights = [(-1) ** (size - (s & mask).bit_count()) for s in ARM_BITS.values()]
            factorial[key] = (np.array(weights), 2 ** (3 - size))
    return primary, factorial, (total, 1)


def summarise(values, indices):
    result = estimate([values], [1])
    result.update(n=len(values), variance=float(values.var(ddof=1)), sd=float(values.std(ddof=1)),
                  bootstrap_ci95=np.quantile(values[indices].mean(axis=1), [0.025, 0.975]).tolist())
    return result


def planning(result):
    sd = result["sd"]
    df = result["n"] - 1
    upper = sd * sqrt(df / chi2.ppf(0.05, df))
    return dict(sd=sd, sd_upper95=upper, scenarios=[
        dict(effect=effect, alpha=alpha, power=target,
             n_seeds=required_n(effect, sd, alpha, target),
             n_seeds_upper_sd=required_n(effect, upper, alpha, target))
        for effect, alpha, target in product((0.10, 0.15), (0.05, 0.05 / 7), (0.8, 0.9))
    ])


def efficiency(cube, weights, totals):
    def exact(coef, values):
        numerator, divisor = coef
        return sum(int(c) * v for c, v in zip(numerator, values, strict=True)) / divisor

    for row in cube:
        values = [Fraction.from_float(float(x)) for x in row]
        require(sum(exact(w, values) for w in weights) == exact(totals, values),
                "Seed-level exact Shapley sum differs from ALL minus baseline")
    total_w, total_d = totals
    residual = sum(cube @ w / d for w, d in weights) - cube @ total_w / total_d
    maximum = float(np.max(np.abs(residual)))
    require(maximum <= 1e-12, "Floating point Shapley sum exceeded tolerance")
    return dict(exact_blocks=len(cube), max_float_abs_residual=maximum, float_tolerance=1e-12)


def analyse(indexed, seeds):
    primary_weights, factorial_weights, total = coefficients()
    rng = np.random.default_rng(int.from_bytes(sha256(b"ATTR-007/bootstrap").digest()[:8], "little"))
    indices = rng.integers(len(seeds), size=(20_000, len(seeds)))
    primary, factorial, secondary = {}, {}, {}
    for metric in METRICS:
        cube = np.array([[indexed[seed, a][metric] for a in ARM_BITS] for seed in seeds])
        results = {key: summarise(cube @ w / d, indices)
                   for key, (w, d) in (primary_weights | factorial_weights).items()}
        if metric == "xgd":
            primary = {k: results[k] for k in primary_weights}
            factorial = {k: results[k] for k in factorial_weights}
            audit = efficiency(cube, [primary_weights[f"shapley/{p}"] for p in POSITIONS], total)
            combined = summarise(cube @ total[0] / total[1], indices)
            del combined["p"]
        else:
            secondary.update({f"{metric}/{k}": v for k, v in results.items()})
    require((len(primary), len(factorial), len(secondary)) == (7, 7, 70), "Unexpected test families")
    for family in (primary, factorial, secondary):
        holm(family)
    return dict(n_matches=len(indexed), n_seed_blocks=len(seeds), primary=primary, factorial=factorial,
                secondary=secondary, combined_xgd=combined, shapley_efficiency=audit,
                confirmation_planning={k: planning(v) for k, v in (primary | factorial).items()})


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DATA / "attr-007")
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

"""Preregistered ATTR-004 analysis. Requires NumPy 2.3.5 and SciPy 1.16.3."""
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from math import isfinite, sqrt
from pathlib import Path

from verify_matches import DATA, match_metrics, read, read_rows


ARMS = ("baseline", "JumpingReach", "Acceleration")
ARM_CONTRASTS = (("JumpingReach", "Acceleration"),
                 ("JumpingReach", "baseline"), ("Acceleration", "baseline"))
METRICS = ("xgd", "xgf", "xga", "gf", "ga", "points")
FACTORS = ("formation", "opponent", "venue")
SCENARIOS = tuple(product(("433", "4231"), (2, 6), (0, 1)))
N = 140
MARGIN = 0.10
ALPHA = 0.05
BUILD = "27.0.0+2493426"


def seed_plan():
    used = {0}
    for seeds in read(DATA / "matches/manifest.json")["seeds"].values():
        used.update(seeds)
    for study in read(DATA / "historical/audit.json")["studies"]:
        used.update(study["seeds"])

    def allocate(phase, scenario, count):
        seeds = []
        counter = 0
        while len(seeds) < count:
            token = f"ATTR-004/{phase}/{scenario}/{counter}".encode("ascii")
            seed = int.from_bytes(sha256(token).digest()[:4], "little")
            if seed not in used:
                seeds.append(seed)
                used.add(seed)
            counter += 1
        return seeds

    validation = allocate("validation", 0, 2)
    return validation, {str(i): allocate("main", i, N) for i in range(len(SCENARIOS))}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked_rows(rows, manifest):
    _, plan = seed_plan()
    reference = read(DATA / "matches/manifest.json")
    require(manifest["seeds"] == plan, "Seed plan differs from registration")
    fields = ("build", "engine_sha256", "adapter_version", "adapter_host_sha256", "fixture_sha256")
    require(manifest["build"] == BUILD and all(manifest[k] == reference[k] for k in fields),
            "Unregistered engine, adapter or fixture")
    expected = {(s, seed, arm) for s, seeds in plan.items() for seed in seeds for arm in ARMS}
    indexed = {}
    for row in rows:
        s, seed, arm = key = row["scenario"], row["seed"], row["arm"]
        require(key in expected and key not in indexed, f"Unexpected or duplicate key {key}")
        require(row["status"] == "ok" and row["engine_readback"] is True
                and 0 < row["finish_tick"] < 47996, f"Unvalidated match {key}")
        require(type(seed) is int and row["tested_side"] == SCENARIOS[int(s)][2]
                and all(row[k] == manifest[k] for k in fields), f"Provenance mismatch {key}")
        setup = manifest["scenarios"][s]["setups"]
        require(row["setup_sha256"] == setup[arm]
                and row["baseline_setup_sha256"] == setup["baseline"], f"Setup mismatch {key}")
        for field in ("setup_sha256", "raw_log_sha256", "startup_receipt_sha256", "input_dump_sha256"):
            digest = row[field]
            require(len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
                    f"Invalid proof hash {field} {key}")
        require(len(row["score"]) == len(row["team_statistics"]) == 2
                and all(type(g) is int and g >= 0 for g in row["score"])
                and all(isfinite(t["xg"]) for t in row["team_statistics"]), f"Invalid result {key}")
        indexed[key] = match_metrics(row)
    require(set(indexed) == expected, f"Missing {len(expected - set(indexed))} matches")
    return indexed


def estimate(cells, weights):
    import numpy as np
    from scipy.stats import t

    means = [float(values.mean()) for values in cells]
    mean = sum(w * value for w, value in zip(weights, means, strict=True))
    components = [float(w**2 * values.var(ddof=1) / len(values))
                  for w, values in zip(weights, cells, strict=True)]
    variance = sum(components)
    if variance == 0:
        return dict(mean=mean, se=0.0, df=None, ci95=[mean, mean], p=float(mean == 0))
    df = variance**2 / sum(v**2 / (len(x) - 1) for v, x in zip(components, cells, strict=True))
    se = sqrt(variance)
    half_width = t.ppf(1 - ALPHA / 2, df) * se
    return dict(mean=mean, se=se, df=df, ci95=[mean - half_width, mean + half_width],
                p=float(2 * t.sf(abs(mean / se), df)))


def bootstrap_primary(cells):
    import numpy as np

    token = sha256(b"ATTR-004/bootstrap/primary").digest()
    rng = np.random.default_rng(int.from_bytes(token[:8], "little"))
    estimates = np.zeros(20_000)
    for values in cells:
        for start in range(0, len(estimates), 1000):
            indices = rng.integers(len(values), size=(1000, len(values)))
            estimates[start:start + 1000] += values[indices].mean(axis=1) / len(cells)
    return np.quantile(estimates, [0.025, 0.975]).tolist()


def holm(tests):
    adjusted = 0.0
    for rank, result in enumerate(sorted(tests.values(), key=lambda x: x["p"])):
        adjusted = max(adjusted, min(1.0, (len(tests) - rank) * result["p"]))
        result["p_holm"] = adjusted
        result["reject"] = adjusted <= ALPHA


def analyse(indexed):
    import numpy as np

    _, plan = seed_plan()
    primary = None
    secondary = {}
    descriptions = defaultdict(dict)
    for treatment, comparator in ARM_CONTRASTS:
        label = f"{treatment}-{comparator}"
        direct = comparator != "baseline"
        for metric in ("xgd",) if direct else METRICS:
            cells = [
                np.asarray([indexed[s, seed, treatment][metric] - indexed[s, seed, comparator][metric]
                            for seed in seeds], dtype=float)
                for s, seeds in plan.items()
            ]
            pooled = estimate(cells, [1 / 8] * 8)
            key = f"{label}/{metric}"
            if direct:
                primary = pooled
                lo, hi = pooled["ci95"]
                practical = ("JumpingReach" if lo > MARGIN else
                             "Acceleration" if hi < -MARGIN else
                             "within_margin" if -MARGIN < lo <= hi < MARGIN else "uncertain")
                primary.update(reject=primary["p"] <= ALPHA, practical=practical,
                               bootstrap_ci95=bootstrap_primary(cells))
            else:
                secondary[key] = pooled
            for s, values in zip(plan, cells, strict=True):
                cell = estimate([values], [1])
                cell.pop("p")
                descriptions[s][key] = dict(n=len(values), sd=float(values.std(ddof=1)), **cell)
            if metric == "xgd":
                for order in range(1, len(FACTORS) + 1):
                    for indices in combinations(range(len(FACTORS)), order):
                        name = "*".join(FACTORS[i] for i in indices)
                        signs = product((-1, 1), repeat=len(FACTORS))
                        weights = [(-1) ** sum(level[i] == -1 for i in indices) / 4 for level in signs]
                        secondary[f"{key}/{name}"] = estimate(cells, weights)
    require(len(secondary) == 33, "Wrong secondary family size")
    holm(secondary)
    return dict(n_matches=len(indexed), n_triplets=len(indexed) // len(ARMS),
                primary=primary, secondary=secondary, scenarios=dict(descriptions))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--seed-plan", action="store_true")
    parser.add_argument("--data", type=Path, default=DATA / "attr-004")
    args = parser.parse_args()
    if args.seed_plan:
        validation, seeds = seed_plan()
        print(json.dumps(dict(validation=validation, main=seeds), indent=2))
        return
    manifest = read(args.data / "manifest.json")
    results = analyse(checked_rows(read_rows(args.data / "matches.jsonl"), manifest))
    print(json.dumps(results, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

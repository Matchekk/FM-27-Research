"""Verify and reproduce the archived match statistics. Requires NumPy 2.3.5."""

from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import isclose, sqrt
from pathlib import Path
from statistics import mean, stdev

import numpy as np


DATA = Path(__file__).resolve().parents[1] / "data"
METRICS = ("xgd", "gf", "ga", "points", "xgf", "xga", "sf", "sa", "sotf", "sota")
BOOTSTRAPS = 20_000
PERMUTATIONS = 49_999


def read(path):
    return json.loads(path.read_text(encoding="utf8"))


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf8").splitlines()]


def match_metrics(row):
    side = row["tested_side"]
    a, b = row["team_statistics"][side], row["team_statistics"][1 - side]
    gf, ga = row["score"][side], row["score"][1 - side]
    for team in (a, b):
        assert team["xg"] >= 0 and 0 <= team["shots_on_target"] <= team["shots"]
        assert 0 <= team["completed_passes"] <= team["passes"]
        assert 0 <= team["possession"] <= 1
    assert isclose(a["possession"] + b["possession"], 1, abs_tol=1e-6)
    assert gf >= 0 and ga >= 0
    return dict(zip(METRICS, (a["xg"] - b["xg"], gf, ga, 3 if gf > ga else int(gf == ga),
                              a["xg"], b["xg"], a["shots"], b["shots"],
                              a["shots_on_target"], b["shots_on_target"]), strict=True))


def estimate(values, key):
    a = np.array(values, dtype=np.float64)
    n = len(a)
    rng = np.random.default_rng(int.from_bytes(sha256(key.encode()).digest()[:8], "little"))
    boot = np.concatenate([
        a[rng.integers(n, size=(min(1000, BOOTSTRAPS - i), n))].mean(axis=1)
        for i in range(0, BOOTSTRAPS, 1000)
    ])
    cutoff = abs(a.sum()) - 1e-12
    if n <= 16:
        signs = np.asarray(list(product((-1, 1), repeat=n)))
        p = float(np.mean(np.abs((signs * a).sum(axis=1)) >= cutoff))
    else:
        extreme = 0
        for i in range(0, PERMUTATIONS, 1000):
            signs = rng.integers(0, 2, size=(min(1000, PERMUTATIONS - i), n), dtype=np.int8) * 2 - 1
            extreme += int(np.count_nonzero(np.abs((signs * a).sum(axis=1)) >= cutoff))
        p = (extreme + 1) / (PERMUTATIONS + 1)
    return dict(n=n, mean=float(a.mean()), sd=float(a.std(ddof=1)),
                ci95=np.quantile(boot, [0.025, 0.975]).tolist(), p=p)


def correct(family):
    family = sorted(family, key=lambda item: item["p"])
    m = len(family)
    harmonic = sum(1 / i for i in range(1, m + 1))
    q = 1.0
    for i, item in reversed(list(enumerate(family, 1))):
        q = min(q, item["p"] * m / i)
        item.update(q=q, q_by=min(1.0, q * harmonic))


def compare(a, b):
    if isinstance(a, dict):
        assert a.keys() == b.keys(), (a.keys(), b.keys())
        for k, v in a.items():
            compare(v, b[k])
    elif isinstance(a, list):
        for x, y in zip(a, b, strict=True):
            compare(x, y)
    elif isinstance(a, float):
        assert isclose(a, b, rel_tol=1e-12, abs_tol=1e-12), (a, b)
    else:
        assert a == b, (a, b)


def audit_historical():
    archive = DATA / "historical"
    results = read(archive / "audit.json")
    assert results["passed"]
    for item, t in zip(results["studies"], (2.200985, 2.068658), strict=True):
        rows = read_rows(archive / (item["study"] + ".jsonl"))
        groups = {(r["attribute"], r["seed"]): r for r in rows}
        seeds = item["seeds"]
        assert len(groups) == len(rows) == item["matches"]
        assert set(groups) == {(a, s) for a in ("baseline", *item["reproduced_effects"]) for s in seeds}
        for r in rows:
            assert r["status"] == "ok" and r["tested_side"] == 0
            assert r["baseline_setup_sha256"] == item["legacy_baseline_hash"]
        def metrics(r):
            a, b = r["team_statistics"]
            m = match_metrics(r)
            return dict(goals=m["gf"] - m["ga"], xg=m["xgd"], shots=m["sf"] - m["sa"],
                        passing_percentage=100 * (a["completed_passes"] / a["passes"] -
                                                  b["completed_passes"] / b["passes"]))
        for arm, values in item["reproduced_effects"].items():
            for metric, value in values.items():
                delta = [metrics(groups[arm, s])[metric] - metrics(groups["baseline", s])[metric] for s in seeds]
                m = mean(delta)
                half_width = t * stdev(delta) / sqrt(len(seeds))
                compare(dict(mean=round(m, 4), interval95=[round(m - half_width, 4), round(m + half_width, 4)]), value)


def audit_training():
    archive = DATA / "training"
    exposure = read(archive / "exposure.json")
    groups = {}
    for row in read_rows(archive / "player-deltas.jsonl"):
        key = tuple(row[k] for k in ("trial", "cohort", "checkpoint", "arm"))
        group = groups.setdefault(key, {})
        assert row["subject"] not in group
        group[row["subject"]] = row["delta"]
    assert len(groups) == 30 and all(len(group) == 22 for group in groups.values())

    for trial, cohort, week, intervention in (
        ("conditioning-heavy", "senior", 6, "B"), ("conditioning-rest", "youth", 4, "C"),
    ):
        reference = groups[trial, cohort, week, "A"]
        treated = groups[trial, cohort, week, intervention]
        diffs = {}
        for field in ("acceleration", "pace", "agility", "stamina"):
            diffs[field] = round(mean(treated[u]["raw"][field] - x["raw"][field]
                                      for u, x in reference.items()), 4)
        diffs["ca"] = round(mean(treated[u]["ca"] - x["ca"] for u, x in reference.items()), 4)
        assert sum(w["retained_paired_slots"] for w in exposure[trial]) == 2 * week
        print(f"{trial} endpoint differences: {diffs}")

    plan = exposure["five-week-plans"]
    for cohort, outcomes in plan["outcomes"].items():
        for arm, outcome in outcomes.items():
            deltas = list(groups["five-week-plans", cohort, 5, arm].values())
            for field, key in (("ca", "ca"), ("pa", "pa"), ("condition", "rawCondition"),
                               ("sharpness", "rawSharpness")):
                assert round(mean(x[field] for x in deltas if x[field] is not None), 4) == outcome[key]
            attributes = {}
            for key in deltas[0]["raw"]:
                values = [x["raw"][key] for x in deltas if x["raw"][key] is not None]
                if values:
                    attributes[key] = round(mean(values), 4)
            assert round(mean(attributes.values()), 4) == outcome["rawMean"]
        retained = planned = other = 0
        for week in plan["weeks"]:
            calendars = [arm[cohort] for arm in week["arms"].values()]
            slots = [{(day, slot): (target, actual) for day, slot, target, actual in c["planned"]}
                     for c in calendars]
            assert all(set(s) == set(slots[0]) for s in slots)
            grids = [{(day, slot): code for day, slot, code in c["calendar"]} for c in calendars]
            planned += len(slots[0])
            retained += sum(all(s[k][0] == s[k][1] for s in slots) for k in slots[0])
            other += sum(len({g[k] for g in grids}) > 1 for k in grids[0] if k not in slots[0])
        assert dict(allArmsRetained=retained, planned=planned, unplannedDifferent=other) == plan["calendar_audit"][cohort]


def main():
    archive = DATA / "matches"
    manifest = read(archive / "manifest.json")
    original = read(archive / "effects.json")
    sets = {k: set(v) for k, v in manifest["seeds"].items()}
    assert all(not a & b for a, b in combinations(sets.values(), 2))
    effects, deltas, counts = {}, {}, {}
    for phase, spec in manifest["datasets"].items():
        rows = read_rows(archive / (phase + ".jsonl"))
        seeds = sorted(sets["away" if phase == "venue_home" else phase])
        configs = spec["configs"]
        scenario = spec["scenario"]
        repeat_ids = range(3) if phase == "validation" else (0,)
        index = {(r["attribute"], r["seed"], r["repeat"]): r for r in rows}
        assert len(index) == len(rows) == spec["matches"]
        assert set(index) == {(a, s, repeat) for a in configs for s in seeds for repeat in repeat_ids}
        for (arm, seed, repeat), r in index.items():
            assert r["status"] == "ok" and r["engine_readback"] and 0 < r["finish_tick"] < 47996
            assert (r["phase"], r["scenario"], r["tested_side"]) == (phase, scenario, spec["tested_side"])
            for k in ("build", "adapter_version", "adapter_host_sha256"):
                assert r[k] == manifest[k]
            assert r["setup_sha256"] == configs[arm]["setup_sha256"]
            assert r["baseline_setup_sha256"] == configs["baseline"]["setup_sha256"]
            assert r["pair_id"] == f"{phase}/{scenario}/{seed}/{repeat}"
            assert r["attribute_id"] == manifest["attributes"].get(arm)
            assert r["intervention"] == ("unchanged" if arm == "baseline" else "12->16")
            match_metrics(r)
        if phase == "validation":
            for a in configs:
                for s in seeds:
                    keys = ("score", "team_statistics", "finish_tick", "native_attribute_counts")
                    assert all(index[a, s, repeat][k] == index[a, s, 0][k] for k in keys for repeat in repeat_ids)
            continue
        counts[phase] = dict(ok=len(rows), failed=0, not_run=0, failed_attempts=0)
        deltas[phase] = {}
        for a in set(configs) - {"baseline"}:
            deltas[phase][a] = {
                s: {k: v - match_metrics(index["baseline", s, 0])[k]
                    for k, v in match_metrics(index[a, s, 0]).items()}
                for s in seeds
            }
        effects[phase] = {
            a: {k: estimate([x[k] for x in pairs.values()], f"{phase}/{a}/{k}") for k in METRICS}
            for a, pairs in deltas[phase].items()
        }
        for k in METRICS:
            correct([r[k] for r in effects[phase].values()])

    order = sorted(effects["screening"], key=lambda a: (-effects["screening"][a]["xgd"]["mean"], a))
    selected = order[:5]
    assert manifest["selection"]["ranking"] == order and manifest["selection"]["selected"] == selected
    assert set(selected) == deltas["confirmation"].keys()
    assert all(set(selected[:2]) == deltas[p].keys() for p in ("opponent", "away", "venue_home"))
    confirm = deltas["confirmation"]
    direct = {
        f"{a} - {b}": estimate([confirm[a][s]["xgd"] - confirm[b][s]["xgd"] for s in sorted(sets["confirmation"])],
                               f"rank/{a}/{b}")
        for a, b in combinations(selected, 2)
    }
    venue = {
        a: estimate([deltas["away"][a][s]["xgd"] - deltas["venue_home"][a][s]["xgd"] for s in sorted(sets["away"])],
                    f"venue/{a}")
        for a in selected[:2]
    }
    correct(list(direct.values()))
    correct(list(venue.values()))
    compare(dict(counts=counts, metrics=effects, direct_rank_contrasts=direct, venue_contrasts=venue), original)
    bad = read_rows(archive / "validation-failures.jsonl")
    assert len(bad) == 2 and all(r["status"] == "failed" and "score" not in r and r["exit_code"] == 108 for r in bad)
    audit_historical()
    audit_training()
    print("Reproduced 2,504 matches, 2,080 baseline contrasts, 10 rank contrasts and 2 venue contrasts.")
    print("Historical summaries from another 228 matches match the archive.")


if __name__ == "__main__":
    main()

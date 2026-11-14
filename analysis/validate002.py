"""Bounded technical validation. Never evaluates tactical superiority."""
import argparse
import base64
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research.native import NativeLab, digest, event, read, require, rows, write

ROOT = Path(__file__).resolve().parents[1]
RESULT_FIELDS = ("score", "finish_tick", "team_statistics")


def seeds():
    used = {0}
    for path in (ROOT / "data").rglob("*.jsonl"):
        used.update(r["seed"] for r in rows(path) if "seed" in r)
    result, counter = [], 0
    while len(result) < 2:
        seed = int.from_bytes(sha256(f"VALID-002/technical/{counter}".encode()).digest()[:4], "little")
        counter += 1
        if seed not in used:
            used.add(seed)
            result.append(seed)
    return result


def make_jobs(lab, configs, plan, repeats):
    jobs = []
    for name, config in configs.items():
        binary = lab.artifacts / (name + ".bin")
        lab.encode(config, binary)
        for seed in plan:
            for repeat in range(repeats):
                jobs.append(dict(key=f"{name}-{seed}-r{repeat}", seed=seed, config=config,
                                 binary=binary, arm=name, side=int(name.startswith("away"))))
    return sorted(jobs, key=lambda j:sha256(j["key"].encode()).digest())


def core(lab):
    base = lab.baseline()
    pressing = deepcopy(base)
    group = next(g for g in lab.server.GROUPS.values() if g["name"] == "TriggerPress")
    old = pressing["teams"][0]["instructions"][str(group["id"]) ]
    chosen = next(o["id"] for o in reversed(group["options"]) if o["id"] != old)
    pressing["teams"][0]["instructions"][str(group["id"])] = chosen
    pressing = lab.server.validate_scenario(pressing)
    configs = dict(home_baseline=base, home_pressing=pressing,
                   away_baseline=lab.mirror(base), away_pressing=lab.mirror(pressing))
    write(lab.artifacts / "configs.json", configs)
    plan = seeds()
    write(lab.artifacts / "plan.json", dict(identity=lab.identity, seeds=plan,
                                           intervention=dict(group=group["name"], before=old, after=chosen)))
    results, timing = lab.run(make_jobs(lab, configs, plan, 2), lab.artifacts / "core", 2, bounded_validation=True)
    indexed = {(r["arm"],r["seed"],r["key"].split("-r")[-1]):r for r in results}
    checks = []
    for arm in configs:
        for seed in plan:
            a,b = (indexed[arm,seed,str(i)] for i in (0,1))
            same = all(a[k] == b[k] for k in RESULT_FIELDS)
            checks.append(dict(arm=arm, seed=seed, exact=same))
    require(all(c["exact"] for c in checks), "Deterministic repeat mismatch")
    for arm in ("home_baseline", "home_pressing"):
        mirror = configs[arm.replace("home", "away")]
        for a,b in zip(configs[arm]["teams"], reversed(mirror["teams"]), strict=True):
            require(a["phases"] == b["phases"] and a["instructions"] == b["instructions"] and
                    [p["attributes"] for p in a["players"][:23]] == [p["attributes"] for p in b["players"][:23]], "Side transfer differs")
    write(lab.artifacts / "core-summary.json", dict(passed=True, repeats=checks, timing=timing))


def extras(lab, fmf, saved):
    require(read(lab.artifacts / "core-summary.json")["passed"], "Core gate missing")
    configs, plan = read(lab.artifacts / "configs.json"), read(lab.artifacts / "plan.json")["seeds"]
    core_rows = rows(lab.artifacts / "core/ledger.jsonl")
    reference = {(r["arm"],r["seed"]):r for r in core_rows}
    benchmark = []
    for workers in (1,2,4):
        result, timing = lab.run(make_jobs(lab, configs, plan, 1), lab.artifacts / f"benchmark-{workers}", workers, bounded_validation=True)
        require(all(all(r[k] == reference[r["arm"],r["seed"]][k] for k in RESULT_FIELDS) for r in result), "Worker-count result mismatch")
        benchmark.append(timing)
    write(lab.artifacts / "benchmark-summary.json", benchmark)
    full, timing = lab.run(make_jobs(lab, {"home_baseline": configs["home_baseline"]}, plan[:1], 2), lab.artifacts / "full-events", 1, full=True, bounded_validation=True)
    require(all(r["events_verified"] for r in full), "Full event audit missing")
    require(all(r[k] == reference[r["arm"],r["seed"]][k] for r in full for k in RESULT_FIELDS), "Quick/full mismatch")
    write(lab.artifacts / "full-summary.json", dict(passed=True, timing=timing))
    scenario = configs["home_baseline"]
    results = {}
    for name, changed in (("schema", dict(scenario, schema=999)), ("role", deepcopy(scenario))):
        if name == "role":
            changed["teams"][0]["phases"][0][10]["role"] = "INTENTIONALLY_INVALID"
        try:
            lab.server.validate_scenario(changed)
        except ValueError:
            results[name] = "rejected"
        else:
            raise ValueError(f"Invalid {name} was accepted")
    try:
        lab.server.import_fmf(dict(side=0, scenario=scenario, file_base64=base64.b64encode(b"invalid").decode()))
    except ValueError:
        results["fmf"] = "rejected"
    else:
        raise ValueError("Invalid FMF accepted")
    invalid = lab.artifacts / "invalid.bin"
    invalid.write_bytes(b"INTENTIONAL_INVALID_CONFIGURATION")
    log = lab.artifacts / "negative.jsonl"
    p = subprocess.run([str(lab.server.native_host()), "--scenario-file", str(invalid), "--output", str(log)],
                       cwd=lab.root, capture_output=True, timeout=45, creationflags=subprocess.CREATE_NO_WINDOW)
    (lab.artifacts / "negative.stdout").write_bytes(p.stdout+p.stderr)
    require(p.returncode == 108 and not any(r.get("event") == "natural_match_finished" for r in rows(log)), "Native negative probe failed")
    results["binary"] = dict(returncode=p.returncode, raw_log_sha256=digest(log))
    write(lab.artifacts / "negative-summary.json", results)
    imported = lab.server.import_fmf(dict(side=0, scenario=scenario, file_base64=base64.b64encode(fmf.read_bytes()).decode()))
    out = lab.server.export_fmf(dict(side=0, scenario=imported["scenario"], name="VALID002-roundtrip"))
    require(out["report"]["native_roundtrip_verified"], "FMF semantic parity failed")
    write(lab.artifacts / "fmf-summary.json", dict(source_sha256=digest(fmf), report=out["report"],
             in_possession=[c["position"] for c in imported["scenario"]["teams"][0]["phases"][0]],
             out_of_possession=[c["position"] for c in imported["scenario"]["teams"][0]["phases"][1]]))
    if saved:
        # A saved PKM is only tested for reader acceptance and controlled re-simulation.
        jobs = make_jobs(lab, {"home_baseline":scenario}, plan[:1], 2)
        for job in jobs:
            job["fixture"] = saved.resolve()
        try:
            result,timing = lab.run(jobs, lab.artifacts / "saved-pkm", 1, bounded_validation=True)
            write(lab.artifacts / "saved-summary.json", dict(passed=True, source_sha256=digest(saved),
                exact=all(result[0][k]==result[1][k] for k in RESULT_FIELDS), timing=timing,
                historical_replay_equivalence=False))
        except (RuntimeError,ValueError) as error:
            write(lab.artifacts / "saved-summary.json", dict(passed=False, source_sha256=digest(saved),
                  error_type=type(error).__name__, historical_replay_equivalence=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("core", "extras"))
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--fmf", type=Path)
    parser.add_argument("--saved", type=Path)
    args = parser.parse_args()
    lab = NativeLab(args.runtime, args.game, args.artifacts)
    if args.phase == "core":
        core(lab)
    else:
        require(args.fmf is not None, "FMF source required")
        extras(lab, args.fmf, args.saved)

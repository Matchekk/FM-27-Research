"""Small experiment contracts, immutable registrations, seeds and match plans."""
from hashlib import sha256
from itertools import product
import json
import math
from pathlib import Path
import re

from .native import digest, require, rows, write

MODULES = ("TACT", "ATTR", "TRAIN", "SET", "MECH", "SCOUT")
IDENTITY_FIELDS = ("build", "engine_sha256", "adapter_host_sha256", "adapter_version",
                   "fixture_sha256", "resource_fingerprint", "lab_version", "lab_commit")
HASH = re.compile(r"[0-9a-f]{64}\Z")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf8")


def config_hash(value):
    return sha256(canonical(value)).hexdigest()


def validate(config, executable=False):
    """The same contract governs every module; draft plans cannot execute."""
    require(isinstance(config, dict) and config.get("schema_version") == 1, "Unknown experiment schema")
    module = config.get("module")
    require(module in MODULES and re.fullmatch(module+r"-\d{3}(?:-[A-Za-z0-9-]+)?", config.get("experiment_id", "")), "Invalid experiment ID/module")
    require(config.get("kind") in ("native", "career") and config.get("stage") in
            ("technical", "discovery", "confirmation"), "Unknown experiment kind/stage")
    require(config.get("status") in ("draft", "registered"), "Unknown registration status")
    for key in ("hypothesis", "control", "intervention", "conditions"):
        require(isinstance(config.get(key), str) and config[key].strip(), f"Missing {key}")
    metrics, design, science, budget = (config[k] for k in ("metrics", "design", "science", "budget"))
    require(isinstance(metrics["primary"], str) and metrics["primary"] and
            isinstance(metrics["secondary"], list) and len(set(metrics["secondary"])) == len(metrics["secondary"]), "Invalid endpoints")
    require(design["unit"] == ("seed_block" if config["kind"] == "native" else "career_branch"), "Wrong independent unit")
    require(type(design["n_blocks"]) is int and design["n_blocks"] > 0, "Invalid sample size")
    arms, scenarios = design["arms"], design["scenarios"]
    require(len(arms) >= 2 and len({a['id'] for a in arms}) == len(arms) and
            arms[0]["id"] == design.get("control_arm", "baseline"), "Invalid arms/control")
    require(scenarios and len({s['id'] for s in scenarios}) == len(scenarios), "Invalid scenarios")
    require(design["sides"] and len(set(design["sides"])) == len(design["sides"]) and
            all(type(s) is int and s in (0,1) for s in design["sides"]), "Invalid team sides")
    require(all(s.get("opponent") and s.get("strength") and s.get("split") in ("discovery","confirmation","technical") for s in scenarios), "Missing opponent/strength/split")
    require(all(s["split"] == config["stage"] for s in scenarios), "Discovery/confirmation scenario leakage")
    for key in ("analysis", "exclusions", "negative_controls", "readback_fields", "stopping_rule", "selection_rule", "power_basis"):
        require(science.get(key), f"Missing scientific requirement: {key}")
    require(science.get("multiple_testing") in ("none", "holm", "bh"), "Missing multiplicity rule")
    require(type(science.get("family_size")) is int and science["family_size"] > 0, "Invalid family size")
    require(science["family_size"] == 1 or science["multiple_testing"] != "none", "Multiple testing uncorrected")
    require(type(science.get("alpha")) in (float,int) and 0 < science["alpha"] < 1, "Invalid alpha")
    if config["stage"] != "technical":
        require(type(science.get("power")) in (int,float) and .5 < science["power"] < 1, "Missing power plan")
        require(type(science.get("min_effect")) in (int,float) and science["min_effect"] > 0 and math.isfinite(science["min_effect"]), "Missing practical effect")
    require(re.fullmatch(r"[A-Za-z0-9._/-]+", config["seed_namespace"]), "Invalid seed namespace")
    require(type(budget["max_workers"]) is int and 1 <= budget["max_workers"] <= 4 and
            type(budget["max_matches"]) is int and budget["max_matches"] > 0 and
            type(budget["timeout_seconds"]) is int and 1 <= budget["timeout_seconds"] <= 90, "Invalid resource budget")
    if config["kind"] == "native":
        planned = design["n_blocks"] * len(arms) * len(scenarios) * len(design["sides"])
        require(planned <= budget["max_matches"], "Plan exceeds match budget")
    else:
        require(config["module"] == "TRAIN" or config.get("career"), "Career conditions missing")
    if executable:
        require(config["status"] == "registered", "Draft cannot execute")
        require(module != "SCOUT", "SCOUT is reserved for later application")
        identity = config["identity"]
        require(all(identity.get(k) for k in IDENTITY_FIELDS), "Unpinned native identity")
        require(all(HASH.fullmatch(identity[k]) for k in IDENTITY_FIELDS if k.endswith("sha256") or k=="resource_fingerprint"), "Invalid identity digest")
        require(all(HASH.fullmatch(a.get("setup_sha256", "")) for a in arms), "Unpinned arm setup")
        if "setups" in design:
            cells=design["setups"]
            require(set(cells)=={s["id"] for s in scenarios}, "Setup scenarios differ")
            for by_side in cells.values():
                require(set(by_side)=={str(s) for s in design["sides"]}, "Setup sides differ")
                for by_arm in by_side.values():
                    require(set(by_arm)=={a["id"] for a in arms} and all(HASH.fullmatch(v) for v in by_arm.values()), "Incomplete cell setup hashes")
        require(re.fullmatch(r"[0-9a-f]{40}", config["preregistration"]["commit"]), "Preregistration commit missing")
        require(HASH.fullmatch(config["preregistration"]["document_sha256"]) and
                HASH.fullmatch(config["preregistration"]["analysis_sha256"]), "Unpinned preregistration/analysis")
        if config["stage"] == "confirmation" and module == "TACT":
            require(HASH.fullmatch(science.get("frozen_candidate_sha256", "")) and science.get("held_out_opponents") and
                    metrics["primary"] == "points", "Confirmation needs frozen candidate, held-out opponents and actual points")
            require(len(arms)==2 and arms[1]["setup_sha256"]==science["frozen_candidate_sha256"], "Frozen candidate differs from confirmation setup")
    canonical(config)  # reject NaN/Infinity anywhere
    return config


def historical_seeds(data):
    used = {0}
    def visit(obj, seed_context=False):
        if isinstance(obj, dict):
            for key,value in obj.items():
                visit(value, seed_context or key in ("seed", "seeds", "validation_seeds", "effective_seed"))
        elif isinstance(obj,list):
            for value in obj:
                visit(value, seed_context)
        elif seed_context and type(obj) is int:
            used.add(obj)
    for path in Path(data).rglob("*.json*"):
        if path.suffix == ".jsonl":
            for row in rows(path):
                visit(row)
        elif path.suffix == ".json":
            visit(json.loads(path.read_text(encoding="utf8")))
    return used


def allocate(namespace, count, used):
    require(type(count) is int and 0 < count <= 100000, "Invalid seed count")
    taken, result, counter = set(used) | {0}, [], 0
    while len(result) < count:
        candidate = int.from_bytes(sha256(f"{namespace}/{counter}".encode()).digest()[:4], "little")
        counter += 1
        if candidate not in taken:
            result.append(candidate)
            taken.add(candidate)
    return result


class Registry:
    """One immutable JSON registration per ID; an exclusive lock serializes seeds."""
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def register(self, config, data):
        validate(config, executable=True)
        lock = self.directory / ".allocation.lock"
        lock.touch(exist_ok=False)
        try:
            path = self.directory / (config["experiment_id"]+".json")
            require(not path.exists(), "Experiment ID already registered")
            used = historical_seeds(data)
            for prior in self.directory.glob("*.json"):
                used.update(json.loads(prior.read_text(encoding="utf8"))["seeds"])
            if config["stage"] == "confirmation":
                prior_ids=config["science"].get("discovery_experiment_ids",[])
                require(prior_ids, "Confirmation must identify its discovery registrations")
                opponents={s["opponent"] for s in config["design"]["scenarios"]}
                seen=set()
                for ident in prior_ids:
                    require(re.fullmatch(r"[A-Z]+-\d{3}(?:-[A-Za-z0-9-]+)?",ident), "Invalid discovery ID")
                    previous=json.loads((self.directory/(ident+".json")).read_text(encoding="utf8"))["config"]
                    require(previous["stage"]=="discovery", "Source is not a discovery experiment")
                    seen.update(s["opponent"] for s in previous["design"]["scenarios"])
                require(not opponents & seen, "Held-out opponents overlap discovery")
                require(opponents==set(config["science"].get("held_out_opponents",[])), "Held-out opponent list differs")
            count = config["design"]["n_blocks"] * len(config["design"]["scenarios"])
            seed_list = allocate(config["seed_namespace"], count, used)
            receipt = dict(config=config, config_sha256=config_hash(config), seeds=seed_list)
            with path.open("x", encoding="utf8") as stream:
                stream.write(json.dumps(receipt, ensure_ascii=False, allow_nan=False, indent=2)+"\n")
            return receipt
        finally:
            lock.unlink()


def schedule(receipt):
    config = validate(receipt["config"], executable=True)
    require(receipt["config_sha256"] == config_hash(config), "Registration changed")
    require(config["kind"] == "native", "Career experiments use checkpoints, not a match schedule")
    design, seeds = config["design"], receipt["seeds"]
    n = design["n_blocks"]
    require(len(seeds) == n * len(design["scenarios"]) and len(set(seeds)) == len(seeds)
            and all(type(s) is int and 0 < s <= 0xffffffff for s in seeds), "Invalid seed reservation")
    jobs = []
    for i,scenario in enumerate(design["scenarios"]):
        for seed, side, arm in product(seeds[i*n:(i+1)*n], design["sides"], design["arms"]):
            key = f"{scenario['id']}-{seed}-{side}-{arm['id']}"
            setup=design["setups"][scenario["id"]][str(side)][arm["id"]] if "setups" in design else arm["setup_sha256"]
            jobs.append(dict(key=key, scenario=scenario["id"], seed=seed, side=side, arm=arm["id"],
                             setup_sha256=setup, config_sha256=receipt["config_sha256"],identity=config["identity"]))
    require(len(jobs) <= config["budget"]["max_matches"], "Schedule exceeds budget")
    return sorted(jobs, key=lambda j:sha256(j["key"].encode()).digest())


def check_identity(expected, actual, validation):
    require(validation.get("passed") is True, "Native validation not passed")
    require(all(actual.get(k) == expected.get(k) == validation["identity"].get(k) for k in IDENTITY_FIELDS), "Build/tool/input identity drift: new validation required")


def verify_artifacts(directory, manifest):
    root = Path(directory).resolve()
    for name, expected in manifest.items():
        path = (root / name).resolve()
        require(root in path.parents and digest(path) == expected, "Missing, escaped or changed raw artifact")
    return True

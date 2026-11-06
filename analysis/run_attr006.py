"""Validate, run and export ATTR-006 with the existing native harness."""
from argparse import ArgumentParser
from copy import deepcopy
from itertools import product
from pathlib import Path

from analyse_attr006 import ARMS, EXPERIMENT, PRIOR, checked_rows, require, seed_plan
from export_attr004 import export_rows, write_jsonl
from run_attr004 import ATTRIBUTES, IDENTITY, execute, git, initialize, negative_probe, records, save, sha
from run_attr005 import EVIDENCE, SCENARIO, baseline, encode, jobs, native_groups
from verify_matches import DATA, read


REGISTRATION = "b9cb3e628db4b10984f5c5e974b648bf2029189b"
INPUTS = ("analysis/run_attr006.py", "analysis/run_attr005.py", "analysis/run_attr004.py",
          "analysis/analyse_attr006.py", "analysis/export_attr004.py")
ARM = ARMS[1]


def check_registration():
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    for head in (remote, "HEAD"):
        git("merge-base", "--is-ancestor", REGISTRATION, head)
    for path in ("experiments/ATTR-006-vorregistrierung.md", "analysis/analyse_attr006.py"):
        require(not git("diff", REGISTRATION, "--", path), f"Registration changed: {path}")


def native_values(path):
    return {(side, player["index"], i): value
            for side, team in enumerate(read(path)["teams"])
            for player in team["players"]
            for i, value in enumerate(player["attributes"])}


def validate(args):
    check_registration()
    server, fixture = initialize(args)
    validation_seeds, main_seeds = seed_plan()
    previous = PRIOR["scenarios"][SCENARIO]
    scenario = dict(previous, setups={})
    setups = scenario["setups"]
    manifest = dict(**IDENTITY, experiment_id=EXPERIMENT, preregistration_commit=REGISTRATION,
                    **{key: PRIOR[key] for key in ("lab_release", "lab_commit", "adapter_source_sha256",
                                                  "resource_fingerprint", "mode", "worker_cap", "timeout_seconds")},
                    seeds=main_seeds, validation_seeds=validation_seeds, scenarios={SCENARIO: scenario},
                    code_sha256={f: sha(DATA.parent / f) for f in INPUTS})
    configs = {}
    config = baseline(server)
    setups["baseline"] = encode(server, args.local, configs, config, "baseline")
    require(setups["baseline"] == previous["setups"]["baseline"], "Baseline differs from ATTR-005")
    base_dir = args.local / "baseline-checks"
    baseline_rows = execute(base_dir, server, manifest, jobs(configs, fixture, validation_seeds, 2))
    groups = native_groups(base_dir, baseline_rows, config, server)
    require(groups == PRIOR["native_position_groups"], "Native lineup differs from ATTR-005")
    manifest["native_position_groups"] = groups

    treated = deepcopy(config)
    index = ATTRIBUTES["JumpingReach"]
    slots = [p["roster_slot"] for p in groups["FW"].values()]
    require(len(set(slots)) == 3, "Expected exactly three native forward slots")
    for slot in slots:
        attrs = treated["teams"][0]["players"][slot]["attributes"]
        require(attrs[index] == 60, "Unexpected baseline JumpingReach")
        attrs[index] = 80
    setups[ARM] = encode(server, args.local, configs, treated, ARM)
    require(setups[ARM] == previous["setups"][ARM], "Intervention differs from ATTR-005")
    first, other_first = records(configs["baseline"][1])
    second, other_second = records(configs[ARM][1])
    targets = {(0, slot, index) for slot in slots}
    require(first.keys() == second.keys() and other_first == other_second
            and {k for k in first if first[k] != second[k]} == {(1, *k) for k in targets}
            and all(first[1, *k] == 60 and second[1, *k] == 80 for k in targets),
            "The binary inputs differ outside the three registered changes")
    path = args.local / "manifest.json"
    if path.exists():
        require(read(path) == manifest, "Stored manifest changed")
    else:
        save(path, manifest)

    treatment_dir = args.local / "intervention-checks"
    treatment_rows = execute(treatment_dir, server, manifest,
                             jobs({ARM: configs[ARM]}, fixture, validation_seeds, 2))
    comparisons = []
    for arm, rows in (("baseline", baseline_rows), (ARM, treatment_rows)):
        for seed in validation_seeds:
            first, second = (rows[f"{SCENARIO}-{seed}-{arm}-r{repeat}"] for repeat in (0, 1))
            exact = {field: first[field] == second[field] for field in EVIDENCE}
            require(all(exact.values()), f"Nonrepeatable validation match: {arm}/{seed}")
            comparisons.append(dict(arm=arm, seed=seed, exact=exact))
    for seed, repeat in product(validation_seeds, (0, 1)):
        a = baseline_rows[f"{SCENARIO}-{seed}-baseline-r{repeat}"]
        b = treatment_rows[f"{SCENARIO}-{seed}-{ARM}-r{repeat}"]
        first, second = native_values(base_dir / a["dump"]), native_values(treatment_dir / b["dump"])
        require(first.keys() == second.keys() and {k for k in first if first[k] != second[k]} == targets
                and all(first[k] == 60 and second[k] == 80 for k in targets),
                "The native attribute readback differs outside the three registered changes")
    probe = negative_probe(args.local / "negative", fixture, validation_seeds[0])
    summary = dict(passed=True, matches=8, native_forward_positions=groups["FW"],
                   paired_native_comparisons=4, native_attribute_changes_per_comparison=3,
                   repeat_comparisons=comparisons, negative_probe=probe)
    save(args.local / "validation-summary.json", summary)
    print("Native gate passed: eight matches, four exact repetitions, three attribute changes per readback.", flush=True)
    return server, fixture, manifest, configs


def publish(local, validation_only):
    manifest = read(local / "manifest.json")
    summary = read(local / "validation-summary.json")
    require(summary["passed"] and summary["negative_probe"]["passed"]
            and manifest["preregistration_commit"] == REGISTRATION, "Missing technical release")
    for file, digest in manifest["code_sha256"].items():
        require(sha(DATA.parent / file) == digest, f"Executed code differs: {file}")

    destination = DATA / "attr-006"
    destination.mkdir(exist_ok=True)
    validation, failed = {}, []
    for arm, directory in zip(ARMS, ("baseline-checks", "intervention-checks"), strict=True):
        keys = set(product((SCENARIO,), manifest["validation_seeds"], (arm,), (0, 1)))
        rows, failures = export_rows(local / directory, keys, manifest)
        validation.update(rows)
        failed.extend(failures)
    require(len(validation) == summary["matches"] == 8, "Wrong validation count")
    for key in validation:
        if key[-1] == 0:
            require(all(validation[key][f] == validation[(*key[:-1], 1)][f] for f in EVIDENCE),
                    f"Nonrepeatable validation match: {key}")
    save(destination / "validation-summary.json", summary)
    write_jsonl(destination / "validation.jsonl", [validation[k] for k in sorted(validation)])
    if failed:
        write_jsonl(destination / "validation-failures.jsonl", failed)
    counts = dict(validation_matches=len(validation), validation_failed_attempts=len(failed))
    if not validation_only:
        keys = set(product((SCENARIO,), manifest["seeds"], ARMS, (0,)))
        accepted, failures = export_rows(local / "main", keys, manifest)
        rows = [accepted[k] for k in sorted(accepted)]
        checked_rows(rows, manifest)
        write_jsonl(destination / "matches.jsonl", rows)
        if failures:
            write_jsonl(destination / "failures.jsonl", failures)
        counts.update(matches=len(accepted), failed_attempts=len(failures), not_run=0, excluded_pairs=0)
    save(destination / "manifest.json", dict(manifest, publication_counts=counts))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("validate", "main", "publish-validation", "publish"))
    parser.add_argument("--local", type=Path, required=True)
    for name in ("lab", "game", "player-log"):
        parser.add_argument("--" + name, type=Path)
    args = parser.parse_args()
    args.local = args.local.resolve()
    require(args.local.is_dir() and DATA.parent not in args.local.parents and args.local != DATA.parent,
            "Use a local artifact directory outside the Git checkout")
    if args.phase.startswith("publish"):
        publish(args.local, validation_only=args.phase == "publish-validation")
        return
    for name in ("lab", "game", "player_log"):
        path = getattr(args, name)
        require(path is not None, f"Missing native run argument: {name}")
        setattr(args, name, path.resolve())
    server, fixture, manifest, configs = validate(args)
    if args.phase == "main":
        execute(args.local / "main", server, manifest, jobs(configs, fixture, manifest["seeds"], 1))


if __name__ == "__main__":
    main()

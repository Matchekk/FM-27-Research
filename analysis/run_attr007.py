"""Native validation, simulation and public export for the ATTR-007 factorial."""
from argparse import ArgumentParser
from copy import deepcopy
from itertools import product
from pathlib import Path

from analyse_attr007 import ARM_BITS, EXPERIMENT, POSITIONS, PRIOR, checked_rows, require, seed_plan
from export_attr004 import export_rows, write_jsonl
from run_attr004 import ATTRIBUTES, IDENTITY, execute, git, initialize, negative_probe, records, save, sha
from run_attr005 import EVIDENCE, SCENARIO, baseline, encode, jobs, native_groups
from run_attr006 import native_values
from verify_matches import DATA, read, read_rows


REGISTRATION = "9ceaf95e58b68a7e37c7f138b4274ad0563d240d"
CODE = ("run_attr007", "run_attr006", "run_attr005", "run_attr004", "export_attr004",
        "analyse_attr007", "analyse_attr006", "analyse_attr005", "analyse_attr004", "verify_matches")


def check_registration():
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    for head in (remote, "HEAD"):
        git("merge-base", "--is-ancestor", REGISTRATION, head)
    for path in ("experiments/ATTR-007-vorregistrierung.md", "analysis/analyse_attr007.py"):
        require(not git("diff", REGISTRATION, "--", path), f"Registration changed: {path}")


def variant(server, folder, configs, base, arm, target_slots):
    index = ATTRIBUTES["JumpingReach"]
    changed = deepcopy(base)
    for slot in target_slots:
        values = changed["teams"][0]["players"][slot]["attributes"]
        require(values[index] == 60, "Unexpected baseline attribute")
        values[index] = 80
    digest = encode(server, folder, configs, changed, arm)
    a, other_a = records(configs["baseline"][1])
    b, other_b = records(configs[arm][1])
    expected = {(1, 0, slot, index) for slot in target_slots}
    require(other_a == other_b and a.keys() == b.keys() and {k for k in a if a[k] != b[k]} == expected
            and all(a[k] == 60 and b[k] == 80 for k in expected), f"Unexpected binary changes: {arm}")
    return digest


def phase_config(path):
    entries = [r for r in read_rows(path) if r.get("event") == "native_phase_configuration"]
    config = {(e["side"], e["phase"]): e for e in entries}
    require(len(entries) == 4 and config.keys() == set(product((0, 1), repeat=2)),
            "Missing or duplicate native team phase")
    return config


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
                    arm_positions={arm: [p for i, p in enumerate(POSITIONS) if bits & (1 << i)]
                                   for arm, bits in ARM_BITS.items()},
                    code_sha256={f"analysis/{name}.py": sha(DATA.parent / "analysis" / f"{name}.py") for name in CODE})
    configs = {}
    base = baseline(server)
    setups["baseline"] = encode(server, args.local, configs, base, "baseline")
    require(setups["baseline"] == previous["setups"]["baseline"], "Baseline differs from ATTR-006")
    base_dir = args.local / "baseline-checks"
    baseline_rows = execute(base_dir, server, manifest, jobs(configs, fixture, validation_seeds, 2))
    groups = native_groups(base_dir, baseline_rows, base, server)
    require(groups == PRIOR["native_position_groups"], "Native lineup differs from ATTR-006")
    manifest["native_position_groups"] = groups

    slots = {arm: [groups["FW"][p]["roster_slot"] for p in positions]
             for arm, positions in manifest["arm_positions"].items()}
    require(len(set(slots["ALL"])) == 3, "Expected three distinct forward slots")
    for arm in tuple(ARM_BITS)[1:]:
        setups[arm] = variant(server, args.local, configs, base, arm, slots[arm])
    require(setups["ALL"] == previous["setups"]["FW-JumpingReach"], "ALL differs from ATTR-006")
    path = args.local / "manifest.json"
    if path.exists():
        require(read(path) == manifest, "Stored manifest changed")
    else:
        save(path, manifest)

    treatment_dir = args.local / "intervention-checks"
    treatment_rows = execute(treatment_dir, server, manifest,
                             jobs({arm: configs[arm] for arm in tuple(ARM_BITS)[1:]}, fixture, validation_seeds, 2))
    observed = {(r["arm"], r["seed"], r["repeat"]): (folder, r)
                for folder, rows in ((base_dir, baseline_rows), (treatment_dir, treatment_rows))
                for r in rows.values()}
    comparisons = []
    for arm, seed in product(ARM_BITS, validation_seeds):
        a, b = (observed[arm, seed, repeat][1] for repeat in (0, 1))
        exact = {field: a[field] == b[field] for field in EVIDENCE}
        require(all(exact.values()), f"Nonrepeatable validation match: {arm}/{seed}")
        comparisons.append(dict(arm=arm, seed=seed, exact=exact))
    for seed, repeat in product(validation_seeds, (0, 1)):
        folder, a = observed["baseline", seed, repeat]
        a_values = native_values(folder / a["dump"])
        phase = phase_config(folder / a["log"])
        for arm in tuple(ARM_BITS)[1:]:
            folder, b = observed[arm, seed, repeat]
            b_values = native_values(folder / b["dump"])
            targets = {(0, slot, ATTRIBUTES["JumpingReach"]) for slot in slots[arm]}
            require(a_values.keys() == b_values.keys()
                    and {k for k in a_values if a_values[k] != b_values[k]} == targets
                    and all(a_values[k] == 60 and b_values[k] == 80 for k in targets),
                    f"Unexpected native attributes: {arm}/{seed}/{repeat}")
            require(phase_config(folder / b["log"]) == phase, f"Native phase mismatch: {arm}/{seed}/{repeat}")
    probe = negative_probe(args.local / "negative", fixture, validation_seeds[0])
    summary = dict(passed=True, matches=len(observed), native_forward_positions=groups["FW"],
                   paired_native_comparisons=28, native_attribute_changes_per_arm={k: len(v) for k, v in slots.items()},
                   both_teams_native_phase_configurations_identical=True, binary_input_differences_verified=True,
                   repeat_comparisons=comparisons, negative_probe=probe)
    save(args.local / "validation-summary.json", summary)
    print("Native gate passed: 32 matches, 16 exact repetitions and 28 paired native readbacks.", flush=True)
    return server, fixture, manifest, configs


def publish(local, validation_only):
    manifest = read(local / "manifest.json")
    summary = read(local / "validation-summary.json")
    require(summary["passed"] and summary["negative_probe"]["passed"]
            and manifest["preregistration_commit"] == REGISTRATION, "Missing technical release")
    for file, digest in manifest["code_sha256"].items():
        require(sha(DATA.parent / file) == digest, f"Executed code differs: {file}")
    destination = DATA / "attr-007"
    destination.mkdir(exist_ok=True)
    validation, failed = {}, []
    for arms, directory in ((("baseline",), "baseline-checks"), (tuple(ARM_BITS)[1:], "intervention-checks")):
        keys = set(product((SCENARIO,), manifest["validation_seeds"], arms, (0, 1)))
        rows, failures = export_rows(local / directory, keys, manifest)
        validation.update(rows)
        failed.extend(failures)
    require(len(validation) == summary["matches"] == 32, "Wrong validation count")
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
        keys = set(product((SCENARIO,), manifest["seeds"], ARM_BITS, (0,)))
        accepted, failures = export_rows(local / "main", keys, manifest)
        rows = [accepted[k] for k in sorted(accepted)]
        checked_rows(rows, manifest)
        write_jsonl(destination / "matches.jsonl", rows)
        if failures:
            write_jsonl(destination / "failures.jsonl", failures)
        counts.update(matches=len(accepted), failed_attempts=len(failures), not_run=0, excluded_seed_blocks=0)
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

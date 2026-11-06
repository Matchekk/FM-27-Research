"""Run ATTR-005 with the validated native match host and archive allowed fields."""
from argparse import ArgumentParser
from copy import deepcopy
from hashlib import sha256
from itertools import product
from pathlib import Path

from analyse_attr005 import ARMS, ATTRIBUTES, GROUPS, SCENARIO, checked_rows, require, seed_plan
from export_attr004 import export_rows, write_jsonl
from run_attr004 import (
    ATTRIBUTES as LAB_ATTRIBUTES, IDENTITY, REFERENCE, execute, git, initialize,
    negative_probe, one, records, save, sha,
)
from verify_matches import DATA, read, read_rows


EXPERIMENT = "ATTR-005"
REGISTRATION = "41460cc49e4d0a19eb27f8565d163d4eb39eead3"
PRIOR = read(DATA / "attr-004/manifest.json")
EVIDENCE = ("score", "team_statistics", "finish_tick")


def check_registration():
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    for head in (remote, "HEAD"):
        git("merge-base", "--is-ancestor", REGISTRATION, head)
    for path in ("experiments/ATTR-005-position-screening.md", "analysis/analyse_attr005.py"):
        require(not git("diff", REGISTRATION, "--", path), f"Registration changed: {path}")


def baseline(server):
    config = deepcopy(server.DEFAULT)
    home, away = config["teams"]
    require([len(t["players"]) for t in (home, away)] == [23, 26]
            and [t["mentality"] for t in (home, away)] == [4, 4], "Standard fixture changed")
    for t in (home, away):
        t["roster_size"] = len(t["players"])
    outfield = [index for index, cell in zip(home["lineup"], home["phases"][0], strict=True)
                if cell["position"] != "GK"]
    require(len(set(outfield)) == 10, "Expected exactly ten field players")
    for index in outfield:
        for field in LAB_ATTRIBUTES.values():
            home["players"][index]["attributes"][field] = 60
    return server.validate_scenario(config)


def encode(server, folder, configs, data, arm):
    blob = server.encode_scenario(data, absolute=True)
    path = folder / f"{arm}.bin"
    if path.exists():
        require(path.read_bytes() == blob, f"Stored setup changed: {arm}")
    else:
        path.write_bytes(blob)
    configs[arm] = (data, blob, path)
    return sha256(blob).hexdigest()


def jobs(configs, fixture, seeds, repeats):
    for arm, seed, repeat in product(configs, seeds, range(repeats)):
        data, blob, path = configs[arm]
        attr, other = records(blob)
        yield dict(variant=f"{SCENARIO}-{seed}-{arm}-r{repeat}", seed=seed, config=path,
                   fixture=fixture, event_details=False, scenario=data, arm=arm, s=SCENARIO,
                   repeat=repeat, side=0, records=len(attr) + len(other),
                   profile_fields=sum(r[0] == 15 for r in other))


def native_groups(folder, rows, baseline_data, server):
    home = baseline_data["teams"][0]
    masks = {entry["mask"]: entry["id"] for entry in server.POSITIONS.values()}
    slot_by_identity = {player["native_id"]: i for i, player in enumerate(home["players"])}
    observed = []
    for row in rows.values():
        phase_events = [e for e in read_rows(folder / row["log"])
                        if e.get("side") == 0 and e.get("phase") == 0]
        phase = one(phase_events, "native_phase_configuration")
        starters = read(folder / row["dump"])["teams"][0]["players"][:11]
        layout = {}
        for logged, player in zip(phase["players"], starters, strict=True):
            starter = player["index"]
            position = masks[logged["position"]]
            slot = slot_by_identity[player["id"]]
            expected = home["phases"][0][starter]
            require(logged["slot"] == starter and home["lineup"][starter] == slot
                    and position == expected["position"] and position not in layout,
                    "Native lineup or position does not match the baseline")
            layout[position] = dict(start_slot=starter, roster_slot=slot, role=expected["role"],
                                    native_role=logged["role"])
        require(set(layout) == {"GK", *(p for group in GROUPS.values() for p in group)},
                "Expected a native 4-3-3 formation")
        observed.append(layout)
    require(len(observed) == 4 and all(x == observed[0] for x in observed), "Native position map changed")
    return {group: {p: observed[0][p] for p in positions} for group, positions in GROUPS.items()}


def treatments(server, folder, config, groups, configs, setups):
    first, nonattr = records(configs["baseline"][1])
    for group, attribute in product(groups, ATTRIBUTES):
        arm = f"{group}-{attribute}"
        index = LAB_ATTRIBUTES[attribute]
        slots = [p["roster_slot"] for p in groups[group].values()]
        data = deepcopy(config)
        for slot in slots:
            attrs = data["teams"][0]["players"][slot]["attributes"]
            require(attrs[index] == 60, f"Unexpected baseline value: {arm}")
            attrs[index] = 80
        setups[arm] = encode(server, folder, configs, data, arm)
        changed, other = records(configs[arm][1])
        targets = {(1, 0, slot, index) for slot in slots}
        require(first.keys() == changed.keys() and nonattr == other
                and {key for key in first if first[key] != changed[key]} == targets
                and all(first[k] == 60 and changed[k] == 80 for k in targets), f"Invalid delta: {arm}")


def prepare(args):
    check_registration()
    server, fixture = initialize(args)
    validation, seeds = seed_plan()
    manifest = dict(**IDENTITY, experiment_id=EXPERIMENT, preregistration_commit=REGISTRATION,
                    lab_release=REFERENCE["lab_release"], lab_commit=REFERENCE["lab_commit"],
                    adapter_source_sha256=REFERENCE["adapter_source_sha256"],
                    resource_fingerprint=PRIOR["resource_fingerprint"],
                    validation_seeds=validation, seeds=seeds, mode="quick", worker_cap=4,
                    timeout_seconds=90, scenarios={SCENARIO: dict(
                        formation="433", opponent_formation="4231", mentalities=[4, 4],
                        tested_side=0, active_rosters=[23, 26], setups={})},
                    code_sha256={f: sha(DATA.parent / f) for f in (
                        "analysis/run_attr005.py", "analysis/run_attr004.py", "analysis/analyse_attr005.py")})
    config, configs = baseline(server), {}
    setups = manifest["scenarios"][SCENARIO]["setups"]
    setups["baseline"] = encode(server, args.local, configs, config, "baseline")
    base_dir = args.local / "baseline-checks"
    base = execute(base_dir, server, manifest, jobs(configs, fixture, validation, 2))
    groups = native_groups(base_dir, base, config, server)
    manifest["native_position_groups"] = groups
    treatments(server, args.local, config, groups, configs, setups)
    manifest_path = args.local / "manifest.json"
    if manifest_path.exists():
        require(read(manifest_path) == manifest, "Stored manifest changed")
    else:
        save(manifest_path, manifest)

    remaining = {arm: c for arm, c in configs.items() if arm != "baseline"}
    intervention = execute(args.local / "intervention-checks", server, manifest,
                           jobs(remaining, fixture, validation, 2))
    observed = {(r["arm"], r["seed"], r["repeat"]): r for r in (*base.values(), *intervention.values())}
    comparisons = []
    for arm, seed in product(ARMS, validation):
        a, b = (observed[arm, seed, repeat] for repeat in (0, 1))
        exact = {f: a[f] == b[f] for f in EVIDENCE}
        require(all(exact.values()), f"Nonrepeatable native match: {arm}/{seed}")
        comparisons.append(dict(arm=arm, seed=seed, exact=exact))
    negative = negative_probe(args.local / "negative", fixture, validation[0])
    summary = dict(passed=True, matches=len(observed), native_position_groups=groups,
                   native_position_readback_matches=len(base), verified_attribute_and_profile_readbacks=len(observed),
                   repeat_comparisons=comparisons, negative_probe=negative)
    save(args.local / "validation-summary.json", summary)
    print("Native quality gate passed: 36 matches, 18 exact repetitions, invalid input rejected.", flush=True)
    return server, fixture, manifest, configs


def publish(local, validation_only):
    manifest = read(local / "manifest.json")
    summary = read(local / "validation-summary.json")
    require(summary["passed"] and summary["negative_probe"]["passed"]
            and manifest["preregistration_commit"] == REGISTRATION, "Missing technical release")
    for file, digest in manifest["code_sha256"].items():
        require(sha(DATA.parent / file) == digest, f"Executed code differs: {file}")

    def expected(arms, seeds, repeats):
        return set(product((SCENARIO,), seeds, arms, range(repeats)))

    checks, seeds = manifest["validation_seeds"], manifest["seeds"]
    baseline_runs, baseline_failures = export_rows(local / "baseline-checks",
                                                   expected(("baseline",), checks, 2), manifest)
    treatment_runs, treatment_failures = export_rows(local / "intervention-checks",
                                                     expected(ARMS[1:], checks, 2), manifest)
    validation = baseline_runs | treatment_runs
    for key, row in validation.items():
        if key[-1] == 0:
            require(all(row[f] == validation[(*key[:-1], 1)][f] for f in EVIDENCE),
                    f"Nonrepeatable validation match: {key}")
    require(len(validation) == summary["matches"] == 36, "Wrong technical count")
    failure_checks = baseline_failures + treatment_failures
    counts = dict(validation_matches=len(validation), validation_failed_attempts=len(failure_checks))
    destination = DATA / "attr-005"
    destination.mkdir(exist_ok=True)
    save(destination / "validation-summary.json", summary)
    write_jsonl(destination / "validation.jsonl", [validation[k] for k in sorted(validation)])
    if failure_checks:
        write_jsonl(destination / "validation-failures.jsonl", failure_checks)
    if not validation_only:
        main, failures = export_rows(local / "main", expected(ARMS, seeds, 1), manifest)
        rows = [main[k] for k in sorted(main)]
        checked_rows(rows, manifest)
        write_jsonl(destination / "matches.jsonl", rows)
        if failures:
            write_jsonl(destination / "failures.jsonl", failures)
        counts.update(matches=len(main), failed_attempts=len(failures), not_run=0, excluded_seed_blocks=0)
    save(destination / "manifest.json", dict(manifest, publication_counts=counts))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("validate", "main", "publish-validation", "publish"))
    path = lambda p: Path(p).resolve()
    parser.add_argument("--local", type=path, required=True)
    for name in ("lab", "game", "player-log"):
        parser.add_argument("--" + name, type=path)
    args = parser.parse_args()
    require(args.local.is_dir() and DATA.parent not in args.local.parents and args.local != DATA.parent,
            "Use an existing local artifact directory outside the Git checkout")
    if args.phase.startswith("publish"):
        publish(args.local, validation_only=args.phase == "publish-validation")
        return
    require(all((args.lab, args.game, args.player_log)), "Native run requires lab, game and player log")
    server, fixture, manifest, configs = prepare(args)
    if args.phase == "main":
        execute(args.local / "main", server, manifest, jobs(configs, fixture, manifest["seeds"], 1))


if __name__ == "__main__":
    main()

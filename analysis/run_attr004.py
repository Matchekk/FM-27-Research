"""Run ATTR-004 with the pinned local FM27 Tactics Lab host; keep native assets local."""
from argparse import ArgumentParser
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
from hashlib import file_digest, sha256
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

from analyse_attr004 import ARMS, BUILD, SCENARIOS, require, seed_plan
from verify_matches import DATA, match_metrics, read, read_rows


REGISTRATION = "ccfd6300ccaccb6aa6766b178fda973196c9891e"
REFERENCE = read(DATA / "matches/manifest.json")
ATTRIBUTES = REFERENCE["attributes"]
IDENTITY = {k: REFERENCE[k] for k in ("build", "engine_sha256", "adapter_version",
                                      "adapter_host_sha256", "fixture_sha256")}
STATS = ("xg", "shots", "shots_on_target", "passes", "completed_passes", "possession", "possession_ticks")


def sha(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=DATA.parent, text=True).strip()


def check_registration():
    # The registered version must already be reachable from the GitHub main branch.
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    for descendant in (remote, "HEAD"):
        git("merge-base", "--is-ancestor", REGISTRATION, descendant)
    for path in ("analysis/analyse_attr004.py", "experiments/ATTR-004-cross-tactic.md"):
        require(not git("diff", REGISTRATION, "--", path), f"Registration changed: {path}")


def initialize(args):
    native = args.lab / "private/engine/fm27_native"
    dll = args.game / "fm_Data/Plugins/x86_64/game_plugin.dll"
    host, fixture = native / "FM27Simulator.exe", native / "fixtures/match.pkm"
    require(any("Football Manager 27 plugin version: " + BUILD in row.get("Message", "")
                for line in args.player_log.read_text(encoding="utf8", errors="replace").splitlines()
                if line.startswith('{"Timestamp"') for row in [json.loads(line)]),
            "FM27 runtime version not confirmed by the game startup log")
    for key, path in zip(("engine_sha256", "adapter_host_sha256", "fixture_sha256"), (dll, host, fixture)):
        require(sha(path) == IDENTITY[key], f"Unregistered native component: {key}")
    for key, digest in REFERENCE["adapter_source_sha256"].items():
        require(sha(args.lab / key) == digest, f"Unregistered Lab source: {key}")
    require(git_lab(args.lab) == REFERENCE["lab_commit"], "Unregistered Lab base commit")
    for name in list(os.environ):
        if name.startswith("FM27_"):
            del os.environ[name]
    os.environ.update(FM27_ENGINE_ROOT=str(native.parent), FM27_GAME_ROOT=str(args.game),
                      FM27_DESKTOP_DATA=str(args.local / "lab-data"))
    sys.path.insert(0, str(args.lab / "src"))
    import fm27_tactics_server as server

    status = server.ENGINE_COMPATIBILITY
    require(status["compatible"] and status["original_build_verified"]
            and status["profile"] == IDENTITY["adapter_version"]
            and status["resource_fingerprint"] == REFERENCE["compatibility"]["resource_fingerprint"],
            "Pinned Lab compatibility gate failed")
    return server, fixture


def git_lab(lab):
    return subprocess.check_output(["git", "-C", str(lab), "rev-parse", "HEAD"], text=True).strip()


def setup(server, scenario, arm):
    formation, mentality, tested = SCENARIOS[int(scenario)]
    teams = deepcopy(server.DEFAULT["teams"])
    if formation == "4231":
        cells = {c["position"]: c for c in teams[1]["phases"][0]}
        teams[0]["phases"][0][5:8] = [deepcopy(cells[p]) for p in ("DMR", "DML", "AMC")]
    teams[1]["mentality"] = mentality
    for player in teams[0]["players"][1:11]:
        for name, index in ATTRIBUTES.items():
            player["attributes"][index] = 80 if name == arm else 60
    if tested:
        teams.reverse()
    for team, destination in zip(teams, server.DEFAULT["teams"], strict=True):
        team["roster_size"] = 23
        team["players"][23:] = deepcopy(destination["players"][23:])
        for player, target in zip(team["players"], destination["players"], strict=True):
            player["native_id"] = target["native_id"]
        size = len(destination["opposition"]["players"])
        team["opposition"]["players"][23:] = deepcopy(destination["opposition"]["players"][23:size])
    scenario = dict(server.DEFAULT, teams=teams)
    return server.validate_scenario(scenario)


def records(blob):
    require(blob[:8] == b"FM27CFG1", "Unexpected native input format")
    entries = list(struct.iter_unpack("<5I", blob[12:]))
    require(len(entries) == struct.unpack_from("<I", blob, 8)[0], "Invalid input record count")
    attributes = {tuple(row[:4]): row[4] for row in entries if row[0] == 1}
    other = [row for row in entries if row[0] != 1]
    return attributes, other


def compare_arms(baseline, treatment, side, arm):
    attr_a, other_a = records(baseline)
    attr_b, other_b = records(treatment)
    expected = {(1, side, i, ATTRIBUTES[arm]) for i in range(1, 11)}
    changed = {k for k in attr_a.keys() | attr_b.keys() if attr_a.get(k) != attr_b.get(k)}
    require(changed == expected and other_a == other_b
            and all(attr_a[k] == 60 and attr_b[k] == 80 for k in expected), "Invalid arm input difference")


def active_team(team):
    active = deepcopy(team)
    active["players"] = active["players"][:23]
    active["opposition"]["players"] = active["opposition"]["players"][:23]
    for player in active["players"]:
        player.pop("native_id")
    return active


def save(path, obj):
    text = json.dumps(obj, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf8")
    temporary.replace(path)


def prepare(server, folder):
    validation_seeds, seeds = seed_plan()
    configs, scenarios = {}, {}
    for s in seeds:
        formation, mentality, tested = SCENARIOS[int(s)]
        scenarios[s] = dict(formation=formation, opponent_mentality=mentality, tested_side=tested, setups={})
        for arm in ARMS:
            data = setup(server, s, arm)
            # Encode the complete active roster and all explicit tactic/lineup fields.
            blob = server.encode_scenario(data, absolute=True)
            if arm != "baseline":
                compare_arms(configs[s, "baseline"]["blob"], blob, tested, arm)
            path = folder / f"{s}-{arm}.bin"
            if path.exists():
                require(path.read_bytes() == blob, f"Setup changed: {s}/{arm}")
            else:
                path.write_bytes(blob)
            configs[s, arm] = dict(data=data, blob=blob, path=path)
            scenarios[s]["setups"][arm] = sha256(blob).hexdigest()
            if tested:
                home = configs[str(int(s) - 1), arm]["data"]["teams"]
                away = data["teams"]
                require(all(active_team(a) == active_team(b) for a, b in zip(home, reversed(away))),
                        f"Venue profile/role transfer mismatch: {s}/{arm}")
    manifest = dict(**IDENTITY, preregistration_commit=REGISTRATION, experiment_id="ATTR-004",
                    lab_release=REFERENCE["lab_release"], lab_commit=REFERENCE["lab_commit"],
                    resource_fingerprint=REFERENCE["compatibility"]["resource_fingerprint"],
                    adapter_source_sha256=REFERENCE["adapter_source_sha256"], validation_seeds=validation_seeds,
                    seeds=seeds, scenarios=scenarios, mode="quick", worker_cap=4, timeout_seconds=90)
    path = folder / "manifest.json"
    if path.exists():
        require(read(path) == manifest, "Local manifest changed")
    else:
        save(path, manifest)
    return manifest, configs


def one(rows, event):
    found = [row for row in rows if row.get("event") == event]
    require(len(found) == 1, f"Missing or duplicate native event: {event}")
    return found[0]


def audit_dump(path, data, server):
    teams = read(path)["teams"]
    for side, (actual, expected) in enumerate(zip(teams, data["teams"], strict=True)):
        players = [(p["id"], p["attributes"]) for p in actual["players"]]
        count = expected.get("roster_size", len(expected["players"]))
        wanted = [(p["native_id"], p["attributes"]) for p in expected["players"][:count]]
        require(actual["side"] == side and actual["count"] == count and players == wanted,
                f"Native roster, start order or attributes differ: side {side}")
        require(bytes.fromhex(actual["creator_hex"])[0x25] == expected["mentality"],
                f"Native mentality mismatch: side {side}")
        for phase, cells in enumerate(expected["phases"]):
            for i, cell in enumerate(cells):
                slot = server.OOP_MAP[side][i] if phase else i
                raw = bytes.fromhex(actual["tactical_slots"][phase][slot])
                require(struct.unpack_from("<I", raw)[0] == server.POSITIONS[cell["position"]]["mask"]
                        and struct.unpack_from("<Q", raw, 64)[0] ==
                        int(server.ROLES[cell["role"]]["flags"]) | int(cell["duty"]),
                        f"Native position/role/duty mismatch: side {side}, phase {phase}, slot {i}")


def audit_match(result, job, server):
    from desktop_warm_batch import inspect_saved_run

    log = job["path"].parent / result["log"]
    require(result["verified"] and result["collector_sha256"] == IDENTITY["adapter_host_sha256"]
            and result["engine_dll_sha256"] == IDENTITY["engine_sha256"]
            and result["engine_compatibility"]["compatible"], "Native provenance mismatch")
    checked = inspect_saved_run(log.parent, result)
    require(checked["seed"]["override"] and checked["seed"]["effective_seed"] == job["seed"],
            "Effective seed mismatch")
    rows = read_rows(log)
    readback = one(rows, "native_scenario_readback_verified")
    require(readback["after_original_preparation"] and readback["records"] == job["records"],
            "Native input readback differs from encoded setup")
    require(one(rows, "native_profile_bindings_verified")["fields"] == job["profile_fields"],
            "Native profile readback count mismatch")
    require(one(rows, "native_player_tactic_bindings_verified")["players"] == 22,
            "Native player-tactic binding mismatch")
    audit_dump(job["dump"], job["scenario"], server)
    stats = one(rows, "native_match_statistics")
    require(stats["source"] == "original_team_statistics" and [t["side"] for t in stats["teams"]] == [0, 1],
            "Missing original team statistics in home/away order")
    accepted = dict(status="ok", engine_readback=True, raw_log_sha256=sha(log),
                    input_dump_sha256=sha(job["dump"]), startup_receipt_sha256=result["startup_receipt_sha256"],
                    score=checked["result"]["score"], finish_tick=checked["result"]["tick"],
                    team_statistics=[{k: t[k] for k in STATS} for t in stats["teams"]])
    require(0 < accepted["finish_tick"] < 47996, "Invalid natural finish tick")
    match_metrics(dict(accepted, tested_side=job["side"]))
    return accepted


def plan_jobs(manifest, configs, fixture, phase):
    for s, seeds in manifest["seeds"].items():
        for seed in (seeds if phase == "main" else manifest["validation_seeds"]):
            for arm in ARMS:
                cfg = configs[s, arm]
                for repeat in range(1 if phase == "main" else 2):
                    key = f"{s}-{seed}-{arm}-r{repeat}"
                    yield dict(variant=key, seed=seed, config=cfg["path"], fixture=fixture,
                               event_details=False, scenario=cfg["data"], arm=arm, s=s, repeat=repeat,
                               side=SCENARIOS[int(s)][2], records=struct.unpack_from("<I", cfg["blob"], 8)[0],
                               profile_fields=sum(row[0] == 15 for row in records(cfg["blob"])[1]))


def append(stream, row):
    stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n")
    stream.flush()
    os.fsync(stream.fileno())


def execute(folder, server, manifest, jobs):
    from desktop_warm_batch import DesktopWarmRunner
    from fm27_batch import worker_limits

    folder.mkdir(exist_ok=True)
    ledger = folder / "ledger.jsonl"
    jobs = sorted(jobs, key=lambda j: sha256(f"{manifest['experiment_id']}/order/{j['variant']}".encode()).digest())
    by_key = {j["variant"]: j for j in jobs}
    require(len(by_key) == len(jobs), "Duplicate planned key")
    prior = read_rows(ledger) if ledger.exists() else []
    attempts = Counter()
    accepted = {}
    for row in prior:
        j = by_key[row["key"]]
        attempts[row["key"]] += 1
        require(attempts[row["key"]] == row["attempt"] and row["attempt"] <= 2
                and row["setup_sha256"] == manifest["scenarios"][j["s"]]["setups"][j["arm"]]
                and all(row[k] == v for k, v in IDENTITY.items()), "Resume provenance failed")
        if row["status"] == "ok":
            require(row["key"] not in accepted and sha(folder / row["log"]) == row["raw_log_sha256"]
                    and sha(folder / row["dump"]) == row["input_dump_sha256"]
                    and sha(folder / row["receipt"]) == row["startup_receipt_sha256"], "Resume proof changed")
            accepted[row["key"]] = row
        else:
            require(row["retryable"], "Unresolved integrity failure in ledger")

    while True:
        pending = [j.copy() for j in jobs if j["variant"] not in accepted and attempts[j["variant"]] < 2]
        if not pending:
            break
        batch = {j["variant"]: j for j in pending}
        for key, j in batch.items():
            attempt = attempts[key] + 1
            j.update(path=folder / f"{key}-a{attempt}.jsonl", dump=folder / f"{key}-a{attempt}.input.json")
            require(not j["path"].exists() and not j["dump"].exists(), f"Unreconciled prior attempt: {key}")
        runner = DesktopWarmRunner(Path(os.environ["FM27_ENGINE_ROOT"]), workers=worker_limits()["maximum"],
                                   retries=0, timeout=90)
        reported = set()
        integrity_failures = []
        with ledger.open("a", encoding="utf8") as stream:
            def callback(result):
                key = result["variant"]
                j = batch[key]
                if key in reported:
                    return
                attempts[key] += 1
                setups = manifest["scenarios"][j["s"]]["setups"]
                row = dict(**IDENTITY, key=key, attempt=attempts[key], scenario=j["s"], seed=j["seed"],
                           arm=j["arm"], repeat=j["repeat"], tested_side=j["side"],
                           pair_id=f"{manifest['experiment_id']}/{j['s']}/{j['seed']}/{j['repeat']}",
                           setup_sha256=setups[j["arm"]], baseline_setup_sha256=setups["baseline"],
                           log=result["log"], timestamp_utc=datetime.now(timezone.utc).isoformat())
                try:
                    if result.get("failed"):
                        raise ValueError("; ".join(result["errors"]))
                    row.update(audit_match(result, j, server), dump=j["dump"].name,
                               receipt=result["startup_receipt"])
                except (ValueError, KeyError, TypeError, OSError, AssertionError) as error:
                    # Permit the same-key retry only for native-worker infrastructure failures.
                    retryable = result.get("failure_phase") in ("native_session", "worker_abort")
                    detail = str(error)
                    path = folder / result["log"]
                    if path.is_file():
                        row["raw_log_sha256"] = sha(path)
                        log_text = path.read_text(encoding="utf8", errors="replace")
                        if any(marker in log_text for marker in ("mismatch", "scenario_rejected",
                                                                  "engine_changed_within_session")):
                            retryable = False
                    row.update(status="failed", error=detail, retryable=retryable,
                               failure_phase=result.get("failure_phase", "input_or_result_audit"))
                    if not retryable:
                        integrity_failures.append(key)
                        runner.cancel()
                append(stream, row)
                reported.add(key)
                if row["status"] == "ok":
                    accepted[key] = row
                if row["status"] != "ok" or len(accepted) % 50 == 0:
                    print(folder.name, len(accepted), "/", len(jobs), row["status"], key,
                          row.get("error", ""), flush=True)

            try:
                runner.run(pending, callback)
            except RuntimeError as error:
                for j in pending:
                    if j["variant"] not in reported and j["path"].exists():
                        callback(dict(variant=j["variant"], log=j["path"].name, failed=True,
                                      failure_phase="worker_abort", errors=[str(error)]))
                require(reported, f"Worker failed without a recorded attempt: {error}")
        require(not integrity_failures, f"Integrity gate failed: {', '.join(integrity_failures)}")
        require(reported, "No native jobs completed or recorded")
    print(folder.name, len(accepted), "/", len(jobs), "accepted", flush=True)
    require(len(accepted) == len(jobs), "Permanently incomplete batch")
    return accepted


def negative_probe(folder, fixture, seed):
    from desktop_warm_batch import DesktopWarmRunner, save as save_lab

    folder.mkdir(exist_ok=True)
    report = folder / "probe.json"
    if report.exists():
        result = read(report)
        require(result["passed"] and sha(folder / "invalid.jsonl") == result["raw_log_sha256"],
                "Invalid stored negative probe")
        return result
    invalid = folder / "invalid.bin"
    invalid.write_bytes(b"INTENTIONAL_INVALID_CONFIGURATION")
    log = folder / "invalid.jsonl"
    require(not log.exists(), "Unreconciled negative probe")
    runner = DesktopWarmRunner(Path(os.environ["FM27_ENGINE_ROOT"]), workers=1, retries=0, timeout=90)
    attempts = []
    try:
        runner.run([dict(variant="negative", seed=seed, config=invalid, fixture=fixture,
                         path=log, event_details=False)], attempts.append)
    except RuntimeError:
        pass
    if log.is_file():
        evidence = read_rows(log)
        receipts = runner.session_diagnostics
        passed = (len(attempts) == 1 and attempts[0].get("failed") is True
                  and len(receipts) == 1 and receipts[0]["returncode"] == 108
                  and not any(r["event"] == "natural_match_finished" for r in evidence))
        result = dict(passed=passed, returncode=receipts[0]["returncode"] if receipts else None,
                      raw_log_sha256=sha(log), invalid_setup_sha256=sha(invalid))
        save_lab(report, result)
        require(passed, "Native invalid-input probe did not fail as expected")
        return result
    raise RuntimeError("Negative probe did not reach the native match host")


def validate(folder, server, manifest, configs, fixture):
    jobs = list(plan_jobs(manifest, configs, fixture, "validation"))
    accepted = execute(folder / "validation", server, manifest, jobs)
    comparisons = []
    for job in jobs:
        if job["repeat"] == 0:
            stem = job["variant"][:-1]
            a, b = accepted[stem + "0"], accepted[stem + "1"]
            fields = ("score", "team_statistics", "finish_tick")
            equal = {field: a[field] == b[field] for field in fields}
            comparisons.append(dict(scenario=job["s"], arm=job["arm"], seed=job["seed"], exact=equal))
    require(all(all(row["exact"].values()) for row in comparisons), "A/A repeatability failed")
    probe = negative_probe(folder / "negative", fixture, manifest["validation_seeds"][0])
    report = dict(passed=True, matches=len(accepted), native_profile_and_tactics_readback=True,
                  complete_native_attributes_and_roster_readback=True, both_venue_transfers_verified=True,
                  repeat_comparisons=comparisons, negative_probe=probe)
    save(folder / "validation-summary.json", report)
    print("Technical validation passed; 48 exact repetitions and the separate negative probe.", flush=True)


def main():
    parser = ArgumentParser(description=__doc__)
    for name in ("lab", "game", "player-log", "local"):
        parser.add_argument("--" + name, type=lambda p: Path(p).resolve(), required=True)
    parser.add_argument("phase", choices=("prepare", "validate", "main"))
    args = parser.parse_args()
    require(args.local.is_dir() and DATA.parent not in args.local.parents and args.local != DATA.parent,
            "Use an existing local artifact directory outside the Git checkout")
    check_registration()
    server, fixture = initialize(args)
    manifest, configs = prepare(server, args.local)
    if args.phase != "prepare":
        validate(args.local, server, manifest, configs, fixture)
    if args.phase == "main":
        execute(args.local / "main", server, manifest, plan_jobs(manifest, configs, fixture, "main"))


if __name__ == "__main__":
    main()

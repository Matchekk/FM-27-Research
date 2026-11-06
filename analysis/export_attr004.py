"""Export only publishable ATTR-004 fields after the applicable run gate."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import json

from analyse_attr004 import ARMS, SCENARIOS, checked_rows, require
from run_attr004 import IDENTITY, REGISTRATION, git, save, sha
from verify_matches import DATA, read, read_rows


COMMON = (*IDENTITY, "scenario", "seed", "arm", "repeat", "tested_side", "pair_id",
          "attempt", "timestamp_utc", "status", "setup_sha256", "baseline_setup_sha256")
EVIDENCE = ("engine_readback", "raw_log_sha256", "input_dump_sha256", "startup_receipt_sha256")
RESULT = ("score", "finish_tick", "team_statistics")


def export_rows(source, expected, manifest):
    rows = read_rows(source / "ledger.jsonl")
    attempts = Counter()
    successes = {}
    failures = []
    for row in rows:
        key = (row["scenario"], row["seed"], row["arm"], row["repeat"])
        attempts[key] += 1
        require(key in expected and key not in successes and attempts[key] == row["attempt"] <= 2,
                f"Unexpected run attempt: {key}")
        setup = manifest["scenarios"][row["scenario"]]["setups"]
        require(all(row[k] == v for k, v in IDENTITY.items()) and row["setup_sha256"] == setup[row["arm"]]
                and row["baseline_setup_sha256"] == setup["baseline"], f"Run provenance differs: {key}")
        if row["status"] == "ok":
            for path_key, digest_key in (("log", "raw_log_sha256"), ("dump", "input_dump_sha256"),
                                         ("receipt", "startup_receipt_sha256")):
                path = (source / row[path_key]).resolve()
                require(source in path.parents and sha(path) == row[digest_key], f"Run evidence differs: {key}")
            successes[key] = {k: row[k] for k in (*COMMON, *EVIDENCE, *RESULT)}
        else:
            require(row["status"] == "failed", f"Unknown run status: {key}")
            # Retain failure classification and proof hash. Raw diagnostic text can contain private paths.
            fields = (*COMMON, "failure_phase", "retryable", "raw_log_sha256")
            failures.append({k: row[k] for k in fields if k in row})
    require(successes.keys() == expected, f"Incomplete export: {len(successes)}/{len(expected)}")
    return successes, failures


def write_jsonl(path, rows):
    with path.open("w", encoding="utf8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False, separators=(",", ":")) + "\n")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("local", type=lambda p: Path(p).resolve())
    parser.add_argument("--validation-only", action="store_true")
    args = parser.parse_args()
    source = args.local
    destination = DATA / "attr-004"
    manifest = read(source / "manifest.json")
    validation = read(source / "validation-summary.json")
    require(manifest["preregistration_commit"] == REGISTRATION and validation["passed"]
            and validation["negative_probe"]["passed"], "Missing registered technical validation")
    require(not git("diff", "--", "analysis/run_attr004.py"), "Runner differs from its staged copy")
    scenarios = tuple(map(str, range(len(SCENARIOS))))
    checks = {(s, seed, arm, repeat) for s in scenarios for seed in manifest["validation_seeds"]
              for arm in ARMS for repeat in (0, 1)}
    runs, validation_failures = export_rows(source / "validation", checks, manifest)
    for key in checks:
        if key[-1] == 0:
            require(all(runs[key][field] == runs[(*key[:-1], 1)][field] for field in RESULT),
                    f"Nonidentical validation repetition: {key}")
    require(len(runs) == validation["matches"] == 96, "Wrong validation match count")
    validation_rows = [runs[key] for key in sorted(runs)]

    destination.mkdir(exist_ok=True)
    write_jsonl(destination / "validation.jsonl", validation_rows)
    save(destination / "validation-summary.json", validation)
    published = dict(validation_matches=len(validation_rows), validation_failed_attempts=len(validation_failures))
    if validation_failures:
        write_jsonl(destination / "validation-failures.jsonl", validation_failures)
    if not args.validation_only:
        keys = {(s, seed, arm, 0) for s, seeds in manifest["seeds"].items() for seed in seeds for arm in ARMS}
        matches, failures = export_rows(source / "main", keys, manifest)
        published_rows = [matches[key] for key in sorted(matches)]
        checked_rows(published_rows, manifest)
        write_jsonl(destination / "matches.jsonl", published_rows)
        if failures:
            write_jsonl(destination / "failures.jsonl", failures)
        published.update(matches=len(matches), failed_attempts=len(failures), not_run=0, excluded_triplets=0)
    manifest.update(publication_counts=published, runner_sha256=sha(DATA.parent / "analysis/run_attr004.py"),
                    runner_git_blob=git("hash-object", "analysis/run_attr004.py"))
    save(destination / "manifest.json", manifest)


if __name__ == "__main__":
    main()

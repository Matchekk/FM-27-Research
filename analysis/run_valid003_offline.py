"""Emit own profile intentions and run two fixed harmless coordination probes.

No host, match, PKM decoder, real Registry or actual global-native lease is used.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.coordination_testpath import run_probe
from research.validation003 import profile_catalog


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "local/valid003-offline")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)  # never reset counters or overwrite a run
    profiles = profile_catalog()
    (output / "own-profile-catalog.json").write_text(json.dumps(profiles, indent=2) + "\n", encoding="utf8")
    results = [run_probe(output / "probe-study", output / "offline-test-lease", name, [name])
               for name in ("first", "second")]
    report = dict(id="VALID-003-offline-preparation", native_processes_started=0,
        seed_reservations=0, career_replay_released=False, profile_vectors=len(profiles),
        profile_native_validation=False, synthetic_python_children=len(results),
        probe_results=results, shared_live_native_lease_used=False,
        code_lf_sha256={p: sha256((ROOT / p).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
            for p in ("research/validation003.py", "research/coordination_testpath.py",
                      "research/coordination.py", "research/budget.py", "research/study_budget.py")})
    (output / "offline-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf8")
    print(json.dumps(report))


if __name__ == "__main__": main()

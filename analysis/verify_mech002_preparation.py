"""Read-only binary preparation check. No server import, subprocess or native I/O."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research.startpolicy import StartPolicy, decode_records, encode_startpolicy, native_status


def inspect_binary(path):
    original = Path(path).read_bytes()
    records = decode_records(original)
    if encode_startpolicy(records) != original:
        raise ValueError("Default byte identity failed")
    sides = []
    for side in (0, 1):
        if encode_startpolicy(records, StartPolicy(side, 10000)) != original:
            raise ValueError("Full policy byte identity failed")
        low = encode_startpolicy(records, StartPolicy(side, 7000))
        changes = [(old, new) for old, new in zip(records, decode_records(low), strict=True) if old != new]
        if len(changes) != 20 or not all(old[:4] == new[:4] and old[0] == 15 and old[1] == side
                and old[3] in (16, 17) and (old[4], new[4]) == (10000, 7000) for old, new in changes):
            raise ValueError("Opt-in exact diff failed")
        sides.append(dict(tested_side=side, full_bytes_identical=True,
                          low_changed_records=len(changes), low_setup_sha256=sha256(low).hexdigest()))
    return dict(name=Path(path).name, baseline_sha256=sha256(original).hexdigest(),
                records=len(records), default_bytes_identical=True, sides=sides)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, action="append", required=True)
    args = parser.parse_args()
    print(json.dumps(dict(kind="offline_binary_preparation_only", native_status=native_status(),
                          new_native_starts=0, new_match_seeds_reserved=0,
                          baselines=[inspect_binary(p) for p in args.baseline]), indent=2))

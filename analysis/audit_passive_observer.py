"""Read an own observer log and input dump offline. Never execute a host."""
import argparse
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.passive_observer import audit_trace, file_hash, read_rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--dump', type=Path, required=True)
    parser.add_argument('--seed', type=int, required=True)
    parser.add_argument('--records', type=int, default=5557)
    args = parser.parse_args()
    result = audit_trace(read_rows(args.log), json.loads(args.dump.read_text(encoding='utf8')),
                         args.seed, args.records)
    result.update(raw_log_sha256=file_hash(args.log), input_dump_sha256=file_hash(args.dump))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()

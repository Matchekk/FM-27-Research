"""Offline public-archive TRAIN-002 diagnostic; never opens a game save."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.training002 import historical_diagnostic


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(historical_diagnostic(ROOT), indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        destination = args.output.resolve()
        permitted = (ROOT / "data/train-002-technical").resolve()
        if not destination.is_relative_to(permitted) or destination.suffix != ".json":
            parser.error("Output must be new JSON under data/train-002-technical")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf8", newline="\n") as stream:
            stream.write(result)
    else:
        print(result, end="")

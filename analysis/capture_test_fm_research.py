"""Create a private, read-only file inventory for the Test FM Research save.

Only explicit user-selected files are hashed. No FM internals are decoded, no game
process is launched, and the result does not grant replay/training validation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

PROJECT = "Test FM Research"
MAX_FILE_BYTES = 20 * 1024**3
FORMATS = {"pre_match_save": ".fm", "post_match_save": ".fm",
           "match_pkm": ".pkm", "match_rec": ".rec"}


class CaptureError(ValueError):
    """Unsafe or incomplete capture request."""


def _fingerprint(path: Path, role: str, ordinal: int) -> dict:
    if path.suffix.lower() != FORMATS[role] or path.is_symlink() or not path.is_file():
        raise CaptureError(f"Invalid {role}: select an existing regular {FORMATS[role]} file")
    before = path.stat()
    if not 0 < before.st_size <= MAX_FILE_BYTES:
        raise CaptureError(f"Invalid {role}: empty or too large to fingerprint")
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            size += len(chunk)
    after = path.stat()
    if (size != before.st_size or after.st_size != before.st_size or
            after.st_mtime_ns != before.st_mtime_ns):
        raise CaptureError(f"Unstable {role}: save/copy must finish before capture")
    return {"role": role, "ordinal": ordinal, "format": FORMATS[role],
            "size_bytes": size, "sha256": digest.hexdigest(),
            "stable_during_hash": True}


def build_receipt(pre_save, *, post_save=None, pkms=(), recs=()) -> dict:
    chosen = [("pre_match_save", Path(pre_save))]
    if post_save is not None:
        chosen.append(("post_match_save", Path(post_save)))
    chosen.extend(("match_pkm", Path(p)) for p in pkms)
    chosen.extend(("match_rec", Path(p)) for p in recs)
    unique = [path.resolve() for _, path in chosen]
    if len(unique) != len(set(unique)):
        raise CaptureError("The same file cannot represent multiple independent artifacts")
    counts = {key: 0 for key in FORMATS}
    artifacts = []
    for role, path in chosen:
        counts[role] += 1
        artifacts.append(_fingerprint(path, role, counts[role]))
    return {
        "schema": "fm27.test_fm_research.capture.v1",
        "project": PROJECT,
        "capture_utc": datetime.now(timezone.utc).isoformat(),
        "source": "explicit_private_files_read_only",
        "artifacts": artifacts,
        "capabilities": {
            "save_content_decoded": False,
            "pkm_content_decoded": False,
            "rec_content_decoded": False,
            "native_matches_started": 0,
            "seed_reservations_created": 0,
            "career_advances": 0,
            "original_career_replay_released": False,
            "training_executor_released": False,
        },
    }


def write_private_receipt(receipt: dict, destination, *, private_root) -> Path:
    root = Path(private_root).resolve()
    output = Path(destination)
    if not output.is_absolute():
        output = Path.cwd() / output
    resolved = output.resolve()
    if not resolved.is_relative_to(root) or resolved == root or resolved.suffix.lower() != ".json":
        raise CaptureError("Receipt must be a JSON file strictly inside the private local/ directory")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(receipt, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    try:
        with resolved.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
    except FileExistsError as exc:
        raise CaptureError("Receipt already exists; use a new versioned filename") from exc
    return resolved


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pre-save", required=True, help="Local .fm save made before the target match")
    parser.add_argument("--post-save", help="Optional distinct local .fm save made after the match")
    parser.add_argument("--pkm", action="append", default=[], help="Explicit local .pkm file (repeatable)")
    parser.add_argument("--rec", action="append", default=[], help="Explicit local .rec file (repeatable)")
    parser.add_argument("--output", required=True, help="New JSON receipt path below repository local/")
    args = parser.parse_args(argv)
    receipt = build_receipt(args.pre_save, post_save=args.post_save, pkms=args.pkm, recs=args.rec)
    repository = Path(__file__).resolve().parents[1]
    output = write_private_receipt(receipt, args.output, private_root=repository / "local")
    print("Private read-only inventory saved:", output)
    print("No native replay, calendar advance, decoder, or research gate was executed.")


if __name__ == "__main__":
    main()

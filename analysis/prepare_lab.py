"""Stage the pinned upstream release locally without launching its desktop EXE."""
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import struct
import zipfile

RELEASE = "v1114.6"
EXE_SHA256 = "12be6612326b8264fbb2a9901555bfa1ebc964346b78f05af5854e1b473a8278"


def prepare(executable, destination):
    raw = executable.read_bytes()
    if sha256(raw).hexdigest() != EXE_SHA256:
        raise ValueError("Release EXE does not match GitHub release asset digest")
    # PE data after the payload can contain ZIP marker strings: validate boundaries.
    candidates = []
    position = 0
    while (position := raw.find(b"PK\x05\x06", position)) >= 0:
        end = position
        position += 4
        if end + 22 > len(raw):
            continue
        _, disk, central_disk, count, total, size, offset, comment = struct.unpack_from("<4s4H2IH", raw, end)
        start = end - size - offset
        if disk == central_disk == 0 and count == total and count > 0 and start >= 0 and end + 22 + comment <= len(raw):
            payload = raw[start:end + 22 + comment]
            if payload.startswith(b"PK\x03\x04"):
                candidates.append(payload)
    if len(candidates) != 1:
        raise ValueError("Expected one validated embedded payload")
    payload = candidates[0]
    destination.mkdir(parents=True, exist_ok=False)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for entry in archive.infolist():
            name = entry.filename
            if not (name.startswith("engine/") or name.startswith("source/")) or entry.is_dir():
                continue
            target = (destination / name).resolve()
            if destination.resolve() not in target.parents:
                raise ValueError("Unsafe archive path")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(entry))
    receipt = dict(release=RELEASE, release_exe_sha256=EXE_SHA256,
                   payload_sha256=sha256(payload).hexdigest(), desktop_exe_executed=False)
    (destination / "preparation.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf8")
    print(json.dumps(receipt))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable", type=Path)
    parser.add_argument("destination", type=Path, help="New ignored local/ directory")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1] / "local"
    if root.resolve() not in args.destination.resolve().parents:
        parser.error("Destination must be inside the ignored repository local/ directory")
    prepare(args.executable, args.destination)

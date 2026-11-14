"""Verify the pre-round3 scientific archive without importing any native runtime."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify():
    baseline = json.loads((ROOT / 'docs/round3/baseline.json').read_text(encoding='utf8'))
    for name, expected in baseline['sha256'].items():
        path = ROOT / name
        current = sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        original = subprocess.check_output(
            ['git', 'show', baseline['base_commit'] + ':' + name], cwd=ROOT)
        archived = sha256(original.replace(b'\r\n', b'\n')).hexdigest()
        if current != expected or archived != expected:
            raise ValueError('Historical archive changed: ' + name)
    print(f"Round3 historical archive: {len(baseline['sha256'])} files unchanged")


if __name__ == '__main__':
    verify()

"""Read-only Gitblob and working-tree check of the archive before NIGHT-001."""
from hashlib import sha256
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def verify():
    baseline = json.loads((ROOT/'docs/night-001/baseline.json').read_text(encoding='utf8'))
    for name, wanted in baseline['sha256'].items():
        current = (ROOT/name).read_bytes().replace(b'\r\n', b'\n')
        original = subprocess.check_output(['git','show',baseline['base_commit']+':'+name],cwd=ROOT)
        if sha256(current).hexdigest()!=wanted or sha256(original.replace(b'\r\n',b'\n')).hexdigest()!=wanted:
            raise ValueError('Historical NIGHT-001 archive changed: '+name)
    print('NIGHT-001 historical archive:',len(baseline['sha256']),'files unchanged')


if __name__ == '__main__':
    verify()

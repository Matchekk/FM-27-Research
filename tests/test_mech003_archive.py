"""Small own Git repositories and ZIPs; never use a game/runtime or native host."""
from hashlib import sha1, sha256
from importlib.metadata import version
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
import verify_mech003_archive as archive


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding='utf8', newline='\n')


def fixture(base):
    repo = base / 'repo'; repo.mkdir()
    for name in archive.CODE:
        put(repo / name, '# own synthetic fixture\n')
    put(repo / 'research/stamina003.py', 'EXPECTED=2\n')
    put(repo / 'analysis/verify_mech003.py', '''from argparse import ArgumentParser
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.stamina003 import EXPECTED
p=ArgumentParser();p.add_argument('--directory',type=Path,required=True);a=p.parse_args()
value=json.loads((a.directory/'value.json').read_text())['value']
assert value==EXPECTED,'actual public data differs from historical rule'
print(json.dumps(dict(contract_verified=True,native_starts_by_verifier=0,imported_value=EXPECTED,data_value=value)))
''')
    put(repo / 'data/mech-003-stamina/value.json', '{"value":1}\n')
    put(repo / 'requirements-lock.txt', 'packaging==' + version('packaging') + '\n')
    subprocess.run(['git', 'init', '--object-format=sha1', '-q', str(repo)], check=True, capture_output=True)
    subprocess.run(['git', 'add', '.'], cwd=repo, check=True, capture_output=True)
    subprocess.run(['git', '-c', 'user.name=Own test', '-c', 'user.email=own-test@example.invalid',
                    'commit', '-qm', 'Own archive fixture'], cwd=repo, check=True, capture_output=True)
    commit = archive.git(repo, 'rev-parse', 'HEAD').decode().strip()
    data = base / 'current-public'; data.mkdir()
    code = {n: sha256((repo / n).read_bytes()).hexdigest() for n in archive.CODE}
    receipt = dict(config=dict(experiment_id='MECH-003-STAMINA-R0',
        preregistration=dict(commit=commit), execution=dict(code_sha256=code)))
    put(data / 'manifest.json', json.dumps(receipt)); put(data / 'value.json', '{"value":2}\n')
    return repo, data, commit


class MechArchiveTests(unittest.TestCase):
    def test_public_root_alias_is_canonicalized_before_containment_check(self):
        with tempfile.TemporaryDirectory() as temp:
            data=Path(temp)/'public-measurements';data.mkdir()
            put(data/'value.json','{"value":2}\n')
            expected=archive.public_data_fingerprint(data)
            self.assertEqual(archive.public_data_fingerprint(data/'..'/data.name),expected)
            if sys.platform=='win32':
                import ctypes
                from ctypes import wintypes
                kernel=ctypes.WinDLL('kernel32',use_last_error=True)
                kernel.GetShortPathNameW.argtypes=[wintypes.LPCWSTR,wintypes.LPWSTR,wintypes.DWORD]
                kernel.GetShortPathNameW.restype=wintypes.DWORD
                needed=kernel.GetShortPathNameW(str(data),None,0)
                self.assertGreater(needed,0)
                buffer=ctypes.create_unicode_buffer(needed)
                self.assertGreater(kernel.GetShortPathNameW(str(data),buffer,needed),0)
                self.assertEqual(archive.public_data_fingerprint(Path(buffer.value)),expected)

    def test_historical_imports_and_current_data_are_both_real(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, data, commit = fixture(Path(temp))
            put(repo / 'research/stamina003.py', 'EXPECTED=99\n')
            put(repo / 'analysis/verify_mech003.py', 'raise RuntimeError("current verifier must never run")\n')
            before = archive.public_data_fingerprint(data)
            result = archive.verify_archive(repo, data, expected_commit=commit)
            self.assertEqual(result['historical_verifier']['imported_value'], 2)
            self.assertEqual(result['historical_verifier']['data_value'], 2)
            self.assertEqual(result['frozen_code_files_verified'], 16)
            self.assertEqual(archive.public_data_fingerprint(data), before)
            put(data / 'value.json', '{"value":3}\n')
            with self.assertRaisesRegex(archive.ArchiveError, 'Historical verifier rejected current public'):
                archive.verify_archive(repo, data, expected_commit=commit)

    def test_wrong_commit_hash_and_code_inventory_block_before_extraction(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, data, commit = fixture(Path(temp))
            manifest = data / 'manifest.json'; original = manifest.read_text()
            for kind in ('commit', 'hash', 'inventory'):
                receipt = json.loads(original)
                if kind == 'commit':receipt['config']['preregistration']['commit'] = '0' * 40
                elif kind == 'hash':receipt['config']['execution']['code_sha256'][archive.CODE[0]] = '0' * 64
                else:receipt['config']['execution']['code_sha256']['research/extra.py'] = '0' * 64
                put(manifest, json.dumps(receipt))
                with patch.object(archive, 'extract_snapshot') as extract:
                    with self.assertRaises(archive.ArchiveError):archive.verify_archive(repo, data, expected_commit=commit)
                    extract.assert_not_called()

    def test_lock_and_installed_dependency_drift_block(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, data, commit = fixture(Path(temp)); lock = repo / 'requirements-lock.txt'; original = lock.read_text()
            put(lock, original + '# current drift\n')
            with self.assertRaisesRegex(archive.ArchiveError, 'Dependency lock drift'):
                archive.verify_archive(repo, data, expected_commit=commit)
            put(lock, original)
            with patch.object(archive, 'version', return_value='0.0-unexpected'):
                with self.assertRaisesRegex(archive.ArchiveError, 'Installed dependency drift'):
                    archive.verify_archive(repo, data, expected_commit=commit)

    def test_git_tree_rejects_links_and_resource_overflow(self):
        def metadata(mode='100644', name='own.txt', size=4):
            return f'{mode} blob {"a"*40} {size}\t{name}\0'.encode()
        for raw in (metadata('120000'), metadata(size=archive.MAX_FILE_BYTES+1),
                    metadata(name='A/x') + metadata(name='a/y'), metadata(name='../outside')):
            with patch.object(archive, 'git', return_value=raw):
                with self.assertRaises(archive.ArchiveError):archive.tree_manifest(Path('.'), 'a'*40)

    def test_zip_paths_links_collisions_and_content_are_rejected(self):
        names = ('../outside', '/absolute', 'C:/absolute', 'x\\outside', 'x/../outside',
                 'x:stream', 'bad.', 'NUL', 'x/COM1.txt', 'x/quote".txt')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for index, name in enumerate(names):
                path = root / f'bad-{index}.zip'
                with ZipFile(path, 'w') as bundle:bundle.writestr(name, b'own')
                with self.assertRaises(archive.ArchiveError):archive.extract_snapshot(path, root / f'out-{index}', {})
            for kind in ('symlink', 'duplicate', 'content'):
                path = root / (kind + '.zip'); info = ZipInfo('own.txt')
                info.external_attr = ((stat.S_IFLNK if kind=='symlink' else stat.S_IFREG) | 0o644) << 16
                with ZipFile(path, 'w') as bundle:
                    bundle.writestr(info, b'own')
                    if kind=='duplicate':bundle.writestr('OWN.TXT', b'own')
                expected = {'own.txt':dict(size=3, oid='0'*40 if kind=='content' else sha1(b'blob 3\0own').hexdigest())}
                with self.assertRaises(archive.ArchiveError):archive.extract_snapshot(path, root / (kind+'-out'), expected)

    def test_zip_limits_and_missing_full_snapshot_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = root / 'own.zip'
            with ZipFile(path, 'w') as bundle:bundle.writestr('own.txt', b'own')
            expected = {'own.txt':dict(size=3, oid=sha1(b'blob 3\0own').hexdigest())}
            with patch.object(archive, 'MAX_MEMBERS', 0):
                with self.assertRaises(archive.ArchiveError):archive.extract_snapshot(path, root/'count', expected)
            with patch.object(archive, 'MAX_BYTES', 2):
                with self.assertRaises(archive.ArchiveError):archive.extract_snapshot(path, root/'bytes', expected)
            with self.assertRaises(archive.ArchiveError):archive.extract_snapshot(path, root/'missing', dict(expected, missing=dict(size=0,oid='0'*40)))

    def test_cleanup_refuses_changed_or_unowned_absolute_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); owned = root / 'fm27-mech003-archive-own'; owned.mkdir()
            with patch.object(archive.shutil, 'rmtree') as remove:
                with self.assertRaises(archive.ArchiveError):archive.cleanup_owned(owned, root/'different', root)
                remove.assert_not_called()
            archive.cleanup_owned(owned, owned.resolve(), root)
            self.assertFalse(owned.exists())


if __name__ == '__main__':
    unittest.main()

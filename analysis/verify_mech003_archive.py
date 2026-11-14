"""Run the unchanged preregistered MECH verifier from a bounded Git snapshot.

Only Git, public JSON/text and an isolated historical analysis process are used.
No runtime server, NativeLab constructor, game assets, seeds or registries occur.
"""
from argparse import ArgumentParser
from hashlib import sha1, sha256
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
PREREGISTRATION = '9a5424fe77f465c0b5b3bd3d84e89300a1fe3ec4'
CODE = (
    'research/stamina003.py', 'analysis/run_mech003.py', 'analysis/analyse_mech003.py',
    'analysis/export_mech003.py', 'analysis/verify_mech003.py', 'research/native.py',
    'research/stats.py', 'research/core.py', 'research/cli.py', 'research/budget.py',
    'research/study_budget.py', 'research/coordination.py', 'research/validation003.py',
    'research/night_control.py', 'analysis/night_supervise.py', 'research/native_process005.py',
)
MAX_FILES = 2048
MAX_MEMBERS = 4096
MAX_BYTES = 64 * 1024**2
MAX_FILE_BYTES = 8 * 1024**2
MAX_ARCHIVE_BYTES = MAX_BYTES + 2 * 1024**2
MAX_TREE_BYTES = 2 * 1024**2
TIMEOUT = 60


class ArchiveError(ValueError):
    """An archival provenance, resource, dependency or result gate failed."""


def require(ok, message):
    if not ok:
        raise ArchiveError(message)


def normalized(data):
    return data.replace(b'\r\n', b'\n')


def git(repo, *arguments):
    result = subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.eol=lf', *arguments], cwd=repo, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=TIMEOUT,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    require(result.returncode == 0, 'Required historical Git object/command unavailable')
    return result.stdout


def safe_name(name, directory=False):
    require(type(name) is str and name and '\\' not in name and '\0' not in name,
            'Unsafe archive path')
    if directory and name.endswith('/'):
        name = name[:-1]
    parts = name.split('/')
    require(not PurePosixPath(name).is_absolute() and len(name) <= 240 and len(parts) <= 32,
            'Absolute or oversized archive path')
    reserved = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)), *(f'lpt{i}' for i in range(1, 10))}
    require(all(p not in ('', '.', '..') and not any(ord(c) < 32 or c in '<>:"|?*' for c in p) and p == p.rstrip(' .') and
                p.casefold() != '.git' and p.split('.')[0].casefold() not in reserved for p in parts),
            'Traversal, alternate stream or ambiguous Windows archive path')
    return '/'.join(parts)


def tree_manifest(repo, commit):
    # Git tree metadata bounds the archive before it is generated or extracted.
    raw = git(repo, 'ls-tree', '-r', '-z', '-l', commit)
    require(len(raw) <= MAX_TREE_BYTES, 'Historical tree metadata too large')
    entries = raw.rstrip(b'\0').split(b'\0') if raw else []
    require(0 < len(entries) <= MAX_FILES, 'Historical snapshot file count exceeded')
    result = {}; folded = {}; total = 0
    for entry in entries:
        metadata, raw_name = entry.split(b'\t', 1)
        mode, kind, oid, size = metadata.decode('ascii').split()
        name = safe_name(raw_name.decode('utf8'))
        require(mode in ('100644', '100755') and kind == 'blob' and re.fullmatch('[0-9a-f]{40}', oid),
                'Historical links, submodules or unknown Git object format forbidden')
        length = int(size)
        require(0 <= length <= MAX_FILE_BYTES, 'Historical file too large')
        for path in (*reversed(PurePosixPath(name).parents), PurePosixPath(name)):
            if str(path) == '.':continue
            value = (str(path), 'file' if str(path) == name else 'directory')
            require(str(path).casefold() not in folded or folded[str(path).casefold()] == value,
                    'Historical path has case or file/directory collision')
            folded[str(path).casefold()] = value
        total += length
        require(total <= MAX_BYTES, 'Historical snapshot total bytes exceeded')
        result[name] = dict(size=length, oid=oid)
    return result


def check_dependencies(repo, commit):
    archived = normalized(git(repo, 'show', commit + ':requirements-lock.txt'))
    current = normalized((repo / 'requirements-lock.txt').read_bytes())
    require(current == archived, 'Dependency lock drift: current requirements must equal preregistration')
    installed = {}; keys = set()
    for line in archived.decode('utf8').splitlines():
        match = re.fullmatch(r'([A-Za-z0-9][A-Za-z0-9_.-]*)==([A-Za-z0-9][A-Za-z0-9_.+!-]*)', line)
        require(match is not None, 'Unsupported or unpinned historical dependency')
        name, expected = match.groups(); key = re.sub('[-_.]+', '-', name).lower()
        require(key not in keys, 'Duplicate historical dependency'); keys.add(key)
        try:
            actual = version(name)
        except PackageNotFoundError as error:
            raise ArchiveError('Historical dependency not installed: ' + name) from error
        require(actual == expected, 'Installed dependency drift: ' + name)
        installed[name] = actual
    require(installed, 'Empty historical dependency lock')
    return sha256(archived).hexdigest(), installed


def extract_snapshot(archive, destination, expected):
    """Validate the complete ZIP before extraction; verify each exact Git blob."""
    require(archive.stat().st_size <= MAX_ARCHIVE_BYTES, 'Compressed snapshot too large')
    require(not destination.exists(), 'Snapshot destination must be new')
    with ZipFile(archive) as bundle:
        infos = bundle.infolist()
        require(len(infos) <= MAX_MEMBERS, 'ZIP member count exceeded')
        files = {}; folded = set(); total = 0
        directories = {str(p) for n in expected for p in PurePosixPath(n).parents if str(p) != '.'}
        for info in infos:
            name = safe_name(info.filename, info.is_dir())
            require(name.casefold() not in folded, 'Duplicate/case-colliding ZIP member'); folded.add(name.casefold())
            mode = info.external_attr >> 16
            require(not (info.flag_bits & 1) and stat.S_IFMT(mode) in (0, stat.S_IFDIR if info.is_dir() else stat.S_IFREG),
                    'Encrypted, linked or special ZIP member forbidden')
            if info.is_dir():
                require(name in directories and info.file_size == 0, 'Unexpected ZIP directory')
                continue
            require(name in expected and info.file_size == expected[name]['size'] and info.file_size <= MAX_FILE_BYTES,
                    'ZIP file absent from exact Git tree or wrong size')
            total += info.file_size; require(total <= MAX_BYTES, 'Expanded snapshot too large')
            files[name] = info
        require(set(files) == set(expected), 'ZIP does not contain the full historical repository')
        destination.mkdir(mode=0o700)
        base = destination.resolve()
        for name, info in files.items():
            target = destination.joinpath(*name.split('/'))
            require(target.resolve().is_relative_to(base), 'Extraction target escaped snapshot')
            target.parent.mkdir(parents=True, exist_ok=True)
            digest = sha1(b'blob ' + str(info.file_size).encode() + b'\0'); written = 0
            with bundle.open(info) as source, target.open('xb') as output:
                while chunk := source.read(1024 * 1024):
                    written += len(chunk)
                    require(written <= info.file_size, 'ZIP decompression exceeded declared size')
                    digest.update(chunk); output.write(chunk)
            require(written == info.file_size and digest.hexdigest() == expected[name]['oid'],
                    'Extracted content differs from exact historical Git blob')
    return dict(files=len(files), bytes=total)


def cleanup_owned(base, original, temporary_root):
    # Never recursively delete a computed Windows target without this check.
    require(base.is_absolute() and base.resolve() == original and base.parent.resolve() == temporary_root and
            original.is_relative_to(temporary_root) and base.name.startswith('fm27-mech003-archive-') and
            not base.is_symlink() and not (hasattr(base, 'is_junction') and base.is_junction()),
            'Temporary cleanup target changed; retain it for manual reconciliation')
    shutil.rmtree(base)


def public_data_fingerprint(directory):
    directory = Path(directory).resolve()
    files = sorted(p for p in directory.rglob('*') if p.is_file())
    require(0 < len(files) <= MAX_FILES, 'Current public measurement file count exceeded')
    digest = sha256(); total = 0
    for path in files:
        require(not path.is_symlink() and path.resolve().is_relative_to(directory), 'Public measurement link forbidden')
        size = path.stat().st_size; total += size
        require(size <= MAX_FILE_BYTES and total <= MAX_BYTES, 'Public measurement byte limit exceeded')
        digest.update(path.relative_to(directory).as_posix().encode() + b'\0'); digest.update(path.read_bytes())
    return digest.hexdigest()


def verify_archive(repo=ROOT, directory=None, *, expected_commit=PREREGISTRATION):
    repo = Path(repo).resolve(); directory = Path(directory or repo / 'data/mech-003-stamina').resolve()
    receipt = json.loads((directory / 'manifest.json').read_text(encoding='utf8'))
    config = receipt['config']; commit = config['preregistration']['commit']
    require(re.fullmatch('[0-9a-f]{40}', expected_commit) and commit == expected_commit,
            'Wrong preregistration commit; expected the exact published MECH release')
    require(git(repo, 'rev-parse', '--verify', commit + '^{commit}').decode().strip() == commit,
            'Historical object is not the exact commit')
    require(config['experiment_id'] == 'MECH-003-STAMINA-R0', 'Wrong experiment manifest')
    code = config['execution']['code_sha256']
    require(set(code) == set(CODE), 'Frozen code inventory must contain the exact sixteen paths')
    for name, expected in code.items():
        require(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected) and
                sha256(normalized(git(repo, 'show', commit + ':' + name))).hexdigest() == expected,
                'Frozen code hash differs from preregistered Git blob: ' + name)
    lock_hash, installed = check_dependencies(repo, commit)
    expected = tree_manifest(repo, commit)
    before = public_data_fingerprint(directory)
    temporary_root = Path(tempfile.gettempdir()).resolve()
    base = Path(tempfile.mkdtemp(prefix='fm27-mech003-archive-', dir=temporary_root)).resolve()
    original = base
    try:
        archive = base / 'repository.zip'; snapshot = base / 'snapshot'
        git(repo, 'archive', '--format=zip', '--output=' + str(archive), commit)
        size = extract_snapshot(archive, snapshot, expected)
        env = {k: v for k, v in os.environ.items() if k not in ('PYTHONPATH', 'PYTHONHOME',
                'NIGHT_PROGRAM_TOKEN', 'TACT_P0_SUPERVISOR_TOKEN', 'MECH003_CONTAINED_STUDY') and
                not k.startswith(('FM27_', '_FM27_'))}
        env.update(PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1')
        result = subprocess.run([sys.executable, '-B', str(snapshot / 'analysis/verify_mech003.py'),
                '--directory', str(directory)], cwd=snapshot, env=env, capture_output=True, text=True,
                timeout=TIMEOUT, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        require(public_data_fingerprint(directory) == before, 'Historical verification mutated current public data')
        diagnostic = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else 'no diagnostic'
        require(result.returncode == 0, 'Historical verifier rejected current public measurements: ' +
                diagnostic.replace(str(base), '<snapshot>'))
        historical = json.loads(result.stdout)
        require(type(historical) is dict and historical.get('contract_verified') is True and
                historical.get('native_starts_by_verifier') == 0, 'Historical verifier did not return a successful nonnative contract check')
        return dict(preregistration_commit=commit, frozen_code_files_verified=len(code), snapshot=size,
                    dependency_lock_sha256=lock_hash, installed_dependencies=installed,
                    current_public_data_sha256=before, historical_verifier=historical,
                    current_sources_imported=False, native_starts_by_archive_wrapper=0)
    finally:
        cleanup_owned(base, original, temporary_root)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, default=ROOT / 'data/mech-003-stamina')
    args = parser.parse_args()
    try:
        print(json.dumps(verify_archive(directory=args.directory), sort_keys=True))
    except (ArchiveError, OSError, KeyError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        raise SystemExit('MECH archive verification blocked: ' + str(error))

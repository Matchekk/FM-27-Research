"""Independent fixed-deadline accounting for the NIGHT-002 mission.

NIGHT-001 files and terminal study ledgers are never opened for mutation here.
Every study retains its own narrower budget, publication gates and NativeLease.
"""
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import os
from pathlib import Path
import stat

from .budget import NativeBudget, atomic, supervisor_alive
from .native import read, require

DEADLINE = '2026-11-15T07:00:00+00:00'
CAPS = {'technical': 192, 'main': 2048}
CHILD_SECONDS = 3600
ARTIFACT_LIMIT_BYTES = 4 * 1024**3
PROGRAM = 'NIGHT-002'


def utcnow():
    return datetime.now(timezone.utc)


def artifact_bytes(directory):
    """Count the whole mission tree; reject links/reparse points and escapes."""
    directory = Path(directory)
    if not directory.exists():
        return 0
    root = directory.resolve()
    total = 0
    for path in [directory, *directory.rglob('*')]:
        try:
            value = path.lstat()
        except FileNotFoundError:
            continue  # Independent admitted workers can remove pending markers.
        require(not path.is_symlink() and not (getattr(value, 'st_file_attributes', 0) & 0x400),
                'Mission artifact links/reparse points are forbidden')
        require(path.resolve().is_relative_to(root), 'Mission artifact path escaped')
        if stat.S_ISREG(value.st_mode):
            total += value.st_size
    return total


def assert_artifact_limit(root):
    size = artifact_bytes(Path(root) / 'local/night-002')
    require(size < ARTIFACT_LIMIT_BYTES, 'NIGHT-002 cumulative private artifact limit reached')
    return size


# Study runners use the same mission-wide check before every native admission.
check_artifacts = assert_artifact_limit


class Night002Budget(NativeBudget):
    """Whole supervised phase-child time is charged, including Python audits."""
    def __init__(self, path, deadline=DEADLINE):
        path = Path(path)
        self.deadline = deadline
        end = datetime.fromisoformat(deadline)
        require(end.tzinfo is not None and end.utcoffset() == timedelta(0),
                'An explicit immutable UTC deadline is required')
        require(deadline == DEADLINE, 'NIGHT-002 fixed deadline changed')
        new = not path.exists()
        super().__init__(path, experiment=PROGRAM, seconds=CHILD_SECONDS, caps=CAPS)
        if new:
            state = self.load()
            state.update(absolute_deadline_utc=deadline, first_operation_utc=None,
                         artifact_limit_bytes=ARTIFACT_LIMIT_BYTES)
            atomic(self.path, state)
        state = self.load()
        require(state.get('absolute_deadline_utc') == deadline and
                state.get('artifact_limit_bytes') == ARTIFACT_LIMIT_BYTES,
                'NIGHT-002 deadline/artifact limit changed; retain original budget')

    def reserve(self, name, kind, keys):
        state = self.load()
        require(state['absolute_deadline_utc'] == self.deadline and
                state['artifact_limit_bytes'] == ARTIFACT_LIMIT_BYTES,
                'NIGHT-002 deadline/artifact limit changed')
        now = utcnow()
        remaining = (datetime.fromisoformat(self.deadline) - now).total_seconds() - 5
        require(remaining > 0, 'NIGHT-002 fixed deadline reached; no new native operation')
        allowance = min(remaining, super().reserve(name, kind, keys))
        state = self.load()
        if state['first_operation_utc'] is None:
            state['first_operation_utc'] = now.isoformat()
        state['active']['child_deadline_utc'] = (now + timedelta(seconds=allowance)).isoformat()
        atomic(self.path, state)
        return allowance


def assert_night002_admission(root, experiment, phase, keys):
    """Require the exact live outer reservation and its private process token."""
    path = Path(root) / 'local/night-002/program-budget.json'
    require(path.is_file(), 'No persistent NIGHT-002 admission')
    state = read(path)
    require(state['experiment'] == PROGRAM and state['limits'] == CAPS and
            state['limit_seconds'] == CHILD_SECONDS and state['absolute_deadline_utc'] == DEADLINE and
            state['artifact_limit_bytes'] == ARTIFACT_LIMIT_BYTES,
            'NIGHT-002 program identity/limits changed')
    require(phase in ('technical', 'main'), 'No NIGHT-002 native preparation route')
    active = state['active']
    require(active and not state['halted'] and active['name'] == experiment + '/' + phase,
            'No matching active NIGHT-002 phase')
    qualified = [experiment + ':' + key for key in keys]
    require(qualified and len(set(qualified)) == len(qualified) and active['kind'] == phase and
            active['keys'] == qualified, 'NIGHT-002 exact ordered reservation differs')
    token = os.environ.get('NIGHT002_PROGRAM_TOKEN', '')
    require(token and active.get('token_sha256') == sha256(token.encode()).hexdigest() and
            supervisor_alive(active['supervisor_pid']), 'No authenticated live NIGHT-002 supervisor')
    now = utcnow()
    elapsed = (now - datetime.fromisoformat(active['start_utc'])).total_seconds()
    require(now < datetime.fromisoformat(DEADLINE) and
            now < datetime.fromisoformat(active['child_deadline_utc']) and
            state['charged_seconds'] + max(0, elapsed) < CHILD_SECONDS - 5,
            'NIGHT-002 native allowance/deadline exhausted')
    size = assert_artifact_limit(root)
    return dict(operation=active['name'], supervisor_pid=active['supervisor_pid'],
                deadline_utc=DEADLINE, reserved_matches=len(qualified),
                mission_private_bytes=size)

"""Independent fixed-deadline accounting for the NIGHT-002 mission.

NIGHT-001 files and terminal study ledgers are never opened for mutation here.
Every study retains its own narrower budget, publication gates and NativeLease.
"""
from datetime import datetime, timedelta, timezone
from copy import deepcopy
from hashlib import sha256
import json
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
TERMINAL_STUDY = 'MECH-004-SPLIT-R0'
INDEPENDENT_STUDY = 'TACT-003-STLESS-R0'
FAILED_GLOBAL_SHA256 = 'dad11f1be95f9bbccff8e9b62079d943af63cbd3828790e96f07809986bad114'
FAILED_CHARGED_SECONDS = 589.7353507000007


def utcnow():
    return datetime.now(timezone.utc)


def artifact_bytes(directory):
    """Count the whole mission tree; reject links/reparse points and escapes."""
    directory = Path(directory)
    try:
        root_stat = directory.lstat()
    except FileNotFoundError:
        return 0
    def safe(value):
        require(not stat.S_ISLNK(value.st_mode) and not (getattr(value, 'st_file_attributes', 0) & 0x400),
                'Mission artifact links/reparse points are forbidden')
    safe(root_stat)
    if stat.S_ISREG(root_stat.st_mode):return root_stat.st_size
    require(stat.S_ISDIR(root_stat.st_mode), 'Mission artifact root must be a directory')
    root = directory.resolve()  # One canonical root; never resolve vanished leaves.
    def scan(parent):
        total = 0
        try:
            with os.scandir(parent) as entries:
                for entry in entries:
                    try:value = entry.stat(follow_symlinks=False)
                    except FileNotFoundError:continue  # Legitimate pending-marker removal.
                    safe(value)
                    if stat.S_ISDIR(value.st_mode):total += scan(entry.path)
                    elif stat.S_ISREG(value.st_mode):total += value.st_size
        except FileNotFoundError:
            return total
        return total
    return scan(root)


def assert_artifact_limit(root):
    size = artifact_bytes(Path(root) / 'local/night-002')
    require(size < ARTIFACT_LIMIT_BYTES, 'NIGHT-002 cumulative private artifact limit reached')
    return size


# Study runners use the same mission-wide check before every native admission.
check_artifacts = assert_artifact_limit


def assert_study_allowed(state, experiment):
    require(experiment != TERMINAL_STUDY and experiment not in state.get('terminal_studies', []),
            'Terminal study permanently denied; no resume')
    if state.get('reconciliations'):
        require(experiment == INDEPENDENT_STUDY, 'Only the independently released TACT study may continue')


def reconcile_terminal_state(before_bytes, expected_sha256, proof, review, binding):
    """Pure one-time state transition; no file, process, lease or native action.

    The failed study retains its own halted ledger. Every original mission
    field except the administrative halt is preserved exactly, including the
    failed operation, all545 reserved jobs and all elapsed charges.
    """
    require(type(before_bytes) is bytes and sha256(before_bytes).hexdigest() == expected_sha256 == proof['global_budget_sha256'],
            'Failed global budget SHA differs; no reconciliation')
    state = json.loads(before_bytes)
    require(state['experiment'] == PROGRAM and state['limits'] == CAPS and state['limit_seconds'] == CHILD_SECONDS and
            state['absolute_deadline_utc'] == DEADLINE and state['artifact_limit_bytes'] == ARTIFACT_LIMIT_BYTES and
            state['active'] is None and state['halted'] is True and state['charged_seconds'] == FAILED_CHARGED_SECONDS and
            not state.get('terminal_studies') and not state.get('reconciliations'), 'Not the exact unreconciled failed mission')
    ops = state['operations'];reserved = state['reserved']
    require([o['name'] for o in ops] == [TERMINAL_STUDY+'/technical', TERMINAL_STUDY+'/main'] and
            [o['returncode'] for o in ops] == [0, 1] and all(o['timed_out'] is False for o in ops) and
            sum(o['elapsed_seconds'] for o in ops) == state['charged_seconds'], 'Original failed operations/charges differ')
    require(len(reserved) == 545 and {kind:sum(v == kind for v in reserved.values()) for kind in CAPS} ==
            {'technical':33, 'main':512} and all(k.startswith(TERMINAL_STUDY+':') for k in reserved) and
            {key:op['kind'] for op in ops for key in op['keys']} == reserved and
            all(len(op['keys']) == len(set(op['keys'])) for op in ops), 'Original reserved jobs changed/refunded')
    require(proof['experiment_id'] == TERMINAL_STUDY and proof['terminal_closed'] is True and
            proof['scientific_series_complete'] is False and proof['allow_resume'] is False and
            proof['cleanup_verified'] is True and proof['archive_restored'] is True and
            proof['global_charged_seconds'] == state['charged_seconds'] and
            proof['global_reserved_counts'] == {'technical':33, 'main':512}, 'Terminal cleanup/prohibition proof differs')
    require(all(proof[key] == value for key, value in (
            ('main_planned',512),('technical_planned_jobs',33),('main_accepted',224),
            ('main_failed_before_native',1),('main_not_started',287),('native_calls',257),
            ('kernel_active_processes',0),('pending_markers',0),('archive_entries_restored',1024))) and
            proof['global_lease_absent'] is True, 'Terminal job/cleanup coverage differs')
    require(review['experiment_id'] == TERMINAL_STUDY and review['terminal_cleanup_verified'] is True and
            review['independent_study_only'] == INDEPENDENT_STUDY and review['no_original_study_resumption'] is True and
            review['scientific_analysis_allowed'] is False and
            review['termination_sha256'] == binding['termination_sha256'] and
            review['review_sha256'] == binding['review_sha256'], 'Independent terminal review binding differs')
    result = deepcopy(state);result['halted'] = False
    result['terminal_studies'] = [TERMINAL_STUDY]
    result['reconciliations'] = [dict(failed_study=TERMINAL_STUDY, independent_study_only=INDEPENDENT_STUDY,
        before_budget_sha256=expected_sha256, **binding)]
    require(all(result[key] == value for key, value in state.items() if key != 'halted'),
            'Reconciliation attempted to alter original mission accounting')
    return result


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
        assert_study_allowed(state, name.split('/')[0])
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
    assert_study_allowed(state, experiment)
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

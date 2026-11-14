"""Fixed-deadline outer accounting for the user-authorized night research program.

This is not a native runner or lease. Every admitted study still needs its own
preregistration, published gates, inner budget and central NativeLease. The outer
budget additionally prevents separate study processes from extending midnight
or collectively exceeding the declared supervised-child allowance.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
from hashlib import sha256
import os

from .budget import NativeBudget, atomic, supervisor_alive
from .native import require, read

DEADLINE = '2026-11-14T23:00:00+00:00'
CAPS = {'technical': 192, 'main': 2048}
CHILD_SECONDS = 1800


def utcnow():
    return datetime.now(timezone.utc)


class NightBudget(NativeBudget):
    def __init__(self, path, deadline=DEADLINE):
        path = Path(path)
        self.deadline = deadline
        end = datetime.fromisoformat(deadline)
        require(end.tzinfo is not None and end.utcoffset() == timedelta(0),
                'An explicit immutable UTC deadline is required')
        new = not path.exists()
        super().__init__(path, experiment='NIGHT-001', seconds=CHILD_SECONDS, caps=CAPS)
        if new:
            state = self.load()
            state.update(absolute_deadline_utc=deadline, first_operation_utc=None)
            atomic(self.path, state)
        require(self.load().get('absolute_deadline_utc') == deadline,
                'Program deadline changed; retain the original budget')

    def reserve(self, name, kind, keys):
        state = self.load()
        require(state['absolute_deadline_utc'] == self.deadline, 'Program deadline changed')
        now = utcnow()
        end = datetime.fromisoformat(state['absolute_deadline_utc'])
        remaining = (end - now).total_seconds() - 5
        require(remaining > 0, 'Midnight deadline reached; no new native operation')
        allowance = min(remaining, super().reserve(name, kind, keys))
        state = self.load()
        if state['first_operation_utc'] is None:
            state['first_operation_utc'] = now.isoformat()
        state['active']['child_deadline_utc'] = (now + timedelta(seconds=allowance)).isoformat()
        atomic(self.path, state)
        return allowance


def assert_night_admission(root, experiment, phase, keys):
    """Bind an inner study process to an authenticated live outer reservation.

    The bootstrap preserves the outer token under a separate name before an
    inner NativeBudget generates its own TACT_P0_SUPERVISOR_TOKEN. Reading this
    proof neither creates nor repairs a missing/interrupted program budget.
    """
    path = Path(root)/'local/night-001/program-budget.json'
    require(path.is_file(), 'No persistent night program admission')
    state = read(path)
    require(state['experiment']=='NIGHT-001' and state['limits']==CAPS and
            state['limit_seconds']==CHILD_SECONDS and state['absolute_deadline_utc']==DEADLINE,
            'Night program identity/limits changed')
    active = state['active']
    require(active and not state['halted'] and active['name']==experiment+'/'+phase,
            'No matching active night phase')
    kind = 'main' if phase=='main' else 'technical'
    qualified = [experiment+':'+key for key in keys]
    require(len(set(qualified))==len(qualified) and active['kind']==kind and
            set(active['keys'])==set(qualified), 'Night match reservation differs')
    token = os.environ.get('NIGHT_PROGRAM_TOKEN','')
    require(token and active.get('token_sha256')==sha256(token.encode()).hexdigest() and
            supervisor_alive(active['supervisor_pid']), 'No authenticated live outer supervisor')
    now = utcnow()
    require(now < datetime.fromisoformat(DEADLINE) and
            now < datetime.fromisoformat(active['child_deadline_utc']),
            'Outer native allowance/deadline exhausted')
    return dict(operation=active['name'], supervisor_pid=active['supervisor_pid'],
                deadline_utc=DEADLINE, reserved_matches=len(qualified))

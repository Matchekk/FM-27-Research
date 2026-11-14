"""Fixed-deadline outer accounting for the user-authorized night research program.

This is not a native runner or lease. Every admitted study still needs its own
preregistration, published gates, inner budget and central NativeLease. The outer
budget additionally prevents separate study processes from extending midnight
or collectively exceeding the declared supervised-child allowance.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .budget import NativeBudget, atomic
from .native import require

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

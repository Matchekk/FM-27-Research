"""A fixed study-wide UTC deadline in addition to the existing child-time cap."""
from datetime import datetime, timedelta, timezone

from .budget import NativeBudget, atomic
from .native import require


def utcnow():
    return datetime.now(timezone.utc)


class DeadlineBudget(NativeBudget):
    def __init__(self,path,experiment="TACT-001-P1B",seconds=2400,caps=None,wall_seconds=2400):
        new=not path.exists()
        super().__init__(path,experiment,seconds,caps or {"technical":73,"main":2048})
        state=self.load()
        if new:
            state.update(wall_limit_seconds=wall_seconds,wall_start_utc=None,wall_deadline_utc=None)
            atomic(self.path,state)
        require(self.load().get("wall_limit_seconds")==wall_seconds,"Study deadline limit changed")

    def reserve(self,name,kind,keys):
        state=self.load()
        if state["wall_start_utc"] is None:
            start=utcnow()
            state.update(wall_start_utc=start.isoformat(),
                         wall_deadline_utc=(start+timedelta(seconds=state["wall_limit_seconds"])).isoformat())
            atomic(self.path,state)
        remaining=(datetime.fromisoformat(state["wall_deadline_utc"])-utcnow()).total_seconds()-5
        require(remaining>0,"Fixed study UTC deadline exhausted; no new native operation")
        child_allowance=super().reserve(name,kind,keys)
        allowance=min(remaining,child_allowance)
        state=self.load()
        state["active"]["child_deadline_utc"]=(utcnow()+timedelta(seconds=allowance)).isoformat()
        atomic(self.path,state)
        return allowance

"""Separate offline integration of the existing NativeLease and DeadlineBudget.

Only fixed harmless Python children are exposed, never arbitrary commands or an
FM host. The caller supplies a dedicated test coordination directory, not the
actual global native directory used by a live TACT supervisor.
"""
from pathlib import Path
import sys

from .coordination import NativeLease
from .study_budget import DeadlineBudget


PROBES = {"ok": "print('offline-probe-ok')", "fail": "raise SystemExit(7)",
          "hold": "import time; time.sleep(30)"}


def run_probe(artifacts, coordination, name, keys, *, mode="ok", workers=1,
              seconds=30, wall_seconds=60, cap=2):
    """Real exclusive supervision and durable counters around a synthetic child."""
    if mode not in PROBES:
        raise ValueError("Only the fixed offline Python probe modes are permitted")
    artifacts = Path(artifacts).resolve(); artifacts.mkdir(parents=True, exist_ok=True)
    with NativeLease(coordination, "VALID-003-offline", workers):
        budget = DeadlineBudget(artifacts / "budget.json", experiment="VALID-003-offline",
                                seconds=seconds, caps={"technical": cap}, wall_seconds=wall_seconds)
        budget.run(name, "technical", keys, [sys.executable, "-c", PROBES[mode]],
                   artifacts, artifacts / ("probe-" + str(len(budget.load()["operations"])) + ".stdout"))
        return dict(native_processes_started=0, synthetic_python_children=1,
                    charged_seconds=budget.load()["charged_seconds"],
                    reserved_attempts=len(budget.load()["reserved"]),
                    halted=budget.load()["halted"], actual_python_child_workers=1)

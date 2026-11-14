"""Real harmless Python-process integration tests; no FM or live registry."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research.coordination import LeaseBusy, NativeLease
from research.coordination_testpath import run_probe
from research.study_budget import DeadlineBudget

ROOT = Path(__file__).resolve().parents[1]


class CoordinatedBudgetTests(unittest.TestCase):
    def test_fixed_probe_charges_and_reopen_cannot_refund_or_retry(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); shared = root / "shared"; artifacts = root / "study"
            first = run_probe(artifacts, shared, "first", ["a"])
            self.assertEqual(first["native_processes_started"], 0)
            self.assertEqual(first["reserved_attempts"], 1)
            before = json.loads((artifacts / "budget.json").read_text())
            with self.assertRaises(ValueError): run_probe(artifacts, shared, "retry", ["a"])
            run_probe(artifacts, shared, "second", ["b"])
            state = json.loads((artifacts / "budget.json").read_text())
            self.assertEqual(state["wall_deadline_utc"], before["wall_deadline_utc"])
            self.assertGreater(state["charged_seconds"], before["charged_seconds"])
            with self.assertRaises(ValueError): run_probe(artifacts, shared, "overcap", ["c"])
            self.assertEqual(len(json.loads((artifacts / "budget.json").read_text())["reserved"]), 2)

    def test_timeout_stops_real_python_child_and_halts_study(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                run_probe(root / "study", root / "shared", "timeout", ["t"],
                          mode="hold", seconds=5.4, wall_seconds=5.4)
            state = json.loads((root / "study/budget.json").read_text())
            self.assertTrue(state["halted"]); self.assertTrue(state["operations"][0]["timed_out"])
            self.assertIn("t", state["reserved"])
            self.assertFalse((root / "shared/native-execution.lease.json").exists())
            with self.assertRaises(ValueError):
                run_probe(root / "study", root / "shared", "after-timeout", ["u"],
                          seconds=5.4, wall_seconds=5.4)

    def test_existing_real_owner_blocks_probe_before_budget_initialization(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); shared = root / "shared"
            code = "from research.coordination import NativeLease;import sys,time;NativeLease(sys.argv[1],'OTHER',4).acquire();print('ready',flush=True);time.sleep(10)"
            proc = subprocess.Popen([sys.executable, "-c", code, str(shared)], cwd=ROOT,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                self.assertEqual(proc.stdout.readline().strip(), "ready")
                with self.assertRaises(LeaseBusy): run_probe(root / "study", shared, "blocked", ["x"])
                self.assertFalse((root / "study/budget.json").exists())
            finally:
                proc.terminate(); proc.communicate(timeout=5)
            self.assertTrue((shared / "native-execution.lease.json").exists())

    def test_abrupt_supervisor_retains_lease_and_active_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            code = ("from pathlib import Path;from research.coordination import NativeLease;"
                    "from research.study_budget import DeadlineBudget;import os,sys;"
                    "r=Path(sys.argv[1]);NativeLease(r/'shared','CRASH',4).acquire();"
                    "b=DeadlineBudget(r/'study/budget.json',experiment='CRASH',seconds=30,caps={'technical':1},wall_seconds=60);"
                    "b.reserve('pending','technical',['a']);os._exit(23)")
            result = subprocess.run([sys.executable, "-c", code, str(root)], cwd=ROOT, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 23, result.stderr)
            state = json.loads((root / "study/budget.json").read_text())
            self.assertIsNotNone(state["active"]); self.assertIn("a", state["reserved"])
            with self.assertRaises(LeaseBusy): NativeLease(root / "shared", "NEXT").acquire()
            budget = DeadlineBudget(root / "study/budget.json", experiment="CRASH", seconds=30,
                                    caps={"technical": 1}, wall_seconds=60)
            with self.assertRaises(ValueError): budget.reserve("again", "technical", ["b"])

    def test_failure_retains_budget_and_unknown_command_or_workers_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError): run_probe(root / "bad", root / "shared", "bad", [], mode="anything")
            self.assertFalse((root / "bad").exists())
            with self.assertRaises(ValueError): run_probe(root / "bad", root / "shared", "bad", [], workers=5)
            self.assertFalse((root / "bad/budget.json").exists())
            with self.assertRaises(ValueError): run_probe(root / "study", root / "shared", "fail", ["f"], mode="fail")
            state = json.loads((root / "study/budget.json").read_text())
            self.assertTrue(state["halted"]); self.assertEqual(state["operations"][0]["returncode"], 7)


if __name__ == "__main__": unittest.main()

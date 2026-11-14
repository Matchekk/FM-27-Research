"""Offline, opt-in lease tests. No native program or real registry is used."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from research.coordination import LeaseBusy, NativeLease

ROOT = Path(__file__).resolve().parents[1]


class NativeLeaseTests(unittest.TestCase):
    def test_single_shared_lease_blocks_another_process_and_releases(self):
        with tempfile.TemporaryDirectory() as temporary:
            with NativeLease(temporary, "VALID-003", workers=4) as lease:
                self.assertEqual(lease.assert_owned()["workers"], 4)
                code = "from research.coordination import NativeLease,LeaseBusy\ntry: NativeLease(__import__('sys').argv[1],'MECH-001').acquire()\nexcept LeaseBusy: raise SystemExit(17)\nraise SystemExit(1)"
                result = subprocess.run([sys.executable, "-c", code, temporary], cwd=ROOT, capture_output=True, timeout=5)
                self.assertEqual(result.returncode, 17, result.stderr)
            with NativeLease(temporary, "MECH-001") as lease:
                self.assertEqual(lease.assert_owned()["experiment"], "MECH-001")
            self.assertFalse(lease.path.exists())

    def test_crashed_owner_is_retained_without_automatic_takeover(self):
        with tempfile.TemporaryDirectory() as temporary:
            code = "from research.coordination import NativeLease;import os,sys;NativeLease(sys.argv[1],'VALID-003').acquire();os._exit(23)"
            result = subprocess.run([sys.executable, "-c", code, temporary], cwd=ROOT, capture_output=True, timeout=5)
            self.assertEqual(result.returncode, 23, result.stderr)
            path = Path(temporary) / "native-execution.lease.json"
            original = path.read_bytes()
            with self.assertRaises(LeaseBusy):
                NativeLease(temporary, "TRAIN-002").acquire()
            self.assertEqual(path.read_bytes(), original)

    def test_changed_owner_or_corrupt_evidence_never_gets_deleted(self):
        with tempfile.TemporaryDirectory() as temporary:
            lease = NativeLease(temporary, "VALID-003").acquire()
            payload = json.loads(lease.path.read_text())
            payload["owner_token"] = "different-owner"
            lease.path.write_text(json.dumps(payload), encoding="utf8")
            with self.assertRaises(RuntimeError):lease.release()
            self.assertTrue(lease.path.exists())
            lease.path.write_text("incomplete", encoding="utf8")
            with self.assertRaises(RuntimeError):lease.release()
            self.assertTrue(lease.path.exists())

    def test_worker_cap_reentrancy_and_exception_release(self):
        with tempfile.TemporaryDirectory() as temporary:
            for workers in (0,5,True,1.0):
                with self.assertRaises(ValueError):NativeLease(temporary, "VALID-003", workers)
            with self.assertRaisesRegex(ValueError, "required"):NativeLease(temporary, "")
            lease = NativeLease(temporary, "VALID-003")
            with self.assertRaisesRegex(RuntimeError, "body"):
                with lease:
                    with self.assertRaises(RuntimeError):lease.acquire()
                    raise RuntimeError("body")
            self.assertFalse(lease.path.exists())
            with self.assertRaises(RuntimeError):lease.release()


if __name__ == "__main__":unittest.main()

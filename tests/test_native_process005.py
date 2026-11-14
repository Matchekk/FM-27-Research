"""Harmless Windows kernel tests. Never imports or starts the game/engine."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from research import native_process005 as m

BASE = getattr(sys, '_base_executable', sys.executable)


@unittest.skipUnless(os.name == 'nt', 'Windows job-object tests')
class ContainmentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / 'call.stdout'
        self.log = self.root / 'progress.log'
        self.marker = self.root / 'marker.json'

    def tearDown(self):
        self.temp.cleanup()

    def call(self, source, **kwargs):
        return m.contained_call([BASE, '-I', '-c', source], dict(os.environ),
                                self.log, self.output, **kwargs)

    def proof(self):
        return json.loads(self.output.with_suffix('.containment.json').read_text())

    def assert_clean(self, limit=3):
        self.assertTrue(m.confirmed_cleanup(self.output, expected_limit=limit), self.proof())
        self.assertEqual(self.proof()['kernel_active_processes'], 0)
        self.assertTrue(self.proof()['capsule_exit_confirmed'])

    def test_normal_gate_policy_and_direct_base_python(self):
        code, elapsed = self.call(
            "import os; print(os.environ.get('FM27_CONTAINED_CALL_V1')); "
            "print('_FM27_CAPSULE_TOKEN_SHA256' in os.environ)")
        self.assertEqual(code, 0)
        self.assertLess(elapsed, 2)
        self.assertEqual(self.output.read_text().splitlines(), ['1', 'False'])
        self.assert_clean()
        receipt = json.loads(self.output.with_suffix('.process.json').read_text())
        self.assertTrue(receipt['membership_verified_before_go'])
        self.assertEqual(receipt['job_policy']['limit_flags'], 0x2008)
        self.assertFalse(receipt['job_policy']['memory_limit_claimed'])

    def test_assignment_failure_prevents_command(self):
        source = f'from pathlib import Path; Path({str(self.marker)!r}).touch()'
        with patch.object(m._WindowsJob, 'assign', side_effect=OSError('assignment fixture')):
            with self.assertRaises(OSError) as caught:
                self.call(source)
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.proof()['host_start_permission_sent'])
        self.assertTrue(caught.exception.containment_evidence['cleanup_confirmed'])
        self.assert_clean()

    def test_receipt_io_failure_prevents_command(self):
        real = m._write_json
        def fail_process(path, value):
            if str(path).endswith('.process.json'):
                raise OSError('receipt fixture')
            return real(path, value)
        with patch.object(m, '_write_json', side_effect=fail_process):
            with self.assertRaises(OSError):
                self.call(f'from pathlib import Path; Path({str(self.marker)!r}).touch()')
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.proof()['host_start_permission_sent'])
        self.assert_clean()

    def test_callback_error_kills_live_parent_and_descendant(self):
        source = ("import subprocess,time,json,os; from pathlib import Path; "
            f"p=subprocess.Popen([{BASE!r},'-I','-c','import time; time.sleep(5)'],creationflags=0x08000000); "
            f"Path({str(self.marker)!r}).write_text(json.dumps([os.getpid(),p.pid])); time.sleep(5)")
        def callback():
            deadline = time.monotonic()+1
            while not self.marker.exists() and time.monotonic()<deadline:
                time.sleep(.005)
            self.assertTrue(self.marker.exists(), 'harmless descendants did not start')
            raise OSError('callback fixture')
        with self.assertRaises(OSError):
            self.call(source, on_start=callback)
        self.assert_clean()
        self.assertGreaterEqual(self.proof()['kernel_total_processes'], 3)

    def test_progress_stat_error_after_admission_cleans(self):
        with patch.object(m, '_progress_signature', side_effect=OSError('stat fixture')):
            with self.assertRaises(OSError):
                self.call('import time; time.sleep(5)')
        self.assertTrue(self.proof()['host_start_permission_sent'])
        self.assert_clean()

    def test_progress_and_total_timeouts_clean(self):
        with self.assertRaises(TimeoutError):
            self.call('import time; time.sleep(5)', timeout=.15)
        self.assert_clean()
        self.output = self.root / 'total.stdout'
        with self.assertRaises(TimeoutError):
            self.call('import time; time.sleep(5)', timeout=None, total_timeout=.15)
        self.assert_clean()

    def test_early_parent_exit_with_live_child_is_error_and_cleanup(self):
        source = ("import subprocess; "
            f"subprocess.Popen([{BASE!r},'-I','-c','import time; time.sleep(5)'],creationflags=0x08000000)")
        with self.assertRaises(m.ProcessTreeIncomplete):
            self.call(source)
        self.assert_clean()
        self.assertGreaterEqual(self.proof()['kernel_total_processes'], 3)

    def test_nested_child_job_supported_with_three_process_cap(self):
        module = str(Path(m.__file__).resolve())
        source = ("import importlib.util,subprocess; "
            f"s=importlib.util.spec_from_file_location('containment',{module!r}); "
            "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
            "j=m._WindowsJob(1); "
            f"p=subprocess.Popen([{BASE!r},'-I','-c','import time; time.sleep(.05)'],creationflags=0x08000000); "
            "j.assign(p); assert p.wait()==0; j.close()")
        code, _ = self.call(source)
        self.assertEqual(code, 0, self.output.read_text())
        self.assert_clean()
        self.assertGreaterEqual(self.proof()['kernel_total_processes'], 3)

    def test_kernel_limit_blocks_fourth_process_without_relaxation(self):
        source = ("import subprocess,time; "
            f"p=subprocess.Popen([{BASE!r},'-I','-c','import time; time.sleep(.15)'],creationflags=0x08000000); "
            f"q=subprocess.Popen([{BASE!r},'-I','-c','print(123)'],creationflags=0x08000000); "
            "p.wait(); q.wait()")
        try:
            code, _ = self.call(source)
            self.assertNotEqual(code, 0)
        except m.ProcessTreeIncomplete:
            pass
        self.assert_clean()
        # Creation itself is refused; it need not increment termination counters.
        self.assertIn('WinError 1816', self.output.read_text(errors='replace'))

    def test_missing_kernel_zero_proof_retains_unknown_marker(self):
        with patch.object(m._WindowsJob, 'accounting', side_effect=OSError('kernel query fixture')):
            with self.assertRaises(m.CleanupUnconfirmed) as caught:
                self.call('print(1)')
        self.assertFalse(caught.exception.evidence['cleanup_confirmed'])
        self.assertTrue(caught.exception.evidence['kill_close_fallback'])
        self.assertFalse(m.confirmed_cleanup(self.output))

    def test_final_receipt_error_still_proves_cleanup_in_exception(self):
        real = m._write_json
        def fail_final(path, value):
            if str(path).endswith('.containment.json'):
                raise OSError('final receipt fixture')
            return real(path, value)
        with patch.object(m, '_write_json', side_effect=fail_final):
            with self.assertRaises(OSError) as caught:
                self.call('print(1)')
        self.assertTrue(caught.exception.containment_evidence['cleanup_confirmed'])
        self.assertFalse(m.confirmed_cleanup(self.output))

    def test_max10_and_strict_validation(self):
        self.assertEqual(self.call('print(1)', timeout=None, total_timeout=2, max_processes=10)[0], 0)
        self.assert_clean(10)
        for kwargs in ({'max_processes': True}, {'max_processes': 2}, {'max_processes': 11},
                       {'timeout': None}, {'timeout': float('nan')}, {'timeout': False}):
            with self.assertRaises(ValueError):
                self.call('print(1)', **kwargs)

    def test_helper_rejects_malformed_or_boolean_zero(self):
        receipt = self.output.with_suffix('.containment.json')
        for value in ([], None, {'job_policy': None}, {'cleanup_confirmed': True,
                'capsule_exit_confirmed': True, 'kernel_active_processes': False}):
            receipt.write_text(json.dumps(value))
            self.assertFalse(m.confirmed_cleanup(self.output))


if __name__ == '__main__':
    unittest.main()

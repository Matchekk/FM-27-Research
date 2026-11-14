"""Independent regressions for night accounting; harmless temporary metadata only."""
from datetime import datetime
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from analysis.review_night001 import audit_public
from research.night_control import NightBudget


class NightIndependentReviewTests(unittest.TestCase):
    def test_public_dossier_consistent_without_release(self):
        report = audit_public()
        self.assertTrue(report['public_dossier_consistent'])
        self.assertEqual(report['observer_total_probe_plan'], 20)
        self.assertEqual(report['career_not_started'], 11)
        self.assertFalse(report['native_release_granted'])
        self.assertFalse(report['main_release_granted'])

    def test_failed_child_retained_and_blocks_another_study(self):
        with tempfile.TemporaryDirectory() as directory:
            budget = NightBudget(Path(directory)/'budget.json')
            when = datetime.fromisoformat('2026-11-14T20:00:00+00:00')
            with patch('research.night_control.utcnow',return_value=when):
                budget.reserve('A/technical','technical',['A:one'])
                budget.finish(9.5,1)
                before = budget.path.read_bytes()
                with self.assertRaises(ValueError):
                    NightBudget(budget.path).reserve('B/technical','technical',['B:two'])
            self.assertEqual(before,budget.path.read_bytes())
            self.assertTrue(budget.load()['halted'])
            self.assertEqual(budget.load()['charged_seconds'],9.5)
            self.assertEqual(budget.load()['reserved'],{'A:one':'technical'})

    def test_cumulative_caps_refuse_later_study_without_refund(self):
        with tempfile.TemporaryDirectory() as directory:
            budget = NightBudget(Path(directory)/'budget.json')
            when = datetime.fromisoformat('2026-11-14T20:00:00+00:00')
            with patch('research.night_control.utcnow',return_value=when):
                budget.reserve('A/technical','technical',[f'A:{i}' for i in range(192)])
                budget.finish(1,0)
                before = budget.path.read_bytes()
                with self.assertRaisesRegex(ValueError,'cap exceeded'):
                    budget.reserve('B/technical','technical',['B:one'])
            self.assertEqual(before,budget.path.read_bytes())
            self.assertEqual(len(budget.load()['reserved']),192)

    @unittest.skipUnless(os.name=='nt','Windows kernel containment')
    def test_observer_receipt_failure_cleans_before_releasing_marker(self):
        from analysis import run_observer005 as runner
        from research import native_process005 as containment
        with tempfile.TemporaryDirectory() as directory:
            local=Path(directory);output=local/'call.stdout';marker=local/'must-not-start'
            actual=containment._write_json
            def fail_receipt(path,value):
                if str(path).endswith('.process.json'):raise OSError('independent receipt fixture')
                return actual(path,value)
            command=[sys._base_executable,'-I','-c',f'from pathlib import Path;Path({str(marker)!r}).touch()']
            with patch.object(runner,'LOCAL',local),patch.object(containment,'_write_json',side_effect=fail_receipt):
                with self.assertRaises(OSError):runner.native_call(command,dict(os.environ),local/'progress',output)
            self.assertFalse(marker.exists())
            self.assertTrue(containment.confirmed_cleanup(output,expected_limit=3))
            self.assertFalse((local/'native-cleanup-pending.json').exists())

    @unittest.skipUnless(os.name=='nt','Windows kernel containment')
    def test_observer_poll_exception_after_go_confirms_zero_and_clears_marker(self):
        from analysis import run_observer005 as runner
        from research import native_process005 as containment
        real_popen=containment.subprocess.Popen
        def faulting_popen(*args,**kwargs):
            process=real_popen(*args,**kwargs);actual=process.poll;first=True
            def poll():
                nonlocal first
                if first:
                    first=False
                    raise OSError('independent poll fixture')
                return actual()
            process.poll=poll
            return process
        with tempfile.TemporaryDirectory() as directory:
            local=Path(directory);output=local/'poll.stdout'
            with patch.object(runner,'LOCAL',local),patch.object(containment.subprocess,'Popen',side_effect=faulting_popen):
                with self.assertRaises(OSError):
                    runner.native_call([sys._base_executable,'-I','-c','import time;time.sleep(2)'],
                                       dict(os.environ),local/'progress',output)
            self.assertTrue(containment.confirmed_cleanup(output,expected_limit=3))
            self.assertFalse((local/'native-cleanup-pending.json').exists())


if __name__ == '__main__':
    unittest.main()

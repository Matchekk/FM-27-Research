"""Independent regressions for night accounting; harmless temporary metadata only."""
from datetime import datetime
from pathlib import Path
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


if __name__ == '__main__':
    unittest.main()

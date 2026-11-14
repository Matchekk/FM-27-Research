from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from research.night_control import NightBudget, DEADLINE


class NightControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'program.json'

    def test_immutable_midnight_survives_reopen(self):
        budget = NightBudget(self.path)
        self.assertEqual(budget.load()['absolute_deadline_utc'], DEADLINE)
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'deadline changed'):
            NightBudget(self.path, '2026-11-15T23:00:00+00:00')
        self.assertEqual(before, self.path.read_bytes())

    def test_midnight_bounds_child_even_with_unused_native_allowance(self):
        budget = NightBudget(self.path)
        with patch('research.night_control.utcnow', return_value=datetime.fromisoformat('2026-11-14T22:59:45+00:00')):
            self.assertEqual(budget.reserve('study/technical', 'technical', ['unique-job']), 10)
        self.assertEqual(budget.load()['active']['child_deadline_utc'], '2026-11-14T22:59:55+00:00')
        self.assertEqual(budget.load()['reserved'], {'unique-job': 'technical'})

    def test_after_deadline_rejects_without_mutation(self):
        budget = NightBudget(self.path)
        before = self.path.read_bytes()
        with patch('research.night_control.utcnow', return_value=datetime.fromisoformat(DEADLINE)):
            with self.assertRaisesRegex(ValueError, 'Midnight'):
                budget.reserve('late', 'main', ['late-job'])
        self.assertEqual(before, self.path.read_bytes())

    def test_new_study_cannot_refund_or_repeat_prior_phase(self):
        budget = NightBudget(self.path)
        with patch('research.night_control.utcnow', return_value=datetime.fromisoformat('2026-11-14T20:00:00+00:00')):
            budget.reserve('study-a/technical', 'technical', ['a1'])
            budget.finish(100, 0)
            reopened = NightBudget(self.path)
            before = self.path.read_bytes()
            with self.assertRaises(ValueError):
                reopened.reserve('study-a/technical', 'technical', ['a1'])
            self.assertEqual(before, self.path.read_bytes())
            self.assertEqual(reopened.reserve('study-b/technical', 'technical', ['b1']), 1695)
        self.assertEqual(reopened.load()['reserved'], {'a1': 'technical', 'b1': 'technical'})

    def test_crash_or_failed_child_blocks_other_studies(self):
        budget = NightBudget(self.path)
        with patch('research.night_control.utcnow', return_value=datetime.fromisoformat('2026-11-14T20:00:00+00:00')):
            budget.reserve('first', 'technical', ['first-job'])
            before = self.path.read_bytes()
            with self.assertRaises(ValueError):
                NightBudget(self.path).reserve('next', 'technical', ['next-job'])
            self.assertEqual(before, self.path.read_bytes())
            budget.finish(1, 1)
            with self.assertRaises(ValueError):
                NightBudget(self.path).reserve('next', 'technical', ['next-job'])


if __name__ == '__main__':
    unittest.main()

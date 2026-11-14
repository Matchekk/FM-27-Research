from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from hashlib import sha256
import os
from contextlib import redirect_stderr
import io

from research.night_control import NightBudget, DEADLINE, assert_night_admission
from research.budget import atomic


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

    def test_admission_binds_outer_token_live_parent_phase_and_exact_keys(self):
        root=Path(self.temp.name)
        budget=NightBudget(root/'local/night-001/program-budget.json')
        when=datetime.fromisoformat('2026-11-14T20:00:00+00:00')
        with patch('research.night_control.utcnow',return_value=when):
            budget.reserve('STUDY/technical','technical',['STUDY:job'])
        state=budget.load()
        state['active']['token_sha256']=sha256(b'unit-test-token').hexdigest()
        atomic(budget.path,state)
        before=budget.path.read_bytes()
        with patch.dict(os.environ,{'NIGHT_PROGRAM_TOKEN':'unit-test-token'}), \
             patch('research.night_control.utcnow',return_value=when), \
             patch('research.night_control.supervisor_alive',return_value=True):
            proof=assert_night_admission(root,'STUDY','technical',['job'])
            self.assertEqual(proof['reserved_matches'],1)
            self.assertNotIn('token',proof)
            for study,phase,keys in [('OTHER','technical',['job']),('STUDY','main',['job']),
                                      ('STUDY','technical',[]),('STUDY','technical',['job','job'])]:
                with self.assertRaises(ValueError):
                    assert_night_admission(root,study,phase,keys)
            with patch.dict(os.environ,{'NIGHT_PROGRAM_TOKEN':'incorrect'}):
                with self.assertRaises(ValueError):
                    assert_night_admission(root,'STUDY','technical',['job'])
            with patch('research.night_control.supervisor_alive',return_value=False):
                with self.assertRaises(ValueError):
                    assert_night_admission(root,'STUDY','technical',['job'])
            with patch('research.night_control.utcnow',return_value=datetime.fromisoformat(DEADLINE)):
                with self.assertRaises(ValueError):
                    assert_night_admission(root,'STUDY','technical',['job'])
        self.assertEqual(before,budget.path.read_bytes())

    def test_program_cli_requires_explicit_separator_for_inner_arguments(self):
        from analysis.night_supervise import parse_cli
        args,extra=parse_cli(['run','--study','VALID-005-OBSERVER-V1','--phase','prepare',
                             '--','--observer-host','private-placeholder.exe'])
        self.assertEqual(args.phase,'prepare')
        self.assertEqual(extra,['--observer-host','private-placeholder.exe'])
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            parse_cli(['run','--study','VALID-005-OBSERVER-V1','--observer-host','unexpected.exe'])

    def test_preparation_native_loader_cannot_escape_reservations(self):
        from analysis.night_supervise import validate_phase_keys
        validate_phase_keys('VALID-005-OBSERVER-V1','prepare',[])
        validate_phase_keys('MECH-003-STAMINA-R0','prepare',['loader-check-image-prepare'])
        for study,phase,keys in [('MECH-003-STAMINA-R0','prepare',[]),
                ('VALID-005-OBSERVER-V1','prepare',['undeclared']),
                ('MECH-003-STAMINA-R0','main',[]),
                ('MECH-003-STAMINA-R0','technical',['a','a'])]:
            with self.assertRaises(ValueError):validate_phase_keys(study,phase,keys)

    def test_startpolicy_route_forbids_main_and_requires_exact_seventeen_keys(self):
        from analysis.night_supervise import validate_phase_keys
        study='MECH-002-STARTPOLICY-TECH-V1'
        keys=[f'full-{h}-s{s}-sharp{v}-r{r}' for h in ('high_press','deep_block')
              for s in (0,1) for v in (10000,7000) for r in (0,1)]+['negative-malformed']
        validate_phase_keys(study,'prepare',[])
        validate_phase_keys(study,'technical',keys)
        for phase,bad in [('main',keys),('technical',keys[:-1]),('technical',list(reversed(keys)))]:
            with self.assertRaises(ValueError):validate_phase_keys(study,phase,bad)


if __name__ == '__main__':
    unittest.main()

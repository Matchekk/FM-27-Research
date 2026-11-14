"""Offline NIGHT-002 deadline, reservation, authentication and route checks."""
from contextlib import redirect_stderr
from datetime import datetime
from hashlib import sha256
from copy import deepcopy
import io
import json
import os
import stat
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from research.budget import atomic
from research.night002_control import (ARTIFACT_LIMIT_BYTES, CHILD_SECONDS, DEADLINE,
    Night002Budget, TERMINAL_STUDY, INDEPENDENT_STUDY, FAILED_CHARGED_SECONDS, artifact_bytes,
    assert_artifact_limit, assert_night002_admission, reconcile_terminal_state)


class Night002ControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'local/night-002/program-budget.json'
        self.when = datetime.fromisoformat('2026-11-14T23:10:00+00:00')

    def test_new_mission_cannot_reopen_old_budget_or_extend_deadline(self):
        budget = Night002Budget(self.path)
        self.assertEqual(budget.load()['limit_seconds'], 3600)
        self.assertEqual(budget.load()['limits'], {'technical': 192, 'main': 2048})
        before = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'fixed deadline changed'):
            Night002Budget(self.path, '2026-11-15T08:00:00+00:00')
        self.assertEqual(before, self.path.read_bytes())
        state = budget.load();state['experiment'] = 'NIGHT-001';atomic(self.path, state)
        with self.assertRaisesRegex(ValueError, 'identity/limits differ'):
            Night002Budget(self.path)

    def test_absolute_cutoff_bounds_child_and_rejects_late_without_mutation(self):
        budget = Night002Budget(self.path)
        with patch('research.night002_control.utcnow', return_value=datetime.fromisoformat('2026-11-15T06:59:45+00:00')):
            self.assertEqual(budget.reserve('study/technical', 'technical', ['job']), 10)
        self.assertEqual(budget.load()['active']['child_deadline_utc'], '2026-11-15T06:59:55+00:00')
        fresh = Night002Budget(self.root / 'other.json');before = fresh.path.read_bytes()
        with patch('research.night002_control.utcnow', return_value=datetime.fromisoformat(DEADLINE)):
            with self.assertRaisesRegex(ValueError, 'fixed deadline reached'):
                fresh.reserve('late', 'main', ['late'])
        self.assertEqual(before, fresh.path.read_bytes())

    def test_cumulative_caps_time_and_no_retry(self):
        budget = Night002Budget(self.path)
        with patch('research.night002_control.utcnow', return_value=self.when):
            budget.reserve('a/technical', 'technical', [str(i) for i in range(192)])
            budget.finish(100, 0)
            self.assertEqual(budget.load()['charged_seconds'], 100)
            for name, kind, keys in [('a/technical', 'technical', ['0']),
                                      ('b/technical', 'technical', ['new'])]:
                with self.assertRaises(ValueError):budget.reserve(name, kind, keys)
            self.assertEqual(budget.reserve('b/main', 'main', ['m']), CHILD_SECONDS - 105)
            budget.finish(10, 1)
            with self.assertRaises(ValueError):Night002Budget(self.path).reserve('c/main', 'main', ['n'])

    def test_live_outer_token_exact_order_deadline_and_total_time(self):
        budget = Night002Budget(self.path)
        with patch('research.night002_control.utcnow', return_value=self.when):
            budget.reserve('STUDY/technical', 'technical', ['STUDY:a', 'STUDY:b'])
        state = budget.load()
        state['active']['start_utc'] = self.when.isoformat()
        state['active']['token_sha256'] = sha256(b'unit-token').hexdigest()
        atomic(self.path, state);before = self.path.read_bytes()
        with patch.dict(os.environ, {'NIGHT002_PROGRAM_TOKEN': 'unit-token'}), \
             patch('research.night002_control.utcnow', return_value=self.when), \
             patch('research.night002_control.supervisor_alive', return_value=True):
            proof = assert_night002_admission(self.root, 'STUDY', 'technical', ['a', 'b'])
            self.assertEqual(proof['reserved_matches'], 2)
            self.assertNotIn('token', proof)
            for study, phase, keys in [('STUDY', 'technical', ['b', 'a']),
                    ('STUDY', 'technical', ['a']), ('STUDY', 'main', ['a', 'b']),
                    ('OTHER', 'technical', ['a', 'b']), ('STUDY', 'prepare', [])]:
                with self.assertRaises(ValueError):assert_night002_admission(self.root, study, phase, keys)
            with patch.dict(os.environ, {'NIGHT002_PROGRAM_TOKEN': '', 'NIGHT_PROGRAM_TOKEN': 'unit-token'}):
                with self.assertRaisesRegex(ValueError, 'authenticated'):
                    assert_night002_admission(self.root, 'STUDY', 'technical', ['a', 'b'])
            with patch('research.night002_control.supervisor_alive', return_value=False):
                with self.assertRaises(ValueError):assert_night002_admission(self.root, 'STUDY', 'technical', ['a', 'b'])
            state['charged_seconds'] = CHILD_SECONDS - 5;atomic(self.path, state)
            with self.assertRaisesRegex(ValueError, 'allowance/deadline'):
                assert_night002_admission(self.root, 'STUDY', 'technical', ['a', 'b'])
        self.assertNotEqual(before, self.path.read_bytes())

    def test_artifacts_are_global_across_studies_and_rechecked(self):
        (self.root / 'local/night-002/study-a').mkdir(parents=True)
        (self.root / 'local/night-002/study-b').mkdir()
        (self.root / 'local/night-002/study-a/a').write_bytes(b'a' * 5)
        (self.root / 'local/night-002/study-b/b').write_bytes(b'b' * 7)
        self.assertEqual(artifact_bytes(self.root / 'local/night-002'), 12)
        self.assertEqual(assert_artifact_limit(self.root), 12)
        with patch('research.night002_control.ARTIFACT_LIMIT_BYTES', 12):
            with self.assertRaisesRegex(ValueError, 'artifact limit'):assert_artifact_limit(self.root)
        self.assertEqual(ARTIFACT_LIMIT_BYTES, 4 * 1024**3)

    def test_fast_scandir_counts_nested_files_and_rejects_reparse_before_descent(self):
        root=self.root/'nested';(root/'a/b').mkdir(parents=True)
        (root/'a/b/one').write_bytes(b'12345');(root/'two').write_bytes(b'1234567')
        self.assertEqual(artifact_bytes(root),sum(p.stat().st_size for p in root.rglob('*') if p.is_file()))
        fake=SimpleNamespace(path=str(root/'junction'),stat=lambda **kw:SimpleNamespace(st_mode=stat.S_IFDIR,
            st_file_attributes=0x400,st_size=0))
        class Entries:
            def __enter__(self):return iter([fake])
            def __exit__(self,*args):return False
        with patch('research.night002_control.os.scandir',return_value=Entries()) as scan:
            with self.assertRaisesRegex(ValueError,'reparse'):artifact_bytes(root)
            self.assertEqual(scan.call_count,1)

    def test_real_symlink_is_rejected_when_creation_is_permitted(self):
        target=self.root/'target';target.mkdir();link=self.root/'link'
        try:link.symlink_to(target,target_is_directory=True)
        except OSError:self.skipTest('Windows symlink creation privilege unavailable')
        with self.assertRaisesRegex(ValueError,'reparse'):artifact_bytes(link)

    def terminal_fixture(self):
        budget=Night002Budget(self.path);state=budget.load()
        tech=[TERMINAL_STUDY+':t'+str(i) for i in range(33)]
        main=[TERMINAL_STUDY+':m'+str(i) for i in range(512)]
        state.update(halted=True,charged_seconds=FAILED_CHARGED_SECONDS,
            reserved={**dict.fromkeys(tech,'technical'),**dict.fromkeys(main,'main')},
            operations=[dict(name=TERMINAL_STUDY+'/technical',kind='technical',keys=tech,returncode=0,
                timed_out=False,elapsed_seconds=107.96172520000255),
                dict(name=TERMINAL_STUDY+'/main',kind='main',keys=main,returncode=1,
                timed_out=False,elapsed_seconds=481.77362549999816)])
        raw=json.dumps(state).encode();digest=sha256(raw).hexdigest()
        proof=dict(experiment_id=TERMINAL_STUDY,global_budget_sha256=digest,terminal_closed=True,
            scientific_series_complete=False,allow_resume=False,cleanup_verified=True,archive_restored=True,
            global_charged_seconds=FAILED_CHARGED_SECONDS,global_reserved_counts={'technical':33,'main':512},
            main_planned=512,technical_planned_jobs=33,main_accepted=224,main_failed_before_native=1,
            main_not_started=287,native_calls=257,kernel_active_processes=0,pending_markers=0,
            archive_entries_restored=1024,global_lease_absent=True)
        binding=dict(termination_sha256='c'*64,review_sha256='d'*64,publication_commit='a'*40,ci_run=123)
        review=dict(experiment_id=TERMINAL_STUDY,terminal_cleanup_verified=True,independent_study_only=INDEPENDENT_STUDY,
            no_original_study_resumption=True,scientific_analysis_allowed=False,
            termination_sha256='c'*64,review_sha256='d'*64)
        return state,raw,digest,proof,review,binding

    def test_terminal_reconciliation_keeps_all_charges_jobs_and_denies_old_study(self):
        state,raw,digest,proof,review,binding=self.terminal_fixture()
        after=reconcile_terminal_state(raw,digest,proof,review,binding)
        self.assertTrue(state['halted']);self.assertFalse(after['halted'])
        self.assertEqual(after['terminal_studies'],[TERMINAL_STUDY])
        for key,value in state.items():
            if key!='halted':self.assertEqual(after[key],value)
        atomic(self.path,after);before=self.path.read_bytes();budget=Night002Budget(self.path)
        with patch('research.night002_control.utcnow',return_value=self.when):
            with self.assertRaisesRegex(ValueError,'permanently denied'):
                budget.reserve(TERMINAL_STUDY+'/main','main',['retry'])
            self.assertEqual(before,self.path.read_bytes())
            with self.assertRaisesRegex(ValueError,'permanently denied'):
                assert_night002_admission(self.root,TERMINAL_STUDY,'main',['retry'])
            budget.reserve(INDEPENDENT_STUDY+'/technical','technical',[INDEPENDENT_STUDY+':new'])
        self.assertEqual(budget.load()['charged_seconds'],FAILED_CHARGED_SECONDS)
        self.assertEqual(len(budget.load()['reserved']),546)

    def test_literal_terminal_ban_also_holds_without_terminal_metadata(self):
        budget=Night002Budget(self.path)
        for terminal in (None,[TERMINAL_STUDY]):
            state=budget.load()
            if terminal is None:state.pop('terminal_studies',None)
            else:state['terminal_studies']=terminal
            atomic(self.path,state);before=self.path.read_bytes()
            with self.assertRaisesRegex(ValueError,'permanently denied'):
                budget.reserve(TERMINAL_STUDY+'/main','main',['never'])
            with self.assertRaisesRegex(ValueError,'permanently denied'):
                assert_night002_admission(self.root,TERMINAL_STUDY,'main',['never'])
            self.assertEqual(before,self.path.read_bytes())

    def test_terminal_reconciliation_rejects_wrong_sha_cleanup_or_reservation_drift_without_mutation(self):
        state,raw,digest,proof,review,binding=self.terminal_fixture()
        for mode in ('sha','cleanup','reserved','resume','review'):
            p,r=deepcopy(proof),deepcopy(review);payload=raw;wanted=digest
            if mode=='sha':wanted='f'*64
            elif mode=='cleanup':p['cleanup_verified']=False
            elif mode=='reserved':
                changed=deepcopy(state);changed['reserved'].pop(next(iter(changed['reserved'])))
                payload=json.dumps(changed).encode();wanted=sha256(payload).hexdigest();p['global_budget_sha256']=wanted
            elif mode=='resume':p['allow_resume']=True
            else:r['terminal_cleanup_verified']=False
            before=(payload,deepcopy(p),deepcopy(r))
            with self.subTest(mode=mode),self.assertRaises(ValueError):
                reconcile_terminal_state(payload,wanted,p,r,binding)
            self.assertEqual((payload,p,r),before)

    def test_tampered_caps_seconds_or_artifact_contract_reject_without_repair(self):
        for key, value in [('limits', {'technical': 193, 'main': 2048}),
                           ('limit_seconds', 3601), ('artifact_limit_bytes', ARTIFACT_LIMIT_BYTES + 1)]:
            with self.subTest(key=key):
                path = self.root / (key + '.json');budget = Night002Budget(path)
                state = budget.load();state[key] = value;atomic(path, state);before = path.read_bytes()
                with self.assertRaises(ValueError):Night002Budget(path)
                self.assertEqual(before, path.read_bytes())
                with patch('research.night002_control.utcnow', return_value=self.when):
                    with self.assertRaises(ValueError):budget.reserve('study/main', 'main', ['unique'])
                self.assertEqual(before, path.read_bytes())

    def test_exact_technical_and_complete_main_route_schedule(self):
        from analysis.night002_supervise import ARMS, CONTEXTS, STUDY, validate_phase_keys
        technical = [f'tech-{c}-s{s}-{a}-r{r}' for c in CONTEXTS for s in (0, 1)
                     for a in ARMS for r in (0, 1)] + ['negative-malformed']
        validate_phase_keys(STUDY, 'technical', technical)
        main = [f'{c}-{1 + i + n * 32}-{s}-{a}' for n, c in enumerate(CONTEXTS)
                for i in range(32) for s in (0, 1) for a in ARMS]
        main.sort(key=lambda key: sha256(key.encode()).digest())
        validate_phase_keys(STUDY, 'main', main)
        for study, phase, keys in [(STUDY, 'prepare', []), ('MECH-003-STAMINA-R0', 'main', main),
                (STUDY, 'technical', technical[:-1]), (STUDY, 'technical', list(reversed(technical))),
                (STUDY, 'main', main[:-1]), (STUDY, 'main', list(reversed(main))),
                (STUDY, 'main', main[:-1] + [main[0]])]:
            with self.assertRaises(ValueError):validate_phase_keys(study, phase, keys)

    def test_cli_forbids_old_routes_prepare_and_unseparated_arguments(self):
        from analysis.night002_supervise import STUDY, parse_cli
        args, extra = parse_cli(['run', '--study', STUDY, '--phase', 'technical', '--', '--publication', 'abc'])
        self.assertEqual(args.phase, 'technical');self.assertEqual(extra, ['--publication', 'abc'])
        for argv in [['run', '--phase', 'prepare'], ['run', '--study', 'MECH-003-STAMINA-R0'],
                     ['run', '--study', STUDY, '--publication', 'abc']]:
            with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):parse_cli(argv)

    def test_forwarding_accepts_only_exact_publication_evidence_no_abbreviated_child(self):
        from analysis.night002_supervise import validate_inner_arguments
        valid = ['--publication', 'a' * 40, '--ci-run', '123']
        validate_inner_arguments(valid)
        validate_inner_arguments(valid[2:] + valid[:2])
        for arguments in [[], valid + ['--child'], valid + ['--chi'],
                ['--pub', 'a' * 40, '--ci-run', '123'],
                ['--publication', 'a' * 40, '--ci-run', '0'],
                ['--publication', 'a' * 7, '--ci-run', '123'],
                ['--publication', 'a' * 40, '--publication', 'a' * 40]]:
            with self.assertRaises(ValueError):validate_inner_arguments(arguments)


if __name__ == '__main__':
    unittest.main()

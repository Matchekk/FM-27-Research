"""No native starts: exact admission plans, environments and legacy dump audits."""
from collections import Counter
from copy import deepcopy
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from analysis import run_observer005 as runner
from research.native import read, write, rows


class ObserverRunnerTests(unittest.TestCase):
    def test_twenty_logical_probes_sixteen_full_four_unique_paired_cells(self):
        plan=runner.jobs([11,22,33,44])
        self.assertEqual(len(plan),20)
        self.assertEqual(len({j['key'] for j in plan}),20)
        self.assertEqual(Counter(j['kind'] for j in plan),{'full':16,'image':2,'negative':2})
        full=[j for j in plan if j['kind']=='full']
        self.assertEqual(Counter(j['seed'] for j in full),{11:4,22:4,33:4,44:4})
        for seed in (11,22,33,44):
            self.assertEqual({j['mode'] for j in full if j['seed']==seed},set(runner.MODES))
        self.assertEqual(plan[-2]['seed'],11)
        self.assertIsNone(plan[-1]['seed'])
        with self.assertRaises(ValueError):runner.jobs([11,11,33,44])

    def test_environment_removes_diagnostic_hooks_and_preserves_master_token(self):
        frozen=dict(identity=dict(engine_sha256='a'*64))
        with patch.dict(os.environ,{'FM27_DESKTOP_STATS_AUDIT':'1','FM27_IMPORT_FMF':'private',
                                    'FM27_PASSIVE_OBSERVER_V1':'2','NIGHT_PROGRAM_TOKEN':'synthetic-only'}), \
             patch.object(runner,'read',return_value=frozen):
            off=runner.clean_environment('observer_off')
            on=runner.clean_environment('observer_on')
            self.assertEqual(off['NIGHT_PROGRAM_TOKEN'],'synthetic-only')
            self.assertNotIn('FM27_PASSIVE_OBSERVER_V1',off)
            self.assertEqual(on['FM27_PASSIVE_OBSERVER_V1'],'1')
            self.assertNotIn('FM27_DESKTOP_STATS_AUDIT',on)
            self.assertNotIn('FM27_IMPORT_FMF',on)
            self.assertEqual(runner.clean_environment('invalid_opt_in')['FM27_PASSIVE_OBSERVER_V1'],'2')

    def test_reference_input_auditor_against_existing_allowed_private_gold(self):
        # Optional local gold. Public CI uses the synthetic/unit suite and archive;
        # this test never starts a runtime or opens a save/PKM.
        folder=runner.ROOT/'local/tact-002-r0/technical/part-000'
        log=folder/'tech-high_press-0-R00-r0.jsonl'
        if not log.exists():self.skipTest('Private historical native gold not on this host')
        config=read(runner.ROOT/'local/tact-001-p1b/configs.json')['high_press-0-D00']
        dump=read(log.with_suffix('.input.json'))
        catalog=read(runner.RUNTIME/'source/tactics_ui/catalog.json')
        maps=[[0,1,2,3,4,9,5,6,7,8,10],[0,1,2,3,4,5,6,7,9,8,10]]
        binary=(runner.ROOT/'local/tact-002-r0/inputs/high_press-0-R00.bin').read_bytes()
        result=runner.audit_input(rows(log),dump,config,binary,catalog,maps)
        self.assertEqual(result['profile_fields_verified'],1058)
        self.assertEqual(result['attribute_values_verified'],3174)
        broken=deepcopy(dump);broken['teams'][0]['players'][1]['attributes'][52]=40
        with self.assertRaises(ValueError):runner.audit_input(rows(log),broken,config,binary,catalog,maps)

    def test_export_before_preparation_keeps_all_unbegun_probes_without_fake_seeds(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp)/'private';public=Path(temp)/'public';local.mkdir();public.mkdir()
            write(local/'budget.json',dict(experiment=runner.EXPERIMENT,limits={'technical':20,'main':0},
                limit_seconds=180,charged_seconds=1.,reserved={},halted=True,active=None,operations=[],
                wall_start_utc=None,wall_deadline_utc=None,wall_limit_seconds=900))
            with patch.object(runner,'LOCAL',local),patch.object(runner,'PUBLIC',public):runner.export()
            accounting=rows(public/'job-accounting.jsonl')
            self.assertEqual(len(accounting),20)
            self.assertTrue(all(j['status']=='not_started' and j['seed'] is None for j in accounting))
            self.assertFalse(read(public/'technical-summary.json')['passed'])

    def test_registration_requires_full_sha_and_successful_exact_ci(self):
        with self.assertRaises(ValueError):runner.register('short',123)
        with patch.object(runner.subprocess,'check_output',return_value=b'{"status":"completed","conclusion":"success","headSha":"wrong"}'):
            with self.assertRaises(ValueError):runner.successful_ci('a'*40,123)

    def test_locked_identity_rejects_fixture_host_and_setup_drift(self):
        frozen=dict(identity=dict(resource_fingerprint='resources',fixture_sha256='fixture',
            adapter_host_sha256='original'),observer_host_sha256='observer',setups={'cell':'binary'},
            configs_sha256='config',catalog_sha256='catalog')
        original=Path('original');observer=Path('observer');fixture=Path('fixture')
        def value(path):
            if path in (original,observer,fixture):return str(path)
            if path.suffix=='.bin':return 'binary'
            return 'catalog'
        with patch.object(runner,'fingerprint',return_value='resources'), \
             patch.object(runner,'config_hash',return_value='config'),patch.object(runner,'read',return_value={}), \
             patch.object(runner,'digest',side_effect=value):
            runner.verify_locked_identity(frozen,original,observer,fixture)
            for changed in (original,observer,fixture,runner.LOCAL/'inputs/cell.bin'):
                with patch.object(runner,'digest',side_effect=lambda p:'drift' if p==changed else value(p)):
                    with self.assertRaises(ValueError):runner.verify_locked_identity(frozen,original,observer,fixture)

    def test_negative_requires_exact_rejection_cause(self):
        runner.audit_negative([dict(event='native_passive_observer_rejected',reason='invalid_opt_in')],'invalid_opt_in',252)
        runner.audit_negative([dict(event='scenario_rejected',stage='header')],'invalid_binary',108)
        for events,mode,code in (([],'invalid_binary',108),
                ([dict(event='native_passive_observer_rejected',reason='unsupported_input_or_engine')],'invalid_opt_in',252),
                ([dict(event='scenario_rejected'),dict(event='natural_match_finished')],'invalid_binary',108)):
            with self.assertRaises(ValueError):runner.audit_negative(events,mode,code)

    def test_supervisor_retains_global_lease_on_unconfirmed_cleanup(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);lease=Mock(spec=runner.NativeLease);lease.acquire.return_value=lease
            lease.assert_owned.return_value=dict(schema=1,experiment=runner.EXPERIMENT,workers=1,owner_pid=123,acquired_utc='synthetic')
            budget=Mock();budget.path=local/'budget.json';budget.load.return_value={'active':None,'halted':True}
            budget.run.side_effect=ValueError('child failed')
            (local/'native-cleanup-pending.json').touch()
            with patch.object(runner,'LOCAL',local),patch.object(runner,'NativeLease',return_value=lease):
                with self.assertRaises(ValueError):runner.supervised_phase(budget,'technical',[],[],local/'proof.json')
            lease.release.assert_not_called()
            state=read(budget.path)
            self.assertTrue(state['cleanup_unconfirmed']);self.assertTrue(state['global_native_lease_retained'])

    def test_wrapper_requires_persisted_cleanup_proof_even_after_normal_return(self):
        from research.native_process005 import CleanupUnconfirmed
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp)
            with patch.object(runner,'LOCAL',local), \
                 patch('research.native_process005.contained_call',return_value=(0,.1)), \
                 patch('research.native_process005.confirmed_cleanup',return_value=False):
                with self.assertRaises(CleanupUnconfirmed):runner.native_call(['harmless'],{},local/'log',local/'stdout')
            self.assertTrue((local/'native-cleanup-pending.json').exists())

    def test_wrapper_confirms_receipt_before_clearing_failed_attempt_marker(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp)
            with patch.object(runner,'LOCAL',local), \
                 patch('research.native_process005.contained_call',side_effect=OSError('receipt failure')), \
                 patch('research.native_process005.confirmed_cleanup',return_value=True):
                with self.assertRaises(OSError):runner.native_call(['harmless'],{},local/'log',local/'stdout')
            self.assertFalse((local/'native-cleanup-pending.json').exists())

    def test_supervisor_releases_after_clean_confirmed_failure(self):
        from unittest.mock import Mock
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);lease=Mock(spec=runner.NativeLease);lease.acquire.return_value=lease
            lease.assert_owned.return_value=dict(schema=1,experiment=runner.EXPERIMENT,workers=1,owner_pid=123,acquired_utc='synthetic')
            budget=Mock();budget.load.return_value={'active':None};budget.run.side_effect=ValueError('confirmed failure')
            with patch.object(runner,'LOCAL',local),patch.object(runner,'NativeLease',return_value=lease):
                with self.assertRaises(ValueError):runner.supervised_phase(budget,'technical',[],[],local/'proof.json')
            lease.release.assert_called_once()

    def test_offline_crash_export_retains_all_probes_and_redacts_active_token(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp)/'private';public=Path(temp)/'public';local.mkdir();public.mkdir()
            state=dict(experiment=runner.EXPERIMENT,limits={'technical':20,'main':0},limit_seconds=180,
                charged_seconds=0.,reserved={'image-reference':'technical'},halted=True,operations=[],
                wall_start_utc=None,wall_deadline_utc=None,wall_limit_seconds=900,
                active=dict(name='technical',kind='technical',keys=['image-reference'],start_utc='synthetic',
                    child_deadline_utc='synthetic',token_sha256='PRIVATE-TEST-TOKEN',supervisor_pid=123))
            write(local/'budget.json',state);before=(local/'budget.json').read_bytes()
            with patch.object(runner,'LOCAL',local),patch.object(runner,'PUBLIC',public), \
                 patch.object(runner.subprocess,'Popen') as process:runner.export()
            process.assert_not_called()
            self.assertEqual((local/'budget.json').read_bytes(),before)
            self.assertEqual(len(rows(public/'job-accounting.jsonl')),20)
            status=read(public/'budget.json')
            self.assertTrue(status['cleanup_unconfirmed']);self.assertTrue(status['charged_seconds_incomplete'])
            self.assertTrue(status['global_native_lease_retained'])
            self.assertNotIn('PRIVATE-TEST-TOKEN',(public/'budget.json').read_text())
            self.assertFalse(read(public/'technical-summary.json')['passed'])


if __name__=='__main__':unittest.main()

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


if __name__=='__main__':unittest.main()

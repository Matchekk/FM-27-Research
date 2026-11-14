"""Own synthetic start-state gates. No game, engine, registry or native launch."""
from collections import Counter
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from analysis import run_startpolicy002 as runner
from analysis.audit_startpolicy002 import rva_slice
from analysis.startpolicy002_budget import RECONCILIATION, budget_evidence
from analysis import startpolicy002_gate as gate
from research.native import read, write
from research.startpolicy import decode_records, encode_records
from tests.test_mech002 import records
from tests.test_passive_observer import fixture


def baseline():
    source = records()
    # Keep the synthetic codec fixture at the actual historical record count.
    source += [(99, 0, i, 0, 0) for i in range(5557-len(source))]
    # This synthetic test has the ordinary D00 lineup; separate codec tests cover
    # nontrivial lineup permutations. No native legality is claimed for fillers.
    source = [(k, s, a, b, a if k == 11 else v) for k, s, a, b, v in source]
    return encode_records(source)


def trace(side=0, level=10000):
    _, evidence = fixture()
    for row in evidence:
        if row.get('event') != 'native_passive_state':
            continue
        for p in row['players']:
            value = level if p['side'] == side and 1 <= p['roster_index'] <= 10 else 10000
            p.update(condition_accumulator_raw=1000000, sharpness_raw=value, sharpness_secondary_raw=value)
            if p['statistics_cache_region_hex'] is not None:
                cache = bytearray(16); cache[9] = 100; cache[10] = (value+50)//100
                p['statistics_cache_region_hex'] = cache.hex()
    return evidence


class StartpolicyTechnicalTests(unittest.TestCase):
    def test_exact_matrix_seeds_and_windows_safe_keys(self):
        plan = gate.jobs([11,22,33,44])
        self.assertEqual([r['key'] for r in plan], gate.technical_keys())
        self.assertEqual(len(plan), 17)
        self.assertEqual(len(set(gate.technical_keys())), 17)
        self.assertTrue(all(not set('<>:"/\\|?*') & set(k) for k in gate.technical_keys()))
        self.assertEqual(Counter(r['kind'] for r in plan), {'full':16, 'negative':1})
        self.assertEqual(Counter(r['seed'] for r in plan), {11:4,22:4,33:4,44:4,None:1})
        for bad in ([1,1,2,3], [1,2,3], [True,2,3,4], [0,2,3,4], [1,2,3,2**32]):
            with self.assertRaises(ValueError): gate.jobs(bad)

    def test_full_default_byte_identity_and_twenty_low_records(self):
        base = baseline()
        for side in (0,1):
            high, report = gate.compile_cell(base, side, 10000)
            self.assertEqual(high, base); self.assertEqual(report['changed_records'], 0)
            low, report = gate.compile_cell(base, side, 7000)
            changes = [(a,b) for a,b in zip(decode_records(base), decode_records(low)) if a != b]
            self.assertEqual(len(changes), 20); self.assertEqual(report['changed_records'], 20)
            self.assertEqual({a[2] for a,b in changes}, set(range(1,11)))
            self.assertTrue(all(a[:2] == (15,side) and a[3] in (16,17) and b[4] == 7000 for a,b in changes))
        source = list(decode_records(base)); source[0] = (61,0,0,0,1)
        with self.assertRaises(ValueError): gate.compile_cell(encode_records(source), 0, 7000)

    def test_profile_and_actual_cache_both_required_at_both_start_stages(self):
        for side in (0,1):
            for level in gate.LEVELS:
                result = gate.audit_start_state(trace(side,level), baseline(), side, level)
                self.assertTrue(result['start_raw_and_cache_transfer_verified'])
                self.assertFalse(result['scientific_main_released'])
                self.assertEqual([c['target_cache8a'] for c in result['captures']], [(level+50)//100]*2)
        for stage in ('prepared','first_advance'):
            for field in ('sharpness_raw','sharpness_secondary_raw','condition_raw','fatigue_raw',
                          'condition_accumulator_raw','sharpness_penalty_raw','statistics_cache_region_hex'):
                evidence = trace(0,7000)
                player = next(r for r in evidence if r.get('stage') == stage)['players'][1]
                player[field] = '00'*16 if field == 'statistics_cache_region_hex' else player[field]+1
                with self.subTest(stage=stage,field=field), self.assertRaises(ValueError):
                    gate.audit_start_state(evidence, baseline(), 0, 7000)

    def test_initial_controls_tf33_identity_and_no_finish_clamp(self):
        high, low = trace(), trace(0,7000)
        self.assertTrue(gate.initial_control_equivalence(high,low)['initial_control_fields_and_raw_tf33_equal'])
        finish = next(r for r in low if r.get('stage') == 'finished')
        finish['players'][1].update(sharpness_raw=7123,sharpness_secondary_raw=7050,
            condition_accumulator_raw=612345,effectiveness_region_hex='ab'*33)
        self.assertTrue(gate.audit_start_state(low,baseline(),0,7000)['start_raw_and_cache_transfer_verified'])
        changed = deepcopy(low)
        next(r for r in changed if r.get('stage') == 'first_advance')['players'][1]['effectiveness_region_hex'] = 'aa'*33
        with self.assertRaises(ValueError): gate.initial_control_equivalence(high,changed)

    def test_repeat_binds_results_and_identified_cache_but_excludes_opaque_region(self):
        first, second = trace(), trace()
        next(r for r in second if r.get('stage') == 'finished')['players'][1]['runtime_near_morale_region_hex'] = 'ab'*0x70
        self.assertTrue(gate.repeat_equivalence(first,second,123)['exact_outcomes_and_identified_fields_equal'])
        next(r for r in second if r.get('stage') == 'finished')['players'][1]['statistics_cache_region_hex'] = '00'*16
        with self.assertRaises(ValueError): gate.repeat_equivalence(first,second,123)
        second = trace(); next(r for r in second if r.get('event') == 'natural_match_finished')['score'] = [9,0]
        with self.assertRaises(ValueError): gate.repeat_equivalence(first,second,123)

    def test_environment_forbids_hooks_and_retains_outer_admission(self):
        with patch.dict(os.environ, {'FM27_EXECUTION':'1', 'FM27_PASSIVE_OBSERVER_V1':'2', 'NIGHT_PROGRAM_TOKEN':'test-only'}):
            env = runner.clean_environment(dict(engine_sha256='a'*64))
        self.assertNotIn('FM27_EXECUTION',env)
        self.assertEqual(env['FM27_PASSIVE_OBSERVER_V1'],'1')
        self.assertEqual(env['NIGHT_PROGRAM_TOKEN'],'test-only')

    def test_native_wrapper_requires_kernel_receipt_on_all_paths(self):
        from research.native_process005 import CleanupUnconfirmed
        with tempfile.TemporaryDirectory() as temp, patch.object(runner,'LOCAL',Path(temp)), \
             patch('research.native_process005.contained_call',return_value=(0,.1)), \
             patch('research.native_process005.confirmed_cleanup',return_value=False):
            with self.assertRaises(CleanupUnconfirmed):
                runner.native_call(['never-executed'],{},Path(temp)/'log',Path(temp)/'out',lambda:None)
            self.assertTrue((Path(temp)/'native-cleanup-pending.json').exists())

    def test_supervisor_keeps_lease_on_incomplete_cleanup_and_never_main(self):
        with tempfile.TemporaryDirectory() as temp:
            local = Path(temp); budget = Mock(); budget.path = local/'budget.json'
            budget.load.return_value = {'active':None, 'halted':True}
            budget.run.side_effect = ValueError('injected child failure')
            lease = Mock(spec=runner.NativeLease); lease.acquire.return_value = lease
            lease.assert_owned.return_value = dict(schema=1,experiment=gate.EXPERIMENT,workers=1,owner_pid=1,acquired_utc='test')
            (local/'native-cleanup-pending.json').touch()
            with patch.object(runner,'LOCAL',local), patch.object(runner,'NativeLease',return_value=lease), \
                 patch.object(runner,'DeadlineBudget',return_value=budget):
                with self.assertRaises(ValueError): runner.supervise()
            lease.release.assert_not_called()
            self.assertTrue(read(budget.path)['global_native_lease_retained'])
            self.assertEqual(budget.run.call_args.args[1:3], ('technical',gate.technical_keys()))

    def test_export_before_preparation_preserves_unbegun_without_seeds(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(runner,'LOCAL',root/'private'), patch.object(runner,'PUBLIC',root/'public'), \
                 patch.object(runner.subprocess,'Popen') as process:
                runner.export()
            process.assert_not_called()
            plan = [json.loads(line) for line in (root/'public/job-accounting.jsonl').read_text().splitlines()]
            self.assertEqual(len(plan),17)
            self.assertTrue(all(p['status'] == 'not_started' and p['seed'] is None for p in plan))
            self.assertFalse(read(root/'public/technical-summary.json')['passed'])
            self.assertTrue(read(root/'public/technical-summary.json')['technical_set_incomplete'])

    def test_public_review_gate_requires_exact_input_and_both_review_hashes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); public = root/'data'; public.mkdir()
            value = dict(experiment_id=gate.EXPERIMENT,approved_for_technical=True,
                         inputs_sha256='frozen',review_sha256='frozen',observer_results_review_sha256='frozen')
            write(public/'review-gate.json',value)
            with patch.object(runner,'PUBLIC',public), patch.object(runner,'source_hash',return_value='frozen'):
                runner.review_gate()
                value['approved_for_technical'] = False; write(public/'review-gate.json',value)
                with self.assertRaises(ValueError): runner.review_gate()

    def test_inner_admission_binds_deadline_token_lease_and_exact_seventeen_keys(self):
        from hashlib import sha256
        future = (datetime.now(timezone.utc)+timedelta(seconds=60)).isoformat()
        state = dict(experiment=gate.EXPERIMENT,limits={'technical':17,'main':0},limit_seconds=180,
            wall_limit_seconds=900,halted=False,wall_deadline_utc=future,
            active=dict(name='technical',kind='technical',keys=gate.technical_keys(),supervisor_pid=1,
                token_sha256=sha256(b'test-only').hexdigest(),child_deadline_utc=future))
        lease = dict(owner_pid=1,experiment=gate.EXPERIMENT,workers=1)
        with patch.object(runner,'read',side_effect=lambda p: deepcopy(lease if p.name.endswith('.lease.json') else state)), \
             patch.object(runner,'supervisor_alive',return_value=True), \
             patch.dict(os.environ,{'TACT_P0_SUPERVISOR_TOKEN':'test-only'}):
            runner.assert_inner_admission()
            for mutate in ('keys','deadline','workers','main'):
                bad = deepcopy(state); bad_lease = deepcopy(lease)
                if mutate == 'keys': bad['active']['keys'] = gate.technical_keys()[:-1]
                elif mutate == 'deadline': bad['active']['child_deadline_utc'] = '2000-01-01T00:00:00+00:00'
                elif mutate == 'workers': bad_lease['workers'] = 4
                else: bad['limits']['main'] = 1
                with patch.object(runner,'read',side_effect=lambda p: deepcopy(bad_lease if p.name.endswith('.lease.json') else bad)):
                    with self.assertRaises(ValueError): runner.assert_inner_admission()

    def test_private_pe_evidence_hashing_maps_raw_sections_without_publishing_bytes(self):
        import struct
        image = bytearray(1024); image[:2] = b'MZ'; struct.pack_into('<I',image,0x3c,64)
        image[64:68] = b'PE\0\0'; struct.pack_into('<H',image,70,1); struct.pack_into('<H',image,84,0)
        struct.pack_into('<4I',image,96,32,0x1000,32,512)
        image[512:516] = b'own!'
        self.assertEqual(rva_slice(image,0x1000,4),b'own!')
        with self.assertRaises(ValueError): rva_slice(image,0x1020,1)

    def test_malformed_header_requires_observed_initial_stage_not_header_label(self):
        rejected = dict(event='scenario_rejected',stage='initial')
        runner.audit_malformed([rejected],108)
        for events, code in (([dict(rejected,stage='header')],108),
                             ([dict(rejected,stage='records')],108), ([rejected],109),
                             ([rejected,dict(event='natural_match_finished')],108),
                             ([rejected,rejected],108), ([],108)):
            with self.subTest(events=events,code=code), self.assertRaises(ValueError):
                runner.audit_malformed(events,code)

    def test_existing_private_malformed_negative_gold(self):
        directory = runner.ROOT/'local/valid005-observer-v1'
        log = directory/'technical/negative-binary.jsonl'
        ledger = directory/'ledger.jsonl'
        if not log.exists() or not ledger.exists():
            self.skipTest('Existing private technical negative gold unavailable')
        from research.native import rows
        observed = [r for r in rows(ledger) if r['key'] == 'negative-binary']
        self.assertEqual(len(observed),1)
        runner.audit_malformed(rows(log),observed[0]['returncode'])

    def test_budget_gate_and_export_reject_postsummary_fail_timeout_unresolved_and_unaccounted(self):
        keys = gate.technical_keys()
        operation = dict(name='technical',kind='technical',keys=keys,start_utc='2026-11-14T12:00:01+00:00',
            child_deadline_utc='2026-11-14T12:02:56+00:00',elapsed_seconds=10.,returncode=0,timed_out=False,
            token_sha256='PRIVATE-TOKEN',stdout='D:/private/forbidden.save')
        valid = dict(experiment=gate.EXPERIMENT,limits={'technical':17,'main':0},limit_seconds=180,
            charged_seconds=10.,reserved={k:'technical' for k in keys},halted=False,active=None,
            operations=[operation],wall_start_utc='2026-11-14T12:00:00+00:00',
            wall_deadline_utc='2026-11-14T12:15:00+00:00',wall_limit_seconds=900)
        receipt = dict(schema=RECONCILIATION,experiment_id=gate.EXPERIMENT,phase='technical',
            completed_utc='2026-11-14T12:00:12+00:00',budget_sha256='a'*64)
        variants = ('valid','child_failure','timeout','unresolved','unaccounted','no_receipt',
                    'charge_refunded','retry','over180','over900','missing_elapsed','missing_budget')
        for variant in variants:
            state, reconciled = deepcopy(valid), deepcopy(receipt)
            if variant == 'child_failure': state['halted']=True; state['operations'][0]['returncode']=1
            elif variant == 'timeout': state['halted']=True; state['operations'][0]['timed_out']=True
            elif variant == 'unresolved': state['active']=deepcopy(operation); state['operations']=[]; state['charged_seconds']=0.
            elif variant == 'unaccounted': state['operations']=[]
            elif variant == 'no_receipt': reconciled=None
            elif variant == 'charge_refunded': state['charged_seconds']=0.
            elif variant == 'retry': state['operations'].append(deepcopy(operation))
            elif variant == 'over180': state['operations'][0]['elapsed_seconds']=181.; state['charged_seconds']=181.
            elif variant == 'over900': reconciled['completed_utc']='2026-11-14T12:15:01+00:00'
            elif variant == 'missing_elapsed': del state['operations'][0]['elapsed_seconds']
            elif variant == 'missing_budget': state=None
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                root=Path(temp); local=root/'private'; public=root/'public'; local.mkdir(); public.mkdir()
                write(public/'job-plan.json',gate.jobs([1,2,3,4]))
                records=[]
                for job in gate.jobs([1,2,3,4]):
                    row=dict(job,status='ok' if job['kind']=='full' else 'expected_rejection')
                    if job.get('repeat') == 1: row['aa']=dict(exact_outcomes_and_identified_fields_equal=True)
                    if job.get('level_raw') == 7000: row['controls']=dict(initial_control_fields_and_raw_tf33_equal=True)
                    records.append(row)
                (local/'ledger.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in records))
                write(local/'technical-summary.json',dict(passed=True))
                if state is not None:
                    write(local/'budget.json',state)
                    from research.native import digest
                    if reconciled is not None:
                        reconciled['budget_sha256']=digest(local/'budget.json')
                        write(local/'technical-reconciled.json',reconciled)
                with patch.object(runner,'LOCAL',local),patch.object(runner,'PUBLIC',public), \
                     patch.object(runner.subprocess,'Popen') as process, patch('builtins.print'):
                    runner.export()
                process.assert_not_called()
                result=read(public/'technical-summary.json'); evidence=read(public/'budget.json')
                self.assertEqual(result['passed'],variant=='valid')
                self.assertEqual(result['budget_gate']['passed'],variant=='valid')
                self.assertEqual(evidence['acceptance']['passed'],variant=='valid')
                self.assertNotIn('PRIVATE-TOKEN',json.dumps(evidence))
                self.assertNotIn('D:/private',json.dumps(evidence))
                self.assertIn('active',evidence); self.assertIn('operations',evidence)
                if variant in ('unaccounted','unresolved','missing_elapsed','missing_budget','retry','charge_refunded'):
                    self.assertIsNone(evidence['charged_seconds'])
                    self.assertTrue(evidence['charged_seconds_incomplete'])

    def test_budget_redaction_rejects_unknown_private_fields_and_preserves_missing_values(self):
        gate_result, public = budget_evidence(dict(active=dict(name='D:/private/hidden',kind='private',
            keys=['D:/private/key'],token_sha256='PRIVATE-TOKEN'),reserved={'D:/private/reserved':'token'},
            operations=[dict(name='D:/private/log',keys=['D:/private/key'],token_sha256='PRIVATE-TOKEN')]),None,None,True)
        self.assertFalse(gate_result['passed'])
        self.assertIsNone(public['charged_seconds'])
        self.assertIsNone(public['operations'][0]['elapsed_seconds'])
        self.assertNotIn('PRIVATE-TOKEN',json.dumps(public))
        self.assertNotIn('D:/private',json.dumps(public))

    def test_failed_child_after_summary_cannot_create_supervisor_reconciliation(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp); write(local/'technical-summary.json',dict(passed=True))
            budget=Mock(); budget.load.return_value=dict(active=None,halted=True)
            budget.run.side_effect=ValueError('child failed after writing its summary')
            lease=Mock(spec=runner.NativeLease); lease.acquire.return_value=lease
            lease.assert_owned.return_value=dict(schema=1,experiment=gate.EXPERIMENT,workers=1,
                                                owner_pid=1,acquired_utc='test')
            with patch.object(runner,'LOCAL',local),patch.object(runner,'DeadlineBudget',return_value=budget), \
                 patch.object(runner,'NativeLease',return_value=lease):
                with self.assertRaises(ValueError): runner.supervise()
            lease.release.assert_called_once()
            self.assertFalse((local/'technical-reconciled.json').exists())


if __name__ == '__main__':
    unittest.main()

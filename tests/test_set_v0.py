"""SET-V0 own synthetic gold and failure tests; never imports/starts a host."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from research.set_v0 import TraceError, capability_manifest, inspect_native_rows, parse_trace
ROOT = Path(__file__).resolve().parents[1]


def cases():
    return json.loads((ROOT/'data/set-v0/gold-cases.json').read_text(encoding='utf8'))['cases']


def trace(name='repeat_goal'):
    return deepcopy(next(c['trace'] for c in cases() if c['name'] == name))


class SetV0Tests(unittest.TestCase):
    def test_all_eleven_independently_authored_synthetic_gold_cases(self):
        data=cases();self.assertEqual(len(data),11)
        for case in data:
            with self.subTest(case=case['name']):
                result=parse_trace(case['trace'])
                self.assertEqual(result['status'],'synthetic_contract_verified')
                self.assertFalse(result['native_validated']);self.assertFalse(result['performance_ready'])
                for key,want in case['expected'].items():
                    if '/' in key:
                        kind,side,field=key.split('/');got=result['by_type'][kind][side][field]
                    else:got=result[key]
                    self.assertAlmostEqual(got,want,msg=key)

    def test_native_boundary_cannot_be_enabled_by_caller_flags(self):
        for origin in ('native','native_normalized',None):
            value=trace();value['origin']=origin
            value.update(native_validated=True,validated=True,gate_sha256='a'*64)
            result=parse_trace(value)
            self.assertEqual(result['status'],'unresolved_native_mapping')
            self.assertIsNone(result['exposures']);self.assertIsNone(result['attribution'])
            self.assertFalse(result['native_validated']);self.assertFalse(result['performance_ready'])
        m=capability_manifest();m['native_validated']=True;m['native_mapping_implemented']=True
        self.assertFalse(capability_manifest()['native_validated'])
        self.assertTrue(all(not v for v in capability_manifest()['native_capabilities'].values()))

    def test_selection_diagnostics_never_produce_exposure(self):
        raw=[dict(event='native_setpiece_selected',side=s,tick=10) for s in (0,1)]
        raw += [dict(event='native_setpiece_executed',validated=True),dict(event='native_xg_models_parsed')]
        r=inspect_native_rows(raw)
        self.assertEqual(r['diagnostics']['selection_messages'],2)
        self.assertEqual(r['diagnostics']['selection_ticks'],1)
        self.assertIsNone(r['exposures']);self.assertFalse(r['performance_ready'])
        self.assertEqual(inspect_native_rows([dict(event='native_setpiece_selected',tick={})])['diagnostics']['invalid_selection_ticks'],1)

    def test_schema_missing_unknown_clock_and_unsafe_ids_rejected(self):
        variants=[]
        t=trace();t['clock']='native_tick_assumed_4hz';variants.append(t)
        t=trace();t['schema']='raw-native';variants.append(t)
        t=trace();t['private_player_id']=123;variants.append(t)
        t=trace();t['match_id']='../private';variants.append(t)
        t=trace();t['events'][0]['type']='native_setpiece_selected';variants.append(t)
        t=trace();t['events'][0]['type']=[];variants.append(t)
        t=trace();del t['events'][0]['side'];variants.append(t)
        t=trace();t['events'][0]['unexpected']=1;variants.append(t)
        for t in variants:
            with self.subTest(trace=t):
                with self.assertRaises(TraceError):parse_trace(t)

    def test_duplicate_ids_missing_closure_and_clock_regression_rejected(self):
        variants=[]
        t=trace();t['events'][1]['id']=t['events'][0]['id'];variants.append(t)
        t=trace();t['events'][1]['ms']=-1;variants.append(t)
        t=trace();t['events'][0]['ms']=200;variants.append(t)
        t=trace();t['events'][1]['ms']=True;variants.append(t)
        t=trace();t['events'][1]['period']=2;variants.append(t)
        t=trace();t['events']=t['events'][:-1];variants.append(t)
        t=trace('selection_abort');t['events'].pop(-2);variants.append(t)
        for t in variants:
            with self.assertRaises(TraceError):parse_trace(t)

    def test_contact_final_legality_repeat_and_possession_are_mandatory(self):
        variants=[]
        t=trace();t['events'][1]['contact_verified']=False;variants.append(t)
        t=trace();t['events'][1]['legal']=None;variants.append(t)
        t=trace();t['events'][2]['repeat_of']='unknown';variants.append(t)
        t=trace();t['events'][2]['reason']='maybe_legal';variants.append(t)
        t=trace('counter_boundary');t['events'][4]['controlled']=None;variants.append(t)
        t=trace('counter_boundary');t['events'][5]['side']=0;variants.append(t)
        for t in variants:
            with self.assertRaises(TraceError):parse_trace(t)

    def test_repeats_require_unbroken_immediate_illegal_predecessor(self):
        variants=[]
        # The independently reproduced defect: a later contact omitted its link.
        t=trace();t['events'][2]['repeat_of']=None;variants.append(t)
        t=trace();t['events'][1]['repeat_of']='try2';variants.append(t)
        t=trace();t['events'][2]['repeat_of']='future_contact';variants.append(t)
        # Three contacts: final contact must name try_mid, never skip back to try1.
        t=trace();mid=deepcopy(t['events'][1])
        mid.update(id='middle_event',execution_id='try_mid',repeat_of='try1',ms=150)
        t['events'].insert(2,mid);variants.append(deepcopy(t))
        valid=deepcopy(t);valid['events'][3]['repeat_of']='try_mid'
        result=parse_trace(valid)
        self.assertEqual(result['attempts'],3);self.assertEqual(result['illegal_attempts'],2)
        self.assertEqual(result['by_type']['corner']['0']['executed'],1)
        t=deepcopy(valid);t['events'][2]['repeat_of']=None;variants.append(t)
        # A first contact of a new award cannot borrow an illegal contact elsewhere.
        t=trace('same_routine_twice');first=t['events'][2]
        first.update(legal=False,reason='repeat')
        abort=dict(id='abort_first',type='abort',period=1,ms=250,award_id='a1',reason='cancelled')
        t['events'].insert(3,abort);t['events'][-2]['repeat_of']='x1';variants.append(t)
        # A legal contact closes the award; a later contact cannot reference it.
        t=trace();t['events'][1].update(legal=True,reason='legal');variants.append(t)
        for broken in variants:
            with self.subTest(events=broken['events']):
                with self.assertRaises(TraceError):parse_trace(broken)

    def test_invalid_xg_goal_score_or_var_never_silently_zeroed(self):
        for value in (float('nan'),float('inf'),-1,1.1,True,10**1000):
            t=trace();t['events'][3]['xg']=value
            with self.assertRaises(TraceError):parse_trace(t)
        variants=[]
        t=trace();t['events'][3]['counted_in_final_xg']=None;variants.append(t)
        t=trace();t['events'][4]['shot_id']='missing';variants.append(t)
        t=trace();t['events'][4]['shot_id']=None;variants.append(t)
        t=trace();t['events'][4]['side']=1;variants.append(t)
        t=trace();t['final_score']=[0,0];variants.append(t)
        t=trace();t['final_score']=[True,0];variants.append(t)
        t=trace('var_cancel');t['events'][5]['goal_id']='missing';variants.append(t)
        t=trace('var_cancel');t['events'][5]['reason']='unknown';variants.append(t)
        for t in variants:
            with self.assertRaises(TraceError):parse_trace(t)

    def test_shot_snapshot_survives_late_final_goal_after_chain_end(self):
        t=trace('counter_boundary')
        t['events'][6]['ms']=14000;t['events'][7]['ms']=14001;t['events'][8]['ms']=15000
        # Goal report is later than counter expiry; its shot was observed at9999ms.
        r=parse_trace(t)
        self.assertEqual(r['by_type']['free_kick']['0']['counter_goals_against'],1)
        self.assertIsNone(r['attribution']['shots']['s3'])

    def test_extra_sampling_and_opposite_view_do_not_duplicate_execution(self):
        t=trace('same_routine_twice')
        extra=deepcopy(t['events'][1]);extra.update(id='opposite_view',view_side=1)
        t['events'].insert(2,extra)
        r=parse_trace(t)
        self.assertEqual(r['selection_messages'],3)
        self.assertEqual(r['by_type']['corner']['0']['executed'],2)

    def test_score_without_standard_is_preserved_but_unattributed(self):
        t=trace('repeat_goal');t['events']=t['events'][3:]
        r=parse_trace(t)
        self.assertEqual(r['final_score'],[1,0]);self.assertIsNone(r['attribution']['goals']['g1'])
        self.assertEqual(r['by_type']['corner']['0']['goals_for'],0)


if __name__=='__main__':unittest.main()

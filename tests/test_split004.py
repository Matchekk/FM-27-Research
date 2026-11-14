"""Synthetic independent-fields and inference checks; no engine invocations."""
from copy import deepcopy
from collections import Counter
import unittest
import numpy as np

from analysis import split004_design as design
from analysis import analyse_split004 as analysis
from research.core import config_hash, schedule
from research.startpolicy import decode_records, encode_records
from tests.test_sharpness002_design import binary_fixture
from tests.test_passive_observer import fixture


def receipt_and_data():
    identity={k:('a'*64 if k.endswith('sha256') or k=='resource_fingerprint' else 'own-synthetic')
        for k in ('build','engine_sha256','adapter_host_sha256','adapter_version','fixture_sha256','resource_fingerprint','lab_version','lab_commit')}
    setups={h:{str(s):{a:config_hash([h,s,a]) for a in design.ARMS} for s in (0,1)} for h in design.CONTEXTS}
    c=design.contract_definition(identity,setups);c['status']='registered'
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['execution']=dict(runner='analysis/run_split004.py',kind='cold_direct_cli',workers=4,max_processes_per_job=3,
        code_sha256={'own-synthetic':'a'*64},input_manifest_sha256='b'*64,seed_plan_sha256='c'*64)
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(100001,100065)));data=[]
    for job in schedule(receipt):
        tr=design.treatment(job['arm']);h=design.CONTEXTS.index(job['scenario']);side=job['side']
        i=receipt['seeds'][h*32:(h+1)*32].index(job['seed']);a,b=tr['levels'].values()
        # Physical marginal effects .21/.41; interaction .12; attribution -.20.
        y=5+(.10+.01*h+.005*(i-15.5)+.04*(2*side-1))*a+(.20+.01*h+.003*(i-15.5))*b+.03*a*b+.1*side
        stats=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(stats),dict(stats)];teams[side]['xg']+=y;score=[0,0];score[side]=int(a==1)
        descriptive={k:0. for k in design.DESCRIPTIVE}
        for stage in ('prepared','first','finished'):
            descriptive[stage+'_condition_cache89_mean']=100.
            # Deliberately unrelated to either raw field: mapping is not imposed.
            descriptive[stage+'_sharpness_cache8a_mean']=83.
        descriptive.update(prepared_tf33_matches_frozen_d00=True,first_tf33_matches_frozen_d00=True,
            finished_tf33_distinct_hashes=1,finished_condition_raw_mean=10000.,finished_sharpness_raw_mean=float(tr['c90_raw']),
            finished_sharpness_secondary_raw_mean=float(tr['c7a_raw']),finished_condition_accumulator_raw_mean=1000000.)
        audit=dict.fromkeys(analysis.AUDIT_BOOLS,True)
        audit.update(attribute_values_verified=3174,profile_fields_verified=1058,phase_cells_verified=44,pi_groups_verified=748,
            c90_raw=tr['c90_raw'],c7a_raw=tr['c7a_raw'],pressing_bit=0)
        data.append(dict(job_id=job['key'],experiment_id=design.EXPERIMENT,context=job['scenario'],team_side=side,
            seed=job['seed'],arm=job['arm'],status='ok',config_sha256=receipt['config_sha256'],setup_sha256=job['setup_sha256'],
            identity=identity,observer_host_sha256=design.OBSERVER_HOST,result=dict(score=score,team_statistics=teams,tick=22000,clock=5400),
            native_audit=audit,descriptive=descriptive,descriptive_missing_reasons={},test_origin='own_synthetic_not_fm'))
    return receipt,data


def split_trace(c90,c7a):
    _,trace=fixture()
    for row in trace:
        if row.get('event')!='native_passive_state':continue
        for p in row['players']:
            p['condition_accumulator_raw']=1000000
            if p['side']==0 and p['roster_index'] in range(1,11):
                p['sharpness_raw']=c90;p['sharpness_secondary_raw']=c7a
            if p['statistics_cache_region_hex'] is not None:
                cache=bytearray(16);cache[9]=100;cache[10]=83;p['statistics_cache_region_hex']=cache.hex()
    binary=encode_records([(11,s,i,0,i) for s in (0,1) for i in range(11)])
    return trace,binary


class Split004Tests(unittest.TestCase):
    def test_compiler_changes_only_individual_original_fields(self):
        for side in (0,1):
            source,_,targets=binary_fixture(side)
            inputs=design.build_inputs(source,side)
            self.assertEqual(inputs[design.ARMS[-1]],source)
            for arm in design.ARMS:
                tr=design.treatment(arm);before=decode_records(source);after=decode_records(inputs[arm])
                diffs=[(a,b) for a,b in zip(before,after,strict=True) if a!=b]
                expected={(15,side,slot,f,v) for slot in targets for f,v in ((16,tr['c90_raw']),(17,tr['c7a_raw'])) if v==7000}
                self.assertEqual({b for a,b in diffs},expected);self.assertEqual(len(diffs),len(expected))
                self.assertTrue(all(a[:4]==b[:4] and a[4]==10000 for a,b in diffs))
                self.assertEqual([v for k,s,a,b,v in after if k==1 and b==52],[60]*46)

    def test_compiler_rejects_nonstandard_baseline_and_noninteger_side(self):
        source,_,_=binary_fixture(0)
        for mutate in ('raw','stamina','execution','duplicate'):
            rows=list(decode_records(source))
            if mutate=='raw':rows=[(k,s,a,b,7000) if (k,s,a,b)==(15,0,0,16) else (k,s,a,b,v) for k,s,a,b,v in rows]
            elif mutate=='stamina':rows=[(k,s,a,b,59) if (k,s,a,b)==(1,0,0,52) else (k,s,a,b,v) for k,s,a,b,v in rows]
            elif mutate=='execution':rows[-1]=(61,0,0,0,1)
            else:rows[-1]=(15,0,0,16,10000)
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):design.build_inputs(encode_records(rows),0)
        with self.assertRaises(ValueError):design.build_inputs(source,True)

    def test_technical_cells_repeat_twice_with_four_disjoint_context_seeds(self):
        jobs=design.technical_jobs([11,12,13,14]);self.assertEqual(len(jobs),33)
        full=jobs[:-1];self.assertEqual(jobs[-1]['key'],'negative-malformed')
        self.assertEqual(set(Counter((j['context'],j['side'],j['arm']) for j in full).values()),{2})
        self.assertEqual(len({j['seed'] for j in full}),4)
        with self.assertRaises(ValueError):design.technical_jobs([11]*4)

    def test_independent_raw_gate_accepts_all_arms_without_cache_mapping(self):
        for arm in design.ARMS:
            tr=design.treatment(arm);trace,binary=split_trace(tr['c90_raw'],tr['c7a_raw'])
            result=design.audit_split_state(trace,binary,0,tr['c90_raw'],tr['c7a_raw'])
            self.assertTrue(result['independent_raw_transfer_verified']);self.assertFalse(result['cache_mapping_assumed'])
            self.assertEqual(result['snapshots'][0]['target_cache8a_values'],[83]*10)

    def test_raw_collapse_changed_controls_gk_and_missing_snapshot_fail(self):
        for mutate in ('collapse','first','gk','control','missing'):
            trace,binary=split_trace(10000,7000)
            capture=next(r for r in trace if r.get('stage')==('first_advance' if mutate=='first' else 'prepared'))
            if mutate in ('collapse','first'):capture['players'][1]['sharpness_secondary_raw']=10000
            elif mutate=='gk':capture['players'][0]['sharpness_secondary_raw']=7000
            elif mutate=='control':capture['players'][1]['condition_accumulator_raw']=999999
            else:trace.remove(capture)
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):design.audit_split_state(trace,binary,0,10000,7000)

    def test_factorial_physical_scaling_attribution_and_holm8(self):
        levels=np.array([[1,*r['levels'].values(),np.prod(list(r['levels'].values()))] for r in design.matrix()])
        np.testing.assert_array_equal(levels.T@levels,np.eye(4)*4)
        self.assertEqual(tuple(np.array(design.COEFFICIENTS['C90'])-np.array(design.COEFFICIENTS['C7A'])),design.COEFFICIENTS['ATTRIBUTION'])
        receipt,data=receipt_and_data();result,blocks=analysis.analyse(data,receipt)
        self.assertAlmostEqual(result['primary']['mean'],-.2)
        for key,value in (('C90:xgd',.21),('C7A:xgd',.41),('INTERACTION:xgd',.12)):
            self.assertAlmostEqual(result['secondary'][key]['mean'],value)
        self.assertEqual(len(result['secondary']),8);self.assertEqual(len(blocks),576)
        self.assertEqual(result['independent_seed_blocks'],64);self.assertFalse(result['consumer_semantics_validated'])
        other,_=analysis.analyse(reversed(data),receipt);self.assertEqual(result,other)

    def test_incomplete_duplicate_raw_wrong_identity_and_missing_cache_refuse(self):
        receipt,data=receipt_and_data()
        for mutate in ('missing','duplicate','raw','identity','cache','silent_null'):
            bad=deepcopy(data)
            if mutate=='missing':bad.pop()
            elif mutate=='duplicate':bad.append(deepcopy(bad[0]))
            elif mutate=='raw':bad[0]['native_audit']['c7a_raw']=9999
            elif mutate=='identity':bad[0]['identity']={}
            elif mutate=='cache':bad[0]['descriptive']['prepared_sharpness_cache8a_mean']=None
            else:bad[0]['descriptive']['finished_sharpness_cache8a_mean']=None
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):analysis.checked(bad,receipt)
        bad=deepcopy(data);bad[0]['descriptive']['finished_sharpness_cache8a_mean']=None
        bad[0]['descriptive_missing_reasons']={'finished_sharpness_cache8a_mean':'missing actual observation'}
        analysis.checked(bad,receipt)

    def test_frozen_design_budget_family_and_executable_provenance(self):
        c=design.contract_definition();self.assertIsNone(c['identity']);self.assertIsNone(c['execution'])
        with self.assertRaises(ValueError):design.validate_design(c,executable=True)
        receipt,_=receipt_and_data();design.validate_design(receipt['config'],executable=True)
        for section,key,value in (('science','family_size',7),('science','min_effect',.3),('design','n_blocks',33),
                ('budget','global_child_seconds',3601),('budget','total_native_wall_seconds',901),('native_spec','cache_mapping_assumed',True)):
            c=deepcopy(receipt['config']);c[section][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):design.validate_design(c)
        c=deepcopy(receipt['config']);c['execution']['kind']='warm'
        with self.assertRaises(ValueError):design.validate_design(c,executable=True)


if __name__=='__main__':unittest.main()

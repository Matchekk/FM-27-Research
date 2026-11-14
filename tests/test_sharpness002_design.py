"""Own synthetic record/math fixtures only; no native, seed or registry calls."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import sys
import json
import unittest
import numpy as np
from scipy.stats import nct,t

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import sharpness002_design as design
import analyse_sharpness002 as analysis
from research.core import config_hash,schedule
from research.startpolicy import PROFILE_LIMITS,decode_records,encode_records


def binary_fixture(side):
    lineup=[2,0,1,3,4,5,6,7,8,9,10]
    records=[(1,s,a,b,20 if b<15 else 60) for s,n in ((0,23),(1,26)) for a in range(n) for b in range(69)]
    for s,a in ((s,a) for s in (0,1) for a in range(23)):
        for field,(low,_) in enumerate(PROFILE_LIMITS):
            value={15:10000,16:10000,17:10000,18:0,20:80,21:100,22:20}.get(field,low)
            records.append((15,s,a,field,value))
    records.extend((17,s,0,0,23) for s in (0,1))
    records.extend((11,s,i,0,a) for s in (0,1) for i,a in enumerate(lineup))
    records.extend((2,s,10,0,design.PRESS_IDS[0]) for s in (0,1))
    # Typed uint32 filler makes a deliberately synthetic5557record fixture;
    # it is never submitted to any native encoder, normalizer or host.
    records.extend((0,0,i,0,0) for i in range(5557-len(records)))
    source=encode_records(records);affected=set(lineup[1:]);more=[]
    for k,s,a,b,v in records:
        if k==1 and s==side and a in affected and b==52:v=40
        if k==2 and s==side and a==10:v=design.PRESS_IDS[1]
        more.append((k,s,a,b,v))
    return source,encode_records(more),affected


def receipt_and_data():
    identity={k:('a'*64 if k.endswith('sha256') or k=='resource_fingerprint' else 'own-synthetic')
        for k in ('build','engine_sha256','adapter_host_sha256','adapter_version','fixture_sha256','resource_fingerprint','lab_version','lab_commit')}
    setups={h:{str(s):{a:config_hash([h,s,a]) for a in design.ARMS} for s in (0,1)} for h in design.CONTEXTS}
    c=design.contract_definition(identity,setups);c['status']='registered'
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['gates']['tech17'].update(passed=True,independently_released=True,release_commit='d'*40,ci_run=1,summary_sha256='e'*64,review_sha256='f'*64)
    c['execution']=dict(runner='analysis/run_sharpness002.py',kind='cold_direct_cli',workers=4,max_processes_per_job=3,
        code_sha256={'own_synthetic.py':'a'*64},input_manifest_sha256='b'*64,seed_plan_sha256='c'*64)
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(100001,100065)));data=[]
    for job in schedule(receipt):
        tr=design.treatment(job['arm']);h=design.CONTEXTS.index(job['scenario']);side=job['side']
        i=receipt['seeds'][h*32:(h+1)*32].index(job['seed'])
        s,p=tr['levels']['SHARPNESS'],tr['levels']['PRESS']
        y=5+(.10+.01*h+.005*(i-15.5)+.04*(2*side-1))*s+(.20+.01*h+.003*(i-15.5))*p+.03*s*p+.1*side
        stats=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(stats),dict(stats)];teams[side]['xg']+=y;score=[0,0];score[side]=int(s==1)
        descriptive={k:0. for k in design.DESCRIPTIVE}
        for stage in ('prepared','first','finished'):
            descriptive[stage+'_condition_cache89_mean']=100.
            descriptive[stage+'_sharpness_cache8a_mean']=tr['sharpness_raw']/100
        descriptive.update(prepared_tf33_matches_frozen_d00=True,first_tf33_matches_frozen_d00=True,
            finished_tf33_distinct_hashes=1,finished_condition_raw_mean=10000.,finished_sharpness_raw_mean=float(tr['sharpness_raw']),
            finished_sharpness_secondary_raw_mean=float(tr['sharpness_raw']),finished_condition_accumulator_raw_mean=1000000.)
        audit=dict.fromkeys(analysis.AUDIT_BOOLS,True)
        audit.update(attribute_values_verified=3174,profile_fields_verified=1058,phase_cells_verified=44,pi_groups_verified=748,
            sharpness_raw=tr['sharpness_raw'],pressing_bit=tr['pressing_bit'])
        data.append(dict(job_id=job['key'],context=job['scenario'],team_side=side,seed=job['seed'],arm=job['arm'],status='ok',
            config_sha256=receipt['config_sha256'],setup_sha256=job['setup_sha256'],identity=identity,observer_host_sha256=design.OBSERVER_HOST,
            result=dict(score=score,team_statistics=teams,tick=22000,clock=5400),native_audit=audit,
            descriptive=descriptive,descriptive_missing_reasons={},test_origin='own_synthetic_not_fm'))
    return receipt,data


class SharpnessDesignTests(unittest.TestCase):
    def test_published_draft_matches_factory_and_reserves_no_seeds(self):
        draft=json.loads((ROOT/'data/mech-002-sharpness-p0/contract-draft.json').read_text(encoding='utf8'))
        self.assertEqual(draft,design.contract_definition())
        self.assertIsNone(draft['seed_plan']['technical_seeds_reserved']);self.assertIsNone(draft['seed_plan']['main_seeds_reserved'])
        self.assertIsNone(draft['execution']);self.assertFalse(draft['gates']['tech17']['passed'])

    def test_full_factorial_orthogonal_and_physical_contrast_scaling(self):
        matrix=design.matrix();self.assertEqual(len({r['id'] for r in matrix}),4)
        levels=np.array([[1,*r['levels'].values(),np.prod(list(r['levels'].values()))] for r in matrix])
        np.testing.assert_array_equal(levels.T@levels,np.eye(4)*4)
        receipt,data=receipt_and_data();first,blocks=analysis.analyse(data,receipt);second,_=analysis.analyse(reversed(data),receipt)
        self.assertEqual(first,second);self.assertEqual(len(blocks),512)
        self.assertAlmostEqual(first['primary']['mean'],.21)
        self.assertAlmostEqual(first['secondary']['PRESS:xgd']['mean'],.41)
        self.assertAlmostEqual(first['secondary']['SHARPNESSxPRESS:xgd']['mean'],.12)
        self.assertEqual(len(first['secondary']),7);self.assertEqual(first['independent_seed_blocks'],64)
        self.assertFalse(first['ui_scale_calibrated']);self.assertFalse(first['mediation_identified'])

    def test_compiler_restores_only_original_stamina_and_twenty_raw_records(self):
        for side in (0,1):
            base,more,affected=binary_fixture(side);inputs=design.build_inputs(base,more,side)
            self.assertEqual(inputs['S100-P0'],base)
            for arm,payload in inputs.items():
                tr=design.treatment(arm);records=decode_records(payload);original=decode_records(base)
                differences=[(a,b) for a,b in zip(original,records,strict=True) if a!=b]
                self.assertEqual(len(differences),(20 if tr['sharpness_raw']==7000 else 0)+int(tr['pressing_bit']==66))
                self.assertTrue(all(v==60 for k,s,a,b,v in records if k==1 and b==52))
                low={(s,a,b) for k,s,a,b,v in records if k==15 and b in (16,17) and v==7000}
                expected={(side,a,b) for a in affected for b in (16,17)} if tr['sharpness_raw']==7000 else set()
                self.assertEqual(low,expected)

    def test_compiler_rejects_undeclared_tail_gk_baseline_or_execution_changes(self):
        base,more,_=binary_fixture(1)
        for target in ('gk','tail','other','execution','baseline'):
            source=list(decode_records(base));intervention=list(decode_records(more))
            if target in ('gk','tail'):
                slot=2 if target=='gk' else 25
                intervention=[(k,s,a,b,40) if (k,s,a,b)==(1,1,slot,52) else (k,s,a,b,v) for k,s,a,b,v in intervention]
            elif target=='other':intervention[-1]=(0,0,999,0,1)
            elif target=='execution':intervention[-1]=(61,0,0,0,1)
            else:source=[(k,s,a,b,61) if (k,s,a,b)==(1,0,0,52) else (k,s,a,b,v) for k,s,a,b,v in source]
            with self.subTest(target=target),self.assertRaises(ValueError):design.build_inputs(encode_records(source),encode_records(intervention),1)
        with self.assertRaises(ValueError):design.build_inputs(base,more,True)

    def test_technical_plan_has_four_seeds_sixteen_exact_aa_pairs(self):
        jobs=design.technical_jobs([101,102,103,104]);self.assertEqual(len(jobs),33)
        full=[r for r in jobs if r['kind']=='full'];self.assertEqual(len(full),32)
        self.assertEqual(set(Counter((r['context'],r['side'],r['arm']) for r in full).values()),{2})
        self.assertEqual(len({r['seed'] for r in full}),4)
        with self.assertRaises(ValueError):design.technical_jobs([101]*4)

    def test_draft_and_unreleased_tech17_and_warm_execution_never_analyse(self):
        draft=design.contract_definition()
        self.assertFalse(draft['gates']['tech17']['passed']);self.assertIsNone(draft['identity'])
        with self.assertRaises(ValueError):design.validate_design(draft,executable=True)
        receipt,data=receipt_and_data()
        for gate in ('passed','independently_released'):
            bad=deepcopy(receipt);bad['config']['gates']['tech17'][gate]=False
            with self.assertRaises(ValueError):analysis.analyse(data,bad)
        c=deepcopy(receipt['config']);c['execution']['kind']='warm'
        with self.assertRaises(ValueError):design.validate_design(c,executable=True)

    def test_budget_contrasts_family_and_record_interventions_are_frozen(self):
        receipt,_=receipt_and_data()
        for key,value in (('total_native_wall_seconds',901),('absolute_study_wall_seconds',1200),
                          ('minimum_main_admission_seconds',599),('wall_start_policy','inert_prepare')):
            c=deepcopy(receipt['config']);c['budget'][key]=value
            with self.assertRaises(ValueError):design.validate_design(c)
        for key,value in (('family_size',8),('bootstrap_resamples',10000),('context_weights',[.75,.25])):
            c=deepcopy(receipt['config']);c['science'][key]=value
            with self.assertRaises(ValueError):design.validate_design(c)
        c=deepcopy(receipt['config']);c['native_spec']['stamina_raw']=80
        with self.assertRaises(ValueError):design.validate_design(c)

    def test_missing_duplicate_failed_and_wrong_native_rows_block_all_effects(self):
        receipt,data=receipt_and_data()
        for kind in ('missing','duplicate','failed','seed','host','raw','control','pressing','setup'):
            rows=deepcopy(data)
            if kind=='missing':rows.pop()
            elif kind=='duplicate':rows[-1]=deepcopy(rows[0])
            elif kind=='failed':rows[0]['status']='failed'
            elif kind=='seed':rows[0]['seed']+=10000
            elif kind=='host':rows[0]['observer_host_sha256']='0'*64
            elif kind=='raw':rows[0]['native_audit']['sharpness_raw']=7001
            elif kind=='control':rows[0]['native_audit']['controls_verified']=False
            elif kind=='pressing':rows[0]['native_audit']['pressing_bit']=True
            else:rows[0]['setup_sha256']='0'*64
            with self.subTest(kind=kind),self.assertRaises(ValueError):analysis.analyse(rows,receipt)

    def test_only_finished_cache_may_be_missing_with_explicit_reason(self):
        receipt,data=receipt_and_data();field='finished_sharpness_cache8a_mean'
        data[0]['descriptive'][field]=None;data[0]['descriptive_missing_reasons'][field]='actor_cache_unavailable_at_finish'
        effects,_=analysis.analyse(data,receipt)
        desc=effects['descriptive']['by_context_arm'][data[0]['context']][data[0]['arm']][field]
        self.assertEqual(desc['missing'],1);self.assertIsNotNone(desc['mean'])
        data[0]['descriptive_missing_reasons']={}
        with self.assertRaises(ValueError):analysis.analyse(data,receipt)
        receipt,data=receipt_and_data();data[0]['descriptive']['finished_tf33_distinct_hashes']=0
        with self.assertRaises(ValueError):analysis.analyse(data,receipt)

    def test_future_normal_model_power_uses_new_blocks_and_sixteen_n_cost(self):
        planning=analysis.future_planning([.8,1.2])
        for key in ('observed','simultaneous95_sd_upper'):
            sd=np.array(planning[key]['sd'])
            for plan in planning[key]['power90']:
                n=plan['seeds_per_context'];self.assertEqual(plan['matches'],16*n)
                self.assertEqual(plan['independent_blocks'],2*n)
                def power(n_):
                    v=sd**2/(4*n_);variance=v.sum();df=variance**2/(v*v/(n_-1)).sum();cut=t.isf(.025,df)
                    shift=plan['effect']/np.sqrt(variance)
                    return float(nct.cdf(-cut,df,shift)+nct.sf(cut,df,shift))
                self.assertGreaterEqual(power(n),.9)
                if n>2:self.assertLess(power(n-1),.9)


if __name__=='__main__':unittest.main()

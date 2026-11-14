"""Synthetic actor/phase mapping and package-contrast tests; no native process."""
from copy import deepcopy
from collections import Counter
import unittest
import numpy as np

from analysis import stless003_design as design
from analysis import analyse_stless003 as analysis
from research.core import config_hash,schedule
from research.startpolicy import decode_records,encode_records
from tests.test_sharpness002_design import binary_fixture


def own_fixture():
    ip=[('GK','Goalkeeper'),('DR','FullBack'),('DCR','CentreBack'),('DCL','CentreBack'),('DL','FullBack'),
        ('DMR','DefensiveMidfielder'),('DML','DeepLyingPlaymaker'),('AMR','Winger'),('AMC','AttackingMidfielder'),('AML','Winger'),('ST','CentreForward')]
    oop=[('GK','OPGoalkeeper'),('DR','OPFullBack'),('DCR','OPCentreBack'),('DCL','OPCentreBack'),('DL','OPFullBack'),
        ('MCR','OPCentralMidfielder'),('MCL','OPCentralMidfielder'),('MR','OPWideMidfielder'),('AMC','OPAttackingMidfielder'),('ML','OPWideMidfielder'),('ST','OPCentreForward')]
    masks={'GK':1,'DR':4,'DL':8,'DCR':2097168,'DCL':1048592,'DMR':2097280,'DML':1048704,
        'AMR':2048,'AMC':8192,'AML':4096,'ST':16384,'MCR':2098176,'MCL':1049600,'MR':256,'ML':512,'AMCL':1056768,'AMCR':2105344}
    role_names=list(dict.fromkeys(role for _,role in ip+oop))+['SecondStriker']
    flags={r:1<<i for i,r in enumerate(role_names)}
    # Declared synthetic catalog flags; no claim that these are native values.
    roles=[dict(id=r,flags=flags[r],phase=int(r.startswith('OP'))) for r in role_names]
    eligible={p:[[],[]] for p in masks}
    for phase,cells in enumerate((ip,oop)):
        for pos,role in cells:
            if role not in eligible[pos][phase]:eligible[pos][phase].append(role)
    for pos in ('AMCL','AMCR'):
        eligible[pos]=[['AttackingMidfielder','SecondStriker'],['OPAttackingMidfielder']]
    catalog=dict(positions=[dict(id=p,mask=m) for p,m in masks.items()],roles=roles,role_eligibility_context={'0:0':eligible})
    config=dict(rules='game',fixture='bundled_match_pkm',teams=[])
    for side in (0,1):
        phases=[[dict(position=p,role=r,duty='0',instructions={str(i):0 for i in range(17)},target_player=255,target_position=0)
            for p,r in cells] for cells in (ip,oop)]
        config['teams'].append(dict(lineup=list(range(11)),phases=phases,instructions={'10':1313689463},
            players=[dict(attributes=([20]+[0]*14 if slot==0 else [0,0]+[20]*13)+[60]*54) for slot in range(23)]))
    source,_,_=binary_fixture(0);records=list(decode_records(source))
    records=[(k,s,a,b,config['teams'][s]['players'][a]['attributes'][b]) if k==1 else (k,s,a,b,v) for k,s,a,b,v in records]
    mapping=[[0,1,2,3,4,9,5,6,7,8,10],[0,1,2,3,4,5,6,7,9,8,10]]
    extra=[(13,s,0,0,1) for s in (0,1)]
    for s,team in enumerate(config['teams']):
        for phase,cells in enumerate(team['phases']):
            for slot,cell in enumerate(cells):
                native=phase*16+(mapping[s][slot] if phase else slot);f=flags[cell['role']]
                extra.extend(((4,s,native,f>>32,f&0xffffffff),(5,s,native,0,masks[cell['position']])))
    filler=[i for i,r in enumerate(records) if r[0]==0]
    for i,row in zip(filler,extra,strict=False):records[i]=row
    # binary_fixture deliberately has a nonidentity lineup; replace it so config
    # and record bindings in this separate synthetic fixture are exactly equal.
    records=[(k,s,a,b,a) if k==11 else (k,s,a,b,v) for k,s,a,b,v in records]
    return encode_records(records),config,catalog,mapping


def receipt_and_data():
    identity={k:('a'*64 if k.endswith('sha256') or k=='resource_fingerprint' else 'own-synthetic')
        for k in ('build','engine_sha256','adapter_host_sha256','adapter_version','fixture_sha256','resource_fingerprint','lab_version','lab_commit')}
    setups={h:{str(s):{a:config_hash([h,s,a]) for a in design.ARMS} for s in (0,1)} for h in design.CONTEXTS}
    c=design.contract_definition(identity,setups);c['status']='registered'
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['execution']=dict(runner='analysis/run_stless003.py',kind='cold_direct_cli',workers=4,max_processes_per_job=3,
        code_sha256={'own-synthetic':'a'*64},input_manifest_sha256='b'*64,seed_plan_sha256='c'*64)
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(200001,200065)));data=[]
    for job in schedule(receipt):
        tr=design.treatment(job['arm']);h=design.CONTEXTS.index(job['scenario']);side=job['side']
        i=receipt['seeds'][h*32:(h+1)*32].index(job['seed']);a,b=tr['levels'].values()
        y=5+.1*a+.2*b+(.03+.005*h+.001*(i-15.5)+.01*(side-.5))*a*b
        stats=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(stats),dict(stats)];teams[side]['xg']+=y;score=[0,0];score[side]=int(a*b==1)
        desc={k:0. for k in design.DESCRIPTIVE}
        for stage in ('prepared','first','finished'):
            desc[stage+'_condition_cache89_mean']=100.;desc[stage+'_sharpness_cache8a_mean']=100.
        desc.update(prepared_tf33_matches_frozen_d00=True,first_tf33_matches_frozen_d00=True,finished_tf33_distinct_hashes=1,
            finished_condition_raw_mean=10000.,finished_sharpness_raw_mean=10000.,finished_sharpness_secondary_raw_mean=10000.,
            finished_condition_accumulator_raw_mean=1000000.)
        audit=dict.fromkeys(analysis.AUDIT_BOOLS,True)
        audit.update(attribute_values_verified=3174,profile_fields_verified=1058,phase_cells_verified=44,pi_groups_verified=748,
            ip_strikerless=tr['ip_strikerless'],oop_strikerless=tr['oop_strikerless'],pressing_bit=0)
        data.append(dict(job_id=job['key'],experiment_id=design.EXPERIMENT,context=job['scenario'],team_side=side,seed=job['seed'],arm=job['arm'],
            status='ok',config_sha256=receipt['config_sha256'],setup_sha256=job['setup_sha256'],identity=identity,observer_host_sha256=design.OBSERVER_HOST,
            result=dict(score=score,team_statistics=teams,tick=22000,clock=5400),native_audit=audit,descriptive=desc,
            descriptive_missing_reasons={},test_origin='own_synthetic_not_fm'))
    return receipt,data


class Stless003Tests(unittest.TestCase):
    def test_only_six_declared_kind4_kind5_records_change_and_all_profiles_preserved(self):
        raw,base,catalog,mapping=own_fixture();source=decode_records(raw)
        for side in (0,1):
            out=design.build_inputs(raw,side,base,catalog,mapping)
            self.assertEqual(out[design.ARMS[0]],raw)
            self.assertEqual([sum(a!=b for a,b in zip(source,decode_records(out[arm]),strict=True)) for arm in design.ARMS],[0,3,3,6])
            for arm in design.ARMS:
                changed=decode_records(out[arm]);diffs=[(a,b) for a,b in zip(source,changed,strict=True) if a!=b]
                self.assertTrue(all(a[0] in (4,5) and a[0:3]==b[0:3] and a[1]==side for a,b in diffs))
                self.assertEqual([r for r in source if r[0] in (1,11,13,15,17)],[r for r in changed if r[0] in (1,11,13,15,17)])

    def test_oop_records_use_actor_permutation_and_not_same_index_on_both_sides(self):
        raw,base,catalog,mapping=own_fixture();source=decode_records(raw)
        for side,expected in ((0,{23,26}),(1,{25,26})):
            out=design.build_inputs(raw,side,base,catalog,mapping)
            diffs=[b for a,b in zip(source,decode_records(out['I0-O1']),strict=True) if a!=b]
            self.assertEqual({r[2] for r in diffs},expected)

    def test_configs_preserve_every_other_value_and_no_implicit_position_penalty(self):
        _,base,catalog,_=own_fixture()
        for side in (0,1):
            out=design.build_configs(base,side,catalog)
            for arm,config in out.items():
                self.assertEqual(config['teams'][1-side],base['teams'][1-side])
                self.assertEqual(config['teams'][side]['players'],base['teams'][side]['players'])
                self.assertEqual(config['teams'][side]['lineup'],list(range(11)))
                for phase,cells in enumerate(config['teams'][side]['phases']):
                    self.assertEqual(len({x['position'] for x in cells}),11)
                    self.assertTrue(all(cells[i]==base['teams'][side]['phases'][phase][i] for i in range(11) if i not in (8,10)))

    def test_illegal_roles_duplicate_positions_bad_profile_and_experimental_context_reject(self):
        _,base,catalog,_=own_fixture()
        for mutate in ('role','position','profile','execution','lineup','pi'):
            bad=deepcopy(base)
            if mutate=='role':bad['teams'][0]['phases'][0][10]['role']='SecondStriker'
            elif mutate=='position':bad['teams'][0]['phases'][0][10]['position']='AMC'
            elif mutate=='profile':bad['teams'][0]['players'][10]['attributes'][10]=1
            elif mutate=='execution':bad['experimental_execution']={}
            elif mutate=='lineup':bad['teams'][0]['lineup'][8]=10
            else:bad['teams'][0]['phases'][0][8]['instructions']['0']=1
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):design.build_configs(bad,0,catalog)
        bad=deepcopy(catalog);bad['role_eligibility_context']['0:0']['AMCR'][0].remove('SecondStriker')
        with self.assertRaises(ValueError):design.build_configs(base,0,bad)

    def test_missing_native_rules_duplicate_role_wrong_map_and_attribute_mismatch_reject(self):
        raw,base,catalog,mapping=own_fixture()
        for mutate in ('rules','role','map','attribute','execution'):
            rows=list(decode_records(raw));maps=deepcopy(mapping)
            if mutate=='rules':rows=[(k,s,a,b,0) if k==13 and s==0 else (k,s,a,b,v) for k,s,a,b,v in rows]
            elif mutate=='role':
                index=next(i for i,r in enumerate(rows) if r[0:3]==(4,0,8));rows[-1]=rows[index]
            elif mutate=='map':maps[0]=list(range(11))
            elif mutate=='attribute':rows=[(k,s,a,b,59) if (k,s,a,b)==(1,1,20,55) else (k,s,a,b,v) for k,s,a,b,v in rows]
            else:rows[-1]=(61,0,0,0,1)
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):design.build_inputs(encode_records(rows),0,base,catalog,maps)

    def test_technical_sample_and_physical_difference_of_differences(self):
        jobs=design.technical_jobs([11,12,13,14]);self.assertEqual(len(jobs),33)
        self.assertEqual(set(Counter((j['context'],j['side'],j['arm']) for j in jobs[:-1]).values()),{2})
        levels=np.array([[1,*r['levels'].values(),np.prod(list(r['levels'].values()))] for r in design.matrix()])
        np.testing.assert_array_equal(levels.T@levels,np.eye(4)*4)
        receipt,data=receipt_and_data();result,blocks=analysis.analyse(data,receipt)
        self.assertAlmostEqual(result['primary']['mean'],.13)
        self.assertAlmostEqual(result['secondary']['IP:xgd']['mean'],.2)
        self.assertAlmostEqual(result['secondary']['OOP:xgd']['mean'],.4)
        self.assertEqual(len(result['secondary']),7);self.assertEqual(len(blocks),512);self.assertEqual(result['independent_seed_blocks'],64)
        self.assertFalse(result['isolated_role_mechanism_identified'])
        other,_=analysis.analyse(reversed(data),receipt);self.assertEqual(result,other)

    def test_incomplete_duplicate_bad_package_and_uncontrolled_cache_refuse(self):
        receipt,data=receipt_and_data()
        for mutate in ('missing','duplicate','package','rules','cache','identity'):
            bad=deepcopy(data)
            if mutate=='missing':bad.pop()
            elif mutate=='duplicate':bad.append(deepcopy(bad[0]))
            elif mutate=='package':bad[0]['native_audit']['ip_strikerless']=1
            elif mutate=='rules':bad[0]['native_audit']['native_game_rules_verified']=False
            elif mutate=='cache':bad[0]['descriptive']['prepared_sharpness_cache8a_mean']=70.
            else:bad[0]['experiment_id']='TACT-002-R0'
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):analysis.checked(bad,receipt)

    def test_frozen_budget_family_and_source_contract(self):
        c=design.contract_definition()
        with self.assertRaises(ValueError):design.validate_design(c,executable=True)
        receipt,_=receipt_and_data();design.validate_design(receipt['config'],executable=True)
        for section,key,value in (('science','family_size',8),('science','primary_contrast','IP'),('design','n_blocks',16),
                ('budget','total_native_wall_seconds',901),('budget','per_call_absolute_timeout_seconds',31),
                ('budget','per_call_reserved_envelope_seconds',41),('budget','global_native_call_elapsed_limit_seconds',3601),
                ('native_spec','changed_record_kinds',[4,5,1])):
            bad=deepcopy(receipt['config']);bad[section][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):design.validate_design(bad)


if __name__=='__main__':unittest.main()

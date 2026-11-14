"""Synthetic offline ATTR-009 tests; none execute or import a native server."""
from copy import deepcopy
from pathlib import Path
import struct, sys, tempfile, unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from research.attr009 import *
from research.core import schedule
from research.native import read
import analyse_attr009 as analysis
import run_attr009 as runner
import export_attr009 as exporter
from research.native import write


def base():
    ip=['GK','DR','DCR','DCL','DL','DMR','DML','AMR','AMC','AML','ST']
    oop=['GK','DR','DCR','DCL','DL','MCR','MCL','MR','AMC','ML','ST']
    teams=[]
    for side in (0,1):
        players=[dict(native_id=side*100+i+1,attributes=([20]+[0]*14 if i==0 else[0,0]+[20]*13)+[60]*54,native_profile={'unchanged':17})for i in range(23)]
        phases=[[dict(position=p,role='frozen',duty='0',instructions={'1':0})for p in positions]for positions in(ip,oop)]
        teams.append(dict(players=players,roster_size=23,lineup=list(range(11)),phases=phases))
    return dict(rules='game',fixture='bundled_match_pkm',teams=teams)


OOP_MAP=[[0,1,2,3,4,9,5,6,7,8,10],[0,1,2,3,4,5,6,7,9,8,10]]


def fixture():
    c=deepcopy(read(ROOT/'research/specs/TACT-002-R0.json'))
    c.update(experiment_id=EXPERIMENT,module='ATTR',status='registered')
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['metrics']=dict(primary='xgd',secondary=list(SECONDARY))
    c['budget'].update(max_matches=384,max_technical_attempts=33,total_native_wall_seconds=600,absolute_study_wall_seconds=1200)
    c['science'].update(contrast_coefficients=list(COEFFICIENTS),secondary_endpoints=list(SECONDARY),family_size=5,multiple_testing='holm')
    c['design'].update(n_blocks=16,control_arm='OJ',matrix=matrix(),matrix_sha256=config_hash(matrix()),arms=[dict(id=a,setup_sha256='a'*64)for a in ARMS],setups={h:{str(s):{a:config_hash([h,s,a])for a in ARMS}for s in(0,1)}for h in CONTEXTS})
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(10000,10032)))
    data=[]
    for job in schedule(receipt):
        h=CONTEXTS.index(job['scenario']);i=receipt['seeds'][h*16:(h+1)*16].index(job['seed'])
        arm=job['arm'];side=job['side'];y=3+(.4+.02*h+.002*(i-7.5))*(arm=='SJ')+.1*side
        stat=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(stat),dict(stat)];teams[side]['xg']+=y
        data.append(dict(job,**job['identity'],status='ok',engine_readback=True,tested_side=side,score=[1,1],team_statistics=teams,finish_tick=22000,
            input_contract_verified=True,profile_fields_verified=1058,native_roles_verified=44,native_pi_cells_verified=44,native_pi_groups_verified=748,native_raw_dose_verified=True,design_matrix_sha256=config_hash(matrix())))
    return receipt,data


class AttrBridgeTests(unittest.TestCase):
    def test_matrix_and_physical_contrast(self):
        self.assertEqual(len(matrix()),6);self.assertAlmostEqual(sum(COEFFICIENTS),0)
        r,data=fixture();result,blocks=analysis.analyse(data,r)
        self.assertAlmostEqual(result['primary']['mean'],.41)
        self.assertEqual(len(blocks),32*6);self.assertEqual(len(result['secondary']),5)
        self.assertEqual(result['independent_seed_blocks'],32)
        self.assertFalse(result['global_ranking_claimed']);self.assertFalse(result['mechanism_decomposition_identified'])
    def test_incomplete_duplicate_failed_and_seed_drift_refused(self):
        r,data=fixture()
        for bad in(data[:-1],data+[data[0]]):
            with self.assertRaises(ValueError):analysis.checked(bad,r)
        for key,value in [('status','failed'),('engine_readback',False),('seed',2),('native_raw_dose_verified',False),('engine_sha256','b'*64),('profile_fields_verified',1057)]:
            bad=deepcopy(data);bad[0][key]=value
            with self.assertRaises(ValueError):analysis.checked(bad,r)
    def test_mask_union_shared_families_and_oop_native_mapping(self):
        original=base();changed,bound,changes=apply_arm(original,0,'SJ',OOP_MAP)
        self.assertEqual(bound[5]['active_rating_families'],[5,7])
        self.assertEqual(bound[2]['active_rating_families'],[3])
        self.assertEqual(bound[5]['oop_native_slot'],9)
        for cell in bound[1:]:
            values=changed['teams'][0]['players'][cell['roster_slot']]['attributes']
            self.assertEqual(values[:2],[0,0]);self.assertEqual(values[54],80)
            self.assertEqual([i for i in range(2,15)if values[i]==20],cell['active_rating_families'])
        self.assertEqual(original,base());self.assertTrue(changes)
    def test_lineup_permutation_uses_roster_not_native_oop_slot(self):
        original=base();original['teams'][1]['lineup'][5:7]=[6,5]
        changed,bound,_=apply_arm(original,1,'SA',OOP_MAP)
        self.assertEqual(bound[5]['roster_slot'],6);self.assertEqual(bound[8]['oop_native_slot'],9)
        self.assertEqual(changed['teams'][1]['players'][6]['attributes'][7],20)
    def test_away_carrier_unused_tail_is_preserved(self):
        original=base();original['teams'][1]['players']+=deepcopy(original['teams'][1]['players'][11:14])
        changed,_,_=apply_arm(original,1,'SP',OOP_MAP)
        self.assertEqual(len(changed['teams'][1]['players']),26)
        self.assertEqual(changed['teams'][1]['players'][23:],original['teams'][1]['players'][23:])
    def test_only_start_field_attributes_change(self):
        for side in(0,1):
            for arm in ARMS:
                original=base();changed,_,changes=apply_arm(original,side,arm,OOP_MAP)
                reset=deepcopy(changed)
                for c in changes:reset['teams'][c['side']]['players'][c['roster_slot']]['attributes'][c['attribute']]=c['before']
                self.assertEqual(reset,original)
                self.assertEqual(changed['teams'][side]['players'][0],original['teams'][side]['players'][0])
                self.assertEqual(changed['teams'][side]['players'][11:],original['teams'][side]['players'][11:])
                self.assertEqual(changed['teams'][1-side],original['teams'][1-side])
    def test_forbidden_pool_execution_unknown_position_and_bad_raw(self):
        for key in('experimental_execution','away_tactic_pool'):
            b=base();b[key]={}
            with self.assertRaises(ValueError):apply_arm(b,0,'OJ',OOP_MAP)
        b=base();b['teams'][0]['phases'][1][5]['position']='unknown'
        with self.assertRaises(ValueError):apply_arm(b,0,'SJ',OOP_MAP)
        b=base();b['teams'][0]['players'][1]['attributes'][54]=12
        with self.assertRaises(ValueError):apply_arm(b,0,'OJ',OOP_MAP)
        b=base();b['teams'][0]['players'][1]['attributes'][48]=True
        with self.assertRaises(ValueError):apply_arm(b,0,'OJ',OOP_MAP)
    def test_binary_restricts_exact_changes(self):
        change=dict(side=0,roster_slot=5,attribute=54,before=60,after=80)
        header=struct.pack('<3I',1,1,2)
        a=header+struct.pack('<10I',1,0,5,54,60,15,0,5,16,10000)
        b=header+struct.pack('<10I',1,0,5,54,80,15,0,5,16,10000)
        self.assertEqual(audit_binary(a,b,[change])['changed_records'],1)
        with self.assertRaises(ValueError):audit_binary(a,b[:-4]+struct.pack('<I',7000),[change])
    def test_raw_comparator_preserves_display_limit(self):
        def dump(c):return dict(teams=[dict(side=s,count=23,players=[dict(id=p['native_id'],attributes=p['attributes'])for p in t['players']])for s,t in enumerate(c['teams'])])
        before,_,_=apply_arm(base(),0,'OA',OOP_MAP);after,bound,_=apply_arm(base(),0,'OJ',OOP_MAP)
        evidence=raw_readback(dump(before),dump(after),after,0,'OJ',bound)
        self.assertFalse(evidence['native_fm_display_calibrated']);self.assertEqual(len(evidence['raw_dose']),10)
        bad=dump(after);bad['teams'][0]['players'][1]['attributes']=list(bad['teams'][0]['players'][1]['attributes']);bad['teams'][0]['players'][1]['attributes'][54]=60
        with self.assertRaises(ValueError):raw_readback(dump(before),bad,after,0,'OJ',bound)
    def test_exact_technical_match_budget_and_repeat_coverage(self):
        with patch.object(runner,'read',return_value=dict(technical_seeds=[123,456])):
            jobs=runner.technical_jobs()
        self.assertEqual(len(jobs),32);self.assertEqual(len({j['key']for j in jobs}),32)
        self.assertEqual(sum(j['key'].endswith('r1')for j in jobs),8)
        self.assertEqual({j['arm']for j in jobs if j['key'].endswith('r1')},{'OJ','SJ'})
    def test_capability_never_grants_from_ui_arithmetic(self):
        report=capability_report()
        self.assertFalse(report['native_validation_granted'])
        self.assertFalse(report['raw_intervention']['fm_in_game_display_calibrated'])
        self.assertFalse(report['passive_effectiveness']['mechanism_decomposition_identified'])
    def test_frozen_budget_and_contrast_tampering_refused(self):
        r,_=fixture()
        for key,value in [('max_matches',512),('max_technical_attempts',34),('total_native_wall_seconds',601)]:
            c=deepcopy(r['config']);c['budget'][key]=value
            with self.assertRaises(ValueError):analysis.validate_design(c)
        c=deepcopy(r['config']);c['science']['contrast_coefficients']=[1]*6
        with self.assertRaises(ValueError):analysis.validate_design(c)
    def test_prepare_failure_exports_technical_status_without_receipt(self):
        with tempfile.TemporaryDirectory()as temp:
            local=Path(temp)/'private';public=Path(temp)/'public';local.mkdir()
            budget=dict(experiment=EXPERIMENT,limits={'technical':33,'main':384},limit_seconds=600,
                charged_seconds=1.,reserved=[],halted=True,active=None,operations=[],
                wall_start_utc='2026-11-14T10:00:00+00:00',wall_deadline_utc='2026-11-14T10:20:00+00:00',wall_limit_seconds=1200)
            write(local/'budget.json',budget)
            with patch.object(exporter,'LOCAL',local),patch.object(exporter,'PUBLIC',public):exporter.export()
            self.assertFalse(read(public/'run-summary.json')['scientific_series_complete'])
            self.assertEqual(read(public/'run-summary.json')['counts']['main']['not_started'],384)
            self.assertFalse((public/'effects.json').exists())
    def test_phase_reentry_cannot_start_child_or_replace_provenance(self):
        class Budget:
            def load(self):return dict(active=None,halted=False,operations=[dict(name='technical')])
            def run(self,*args):raise AssertionError('Child must not start')
        with tempfile.TemporaryDirectory()as temp,patch.object(runner,'LOCAL',Path(temp)):
            with self.assertRaises(ValueError):runner.run_supervised_phase(Budget(),'technical',[],[])


if __name__=='__main__':unittest.main()

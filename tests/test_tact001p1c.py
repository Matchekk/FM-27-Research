"""Offline P1C pairing, native contract, frozen candidate and power boundary tests."""
from copy import deepcopy
from pathlib import Path
import sys,unittest
from unittest.mock import patch
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from research.native import read,rows
from research.core import config_hash,schedule
import analyse_tact001p1c as p
import run_tact001p1c as runner

def synthetic():
    c=deepcopy(read(ROOT/'research/specs/TACT-001-P1B.json'));c.update(experiment_id='TACT-001-P1C',status='registered')
    c['preregistration'].update(commit='a'*40,analysis_sha256='b'*64,document_sha256='c'*64)
    c['metrics']['primary']='points';c['budget']['max_matches']=512
    c['design'].update(n_blocks=64,control_arm='D00',matrix=p.matrix(),matrix_sha256=config_hash(p.matrix()),arms=[a for a in c['design']['arms'] if a['id'] in p.ARMS])
    c['design']['setups']={h:{s:{a:v for a,v in by.items() if a in p.ARMS} for s,by in sides.items()} for h,sides in c['design']['setups'].items()}
    r=dict(config=c,config_sha256=config_hash(c),seeds=list(range(1000,1128)));data=[]
    for j in schedule(r):
        h=p.CONTEXTS.index(j['scenario']);i=r['seeds'][h*64:(h+1)*64].index(j['seed']);a=p.ARMS.index(j['arm']);s=j['side']
        gf=1 if not a else [2,1,0][i%3];ga=1;score=[ga,ga];score[s]=gf
        stat=dict(xg=1.,shots=8,shots_on_target=3,passes=80,completed_passes=60,possession=.5)
        teams=[dict(stat),dict(stat)];teams[s]['xg']+=a*(.2+i*.001)
        levels=p.matrix()[a]['levels']
        data.append(dict(j,**j['identity'],status='ok',engine_readback=True,tested_side=s,score=score,team_statistics=teams,finish_tick=22000,
            input_contract_verified=True,profile_fields_verified=1058,factor_levels=levels,design_matrix_sha256=config_hash(p.matrix()),native_factor_bits={f['code']:f['high_bit'] if levels[f['code']]==1 else 0 for f in p.FACTORS}))
    return r,data

class P1CTests(unittest.TestCase):
    def test_two_arm_physical_points_and_block_inference(self):
        r,data=synthetic();z,b=p.analyse(data,r)
        expected=np.array([2,0,-1]*21+[2]);self.assertAlmostEqual(z['primary']['mean'],expected.mean())
        self.assertAlmostEqual(z['primary']['context']['high_press']['sd'],expected.std(ddof=1))
        self.assertEqual(len(b),128);self.assertFalse(z['general_career_transfer_confirmed']);self.assertFalse(z['candidate_changed'])
        self.assertAlmostEqual(z['secondary']['xgd']['mean'],.2+31.5*.001)
    def test_missing_duplicate_seed_input_or_identity_stops(self):
        r,data=synthetic()
        for bad in (data[:-1],data+[data[0]]):
            with self.assertRaises(ValueError):p.checked(bad,r)
        for field,value in [('seed',1),('native_factor_bits',{}),('engine_sha256','a'*64),('setup_sha256','a'*64),('factor_levels',{})]:
            bad=deepcopy(data);bad[0][field]=value
            with self.assertRaises(ValueError):p.checked(bad,r)
    def test_d09_and_wrong_primary_refused(self):
        r,_=synthetic()
        for field,value in [('experiment_id','TACT-001-P1B')]:
            bad=deepcopy(r['config']);bad[field]=value
            with self.assertRaises(ValueError):p.validate_design(bad)
        self.assertEqual([x['id'] for x in p.matrix()],['D00','D15'])
    def test_power_and_precision_minimality(self):
        for e in (.1,.15,.2):
            n=p.minimum([1.3,1.5],effect=e);self.assertGreaterEqual(p.properties([1.3,1.5],n,e)['power'],.9);self.assertLess(p.properties([1.3,1.5],n-1,e)['power'],.9)
        n=p.minimum([1.3,1.5],width=.3);self.assertLessEqual(p.properties([1.3,1.5],n)['full_ci_width'],.3)
    def test_prepared_inputs_seeds_and_technical_schedule_when_available(self):
        if not (runner.PUBLIC/'seed-plan.json').exists():return
        seed=read(runner.PUBLIC/'seed-plan.json');self.assertEqual(len(set(seed['seeds'])),131)
        self.assertFalse(set(seed['seeds'])&set(read(runner.PUBLIC/'excluded-seeds.json')))
        with patch.object(runner,"LOCAL",runner.PUBLIC):jobs=runner.technical_jobs()
        self.assertEqual(len(jobs),16)
        self.assertEqual(len({(j['scenario'],j['side'],j['arm']) for j in jobs}),8)
        inputs=read(runner.PUBLIC/'inputs.json');old=read(ROOT/'data/tact-001-p1b/inputs.json')
        for h in p.CONTEXTS:
            for s in ('0','1'):
                for a in p.ARMS:self.assertEqual(inputs['setups'][h][s][a],old['setups'][h][s][a])
    def test_complete_public_pilot_when_available(self):
        if not (runner.PUBLIC/'effects.json').exists():return
        p.checked(rows(runner.PUBLIC/'main.jsonl'),read(runner.PUBLIC/'manifest.json'))
        self.assertEqual(read(runner.PUBLIC/'run-summary.json')['counts'],dict(main=dict(ok=512),technical=dict(ok=16,expected_rejection=1)))
if __name__=='__main__':unittest.main()

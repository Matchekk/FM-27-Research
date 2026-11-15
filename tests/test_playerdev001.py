import json
from pathlib import Path
import unittest
from copy import deepcopy
import numpy as np
from analysis.playerdev001 import jobs, CAPS
from analysis.playerdev001_design import compile_arm, level
from analysis.analyse_playerdev001 import WEIGHTS, planning
from research.startpolicy import encode_records, decode_records

ROOT=Path(__file__).resolve().parents[1]

class PlayerDev001Test(unittest.TestCase):
    def fixture(self):
        # Synthetic grammar fixture; never a real profile or validation sample.
        pi={'0':0}
        cells=[dict(position='GK' if i==0 else f'P{i}',role='G' if i==0 else 'R',duty=0,instructions=pi) for i in range(11)]
        cells[10]=dict(position='ST',role='CentreForward',duty=0,instructions=pi)
        oop=deepcopy(cells);oop[10]['role']='OPCentreForward'
        base=dict(rules='game',fixture='bundled_match_pkm',teams=[dict(lineup=list(range(11)),phases=deepcopy([cells,oop]),players=[dict(attributes=[60]*69) for _ in range(11)]) for _ in range(2)])
        names=['GK',*(f'P{i}' for i in range(1,10)),'ST']
        catalog=dict(positions=[dict(id=n,mask=1 if n=='GK' else 32) for n in names],roles=[dict(id=r,flags=f,phase=p) for r,f,p in [('G',1,0),('R',2,0),('CentreForward',2048,0),('DeepLyingForward',1024,0),('OPCentreForward',8,1)]],role_eligibility_context={'0:0':{n:[['G','R','CentreForward','DeepLyingForward'],['G','R','OPCentreForward']] for n in names}})
        # OOP test role catalog must match its phase too.
        for team in base['teams']:
            for c in team['phases'][1][:-1]:c['role']='OPCentreForward'
        raw=encode_records([(1,s,10,54,60) for s in (0,1)]+[(4,s,10,0,2048) for s in (0,1)]+[(99,0,0,0,42)])
        return raw,base,catalog

    def test_exact_intervention_and_identity(self):
        raw,base,catalog=self.fixture();before=deepcopy(base)
        for s in (0,1):
            for i,a in enumerate(('A','B','C','D')):
                blob,config,proof=compile_arm(raw,base,s,a,catalog)
                changes=[(x,y) for x,y in zip(decode_records(raw),decode_records(blob)) if x!=y]
                self.assertEqual(len(changes),(0,1,1,2)[i])
                self.assertEqual(config['teams'][s]['players'][10]['attributes'][54],level(a))
                self.assertEqual(config['teams'][1-s],base['teams'][1-s])
                self.assertEqual(proof['undeclared_changes'],0)
        self.assertEqual(base,before)

    def test_corrupt_baseline_fails(self):
        raw,base,catalog=self.fixture()
        for records in ([(1,0,10,54,61),(4,0,10,0,2048)],[(1,0,10,54,60),(4,0,10,0,1024)],[(4,0,10,0,2048)]):
            with self.assertRaises(ValueError):compile_arm(encode_records(records),base,0,'D',catalog)
        base['teams'][0]['lineup'][10]=9
        with self.assertRaises(ValueError):compile_arm(raw,base,0,'D',catalog)

    def test_full_paired_blocks_and_technical_separation(self):
        plan=jobs('main',list(range(1,513)))
        self.assertEqual(len(plan),CAPS['main'])
        groups={}
        for j in plan:groups.setdefault((j['scenario'],j['seed']),set()).add((j['side'],j['arm']))
        self.assertEqual(len(groups),512)
        self.assertTrue(all(len(c)==8 for c in groups.values()))
        tech=jobs('technical',[513,514,515,516])
        self.assertEqual(len(tech),33)
        self.assertTrue(all(j['seed'] not in range(1,513) for j in tech if j['kind']=='full'))

    def test_interaction_sign_and_main_effect_cancellation(self):
        w=WEIGHTS['INTERACTION']
        for c in ((0,0,3,3),(0,3,0,3)):self.assertEqual(float(np.dot(w,c)),0)
        self.assertEqual(float(np.dot(w,(0,1,2,5))),2)
        self.assertEqual(planning()['matches'],4096)
        self.assertLess(planning()['sensitivity']['1.0']['power_for_point15'],1)

    def test_public_archive_if_present(self):
        from research.native import rows,read
        from analysis.analyse_playerdev001 import analyse,independent_check,PUB
        if not (PUB/'main.jsonl').exists():self.skipTest('Scientific run not yet executed')
        data=rows(PUB/'main.jsonl');result,_=analyse(data)
        self.assertTrue(independent_check(data,result)['passed'])
        if (PUB/'effects.json').exists():self.assertEqual(result,read(PUB/'effects.json'))
        broken=deepcopy(data);broken[0]['seed']+=1
        with self.assertRaises(ValueError):analyse(broken)
        with self.assertRaises(ValueError):analyse(data[:-1])

if __name__=='__main__':unittest.main()

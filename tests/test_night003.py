import unittest
from analysis.night003 import jobs, ARMS, CAPS, level
from analysis.analyse_night003 import WEIGHTS, planning

class Night003Test(unittest.TestCase):
    def test_full_factorial_independent_blocks(self):
        plan=jobs('main',list(range(1,513)))
        self.assertEqual(len(plan),CAPS['main'])
        self.assertEqual(len({j['key'] for j in plan}),4096)
        self.assertEqual(len({(j['scenario'],j['seed']) for j in plan}),512)
        self.assertEqual(set(j['arm'] for j in plan),set(ARMS))
        for seed in range(1,513):
            self.assertEqual({(j['side'],j['arm']) for j in plan if j['seed']==seed},set((s,a) for s in (0,1) for a in ARMS))

    def test_contrast_sign_and_no_main_effect_leak(self):
        w=WEIGHTS['INTERACTION']
        # Pure structure and sharpness main effects both cancel.
        for cells in ((0,0,3,3),(3,0,3,0)):
            self.assertEqual(sum(a*b for a,b in zip(w,cells)),0)
        self.assertEqual(sum(a*b for a,b in zip(w,(2,1,5,2))),2)
        self.assertEqual([level(a) for a in ARMS],[10000,7000,10000,7000])

    def test_technical_coverage(self):
        plan=jobs('technical',[513,514,515,516])
        self.assertEqual(len(plan),33)
        self.assertEqual(sum(j['kind']=='negative' for j in plan),1)
        self.assertTrue(all(j['seed'] not in range(1,513) for j in plan if j['kind']=='full'))

    def test_power_is_prospective(self):
        p=planning()
        self.assertEqual(p['matches'],4096)
        self.assertGreater(p['anchors']['TACT003_interaction_observed']['power_for_point20'],.9)

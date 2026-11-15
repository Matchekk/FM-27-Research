import unittest
from analysis.night003_amc import jobs,group_jobs
from analysis.analyse_night003_amc import planning
class IsolatedAmcTest(unittest.TestCase):
    def test_new_position_component_design(self):
        p=jobs('main',list(range(1,513)))
        self.assertEqual(len(p),2048)
        self.assertEqual(len({j['key'] for j in p}),2048)
        self.assertEqual(len(group_jobs(p)),512)
        self.assertEqual({j['arm'] for j in p},{'BASE','AMC_LEFT'})
        for b in group_jobs(p):self.assertEqual({(j['side'],j['arm']) for j in b},{(s,a) for s in (0,1) for a in ('BASE','AMC_LEFT')})
    def test_technical_seeds_are_separate(self):
        p=jobs('technical',[513,514,515,516]);self.assertEqual(len(p),17)
        self.assertEqual([len(b) for b in group_jobs(p,technical=True)],[4,4,4,4,1])
        self.assertTrue(all(j['seed']>512 for j in p if j['seed'] is not None))
    def test_prospective_power_not_match_independence(self):
        p=planning();self.assertEqual((p['matches'],p['blocks']),(2048,512))
        self.assertGreater(p['anchors']['joint95_SD_upper']['power']['0.2'],.99)

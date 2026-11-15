import unittest,json
from pathlib import Path
from analysis.analyse_night003_amc import analyse,independent
P=Path(__file__).resolve().parents[1]/'data/night-003-amcshift'
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def rows(n):return [json.loads(x) for x in (P/n).read_text(encoding='utf8').splitlines()]
class AmcArchiveTest(unittest.TestCase):
    @unittest.skipUnless((P/'technical.jsonl').exists(),'AMC technical data not published')
    def test_native_single_position_coverage(self):
        data=rows('technical.jsonl');s=read('technical-summary.json')
        self.assertEqual(len(data),17);self.assertEqual(len({r['job_id'] for r in data}),17)
        self.assertTrue(s['passed'] and s['all_cleanup_confirmed'])
        self.assertEqual(len(s['aa_pairs']),8)
        self.assertTrue(all(r['exact_outcomes_and_identified_fields_equal'] for r in s['aa_pairs']))
        self.assertEqual(sum(r['status']=='ok' for r in data),16)
        self.assertEqual(sum(r['status']=='expected_rejection' for r in data),1)
        for r in data:
            if r['status']=='ok':
                self.assertTrue(r['native_audit']['position_only_verified'])
                self.assertEqual(r['native_audit']['amc_left'],r['arm']=='AMC_LEFT')
    @unittest.skipUnless((P/'effects.json').exists(),'AMC main results not published')
    def test_complete_main_reconstructed(self):
        d=rows('main.jsonl');e,v=analyse(d)
        self.assertEqual(e,read('effects.json'));self.assertEqual(v.shape,(2,256,6))
        self.assertEqual(independent(d,e),read('independent-recalculation.json'))

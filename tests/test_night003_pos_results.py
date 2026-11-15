import unittest,json
from pathlib import Path
from analysis.analyse_night003_pos import analyse,independent
P=Path(__file__).resolve().parents[1]/'data/night-003-sharppos'
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
def rows(n):return [json.loads(x) for x in (P/n).read_text(encoding='utf8').splitlines()]
class PositionalArchiveTest(unittest.TestCase):
    @unittest.skipUnless((P/'technical.jsonl').exists(),'Technical data not published')
    def test_native_two_actor_coverage(self):
        data=rows('technical.jsonl');summary=read('technical-summary.json')
        self.assertEqual(len(data),17);self.assertEqual(len({r['job_id'] for r in data}),17)
        self.assertTrue(summary['passed'] and summary['all_cleanup_confirmed'])
        self.assertEqual(len(summary['aa_pairs']),8)
        self.assertTrue(all(r['exact_outcomes_and_identified_fields_equal'] for r in summary['aa_pairs']))
        self.assertEqual(sum(r['status']=='ok' for r in data),16)
        self.assertEqual(sum(r['status']=='expected_rejection' for r in data),1)
        for r in data:
            if r['status']=='ok':
                self.assertEqual(r['native_audit']['target_start_slots'],[8,10] if r['arm']=='ATTACK_LOW' else [2,3])
                self.assertTrue(r['native_audit']['start_state_verified'])
    @unittest.skipUnless((P/'effects.json').exists(),'Main results not published')
    def test_complete_main_recomputed_twice(self):
        data=rows('main.jsonl');actual,v=analyse(data)
        self.assertEqual(actual,read('effects.json'))
        self.assertEqual(v.shape,(2,512,6))
        self.assertEqual(independent(data,actual),read('independent-recalculation.json'))

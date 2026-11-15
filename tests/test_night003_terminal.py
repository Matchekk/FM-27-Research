import unittest,json
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'data/night-003-amcshift'
def read(n):return json.loads((P/n).read_text(encoding='utf8'))
class TerminalAmcArchiveTest(unittest.TestCase):
    @unittest.skipUnless((P/'termination.json').exists(),'Study not terminal yet')
    def test_no_scientific_values_or_seed_reuse_from_unbegun_series(self):
        t=read('termination.json');plan=read('main-plan.json')
        unbegun=[json.loads(s) for s in (P/'unbegun-main-jobs.jsonl').read_text(encoding='utf8').splitlines()]
        self.assertTrue(t['terminal_closed'] and t['reservations_retained_unchanged'])
        self.assertFalse(t['scientific_series_started'] or t['scientific_statistics_available'])
        self.assertEqual(t['main_calls_attempted'],0)
        self.assertEqual(t['completed_main_matches'],0)
        self.assertEqual(len(plan),2048);self.assertEqual(len(unbegun),2048)
        self.assertEqual({r['job_id'] for r in unbegun},{j['key'] for j in plan})
        self.assertTrue(all(r['status']=='not_started_time_gate' and r['native_invocation_started'] is False and 'result' not in r for r in unbegun))
        self.assertFalse((P/'main.jsonl').exists() or (P/'effects.json').exists())

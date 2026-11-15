"""Portable archived evidence checks; never invoke a native process."""
import unittest
from pathlib import Path
import json
from hashlib import sha256
from analysis.analyse_night003 import analyse, independent_check

P=Path(__file__).resolve().parents[1]/'data/night-003-sharpstruct'
def read(name):return json.loads((P/name).read_text(encoding='utf-8-sig'))
def rows(name):return [json.loads(line) for line in (P/name).read_text().splitlines()]

class Night003ArchiveTest(unittest.TestCase):
    @unittest.skipUnless((P/'technical.jsonl').exists(),'Technical phase not published yet')
    def test_technical_complete_native_gate(self):
        data=rows('technical.jsonl');summary=read('technical-summary.json');release=read('technical-release.json')
        self.assertEqual(len(data),33)
        self.assertEqual(len({r['job_id'] for r in data}),33)
        self.assertEqual(sum(r['status']=='ok' for r in data),32)
        self.assertEqual(sum(r['status']=='expected_rejection' for r in data),1)
        self.assertTrue(summary['passed'] and release['passed'] and summary['all_cleanup_confirmed'])
        self.assertEqual(summary['peak_inflight_claims'],4)
        self.assertEqual(len(summary['aa_pairs']),16)
        self.assertTrue(all(r['exact_outcomes_and_identified_fields_equal'] for r in summary['aa_pairs']))
        for r in data:
            if r['status']=='ok':
                self.assertEqual(r['native_audit']['profile_fields_verified'],1058)
                self.assertEqual(r['native_audit']['phase_cells_verified'],44)
                self.assertTrue(r['native_audit']['start_state_verified'])
        raw=(P/'technical-summary.json').read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(sha256(raw).hexdigest(),release['summary_sha256'])

    @unittest.skipUnless((P/'effects.json').exists(),'Main results not published yet')
    def test_reconstruct_full_main_in_two_implementations(self):
        data=rows('main.jsonl');expected=read('effects.json');actual,contrasts=analyse(data)
        self.assertEqual(actual,expected)
        self.assertEqual(len(contrasts),512)
        self.assertEqual(independent_check(data,actual),read('independent-recalculation.json'))

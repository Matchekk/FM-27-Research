"""Portable public technical/provenance checks, no private resources or host."""
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
import unittest
from research.native import read,rows
from research.core import historical_seeds

ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'data/player-development-001-role'

class PlayerDevArchiveTests(unittest.TestCase):
    def test_frozen_implementation_and_seeds(self):
        frozen=read(PUB/'inputs.json');plan=read(PUB/'seed-plan.json')
        for name,digest in frozen['code_sha256'].items():
            self.assertEqual(sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),digest,name)
        self.assertEqual(len(plan['seeds']),516);self.assertEqual(len(set(plan['seeds'])),516)
        prior=set()
        for directory in (ROOT/'data').iterdir():
            if directory.is_dir() and directory!=PUB:prior.update(historical_seeds(directory))
        self.assertFalse(set(plan['seeds'])&prior)

    def test_complete_technical_readbacks_and_repeats(self):
        if not (PUB/'technical.jsonl').exists():self.skipTest('Technical run not yet exported')
        frozen=read(PUB/'inputs.json');data=rows(PUB/'technical.jsonl');plan=read(PUB/'technical-plan.json')
        expected={j['key']:j for j in plan};self.assertEqual(len(data),33)
        self.assertEqual({r['job_id'] for r in data},set(expected))
        pairs=defaultdict(list)
        for row in data:
            j=expected[row['job_id']]
            if j['kind']=='negative':
                self.assertEqual((row['status'],row['returncode']),('expected_rejection',108));continue
            self.assertEqual(row['status'],'ok');self.assertEqual(row['identity'],frozen['identity'])
            self.assertEqual(row['setup_sha256'],frozen['setups'][f"{j['scenario']}-{j['side']}"][j['arm']])
            self.assertEqual([row[k] for k in ('seed','context','team_side','arm')],[j['seed'],j['scenario'],j['side'],j['arm']])
            self.assertTrue(all(row['native_audit'][k] is True for k in ('input_verified','start_state_verified','controls_verified','game_rules_verified')))
            self.assertEqual([row['native_audit'][k] for k in ('attribute_values_verified','profile_fields_verified','phase_cells_verified','pi_groups_verified')],[3174,1058,44,748])
            pairs[(j['scenario'],j['side'],j['arm'])].append(row)
        self.assertEqual(len(pairs),16)
        for pair in pairs.values():
            self.assertEqual(len(pair),2)
            for field in ('result','descriptive','descriptive_missing_reasons','native_audit','setup_sha256','seed'):
                self.assertEqual(pair[0][field],pair[1][field])
        summary=read(PUB/'technical-summary.json')
        self.assertTrue(summary['passed'] and summary['all_cleanup_confirmed'])
        self.assertEqual(summary['ledger_sha256'],sha256((PUB/'technical.jsonl').read_bytes()).hexdigest())

if __name__=='__main__':unittest.main()

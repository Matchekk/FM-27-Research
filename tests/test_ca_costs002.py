"""Validate scientific archive contracts, single-field controls and missingness."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from analysis.ca_costs002 import ROOT, digest, matrix, source_keys, summarize
from analysis.playerdev002_implications import analyse


class CaCosts002Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = ROOT/'data/player-development-002-ca'
        cls.rows = [json.loads(line) for line in (cls.folder/'model-interventions.jsonl').read_text().splitlines()]
        cls.manifest = json.loads((cls.folder/'manifest.json').read_text())

    def test_archive_requests_are_single_attribute_interventions(self):
        requests, metadata = matrix(self.manifest['attribute_keys'])
        for index, (stored, spec) in enumerate(zip(self.rows, metadata, strict=True)):
            self.assertEqual(stored['before_sha256'], digest(requests[2*index]))
            self.assertEqual(stored['after_sha256'], digest(requests[2*index+1]))
            for field in spec:
                self.assertEqual(stored[field], spec[field])

    def test_duplicate_aliases_are_not_independent_observations(self):
        seen, aliases = set(), 0
        for row in self.rows:
            alias = row['after_sha256'] in seen
            self.assertEqual(alias, row['repeated_request_alias'])
            aliases += alias
            seen.add(row['after_sha256'])
        self.assertEqual((len(seen), aliases), (1539, 81))

    def test_archive_integrity_and_independent_review(self):
        self.assertEqual(hashlib.sha256((self.folder/'model-interventions.jsonl').read_bytes()).hexdigest(),
                         self.manifest['model_matrix_sha256'])
        expected = json.loads((self.folder/'summary.json').read_text())
        self.assertEqual(summarize(self.rows), expected)
        review = json.loads((self.folder/'independent-review.json').read_text())
        for key, value in review['checks'].items():
            self.assertEqual(value, expected[key])
        for row in self.rows:
            self.assertEqual(row['delta_model_rca'], row['after']['estimated_ca']-row['before']['estimated_ca'])

    def test_missing_foot_inputs_never_become_zero_errors(self):
        report = json.loads((self.folder/'export-diagnostic.json').read_text())
        self.assertEqual(report['rows'], 109)
        self.assertEqual(len(report['failures']), 109)
        self.assertEqual(report['eligible_rows'], 0)
        self.assertIsNone(report['mae'])
        self.assertEqual(report['source_evaluations'], 0)
        self.assertFalse(report['actual_ca_costs_identified'])

    def test_different_calculator_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'source.ts'
            path.write_text('throw new Error("untrusted")')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                source_keys(path)

    def test_incomplete_matrix_rejected(self):
        with self.assertRaises(ValueError):
            summarize(self.rows[:-1])

    def test_frozen_index_is_arithmetic_only(self):
        report = analyse()
        self.assertFalse(report['weights_changed'])
        self.assertIsNone(report['actual_ca_efficiency'])
        self.assertAlmostEqual(report['index_gain_differences']['prespecified_46_minus_38']['ST'], 1.05/19)


if __name__ == '__main__':
    unittest.main()

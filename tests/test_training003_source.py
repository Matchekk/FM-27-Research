import json
import tempfile
import unittest
from pathlib import Path

from analysis.audit_training003_source import extract


class TrainingSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((Path(__file__).resolve().parents[1] /
                                 'data/player-development-002-training/source-table-audit.json').read_text(encoding='utf8'))

    def test_different_source_is_rejected_before_zip_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'changed.xlsx'
            path.write_bytes(b'changed source')
            with self.assertRaisesRegex(ValueError, 'SHA256 mismatch'):
                extract(path)

    def test_all_archived_contrasts_and_quickness_reconcile(self):
        profiles = {row['plan_id']: row for row in self.report['profiles']}
        for name in ('prespecified_46_minus_38', 'postinspection_exploratory_1_minus_0'):
            contrast = self.report[name]
            intervention = profiles[contrast['intervention_plan']]
            comparator = profiles[contrast['comparator_plan']]
            self.assertAlmostEqual(contrast['ca_gain_difference'],
                                   intervention['ca_gain'] - comparator['ca_gain'])
            self.assertEqual(set(contrast['attribute_gain_differences']),
                             set(intervention['attribute_gains']))
            self.assertEqual(set(intervention['attribute_gains']),
                             set(comparator['attribute_gains']))
            for attr, difference in contrast['attribute_gain_differences'].items():
                self.assertAlmostEqual(difference, intervention['attribute_gains'][attr] -
                                       comparator['attribute_gains'][attr])
            # Recompute each profile's index before taking the contrast, rather
            # than averaging the already-published differences.
            means = [(row['attribute_gains']['acceleration'] +
                      row['attribute_gains']['pace']) / 2
                     for row in (intervention, comparator)]
            self.assertAlmostEqual(contrast['quickness_mean_gain_difference'], means[0] - means[1])

    def test_key_contrast_and_complete_source_cell_accounting(self):
        contrast = self.report['prespecified_46_minus_38']
        self.assertAlmostEqual(contrast['ca_gain_difference'], 2.10)
        self.assertAlmostEqual(contrast['quickness_mean_gain_difference'], -0.175)
        self.assertEqual(self.report['source_plan_count'], 51)
        self.assertEqual(self.report['source_endpoint_columns'], 37)
        self.assertEqual(self.report['source_numeric_endpoints'], 1887)
        self.assertEqual(self.report['missing_endpoint_cells'], [])
        self.assertEqual(self.report['formula_cells'], 0)
        self.assertEqual(self.report['source_numeric_endpoints'],
                         self.report['source_plan_count'] * self.report['source_endpoint_columns'])

    def test_unknown_cluster_variance_does_not_become_inference(self):
        for name in ('prespecified_46_minus_38', 'postinspection_exploratory_1_minus_0'):
            for key in ('confidence_interval', 'p_value', 'independent_career_pairs'):
                self.assertIsNone(self.report[name][key])
        self.assertIsNone(self.report['independent_career_replicates'])
        self.assertIsNone(self.report['game_build'])
        self.assertFalse(self.report['native_measurements'])
        self.assertFalse(self.report['causal_effect_identified'])


if __name__ == '__main__':
    unittest.main()

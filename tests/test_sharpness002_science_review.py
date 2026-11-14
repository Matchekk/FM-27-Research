"""Independent synthetic raw-score checks, never native execution."""
import unittest
import numpy as np

from analysis import analyse_sharpness002 as project
from analysis.review_sharpness002_science import audit_math,audit_planning,synthetic,independently_group


class IndependentSharpnessScience(unittest.TestCase):
    def test_raw_score_algebra_uncertainty_holm_bootstrap_and_loo(self):
        result=audit_math()
        self.assertEqual(result['independent_blocks'],64)
        self.assertAlmostEqual(result['primary']['mean'],.22)
        self.assertEqual(len(result['secondary_holm']),7)

    def test_unpaired_side_variance_is_not_substituted_for_paired_block_variance(self):
        receipt,data=synthetic();contexts=independently_group(data,receipt)['SHARPNESS:xgd']
        for context in contexts:
            a,b=np.asarray(context['sides']);observed=np.var(context['blocks'],ddof=1)
            expected=(np.var(a,ddof=1)+np.var(b,ddof=1)+2*np.cov(a,b)[0,1])/4
            self.assertAlmostEqual(observed,expected)
            self.assertNotAlmostEqual(observed,(np.var(a,ddof=1)+np.var(b,ddof=1))/4)

    def test_complete_score_table_does_not_override_unreleased_prerequisite(self):
        receipt,data=synthetic();receipt['config']['gates']['tech17']['independently_released']=False
        with self.assertRaises(ValueError):project.analyse(data,receipt)

    def test_independent_future_power_integer_threshold_and_match_cost(self):
        result=audit_planning()
        self.assertEqual(len(result['plans']),4)
        self.assertTrue(all(p['conditional_power']>=.9 for p in result['plans']))


if __name__=='__main__':unittest.main()

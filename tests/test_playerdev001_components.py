import unittest
from copy import deepcopy
from analysis.summarize_playerdev001 import components
from analysis.review_playerdev001 import scalar_summary

class PlayerDevComponentsTest(unittest.TestCase):
    def test_components_preserve_unknowns_and_no_blend(self):
        # Synthetic API fixture; has no real-world prognostic evidential status.
        effect=dict(experiment_id='PD-ROLE-001',n_matches=4096,independent_blocks=512,
            primary={'mean':0,'ci':[-1,1]},descriptive_only={'JR_CF':{'xgd':{}},'JR_DLF':{'xgd':{}}})
        review=dict(passed=True,formal_estimands_checked=7)
        card=components(effect,review)
        self.assertEqual(card['status'],'NO_COMBINED_SUCCESS_SCORE')
        self.assertIsNone(card['development_potential']['probability_reaching_pa'])
        self.assertIsNone(card['current_performance']['actual_ca_efficiency'])
        self.assertFalse(card['baseline_comparison']['verified_improvement_over_baselines'])
        effect['n_matches']=4095
        with self.assertRaises(ValueError):components(effect,review)

    def test_scalar_moments_and_context_difference(self):
        effect=scalar_summary([[1.,2.,3.],[3.,4.,5.]])
        self.assertEqual(effect['mean'],3.)
        self.assertAlmostEqual(effect['se']**2,1/6)
        self.assertEqual(effect['df'],4.)
        difference=scalar_summary([[1.,2.,3.],[3.,4.,5.]],(1.,-1.))
        self.assertEqual(difference['mean'],-2.)

if __name__=='__main__':unittest.main()

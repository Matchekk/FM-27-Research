"""Independent package-score checks with synthetic data, no native engine."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from analysis import review_stless003 as review
from tests.test_stless003 import receipt_and_data


class IndependentPackageReviewTests(unittest.TestCase):
    def setUp(self):
        self.receipt, self.data = receipt_and_data()
        self.seeds = dict(main_seeds=self.receipt['seeds'], technical_seeds=[11, 12, 13, 14])

    def test_physical_interaction_and_holm7_match_independent_raw_score_math(self):
        # Producer import is deliberately confined to this software test.
        from analysis.analyse_stless003 import analyse
        effects, blocks = analyse(self.data, self.receipt)
        result = review.verify_stored_analysis(self.data, self.receipt, effects, blocks)
        self.assertTrue(result['stored_effects_verified']);self.assertEqual(result['derived_contrast_rows'], 512)
        self.assertAlmostEqual(result['primary']['mean'], .13)
        grouped = review.independently_group(self.data, self.receipt)
        self.assertAlmostEqual(review.summarize(grouped['IP:xgd'])['mean'], .2)
        self.assertAlmostEqual(review.summarize(grouped['OOP:xgd'])['mean'], .4)
        self.assertEqual(set(result['secondary_holm']), set(review.FAMILY))

    def test_incomplete_duplicate_wrong_package_and_uncontrolled_cache_reject(self):
        review.check_rows(self.data, self.receipt, self.seeds, 'main')
        wrong = deepcopy(self.data);wrong[0]['native_audit']['ip_strikerless'] = not wrong[0]['native_audit']['ip_strikerless']
        bad_cache = deepcopy(self.data);bad_cache[0]['descriptive']['first_sharpness_cache8a_mean'] = 70.
        for bad in (self.data[:-1], self.data[:-1] + [self.data[0]], wrong, bad_cache):
            with self.assertRaises(ValueError):review.check_rows(bad, self.receipt, self.seeds, 'main')

    def test_corrupt_derived_value_or_stored_holm_claim_rejects(self):
        from analysis.analyse_stless003 import analyse
        effects, blocks = analyse(self.data, self.receipt)
        wrong = deepcopy(blocks);wrong[0]['value'] += .01
        with self.assertRaisesRegex(ValueError, 'derived seed contrast'):
            review.verify_stored_analysis(self.data, self.receipt, effects, wrong)
        bad_effects = deepcopy(effects);bad_effects['secondary']['IP:xgd']['p_holm'] = .9
        with self.assertRaisesRegex(ValueError, 'Holm'):
            review.verify_stored_analysis(self.data, self.receipt, bad_effects, blocks)
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);dispatch=local/'main/dispatch';dispatch.mkdir(parents=True)
            proofs=local/'main/call-admissions';proofs.mkdir()
            (dispatch/'concurrency.jsonl').write_text('\n'.join(json.dumps(row) for row in [
                dict(event='claimed',job_id='a',active_claims=1),
                dict(event='completed',job_id='a',active_claims=0)])+'\n')
            claim=dict(job_id='a',unresolved_claims=0,new_claim_envelope_seconds=40,limit_seconds=3600,
                recorded_native_call_seconds=100.,resulting_bound_seconds=140.)
            (proofs/'a.json').write_text(json.dumps(claim))
            ledger=[dict(job_id='a',native_elapsed_seconds=3.)]
            self.assertEqual(review.audit_claim_envelopes(local,'main',ledger,100.)['actual_cumulative_seconds'],103.)
            claim['resulting_bound_seconds']=139.;(proofs/'a.json').write_text(json.dumps(claim))
            with self.assertRaisesRegex(ValueError,'inflight bound'):
                review.audit_claim_envelopes(local,'main',ledger,100.)


if __name__ == '__main__':
    unittest.main()

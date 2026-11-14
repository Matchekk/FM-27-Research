"""Independent reviewer checks with manufactured football scores, no engine."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from analysis import review_split004 as review
from tests.test_split004 import receipt_and_data


class IndependentSplitReviewTests(unittest.TestCase):
    def setUp(self):
        self.receipt, self.data = receipt_and_data()
        self.seeds = dict(main_seeds=self.receipt['seeds'], technical_seeds=[11, 12, 13, 14])

    def test_score_algebra_and_stored_nine_contrasts_reconstruct_independently(self):
        # Import producer only in this software comparison test, never in reviewer.
        from analysis.analyse_split004 import analyse
        effects, blocks = analyse(self.data, self.receipt)
        result = review.verify_stored_analysis(self.data, self.receipt, effects, blocks)
        self.assertTrue(result['stored_effects_verified'])
        self.assertEqual(result['derived_contrast_rows'], 576)
        self.assertAlmostEqual(result['primary']['mean'], -.2)
        grouped = review.independently_group(self.data, self.receipt)
        self.assertAlmostEqual(review.summarize(grouped['C90:xgd'])['mean'], .21)
        self.assertAlmostEqual(review.summarize(grouped['C7A:xgd'])['mean'], .41)
        self.assertAlmostEqual(review.summarize(grouped['INTERACTION:xgd'])['mean'], .12)

    def test_duplicate_incomplete_or_false_split_inputs_fail_closed(self):
        review.check_rows(self.data, self.receipt, self.seeds, 'main')
        bad_raw = deepcopy(self.data);bad_raw[0]['native_audit']['c90_raw'] = 9999
        for bad in (self.data[:-1], self.data[:-1] + [self.data[0]], bad_raw):
            with self.subTest(count=len(bad)), self.assertRaises(ValueError):
                review.check_rows(bad, self.receipt, self.seeds, 'main')

    def test_corrupt_stored_contrast_or_holm_claim_is_rejected(self):
        from analysis.analyse_split004 import analyse
        effects, blocks = analyse(self.data, self.receipt)
        bad_blocks = deepcopy(blocks);bad_blocks[0]['value'] += .01
        with self.assertRaisesRegex(ValueError, 'derived seed contrast'):
            review.verify_stored_analysis(self.data, self.receipt, effects, bad_blocks)
        bad_effects = deepcopy(effects);bad_effects['secondary']['C90:xgd']['p_holm'] = .9
        with self.assertRaisesRegex(ValueError, 'Holm'):
            review.verify_stored_analysis(self.data, self.receipt, bad_effects, blocks)

    def test_terminal_series_cannot_gain_scientific_outputs_or_success_flag(self):
        source=review.ROOT/'data/night-002-split004'
        if not (source/'termination.json').exists():self.skipTest('Terminal public archive not present')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);target=root/'data/night-002-split004';target.mkdir(parents=True)
            for name in ('termination.json','native-call-time.json','main-summary.json',
                    'main-job-accounting.jsonl','main-job-plan.json','technical-job-plan.json',
                    'seed-plan.json','manifest.json','termination-review.json'):
                if (source/name).exists():shutil.copyfile(source/name,target/name)
            doc=review.ROOT/'docs/night-002/SPLIT004-TERMINATION-REVIEW.md'
            if doc.exists():
                dest=root/'docs/night-002'/doc.name;dest.parent.mkdir(parents=True);shutil.copyfile(doc,dest)
            self.assertTrue(review.audit_terminal(root)['terminal_stop_verified'])
            (target/'effects.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'forbidden scientific'):review.audit_terminal(root)
            (target/'effects.json').unlink()
            summary=json.loads((target/'main-summary.json').read_text());summary['scientific_analysis_allowed']=True
            (target/'main-summary.json').write_text(json.dumps(summary))
            with self.assertRaisesRegex(ValueError,'relabeled successful'):review.audit_terminal(root)


if __name__ == '__main__':
    unittest.main()

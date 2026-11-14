"""Independent reviewer tests; synthetic results never stand for native evidence."""
from copy import deepcopy
import json
import math
from pathlib import Path
import tempfile
import unittest

from analysis import review_round3 as review


def sample():
    config = dict(identity={'build': 'synthetic-review-only'}, design=dict(
        setups={h: {str(s): {a: f'{h}-{s}-{a}' for a in review.ARMS} for s in (0, 1)} for h in review.CONTEXTS},
        matrix_sha256='own-synthetic-matrix'))
    manifest = dict(config=config, config_sha256=review.canonical_hash(config), seeds=list(range(1, 33)))
    data = []
    for context, h in enumerate(review.CONTEXTS):
        for i, seed in enumerate(manifest['seeds'][context*16:(context+1)*16]):
            for side in (0, 1):
                for arm in review.ARMS:
                    # Shared additive nuisance must cancel; side shifts must average.
                    treatment = (.4+.02*context+.002*(i-7.5)+.1*(2*side-1)) if arm == 'SJ' else 0
                    stats = [dict(xg=1., shots=10, shots_on_target=5, passes=100, completed_passes=80, possession=.5) for _ in (0, 1)]
                    stats[side]['xg'] += 2 + .01*i + treatment
                    data.append(dict(key=f'{h}-{seed}-{side}-{arm}', scenario=h, seed=seed, arm=arm,
                        tested_side=side, setup_sha256=f'{h}-{side}-{arm}', config_sha256=manifest['config_sha256'],
                        build='synthetic-review-only', status='ok', engine_readback=True, score=[1, 1],
                        team_statistics=stats, finish_tick=22000, input_contract_verified=True,
                        profile_fields_verified=1058, native_roles_verified=44, native_pi_cells_verified=44,
                        native_pi_groups_verified=748, native_raw_dose_verified=True,
                        design_matrix_sha256='own-synthetic-matrix'))
    return manifest, data


class IndependentReviewTests(unittest.TestCase):
    def calculate(self, manifest, data):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root/'manifest.json').write_text(json.dumps(manifest), encoding='utf8')
            (root/'main.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in data), encoding='utf8')
            return review.attr_results(root)

    def test_direct_contrast_side_context_weights_and_welch(self):
        manifest, data = sample()
        result = self.calculate(manifest, data)
        effect = result['effects']['xgd']
        self.assertAlmostEqual(effect['mean'], .41)
        self.assertAlmostEqual(effect['se'], math.sqrt(.00009066666666666667 / 32))
        self.assertAlmostEqual(effect['df'], 30.)
        self.assertEqual(result['n_matches'], 384)
        self.assertEqual(len(result['blocks']), 192)
        self.assertEqual(len(result['planning']['observed']), 2)
        self.assertEqual(result['effects']['points']['p_holm'], 1.)

    def test_strata_and_deterministic_bootstrap(self):
        a = review.inference([[0, 2], [10, 14]])
        self.assertEqual(a, review.inference([[0, 2], [10, 14]]))
        self.assertEqual(a['mean'], 6.5)
        self.assertAlmostEqual(a['se'], math.sqrt(1.25))
        self.assertLessEqual(a['bootstrap_ci'][0], a['mean'])
        self.assertGreaterEqual(a['bootstrap_ci'][1], a['mean'])

    def test_missing_failed_duplicate_foreign_gates_never_zero(self):
        manifest, data = sample()
        for candidate in (data[:-1], data+[data[0]]):
            with self.assertRaises(ValueError):
                self.calculate(manifest, candidate)
        for field, bad in [('status', 'failed'), ('native_raw_dose_verified', False),
                           ('profile_fields_verified', 1057), ('tested_side', True),
                           ('build', 'wrong'), ('seed', 999), ('setup_sha256', 'wrong')]:
            altered = deepcopy(data)
            altered[0][field] = bad
            with self.assertRaises(ValueError):
                self.calculate(manifest, altered)

    def test_holm_original_order_and_monotonicity(self):
        self.assertEqual(review.holm5([.03, .001, .02, .9, .5]), [.09, .005, .08, 1., 1.])
        with self.assertRaises(ValueError):
            review.holm5([.1])

    def test_historical_direct_rational_numbers(self):
        archive = review.training_archive()
        self.assertEqual(archive['player_rows'], 660)
        self.assertEqual(archive['contrasts'][0]['index_fraction'], '1/44')
        self.assertEqual(archive['contrasts'][1]['index_fraction'], '-3/88')
        self.assertEqual(archive['contrasts'][0]['exposure']['A']['match_minutes'], 14801)
        self.assertIsNone(archive['independent_replicates'])


if __name__ == '__main__':
    unittest.main()

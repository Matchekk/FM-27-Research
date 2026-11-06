"""Focused checks for the frozen ATTR-004 seed plan and statistical contracts."""
from itertools import combinations
import unittest

import numpy as np
from scipy.stats import ttest_rel

from analyse_attr004 import ARMS, METRICS, N, SCENARIOS, analyse, checked_rows, estimate, holm, seed_plan
from verify_matches import DATA, read


class AttributeStudyTests(unittest.TestCase):
    def test_seeds_are_disjoint_from_every_archived_match_series(self):
        validation, plan = seed_plan()
        history = read(DATA / "matches/manifest.json")["seeds"].values()
        historical = [row["seeds"] for row in read(DATA / "historical/audit.json")["studies"]]
        used = set().union(*history, *historical)
        self.assertEqual(len(plan), len(SCENARIOS))
        self.assertEqual(len(validation), 2)
        self.assertTrue(all(len(seeds) == N for seeds in plan.values()))
        for a, b in combinations([validation, *plan.values(), used], 2):
            self.assertFalse(set(a) & set(b))
        self.assertEqual(len(set().union(*plan.values())), 1120)

    def test_one_cell_reproduces_paired_t_test(self):
        a = np.array([0.9, -0.4, 0.7, 1.2, 0.6])
        b = np.array([0.2, 0.3, -0.1, 0.1, 0.0])
        expected = ttest_rel(a, b)
        actual = estimate([a - b], [1])
        ci = expected.confidence_interval()
        self.assertAlmostEqual(actual["p"], expected.pvalue)
        self.assertAlmostEqual(actual["ci95"][0], ci.low)
        self.assertAlmostEqual(actual["ci95"][1], ci.high)

    def test_holm_has_monotonic_adjusted_probabilities(self):
        tests = {str(i): {"p": p} for i, p in enumerate([0.001, 0.02, 0.018, 0.6])}
        for actual, expected in zip(self.adjusted(tests), [0.004, 0.054, 0.054, 0.6], strict=True):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual([r["reject"] for r in tests.values()], [True, False, False, False])

    @staticmethod
    def adjusted(tests):
        holm(tests)
        return [r["p_holm"] for r in tests.values()]

    def test_contrast_directions_and_complete_test_family(self):
        _, plan = seed_plan()
        indexed = {}
        for s, seeds in plan.items():
            formation, _, venue = SCENARIOS[int(s)]
            for j, seed in enumerate(seeds):
                baseline = j / 10
                a = 0.2 + 0.4 * (formation == "4231") + 0.6 * venue
                b = 0.1 + 0.2 * venue
                for arm, value in zip(ARMS, (baseline, baseline + a, baseline + b), strict=True):
                    indexed[s, seed, arm] = dict.fromkeys(METRICS, value)
        result = analyse(indexed)
        self.assertEqual(result["n_matches"], 3360)
        self.assertEqual(len(result["secondary"]), 33)
        self.assertAlmostEqual(result["primary"]["mean"], 0.5)
        self.assertEqual(result["primary"]["practical"], "JumpingReach")
        secondary = result["secondary"]
        for name, expected in (("formation", 0.4), ("opponent", 0.0), ("venue", 0.4),
                               ("formation*opponent*venue", 0.0)):
            self.assertAlmostEqual(secondary[f"JumpingReach-Acceleration/xgd/{name}"]["mean"], expected)
        for metric in METRICS:
            self.assertAlmostEqual(secondary[f"JumpingReach-baseline/{metric}"]["mean"], 0.7)
            self.assertAlmostEqual(secondary[f"Acceleration-baseline/{metric}"]["mean"], 0.2)

    def test_analysis_refuses_to_start_on_missing_matches(self):
        reference = read(DATA / "matches/manifest.json")
        _, seeds = seed_plan()
        with self.assertRaisesRegex(ValueError, "Missing 3360 matches"):
            checked_rows([], dict(reference, seeds=seeds))
        with self.assertRaisesRegex(ValueError, "Unregistered engine"):
            checked_rows([], dict(reference, seeds=seeds, build="changed"))


if __name__ == "__main__":
    unittest.main()

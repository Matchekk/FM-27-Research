"""Deterministic model sanity tests; NOT a held-out match outcome validation."""
import unittest

from analysis.meta_score_v01 import compare, evaluate, load_model


class MetaScoreV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = load_model()

    def profile(self, pos, value):
        return {k: value for k in self.model["positions"][pos]["weights_pct"]}

    def test_all_main_weights_sum_to_100(self):
        for position, entry in self.model["positions"].items():
            self.assertEqual(sum(entry["weights_pct"].values()), 100, position)
            self.assertTrue(all(w >= 0 for w in entry["weights_pct"].values()))

    def test_bounds_for_all_positions(self):
        for position in self.model["positions"]:
            self.assertAlmostEqual(evaluate(position, self.profile(position, 1), self.model)["score"], 0)
            self.assertAlmostEqual(evaluate(position, self.profile(position, 20), self.model)["score"], 100)

    def test_uniform_15_is_same_for_all(self):
        for position in self.model["positions"]:
            self.assertAlmostEqual(evaluate(position, self.profile(position, 15), self.model)["score"],
                                   round(1400 / 19, 2))

    def test_fictive_striker(self):
        data = {"acceleration": 14, "pace": 16, "jumping_reach": 15,
                "stamina": 13, "anticipation": 12, "balance": 13,
                "strength": 13, "finishing": 14, "concentration": 11,
                "dribbling": 13}
        result = evaluate("ST", data, self.model)
        self.assertAlmostEqual(result["score"], 68.68)
        self.assertEqual(result["position"], "ST")
        self.assertTrue(result["heuristic_gray_band"][0] < result["score"])
        self.assertTrue(result["heuristic_gray_band"][1] > result["score"])
        self.assertFalse(result["gray_band_is_statistical_confidence_interval"])

    def test_fictive_goalkeeper(self):
        result = evaluate("TW", {"agility": 16, "reflexes": 15, "aerial_reach": 13,
                                  "acceleration": 11, "handling": 13}, self.model)
        self.assertEqual(result["position"], "GK")
        self.assertAlmostEqual(result["score"], 72.89)
        self.assertEqual(result["heuristic_gray_band"], [67.89, 77.89])

    def test_goalkeeper_agility_weight_exceeds_reflex(self):
        baseline = self.profile("GK", 12)
        a = dict(baseline, agility=13)
        b = dict(baseline, reflexes=13)
        self.assertGreater(evaluate("GK", a, self.model)["score"],
                           evaluate("GK", b, self.model)["score"])

    def test_compare_clear_and_gray(self):
        first = self.profile("ST", 18)
        second = self.profile("ST", 7)
        comparison = compare("ST", first, second, self.model)
        self.assertEqual(comparison["verdict"], "FIRST_FAVORED_WITHIN_MODELED_CONTEXTS")
        same = compare("ST", first, first, self.model)
        self.assertEqual(same["verdict"], "GRAY_OVERLAP")

    def test_reject_missing_and_invalid(self):
        st = self.profile("ST", 12)
        st.pop("pace")
        with self.assertRaisesRegex(ValueError, "Missing attribute"):
            evaluate("ST", st, self.model)
        for val in [0, 21, float("nan"), float("inf"), True, "12"]:
            st = self.profile("ST", 12)
            st["pace"] = val
            with self.assertRaisesRegex(ValueError, "Invalid attribute"):
                evaluate("ST", st, self.model)

    def test_aliases_and_position_scope(self):
        st = self.profile("ST", 12)
        self.assertEqual(evaluate("9", st, self.model)["position"], "ST")
        with self.assertRaisesRegex(ValueError, "Unknown position"):
            evaluate("BPL", st, self.model)


if __name__ == "__main__":
    unittest.main()

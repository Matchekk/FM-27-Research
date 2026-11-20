from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from player_endpoints import endpoint


def rows(*observations):
    return [dict(day=day, ca=ca, birth="2008-01-01", pa=160, position="ST")
            for day, ca in observations]


class QuarterTest(unittest.TestCase):
    def test_missing_exact_end_differs_from_small_gain(self):
        incomplete = endpoint(rows(("2027-03-31", 100), ("2027-06-29", 107)))
        small = endpoint(rows(("2027-03-31", 100), ("2027-06-30", 102)))
        for value in (incomplete, small):
            self.assertIsNone(value["last_observed_quarter_gain_at_least_3_ca"])
        self.assertEqual(incomplete["exact_quarter_windows"], 0)
        self.assertEqual(small["exact_quarter_windows"], 1)

    def test_reports_last_qualified_observed_window(self):
        value = endpoint(rows(("2027-03-30", 100), ("2027-06-30", 104),
                              ("2027-09-30", 107), ("2027-12-30", 108)))
        self.assertEqual(value["exact_quarter_windows"], 3)
        self.assertEqual(value["last_observed_quarter_gain_at_least_3_ca"],
                         {"start":"2027-06-30", "end":"2027-09-30", "delta_ca":3})

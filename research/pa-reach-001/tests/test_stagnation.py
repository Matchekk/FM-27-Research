from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from stagnation import course


class StagnationTest(unittest.TestCase):
    def test_middle_measurement_and_declines_matter(self):
        self.assertEqual(course(100, 101, 100), "stagnant_observed_range_le1")
        self.assertEqual(course(100, 105, 100), "fluctuating_net_within_one")
        self.assertEqual(course(100, 100, 98), "net_decline_ge2")
        self.assertEqual(course(100, 102, 103), "net_gain_ge2")

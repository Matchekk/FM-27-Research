import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from facilities_and_pa import coverage
from immediate_renewals import compile_group


class SavePairTests(unittest.TestCase):
    def test_asymmetric_matrix_and_zero_and_unknown(self):
        def row(factor, ca=100):
            return ("birth", b"name", ca, 120, factor)

        result = compile_group([(row(2), row(3, 101)), (row(0), row(1)), (row(None), row(0))])
        self.assertEqual(result["matrix_before_rows_after_columns_1_to_5"][1][2], 1)
        self.assertEqual(result["matrix_before_rows_after_columns_1_to_5"][2][1], 0)
        self.assertEqual(len(result["zero_or_missing_transitions"]), 2)
        self.assertEqual(result["null_at_either_end"], 1)
        self.assertEqual(result["delta_CA_counts"], {0: 2, 1: 1})

    def test_no_facility_substitution_and_strict_cap_margin(self):
        fixtures = ({1: 16, 2: None, 3: 17, 4: 17}, {1: 16, 2: 17, 3: 16, 4: 17})
        pairs = [(uid, 73, 100, 100, 1, 1) for uid in range(1, 5)]
        pairs.append((4, 72, 100, 100, 1, 1))
        results = coverage(fixtures, pairs)["baseline_outfield_under28"]
        narrow = results["same_observed_club_and_stable_pa_factor_1_4_above_cap_plus_two"]
        self.assertEqual(narrow, {"players": 4, "with_stable_decoded_rating": 2,
                                  "at_decoded_16": 1, "at_decoded_17": 1})

    def test_observed_groups_conserve_the_source_population(self):
        result = json.loads((ROOT / "manifests/immediate-renewals.json").read_bytes())
        groups = result["groups"]
        primary = ("due", "later", "intake", "remaining_club_inventory", "outside_observed_club_inventory")
        self.assertEqual(sum(groups[g]["n"] for g in primary), result["stable_uid_birth_full_name_pairs"])
        for group in groups.values():
            known = sum(sum(row) for row in group["matrix_before_rows_after_columns_1_to_5"])
            others = sum(t["n"] for t in group["zero_or_missing_transitions"])
            self.assertEqual(known + others, group["n"])
            self.assertEqual(sum(group["delta_CA_counts"].values()), group["n"])
            self.assertEqual(sum(group["delta_PA_counts"].values()), group["n"])

"""Censoring and public-ledger checks run without private game data or fmsave."""
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/pa-reach-001/analysis/player_endpoints.py"
SPEC = importlib.util.spec_from_file_location("pa_player_endpoints", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def row(day, ca, pa=101, birth="2000-03-01"):
    return dict(day=day, ca=ca, pa=pa, birth=birth, position="DC")


class Endpoints(unittest.TestCase):
    def test_baseline_pa_and_threshold_rounding(self):
        result = MODULE.endpoint([row("2027-03-01", 95), row("2027-04-01", 96, 99)])
        self.assertEqual(result["targets"]["pa95"]["status"], "OBSERVED_HIT")
        self.assertEqual(result["targets"]["full"]["status"], "RIGHT_CENSORED")
        self.assertTrue(result["pa_changed_in_window"])
        self.assertIsNone(result["ca_at_exact_month"]["12"])

    def test_birthdate_inclusive_but_later_peak_excluded(self):
        result = MODULE.endpoint([row("2028-02-01", 99), row("2028-03-01", 100),
                                  row("2028-03-02", 101)])
        self.assertEqual(result["observed_peak_CA"], 100)
        self.assertEqual(result["targets"]["pa_minus_2"]["status"], "ALREADY_AT_BASELINE")
        self.assertIn("COVERAGE_UNVERIFIED", result["targets"]["full"]["status"])
        result = MODULE.endpoint([row("2028-02-01", 99), row("2028-03-01", 101)])
        self.assertEqual(result["targets"]["full"]["first_observed_hit"], "2028-03-01")

    def test_archived_counts_reconcile_and_release_is_closed(self):
        s = json.loads((ROOT / "data/pa-reach-001/summary.json").read_bytes())
        for day, record in s["snapshots"].items():
            self.assertEqual(record["accepted_ability_pairs"], sum(s["byte_counts"][day].values()))
            excluded = sum(record.get(k, 0) for k in ("no_native_uid", "no_closing_identity",
                           "ambiguous_uid", "birth_missing_or_mismatch", "ability_mismatch", "unresolved_ability"))
            self.assertEqual(record["save_records"], excluded + record["accepted_ability_pairs"])
        self.assertEqual(sum(s["first_last_candidate_transitions"].values()), s["linkage"]["paired"])
        endpoints = s["baseline_outfield_under28_endpoint_counts"]
        self.assertEqual(len({sum(counts.values()) for counts in endpoints.values()}), 1)
        self.assertEqual(s["independent_test_careers"], 0)
        self.assertIsNone(s["calibration_metrics"])

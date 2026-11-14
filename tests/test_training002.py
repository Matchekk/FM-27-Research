from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from research.training002 import (INDEX, calibration_diagnostic, file_sha256, historical_diagnostic,
                                  read_checkpoint, read_json, replicate_diagnostic)

ROOT = Path(__file__).resolve().parents[1]


class Training002Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = self.root / "synthetic-source.txt"
        source.write_bytes(b"OWN SYNTHETIC CHECKPOINT RECEIPT: NO FM SAVE")
        self.digest = file_sha256(source)
        self.sources = {self.digest: source}
        m = self.m
        player = dict(subject="S01", attributes_raw={k: m(60, "attribute_raw") for k in INDEX},
                      attributes_display={k: m(12, "attribute_display") for k in INDEX},
                      ca=m(120, "ca_raw"), pa=m(150, "pa_raw"), condition=m(10000, "condition_raw"),
                      sharpness=m(7000, "sharpness_raw"), fatigue=None, match_minutes=m(90, "minutes"),
                      focus=m("stamina", "focus_code"), intensity=m(2, "intensity_raw"))
        self.row = dict(schema="train002.checkpoint.v1", origin="synthetic", build="synthetic-build",
                        decoder="own-synthetic-v1", start_save_sha256=self.digest,
                        checkpoint_save_sha256=self.digest, replicate="R01", arm="A", day="2026-11-14",
                        rng=m("rng1", "career_rng_stream"), controls={k: m(self.digest, "sha256") for k in
                        ("coaches", "facilities", "roster", "opponents", "policy")},
                        calendar=[dict(day="2026-11-13", slot=0, session=m(303, "session_code"))],
                        participation=[dict(subject="S01", day="2026-11-13", slot=0,
                                            session=m(303, "session_code"), status=m("attended", "participation_status"),
                                            minutes=m(60, "minutes"), coach=m("coach1", "coach_code"))],
                        players=[player], injuries=[])

    def m(self, value, unit):
        return dict(value=value, unit=unit, source_sha256=self.digest, locator="synthetic_field")

    def read(self, row=None):
        path = self.root / "checkpoint.json"
        path.write_text(json.dumps(self.row if row is None else row), encoding="utf8")
        return read_checkpoint(path, self.sources)

    def test_receipts_are_not_release_or_semantic_proof(self):
        r = self.read()
        self.assertTrue(r["structurally_valid"])
        self.assertEqual(r["missing"], ["players.fatigue"])
        self.assertFalse(r["native_released"])
        self.assertFalse(r["career_released"])
        self.assertFalse(r["source_semantics_verified"])
        self.assertEqual(len(r["blocked_gates"]), 7)

    def test_no_flag_or_native_claim_can_bypass_gate(self):
        for key, value in (("individual_exposure_verified", True), ("career_released", True)):
            row = deepcopy(self.row)
            row[key] = value
            with self.assertRaises(ValueError):
                self.read(row)
        self.row["origin"] = "native_validated"
        with self.assertRaises(ValueError):
            self.read()

    def test_byte_receipt_mismatch_and_missing_receipt_fail(self):
        self.row["players"][0]["ca"]["source_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "Unresolved"):
            self.read()
        self.sources[self.digest].write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "SHA256 mismatch"):
            self.read()

    def test_missing_participation_is_not_calendar_or_zero(self):
        self.row["participation"] = None
        r = self.read()
        self.assertIn("participation", r["missing"])
        self.assertIn("individual_session_coverage", r["missing"])
        self.assertEqual(r["scheduled_slots"], 1)
        self.assertFalse(r["career_released"])

    def test_duplicates_wrong_sessions_and_impossible_exposure_fail(self):
        row = deepcopy(self.row)
        row["participation"] *= 2
        with self.assertRaises(ValueError):
            self.read(row)
        row = deepcopy(self.row)
        row["participation"][0]["session"]["value"] = 304
        with self.assertRaisesRegex(ValueError, "session mismatch"):
            self.read(row)
        self.row["participation"][0]["status"]["value"] = "rest"
        with self.assertRaisesRegex(ValueError, "Nonparticipation"):
            self.read()

    def test_units_booleans_and_attribute_bounds(self):
        for field, value in (("ca", True), ("condition", 10001)):
            row = deepcopy(self.row)
            row["players"][0][field]["value"] = value
            with self.assertRaises(ValueError):
                self.read(row)
        self.row["players"][0]["attributes_raw"]["pace"]["unit"] = "attribute_display"
        with self.assertRaisesRegex(ValueError, "Unit mismatch"):
            self.read()

    def test_session_codes_and_participation_slots_are_strict_integers(self):
        for value in (303.5, True, -1, 65536):
            row = deepcopy(self.row)
            row['calendar'][0]['session']['value'] = value
            row['participation'][0]['session']['value'] = value
            with self.assertRaises(ValueError):
                self.read(row)
        for value in (False, 0.0, -1, 3):
            row = deepcopy(self.row)
            row['participation'][0]['slot'] = value
            with self.assertRaises(ValueError):
                self.read(row)

    def test_injury_expected_return_is_not_observed_duration(self):
        self.row["injuries"] = [dict(event="I01", subject="S01", start="2026-11-12", end="2026-11-20",
                                     end_kind="expected_return", cause="training", source_sha256=self.digest,
                                     locator="injury01")]
        self.assertIn("injury_observed_interval", self.read()["missing"])
        self.row["injuries"][0]["end_kind"] = "observed_return"
        with self.assertRaisesRegex(ValueError, "Future"):
            self.read()
        self.row["injuries"][0]["end"] = "2026-11-01"
        with self.assertRaisesRegex(ValueError, "Negative"):
            self.read()

    def test_rng_clone_labels_never_create_independent_n(self):
        a = self.read()
        b = deepcopy(a)
        b["replicate"] = "R02"
        r = replicate_diagnostic([a, b])
        self.assertEqual(r["declared_replicates"], 2)
        self.assertEqual(r["start_clone_groups"], 1)
        self.assertEqual(r["rng_label_clone_groups"], 1)
        self.assertIsNone(r["independent_replicates_verified"])
        b["claimed_rng_stream"] = "different_claim"
        self.assertFalse(replicate_diagnostic([a, b])["rng_independence_verified"])
        b["replicate"] = a["replicate"]
        b["control_hash_claims"]["coaches"] = "a" * 64
        self.assertEqual(replicate_diagnostic([a, b])["within_pair_control_mismatch"], 1)

    def test_no_conversion_inferred_from_sparse_or_conflicting_scales(self):
        result = calibration_diagnostic([(60, 12), (60, 13), (61, 12)])
        self.assertEqual(result["conflicting_raw_values"], [60])
        self.assertFalse(result["mapping_validated"])
        self.assertIsNone(result["conversion_formula"])
        with self.assertRaises(ValueError):
            calibration_diagnostic([(-1, 0)])

    def test_json_negatives_and_save_not_decoded(self):
        path = self.root / "invalid.json"
        for value in ('{"a":1,"a":2}', '{"a":NaN}'):
            path.write_text(value, encoding="utf8")
            with self.assertRaises(ValueError):
                read_json(path)
        with self.assertRaisesRegex(ValueError, "not an FM save decoder"):
            read_json(self.root / "private.fm")

    def test_historical_660_rows_and_descriptions_unchanged(self):
        r = historical_diagnostic(ROOT)
        self.assertEqual(r["player_rows"], 660)
        self.assertEqual(r["build"], "27.0.0+2493426")
        self.assertAlmostEqual(r["exploratory_descriptions"][0]["index_difference_raw"], 1 / 44)
        self.assertAlmostEqual(r["exploratory_descriptions"][1]["index_difference_raw"], -3 / 88)
        self.assertEqual(r["exploratory_descriptions"][0]["observed_exposure_aggregates"]["A"],
                         dict(match_minutes=14801, injury_entries=9))
        self.assertIsNone(r["injury_days"])
        self.assertIsNone(r["individual_participation"])
        self.assertFalse(r["career_released"])
        self.assertNotIn("subject", json.dumps(r))


if __name__ == "__main__":
    unittest.main()

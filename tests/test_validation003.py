"""Offline profile and private capacity contract tests; no native imports."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from research.validation003 import (PROFILE_RANGES, REQUIRED_PROFILE_FIELDS, audit_readback,
    bind_profiles, context_from_dump, inspect_pkm_file, profile, profile_catalog, public_context,
    validate_attributes)


def native_dump(counts=(26, 18)):
    return {"teams": [dict(side=s, count=n, players=[
        dict(id=s * 1000 + i + 1, attributes=profile("ST", "ST", "ST")["attributes"])
        for i in range(n)]) for s, n in enumerate(counts)]}


class ProfileTests(unittest.TestCase):
    def test_native_position_scale20_and_ability_scale100_regression(self):
        # Public own P1C/P1B intent vectors exercise the real API scale in CI.
        root = Path(__file__).resolve().parents[1]
        public = json.loads((root / "data/tact-001-p1b/inputs.json").read_text(encoding="utf8"))
        # The public archive specifies this own profile as an explicit rule,
        # deliberately omitting private player IDs rather than storing dump arrays.
        rule = public["synthetic_profiles"]["attribute_rule"]
        self.assertIn("every ability index 15..68 raw 60", rule)
        self.assertIn("GK 20, other position values 0", rule)
        found = [[20] + [0] * 14 + [60] * 54,
                 [0, 0] + [20] * 13 + [60] * 54]
        self.assertTrue(any(max(v[15:]) > 20 for v in found))
        for v in found: validate_attributes(v)
        vector = [20] * 15 + [100] * 54
        validate_attributes(vector)
        for index, value in ((0, 21), (15, 101), (16, True)):
            bad = list(vector); bad[index] = value
            with self.assertRaises(ValueError): validate_attributes(bad)

    def test_explicit_21_vectors_have_69_values_and_active_union(self):
        catalog = profile_catalog()
        self.assertEqual(len(catalog), 21)
        for item in catalog.values():
            self.assertEqual(len(item["attributes"]), 69)
            self.assertEqual(item["position_ratings"], item["attributes"][:15])
            self.assertFalse(item["native_validated"])
            self.assertTrue(all(item["attributes"][i] == 20 for i in item["active_rating_families"]))
        dm = catalog["DM-medium"]; self.assertEqual(dm["active_rating_families"], [5, 7])
        self.assertEqual(profile("IV", "DCL", "DCR")["active_rating_families"], [3])
        self.assertEqual(catalog["GK-high"]["position_ratings"], [20] + [0] * 14)

    def test_strength_is_declared_skill_vector_not_all_fields_or_ca(self):
        low = profile("ST", "ST", "ST", "low"); high = profile("ST", "ST", "ST", "high")
        self.assertEqual(low["position_ratings"], high["position_ratings"])
        self.assertEqual(low["attributes"][63], high["attributes"][63])  # injury proneness
        self.assertGreater(high["attributes"][17], low["attributes"][17])
        self.assertNotIn("current_ability", high)
        with self.assertRaises(ValueError): profile("GK", "GK", "ST")
        with self.assertRaises(ValueError): profile("ST", "GK", "ST")
        with self.assertRaises(ValueError): profile("ST", "unknown", "ST")

    def test_readback_has_missing_not_invented_defaults(self):
        item = dict(native_id=123, side=0, attributes=profile("ST", "ST", "ST")["attributes"])
        result = audit_readback(item, deepcopy(item))
        self.assertFalse(result["passed"])
        self.assertIn("expected.native_profile.sharpness", result["missing"])
        self.assertIn("observed.after_original_preparation", result["missing"])

    def test_synthetic_full_readback_mismatch_and_type_rejection(self):
        desired = dict(native_id=123, side=0, attributes=profile("ST", "ST", "ST")["attributes"],
                       native_profile={k: lo for k, (lo, hi) in PROFILE_RANGES.items()})
        actual = deepcopy(desired)
        actual.update({k: True for k in ("both_phases_verified", "effective_seed_verified",
            "identity_verified", "after_original_preparation", "passive_effectiveness_verified")})
        self.assertEqual(set(PROFILE_RANGES), set(REQUIRED_PROFILE_FIELDS))
        self.assertTrue(audit_readback(desired, actual)["passed"])
        self.assertFalse(audit_readback(desired, actual)["native_validation_granted"])
        actual["native_profile"]["sharpness"] += 1
        self.assertIn("native_profile.sharpness", audit_readback(desired, actual)["mismatches"])
        actual["side"] = False
        self.assertFalse(audit_readback(desired, actual)["passed"])
        desired["native_profile"]["condition"] = -1
        actual["native_profile"]["condition"] = -1
        self.assertFalse(audit_readback(desired, actual)["passed"])


class CapacityTests(unittest.TestCase):
    def test_arbitrary_native_capacities_preserved_and_public_ids_absent(self):
        context = context_from_dump(native_dump(), "a" * 64)
        self.assertEqual([t["count"] for t in context["private_teams"]], [26, 18])
        intentions = {s: [profile("ST", "ST", "ST")] * n for s, n in enumerate((26, 18))}
        bound = bind_profiles(context, intentions)
        self.assertEqual(len(bound), 44)
        self.assertEqual([x["native_id"] for x in bound[:26]], list(range(1, 27)))
        public = public_context(context)
        self.assertFalse(public["career_replay_released"])
        self.assertNotIn("private", json.dumps(public))
        self.assertNotIn("player_ids", json.dumps(public))
        self.assertIn("fixture_to_dump_binding", public["missing"])
        intentions[0] = intentions[0][:23]
        with self.assertRaisesRegex(ValueError, "capacity exactly"): bind_profiles(context, intentions)

    def test_duplicate_missing_bad_capacity_and_bad_attributes_fail(self):
        for change in (lambda d: d["teams"][0].update(count=23),
                       lambda d: d["teams"][1]["players"][0].update(id=1),
                       lambda d: d["teams"][0]["players"][0].update(attributes=[12] * 68),
                       lambda d: d["teams"][0]["players"][0].update(id=True)):
            data = native_dump(); change(data)
            with self.assertRaises(ValueError): context_from_dump(data, "a" * 64)

    def test_opaque_pkm_is_fingerprinted_not_decoded(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synthetic.pkm"; path.write_bytes(b"test only, not an FM file")
            result = inspect_pkm_file(path)
            self.assertIsNone(result["capacity"])
            self.assertEqual(result["reader_status"], "opaque_not_decoded")
            self.assertFalse(result["career_replay_released"])
            self.assertNotIn(str(path), json.dumps(result))


if __name__ == "__main__": unittest.main()

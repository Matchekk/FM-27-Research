"""Own synthetic codec tests; never a native effectiveness receipt."""
from pathlib import Path
import json
import tempfile
import unittest

from research.startpolicy import (StartPolicy, decode_records, encode_records,
                                  encode_startpolicy, native_status)
from analysis.verify_mech002_preparation import inspect_binary


def records():
    # Own fake slots only. Nontrivial order proves that roster slot != lineup slot.
    result = [(62, 0, 0, 0, 1)]
    for side in (0, 1):
        result += [(17, side, 0, 0, 23)]
        result += [(11, side, i, 0, (i + 3) % 23) for i in range(11)]
        for slot in range(23):
            result += [(15, side, slot, field, value) for field, value in
                       ((15, 10000), (16, 10000), (17, 10000), (18, 0), (20, 80), (21, 100), (22, 20))]
        result += [(1, side, 1, 16, 60), (4, side, 0, 123, 456),
                   (6, side, 0, 2, 0), (2, side, 10, 0, 1313689463)]
    return result


class StartPolicyTests(unittest.TestCase):
    def test_default_binary_identity_and_full_roundtrip(self):
        source = records()
        payload = encode_records(source)
        self.assertEqual(encode_startpolicy(source), payload)
        self.assertEqual(encode_records(decode_records(payload)), payload)
        self.assertEqual(encode_startpolicy(source, StartPolicy(0, 10000)), payload)

    def test_only_twenty_declared_records_both_sides_and_lineup_binding(self):
        source = records()
        for side in (0, 1):
            changed = decode_records(encode_startpolicy(source, StartPolicy(side, 7000)))
            differences = [(a, b) for a, b in zip(source, changed, strict=True) if tuple(a) != b]
            self.assertEqual(len(differences), 20)
            self.assertEqual({a[2] for a, _ in differences}, set(range(4, 14)))
            self.assertEqual({a[3] for a, _ in differences}, {16, 17})
            for old, new in differences:
                self.assertEqual(old[:4], new[:4])
                self.assertEqual(new[0:2], (15, side))
                self.assertEqual((old[4], new[4]), (10000, 7000))
            self.assertEqual(source, records())  # Inputs never mutated.

    def test_strict_policy_types_and_levels(self):
        for side, level in ((True, 7000), (2, 7000), (0, True), (0, 7001), (0, -1)):
            with self.assertRaises(ValueError): StartPolicy(side, level)
        with self.assertRaises(ValueError): encode_startpolicy(records(), {"level_raw": 7000})

    def test_missing_duplicate_invalid_records_and_execution_fail_closed(self):
        source = records()
        cases = [source + [(61, 0, 0, 0, 100)], source + [(15, 0, 0, 23, 0)],
                 source + [(15, 0, 0, 16, 10000)],
                 [r for r in source if r[:4] != (15, 0, 10, 17)],
                 [r for r in source if r[:2] != (17, 0)],
                 [r for r in source if r[:3] != (11, 1, 0)],
                 source + [(15, 0, 23, 16, 10000)]]
        for bad in cases:
            with self.subTest(case=cases.index(bad)):
                with self.assertRaises(ValueError): encode_startpolicy(bad, StartPolicy(0, 7000))
        bad = list(source)
        i = bad.index((15, 1, 0, 18, 0)); bad[i] = (15, 1, 0, 18, 1)
        with self.assertRaises(ValueError): encode_startpolicy(bad, StartPolicy(0, 7000))
        for field, value in ((16, 10001), (17, 0xffffffff), (0, 221)):
            bad = [r for r in source if r[:4] != (15, 0, 1, field)] + [(15, 0, 1, field, value)]
            with self.assertRaises(ValueError): encode_startpolicy(bad, StartPolicy(0, 7000))

    def test_read_only_summary_omits_raw_records_and_identities(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "own-synthetic.bin"
            payload = encode_records(records()); path.write_bytes(payload)
            report = inspect_binary(path)
            self.assertEqual(path.read_bytes(), payload)
            self.assertEqual(report["name"], "own-synthetic.bin")
            self.assertEqual([r["low_changed_records"] for r in report["sides"]], [20, 20])
            self.assertNotIn("players", report)
            self.assertNotIn("path", report)

    def test_binary_negatives_and_no_native_grant(self):
        valid = encode_records(records())
        for bad in (b"", b"FM27CFG1", valid[:-1], valid + b"x", b"BADMAGIC" + valid[8:]):
            with self.assertRaises(ValueError): decode_records(bad)
        for bad in ([(15, 0, 1, 16, True)], [(15, 0, 1, 16, -1)], [(15, 0)]):
            with self.assertRaises(ValueError): encode_records(bad)
        a = native_status(); a["native_execution_allowed"] = True
        self.assertFalse(native_status()["native_execution_allowed"])
        self.assertEqual(native_status()["status"], "blocked")

    def test_draft_contrast_signs_accounting_and_explicit_block(self):
        root = Path(__file__).resolve().parents[1]
        contract = json.loads((root / "data/mech-002/contract-draft.json").read_text(encoding="utf8"))
        self.assertEqual(contract["blockers"], native_status()["blockers"])
        self.assertFalse(contract["native_execution_allowed"])
        self.assertEqual(contract["actual"]["new_seeds_reserved"], 0)
        self.assertEqual(contract["planned_only"]["main_matches"], 32 * 2 * 2 * 4)
        self.assertEqual(contract["actual"]["main_unbegun"], 512)
        self.assertEqual(contract["actual"]["technical_unbegun"], 35)
        self.assertEqual(len(contract["secondary_holm8"]), 8)
        # Full=10, low=6 under Standard; full=12, low=5 under MoreOften.
        # The low-sharpness loss increases from -4 to -7 => DoD=-3.
        arms = (10, 6, 12, 5)
        actual = {k: sum(a * b for a, b in zip(arms, weights, strict=True))
                  for k, weights in contract["contrasts"].items()}
        self.assertEqual(actual, dict(full_advantage=5.5, pressing_main=0.5,
                                      sharpness_loss_by_pressing=-3))


if __name__ == "__main__":
    unittest.main()

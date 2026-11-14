"""Offline-only tests for the Test FM Research private capture; no FM dependency."""
from hashlib import sha256
from pathlib import Path
import json
import tempfile
import unittest

from analysis.capture_test_fm_research import (CaptureError, build_receipt, write_private_receipt)


class TestFMCaptureTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.pre = self.root / "PRIVATE_PLAYER_NAMES_PRE.fm"
        self.pre.write_bytes(b"synthetic test fixture before match")
        self.pkm = self.root / "PRIVATE_MATCH_NAME.pkm"
        self.pkm.write_bytes(b"synthetic match fixture")
        self.rec = self.root / "PRIVATE_REC_NAME.rec"
        self.rec.write_bytes(b"synthetic rec fixture")

    def test_read_only_hashing_and_privacy(self):
        receipt = build_receipt(self.pre, pkms=[self.pkm], recs=[self.rec])
        self.assertEqual(len(receipt["artifacts"]), 3)
        self.assertEqual(receipt["artifacts"][0]["sha256"], sha256(self.pre.read_bytes()).hexdigest())
        self.assertEqual(self.pre.read_bytes(), b"synthetic test fixture before match")
        payload = json.dumps(receipt)
        self.assertNotIn("PRIVATE_PLAYER_NAMES", payload)
        self.assertNotIn("PRIVATE_MATCH_NAME", payload)
        self.assertNotIn(str(self.root), payload)
        self.assertFalse(receipt["capabilities"]["original_career_replay_released"])
        self.assertFalse(receipt["capabilities"]["training_executor_released"])

    def test_missing_wrong_format_empty_and_duplicate_rejected(self):
        with self.assertRaises(CaptureError):
            build_receipt(self.root / "missing.fm")
        with self.assertRaises(CaptureError):
            build_receipt(self.pkm)
        with self.assertRaises(CaptureError):
            build_receipt(self.pre, post_save=self.pre)
        self.pre.write_bytes(b"")
        with self.assertRaises(CaptureError):
            build_receipt(self.pre)

    def test_private_output_no_overwrite_or_escape(self):
        payload = build_receipt(self.pre)
        private = self.root / "local"
        out = private / "test-fm-research" / "capture-001.json"
        written = write_private_receipt(payload, out, private_root=private)
        self.assertEqual(written.resolve(), out.resolve())
        self.assertEqual(json.loads(out.read_text(encoding="utf8"))["project"], "Test FM Research")
        with self.assertRaises(CaptureError):
            write_private_receipt(payload, out, private_root=private)
        with self.assertRaises(CaptureError):
            write_private_receipt(payload, self.root / "leak.json", private_root=private)
        with self.assertRaises(CaptureError):
            write_private_receipt(payload, private / "leak.txt", private_root=private)

    def test_optional_post_and_multiple_pkms(self):
        after = self.root / "after.fm"
        after.write_bytes(b"synthetic after snapshot")
        another = self.root / "another.pkm"
        another.write_bytes(b"synthetic second match")
        receipt = build_receipt(self.pre, post_save=after, pkms=[self.pkm, another])
        self.assertEqual([a["role"] for a in receipt["artifacts"]],
                         ["pre_match_save", "post_match_save", "match_pkm", "match_pkm"])
        self.assertEqual([a["ordinal"] for a in receipt["artifacts"]], [1, 1, 1, 2])


if __name__ == "__main__":
    unittest.main()

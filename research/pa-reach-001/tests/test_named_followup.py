import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from zubieta_named_followup import compare


class NamedFollowupTest(unittest.TestCase):
    def test_mismatch_and_reused_id_stay_outside_confirmed_transitions(self):
        def record(uid, birth, saved, native):
            return {"uid": uid, "birth": birth, "saved_factor": saved, "native_factor": native,
                    "ca": 60, "pa": 120, "native_recalculation_score": 8}

        first = [record(i, "2000-01-01", 0, 0) for i in (1, 2, 3, 4)]
        last = [record(1, "2000-01-01", 4, 4), record(2, "2000-01-01", 3, 0),
                record(3, "2001-01-01", 2, 2)]
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / n for n in ("first.json", "last.json")]
            for path, rows, day in zip(paths, (first, last), ("2027-03-31", "2027-04-07"), strict=True):
                path.write_text(json.dumps({"rows": rows, "game_date": day,
                                            "save_sha256": "fixture", "private_receipt_sha256": "fixture"}))
            result = compare(*paths)
        self.assertEqual(result["paired_uid_dob"], 2)
        self.assertEqual(result["missing_followup"], 2)
        self.assertEqual(result["unresolved_pair_count"], 1)
        self.assertEqual(result["changed_native_and_saved_factor"], 1)
        self.assertEqual(result["factor_pairs"], [{"start": 0, "end": 4, "n": 1}])

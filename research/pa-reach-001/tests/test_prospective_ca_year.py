import json
from pathlib import Path
import sqlite3
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from prospective_ca_year import BASE_DAYS, BRANCH, BUILD, FORECAST_DAYS, TARGET, score, sha


class AnnualScoreTests(unittest.TestCase):
    def setUp(self):
        scratch = TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        self.forecasts, self.receipt = root / "forecasts.jsonl", root / "receipt.json"
        entries = [(1, "2009-01-01", "18–20", "1–2", 3, BASE_DAYS),
                   (2, "2009-01-01", "18–20", "1–2", 198, 200 * BASE_DAYS),
                   (3, "2010-01-01", "U18", ">30", 100, 100 * BASE_DAYS)]
        self.forecasts.write_text("".join(json.dumps(row) + "\n" for row in entries), encoding="utf-8")
        self.receipt.write_text(json.dumps(dict(target=TARGET, target_branch=BRANCH, engine_build=BUILD,
                                               history_days=BASE_DAYS, forecast_days=FORECAST_DAYS,
                                               forecast_file_sha256=sha(self.forecasts), frozen_total=3,
                                               frozen_counts={"18–20|1–2": 2, "U18|>30": 1})), encoding="utf-8")
        self.db = sqlite3.connect(":memory:")
        self.addCleanup(self.db.close)
        self.save_hash, self.native_hash = "a" * 64, "b" * 64
        self.db.executescript("CREATE TABLE snapshot(career,day,build,save_hash,inventory_hash);"
                              "CREATE TABLE observation(career,day,uid,birth,ca);")
        self.db.execute("INSERT INTO snapshot VALUES (?,?,?,?,?)", (BRANCH, TARGET, BUILD, self.save_hash, self.native_hash))
        self.db.executemany("INSERT INTO observation VALUES (?,?,?,?,?)", [
            (BRANCH, TARGET, 1, "2009-01-01", 1), (BRANCH, TARGET, 2, "2009-01-01", 200),
            (BRANCH, TARGET, 3, "2010-01-02", 100), (BRANCH, "2028-03-29", 3, "2010-01-01", 100)])

    def measure(self):
        return score(self.db, self.forecasts, self.save_hash, self.native_hash, receipt=self.receipt)

    def test_bounds_and_missing_exact_identity_and_date(self):
        groups = self.measure()["groups"]
        self.assertEqual(groups["all"]["carry_forward"], dict(n=2, mae_ca=2, rmse_ca=2, bias_ca=0))
        self.assertEqual(groups["all"]["previous_rate"], dict(n=2, mae_ca=0, rmse_ca=0, bias_ca=0))
        self.assertEqual(groups["all"]["mae_difference_previous_rate_minus_carry_forward"], -2)
        self.assertEqual(groups["U18|>30"]["missing"], 1)
        self.assertIsNone(groups["U18|>30"]["carry_forward"]["mae_ca"])

    def test_rejects_wrong_target_provenance(self):
        for column, bad_value in (("day", "2028-03-29"), ("build", "different"),
                                  ("save_hash", "c" * 64), ("inventory_hash", "d" * 64)):
            with self.subTest(column=column):
                self.db.execute("SAVEPOINT verify")
                self.db.execute(f"UPDATE snapshot SET {column}=?", (bad_value,))
                with self.assertRaisesRegex(ValueError, "exact target checkpoint"):
                    self.measure()
                self.db.execute("ROLLBACK TO verify")
                self.db.execute("RELEASE verify")

    def test_rejects_changed_forecast_file(self):
        with self.forecasts.open("a", encoding="utf-8") as stream:
            stream.write("\n")
        with self.assertRaisesRegex(ValueError, "receipt differs"):
            self.measure()

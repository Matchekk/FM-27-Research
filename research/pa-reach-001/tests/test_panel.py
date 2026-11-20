"""Build-specific interpretation of a previously collected raw observation."""
from pathlib import Path
import sqlite3
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))
from pa_reach_capture import initialize_panel
from pa_reach_factor_check import attach


class PanelTest(unittest.TestCase):
    def test_migration_preserves_raw_rows_and_zero(self):
        with sqlite3.connect(":memory:") as conn:
            initialize_panel(conn)
            conn.executescript("""
                DROP VIEW research_panel;
                DROP TABLE factor_check;
                CREATE VIEW research_panel AS SELECT candidate FROM observation;
                PRAGMA user_version=2;
            """)
            for index, (build, factor) in enumerate([
                ("27.1.0+2505117", 0), ("27.1.0+2505117", 4),
                ("27.1.0+2505117", 9), ("27.0.1+2503222", 4)
            ]):
                career = f"series-{index}"
                conn.execute("INSERT INTO snapshot VALUES(?,?,?,?,?,?,?)",
                             (career, "2027-03-31", build, "a", "b", "0.14.1", "{}"))
                conn.execute("INSERT INTO observation VALUES(?,?,?,?,?,?,?,?,?,?)",
                             (career, "2027-03-31", 1, "2010-01-01", 17, "ST", 80, 140, factor, 1))
            conn.commit()
            initialize_panel(conn)
            initialize_panel(conn)
            self.assertEqual(conn.execute("SELECT count(progression_tier_if_verified) FROM research_panel").fetchone()[0], 0)
            for idx, native in enumerate((0, 4, 2, 4)):
                conn.execute("INSERT INTO factor_check VALUES(?,?,?,?,?,?)",
                             (f"series-{idx}", "2027-03-31", 1, "2010-01-01", native, "test"))
            result = conn.execute("""SELECT candidate_byte,stored_progression_factor,
                                     progression_tier_if_verified FROM research_panel
                                     ORDER BY career_id""").fetchall()
            self.assertEqual(result, [(0, 0, None), (4, 4, 4), (9, None, None), (4, None, None)])

    def test_unrelated_database_refused(self):
        with sqlite3.connect(":memory:") as conn:
            conn.execute("CREATE TABLE history (ca INTEGER)")
            with self.assertRaises(ValueError):
                initialize_panel(conn)
            self.assertEqual(conn.execute("PRAGMA user_version").fetchone()[0], 0)

    def test_named_check_retries_and_conflicting_evidence(self):
        day = "2027-04-07"
        private = {"game_date":day, "save_sha256":"s", "private_receipt_sha256":"r",
                   "rows":[{"uid":7, "birth":"2011-01-01", "ca":80, "pa":140,
                            "saved_factor":3, "native_factor":3}]}
        public = {"game_date":day, "snapshot_sha256":"s", "private_receipt_sha256":"r",
                  "engine_build":"27.1.0+2505117", "native_name":"ProgressionFactor",
                  "game_thread_parked_before_and_after":True, "save_ca_relative_byte_offset":7,
                  "binding_modes":{"shared_two_requests":1}, "requested":1,
                  "identity_and_native_type_confirmed":1, "confusion":[{"save":3,"native":3,"n":1}]}
        with sqlite3.connect(":memory:") as conn:
            initialize_panel(conn)
            conn.execute("INSERT INTO snapshot VALUES(?,?,?,?,?,?,?)",
                         ("series",day,public["engine_build"],"s","i","0.14.1","{}"))
            conn.execute("INSERT INTO observation VALUES(?,?,?,?,?,?,?,?,?,?)",
                         ("series",day,7,"2011-01-01",16,"ST",80,140,3,1))
            conn.commit()
            for _ in range(2):
                self.assertEqual(attach(conn,"series",private,public),{"checked":1,"verified_tier":1})
            private["rows"][0]["native_factor"] = 0
            public["confusion"][0]["native"] = 0
            with self.assertRaisesRegex(ValueError,"different property check"):
                attach(conn,"series",private,public)
            self.assertEqual(conn.execute("SELECT native_factor FROM factor_check").fetchall(), [(3,)])

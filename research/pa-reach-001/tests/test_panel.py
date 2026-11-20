"""Build-specific interpretation of a previously collected raw observation."""
from pathlib import Path
import sqlite3
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))
from pa_reach_capture import initialize_panel


class PanelTest(unittest.TestCase):
    def test_migration_preserves_raw_rows_and_zero(self):
        with sqlite3.connect(":memory:") as conn:
            initialize_panel(conn)
            conn.executescript("""
                DROP VIEW research_panel;
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

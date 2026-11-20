import importlib.util
from pathlib import Path
import sqlite3
import unittest


script = Path(__file__).resolve().parents[1] / "analysis" / "zubieta_exposure_summary.py"
spec = importlib.util.spec_from_file_location("exposure_summary", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class StoredMinuteDifferences(unittest.TestCase):
    def test_unchanged_counter_is_distinct_from_missing_changed_team_and_reset(self):
        with sqlite3.connect(":memory:") as db:
            db.executescript("""
                CREATE TABLE observation(career,day,uid,birth,age,position,ca);
                CREATE TABLE minutes(tag,uid,birth,team,minutes,at_managed_club);
                CREATE TABLE injury(tag,uid,birth,game_day,severity);
            """)
            dates = {"A":"2027-01-31", "B":"2027-03-30"}
            for uid in range(4):
                for tag,day in dates.items():
                    db.execute("INSERT INTO observation VALUES(?,?,?,?,?,?,?)",
                               ("C",day,uid,"2009-01-01",18,"DC",100 + (tag == "B")))
                db.execute("INSERT INTO minutes VALUES('A',?,'2009-01-01',1,90,1)",(uid,))
            for uid,team,total in ((0,1,90),(2,2,180),(3,1,10)):
                db.execute("INSERT INTO minutes VALUES('B',?,'2009-01-01',?,?,1)",(uid,team,total))
            r = module.period(db,db,"C","A","B",dates)
        self.assertEqual(r["stored_minute_increase_groups"]["0"]["n"],1)
        s = r["paired_outfield_selection"]
        self.assertEqual(s["no_accepted_total_at_one_or_both_dates"],1)
        self.assertEqual(s["team_keys_changed"],1)
        self.assertEqual(s["at_least_one_counter_decreased"],1)
        self.assertIsNone(r["injury_days_missed"])


if __name__ == "__main__":
    unittest.main()

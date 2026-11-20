"""Identity matching, club aggregation and multiplicity use small analytical fixtures."""
import sqlite3
import sys
from pathlib import Path
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import growth_associations as ga
import zubieta_associations as za


class GrowthTests(unittest.TestCase):
    def test_zubieta_native_endpoints_must_match_dates_hashes_and_abilities(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript("""
          ATTACH DATABASE ':memory:' AS ref;
          CREATE TABLE capture(tag,game_date,build,sha256);
          CREATE TABLE player(tag,uid,birth,name_check,age,ca,pa,pos,club);
          CREATE TABLE ref.snapshot(career,day,build,save_hash);
          CREATE TABLE ref.observation(career,day,uid,birth,ca,pa,club);
        """)
        for i,(tag,day) in enumerate((za.FIRST,za.LAST)):
            conn.execute("INSERT INTO capture VALUES(?,?,?,?)",(tag,day,za.BUILD,str(i)))
            conn.execute("INSERT INTO ref.snapshot VALUES(?,?,?,?)",("root",day,za.BUILD,str(i)))
            for uid in (1,2,3):
                name = "same" if uid != 3 or i==0 else "changed"
                conn.execute("INSERT INTO player VALUES(?,?,?,?,?,?,?,?,?)",
                             (tag,uid,"birth",name,19,100+i,160,"MC",3))
                ca = 50 if uid==2 and i==0 else 100+i
                conn.execute("INSERT INTO ref.observation VALUES(?,?,?,?,?,?,?)",
                             ("root",day,uid,"birth",ca,160,3))
        self.assertEqual([(19,60,100,160,1,"MC",3)],za.read_native_pairs(conn))
        conn.execute("UPDATE ref.snapshot SET save_hash='other' WHERE day=?", (za.LAST[1],))
        with self.assertRaisesRegex(ValueError,"native reference"):
            za.read_native_pairs(conn)
        conn.close()

    def test_pair_requires_birth_root_and_endpoint(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript("""
          CREATE TABLE snapshot(career,day,build);
          INSERT INTO snapshot VALUES('a','2027-01-01','v'),('a','2027-01-20','v');
          CREATE TABLE observation(career,uid,birth,day,age,position,ca,pa,candidate,club);
        """)
        def row(career, uid, birth, day, ca, pos="MC", age=18):
            return career,uid,birth,day,age,pos,ca,120,3,10
        a, b = "2027-01-01", "2027-01-20"
        conn.executemany("INSERT INTO observation VALUES (?,?,?,?,?,?,?,?,?,?)", [
            row("a",1,"d",a,100), row("a",1,"d",b,102),
            row("a",2,"e",a,90), row("a",2,"f",b,140),
            row("a",3,"g",a,110), row("other",3,"g",b,120),
            row("a",4,"h",a,80,"GK"), row("a",4,"h",b,82,"GK"),
            row("a",5,"i",a,75,age=28), row("a",5,"i",b,77,age=28),
        ])
        plan = dict(career="a",build="v",start=a,end=b)
        v,_,_ = ga.read_pairs(conn,plan)
        np.testing.assert_array_equal(v["delta"], [2])
        conn.execute("UPDATE snapshot SET build='other' WHERE day=?", (b,))
        with self.assertRaisesRegex(ValueError, "build"):
            ga.read_pairs(conn,plan)
        conn.close()

    def test_weighted_ranks_and_degenerate_resamples(self):
        x=np.array([1.,1.,2.,3.])
        y=np.array([0.,1.,1.,1.])
        # Identical empirical table in each club makes bootstrap limits analytical.
        clubs=np.repeat([10,11,12],len(x))
        out=ga.club_bootstrap(np.tile(x,3),np.tile(y,3),clubs,draws=30)
        for metric in ("pearson","spearman"):
            np.testing.assert_allclose(out[metric+"_95ci"],[ga.correlations(x,y)[metric]]*2)
        singular=ga.club_bootstrap(np.ones(12),np.tile(y,3),clubs,draws=15)
        self.assertIsNone(singular["spearman_95ci"])
        self.assertEqual(singular["defined_draws"],0)

    def test_holm_includes_all_terms_and_preserves_order(self):
        np.testing.assert_allclose(ga.holm([0.04,0.002,0.03]),[0.06,0.006,0.06])


if __name__ == "__main__":
    unittest.main()

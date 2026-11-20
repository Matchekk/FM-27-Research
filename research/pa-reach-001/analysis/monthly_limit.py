"""Observe above-cap CA gains during the prospective month. No breakthrough labels."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3

from zubieta_readback import digest, iso_birth, quoted_database


MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"
CAP = {1: 70, 2: 75, 3: 85, 4: 95}


def summarize(native, panel, scan):
    plan = json.loads((MANIFESTS / "zubieta-control-native-input.json").read_bytes())
    captures = json.loads((MANIFESTS / "observed-meta.json").read_bytes())["snapshots"]
    start, end = "2027-03-30", "2027-04-30"
    if digest(scan) != captures[start]["hashes"]["dump"]:
        raise ValueError("Wrong bracketed baseline scan")
    with sqlite3.connect(quoted_database(native), uri=True) as db:
        db.execute("ATTACH DATABASE ? AS structural", (quoted_database(panel),))
        for d in (start, end):
            row = db.execute("SELECT save_hash,build FROM snapshot WHERE day=? AND career=?",
                             (d, plan["career_id"])).fetchone()
            if row != (plan["snapshots"][d]["save_sha256"], plan["engine_build"]):
                raise ValueError("Unexpected control snapshot")
        rows = {r[0]:r[1:] for r in db.execute("""
            SELECT a.uid,a.birth,a.ca,a.pa,a.candidate,s.professionalism,b.ca-a.ca
            FROM observation a JOIN observation b USING(career,uid,birth)
            JOIN structural.player s ON s.uid=a.uid AND s.birth=a.birth AND s.ca=a.ca AND s.pa=a.pa
            JOIN structural.capture c ON c.tag=s.tag
            WHERE c.sha256=? AND a.career=? AND a.day=? AND b.day=?
              AND a.age<28 AND a.position<>'GK' AND a.pa=b.pa
              AND a.candidate BETWEEN 1 AND 4 AND a.candidate=b.candidate
        """, (plan["snapshots"][start]["save_sha256"], plan["career_id"], start, end))}
    players = json.loads(scan.read_bytes().decode("utf-8-sig"))["players"]
    ids = Counter(p["id"] for p in players)
    cells = defaultdict(Counter)
    n = 0
    for p in players:
        uid = p["id"]
        if uid not in rows or ids[uid] != 1:
            continue
        birth, ca, pa, byte, pro, gain = rows[uid]
        if (iso_birth(p), p["ca"], p["pa"], p.get("professionalism")) != (birth, ca, pa, pro):
            continue
        if not 1 <= pro <= 20:
            continue
        n += 1
        if 100 * ca <= CAP[byte] * pa + 200:
            continue
        groups = ["all"]
        if pa >= 180 and pro >= 15:
            groups.append("pa_ge180_pro_ge15")
        if pa in (124,125,179,180):
            groups.append(f"pa_{pa}")
        if pro in (14,15):
            groups.append(f"pro_{pro}")
        for group in groups:
            cells[group]["players"] += 1
            cells[group]["observed_net_ca_gain"] += int(gain > 0)
            cells[group]["sum_net_ca_change"] += gain
    return dict(days=31, eligible_before_scout=len(rows), verified_professionalism=n,
                over_cap_by_more_than_two_points=cells, training_facilities=None,
                in_engine_temporary_ceiling=None, monthly_breakthrough_probability=None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("native","panel","scan"):
        parser.add_argument(arg, type=Path)
    print(json.dumps(summarize(**vars(parser.parse_args())), indent=2))

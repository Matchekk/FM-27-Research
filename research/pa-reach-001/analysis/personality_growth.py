"""58-day Zubieta associations, with independently read baseline personality and attributes."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3

import numpy as np

from growth_associations import adjusted, correlations
from zubieta_readback import digest, iso_birth, quoted_database


PLAN = Path(__file__).resolve().parents[1] / "manifests/personality-plan.json"
FIELDS = ("professionalism", "ambition", "determination", "natural_fitness", "injury_proneness")


def checked_context(path):
    result = json.loads(path.read_bytes().decode("utf-8-sig"))
    state = result["Response"]
    if result["Status"] != "completed" or any(str(state[key]).lower() != "false"
            for key in ("Processing", "Saving", "IsDuringMatch")):
        raise ValueError("The scanner did not bracket an idle career state")
    return result["Pid"], state["LastSavePath"], state["Date"]


def analyze(panel, native, scan, before, after):
    plan = json.loads(PLAN.read_bytes())
    context = checked_context(before)
    if context != checked_context(after) or context[2] != plan["baseline"]:
        raise ValueError("Wrong source date, process or career path")
    with sqlite3.connect(quoted_database(panel), uri=True) as db:
        db.execute("ATTACH DATABASE ? AS ref", (quoted_database(native),))
        for tag, day in (("ZD-HIST-02", plan["baseline"]), ("ZD-ROOT-01", plan["outcome_date"])):
            source = db.execute("""SELECT c.sha256 FROM capture c JOIN ref.snapshot s
                ON c.sha256=s.save_hash AND c.build=s.build AND c.game_date=s.day
                WHERE c.tag=? AND c.game_date=? AND c.build=? AND s.career=?""",
                (tag, day, plan["build"], plan["career"])).fetchall()
            if len(source) != 1 or (day == plan["baseline"] and digest(Path(context[1])) != source[0][0]):
                raise ValueError("Native series and save are not bound to this analysis")
        pairs = {r[0]: r[1:] for r in db.execute("""
            SELECT a.uid,a.birth,a.ca,a.pa,a.professionalism,a.ambition,a.determination,
                   a.natural_fitness,a.injury_proneness,a.age,a.pos,m.club,a.candidate,b.ca-a.ca
            FROM player a JOIN player b USING(uid,birth,name_check)
            JOIN ref.observation m ON a.uid=m.uid AND a.birth=m.birth AND a.ca=m.ca AND a.pa=m.pa
            JOIN ref.observation n ON b.uid=n.uid AND b.birth=n.birth AND b.ca=n.ca AND b.pa=n.pa
            WHERE a.tag='ZD-HIST-02' AND b.tag='ZD-ROOT-01' AND m.day=? AND n.day=?
              AND a.age<28 AND a.pos<>'GK' AND m.career=? AND n.career=m.career
        """, (plan["baseline"], plan["outcome_date"], plan["career"]))}
    scout = json.loads(scan.read_bytes().decode("utf-8-sig"))
    if scout["meta"]["game"] != "FM27":
        raise ValueError("Expected FM27 scan")
    players = scout.pop("players")
    counts = Counter(eligible_native_pairs=len(pairs))
    ids = Counter(p["id"] for p in players)
    observations = []
    for player in players:
        uid = player["id"]
        if uid not in pairs or ids[uid] != 1:
            continue
        row = pairs[uid]
        if (iso_birth(player), player["ca"], player["pa"]) != row[:3]:
            counts["baseline_identity_or_ability_mismatch"] += 1
            continue
        values = (player.get("professionalism"), player.get("ambition"),
                  *(player["attrs"].get(key) for key in ("Determination", "NaturalFitness", "InjuryProneness")))
        if any(type(x) is not int or not 1 <= x <= 20 for x in values) or values != row[3:8]:
            counts["missing_out_of_range_or_different_attribute"] += 1
            continue
        ca, pa = row[1:3]
        age, pos, club, candidate, delta = row[8:]
        observations.append((age, pa-ca, ca, candidate, delta, *values, pos, club))
    counts["no_unique_scan_id"] = sum(ids[u] != 1 for u in pairs)
    counts["retained"] = len(observations)
    if not observations or sum(v for k,v in counts.items() if k != "eligible_native_pairs") != len(pairs):
        raise ValueError("Incomplete or empty source accounting")
    columns = list(zip(*observations, strict=True))
    names = ("age", "gap", "ca", "candidate", "delta", *FIELDS)
    v = {key: np.asarray(col, dtype=float) for key, col in zip(names, columns[:-2], strict=True)}
    pos, clubs = np.asarray(columns[-2]), np.asarray(columns[-1])
    known = np.array([club is not None for club in clubs])
    fits = {}
    for name, mask, tiers in (("all", np.ones(len(pos), dtype=bool), False),
                              ("club_subset", known, False),
                              ("candidate_sensitivity", np.isin(v["candidate"], [1,2,3,4,5]), True)):
        subset = {k:x[mask] for k,x in v.items()}
        extra = {k:subset[k]-10 for k in FIELDS}
        extra["age_x_professionalism"] = (subset["age"]-20)*extra["professionalism"]
        fits[name] = adjusted(subset, pos[mask], clubs[mask] if name == "club_subset" else None,
                              include_candidate=tiers, extra_columns=extra)
    return {"plan": PLAN.name, "counts": counts, "scan_sha256": digest(scan),
            "before_sha256": digest(before), "after_sha256": digest(after),
            "scanner_claimed_game_date": scout["meta"].get("gameDate"),
            "native_baseline_day": plan["baseline"], "outcome_day": plan["outcome_date"],
            "correlations": {k:correlations(v[k], v["delta"]) for k in FIELDS},
            "adjusted_models": fits, "independent_holdout": False, "causal_effect": None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for label in ("panel", "native", "scan", "before", "after"):
        parser.add_argument(label, type=Path)
    print(json.dumps(analyze(**vars(parser.parse_args())), indent=2, allow_nan=False))

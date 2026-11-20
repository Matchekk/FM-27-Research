"""Describe a frozen three-date cohort and its subsequent observed CA on the retention branch."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3

from zubieta_readback import digest, iso_birth, quoted_database
from zubieta_exposure_summary import minute_group


JAN, MAR, APR = "2027-01-31", "2027-03-30", "2027-04-30"
CAP = {1:70, 2:75, 3:85, 4:95, 5:100}
ROOT = Path(__file__).resolve().parents[1] / "manifests"


def course(start, middle, end):
    if max(start, middle, end) - min(start, middle, end) <= 1:
        return "stagnant_observed_range_le1"
    if end - start >= 2:
        return "net_gain_ge2"
    if start - end >= 2:
        return "net_decline_ge2"
    return "fluctuating_net_within_one"


def measured_context(c, source, structural, exposures, scout):
    """Measure January personality and Jan–March exposure only for the selected cohort."""
    snapshots = source["snapshots"]
    evidence = json.loads((ROOT / "observed-meta.json").read_bytes())["snapshots"][JAN]
    if digest(scout) != evidence["hashes"]["dump"]:
        raise ValueError("January scanner checksum differs")
    c.execute("ATTACH ? AS profile", (quoted_database(structural),))
    c.execute("ATTACH ? AS exp", (quoted_database(exposures),))
    for tag, day in (("JAN",JAN), ("MAR",MAR)):
        if c.execute("SELECT day,sha256 FROM exp.exposure_snapshot WHERE tag=?", (tag,)).fetchone() != (
                day,snapshots[day]["save_sha256"]):
            raise ValueError("Exposure source differs")
    population = c.execute("""
        SELECT a.uid,a.birth,a.ca,a.pa,p.professionalism FROM main.observation a
        JOIN profile.player p ON a.uid=p.uid AND a.birth=p.birth AND a.ca=p.ca AND a.pa=p.pa
        JOIN profile.capture h USING(tag) WHERE a.day=? AND a.career=? AND h.sha256=?
        AND a.age<28 AND a.position<>'GK' AND a.pa>=150 AND a.pa-a.ca>=20
        """,(JAN,source["career_id"],snapshots[JAN]["save_sha256"]))
    baseline = {uid:(birth,ca,pa,pro) for uid,birth,ca,pa,pro in population}
    scans = [p for p in json.loads(scout.read_bytes().decode("utf-8-sig"))["players"] if p["id"] in baseline]
    multiplicity = Counter(p["id"] for p in scans)
    pros = {}
    for p in scans:
        k = p["id"]
        pro = p.get("professionalism")
        if (multiplicity[k] == 1 and type(pro) is int and 1 <= pro <= 20
                and (iso_birth(p),p["ca"],p["pa"],pro)==baseline[k]):
            pros[k,iso_birth(p)] = "1-10" if pro<=10 else "11-14" if pro<=14 else "15-20"
    injuries = set(c.execute("SELECT uid,birth FROM exp.injury WHERE tag='MAR' AND game_day>? AND game_day<=?",
                             (JAN,MAR)))
    def labels(uid,birth):
        team_counts = []
        for tag in ("JAN","MAR"):
            team_counts.append(dict(c.execute(
                "SELECT team,minutes FROM exp.minutes WHERE tag=? AND uid=? AND birth=?", (tag,uid,birth))))
        a,b = team_counts
        minutes = "missing_or_changed_team_counters"
        if a and a.keys()==b.keys() and all(b[k]>=v for k,v in a.items()):
            minutes = minute_group(sum(b[k]-v for k,v in a.items()))
        event = "dated_event" if (uid,birth) in injuries else "no_documented_event"
        return ("jan_professionalism/"+pros.get((uid,birth),"missing"),
                "jan_mar_minutes/"+minutes, "jan_mar_injury_history/"+event)
    return labels


def read_cohort(history, retention, last_day=None, structural=None, exposures=None, scout=None):
    plans = [json.loads((ROOT / filename).read_bytes()) for filename in
             ("zubieta-native-input.json", "zubieta-retention-native-input-0430.json")]
    with sqlite3.connect(quoted_database(history), uri=True) as c:
        c.execute("ATTACH ? AS ret", (quoted_database(retention),))
        for schema, plan in zip(("main","ret"), plans, strict=True):
            for d, expected in plan["snapshots"].items():
                row = c.execute(f"SELECT save_hash,inventory_hash,build FROM {schema}.snapshot "
                                "WHERE career=? AND day=?", (plan["career_id"],d)).fetchone()
                if row != (expected["save_sha256"],expected["native_sha256"],plan["engine_build"]):
                    raise ValueError("Source differs from dated input manifest")
        root, branch = [p["career_id"] for p in plans]
        covariates = None
        if any(p is not None for p in (structural,exposures,scout)):
            if None in (structural,exposures,scout):
                raise ValueError("All three verified contextual sources are required")
            covariates = measured_context(c,plans[0],structural,exposures,scout)
        if plans[0]["snapshots"][MAR] != plans[1]["snapshots"][MAR]:
            raise ValueError("March source is not shared")
        follow_hash = None
        if last_day:
            follow_hash = c.execute("SELECT save_hash,inventory_hash,build FROM ret.snapshot WHERE career=? AND day=?",
                                    (branch,last_day)).fetchone()
            if last_day <= APR or not follow_hash or follow_hash[2] != plans[1]["engine_build"]:
                raise ValueError("Require a later captured retention checkpoint on this build")
        rows = c.execute("""
            SELECT a.uid,a.birth,a.age,a.ca,a.pa,a.candidate,m.ca,m.pa,e.ca,e.pa,z.ca,z.pa
            FROM main.observation a
            LEFT JOIN main.observation m ON m.uid=a.uid AND m.birth=a.birth AND m.career=a.career AND m.day=?
            LEFT JOIN ret.observation e ON e.uid=a.uid AND e.birth=a.birth AND e.career=? AND e.day=?
            LEFT JOIN ret.observation z ON z.uid=a.uid AND z.birth=a.birth AND z.career=? AND z.day=?
            WHERE a.career=? AND a.day=? AND a.age<28 AND a.position<>'GK' AND a.pa>=150 AND a.pa-a.ca>=20
        """, (MAR,branch,APR,branch,last_day,root,JAN))
        total, strata, outcomes = Counter(), defaultdict(Counter), defaultdict(Counter)
        for uid, birth, age, start, pa, factor, mid, p_mid, end, p_end, follow, follow_pa in rows:
            total["baseline"] += 1
            if mid is None or end is None:
                total["missing_march_or_april"] += 1
                continue
            label = course(start,mid,end)
            total["complete"] += 1
            if pa != p_mid or pa != p_end:
                total["any_pa_change_at_classification"] += 1
            band = "<18" if age<18 else "18-20" if age<=20 else "21-23" if age<=23 else "24-27"
            room = None if factor not in CAP else CAP[factor]*pa - 100*start
            room_group = ("unresolved" if room is None else "above_by_more_than_two" if room < -200
                          else "within_two" if room <= 200 else "up_to_ten_below" if room <= 1000 else "over_ten_below")
            for dimension in ("all", "age/"+band, "stored_factor/"+str(factor), "cap_room/"+room_group,
                              "age_cap_room/"+band+"/"+room_group, *(covariates(uid,birth) if covariates else ())):
                strata[dimension][label] += 1
            if last_day:
                cell = outcomes[label]
                cell["classified"] += 1
                if follow is None:
                    cell["followup_missing"] += 1
                else:
                    cell["followup_measured"] += 1
                    cell["sum_delta_ca"] += follow - end
                    cell["gained_at_least_three"] += follow - end >= 3
                    cell["pa_differs_from_january"] += follow_pa != pa
    return {"schema":"pa-reach-stagnation/v1", "dates":[JAN,MAR,APR], "later_date":last_day,
            "later_save_and_native_sha256":list(follow_hash[:2]) if follow_hash else None,
            "career_roots":1, "accounting":total, "baseline_strata":dict(sorted(strata.items())),
            "later_ca_by_april_classification":dict(outcomes) if last_day else None}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history",type=Path)
    parser.add_argument("retention",type=Path)
    parser.add_argument("--last-day")
    for arg in ("structural","exposures","scout"):
        parser.add_argument("--"+arg,type=Path)
    print(json.dumps(read_cohort(**vars(parser.parse_args())),indent=2,sort_keys=True))

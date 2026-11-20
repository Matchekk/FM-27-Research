"""Aggregate one private capture series. Output contains no individual records."""
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sqlite3
from statistics import mean, median


CAP = {1: 70, 2: 75, 3: 85, 4: 95, 5: 100}


def age_band(age):
    if age < 18:
        return "<18"
    if age < 21:
        return "18-20"
    if age < 24:
        return "21-23"
    return "24-27"


def gap_band(gap):
    if gap < 0:
        return "<0"
    if gap == 0:
        return "0"
    if gap <= 10:
        return "1-10"
    return "11-30" if gap <= 30 else ">30"


def growth(values):
    return dict(n=len(values), sum_delta=sum(values), mean_delta=round(mean(values), 4),
                median_delta=median(values), min_delta=min(values), max_delta=max(values),
                gains=sum(v > 0 for v in values), losses=sum(v < 0 for v in values))


def summarize(conn, career):
    snapshots = list(conn.execute("SELECT day, build, accounting FROM snapshot WHERE career=? ORDER BY day", (career,)))
    if len(snapshots) < 2 or len({s[1] for s in snapshots}) != 1:
        raise ValueError("At least two dates of one build required")
    first, last = snapshots[0][0], snapshots[-1][0]
    histories = defaultdict(list)
    daily = defaultdict(Counter)
    for uid, birth, day, age, pos, ca, pa, tier in conn.execute(
        "SELECT uid,birth,day,age,position,ca,pa,candidate FROM observation WHERE career=? ORDER BY day",
        (career,),
    ):
        histories[(uid, birth)].append((day, age, pos, ca, pa, tier))
        daily[day][tier] += 1
    links, matrix, cap_groups, new_bytes = Counter(), Counter(), defaultdict(list), Counter()
    ratio, endpoint, strata = defaultdict(list), defaultdict(Counter), defaultdict(list)
    new_youth = Counter()
    for (_, birth), history in histories.items():
        start, end = history[0], history[-1]
        _, age, pos, ca, pa, t = start
        if start[0] != first:
            links["first_seen_after_baseline"] += 1
            new_bytes[t] += 1
            if age < 18:
                new_youth["first_seen_under18"] += 1
                if t == 0:
                    new_youth["initially_zero"] += 1
                    if any(r[5] in CAP for r in history[1:]):
                        new_youth["zero_then_1_to_5"] += 1
            continue
        links["baseline"] += 1
        ratio[t].append(ca / pa)
        if any(row[4] != pa for row in history[1:]):
            links["observed_pa_change_from_baseline"] += 1
        eligible = pos is not None and pos != "GK" and age < 28
        if eligible:
            # SQLite stores ISO dates. Feb 29 remains valid after 28 years for this cohort.
            dob = date.fromisoformat(birth)
            try:
                birthday = dob.replace(year=dob.year + 28).isoformat()
            except ValueError:
                birthday = dob.replace(year=dob.year + 28, day=28).isoformat()
            before = [row for row in history if row[0] <= birthday]
            observed_peak = max(row[3] for row in before)
            for name, threshold in (("full", pa), ("pa95", (95 * pa + 99) // 100), ("pa_minus_2", pa - 2)):
                if ca >= threshold:
                    status = "already_at_baseline"
                elif observed_peak >= threshold:
                    status = "newly_observed_hit"
                elif end[0] < birthday:
                    status = "right_censored"
                else:
                    status = "horizon_passed_without_observed_hit_sparse_sampling"
                endpoint[name][status] += 1
        if end[0] != last:
            links["baseline_absent_on_final_date"] += 1
            continue
        links["paired"] += 1
        matrix[f"{t}->{end[5]}"] += 1
        if len(history) == len(snapshots):
            links["present_all_dates"] += 1
        if t in CAP and end[5] in CAP and end[5] < t and 100 * end[3] > CAP[end[5]] * end[4]:
            links["lower_candidate_final_ca_above_new_cap"] += 1
        if eligible:
            strata[(age_band(age), gap_band(pa - ca))].append(end[3] - ca)
        if eligible and t in CAP and all(row[4:] == (pa, t) for row in history):
            room = pa * CAP[t] - 100 * ca
            group = ">10 below" if room > 1000 else ("within 2" if abs(room) <= 200 else
                    ("above by >2" if room < 0 else "2 to 10 below"))
            cap_groups[group].append(end[3] - ca)
    club_intervals = []
    for (left, _, _), (right, _, _) in zip(snapshots, snapshots[1:]):
        for status, n, changed in conn.execute("""
            SELECT CASE WHEN a.club IS NULL OR b.club IS NULL THEN 'unknown'
                        WHEN a.club=b.club THEN 'same' ELSE 'different' END AS status,
                   count(*),sum(a.candidate<>b.candidate) FROM observation a
            JOIN observation b USING(career,uid,birth)
            WHERE a.career=? AND a.day=? AND b.day=?
              AND a.candidate BETWEEN 1 AND 5 AND b.candidate BETWEEN 1 AND 5
            GROUP BY status ORDER BY status
        """, (career, left, right)):
            club_intervals.append(dict(start=left,end=right,club=status,intervals=n,changed=changed))
    return {
        "career_cluster_count": 1, "build": snapshots[0][1],
        "days_between_endpoints": (date.fromisoformat(last) - date.fromisoformat(first)).days,
        "snapshots": {d: json.loads(a) for d, _, a in snapshots},
        "byte_counts": daily, "linkage": links, "first_seen_after_baseline_byte_counts": new_bytes,
        "first_last_candidate_transitions": matrix,
        "new_youth_diagnostics": new_youth, "club_and_candidate_intervals": club_intervals,
        "baseline_median_ca_over_pa": {t: round(median(v), 4) for t, v in ratio.items()},
        "baseline_outfield_under28_endpoint_counts": endpoint,
        "outfield_under28_growth_by_baseline_age_gap": [
            dict(age=a, gap=g, **growth(v)) for (a, g), v in sorted(strata.items())
        ],
        "outfield_under28_growth_by_candidate_cap_room": {g: growth(v) for g, v in cap_groups.items()},
        "independent_test_careers": 0, "calibration_metrics": None,
        "status": ["INSUFFICIENT_LONGITUDINAL_EVIDENCE",
                   "PROGRESSION_FACTOR_FIELD_VALIDATED" if snapshots[0][1] == "27.1.0+2505117"
                   else "PROGRESSION_TIER_UNVERIFIED", "NOT_OUTCOME_VALIDATED"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_database", type=Path)
    parser.add_argument("career")
    args = parser.parse_args()
    with sqlite3.connect(args.private_database.resolve().as_uri() + "?mode=ro", uri=True) as conn:
        print(json.dumps(summarize(conn, args.career), indent=2, sort_keys=True))

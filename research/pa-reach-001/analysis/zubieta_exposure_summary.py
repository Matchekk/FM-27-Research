"""Aggregate explicitly observed team-minute counters and injury-history dates."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3


def minute_group(delta):
    if delta == 0:
        return "0"
    if delta <= 180:
        return "1_to_180"
    if delta <= 450:
        return "181_to_450"
    return "above_450"


def period(exposure, native, career, start, finish, dates):
    def native_rows(day):
        return {(u,b):(age,pos,ca) for u,b,age,pos,ca in native.execute(
            "SELECT uid,birth,age,position,ca FROM observation WHERE career=? AND day=?",(career,day))}

    def by_player(tag):
        groups = defaultdict(dict)
        for uid,birth,team,value,own in exposure.execute(
            "SELECT uid,birth,team,minutes,at_managed_club FROM minutes WHERE tag=?",(tag,)
        ):
            groups[(uid,birth)][team] = (value,own)
        return groups

    early,late = by_player(start),by_player(finish)
    a,b = native_rows(dates[start]),native_rows(dates[finish])
    groups = defaultdict(lambda: Counter(n=0, minutes_difference_sum=0,delta_ca_sum=0))
    sample = Counter()
    for key in a.keys() & b.keys():
        age,pos,ca = a[key]
        if age >= 28 or not pos or pos == "GK":
            continue
        sample["native_pairs_outfield_under28"] += 1
        left,right = early.get(key),late.get(key)
        if not left or not right:
            sample["no_accepted_total_at_one_or_both_dates"] += 1
            continue
        if left.keys() != right.keys():
            sample["team_keys_changed"] += 1
            continue
        diffs = [right[t][0]-left[t][0] for t in left]
        if min(diffs)<0:
            sample["at_least_one_counter_decreased"] += 1
            continue
        sample["matched_non_decreasing_totals"] += 1
        if all(left[t][1]==right[t][1]==1 for t in left):
            sample["all_rows_managed_club"] += 1
        change = sum(diffs)
        group = groups[minute_group(change)]
        group["n"] += 1
        group["minutes_difference_sum"] += change
        group["delta_ca_sum"] += b[key][2]-ca
    events = list(exposure.execute(
        "SELECT uid,birth,game_day FROM injury WHERE tag=? AND game_day>? AND game_day<=?",
        (finish,dates[start],dates[finish])))
    return {
        "start": dates[start],"finish": dates[finish],"career": career,"paired_outfield_selection":dict(sample),
        "stored_minute_increase_groups":{k:{**v,"mean_delta_ca":round(v["delta_ca_sum"]/v["n"],4)} for k,v in groups.items()},
        "dated_history_rows_inside_interval_endpoint_reader":len(events),
        "distinct_endpoint_people_with_dated_history_inside_interval":len({(u,b) for u,b,_ in events}),
        "distinct_endpoint_person_days_with_dated_history_inside_interval":len(set(events)),
        "injury_days_missed":None,"causal_playing_time_effect":None,
    }


def readonly(path):
    return sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for field in ("exposure","history_native","pilot_native"):
        parser.add_argument(field,type=Path)
    args=parser.parse_args()
    with readonly(args.exposure) as exposure, readonly(args.history_native) as history, readonly(args.pilot_native) as pilot:
        delivered=list(exposure.execute("SELECT tag,day,accounting FROM exposure_snapshot"))
        dates={tag:day for tag,day,_ in delivered}
        output={
            "field_status":"SAVE_READER_EXPLICIT_COUNTS_NOT_INDEPENDENTLY_NATIVE_VERIFIED",
            "snapshots":{day:json.loads(counts) for _,day,counts in delivered},
            "intervals":[period(exposure,history,"ZD-ROOT-01","JAN","MAR",dates),
                         period(exposure,pilot,"ZD-CONTROL-01","MAR","APR",dates)],
        }
        print(json.dumps(output,indent=2,sort_keys=True))

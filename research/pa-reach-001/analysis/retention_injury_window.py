"""Compare recorded new injuries and saved factor directions in a two-day window."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3
import warnings

import fmsave
from fmsave import InjuryRecordKind

from retention_transfer_window import BRANCH, BUILD, CHECKPOINTS, END, START, sha


def save_events(path, day, wanted):
    _, digest, _ = CHECKPOINTS[day]
    if fmsave.__version__ != "0.14.1" or sha(path) != digest:
        raise ValueError("Unexpected source or parser")
    audit, injuries = Counter(), defaultdict(set)
    with warnings.catch_warnings(record=True) as caught, fmsave.open(path, strict=True) as save:
        if (str(save.info.game_date), save.info.build) != (day, BUILD):
            raise ValueError("Unexpected saved date or build")
        roster = {row.uid: (row.unique_id, str(row.birth_date)) for row in save.players()
                  if (row.unique_id, str(row.birth_date)) in wanted and row.club_uid == wanted[row.unique_id, str(row.birth_date)]}
        contracts = {roster[row.player_uid]: (row.club_uid, str(row.start), str(row.end))
                     for row in save.contracts() if row.player_uid in roster and row.start and row.end}
        for row in save.injuries():
            audit["injury_source_" + row.kind.value] += 1
            if row.kind == InjuryRecordKind.HISTORY and row.player_uid in roster and row.date:
                injuries[roster[row.player_uid]].add(str(row.date))
        for entry in caught:
            audit["warning_" + type(entry.message).__name__] += 1
    audit["stable_native_players_bound_in_save"] = len(roster)
    if sha(path) != digest:
        raise ValueError("Source changed during read")
    return contracts, injuries, audit


def measure(panel, start_save, end_save):
    with sqlite3.connect(panel.resolve().as_uri()+"?mode=ro", uri=True) as db:
        for day, (_, save_hash, native_hash) in CHECKPOINTS.items():
            if db.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                          (BRANCH, day)).fetchone() != (BUILD, save_hash, native_hash):
                raise ValueError("Snapshot differs from independently confirmed inventory")
        paired = {(u, b): (club, f0, f1, ca1-ca0, pa1-pa0) for u,b,club,f0,f1,ca0,ca1,pa0,pa1 in db.execute("""
            SELECT a.uid,a.birth,a.club,a.candidate,b.candidate,a.ca,b.ca,a.pa,b.pa
            FROM observation a JOIN observation b USING(career,uid,birth)
            WHERE a.career=? AND a.day=? AND b.day=? AND a.club=b.club AND a.club>0
              AND a.candidate BETWEEN 0 AND 5 AND b.candidate BETWEEN 0 AND 5
        """, (BRANCH, START, END))}
    wanted = {key: values[0] for key, values in paired.items()}
    contract_start, injury_start, audit_start = save_events(start_save, START, wanted)
    contract_end, injury_end, audit_end = save_events(end_save, END, wanted)
    counts, event_dates = Counter(), Counter()
    groups = {label: Counter(factor_up=0, factor_down=0, factor_equal=0, ca_changed=0, pa_changed=0)
              for label in ("new_dated_injury_history", "no_recorded_new_injury_history")}
    for key, (club, f0, f1, ca_delta, pa_delta) in paired.items():
        new = {d for d in injury_end.get(key, set()) - injury_start.get(key, set()) if START < d <= END}
        active = contract_start.get(key)
        if not active or active != contract_end.get(key) or active[0] != club or not active[1] <= START < END <= active[2]:
            counts["contract_not_confirmed_stable_and_active"] += 1
            counts["new_injury_among_contract_exclusions"] += bool(new)
            continue
        label = "new_dated_injury_history" if new else "no_recorded_new_injury_history"
        counts[label] += 1
        groups[label]["factor_up" if f1 > f0 else "factor_down" if f1 < f0 else "factor_equal"] += 1
        groups[label]["ca_changed"] += ca_delta != 0
        groups[label]["pa_changed"] += pa_delta != 0
        event_dates.update(new)
    return {"schema": "pa-reach-retention-injury-window/v1", "build": BUILD, "branch": BRANCH,
            "snapshots": {day: {"save_sha256": h, "native_sha256": n} for day, (_, h, n) in CHECKPOINTS.items()},
            "independent_careers": 1, "stable_verified_club_pairs": len(paired), "capture": {START:audit_start, END:audit_end},
            "counts": counts, "factor_ca_pa": groups, "new_dated_history_by_day": event_dates,
            "severity_or_time_lost_measured": False, "factor_field": "saved_CA_plus_7"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for operand in ("panel", "start_save", "end_save"):
        parser.add_argument(operand, type=Path)
    print(json.dumps(measure(**vars(parser.parse_args())), indent=2, sort_keys=True))

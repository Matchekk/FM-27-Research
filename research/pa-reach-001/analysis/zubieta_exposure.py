"""Read stored season minute totals and dated injury history. Private SQLite output."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3
import warnings

import fmsave
from fmsave import InjuryRecordKind, SeasonStatsKind

from zubieta_readback import digest, quoted_database


SCHEMA = """
CREATE TABLE IF NOT EXISTS exposure_snapshot(tag TEXT PRIMARY KEY,day TEXT,sha256 TEXT,accounting TEXT);
CREATE TABLE IF NOT EXISTS minutes(tag TEXT,uid INTEGER,birth TEXT,team INTEGER,club INTEGER,
 minutes INTEGER,starts INTEGER,subs INTEGER,at_managed_club INTEGER,PRIMARY KEY(tag,uid,team));
CREATE TABLE IF NOT EXISTS injury(tag TEXT,uid INTEGER,birth TEXT,game_day TEXT,severity INTEGER);
"""


def capture(path, cohort, career, tag, expected_sha, conn):
    if fmsave.__version__ != "0.14.1" or digest(path) != expected_sha:
        raise ValueError("Unbound save")
    counts = Counter()
    with warnings.catch_warnings(record=True) as caught, fmsave.open(path, strict=True) as save:
        if save.info.build != "27.1.0+2505117":
            raise ValueError("Unsupported build")
        day = str(save.info.game_date)
        with sqlite3.connect(quoted_database(cohort), uri=True) as source:
            sha = source.execute("SELECT save_hash FROM snapshot WHERE career=? AND day=?", (career,day)).fetchone()
            if not sha or sha[0] != expected_sha:
                raise ValueError("Missing native reference")
            verified = dict(source.execute("SELECT uid,birth FROM observation WHERE career=? AND day=?", (career,day)))
        managed, = list(save.managed_clubs())
        ids = {}
        for p in save.players():
            uid = p.unique_id
            if uid in verified and p.birth_date and verified[uid] == p.birth_date.isoformat():
                ids[p.uid] = (uid,verified[uid])
        counts["native_uid_dob_bound"] = len(ids)
        # Only use one OVERALL row per spell's team. Calendar-year, league and cup
        # totals overlap and must not be added to that row.
        stats = save.player_season_stats()
        counts["all_stat_rows"] = len(stats)
        overall = [row for row in stats if row.kind == SeasonStatsKind.OVERALL]
        components = defaultdict(list)
        for row in stats:
            if row.kind in (SeasonStatsKind.LEAGUE, SeasonStatsKind.CUP, SeasonStatsKind.CONTINENTAL):
                components[(row.player_uid,row.team_id)].append(row)
        multiplicity = Counter((row.player_uid,row.team_id) for row in overall)
        counts["overall_team_rows"] = len(overall)
        for row in overall:
            if row.player_uid not in ids:
                counts["stat_outside_bound_population"] += 1
                continue
            if (multiplicity[(row.player_uid,row.team_id)] != 1 or row.team_id is None
                    or min(row.minutes,row.starts,row.substitute_appearances) < 0):
                counts["ambiguous_or_invalid_stat_row"] += 1
                continue
            parts = components[(row.player_uid,row.team_id)]
            if not parts or len({p.kind for p in parts}) != len(parts):
                counts["absent_or_duplicate_component_lines"] += 1
                continue
            if any(sum(getattr(p,k) for p in parts) != getattr(row,k)
                   for k in ("minutes","starts","substitute_appearances")):
                counts["totals_differ_from_recorded_competitions"] += 1
                continue
            uid,birth = ids[row.player_uid]
            conn.execute("INSERT INTO minutes VALUES(?,?,?,?,?,?,?,?,?)",
                         (tag,uid,birth,row.team_id,row.club_uid,row.minutes,row.starts,
                          row.substitute_appearances,row.club_uid == managed.club_uid if row.club_uid is not None else None))
            counts["accepted_overall_team_rows"] += 1
        injuries = save.injuries()
        for event in injuries:
            counts["injury_source_" + event.kind.value] += 1
            if event.kind != InjuryRecordKind.HISTORY:
                continue
            if event.player_uid not in ids or event.date is None or event.date > save.info.game_date:
                counts["history_unbound_undated_or_future"] += 1
                continue
            uid,birth = ids[event.player_uid]
            conn.execute("INSERT INTO injury VALUES(?,?,?,?,?)",
                         (tag,uid,birth,str(event.date),None if event.severity is None else event.severity.raw))
            counts["accepted_dated_history_rows"] += 1
        for w in caught:
            counts["warning_" + type(w.message).__name__] += 1
    if digest(path) != expected_sha:
        raise ValueError("Copy changed")
    conn.execute("INSERT INTO exposure_snapshot VALUES(?,?,?,?)", (tag,day,expected_sha,json.dumps(counts)))
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("private_db","save_copy","native_cohort"):
        parser.add_argument(name, type=Path)
    for name in ("career","tag","sha256"):
        parser.add_argument(name)
    args = parser.parse_args()
    with sqlite3.connect(args.private_db) as conn:
        conn.executescript(SCHEMA)
        conn.execute("BEGIN IMMEDIATE")
        print(json.dumps(capture(args.save_copy,args.native_cohort,args.career,args.tag,args.sha256,conn)))

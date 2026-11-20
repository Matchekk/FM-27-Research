"""Bind scout-announced destinations to observed registration moves around 1 July."""

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sqlite3
from statistics import mean

import fmsave

from observed_meta import bracketed_scan
from prospective_ca61 import BRANCH, BUILD, sha
from zubieta_readback import iso_birth


START, END = "2027-06-30", "2027-07-02"
CHECKPOINTS = {
    START: ("ZD-RET-0630", "040140911df6862dcc21bd20e0ba5b1acfeb616af7a66052bebbcd4ac1932088", "e651e5174995bd95b0e71c708f4595d0163c0bc6fb47e7e4bd149bc8956cba6e"),
    END: ("ZD-RET-0702", "09297f2e9af3573299b1ac8985a9877718796fca0a16426c980ec446490d672e", "b78888aaac0fedcbd83eac9dcc9ab881092262af8aafd73e2a26e1ffae75a5dc"),
}


def normalized(name):
    return " ".join((name or "").casefold().split())


def read_day(db, day, paths):
    tag, expected_save, expected_native = CHECKPOINTS[day]
    if db.execute("SELECT build,save_hash,inventory_hash FROM n.snapshot WHERE career=? AND day=?",
                  (BRANCH, day)).fetchone() != (BUILD, expected_save, expected_native):
        raise ValueError("Unverified independent native panel")
    dump, audit = bracketed_scan(db, day, *paths, tag)
    if audit["hashes"]["loaded_copy"] != expected_save:
        raise ValueError("Unexpected save for the transfer window")
    audit["hashes"]["native_inventory"] = expected_native
    multiplicity = Counter(p["id"] for p in dump["players"])
    indexed = {(p["id"], iso_birth(p)): p for p in dump["players"] if multiplicity[p["id"]] == 1}
    club_name_to_ids, clubs = defaultdict(Counter), {}
    for uid, birth, club, ca, pa, name_check in db.execute("""
        SELECT uid,birth,club,ca,pa,name_check FROM player WHERE tag=? AND club>0
    """, (tag,)):
        p = indexed.get((uid, birth))
        if p and name_check and (ca, pa) == (p["ca"], p["pa"]) and normalized(p.get("club")):
            name = normalized(p["club"])
            club_name_to_ids[name][club] += 1
            clubs[uid,birth] = (club, name, name_check)
    observed = {}
    for uid, birth, ca, pa, factor, age, native_club in db.execute("""
        SELECT p.uid,p.birth,p.ca,p.pa,p.candidate,p.age,o.club FROM player p JOIN n.observation o
          ON p.uid=o.uid AND p.birth=o.birth AND p.ca=o.ca AND p.pa=o.pa AND p.candidate=o.candidate
        WHERE p.tag=? AND o.career=? AND o.day=? AND o.candidate BETWEEN 0 AND 5
    """, (tag, BRANCH, day)):
        k = uid, birth
        if k in clubs:
            club, name, name_check = clubs[k]
            if set(club_name_to_ids[name]) == {club}:
                scan = indexed[k]
                observed[k] = (club, name_check, ca, pa, factor, age, normalized(scan.get("transferTo")),
                               scan.get("transferDate"), scan.get("expires"), name, native_club == club,
                               club_name_to_ids[name][club] >= 2)
    planned = [p for p in dump["players"] if p.get("transferTo") and p.get("transferDate")]
    announced = {(p["id"], iso_birth(p)): (normalized(p["transferTo"]), p["transferDate"])
                 for p in planned if multiplicity[p["id"]] == 1}
    return observed, club_name_to_ids, announced, len(planned), audit


def end_contracts(save_path, wanted):
    if fmsave.__version__ != "0.14.1" or sha(save_path) != CHECKPOINTS[END][1]:
        raise ValueError("Wrong contract-source save or parser")
    with fmsave.open(save_path) as save:
        if save.info.build != BUILD or save.info.game_date.isoformat() != END:
            raise ValueError("Mismatched contract-source checkpoint")
        source = {p.uid: (p.unique_id, p.birth_date.isoformat()) for p in save.players()
                  if p.birth_date and (p.unique_id, p.birth_date.isoformat()) in wanted}
        return {source[c.player_uid]: (c.club_uid, c.start.isoformat() if c.start else None,
                                       c.end.isoformat() if c.end else None)
                for c in save.contracts() if c.player_uid in source}


def summarize(rows):
    n = len(rows)
    return {"n": n, "factor_changed": sum(a[4] != b[4] for a, b in rows),
            "factor_up": sum(a[4] < b[4] for a, b in rows), "factor_down": sum(a[4] > b[4] for a, b in rows),
            "mean_ca_change": mean(b[2]-a[2] for a, b in rows) if n else None,
            "mean_pa_change": mean(b[3]-a[3] for a, b in rows) if n else None,
            "ca_changed": sum(a[2] != b[2] for a, b in rows), "pa_changed": sum(a[3] != b[3] for a, b in rows)}


def measure(db, june, july, save):
    first, first_clubs, plans, count_start, audit_start = read_day(db, START, june)
    last, last_clubs, _, count_end, audit_end = read_day(db, END, july)
    relevant_dates = {START, "2027-07-01", END}
    near = {k: v for k, v in plans.items() if v[1] in relevant_dates}
    coverage = Counter()
    pairs = defaultdict(list)
    matched_keys = set()
    for k, (target, planned_day) in near.items():
        coverage[f"announced_date_{planned_day}"] += 1
        if k not in first or k not in last or first[k][1] != last[k][1]:
            coverage["player_or_club_unverified_either_side"] += 1
            continue
        a, b = first[k], last[k]
        target_ids = set(first_clubs.get(target, ())) | set(last_clubs.get(target, ()))
        if len(target_ids) != 1:
            coverage["unmapped_or_ambiguous_target_club"] += 1
        elif a[0] == b[0]:
            coverage["verified_club_unchanged"] += 1
        elif target_ids != {b[0]}:
            coverage["verified_moved_to_different_club"] += 1
        else:
            coverage["verified_moved_to_announced_club"] += 1
            matched_keys.add(k)
    stable_keys = {k for k, a in first.items() if k in last and a[:2] == last[k][:2]
                   and not any(a[6:8]) and not any(last[k][6:8])}
    contracts = end_contracts(save, matched_keys | stable_keys)
    strict = defaultdict(list)
    for k, a in first.items():
        b = last.get(k)
        if not b or a[1] != b[1]:
            continue
        club, start, end = contracts.get(k, (None, None, None))
        if club == b[0] and start and START < start <= END:
            overlap = "new_observed_club_contract_started_in_window"
        elif club is None or start is None:
            overlap = "contract_owner_or_start_unresolved"
        else:
            overlap = "no_matching_club_contract_start_in_window"
        if k in matched_keys:
            label = "moved_to_announced_club"
            if club == b[0] and start and START < start <= END:
                coverage["in_window_contract_start_and_exact_scan_expiry_match"] += bool(end and end == b[8])
                coverage["in_window_contract_start_matches_announcement_date"] += start == plans[k][1]
        elif k in stable_keys:
            label = "stable_club_no_positive_announcement_either_scan"
            if a[8] and b[8] and a[8] != b[8]:
                pairs[label + "|" + "scout_expiry_changed"].append((a, b))
        else:
            continue
        age = a[5]
        age_band = "U18" if age < 18 else "18–20" if age < 21 else "21–23" if age < 24 else "24–27" if age < 28 else "28+"
        pairs[label].append((a, b))
        pairs[label + "|" + overlap].append((a, b))
        pairs[label + "|age:" + age_band].append((a, b))
        if a[10] and b[10]:
            strict[label + "|independent_club_id_both_days"].append((a, b))
        target_confirmed_by_other = (k not in matched_keys or
                                     last_clubs[plans[k][0]][b[0]] > (plans[k][0] == b[9]))
        if a[11] and b[11] and target_confirmed_by_other:
            strict[label + "|third_party_club_name_both_days"].append((a, b))
    return {"schema": "pa-reach-retention-transfer-window/v1", "build": BUILD, "branch": BRANCH,
            "independent_careers": 1, "snapshots": {START: audit_start, END: audit_end},
            "all_scout_complete_announcement_rows": {START: count_start, END: count_end},
            "near_announcement_unique_players": len(near), "coverage": coverage,
            "groups": {name: summarize(rows) for name, rows in pairs.items()},
            "club_binding_sensitivity": {name: summarize(rows) for name, rows in strict.items()},
            "factor_field": "saved_CA_plus_7_on_identity_and_ability_checked_players; no_named_reads_at_these_dates"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for operand in ("structural_panel", "native_panel", "july_save"):
        parser.add_argument(operand, type=Path)
    for name in ("june", "july"):
        parser.add_argument("--"+name, nargs=3, type=Path, required=True, metavar=("SCAN", "BEFORE", "AFTER"))
    args = parser.parse_args()
    with sqlite3.connect(args.structural_panel.resolve().as_uri()+"?mode=ro", uri=True) as conn:
        conn.execute("ATTACH DATABASE ? AS n", (args.native_panel.resolve().as_uri()+"?mode=ro",))
        print(json.dumps(measure(conn, args.june, args.july, args.july_save), indent=2, sort_keys=True))

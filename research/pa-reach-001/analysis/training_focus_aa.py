"""Compare two save/native/Scout captures for the fixed training A/A cohort. Aggregate stdout only."""
import argparse
from collections import Counter, defaultdict
from contextlib import closing
from datetime import date
import json
from pathlib import Path
import sqlite3
from statistics import mean, median
import sys

import fmsave
from fmsave import SeasonStatsKind
from zubieta_snapshot import SCHEMA, capture_copy, file_hash
from zubieta_readback import iso_birth

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))
from pa_reach_capture import decode


def read(path):
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def validate_package(root, package, day, module_hash):
    paths = {key: root / package[key] for key in ("save", "native", "scout", "before", "after")}
    before, after = read(paths["before"]), read(paths["after"])
    context = before["Response"]
    fields = ("Date", "LastSavePath", "ManagerIdentity", "TeamIdentity")
    if (before["Status"] != "completed" or after["Status"] != "completed" or before["Pid"] != after["Pid"]
            or any(context[f] != after["Response"][f] for f in fields) or context["Date"] != day.isoformat()
            or any(bracket["Response"][field] != "False" for bracket in (before, after)
                   for field in ("Processing", "Saving", "IsDuringMatch"))
            or not Path(context["LastSavePath"]).samefile(paths["save"])):
        raise ValueError("Controller brackets do not bind the expected source")
    for key in ("native", "scout"):
        if not paths["before"].stat().st_mtime <= paths[key].stat().st_mtime <= paths["after"].stat().st_mtime:
            raise ValueError(f"Unbracketed {key} source")
    hashes = {key: file_hash(path) for key, path in paths.items()}
    if hashes["save"] != package["save_sha256"]:
        raise ValueError("Save hash mismatch")
    inventory, scout = read(paths["native"]), read(paths["scout"])
    if (inventory["Pid"] != before["Pid"] or inventory["ReadOnly"] is not True
            or inventory["ModuleSha256"].lower() != module_hash
            or scout["meta"]["game"] != "FM27" or scout["meta"]["versionOk"] is not True):
        raise ValueError("Independent reader provenance mismatch")
    return paths["save"], hashes, inventory["Players"], scout["players"]


def validated_minutes(save, ids):
    stats = defaultdict(list)
    for row in save.player_season_stats():
        if row.player_uid in ids and row.team_id is not None:
            stats[row.player_uid, row.team_id].append(row)
    result = defaultdict(list)
    for (uid, team), rows in stats.items():
        overall = [r for r in rows if r.kind == SeasonStatsKind.OVERALL]
        kinds = (SeasonStatsKind.LEAGUE, SeasonStatsKind.CUP, SeasonStatsKind.CONTINENTAL)
        parts = [r for r in rows if r.kind in kinds]
        if len(overall) != 1 or not parts or len({r.kind for r in parts}) != len(parts):
            continue
        fields = ("minutes", "starts", "substitute_appearances")
        values = tuple(getattr(overall[0], f) for f in fields)
        if min(values) >= 0 and values == tuple(sum(getattr(r, f) for r in parts) for f in fields):
            result[uid].append((team, *values))
    return result


def fixtures(save, first, last):
    managed, = save.managed_clubs()
    found = {}
    try:
        table = save.fixtures()
    except fmsave.ReaderCheckError:
        return None
    for match in table:
        own = ((match.home_club_uid, match.home_team_slot), (match.away_club_uid, match.away_team_slot))
        if not match.date or not first < match.date <= last or (managed.club_uid, 0) not in own or not match.played:
            continue
        key = (match.date, match.kick_off_time, match.stage_id, match.home_team_id, match.away_team_id)
        if key in found or match.home_goals is None or match.away_goals is None:
            return None
        found[key] = (match.home_goals, match.away_goals)
    return found


def collect(root, package, cohort, first, last, build, module_hash):
    source, hashes, native, scanner = validate_package(root, package, last, module_hash)
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.executescript(SCHEMA)
        day, written_build, _ = capture_copy(conn, "AA", source, hashes["save"])
        if (day, written_build) != (last.isoformat(), build):
            raise ValueError("Unexpected save date or build")
        saved = {(uid, birth): (ca, pa, factor, attrs, pers, positions) for uid, birth, ca, pa, factor, attrs, pers, positions
                 in conn.execute("SELECT uid,birth,ca,pa,candidate,raw_attrs,personality,positions FROM player")
                 if (uid, birth) in cohort}

    scanner_ids = Counter(r["id"] for r in scanner)
    independent = {(r["id"], iso_birth(r)): r for r in scanner if scanner_ids[r["id"]] == 1}
    with fmsave.open(source, strict=True) as save:
        checked, _ = decode(save, native)
        abilities = {(uid, birth): (ca, pa) for uid, birth, _, _, ca, pa, _, _ in checked}
        ids = defaultdict(list)
        for p in save.players():
            key = (p.unique_id, p.birth_date.isoformat()) if p.birth_date else None
            if key in cohort:
                ids[key].append(p.uid)
        bound = {key: values[0] for key, values in ids.items() if len(values) == 1}
        margins = validated_minutes(save, set(bound.values()))
        terms = defaultdict(list)
        for c in save.contracts():
            terms[c.player_uid].append(c)
        records = {}
        for key, uid in bound.items():
            source_row = saved.get(key)
            if source_row is None or source_row[:2] != abilities.get(key):
                continue
            record = {"ca": source_row[0], "pa": source_row[1], "factor": source_row[2],
                      "raw_attributes": source_row[3], "personality": source_row[4], "positions": source_row[5],
                      "minutes_starts_subs": tuple(sorted(margins[uid])) if margins[uid] else None,
                      "verified_contract": None}
            scan = independent.get(key)
            if len(terms[uid]) == 1 and scan and (scan["ca"], scan["pa"]) == source_row[:2]:
                c, = terms[uid]
                if c.end and scan.get("expires") == c.end.isoformat() and c.on_loan is not None:
                    record["verified_contract"] = (c.end, str(c.kind), c.on_loan, c.loan_start, c.loan_end)
            records[key] = record
        results = fixtures(save, first, last)
    if file_hash(source) != hashes["save"]:
        raise ValueError("Source changed during readback")
    return records, results, hashes


def compare(cohort, left, right):
    pairs = left.keys() & right.keys()
    fields = sorted(set().union(*(left[k].keys() for k in pairs)))
    audit = {}
    for field in fields:
        known = [k for k in pairs if left[k][field] is not None and right[k][field] is not None]
        audit[field] = {"verified": len(known), "unverified": len(cohort) - len(known),
                        "different": sum(left[k][field] != right[k][field] for k in known)}
    differences = [abs(left[k]["ca"] - right[k]["ca"]) for k in pairs]
    ca_deviation = None
    if differences:
        ca_deviation = {"n": len(differences), "sum_abs_ca_difference": sum(differences),
                        "mean_abs_ca_difference": mean(differences), "median_abs_ca_difference": median(differences),
                        "max_abs_ca_difference": max(differences),
                        "abs_ca_difference_frequency": dict(sorted(Counter(differences).items()))}
    return {"predeclared": len(cohort), "paired": len(pairs), "fields": audit,
            "ca_repeat_deviation": ca_deviation,
            "all_cohort_fields_verified_equal": pairs == cohort and all(
                not v["unverified"] and not v["different"] for v in audit.values())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_cohort", type=Path)
    parser.add_argument("private_packages", type=Path)
    args = parser.parse_args()
    if file_hash(args.private_cohort) != "f9a61087c18840d2d3697f629784a80a65f9080174fadaf86cf0ad11242f4887":
        raise ValueError("Cohort differs from the preregistered April training group")
    roster, plan = read(args.private_cohort), read(args.private_packages)
    selected = [roster["treatment_candidate"], *roster["unchanged_teammates"]]
    cohort = {(p["uid"], p["birth"]) for p in selected}
    if len(cohort) != len(selected) or len(cohort) < 2 or len(plan["packages"]) != 2:
        raise ValueError("Expected unique predeclared players and two packages")
    first, last = map(date.fromisoformat, (roster["save_game_date"], plan["end"]))
    if last <= first or plan["baseline_sha256"] != roster["save_sha256"]:
        raise ValueError("A/A packages do not declare the preselected baseline and a later date")
    packages = plan["packages"]
    root = args.private_packages.parent
    for key in ("save", "native", "scout", "before", "after"):
        if (root / packages[0][key]).samefile(root / packages[1][key]):
            raise ValueError("Two separately acquired A/A packages are required")
    results = [collect(root, p, cohort, first, last, roster["build"],
                       plan["native_module_sha256"]) for p in packages]
    (left, left_fixtures, left_hashes), (right, right_fixtures, right_hashes) = results
    schedule = None if left_fixtures is None or right_fixtures is None else {
        "left_played_with_results": len(left_fixtures), "right_played_with_results": len(right_fixtures),
        "same_matches_and_scores": left_fixtures == right_fixtures}
    summary = {**compare(cohort, left, right), "start": first.isoformat(), "end": last.isoformat(),
               "first_team_fixtures": schedule, "source_hashes": [left_hashes, right_hashes]}
    print(json.dumps(summary, indent=2, sort_keys=True))

"""Read aggregated growth of a frozen intake against one independently checked follow-up."""
import argparse
from collections import Counter
from contextlib import closing
from datetime import date
import json
from pathlib import Path
import sqlite3
from statistics import mean, median, pstdev

from zubieta_readback import digest, iso_birth, quoted_database


def read(path):
    return json.loads(path.read_bytes().decode("utf-8-sig"))


def scout_at(capture, source, expected_day):
    before, after = (read(capture[key]) for key in ("before", "after"))
    contexts = [r["Response"] for r in (before, after)]
    checks = ("Date", "LastSavePath", "ManagerIdentity", "TeamIdentity")
    states = ("Processing", "Saving", "IsDuringMatch")
    if (before["Status"] != "completed" or after["Status"] != "completed" or before["Pid"] != after["Pid"]
            or any(contexts[0][field] != contexts[1][field] for field in checks)
            or contexts[0]["Date"] != expected_day or any(r[k] != "False" for r in contexts for k in states)):
        raise ValueError("Stable Scout context at requested date is required")
    if (not capture["before"].stat().st_mtime <= capture["scout"].stat().st_mtime <= capture["after"].stat().st_mtime
            or digest(Path(contexts[0]["LastSavePath"])) != source):
        raise ValueError("Scout source is not bound to the requested dated save")
    exported = read(capture["scout"])
    if exported["meta"]["game"] != "FM27" or exported["meta"]["versionOk"] is not True:
        raise ValueError("Scout edition or compatibility mismatch")
    players = exported["players"]
    multiplicity = Counter(p["id"] for p in players)
    profiles = {(p["id"], iso_birth(p)): p for p in players if multiplicity[p["id"]] == 1}
    hashes = {key: digest(capture[key]) for key in ("before", "scout", "after")}
    return profiles, {"hashes": hashes, "scanner_build": exported["meta"]["pluginVersion"],
                      "scanner_reported_date": exported["meta"]["gameDate"]}


def measure(conn, career, cohort, baseline_tag, end_tag, base_scout, end_scout, end_day):
    ledger = Counter()
    deltas, factors = [], Counter()
    for member in cohort["roster"]:
        key = member["uid"], member["birth"]
        reviewed = base_scout.get(key)
        if (reviewed is None or reviewed["name"] != member["source_name"]
                or (reviewed["ca"], reviewed["pa"]) != (member["ca"], member["pa"])):
            raise ValueError("Frozen identity and baseline Scout check disagree")
        row = conn.execute("""
            SELECT a.ca,a.pa,a.candidate,a.club,b.ca,b.pa,b.candidate,b.club,n.ca,n.pa,n.club
            FROM structural.player a JOIN structural.player b USING(uid,birth)
            LEFT JOIN observation n ON n.career=? AND n.day=? AND n.uid=b.uid AND n.birth=b.birth
            WHERE a.tag=? AND b.tag=? AND a.uid=? AND a.birth=?
                  AND a.name_check IS NOT NULL AND a.name_check=b.name_check
        """, (career, end_day, baseline_tag, end_tag, *key)).fetchone()
        if row is None:
            ledger["structural_identity_missing"] += 1
            continue
        base_ca, base_pa, base_factor, base_club, ca, pa, factor, club, native_ca, native_pa, native_club = row
        if (base_ca, base_pa, base_factor, base_club) != tuple(member[k] for k in ("ca", "pa", "factor", "saved_club")):
            raise ValueError("Frozen baseline values differ from structural source")
        scout = end_scout.get(key)
        native_ok = (ca, pa) == (native_ca, native_pa)
        scout_ok = scout is not None and (ca, pa) == (scout["ca"], scout["pa"])
        if (native_ca is not None and not native_ok) or (scout is not None and not scout_ok):
            ledger["ability_readback_disagreement"] += 1
            continue
        if not native_ok and not scout_ok:
            ledger["structural_only"] += 1
            continue
        ledger["paired"] += 1
        ledger["native_ca_pa_verified"] += native_ok
        ledger["scout_ca_pa_verified"] += scout_ok
        ledger["pa_changed"] += pa != member["pa"]
        deltas.append(ca - member["ca"])
        factors[f"{member['factor']}->{factor}"] += 1
        has_save_clubs = club is not None and member["saved_club"] is not None
        has_scout_clubs = scout_ok and reviewed.get("club") and scout.get("club")
        # Confirm that both paths tell the same story about a change of club.
        same_save = club == member["saved_club"]
        if has_save_clubs and has_scout_clubs and same_save == (reviewed["club"] == scout["club"]):
            ledger["same_current_club" if same_save else "changed_current_club"] += 1
        elif has_save_clubs and native_ok and club == native_club and same_save and member["native_club"] == club:
            ledger["same_current_club"] += 1
        else:
            ledger["current_club_change_unverified"] += 1
    change = None if not deltas else {"n": len(deltas), "mean": mean(deltas), "median": median(deltas),
                                      "sd": pstdev(deltas), "min": min(deltas), "max": max(deltas),
                                      "distribution": dict(sorted(Counter(deltas).items()))}
    return {"coverage": dict(ledger), "ca_change": change, "stored_factor_transitions": dict(sorted(factors.items()))}


def analyze(cohort, native_input, native_panel, structural_panel, captures):
    career, build = native_input["career_id"], native_input["engine_build"]
    start, end = captures["baseline"], captures["followup"]
    baseline_day, end_day = start["day"], end["day"]
    if cohort["baseline_day"] != baseline_day or cohort["build"] != build or end_day <= baseline_day:
        raise ValueError("Expected same-build frozen baseline and a later snapshot")
    identities = {(p["uid"], p["birth"]) for p in cohort["roster"]}
    if not identities or len(identities) != len(cohort["roster"]):
        raise ValueError("Frozen intake identities must be unique")
    snapshots = native_input["snapshots"]
    if snapshots[baseline_day] != cohort["baseline_hashes"]:
        raise ValueError("Frozen baseline hashes differ from dated input manifest")
    profiles, evidence = {}, {}
    with closing(sqlite3.connect(quoted_database(native_panel), uri=True)) as conn:
        conn.execute("ATTACH DATABASE ? AS structural", (quoted_database(structural_panel),))
        for entry in (start, end):
            day, tag = entry["day"], entry["tag"]
            hashes = snapshots[day]
            native = conn.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                                  (career, day)).fetchone()
            structural = conn.execute("SELECT build,sha256,game_date FROM structural.capture WHERE tag=?", (tag,)).fetchone()
            if native != (build, hashes["save_sha256"], hashes["native_sha256"]) or structural != (build, hashes["save_sha256"], day):
                raise ValueError("Capture databases disagree with the dated input manifest")
            files = {k: Path(entry[k]) for k in ("scout", "before", "after")}
            profiles[day], readback = scout_at(files, hashes["save_sha256"], day)
            evidence[day] = {**hashes, **readback}
        result = measure(conn, career, cohort, start["tag"], end["tag"], profiles[baseline_day], profiles[end_day], end_day)
    return {"schema": "pa-reach-intake-growth/v1", "engine_build": build, "cohort_n": len(identities),
            "days": (date.fromisoformat(end_day) - date.fromisoformat(baseline_day)).days,
            "snapshots": evidence, **result}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("private_cohort", "private_input_manifest", "native_panel", "structural_panel", "private_captures"):
        parser.add_argument(argument, type=Path)
    args = parser.parse_args()
    print(json.dumps(analyze(read(args.private_cohort), read(args.private_input_manifest), args.native_panel,
                             args.structural_panel, read(args.private_captures)), indent=2, sort_keys=True))

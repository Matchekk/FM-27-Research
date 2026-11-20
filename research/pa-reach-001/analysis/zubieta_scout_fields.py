"""Independent FMSuperScout vs saved profile comparison at a game-thread-bracketed date."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3

from zubieta_readback import digest, iso_birth, quoted_database


def compare(panel, native, scout, before, after, tag="ZD-ROOT-01", career="ZD-ROOT-01"):
    contexts = [json.loads(p.read_bytes().decode("utf-8-sig")) for p in (before, after)]
    first, last = contexts
    if (first["Pid"] != last["Pid"] or any(c["Status"] != "completed" for c in contexts)
            or any(first["Response"][k] != last["Response"][k] for k in ("Date", "LastSavePath"))
            or any(c["Response"][k] != "False" for c in contexts for k in ("Processing", "Saving", "IsDuringMatch"))):
        raise ValueError("Unstable scanner observation")
    day = first["Response"]["Date"]
    export = json.loads(scout.read_bytes().decode("utf-8-sig"))
    meta = export["meta"]
    if meta["game"] != "FM27":
        raise ValueError("Edition mismatch")
    with sqlite3.connect(quoted_database(panel), uri=True) as conn:
        conn.execute("ATTACH DATABASE ? AS n", (quoted_database(native),))
        attrs, = conn.execute("SELECT labels FROM field_order WHERE name='raw_attrs'").fetchone()
        personal, = conn.execute("SELECT labels FROM field_order WHERE name='personality'").fetchone()
        q = """SELECT p.uid,p.birth,p.ca,p.pa,p.raw_attrs,p.personality
               FROM player p JOIN capture c USING(tag)
               JOIN n.observation n USING(uid,birth,ca,pa)
               JOIN n.snapshot s USING(career,day)
               WHERE p.tag=? AND n.career=? AND n.day=? AND c.game_date=n.day
                 AND c.sha256=s.save_hash AND c.build=s.build"""
        matched = {u: (b, ca, pa, a, pers) for u,b,ca,pa,a,pers in conn.execute(q, (tag,career,day))}
    if not matched:
        raise ValueError("No verified save at bracketed date")
    body = export["players"]
    frequencies = Counter(p["id"] for p in body)
    attrs = json.loads(attrs)
    personal = json.loads(personal)
    aliases = {label: ("FreeKicks" if label == "free_kick_taking" else
                       "".join(seg.capitalize() for seg in label.split("_"))) for label in attrs}
    keys = attrs + personal
    checked = {k: Counter() for k in keys}
    ledger = Counter(export_rows=len(body), reference_pairs=len(matched))
    for row in body:
        uid = row["id"]
        ref = matched.get(uid)
        if frequencies[uid] != 1 or not ref or iso_birth(row) != ref[0]:
            ledger["not_in_reference_with_unique_uid_and_birth"] += 1
            continue
        if (row["ca"], row["pa"]) != ref[1:3]:
            ledger["ability_mismatch"] += 1
            continue
        ledger["matched"] += 1
        for key, raw in zip(attrs, ref[3], strict=True):
            value = row["attrs"].get(aliases[key])
            if type(value) is not int or not 1 <= value <= 20:
                checked[key]["missing_or_out_of_range"] += 1
            else:
                expected = max(1, (raw + 2) // 5)
                checked[key]["equal" if value == expected else "different"] += 1
        for key, expected in zip(personal, ref[4], strict=True):
            value = row.get(key)
            if type(value) is not int or not 1 <= value <= 20 or not 1 <= expected <= 20:
                checked[key]["missing_or_out_of_range"] += 1
            else:
                checked[key]["equal" if value == expected else "different"] += 1
    return dict(bracket_date=day, scanner_reported_date=meta["gameDate"],
                scanner_date_source=meta["gameDateSource"], scanner_version=meta["pluginVersion"],
                same_pid_before_after=True, counts=ledger, fields=checked, scout_sha256=digest(scout),
                context_sha256=[digest(before),digest(after)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("panel", "native", "scout", "before", "after"):
        parser.add_argument(field, type=Path)
    parser.add_argument("--tag", default="ZD-ROOT-01")
    parser.add_argument("--career", default="ZD-ROOT-01")
    args = parser.parse_args()
    print(json.dumps(compare(args.panel,args.native,args.scout,args.before,args.after,args.tag,args.career),indent=2,sort_keys=True))

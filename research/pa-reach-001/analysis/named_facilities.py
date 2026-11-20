"""Check club identity and a named UI facility rating against an independently read save field."""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3

from facilities_and_pa import club_ratings, manifest, sha256


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def assess(directory, queue, before, after, database, checkpoint, cli):
    reader = manifest("facilities-and-pa.json")
    if sha256(cli) != reader["local_executable_sha256"]:
        raise ValueError("Club reader differs from the original pinned facility experiment")
    start, stop = read(before), read(after)
    state = start["Response"]
    day = state["Date"]
    for ctx in (start, stop):
        cur = ctx["Response"]
        if (ctx["Status"] != "completed" or any(ctx[k] != start[k] for k in ("Pid", "ThreadId"))
                or Path(cur["LastSavePath"]).resolve() != checkpoint.resolve() or cur["Date"] != day
                or any(cur[k] != "False" for k in ("Processing", "Saving", "IsDuringMatch"))):
            raise ValueError("Different checkpoint or ongoing processing")
    subjects = read(queue)
    if len({r["club"] for r in subjects}) != len(subjects):
        raise ValueError("Duplicate candidate clubs")
    counts, mapping, labels = Counter(), Counter(), Counter()
    supplied = [queue, before, after]
    with sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True) as db:
        sha, build = db.execute(
            "SELECT save_hash,build FROM snapshot WHERE career='ZD-RETENTION-01' AND day=?", (day,)
        ).fetchone()
        if build != "27.1.0+2505117":
            raise ValueError("Unexpected build")
        ratings = club_ratings(cli, checkpoint, sha)
        for q in subjects:
            prefix = f"lpRead/CheatPerson{q['index']}/"
            req_file = directory / f"{q['index']}-request.json"
            resp_file = directory / f"{q['index']}-response.json"
            req, resp = read(req_file), read(resp_file)
            supplied.extend((req_file, resp_file))
            if (req["PersonIndex"] != q["index"] or req["Operation"] != "read-properties"
                    or req["UniquePersonBinding"] is not True or resp["Status"] != "completed"
                    or any(resp[k] != start[k] for k in ("Pid", "ThreadId"))):
                raise ValueError("Unverified object")
            values = {}
            for i, field in enumerate(resp["Response"], 1):
                src = directory / f"{q['index']}-{i}.json"
                if not src.exists() or not field["Exists"]:
                    continue
                supplied.append(src)
                prop = read(src)
                time = datetime.fromisoformat(prop["Utc"].replace("Z", "+00:00")).timestamp()
                if (prop["Path"] != field["Path"] or prop["Path"] not in req["Paths"]
                        or not prop["Path"].startswith(prefix) or not before.stat().st_mtime <= time <= after.stat().st_mtime):
                    raise ValueError("Callback outside object or acquisition bracket")
                values[prop["Path"][len(prefix):]] = prop
            base = "PrimaryClubTeam/Club"
            ref = db.execute(
                "SELECT club FROM observation WHERE career='ZD-RETENTION-01' AND day=? AND uid=? AND birth=?",
                (day, q["uid"], q["birth"]),
            ).fetchone()
            if ref != (q["club"],) or ratings.get(q["club"]) != q["rating"]:
                raise ValueError("Independent player/club source or save rating disagrees")
            if (int(values["UniqueId"]["Value"]) != q["uid"] or values["DateOfBirth"]["Value"] != q["birth"]):
                counts["wrong_person_or_birth"] += 1
                continue
            counts["player_uid_birth_confirmed"] += 1
            if (values[base]["Type"] != "FM.UI.ClubReference" or int(values[base+"/UniqueId"]["Value"]) != q["club"]):
                counts["wrong_native_club"] += 1
                continue
            prop = values[base+"/TrainingFacilityRating"]
            if prop["Type"] != "SI.Bindable.DynamicReference":
                raise ValueError("Unexpected facility rating type")
            fields = {f["Name"].split(":")[0]: f["Data"] for f in prop["Details"]["Fields"]}
            bounds = {f["Name"].split(":")[0]: f["Data"]["Value"] for f in fields["FacilityStarRange"]["Fields"]}
            score = int(fields["Rating"]["Value"])
            if (fields["Rating"]["Type"] != "SI.Core.DynamicNumber" or bounds["IsScoutsOpinion"] != "False"
                    or int(bounds["MinValue"]) != score or int(bounds["MaxValue"]) != score):
                raise ValueError("Incomplete facility rating or scout range")
            counts["intended_club_confirmed"] += 1
            mapping[q["rating"], score] += 1
            if q["rating"] in (16, 17):
                labels[fields["Description"]["Value"]] += 1
    receipt = hashlib.sha256()
    for src in supplied:
        receipt.update(hashlib.sha256(src.read_bytes()).digest())
    return {
        "schema": "pa-reach-named-facility-rating/v1", "date": day, "game_build": build, "save_sha256": sha,
        "reader_revision": reader["external_reader_revision"], "reader_sha256": reader["local_executable_sha256"],
        "private_receipt_sha256": receipt.hexdigest(), "clubs_requested": len(subjects), **counts,
        "native_property": "Person.PrimaryClubTeam.Club.TrainingFacilityRating.Rating",
        "included_rows": [{"reader_integer": a, "named_ui_rating": b, "clubs": n}
                          for (a,b),n in sorted(mapping.items())],
        "included_exact_matches": sum(n for (a,b),n in mapping.items() if a==b),
        "descriptions_for_included_16_17": dict(labels),
        "numeric_boundary_independently_resolved": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("directory", "queue", "before", "after", "database", "checkpoint", "cli"):
        parser.add_argument(arg, type=Path)
    print(json.dumps(assess(**vars(parser.parse_args())), indent=2, ensure_ascii=False))

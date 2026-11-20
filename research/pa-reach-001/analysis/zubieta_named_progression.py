"""Verify existing private, parked-game property callbacks against a frozen save panel."""

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3


PROPERTIES = {
    "UniqueId": "SI.Core.DynamicNumber",
    "DateOfBirth": "FM.GamePlugin.GameDate",
    "ProgressionFactor": "SI.Core.DynamicNumber",
    "ProgressionFactorRecalculationScore": "SI.Core.DynamicNumber",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def summarize(directory, queue, panel, tag, checkpoint, before, after, private_rows=None):
    with sqlite3.connect(f"{panel.resolve().as_uri()}?mode=ro", uri=True) as conn:
        source_hash, date, build = conn.execute(
            "SELECT sha256, game_date, build FROM capture WHERE tag=?", (tag,)
        ).fetchone()
        contexts = [read(path) for path in (before, after)]
        if source_hash != digest(checkpoint) or build != "27.1.0+2505117":
            raise ValueError("Checkpoint or build mismatch")
        for context in contexts:
            state = context["Response"]
            quiet = all(str(state[k]).lower() == "false" for k in ("IsDuringMatch", "Processing", "Saving"))
            if (context["Status"] != "completed" or not quiet or state["Date"] != date
                    or Path(state["LastSavePath"]).resolve() != checkpoint.resolve()):
                raise ValueError("Incomplete same-day parked-game bracket")
        if any(contexts[0][k] != contexts[1][k] for k in ("ThreadId", "Pid")):
            raise ValueError("Live process changed")

        queue_rows = read(queue)
        if (len({p["uid"] for p in queue_rows}) != len(queue_rows)
                or len({p["index"] for p in queue_rows}) != len(queue_rows)):
            raise ValueError("Duplicate private queue key")
        matrix, score_counts, excluded = Counter(), Counter(), Counter()
        linked = []
        source_files = [before, after, queue]
        for person in queue_rows:
            prefix = str(person["index"])
            def load_part(label):
                artifact = directory / f"{prefix}-{label}.json"
                source_files.append(artifact)
                return read(artifact)

            req, resp = load_part("request"), load_part("response")
            if (req["Operation"] != "read-properties" or not req["UniquePersonBinding"]
                    or req["PersonIndex"] != person["index"] or resp["Status"] != "completed"
                    or any(resp[k] != contexts[0][k] for k in ("Pid", "ThreadId"))):
                raise ValueError("Unverified player request")
            existing = {row["Path"] for row in resp["Response"] if row["Exists"] is True}
            values = {}
            for key, native_type in PROPERTIES.items():
                prop = load_part(key)
                path = f"lpRead/CheatPerson{prefix}/{key}"
                timestamp = datetime.fromisoformat(prop["Utc"].replace("Z", "+00:00")).timestamp()
                if not before.stat().st_mtime <= timestamp <= after.stat().st_mtime:
                    raise ValueError("Callback not inside acquisition bracket")
                if (path in req["Paths"] and path in existing and prop["Path"] == path
                        and prop["Type"] == native_type and prop["Value"] is not None):
                    values[key] = prop["Value"]
            if values.keys() != PROPERTIES.keys():
                excluded["missing_named_value"] += 1
                continue
            if int(values["UniqueId"]) != person["uid"]:
                excluded["native_id_disagrees"] += 1
                continue
            rows = conn.execute(
                "SELECT birth, candidate, ca, pa FROM player WHERE tag=? AND uid=?", (tag, person["uid"])
            ).fetchall()
            if len(rows) != 1 or rows[0][0] != values["DateOfBirth"]:
                excluded["save_identity_unconfirmed"] += 1
                continue
            matrix[rows[0][1], int(values["ProgressionFactor"])] += 1
            score_counts[int(values["ProgressionFactorRecalculationScore"])] += 1
            linked.append({
                "uid": person["uid"], "birth": rows[0][0], "ca": rows[0][2], "pa": rows[0][3],
                "saved_factor": rows[0][1], "native_factor": int(values["ProgressionFactor"]),
                "native_recalculation_score": int(values["ProgressionFactorRecalculationScore"]),
            })
    # A digest of ordered content hashes attests to private files without exposing their names.
    receipt = hashlib.sha256("".join(digest(path) for path in source_files).encode()).hexdigest()
    if private_rows:
        with private_rows.open("x", encoding="utf-8") as out:
            json.dump({"game_date": date, "save_sha256": source_hash,
                       "private_receipt_sha256": receipt, "rows": linked}, out)
    return {
        "schema": "pa-reach-named-progression/v1", "game_date": date,
        "engine_build": build, "snapshot_sha256": source_hash, "private_receipt_sha256": receipt,
        "game_thread_parked_before_and_after": True, "independent_careers": 1,
        "selection": "purposeful; frequency distribution and predictive calibration not estimable",
        "requested": len(queue_rows), "identity_and_native_type_confirmed": matrix.total(),
        "excluded": dict(excluded), "save_ca_relative_byte_offset": 7,
        "native_name": "ProgressionFactor", "native_type": PROPERTIES["ProgressionFactor"],
        "equal": sum(n for (a, b), n in matrix.items() if a == b),
        "confusion": [{"save": a, "native": b, "n": n} for (a, b), n in sorted(matrix.items())],
        "recalculation_score_frequency_in_panel": dict(sorted(score_counts.items())),
        "zero_meaning": "NOT_ROLLED_OR_UNVERIFIED",
        "growth_caps_monthly_exceptions_rerolls": "NOT_ESTABLISHED_BY_FIELD_IDENTITY",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("directory", "queue", "panel"):
        parser.add_argument(arg, type=Path)
    parser.add_argument("tag")
    for arg in ("checkpoint", "before", "after"):
        parser.add_argument(arg, type=Path)
    parser.add_argument("--private-rows", type=Path, help="exclusive new private file for follow-up linkage")
    print(json.dumps(summarize(**vars(parser.parse_args())), indent=2))

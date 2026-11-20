"""Attach one source-checked named property read to an already independently captured date."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3

from pa_reach_capture import initialize_panel


def attach(conn, career, private, public):
    day, source, receipt = (private[k] for k in ("game_date", "save_sha256", "private_receipt_sha256"))
    if ((day, source, receipt) != (public["game_date"], public["snapshot_sha256"], public["private_receipt_sha256"])
            or public["engine_build"] != "27.1.0+2505117" or public["native_name"] != "ProgressionFactor"
            or public["game_thread_parked_before_and_after"] is not True
            or public["save_ca_relative_byte_offset"] != 7
            or public["binding_modes"] != {"shared_two_requests": public["requested"]}):
        raise ValueError("Requires dated, identity-checked two-request binding evidence")
    rows = private["rows"]
    matrix = Counter((r["saved_factor"], r["native_factor"]) for r in rows)
    expected = {(m["save"], m["native"]): m["n"] for m in public["confusion"]}
    if (len({r["uid"] for r in rows}) != len(rows) or len(rows) != public["identity_and_native_type_confirmed"]
            or dict(matrix) != expected):
        raise ValueError("Private identity ledger differs from named-read manifest")
    snapshot = conn.execute("SELECT build,save_hash FROM snapshot WHERE career=? AND day=?", (career, day)).fetchone()
    if snapshot != (public["engine_build"], source):
        raise ValueError("Private panel has no matching career checkpoint")
    counts = Counter()
    with conn:
        conn.execute("BEGIN IMMEDIATE")
        for r in rows:
            key = (career, day, r["uid"], r["birth"])
            match = conn.execute("SELECT ca,pa,candidate FROM observation WHERE career=? AND day=? AND uid=? AND birth=?",
                                 key).fetchone()
            if match is None:
                counts["no_independent_ability_row"] += 1
                continue
            if match != (r["ca"],r["pa"],r["saved_factor"]):
                raise ValueError("Independent ability panel and named-read record differ")
            record = (*key, r["native_factor"], receipt)
            conn.execute("INSERT OR IGNORE INTO factor_check VALUES(?,?,?,?,?,?)",record)
            if conn.execute("SELECT * FROM factor_check WHERE career=? AND day=? AND uid=? AND birth=?",key).fetchone() != record:
                raise ValueError("A different property check exists for this player and date")
            counts["checked"] += 1
            if r["native_factor"] != r["saved_factor"]:
                counts["native_save_disagreement"] += 1
            elif r["native_factor"] in range(1,6):
                counts["verified_tier"] += 1
            elif r["native_factor"] == 0:
                counts["verified_zero_unknown_meaning"] += 1
    return dict(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for label in ("database","private_ledger","manifest"):
        parser.add_argument(label,type=Path)
    parser.add_argument("career")
    a = parser.parse_args()
    with sqlite3.connect(a.database.resolve().as_uri()+"?mode=rw",uri=True) as c:
        initialize_panel(c)
        print(json.dumps(attach(c,a.career,json.loads(a.private_ledger.read_bytes()),json.loads(a.manifest.read_bytes()))))

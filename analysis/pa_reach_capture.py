"""Private, append-only PA-REACH capture. Requires fmsave==0.14.1 and Python 3.12+."""
import argparse
import hashlib
import json
import sqlite3
import struct
from collections import Counter
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshot(
 career TEXT, day TEXT, build TEXT, save_hash TEXT, inventory_hash TEXT,
 reader TEXT, accounting TEXT, PRIMARY KEY(career,day), UNIQUE(career,save_hash)
);
CREATE TABLE IF NOT EXISTS observation(
 career TEXT, day TEXT, uid INTEGER, birth TEXT, age INTEGER,
 position TEXT, ca INTEGER, pa INTEGER, candidate INTEGER, club INTEGER,
 PRIMARY KEY(career,day,uid),
 FOREIGN KEY(career,day) REFERENCES snapshot(career,day)
);
CREATE TABLE IF NOT EXISTS factor_check(
 career TEXT NOT NULL, day TEXT NOT NULL, uid INTEGER NOT NULL, birth TEXT NOT NULL,
 native_factor INTEGER NOT NULL, receipt TEXT NOT NULL, PRIMARY KEY(career,day,uid),
 FOREIGN KEY(career,day,uid) REFERENCES observation(career,day,uid)
);
CREATE VIEW IF NOT EXISTS research_panel AS
 SELECT o.career AS career_id, o.day AS snapshot_date, s.build AS engine_build,
        o.uid AS player_id_within_career, o.birth, o.age, o.position AS position_family,
        o.ca AS current_CA, o.pa AS snapshot_PA,
        first_value(o.pa) OVER (PARTITION BY o.career,o.uid,o.birth ORDER BY o.day) AS baseline_PA,
        o.candidate AS candidate_byte,
        CASE WHEN s.build='27.1.0+2505117' AND o.candidate BETWEEN 0 AND 5
             THEN o.candidate END AS stored_progression_factor,
        CASE WHEN s.build='27.1.0+2505117' AND o.candidate BETWEEN 1 AND 5
                  AND f.native_factor=o.candidate
             THEN o.candidate END AS progression_tier_if_verified,
        NULL AS professionalism, NULL AS ambition, NULL AS determination,
        o.club AS current_club, NULL AS club_reputation, NULL AS training_facilities_if_verified,
        NULL AS contract_start_if_verified, NULL AS playing_minutes_if_verified,
        NULL AS injury_days_if_verified, NULL AS loan_status
 FROM observation o JOIN snapshot s USING(career,day)
 LEFT JOIN factor_check f USING(career,day,uid,birth);
"""


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def initialize_panel(conn):
    """Update derived interpretation without editing saved raw observations."""
    conn.execute("PRAGMA foreign_keys=ON")
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    if version == 4:
        return
    if version in (2, 3):
        columns = [c[1] for c in conn.execute("PRAGMA table_info(observation)")]
        snapshots = [c[1] for c in conn.execute("PRAGMA table_info(snapshot)")]
        if (columns != ["career", "day", "uid", "birth", "age", "position", "ca", "pa", "candidate", "club"]
                or snapshots != ["career", "day", "build", "save_hash", "inventory_hash", "reader", "accounting"]):
            raise ValueError("Unrecognized private capture panel")
    elif version or conn.execute("SELECT 1 FROM sqlite_master LIMIT 1").fetchone():
        raise ValueError("Existing database has unrelated schema")
    migration = "DROP VIEW IF EXISTS research_panel;" if version else ""
    conn.executescript("BEGIN IMMEDIATE;\n" + migration + SCHEMA + "PRAGMA user_version=4;\nCOMMIT;")


def decode(save, native):
    """Yield accepted rows; the ledger accounts for every indexed save record."""
    from fmsave._layouts import ContractLayout, PersonBlockLayout, find_layout
    from fmsave._scan import decode_date
    from fmsave.readers.player_scan import window_end
    from fmsave.readers.players import build_player_decoder

    counts = Counter(native_records=len(native))
    frequencies = Counter(row["Uid"] for row in native)
    reference = {row["Uid"]: row for row in native if frequencies[row["Uid"]] == 1}
    ctx = save._context
    build = save.info.build
    schema = save.info.section_schemas["game_db"]
    if schema != 4000:
        raise ValueError("Unsupported game_db schema")
    with ctx.section("game_db") as db:
        records = ctx.player_records()
        layout = records.layout
        decoder = build_player_decoder(
            layout, ctx.club_index(), ctx.name_pools(), save.info.game_date,
            find_layout(PersonBlockLayout, "game_db", schema, build).layout,
            find_layout(ContractLayout, "game_db", schema, build).layout, save.info.file_name,
        )
        counts["save_records"] = len(records.uids)
        rows = []
        closings = []
        for i, offset in enumerate(records.record_offsets):
            end = window_end(records, i, len(db))
            closing = decoder.closing_header(
                db, offset, end, records.pindexes[i], records.uids[i],
                is_last_record=i == len(records.uids) - 1,
                next_record_ambiguous=i + 1 in records.ambiguous_positions,
            )
            closings.append(closing)
        identities = Counter(c.uid for c in closings if c)
        counts["native_uid_absent_from_save"] = sum(
            frequencies[uid] for uid in frequencies.keys() - identities.keys()
        )
        for i, closing in enumerate(closings):
            if closing is None:
                counts["no_closing_identity"] += 1
                continue
            uid = closing.uid
            if i in records.ambiguous_positions or frequencies[uid] > 1 or identities[uid] > 1:
                counts["ambiguous_uid"] += 1
                continue
            other = reference.get(uid)
            if other is None:
                counts["no_native_uid"] += 1
                continue
            offset = records.record_offsets[i]
            end = window_end(records, i, len(db))
            person = decoder.decode_person(db, offset, end, closing)
            birth = decode_date(struct.pack("<I", other["BirthRaw"]), 0)
            if not person or birth is None or person[6] != birth:
                counts["birth_missing_or_mismatch"] += 1
                continue
            ca_start = offset + layout.current_ability_offset
            ca, pa = struct.unpack_from("<hh", db, ca_start)
            if (ca, pa) != (other["Ca"], other["Pa"]):
                counts["ability_mismatch"] += 1
                continue
            if not (1 <= ca <= 200 and 1 <= pa <= 200):
                counts["unresolved_ability"] += 1
                continue
            positions = db[offset + layout.ratings_offset:offset + layout.ratings_offset + layout.ratings_count]
            best = max(positions)
            natural = [code for code, rating in zip(layout.position_codes, positions, strict=True)
                       if rating == best and rating >= 18]
            position = "GK" if "GK" in natural else (natural[0] if natural else None)
            candidate = db[ca_start + 7]
            if candidate > 5:
                counts["outside_candidate_range"] += 1
            team_id, = struct.unpack_from("<I", db, offset + layout.team_id_offset)
            team = decoder.team_fields.get(team_id)
            club = team[0] if team and team[0] == other["ClubUid"] else None
            if club is None:
                counts["club_unverified_among_accepted"] += 1
            rows.append((uid, birth.isoformat(), person[7], position, ca, pa, candidate, club))
        counts["accepted_ability_pairs"] = len(rows)
    return rows, dict(counts)


def capture(db_path, manifest, day, save_path, inventory_path):
    import fmsave

    meta = manifest["snapshots"][day]
    build, career = manifest["engine_build"], manifest["career_id"]
    if manifest["schema_version"] != 1 or fmsave.__version__ != "0.14.1" or build not in {"27.0.1+2503222", "27.1.0+2505117"}:
        raise ValueError("Unsupported reader or build")
    if digest(save_path) != meta["save_sha256"] or digest(inventory_path) != meta["native_sha256"]:
        raise ValueError("Source hash differs from dated manifest")
    native = json.loads(inventory_path.read_bytes())
    if native["ReadOnly"] is not True or native["ModuleSha256"].lower() != manifest["native_module_sha256"]:
        raise ValueError("Native source provenance mismatch")
    with fmsave.open(save_path) as save:
        if (save.info.game, save.info.build, str(save.info.game_date)) != ("FM27", build, day):
            raise ValueError("Save metadata differs from manifest")
        rows, counts = decode(save, native["Players"])
    with sqlite3.connect(db_path) as conn:
        initialize_panel(conn)
        conn.execute("BEGIN IMMEDIATE")
        if conn.execute("SELECT 1 FROM snapshot WHERE career=? AND build<>?", (career, build)).fetchone():
            raise ValueError("Use a separate series for different builds")
        conn.execute("INSERT INTO snapshot VALUES(?,?,?,?,?,?,?)", (
            career, day, build, meta["save_sha256"], meta["native_sha256"],
            fmsave.__version__, json.dumps(counts, sort_keys=True),
        ))
        conn.executemany("INSERT INTO observation VALUES(?,?,?,?,?,?,?,?,?,?)",
                         ((career, day, *r) for r in rows))
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ("private_database", "manifest", "day", "save", "native_inventory"):
        parser.add_argument(field, type=str if field == "day" else Path)
    args = parser.parse_args()
    print(json.dumps(capture(args.private_database, json.loads(args.manifest.read_bytes()),
                             args.day, args.save, args.native_inventory), sort_keys=True))

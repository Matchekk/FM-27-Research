"""Capture one authorised COPY to private SQLite. No live attachment. fmsave==0.14.1."""

import argparse
from collections import Counter
from dataclasses import astuple, fields
import hashlib
import json
from pathlib import Path
import sqlite3
import struct

import fmsave
from fmsave._layouts import ContractLayout, PersonBlockLayout, find_layout
from fmsave.models.players import Attributes, Personality
from fmsave.readers.player_scan import window_end
from fmsave.readers.players import build_player_decoder


SCHEMA = """
CREATE TABLE IF NOT EXISTS capture(
 tag TEXT PRIMARY KEY, sha256 TEXT NOT NULL UNIQUE, game_date TEXT NOT NULL,
 build TEXT NOT NULL, reader TEXT NOT NULL, managed TEXT, accounting TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS player(
 tag TEXT NOT NULL REFERENCES capture(tag), uid INTEGER NOT NULL, birth TEXT NOT NULL,
 name_check BLOB, age INTEGER, pos TEXT, ca INTEGER, pa INTEGER, candidate INTEGER,
 club INTEGER, reputation INTEGER, professionalism INTEGER, ambition INTEGER, determination INTEGER,
 natural_fitness INTEGER, injury_proneness INTEGER, positions BLOB, raw_attrs BLOB, personality BLOB,
 PRIMARY KEY(tag,uid)
);
CREATE TABLE IF NOT EXISTS field_order(name TEXT PRIMARY KEY, labels TEXT NOT NULL);
"""


def file_hash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def capture_copy(conn, tag, source, expected_sha):
    if fmsave.__version__ != "0.14.1" or file_hash(source) != expected_sha:
        raise ValueError("Unexpected reader or source digest")
    with fmsave.open(source) as save:
        schema = save.info.section_schemas.get("game_db")
        if save.info.game != "FM27" or schema != 4000 or save.info.game_date is None:
            raise ValueError("Unusable edition, schema or game date")
        build, day = save.info.build, save.info.game_date.isoformat()
        if build not in {"27.0.1+2494687", "27.1.0+2505117"}:
            raise ValueError("Unreviewed build")
        # Separate native confirmation is required before any field becomes a gold measurement.
        managed = [(m.manager_staff_uid, m.club_uid) for m in save.managed_clubs()]
        ctx = save._context
        with ctx.section("game_db") as db:
            records = ctx.player_records()
            layout = records.layout
            decoder = build_player_decoder(
                layout, ctx.club_index(), ctx.name_pools(), save.info.game_date,
                find_layout(PersonBlockLayout, "game_db", schema, build).layout,
                find_layout(ContractLayout, "game_db", schema, build).layout, save.info.file_name,
            )
            closings = []
            for i, offset in enumerate(records.record_offsets):
                end = window_end(records, i, len(db))
                closings.append(decoder.closing_header(
                    db, offset, end, records.pindexes[i], records.uids[i],
                    is_last_record=i == len(records.uids) - 1,
                    next_record_ambiguous=i + 1 in records.ambiguous_positions,
                ))
            multiplicity = Counter(c.uid for c in closings if c is not None)
            counts = Counter(indexed=len(closings))
            conn.execute("INSERT INTO capture VALUES(?,?,?,?,?,?,?)",
                         (tag, expected_sha, day, build, fmsave.__version__, json.dumps(managed), "{}"))
            orders = {
                "raw_attrs": [f.name for f in fields(Attributes)],
                "personality": [f.name for f in fields(Personality)],
                "positions": list(layout.position_codes),
            }
            for key, labels in orders.items():
                encoded = json.dumps(labels)
                conn.execute("INSERT OR IGNORE INTO field_order VALUES(?,?)", (key, encoded))
                if conn.execute("SELECT labels FROM field_order WHERE name=?", (key,)).fetchone()[0] != encoded:
                    raise ValueError("Field order changed")
            for i, closing in enumerate(closings):
                if closing is None or multiplicity[closing.uid] != 1 or i in records.ambiguous_positions:
                    counts["absent_or_ambiguous_id"] += 1
                    continue
                offset = records.record_offsets[i]
                person = decoder.decode_person(db, offset, window_end(records, i, len(db)), closing)
                if person is None or person[6] is None or person[7] is None:
                    counts["missing_dob_or_age"] += 1
                    continue
                ca_start = offset + layout.current_ability_offset
                ca, pa = struct.unpack_from("<hh", db, ca_start)
                if not (1 <= ca <= 200 and 1 <= pa <= 200):
                    counts["unresolved_ca_pa"] += 1
                    continue
                raw = db[offset + layout.attributes_offset:offset + layout.attributes_offset + layout.attribute_count]
                attrs = Attributes(*decoder.attribute_struct.unpack(raw.translate(decoder.scale_table)))
                pos = db[offset + layout.ratings_offset:offset + layout.ratings_offset + layout.ratings_count]
                best = max(pos)
                natural = [code for code, rating in zip(layout.position_codes, pos, strict=True)
                           if rating == best and rating >= 18]
                position = "GK" if "GK" in natural else next(iter(natural), None)
                personality = person[13]
                team_id, = struct.unpack_from("<I", db, offset + layout.team_id_offset)
                team = decoder.team_fields.get(team_id)
                # Keep names out of the panel. The private hash is an additional linkage check.
                name = person[4] or person[0]
                name_check = hashlib.sha256(name.strip().casefold().encode()).digest() if name else None
                conn.execute("INSERT INTO player VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                    tag, closing.uid, person[6].isoformat(), name_check, person[7], position,
                    ca, pa, db[ca_start + 7], team[0] if team else None, team[5] if team else None,
                    personality.professionalism, personality.ambition, attrs.determination,
                    attrs.natural_fitness, attrs.injury_proneness, pos,
                    bytes(decoder.attribute_struct.unpack(raw)), bytes(astuple(personality)),
                ))
                counts["accepted_save_rows"] += 1
        if file_hash(source) != expected_sha:
            raise ValueError("Copy changed during capture")
        conn.execute("UPDATE capture SET accounting=? WHERE tag=?", (json.dumps(counts, sort_keys=True), tag))
    return day, build, dict(counts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_db", type=Path)
    parser.add_argument("tag")
    parser.add_argument("copy", type=Path)
    parser.add_argument("sha256")
    args = parser.parse_args()
    with sqlite3.connect(args.private_db) as conn:
        conn.execute("PRAGMA foreign_keys=ON")
        conn.executescript(SCHEMA)
        conn.execute("BEGIN IMMEDIATE")
        print(capture_copy(conn, args.tag, args.copy, args.sha256))

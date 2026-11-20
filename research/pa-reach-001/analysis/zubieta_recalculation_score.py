"""Predefined signed relative *positions*, unsigned byte values. Private inputs, aggregate output."""

import argparse
from collections import Counter
import json
from pathlib import Path
import struct

import fmsave
from fmsave._layouts import ContractLayout, PersonBlockLayout, find_layout
from fmsave.readers.player_scan import window_end
from fmsave.readers.players import build_player_decoder

from zubieta_snapshot import file_hash


def read_windows(source, receipt):
    native = json.loads(receipt.read_text(encoding="utf-8"))
    targets = {r["uid"]: r for r in native["rows"]}
    if len(targets) != len(native["rows"]) or file_hash(source) != native["save_sha256"]:
        raise ValueError("Snapshot receipt or identity count failed")
    windows = {}
    with fmsave.open(source) as save:
        build = save.info.build
        if (build != "27.1.0+2505117" or save.info.game_date.isoformat() != native["game_date"]
                or save.info.section_schemas.get("game_db") != 4000 or fmsave.__version__ != "0.14.1"):
            raise ValueError("Unexpected checkpoint, reader or build")
        ctx = save._context
        with ctx.section("game_db") as db:
            records = ctx.player_records()
            layout = records.layout
            decoder = build_player_decoder(
                layout, ctx.club_index(), ctx.name_pools(), save.info.game_date,
                find_layout(PersonBlockLayout, "game_db", 4000, build).layout,
                find_layout(ContractLayout, "game_db", 4000, build).layout, save.info.file_name,
            )
            for i, offset in enumerate(records.record_offsets):
                end = window_end(records, i, len(db))
                clos = decoder.closing_header(
                    db, offset, end, records.pindexes[i], records.uids[i],
                    is_last_record=i == len(records.uids)-1, next_record_ambiguous=i+1 in records.ambiguous_positions,
                )
                if clos is None or clos.uid not in targets:
                    continue
                row = targets[clos.uid]
                person = decoder.decode_person(db, offset, end, clos)
                start = offset + layout.current_ability_offset
                if (i in records.ambiguous_positions or clos.uid in windows
                        or person[6].isoformat() != row["birth"] or db[start+7] != row["native_factor"]
                        or struct.unpack_from("<hh", db, start) != (row["ca"], row["pa"])):
                    raise ValueError("Private row or positive control failed")
                windows[clos.uid] = (bytes(db[start-24:start+25]), row["native_recalculation_score"])
    if windows.keys() != targets.keys():
        raise ValueError("Incomplete source coverage")
    return windows, native["private_receipt_sha256"]


def matching(windows, offsets):
    return {offset: sum(chunk[offset+24] == score for chunk, score in windows.values()) for offset in offsets}


def compare(discovery_save, discovery_native, replication_save, replication_native):
    disc, receipt_a = read_windows(discovery_save, discovery_native)
    rep, receipt_b = read_windows(replication_save, replication_native)
    if len(disc)!=12 or len(rep)!=16 or disc.keys() & rep.keys():
        raise ValueError("Predefined disjoint group sizes failed")
    counts = matching(disc, range(-24, 25))
    winners = [offset for offset,count in counts.items() if count==len(disc)]
    follow = matching(rep, winners)
    return {
        "schema": "pa-reach-recalculation-byte/v1", "build": "27.1.0+2505117", "game_date": "2027-03-31",
        "private_receipt_sha256": [receipt_a, receipt_b], "career_clusters": 1,
        "searched_bytes_relative_to_ca": [-24, 24], "positions_tested": len(counts),
        "discovery_players": len(disc), "replication_players_available": len(rep),
        "positive_control_factor_equal": [len(disc),len(rep)],
        "discovery_match_count_histogram_across_offsets": dict(sorted(Counter(counts.values()).items())),
        "offsets_matching_all_discovery_players": winners, "replication_matches_by_candidate_offset": follow,
        "offsets_matching_both_groups": [offset for offset,count in follow.items() if count==len(rep)],
    }


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ("discovery_save","discovery_native","replication_save","replication_native"):
        parser.add_argument(arg,type=Path)
    print(json.dumps(compare(**vars(parser.parse_args())),indent=2))

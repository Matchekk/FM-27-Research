"""Inventory a managed club's current contracts and registrations from an immutable copy."""

import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

import fmsave

from zubieta_readback import digest, iso_birth


def iso(value):
    return value.isoformat() if value else None


def inventory(source, expected, deadline, private_output, scout=None):
    if digest(source) != expected or fmsave.__version__ != "0.14.1":
        raise ValueError("Unexpected source or reader")
    scanned = {}
    if scout:
        scan = json.loads(scout.read_bytes().decode("utf-8-sig"))
        multiplicity = Counter(p["id"] for p in scan["players"])
        scanned = {(p["id"],iso_birth(p)): p for p in scan["players"] if multiplicity[p["id"]] == 1}
    with fmsave.open(source) as save:
        if save.info.build != "27.1.0+2505117":
            raise ValueError("Unreviewed build")
        managed = list(save.managed_clubs())
        if len(managed) != 1:
            raise ValueError("Club cannot be bound to one manager")
        club = managed[0].club_uid
        day = save.info.game_date
        players = save.players()
        contracts = {c.player_uid: c for c in save.contracts()}
        uids = Counter(p.unique_id for p in players)
        members = []
        for p in players:
            c = contracts.get(p.uid)
            registered = p.club_uid == club
            owner = bool(c and c.club_uid == club and (c.end is None or c.end >= day))
            if not registered and not owner:
                continue
            uid, birth = p.unique_id, iso(p.birth_date)
            stable = uid is not None and uids[uid] == 1 and birth is not None
            other = scanned.get((uid,birth)) if stable else None
            verified_profile = bool(other and other["ca"] == p.ability.current and other["pa"] == p.ability.potential)
            end = c.end if c else None
            end_other = other.get("expires") if verified_profile else None
            future = [dict(start=iso(e.start),end=iso(e.end),same_club=e.club_uid == club,has_terms=e.has_terms)
                      for e in c.chain if e.start and e.start > day] if c else []
            members.append(dict(
                id=uid, birth=birth, name=p.name, age=p.age, stable=stable, registered=registered,
                contract_owner=owner, owner_missing=c is None or c.club_uid is None,
                loan_status=p.on_loan, stored_team_slot=p.team_slot,
                contract_start=iso(c.start) if c else None, contract_end=iso(end),
                end_source=str(c.end_source.value) if c and c.end_source else None,
                contract_kind=c.kind.label.name if c and c.kind else None,
                expires_by_cutoff=bool(end and day <= end <= deadline) if end else None,
                scan_end=end_other, scan_agrees_end=iso(end) == end_other if end and end_other else None,
                future_spells=future,
            ))
        if digest(source) != expected:
            raise ValueError("Source changed")
        result = dict(game_date=iso(day),build=save.info.build,source_sha256=expected,
                      deadline=iso(deadline),members=members)
    # Identities and exact dates reside only in a user-selected private directory.
    with private_output.open("x", encoding="utf8") as stream:
        json.dump(result,stream,ensure_ascii=False)
    owned = [p for p in members if p["contract_owner"]]
    due = [p for p in owned if p["expires_by_cutoff"] is True]
    undated = [p for p in owned if p["contract_end"] is None]
    return {
        "game_date": iso(day), "save_sha256": expected, "build": result["build"], "cutoff": iso(deadline),
        "registered_or_contracted": len(members), "registered": sum(p["registered"] for p in members),
        "contract_owner_resolves_to_club": len(owned), "club_held_outside_registered_squad": sum(not p["registered"] for p in owned),
        "registered_ownership_unresolved": sum(p["registered"] and p["owner_missing"] for p in members),
        "owned_without_end": len(undated),
        "owned_without_end_age_counts": dict(Counter(p["age"] for p in undated)),
        "owned_without_end_start_counts": dict(Counter(p["contract_start"] for p in undated)),
        "owned_expiring_by_cutoff": len(due), "due_stable_identity": sum(p["stable"] for p in due),
        "due_same_day_scan_end_agrees": sum(p["scan_agrees_end"] is True for p in due),
        "due_scan_end_differs": sum(p["scan_agrees_end"] is False for p in due),
        "due_scan_end_missing": sum(p["scan_agrees_end"] is None for p in due),
        "due_with_later_same_club_terms": sum(any(e["same_club"] and e["has_terms"] and e["end"] and e["end"] > iso(deadline)
                                                   for e in p["future_spells"]) for p in due),
        "youth_intake_candidates_identified_from_team_slot": None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save_copy", type=Path)
    parser.add_argument("sha256")
    parser.add_argument("deadline", type=date.fromisoformat)
    parser.add_argument("private_output", type=Path)
    parser.add_argument("--bracketed-scout", type=Path, help="Use only a scanner export independently bound to this game date")
    args = parser.parse_args()
    print(json.dumps(inventory(args.save_copy,args.sha256,args.deadline,args.private_output,args.bracketed_scout),indent=2))

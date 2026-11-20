"""Link private intake UI receipts to registered players and a separately dated branch."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def cohort(source, day):
    return [r for r in source["members"] if r["contract_owner"] and r["contract_start"] == day
            and r["contract_end"] is None and r["stable"]]


def link(offers, retention, control, retention_panel, control_panel, local_link):
    ret, ctl = read(retention), read(control)
    queue = read(offers)["intake"]
    day = ret["game_date"]
    first, second = cohort(ret, day), cohort(ctl, day)
    named = Counter(r["name"] for r in first)
    ui_names = Counter(r["name"] for r in queue["entries"])
    linked_offers = {r["name"]: r for r in queue["entries"] if named[r["name"]] == ui_names[r["name"]] == 1}
    local = [
        {**{key: r[key] for key in ("id", "birth", "name")}, **linked_offers[r["name"]]}
        for r in first if r["name"] in linked_offers
    ]
    if local_link:
        # These names and identifiers must remain outside public version control.
        with local_link.open("x", encoding="utf-8") as output:
            json.dump(local, output, indent=2, ensure_ascii=False)

    db_uri = lambda p: f"{p.resolve().as_uri()}?mode=ro"
    with sqlite3.connect(db_uri(retention_panel), uri=True) as db:
        db.execute("ATTACH ? AS ctrl", (db_uri(control_panel),))
        ret_tag, = db.execute("SELECT tag FROM capture WHERE sha256=?", (ret["source_sha256"],)).fetchone()
        ctl_tag, = db.execute("SELECT tag FROM ctrl.capture WHERE sha256=?", (ctl["source_sha256"],)).fetchone()
        common = {(r["id"], r["birth"]) for r in first} & {(r["id"], r["birth"]) for r in second}
        checks, changes, factors = Counter(), Counter(), Counter()
        for uid, birth in sorted(common):
            pair = db.execute(
                "SELECT a.name_check = b.name_check, a.ca, b.ca, a.pa, b.pa, a.candidate, b.candidate "
                "FROM player a JOIN ctrl.player b ON a.uid=b.uid AND a.birth=b.birth "
                "WHERE a.tag=? AND b.tag=? AND a.uid=? AND a.birth=?",
                (ret_tag, ctl_tag, uid, birth),
            ).fetchone()
            if pair is None or pair[0] != 1:
                continue
            checks["name_hash_also_equal"] += 1
            checks["equal_pa"] += pair[3] == pair[4]
            changes[pair[2]-pair[1]] += 1
            factors[pair[5], pair[6]] += 1
    return {
        "schema": "zubieta-youth-intake-cross-branch/v1",
        "retention_snapshot": {"date": day, "sha256": ret["source_sha256"]},
        "control_snapshot": {"date": ctl["game_date"], "sha256": ctl["source_sha256"]},
        "retention_candidates": len(first), "control_candidates": len(second),
        "ui_offer_entries": len(queue["entries"]), "uniquely_name_linked_offers": len(local),
        "same_day_terms_submitted": sum(r["offer_status"] == "TERMS_SUBMITTED" and r["offer_date"] == day for r in local),
        "ui_confirmed_future_start": sum(r["future_start_confirmed"] is True for r in local),
        "reader_without_future_spell_in_retention": sum(not r["future_spells"] for r in first),
        "reader_with_confirmed_contract_end_in_retention": sum(r["contract_end"] is not None for r in first),
        "unique_uid_birth_overlap": len(common), **checks,
        "control_ca_minus_retention_ca": dict(sorted(changes.items())),
        "progression_factor_pairs": [{"retention": a, "control": b, "n": n} for (a,b),n in sorted(factors.items())],
        "scope": "different dates and branches, no same-arm transition or causal effect",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("offers", "retention", "control", "retention_panel", "control_panel"):
        parser.add_argument(arg, type=Path)
    parser.add_argument("--local-link", type=Path)
    print(json.dumps(link(**vars(parser.parse_args())), indent=2))

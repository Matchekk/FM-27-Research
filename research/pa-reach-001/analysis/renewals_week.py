"""Follow the frozen March 31 contract cohorts to April 7 in the same retention arm."""

import argparse
from collections import Counter
from contextlib import closing
from datetime import date
import json
from pathlib import Path
import sqlite3

from facilities_and_pa import manifest
from immediate_renewals import compile_group, index, read, tag_name


BASE = "2027-03-31"
END = "2027-04-07"
TAGS = ("ZD-RET-MAR31-RENEWALS", "ZD-RET-APR07")


def spell_changed(old, new):
    return (new["contract_owner"] and new["contract_end"] and new["contract_start"]
            and (old["contract_end"] is None or old["contract_end"] < new["contract_end"])
            and new["contract_start"] != old["contract_start"])


def summarize(rows):
    result = compile_group([(row["a"], row["b"]) for row in rows])
    signed = Counter()
    for row in rows:
        a, b = row["a"][4], row["b"][4]
        if a == 0 or b == 0 or a is None or b is None:
            signed["zero_or_missing"] += 1
        else:
            signed["up" if b > a else "down" if b < a else "same"] += 1
    result["positive_factor_directions"] = {s: signed[s] for s in ("up", "down", "same", "zero_or_missing")}
    result["separate_april7_native_CA_PA"] = sum(r["native_end"] for r in rows)
    result["separate_march30_native_CA_PA_agree_with_march31"] = sum(r["native_prior"] for r in rows)
    result["april7_scan_agrees_with_contract_end"] = sum(r["agrees"] for r in rows)
    result["april7_current_spell_start_dates_for_observed_renewals_or_signings"] = dict(sorted(
        Counter(r["start"] for r in rows if r["start"]).items()))
    result["mar31_new_end_still_agrees_april7"] = sum(r["stable_new_end"] for r in rows)
    return result


def audit(panel, native, before, after, end, queue, intake):
    immediate = manifest("immediate-renewals.json")
    design = manifest("zubieta-retention-native-input.json")
    expected = [*immediate["save_hash_before_after"], design["snapshots"][END]["save_sha256"]]
    contracts = []
    for path, digest, day in zip((before, after, end), expected, (BASE, BASE, END), strict=True):
        ledger = read(path)
        if (ledger["source_sha256"], ledger["game_date"], ledger["build"]) != (
                digest, day, design["engine_build"]):
            raise ValueError("Unexpected contract source")
        contracts.append(index(ledger["members"], "id"))
    prior, immediate_contracts, final_contracts = contracts
    original = index(read(queue)["baseline_rows"], "player_id")
    youths = index(read(intake), "id")
    if original.keys() & youths.keys():
        raise ValueError("Overlapping groups")
    groups = {g: [] for g in ("due", "due_immediately_renewed", "due_without_immediate_renewal",
                              "later", "later_renewed_during_week", "later_without_observed_extension", "intake")}
    with closing(sqlite3.connect(panel.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        db.execute("ATTACH DATABASE ? AS native", (native.resolve().as_uri() + "?mode=ro",))
        for day, digest, tag in zip((BASE, END), expected[1:], TAGS, strict=True):
            meta = db.execute("SELECT game_date,sha256,build FROM capture WHERE tag=?", (tag,)).fetchone()
            if meta != (day, digest, design["engine_build"]):
                raise ValueError("Unexpected retention structural panel")
        for day, spec in design["snapshots"].items():
            meta = db.execute("SELECT save_hash,inventory_hash,build FROM native.snapshot WHERE day=? AND career=?",
                              (day, design["career_id"])).fetchone()
            if meta != (spec["save_sha256"], spec["native_sha256"], design["engine_build"]):
                raise ValueError("Unexpected independently measured native panel")
        for uid, person in (original | youths).items():
            first, last = immediate_contracts[uid], final_contracts[uid]
            if any(not ledger[uid]["stable"] or ledger[uid]["birth"] != person["birth"]
                   or tag_name(ledger[uid]["name"]) != tag_name(person["name"]) for ledger in contracts):
                raise ValueError("Unstable contract identity")
            a, b = [db.execute("SELECT birth,name_check,ca,pa,candidate FROM player WHERE tag=? AND uid=?",
                               (tag, uid)).fetchone() for tag in TAGS]
            if not a or not b or a[0] != person["birth"] or not a[1] or a[:2] != b[:2]:
                raise ValueError("Unresolved structural identity")
            n = [db.execute("""SELECT ca,pa FROM native.observation WHERE career=? AND day=?
                               AND uid=? AND birth=?""", (design["career_id"], day, uid, a[0])).fetchone()
                 for day in ("2027-03-30", END)]
            if n[1] != b[2:4] or last["scan_agrees_end"] is not True:
                raise ValueError("April 7 independent check failed")
            immediate_renewal = spell_changed(prior[uid], first) and first["contract_start"] == BASE
            week_start = spell_changed(first, last) and BASE < last["contract_start"] <= END
            row = dict(a=a, b=b, native_end=True, native_prior=n[0] == a[2:4], agrees=True,
                       stable_new_end=bool(immediate_renewal and first["contract_end"] == last["contract_end"]),
                       start=last["contract_start"] if week_start or immediate_renewal else None)
            if uid in youths:
                groups["intake"].append(row)
            elif person["due_by_june"]:
                groups["due"].append(row)
                groups["due_immediately_renewed" if immediate_renewal
                       else "due_without_immediate_renewal"].append(row)
            else:
                groups["later"].append(row)
                groups["later_renewed_during_week" if week_start else "later_without_observed_extension"].append(row)
    for key in ("due", "due_immediately_renewed", "later", "intake"):
        baseline_key = "due_with_later_end_and_new_same_day_start" if key == "due_immediately_renewed" else key
        if len(groups[key]) != immediate["groups"][baseline_key]["n"]:
            raise ValueError("Group size differs from same-day cohort")
    return dict(build=design["engine_build"], branch=design["career_id"], baseline=BASE, end=END,
                elapsed_days=(date.fromisoformat(END)-date.fromisoformat(BASE)).days,
                save_sha256=expected[1:], full_native_ability_inventory_on_march31=False,
                groups={k: summarize(rows) for k, rows in groups.items()})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("panel", "native", "before", "after", "end", "queue", "intake"):
        parser.add_argument(name, type=Path)
    print(json.dumps(audit(**vars(parser.parse_args())), indent=2))

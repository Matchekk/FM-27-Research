"""Paired end-state comparison for predefined club cohorts in two Zubieta branches."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sqlite3
from statistics import mean, median
from zubieta_readback import digest, iso_birth


def read(path):
    return json.loads(path.read_bytes())


def key(row):
    return row["id"], row["birth"]


def compare(baseline, intake, control, retention, control_panel, retention_panel,
            control_scout=None, control_save_panel=None, control_scout_sha=None):
    b, c, r = map(read, (baseline, control, retention))
    if c["game_date"] != r["game_date"] or c["game_date"] <= b["game_date"]:
        raise ValueError("Different or invalid outcome dates")
    if len({s["build"] for s in (b,c,r)}) != 1 or c["source_sha256"] == r["source_sha256"]:
        raise ValueError("Check branch build and distinct endpoint hashes")
    owned = [p for p in b["members"] if p["contract_owner"]]
    groups = {"due": [p for p in owned if p["expires_by_cutoff"] is True],
              "later": [p for p in owned if p["expires_by_cutoff"] is False],
              "intake": read(intake)}
    ids = [key(p) for g in groups.values() for p in g]
    if len(ids) != len(set(ids)) or len(groups["due"]) + len(groups["later"]) != len(owned):
        raise ValueError("Cohort overlap or unclassified contract expiry")

    def endpoint(inventory, db, career):
        with sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True) as con:
            source = con.execute("SELECT build,save_hash FROM snapshot WHERE career=? AND day=?",
                                 (career,inventory["game_date"])).fetchone()
            if source != (inventory["build"], inventory["source_sha256"]):
                raise ValueError("Native panel and contract inventory differ")
            root = con.execute("SELECT save_hash FROM snapshot WHERE career=? AND day=?",
                               (career, b["game_date"])).fetchone()
            if root != (b["source_sha256"],):
                raise ValueError("No common career baseline")
            select = "SELECT ca,pa,candidate FROM observation WHERE career=? AND day=? AND uid=? AND birth=?"
            obs = {k: con.execute(select,(career, inventory["game_date"], *k)).fetchone() for k in ids}
        counts = Counter(key(row) for row in inventory["members"] if row["stable"])
        ledger = {key(p):p for p in inventory["members"] if p["stable"] and counts[key(p)] == 1}
        return obs, ledger
    co, cl = endpoint(c, control_panel, "ZD-CONTROL-01")
    ro, rl = endpoint(r, retention_panel, "ZD-RETENTION-01")
    fallback_keys = set()
    if any(v is not None for v in (control_scout, control_save_panel, control_scout_sha)):
        if None in (control_scout, control_save_panel, control_scout_sha):
            raise ValueError("The alternative reader requires the dated scan, checksum and structural panel")
        if digest(control_scout) != control_scout_sha:
            raise ValueError("Control scan differs from bracketed input")
        wanted = {k for k in ids if co[k] is None}
        wanted_ids = {k[0] for k in wanted}
        players = [p for p in read(control_scout)["players"] if p["id"] in wanted_ids]
        multiplicity = Counter(p["id"] for p in players)
        with sqlite3.connect(control_save_panel.resolve().as_uri()+"?mode=ro",uri=True) as db:
            for profile in players:
                k = (profile["id"], iso_birth(profile))
                if k not in wanted or multiplicity[k[0]] != 1:
                    continue
                pair = db.execute("""SELECT p.ca,p.pa,p.candidate FROM player p JOIN capture h USING(tag)
                                     WHERE h.sha256=? AND h.game_date=? AND h.build=?
                                     AND p.uid=? AND p.birth=? AND length(p.name_check)>0""",
                                  (c["source_sha256"],c["game_date"],c["build"],*k)).fetchone()
                if pair and pair[:2] == (profile["ca"],profile["pa"]):
                    co[k] = pair
                    fallback_keys.add(k)
    results = {}
    for group, members in groups.items():
        values, matrix, missing, contracts = [], Counter(), Counter(), Counter()
        pa_same = 0
        for p in members:
            k = key(p)
            for label, lookup in (("control", cl), ("retention", rl)):
                v = lookup.get(k)
                if v is None or v["name"] != p["name"]:
                    contracts[label + "_club_record_unconfirmed"] += 1
                elif v["contract_owner"]:
                    contracts[label + "_club_held"] += 1
                    if v["scan_agrees_end"] is True:
                        contracts[label + "_fixed_end_confirmed"] += 1
            if any(v is not None and v["name"] != p["name"] for v in (cl.get(k),rl.get(k))):
                missing["name_disagreement"] += 1
                continue
            if co[k] is None or ro[k] is None:
                missing["identity_or_ability_not_confirmed_in_both_native_panels"] += 1
                continue
            ca, pa, factor = co[k]
            ca_ret, pa_ret, factor_ret = ro[k]
            values.append(ca_ret-ca)
            pa_same += pa_ret == pa
            matrix[f"{factor}->{factor_ret}"] += 1
        results[group] = {"baseline_n":len(members), "paired_n":len(values), "missing":missing,
                          "control_matched_via_alternative_scanner":sum(key(p) in fallback_keys for p in members),
                          "pa_equal":pa_same, "factor_pairs_control_to_retention":matrix,
                          "mean_ca_retention_minus_control":mean(values) if values else None,
                          "median_ca_retention_minus_control":median(values) if values else None,
                          "ca_difference_counts":dict(sorted(Counter(values).items())), "contracts":contracts}
    return {"schema":"pa-reach-club-branch-comparison/v1", "date":c["game_date"],
            "supplementary_control_scout_sha256":control_scout_sha,
            "save_hashes":[b["source_sha256"],c["source_sha256"],r["source_sha256"]],
            "independent_career_roots":1, "groups":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for entry in ("baseline","intake","control","retention","control_panel","retention_panel"):
        parser.add_argument(entry,type=Path)
    parser.add_argument("--control-scout",type=Path)
    parser.add_argument("--control-save-panel",type=Path)
    parser.add_argument("--control-scout-sha")
    print(json.dumps(compare(**vars(parser.parse_args())),indent=2))

"""Audit original FMSuperScout PA-Meta among exact subsequent baseline-PA matches."""

import argparse
from collections import Counter
from datetime import date
import json
import os
from pathlib import Path
import sqlite3
import subprocess

from observed_meta import KEYS, bracketed_scan
from player_endpoints import birthday_28
from prospective_ca61 import BRANCH, BUILD, metrics, sha


EARLY, LATE, NEXT = "2027-03-30", "2028-03-30", "2029-03-30"
ROOT = "ZD-ROOT-01"
FORK = "977ecefe623a3d4081871a0f558ab12d9bce850d"
HIDDEN = {"consistency", "important_matches", "versatility", "injury_proneness", "dirtiness"}


def read_snapshot(day, native, source, *, for_projection=False):
    panel, tag, scan, before, after = source
    tag, paths = str(tag), tuple(map(Path, (scan, before, after)))
    with sqlite3.connect(Path(panel).resolve().as_uri()+"?mode=ro", uri=True) as conn:
        dump, audit = bracketed_scan(conn, day, *paths, tag)
        conn.execute("ATTACH DATABASE ? AS n", (native.resolve().as_uri()+"?mode=ro",))
        career = ROOT if day == EARLY else BRANCH
        proof = conn.execute("SELECT build,save_hash,inventory_hash FROM n.snapshot WHERE career=? AND day=?",
                             (career, day)).fetchone()
        if not proof or proof[:2] != (BUILD, audit["hashes"]["loaded_copy"]):
            raise ValueError("Native inventory and loaded save differ")
        audit["hashes"]["native_inventory"] = proof[2]
        labels = json.loads(conn.execute("SELECT labels FROM field_order WHERE name='raw_attrs'").fetchone()[0])
        positions = json.loads(conn.execute("SELECT labels FROM field_order WHERE name='positions'").fetchone()[0])
        positions = ["ST" if label == "STC" else label for label in positions]
        visible = {("FreeKicks" if label=="free_kick_taking" else "".join(k.capitalize() for k in label.split("_"))): index
                   for index, label in enumerate(labels) if label not in HIDDEN}
        if len(visible) != 47 or not set(KEYS) <= visible.keys():
            raise ValueError("Displayed attribute map mismatch")
        indexes = visible if for_projection else {k: visible[k] for k in KEYS}
        freq = Counter(p["id"] for p in dump["players"])
        scan_players = {p["id"]: p for p in dump["players"] if freq[p["id"]] == 1}
        checked, eligible, ledger = {}, {}, Counter()
        for uid,birth,age,pos,ca,pa,name,raw,ratings in conn.execute("""
            SELECT p.uid,p.birth,p.age,p.pos,p.ca,p.pa,p.name_check,p.raw_attrs,p.positions
            FROM player p JOIN n.observation o USING(uid,birth,ca,pa)
            WHERE p.tag=? AND o.career=? AND o.day=? ORDER BY p.uid,p.birth
        """, (tag,career,day)):
            if for_projection and (age >= 28 or pos in (None,"","GK") or not 1 <= ca < pa <= 200):
                continue
            key = uid,birth
            eligible[key] = (ca,pa)
            p = scan_players.get(uid)
            dob = date.fromisoformat(birth)
            if not p or not name or (p["birthYear"],p["birthDoy"],p["ca"],p["pa"]) != (dob.year,dob.timetuple().tm_yday,ca,pa):
                ledger["scan_identity_or_ability_unverified"] += 1
                continue
            attrs = p["attrs"]
            if any(type(attrs.get(k)) is not int or not 1 <= attrs[k] <= 20 or attrs[k] != max(1,(raw[i]+2)//5)
                   for k,i in indexes.items()):
                ledger["attribute_unverified"] += 1
                continue
            ranked = sorted(zip(positions,ratings,strict=True),key=lambda value:-value[1])
            natural = [label for label, r in ranked if r>=max(15,ranked[0][1]-2)] or [ranked[0][0]]
            available = [label for label,r in ranked if r>=15] or natural
            if (set(p["posArr"]) != set(available) or set(p.get("posNat",p["posArr"])) != set(natural)
                    or p["pos"] != ", ".join(p["posArr"])):
                ledger["position_unverified"] += 1
                continue
            payload = {k:p[k] for k in ("birthYear", "birthDoy", "age", "ca", "pa", "pos", "posArr", "posNat", "attrs") if k in p}
            checked[key] = (bytes(name).hex(), payload)
        audit['accounting'] = {"eligible_native_and_save":len(eligible),"verified_inputs":len(checked),**ledger}
        meta = {k: dump["meta"][k] for k in ("game","gameDate","gameYear")}
    return eligible, checked, audit, [meta, {**meta, "gameDate":day, "gameYear":int(day[:4])}]


def app_scores(app, scorer, meta, players):
    script = Path(__file__).with_name("potential_meta_app.cjs")
    inp = "\n".join(map(json.dumps, (meta, *players)))+"\n"
    run = subprocess.run(["node", str(script), str(app), str(scorer)], input=inp, capture_output=True,
                         text=True, encoding="utf-8", check=True, env={**os.environ, "TZ":"Europe/Berlin"})
    return list(map(json.loads, run.stdout.splitlines()))


def freeze(day, native, source, app, scorer, output):
    target = LATE if day == EARLY else NEXT
    if day == LATE:
        with sqlite3.connect(native.resolve().as_uri()+"?mode=ro", uri=True) as conn:
            if conn.execute("SELECT 1 FROM snapshot WHERE career=? AND day>=?", (BRANCH,target)).fetchone():
                raise ValueError("Target already in baseline native panel")
    _, checked, audit, meta = read_snapshot(day,native,source,for_projection=True)
    scored = Counter()
    scores = app_scores(app,scorer,meta,[p for _,p in checked.values()])
    with output.open("x",encoding="utf-8",newline="\n") as out:
        for ((uid,birth),(name,p)), (header, exact) in zip(checked.items(), scores, strict=True):
            position, base, projection = header
            if position is None or base is None or projection is None:
                scored["unsupported_app_profile"] += 1
                continue
            if exact[:2] != header[:2] or exact[2] is None:
                raise ValueError("Unexpected dependence of current score on date")
            out.write(json.dumps([uid,birth,name,p["pa"],position,base,projection,exact[2]],separators=(",",":"))+"\n")
            scored["scored"] += 1
            scored["date_sensitivity_differs"] += projection != exact[2]
    return {"schema":"pa-reach-conditional-pa-meta-freeze/v1", "source":audit,"app_commit":FORK,
            "target":target,"forecast_sha256":sha(output),"scores":scored}


def compare(args, receipts):
    receipt = json.loads(receipts.read_bytes())
    if receipt["forecast_sha256"] != sha(args.forecasts) or receipt["app_commit"] != FORK or receipt["target"] != args.day:
        raise ValueError("Frozen baseline score receipt differs")
    day = receipt["source"]["controller_day"]
    eligible, end, audit, meta = read_snapshot(args.day,args.native,args.source)
    with sqlite3.connect(args.baseline_native.resolve().as_uri()+"?mode=ro", uri=True) as conn:
        career = ROOT if day == EARLY else BRANCH
        proof = conn.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",(career,day)).fetchone()
        if not proof or proof != (BUILD,receipt["source"]["hashes"]["loaded_copy"],receipt["source"]["hashes"]["native_inventory"]):
            raise ValueError("Unexpected baseline native source")
        baseline = {(uid,b):pa for uid,b,pa in conn.execute("""
            SELECT uid,birth,pa FROM observation WHERE career=? AND day=? AND age<28 AND position NOT IN ('GK','')
              AND ca>=1 AND ca<pa AND pa<=200
        """,(career,day))}
    hit = {key for key, pa in baseline.items() if key in eligible and eligible[key][0]==pa}
    target_day = date.fromisoformat(args.day)
    within_horizon = {k for k in hit if target_day <= birthday_28(date.fromisoformat(k[1]))}
    accepted, exclusions = [], Counter()
    with args.forecasts.open(encoding="utf-8") as forecasts:
        for u,b,name,pa,position,base,projection,corrected in map(json.loads,forecasts):
            key = u,b
            if key not in hit or baseline[key] != pa:
                continue
            if key not in end or end[key][0] != name:
                exclusions["followup_scan_or_name_unverified"] += 1
                continue
            accepted.append((end[key][1],position,base,projection,corrected,key in within_horizon))
    exclusions["baseline_app_input_or_structural_unverified"] = len(hit)-len(accepted)-exclusions["followup_scan_or_name_unverified"]
    errors = {mode: [] for mode in ("unchanged_baseline_meta","original_pa_meta","verified_date_pa_meta")}
    horizon_errors = {mode: [] for mode in errors}
    for (_,position,base,projection,corrected,in_horizon), (header,_) in zip(accepted, app_scores(args.app,args.scorer,meta,[a[0] for a in accepted]),strict=True):
        final_position, observed, _ = header
        if final_position != position or observed is None:
            exclusions["app_position_changed_or_unavailable"] += 1
            continue
        for mode, value in zip(errors,(base,projection,corrected),strict=True):
            errors[mode].append(value-observed)
            if in_horizon:
                horizon_errors[mode].append(value-observed)

    def summarize(samples):
        return {mode: {key.replace("_ca", "_meta"): value for key, value in metrics(data).items()}
                for mode, data in samples.items()}
    return {"schema":"pa-reach-conditional-pa-meta-compare/v1","app_commit":FORK,"baseline_receipt_sha256":sha(receipts),
            "source": audit,"baseline_native_eligible":len(baseline),"exact_pa_at_target":len(hit),
            "baseline_native_missing_followup":sum(k not in eligible for k in baseline),
            "selection_exclusions":exclusions,"scores":summarize(errors),
            "target_at_or_before_28th_birthday": {"exact_pa_at_target":len(within_horizon),
                                                  "scores":summarize(horizon_errors)},
            "independent_test_careers":0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="operation", required=True)
    for operation, dates in (("freeze",(EARLY,LATE)),("compare",(LATE,NEXT))):
        sub = commands.add_parser(operation)
        sub.add_argument("day",choices=dates)
        for flag in ("native","app","scorer","forecasts"):
            sub.add_argument(flag,type=Path)
        sub.add_argument("--source",nargs=5,required=True,metavar=("PANEL","TAG","SCAN","BEFORE","AFTER"))
        if operation=="compare":
            sub.add_argument("baseline_native",type=Path)
            sub.add_argument("receipt",type=Path)
    args = parser.parse_args()
    result = (freeze(args.day,args.native,args.source,args.app,args.scorer,args.forecasts)
              if args.operation=="freeze" else compare(args,args.receipt))
    print(json.dumps(result,indent=2,sort_keys=True))

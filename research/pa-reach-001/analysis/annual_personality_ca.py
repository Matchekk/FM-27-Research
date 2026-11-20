"""Fit nested year-one point-CA models, freeze year-two predictions, then score them."""
import argparse
from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path
import sqlite3

import numpy as np

from observed_meta import bracketed_scan
from player_endpoints import birthday_28
from prospective_ca61 import BRANCH, BUILD, metrics, sha


EARLY, MIDDLE, END = "2027-03-30", "2028-03-30", "2029-03-30"
POSITIONS = "AMC AML AMR DC DL DM DR MC ML MR STC WBL WBR".split()
FIELDS = ["professionalism", "ambition", "determination", "natural_fitness", "injury_proneness"]
CELLS = [f"{a}/{g}" for a in ("U18","18-20","21-23","24-27") for g in ("0-10","11-30",">30")]


def panel_rows(native, spec, day, target=None):
    """Only the origins need personality observations. End points need identity and real CA."""
    panel, tag = spec[:2]
    db = sqlite3.connect(Path(panel).resolve().as_uri()+"?mode=ro", uri=True)
    try:
        db.execute("ATTACH DATABASE ? AS n", (native.resolve().as_uri()+"?mode=ro",))
        proof = db.execute("""SELECT c.sha256,s.inventory_hash FROM capture c JOIN n.snapshot s
            ON c.sha256=s.save_hash AND c.build=s.build AND c.game_date=s.day
            WHERE c.tag=? AND c.build=? AND s.career=? AND s.day=?""", (tag,BUILD,BRANCH,day)).fetchone()
        if proof is None:
            raise ValueError("Native reference and structural save must match on the exact day")
        audit = {"day":day, "save_sha256":proof[0], "native_sha256":proof[1]}
        profiles = {}
        if target:
            dump, scan_audit = bracketed_scan(db, day, *map(Path,spec[2:]), tag)
            players = dump.pop("players")
            freq = Counter(p["id"] for p in players)
            profiles = {p["id"]:p for p in players if freq[p["id"]]==1}
            audit["scout"] = scan_audit
        accepted, counts = {}, Counter()
        for uid,birth,name,age,pos,ca,pa,native_pos,*traits in db.execute("""
            SELECT p.uid,p.birth,p.name_check,p.age,p.pos,p.ca,p.pa,o.position,
                p.professionalism,p.ambition,p.determination,p.natural_fitness,p.injury_proneness
            FROM player p JOIN n.observation o USING(uid,birth,ca,pa)
            WHERE p.tag=? AND o.career=? AND o.day=? ORDER BY p.uid""", (tag,BRANCH,day)):
            if not name or not (1<=ca<=200 and 1<=pa<=200):
                continue
            key = (uid,birth,bytes(name).hex())
            if not target:
                accepted[key] = (ca,pa)
                continue
            dob = date.fromisoformat(birth)
            start = date.fromisoformat(day)
            real_age = start.year-dob.year-((start.month,start.day)<(dob.month,dob.day))
            if pos not in POSITIONS or age!=real_age or age>=28 or date.fromisoformat(target)>birthday_28(dob) or ca>pa:
                continue
            counts["eligible_in_native_and_save"] += 1
            if native_pos!=pos:
                counts["position_mismatch"] += 1
                continue
            p = profiles.get(uid)
            if not p or (p["birthYear"],p["birthDoy"],p["ca"],p["pa"])!=(dob.year,dob.timetuple().tm_yday,ca,pa):
                counts["scout_identity_or_ability_missing"] += 1
                continue
            seen = [p.get("professionalism"),p.get("ambition"),*(p["attrs"].get(k) for k in
                    ("Determination","NaturalFitness","InjuryProneness"))]
            if traits!=seen or any(type(x)!=int or not 1<=x<=20 for x in seen):
                counts["personality_or_attribute_unverified"] += 1
                continue
            gap = pa-ca
            band = "U18" if age<18 else "18-20" if age<21 else "21-23" if age<24 else "24-27"
            group = band+"/"+("0-10" if gap<=10 else "11-30" if gap<=30 else ">30")
            x = [int(k==group) for k in CELLS] + [age-20,gap,ca]+[int(k==pos) for k in POSITIONS[1:]]
            z = [t-10 for t in traits] + [(age-20)*(traits[0]-10)]
            accepted[key] = (ca,pa,group,x,z)
        counts["accepted"] = len(accepted)
        audit["accounting"] = counts
        return accepted, audit
    finally:
        db.close()


def freeze(native, early, middle, output):
    with sqlite3.connect(native.resolve().as_uri()+"?mode=ro",uri=True) as db:
        if db.execute("SELECT 1 FROM snapshot WHERE career=? AND day>=?", (BRANCH,END)).fetchone():
            raise ValueError("Outcome already available")
    train, a = panel_rows(native, early, EARLY, MIDDLE)
    outcomes, b = panel_rows(native, middle[:2], MIDDLE)
    forecast, c = panel_rows(native, middle, MIDDLE, END)
    matched = sorted(train.keys() & outcomes.keys())
    y = [outcomes[k][0]-train[k][0] for k in matched]
    fitted = []
    for extra in (False,True):
        matrix = [train[k][3]+(train[k][4] if extra else []) for k in matched]
        coef,_,rank,_ = np.linalg.lstsq(matrix,y,rcond=None)
        if rank!=len(coef):
            raise ValueError("Design matrix has incomplete rank")
        fitted.append(coef)
    with output.open("x",encoding="utf-8",newline="\n") as f:
        in_train = set(matched)
        for k,(ca,pa,group,x,z) in sorted(forecast.items()):
            preds = [float(np.clip(ca+np.dot(v,coef),1,200)) for v,coef in zip((x,x+z),fitted,strict=True)]
            row = [*k,ca,pa,group,k in in_train,*preds]
            f.write(json.dumps(row,separators=(",",":"))+"\n")
    labels = CELLS+["age_minus_20","gap","baseline_ca"]+POSITIONS[1:]
    return {"schema":"pa-reach-annual-personality-freeze/v1","root_count":1,"independent_test_roots":0,
            "outcome_seen":False,"target":END,"sources":[a,b,c],"training_pairs":len(y),
            "training_missing":len(train)-len(y),"training_changed_pa":sum(train[k][1]!=outcomes[k][1] for k in matched),
            "frozen":len(forecast),"present_in_fitted_training_pairs":len(in_train & forecast.keys()),
            "file_sha256":sha(output),"coefficients":[dict(zip(names,map(float,coef),strict=True)) for
                names,coef in zip((labels,labels+FIELDS+["age_x_professionalism"]),fitted,strict=True)]}


def score(native, end, predictions, receipt):
    audit = json.loads(receipt.read_bytes())
    if audit["file_sha256"]!=sha(predictions) or audit["target"]!=END:
        raise ValueError("Frozen forecast receipt mismatch")
    outcomes, source = panel_rows(native, end, END)
    counts, errors = defaultdict(Counter),defaultdict(lambda:defaultdict(list))
    with predictions.open(encoding="utf-8") as f:
        for line in f:
            uid,birth,name,ca,pa,cell,previous,basic,extended = json.loads(line)
            observed = outcomes.get((uid,birth,name))
            for g in ("all",cell,"seen_in_fit" if previous else "unseen_in_fit"):
                counts[g]["frozen"] += 1
                if observed is None:
                    counts[g]["missing"] += 1
                    continue
                counts[g]["observed"] += 1
                counts[g]["changed_pa"] += observed[1]!=pa
                for label,pred in (("constant",ca),("basic",basic),("extended",extended)):
                    errors[g][label].append(pred-observed[0])
    if counts["all"]["frozen"]!=audit["frozen"]:
        raise ValueError("Forecast count mismatch")
    return {"schema":"pa-reach-annual-personality-score/v1","target":END,"forecast_sha256":audit["file_sha256"],
            "outcome_source":source,"groups":{g:{"counts":counts[g],"metrics":{k:metrics(v) for k,v in errors[g].items()}}
            for g in counts},"independent_test_roots":0}


if __name__ == "__main__":
    command = argparse.ArgumentParser(description=__doc__)
    modes = command.add_subparsers(dest="mode",required=True)
    fit, test = modes.add_parser("freeze"),modes.add_parser("score")
    for mode in (fit,test):
        mode.add_argument("native",type=Path)
    for name in ("early","middle"):
        fit.add_argument(name,nargs=5,metavar="SOURCE",help="panel tag scan before after")
    fit.add_argument("output",type=Path)
    test.add_argument("end",nargs=2,metavar="SOURCE",help="panel tag")
    test.add_argument("predictions",type=Path)
    test.add_argument("receipt",type=Path)
    args = vars(command.parse_args())
    method = freeze if args.pop("mode")=="freeze" else score
    print(json.dumps(method(**args),indent=2,allow_nan=False))

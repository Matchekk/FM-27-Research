"""Freeze private 61-day point forecasts before observing June, then score the frozen file."""
import argparse
from collections import Counter, defaultdict
from hashlib import file_digest
import json
from math import sqrt
from pathlib import Path
import sqlite3


MARCH, APRIL, JUNE = "2027-03-30", "2027-04-30", "2027-06-30"
BRANCH = "ZD-RETENTION-01"
BUILD = "27.1.0+2505117"
MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"


def sha(path):
    with path.open("rb") as f:
        return file_digest(f, "sha256").hexdigest()


def freeze(db, private_output):
    source = json.loads((MANIFESTS / "zubieta-retention-native-input-0430.json").read_bytes())
    for date in (MARCH, APRIL):
        item = source["snapshots"][date]
        row = db.execute("SELECT save_hash,inventory_hash,build FROM snapshot WHERE day=? AND career=?",
                         (date, BRANCH)).fetchone()
        if row != (item["save_sha256"],item["native_sha256"],BUILD):
            raise ValueError("Baseline input differs from the declared sources")
    if db.execute("SELECT 1 FROM snapshot WHERE career=? AND day>=?",(BRANCH,JUNE)).fetchone():
        raise ValueError("Outcome already present in this store")
    rows = db.execute("""
        SELECT a.uid,a.birth,a.age,a.pa-a.ca,a.ca,m.ca
        FROM observation a JOIN observation m USING(career,uid,birth)
        WHERE a.career=? AND a.day=? AND m.day=? AND a.age<28 AND a.position<>'GK'
        ORDER BY a.uid,a.birth
        """, (BRANCH, APRIL, MARCH))
    count = Counter()
    with private_output.open("x",encoding="utf-8",newline="\n") as out:
        for uid,birth,age,gap,ca,previous in rows:
            group = "other"
            if gap > 30 and age < 18:
                group = "under18_gap_gt30"
            if gap > 30 and age >= 24:
                group = "age24_27_gap_gt30"
            count[group] += 1
            trend = max(31,min(6200,ca*31 + 61*(ca-previous)))
            out.write(json.dumps([uid,birth,group,ca,trend],separators=(",",":"))+"\n")
    return {"schema":"pa-reach-frozen-ca61/v1", "career":BRANCH, "engine_build":BUILD,
            "origin":APRIL, "target":JUNE, "previous":MARCH, "fixed_rule_trend_denominator":31,
            "predictor_sources":{d:source["snapshots"][d] for d in (MARCH,APRIL)},
            "prediction_file_sha256":sha(private_output), "counts":count, "total":sum(count.values()),
            "outcome_seen_at_freeze":False, "training_career_count":0, "independent_test_careers":0}


def score(db, private_forecasts, receipt):
    saved = json.loads(receipt.read_bytes())
    if saved["prediction_file_sha256"] != sha(private_forecasts) or saved["target"] != JUNE:
        raise ValueError("Forecast receipt mismatch")
    source = db.execute("SELECT build,save_hash,inventory_hash FROM snapshot WHERE career=? AND day=?",
                        (BRANCH,JUNE)).fetchone()
    if not source or source[0] != BUILD:
        raise ValueError("Exact verified June checkpoint required")
    actual = {(u,b):v for u,b,v in db.execute("SELECT uid,birth,ca FROM observation WHERE career=? AND day=?",
                                              (BRANCH,JUNE))}
    counts, errors = defaultdict(Counter), defaultdict(lambda: defaultdict(list))
    with private_forecasts.open(encoding="utf-8") as f:
        for line in f:
            uid,birth,group,ca,trend_num = json.loads(line)
            observed = actual.get((uid,birth))
            for g in ("all",group):
                counts[g]["frozen"] += 1
                if observed is None:
                    counts[g]["missing"] += 1
                    continue
                counts[g]["observed"] += 1
                errors[g]["carry_forward"].append(ca-observed)
                errors[g]["previous_rate"].append(trend_num/31-observed)
    if counts["all"]["frozen"] != saved["total"]:
        raise ValueError("Frozen cohort size differs")
    def metrics(v):
        n = len(v)
        return dict(n=n,mae_ca=sum(map(abs,v))/n,rmse_ca=sqrt(sum(x*x for x in v)/n),bias_ca=sum(v)/n)
    return {"schema":"pa-reach-scored-ca61/v1", "receipt_sha256":sha(receipt), "target":JUNE,
            "save_sha256":source[1], "native_sha256":source[2], "accounting":counts,
            "metrics":{g:{m:metrics(v) for m,v in pairs.items()} for g,pairs in errors.items()},
            "career_origins":1, "independent_test_careers":0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="operation",required=True)
    for task in ("freeze","score"):
        command = sub.add_parser(task)
        command.add_argument("native_panel",type=Path)
        command.add_argument("private_file",type=Path)
        if task == "score":
            command.add_argument("receipt",type=Path)
    args=parser.parse_args()
    with sqlite3.connect(args.native_panel.resolve().as_uri()+"?mode=ro",uri=True) as conn:
        result=(freeze(conn,args.private_file) if args.operation=="freeze"
                else score(conn,args.private_file,args.receipt))
        print(json.dumps(result,indent=2,sort_keys=True))

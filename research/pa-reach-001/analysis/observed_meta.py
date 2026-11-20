"""Check dated full scanner dumps against private structural saves before scoring."""
import argparse
from collections import Counter
from datetime import date
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess


KEYS = ("Acceleration", "Pace", "JumpingReach", "Stamina", "Anticipation",
        "Balance", "Strength", "Finishing", "Concentration", "Dribbling")
TAGS = {"2027-01-31":"ZD-HIST-02", "2027-03-30":"ZD-ROOT-01", "2027-04-30":"ZD-CONTROL-APR"}


def read_scan(conn, day, scan, before, after, *, tag=None, exclusions=None):
    tag = tag or TAGS[day]
    context = []
    public_hashes = {}
    for label, path in (("before",before),("after",after)):
        raw = path.read_bytes()
        check = json.loads(raw)
        item = check["Response"]
        if (check["Status"] != "completed" or item["Date"] != day or
                any(str(item[k]).lower() != "false" for k in ("Saving","Processing","IsDuringMatch"))):
            raise ValueError("Controller date or state mismatch")
        context.append((check["Pid"],item["LastSavePath"],item["ManagerIdentity"],item["TeamIdentity"]))
        public_hashes[label] = hashlib.sha256(raw).hexdigest()
    if context[0] != context[1] or not before.stat().st_mtime <= scan.stat().st_mtime <= after.stat().st_mtime:
        raise ValueError("Scanner not bracketed by consistent controller state")
    source = conn.execute("SELECT build,game_date,sha256 FROM capture WHERE tag=?", (tag,)).fetchone()
    with Path(context[0][1]).open("rb") as stream:
        public_hashes["loaded_copy"] = hashlib.file_digest(stream, "sha256").hexdigest()
    if source != ("27.1.0+2505117",day,public_hashes["loaded_copy"]):
        raise ValueError("Unexpected loaded copy, date or build")
    with scan.open("rb") as stream:
        public_hashes["dump"] = hashlib.file_digest(stream,"sha256").hexdigest()
    dump = json.loads(scan.read_bytes())
    meta = dump["meta"]
    if meta["game"] != "FM27" or meta["versionOk"] is not True:
        raise ValueError("Scanner rejected game version")
    fields = json.loads(conn.execute("SELECT labels FROM field_order WHERE name='raw_attrs'").fetchone()[0])
    position_codes = json.loads(conn.execute("SELECT labels FROM field_order WHERE name='positions'").fetchone()[0])
    position_codes = ["ST" if code=="STC" else code for code in position_codes]
    indices = [fields.index("jumping_reach" if k == "JumpingReach" else k.lower()) for k in KEYS]
    freq = Counter(p["id"] for p in dump["players"])
    players = {p["id"]:p for p in dump["players"] if freq[p["id"]] == 1}
    accepted = {}
    ledger = Counter()
    def reject(reason, uid, birth):
        ledger[reason] += 1
        if exclusions is not None:
            exclusions[uid,birth] = reason

    for uid,birth,age,pos,ca,pa,names,raw,ratings in conn.execute(
            "SELECT uid,birth,age,pos,ca,pa,name_check,raw_attrs,positions FROM player WHERE tag=?", (tag,)):
        p = players.get(uid)
        dt = date.fromisoformat(birth)
        if not p or (p["birthYear"],p["birthDoy"]) != (dt.year,dt.timetuple().tm_yday) or (p["ca"],p["pa"]) != (ca,pa):
            reject("unmatched_identity_or_ability",uid,birth)
            continue
        if not names:
            reject("missing_name_check",uid,birth)
            continue
        attrs = {k:p["attrs"].get(k) for k in KEYS}
        # The score accepts displayed 1..20 inputs. A scanner zero is missing for this purpose.
        if any(not isinstance(x,int) or not 1 <= x <= 20 for x in attrs.values()):
            reject("invalid_scanner_attribute",uid,birth)
            continue
        if any(attrs[k] != max(1,(raw[i]+2)//5) for k,i in zip(KEYS,indices,strict=True)):
            reject("attribute_disagreement",uid,birth)
            continue
        ranked = sorted(zip(position_codes,ratings,strict=True), key=lambda x:-x[1])
        natural = [code for code,rating in ranked if rating>=max(15,ranked[0][1]-2)] or [ranked[0][0]]
        selected = [code for code,rating in ranked if rating>=15] or natural
        if (set(selected) != set(p["posArr"]) or set(natural) != set(p.get("posNat",p["posArr"]))
                or p["pos"] != ", ".join(p["posArr"])):
            reject("position_disagreement",uid,birth)
            continue
        record = {k:p[k] for k in ("pos", "posArr", "posNat") if k in p}
        record["attrs"] = attrs
        accepted[uid,birth,names] = (age,pos,ca,record)
        ledger["accepted_inputs_all_ages_positions"] += 1
    return accepted, {"controller_day":day,"scanner_reported_day":meta["gameDate"],
                      "scanner_version":meta["pluginVersion"],"hashes":public_hashes,"accounting":dict(ledger)}


def score_pairs(start, end, model, *, extended=False):
    eligible = [k for k,(age,pos,_,_) in start.items() if age<28 and pos and pos!="GK"]
    js = Path(__file__).with_suffix(".cjs")
    command = ["node", str(js), str(model)]
    if extended:
        command.append("--with-ca")
    with subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                          text=True,encoding="utf-8") as child:
        for k in eligible:
            if k in end:
                child.stdin.write(json.dumps([start[k][3],end[k][3],end[k][2]-start[k][2]])+"\n")
        child.stdin.close()
        result = child.stdout.read()
        if child.wait() != 0:
            raise RuntimeError("Pinned scorer failed")
    return {"eligible_at_baseline_after_input_checks":len(eligible),
            "missing_followup_identity_or_attributes":sum(k not in end for k in eligible),
            "meta_delta":json.loads(result),"status":"OBSERVED_PAIRED_INDEX_NOT_PEAK_FORECAST"}


def run(args):
    cohort, audits, intervals = {}, {}, {}
    for day, name in zip(TAGS,("january","march","april"),strict=True):
        inputs = getattr(args,name)
        if inputs:
            panel = args.april_panel if name=="april" else args.panel
            if panel is None:
                raise ValueError("April capture requires the pilot panel")
            with sqlite3.connect(panel.resolve().as_uri()+"?mode=ro",uri=True) as conn:
                cohort[day], audits[day] = read_scan(conn,day,*inputs)
    for first,last in zip(TAGS, list(TAGS)[1:]):
        key = first + "_to_" + last
        intervals[key] = (score_pairs(cohort[first],cohort[last],args.model) if first in cohort and last in cohort
                          else {"meta_delta":None,"status":"MISSING_SECOND_VERIFIED_ATTRIBUTE_SNAPSHOT"})
    return {"snapshots":audits,"intervals":intervals}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("panel",type=Path)
    parser.add_argument("model",type=Path)
    parser.add_argument("--april-panel",type=Path)
    for option in ("january","march","april"):
        parser.add_argument("--"+option,nargs=3,metavar=("SCAN","BEFORE","AFTER"),type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args),indent=2))

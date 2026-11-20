"""Dated contract-chain evidence and byte changes. Private inputs, aggregate output only."""
import argparse
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import random
import sqlite3
from statistics import quantiles
import struct

DAYS = ("2027-01-31", "2027-03-30", "2027-04-30")
BUILD = "27.1.0+2505117"
MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def source_rows(conn, day, save_hash):
    reference = list(conn.execute(
        "SELECT career FROM snapshot WHERE day=? AND build=? AND save_hash=?", (day,BUILD,save_hash)))
    if len(reference) != 1:
        raise ValueError("Ambiguous native series or unbound save")
    return {uid:(birth,ca,pa,club,candidate) for uid,birth,ca,pa,club,candidate in conn.execute(
        "SELECT uid,birth,ca,pa,club,candidate FROM observation WHERE career=? AND day=?",
        (reference[0][0],day))}


def scout_ends(path, reference):
    import ijson
    from zubieta_readback import iso_birth
    ends = {}
    seen = set()
    with path.open("rb") as stream:
        for p in ijson.items(stream,"players.item"):
            uid = p["id"]
            row = reference.get(uid)
            if row is None or row[3] is None:
                continue
            if uid in seen:
                ends.pop(uid,None)
                continue
            seen.add(uid)
            if (iso_birth(p),p["ca"],p["pa"]) == row[:3]:
                ends[uid] = p.get("expires")
    return ends


def read_day(day, source, scout, native, audit):
    import fmsave
    from fmsave._layouts import ContractLayout, PersonBlockLayout, find_layout
    from fmsave.readers.player_scan import window_end
    from fmsave.readers.players import build_player_decoder
    evidence = audit["snapshots"][day]["hashes"]
    if digest(source)!=evidence["loaded_copy"] or digest(scout)!=evidence["dump"]:
        raise ValueError("Input hash mismatch")
    with sqlite3.connect(native.resolve().as_uri()+"?mode=ro",uri=True) as conn:
        reference = source_rows(conn, day, evidence["loaded_copy"])
    scan_end = scout_ends(scout,reference)
    out = {}
    with fmsave.open(source) as s:
        if str(s.info.game_date)!=day or s.info.build!=BUILD or s.info.section_schemas["game_db"]!=4000:
            raise ValueError("Unexpected date, build or schema")
        ctx = s._context
        with ctx.section("game_db") as db:
            rec = ctx.player_records()
            d = build_player_decoder(rec.layout, ctx.club_index(), ctx.name_pools(), s.info.game_date,
                find_layout(PersonBlockLayout,"game_db",4000,BUILD).layout,
                find_layout(ContractLayout,"game_db",4000,BUILD).layout, s.info.file_name)
            for i,offset in enumerate(rec.record_offsets):
                end = window_end(rec,i,len(db))
                last = i == len(rec.record_offsets)-1
                opening = rec.uids[i]
                ix = rec.pindexes[i]
                closing = d.closing_header(db,offset,end,ix,opening,is_last_record=last,
                                           next_record_ambiguous=i+1 in rec.ambiguous_positions)
                if closing is None or closing.uid not in reference:
                    continue
                uid = closing.uid
                birth,ca,pa,club,tier = reference[uid]
                if club is None:
                    continue
                t, = struct.unpack_from("<I",db,offset+rec.layout.team_id_offset)
                team = d.team_fields.get(t)
                if not team or team[0]!=club:
                    continue
                c,loan,*_ = d.contract_decoder.decode(db,offset,end,last,ix,opening,None,club,
                    registration_missing=False,object_end=closing.offset)
                status = "no_current_terms"
                start = finish = None
                future = ()
                if c and c.club_uid==club and c.start and c.end:
                    start,finish = c.start.isoformat(),c.end.isoformat()
                    future = tuple((e.start.isoformat(),e.end.isoformat()) for e in c.chain
                                   if e.has_terms and e.club_uid==club and e.start and e.end
                                   and e.start.isoformat()>day)
                    terms = [e for e in c.chain if e.has_terms and e.club_uid==club and
                             (e.start,e.end)==(c.start,c.end)]
                    if loan is not False:
                        status = "loan_or_unresolved_loan"
                    elif c.end_source.value!="contract" or len(terms)!=1:
                        status = "terms_or_owner_ambiguous"
                    elif not start <= day <= finish:
                        status = "outside_effective_dates"
                    elif scan_end.get(uid)!=finish:
                        status = "end_not_independently_confirmed"
                    else:
                        status = "readable"
                out[uid,birth] = (club,tier,status,start,finish,future)
    return reference,out


def classify(a,b,first,last):
    if "readable" != a[2] or "readable" != b[2]:
        return "contract_evidence_missing"
    if first < b[3] <= last and b[4] > a[4]:
        return "new_chain_start_and_later_confirmed_end"
    if a[3]==b[3] and a[4]==b[4]:
        return "no_detected_change_in_current_terms"
    return "other_contract_date_change"


def change(before,after):
    if before==0 or after==0:
        return f"zero_{before}_to_{after}"
    if before not in range(1,6) or after not in range(1,6):
        return "outside_range"
    return "higher" if after>before else "lower" if after<before else "unchanged"


def standardized_contrast(strata):
    """Use each eligible exposed player's club and baseline byte to weight controls."""
    by_club = defaultdict(lambda: [0,0,0.0])
    for (club,_),counts in strata.items():
        ne, ce, nc, cc = counts
        if not ne or not nc:
            continue
        block = by_club[club]
        block[0] += ne
        block[1] += ce
        block[2] += ne*cc/nc
    if not by_club:
        return None
    blocks = [by_club[k] for k in sorted(by_club)]
    n,total,expected = map(sum,zip(*blocks,strict=True))
    rng = random.Random(60419)
    differences = []
    for _ in range(1999):
        sample = rng.choices(blocks,k=len(blocks))
        nj,ej,cj = map(sum,zip(*sample,strict=True))
        differences.append((ej-cj)/nj)
    percentiles = quantiles(differences,n=1000,method="inclusive")
    return {"clubs":len(blocks),"exposed_on_common_support":n,"exposed_changed":total,
            "control_change_fraction_weighted_to_exposed":expected/n,
            "change_fraction_difference":(total-expected)/n,
            "within_career_club_bootstrap_95ci":[percentiles[24],percentiles[974]],
            "career_cluster_95ci":None}


def interval(first, last, ref1, ref2, a, b):
    one = {(uid,r[0]) for uid,r in ref1.items()}
    two = {(uid,r[0]) for uid,r in ref2.items()}
    pairs = one & two
    common = a.keys() & b.keys()
    data = [(a[k][0], classify(a[k],b[k],first,last), change(a[k][1],b[k][1]))
            for k in common if a[k][0] == b[k][0]]
    events = {club for club,status,_ in data if status=="new_chain_start_and_later_confirmed_end"}
    by_group = defaultdict(Counter)
    matched_club = defaultdict(Counter)
    previously_future = Counter()
    still_only_future = Counter()
    strata = defaultdict(lambda:[0,0,0,0])
    for k in common:
        if a[k][0] != b[k][0]:
            continue
        status = classify(a[k],b[k],first,last)
        if a[k][1] in range(1,6) and b[k][1] in range(1,6):
            group = {"new_chain_start_and_later_confirmed_end":0,
                     "no_detected_change_in_current_terms":2}.get(status)
            if group is not None:
                s = strata[a[k][0],a[k][1]]
                s[group] += 1
                s[group+1] += a[k][1] != b[k][1]
        if status=="new_chain_start_and_later_confirmed_end" and (b[k][3],b[k][4]) in a[k][5]:
            previously_future[change(a[k][1],b[k][1])] += 1
        if status=="no_detected_change_in_current_terms" and any(
                c not in a[k][5] for c in b[k][5]):
            still_only_future[change(a[k][1],b[k][1])] += 1
    for club,status,transition in data:
        by_group[status][transition] += 1
        if club in events:
            matched_club[status][transition] += 1
    return {"start":first,"end":last,"days":(date.fromisoformat(last)-date.fromisoformat(first)).days,
            "identities_matched_native_ca_pa":len(pairs), "missing_club_or_record_at_either_date":len(pairs)-len(common),
            "different_clubs":len(common)-len(data), "same_club":len(data),
            "event_clubs":len(events),"all_same_club_groups":by_group, "within_event_clubs":matched_club,
            "descriptive_contrast_same_club_and_baseline_byte":standardized_contrast(strata),
            "subset_exposed_already_future_terms_at_baseline":previously_future,
            "subset_unchanged_terms_with_new_future_spells":still_only_future}


if __name__=="__main__":
    import fmsave
    import ijson
    parser=argparse.ArgumentParser(description=__doc__)
    for opt in ("january","march","april"):
        parser.add_argument("--"+opt,required=True,nargs=3,type=Path,metavar=("SAVE","SCOUT","NATIVE_PANEL"))
    args=parser.parse_args()
    if fmsave.__version__!="0.14.1":
        raise ValueError("Wrong fmsave version")
    audit=json.loads((MANIFESTS/"observed-meta.json").read_bytes())
    result={"build":BUILD,"reader":fmsave.__version__,"ijson":ijson.__version__,
            "career_clusters":1,"per_date_contract_status":{}, "intervals":[]}
    previous=None
    for day,choice in zip(DAYS,("january","march","april"),strict=True):
        current=read_day(day,*getattr(args,choice),audit)
        result["per_date_contract_status"][day]=Counter(r[2] for r in current[1].values())
        if previous:
            oldday,(ref,rows)=previous
            result["intervals"].append(interval(oldday,day,ref,current[0],rows,current[1]))
        previous=day,current
    print(json.dumps(result,indent=2))

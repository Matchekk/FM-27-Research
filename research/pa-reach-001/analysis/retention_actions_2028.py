"""Reconcile the 2028 youth offers and annual requests against the private club census."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

from prospective_ca61 import BUILD, sha


def reconcile(census, actions, offers, previous):
    baseline = json.loads(census.read_bytes())
    if (baseline["game_date"],baseline["build"])!=("2028-04-05",BUILD):
        raise ValueError("Unexpected annual census date or build")
    roster = {(r["id"],r["birth"]):r for r in baseline["members"] if r.get("contract_owner")}
    intake = {k for k,r in roster.items() if r["contract_start"]=="2028-03-31" and r["contract_end"] is None}
    old = {k for k in roster if k not in intake}
    exempt = {(r["player_id"],r["birth"]) for r in json.loads(previous.read_bytes())} & old
    youth = json.loads(offers.read_bytes())
    if {(r["uid"],r["birth"]) for r in youth}!=intake or len(youth)!=len(intake) or any(
            r["status"]!="TERMS_SUBMITTED" or r["offer_date"]!="2028-04-05" for r in youth):
        raise ValueError("Intake census and submitted offer receipts differ")
    history = defaultdict(list)
    for line in actions.read_text(encoding="utf8").splitlines():
        r = json.loads(line)
        k = r["player_id"],r["birth"]
        if k not in old or r["day"] not in ("2028-03-05","2028-04-05"):
            raise ValueError("Unexpected incumbent identity or action date")
        history[k].append(r["status"])
    if any(h.count("ATTEMPT_STARTED")>1 for h in history.values()):
        raise ValueError("Repeated contract attempt")
    if any(h!=["PREVIOUSLY_UNRESOLVED_NO_RETRY"] for k,h in history.items() if k in exempt):
        raise ValueError("Action recorded on an exempt player")
    counts = Counter(history[k][-1] if k in history else "UNTOUCHED" for k in old)
    due = {k for k in old if roster[k].get("contract_end") and roster[k]["contract_end"]<="2028-06-30"}
    return {"schema":"pa-reach-annual-contract-actions/v1","census_date":"2028-04-05","build":BUILD,
            "owned_incumbents":len(old),"intake_offers_submitted":len(youth),"last_ledger_status":counts,
            "expiring_by_june":len(due),"expiring_legacy_exempt":len(due & exempt),
            "expiring_untouched_outside_exempt":len(due-exempt-history.keys()),"legacy_exempt":len(exempt),
            "identities_with_repeated_started_attempt":0,"contract_signature_outcome":None,
            "source_sha256":{k:sha(f) for k,f in (("census",census),("actions",actions),("offers",offers),("exemption_list",previous))}}


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("census","actions","offers","previous"):
        parser.add_argument(name,type=Path)
    print(json.dumps(reconcile(**vars(parser.parse_args())),indent=2,sort_keys=True))

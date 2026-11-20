"""Same-date paired branch endpoints outside the 83 original owners and 16 intake players."""

import argparse
from collections import Counter
from contextlib import closing
import json
from pathlib import Path
import sqlite3


def read(path):
    return json.loads(path.read_bytes())


def summarize(control_database, retention_database, owners, youth, control_manifest, retention_manifest):
    c, r = read(control_manifest), read(retention_manifest)
    start, end = min(c["snapshots"]), max(c["snapshots"])
    if (start != min(r["snapshots"]) or end != max(r["snapshots"]) or c["engine_build"] != r["engine_build"]
            or c["snapshots"][start] != r["snapshots"][start]
            or c["snapshots"][end]["save_sha256"] == r["snapshots"][end]["save_sha256"]):
        raise ValueError("Not a common root or not distinct equal-date branch endpoints")
    old = {(p["id"], p["birth"]) for p in read(owners)["members"] if p["contract_owner"]}
    added = {(p["id"], p["birth"]) for p in read(youth)}
    if len(old) != 83 or len(added) != 16 or old & added:
        raise ValueError("Unexpected targeted population")
    targets = old | added
    totals, ca_delta, tier_delta = Counter(), Counter(), Counter()
    with closing(sqlite3.connect(control_database.resolve().as_uri()+"?mode=ro", uri=True)) as db:
        db.execute("ATTACH ? AS r", (retention_database.resolve().as_uri()+"?mode=ro",))
        for schema, manifest in (("main",c), ("r",r)):
            for day in (start,end):
                actual = db.execute(f"SELECT save_hash,inventory_hash,build FROM {schema}.snapshot WHERE career=? AND day=?",
                                    (manifest["career_id"], day)).fetchone()
                meta = manifest["snapshots"][day]
                if actual != (meta["save_sha256"],meta["native_sha256"],manifest["engine_build"]):
                    raise ValueError("Evidence and snapshot database disagree")
        rows = db.execute("""
            SELECT b.uid,b.birth,b.pa,x.ca,y.ca,x.pa,y.pa,x.candidate,y.candidate
            FROM main.observation b JOIN r.observation v USING(uid,birth,ca,pa)
            JOIN main.observation x ON x.uid=b.uid AND x.birth=b.birth AND x.career=b.career
            JOIN r.observation y ON y.uid=b.uid AND y.birth=b.birth AND y.career=v.career
            WHERE b.career=? AND v.career=? AND b.day=? AND v.day=?
              AND x.day=? AND y.day=? AND b.age<28 AND b.position<>'GK'
        """,(c["career_id"],r["career_id"],start,start,end,end))
        for uid, birth, pa, ca_c, ca_r, pa_c, pa_r, tier_c, tier_r in rows:
            totals["common_u28_outfield_endpoints"] += 1
            if (uid,birth) in targets:
                totals["known_target_persons_removed"] += 1
                continue
            totals["background_paired"] += 1
            ca_delta[ca_r-ca_c] += 1
            tier_delta[tier_r-tier_c] += 1
            totals["different_end_pa"] += pa_c != pa_r
            totals["different_end_full_baseline_pa_status"] += (ca_c >= pa) != (ca_r >= pa)
            totals["different_end_95_baseline_pa_status"] += (100*ca_c >= 95*pa) != (100*ca_r >= 95*pa)
    return {
        "schema":"pa-reach-branch-background/v1", "build":c["engine_build"], "start":start,"end":end,
        "source_root":c["snapshots"][start],"control_end":c["snapshots"][end],"retention_end":r["snapshots"][end],
        "excluded_roster_union":len(targets), "career_cluster_count":1, **totals,
        "end_ca_delta_retention_minus_control_frequency":dict(sorted(ca_delta.items())),
        "end_saved_factor_delta_retention_minus_control_frequency":dict(sorted(tier_delta.items())),
        "causal_effect":None,
    }


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ("control_database","retention_database","owners","youth","control_manifest","retention_manifest"):
        parser.add_argument(name,type=Path)
    print(json.dumps(summarize(**vars(parser.parse_args())),indent=2))

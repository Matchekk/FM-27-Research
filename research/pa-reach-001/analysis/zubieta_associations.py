"""Public 58-day association summary from Zubieta copies and a native endpoint readback."""
import argparse
import json
from pathlib import Path
import sqlite3

import numpy as np

from growth_associations import adjusted, club_bootstrap, correlations, design, partial


BUILD = "27.1.0+2505117"
FIRST = ("ZD-HIST-02", "2027-01-31")
LAST = ("ZD-ROOT-01", "2027-03-30")


def read_native_pairs(db):
    for tag, day in (FIRST, LAST):
        found = db.execute("SELECT build,game_date,sha256 FROM capture WHERE tag=?", (tag,)).fetchone()
        if found is None or found[:2] != (BUILD,day):
            raise ValueError("Unexpected Zubieta source date or build")
        refs = list(db.execute("SELECT career FROM ref.snapshot WHERE save_hash=? AND day=? AND build=?",
                               (found[2], day, BUILD)))
        if len(refs) != 1:
            raise ValueError("Missing or ambiguous native reference")
        if tag == FIRST[0]:
            career = refs[0][0]
        elif career != refs[0][0]:
            raise ValueError("Native references do not belong to the same series")
    rows = list(db.execute("""
        SELECT a.age, a.pa-a.ca, a.ca, a.pa, b.ca-a.ca, a.pos, m.club
          FROM player a JOIN player b USING(uid,birth)
          JOIN ref.observation m ON a.uid=m.uid AND a.birth=m.birth AND a.ca=m.ca AND a.pa=m.pa
          JOIN ref.observation n ON b.uid=n.uid AND b.birth=n.birth AND b.ca=n.ca AND b.pa=n.pa
         WHERE a.tag=? AND b.tag=? AND m.day=? AND n.day=? AND m.career=? AND n.career=m.career
           AND a.age<28 AND a.pos<>'GK' AND a.name_check=b.name_check
         ORDER BY a.uid,a.birth
    """,(FIRST[0],LAST[0],FIRST[1],LAST[1],career)))
    if not rows:
        raise ValueError("No eligible native-endpoint pairs")
    return rows


def run(db):
    rows = read_native_pairs(db)
    cols = list(zip(*rows,strict=True))
    v = {k:np.asarray(x,dtype=float) for k,x in zip(("age","gap","ca","pa","delta"),cols[:5],strict=True)}
    pos, club = np.asarray(cols[5]),np.asarray(cols[6])
    known = np.array([c is not None for c in club])
    conditional = {k:club_bootstrap(v[k][known],v["delta"][known],club[known]) for k in ("age","gap","ca","pa")}
    groups = {"<18":v["age"]<18, "18-20":(v["age"]>=18)&(v["age"]<=20),
              "21-23":(v["age"]>=21)&(v["age"]<=23),"24-27":v["age"]>=24}
    cells = []
    for age_group, age_mask in groups.items():
        for gap_group, gap_mask in (("<0",v["gap"]<0),("0",v["gap"]==0),
                ("1-10",(v["gap"]>=1)&(v["gap"]<=10)),("11-30",(v["gap"]>10)&(v["gap"]<=30)),
                (">30",v["gap"]>30)):
            outcome = v["delta"][age_mask & gap_mask]
            cells.append({"age":age_group,"gap":gap_group,"n":len(outcome),
                          "mean_delta":float(outcome.mean()) if len(outcome) else None})
    x,_ = design(v,pos,include_candidate=False)
    knots = (18,21,24)
    hinges = [np.maximum(v["age"]-k,0) for k in knots]
    x = np.column_stack((x,*hinges))
    beta,_,rank,_ = np.linalg.lstsq(x,v["delta"],rcond=None)
    if rank != x.shape[1]:
        raise ValueError("Age spline design is rank deficient")
    residual = v["delta"]-x@beta
    slopes = np.r_[beta[1],beta[-3:]].cumsum()
    groups.update({"position_"+p:pos==p for p in np.unique(pos)})
    return {
        "career_roots":1, "build":BUILD, "start":FIRST[1],"end":LAST[1],"days":58,
        "status":"NATIVE_CONFIRMED_CA_PA_BOTH_DATES",
        "inclusion":"outfield at baseline under 28, paired database UID + DOB + nonempty equal name checksum, CA/PA verified at January and March against dated native inventories",
        "n_distinct_end_to_end":len(rows),"baseline_verified_club_missing":int(sum(~known)),
        "complete_player_seasons":0, "delta_distribution":{str(int(k)):int(n) for k,n in zip(*np.unique(v["delta"],return_counts=True),strict=True)},
        "correlations":{k:correlations(x,v["delta"]) for k,x in v.items() if k!="delta"},
        "conditional_club_subset_correlations":conditional,
        "partial_pearson":{k:partial(v,pos,k) for k in ("age","gap")},
        "gap_delta_by_group":{g:correlations(v["gap"][mask],v["delta"][mask]) for g,mask in groups.items()},
        "age_gap_cells":cells,
        "exploratory_piecewise_age":{"prespecified_band_boundaries_used_as_knots":knots,
            "slope_per_year_at_gap_20_by_segment":slopes.tolist(),
            "descriptive_r_squared":float(1-residual@residual/np.sum((v["delta"]-v["delta"].mean())**2))},
        "adjusted_all":adjusted(v,pos,include_candidate=False),
        "adjusted_with_baseline_club":adjusted({k:x[known] for k,x in v.items()},pos[known],club[known],include_candidate=False),
        "career_cluster_95ci":None,"causal_ate":None
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("panel",type=Path)
    parser.add_argument("native",type=Path)
    args = parser.parse_args()
    with sqlite3.connect(args.panel.resolve().as_uri()+"?mode=ro",uri=True) as db:
        db.execute("ATTACH DATABASE ? AS ref",(args.native.resolve().as_uri()+"?mode=ro",))
        print(json.dumps(run(db),indent=2,allow_nan=False))

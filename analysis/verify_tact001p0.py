"""Independent recalculation from public rows, without importing the frozen analyser."""
from collections import defaultdict
from hashlib import sha256
from math import isclose, sqrt
from pathlib import Path
import json

import numpy as np
from scipy.stats import chi2, nct, t

ROOT=Path(__file__).resolve().parents[1]/"data/tact-001-p0"
METRICS=("xgd","points","gf","ga","xgf","xga","shots_for","shots_against","sot_for","sot_against","possession_for")
SCENARIOS=("high_press","deep_block")
COEFFICIENTS={"baseline":1,"press":-1,"line":-1,"combined":1}


def verify():
    observed=[json.loads(line) for line in (ROOT/"main.jsonl").read_text(encoding="utf8").splitlines()]
    archived=json.loads((ROOT/"effects.json").read_text(encoding="utf8"))
    manifest=json.loads((ROOT/"manifest.json").read_text(encoding="utf8"))
    blocks=defaultdict(dict)
    for row in observed:
        side=row["tested_side"]
        own,other=row["team_statistics"][side],row["team_statistics"][1-side]
        gf,ga=row["score"][side],row["score"][1-side]
        values=dict(xgd=own["xg"]-other["xg"],points=3 if gf>ga else int(gf==ga),gf=gf,ga=ga,
                    xgf=own["xg"],xga=other["xg"],shots_for=own["shots"],shots_against=other["shots"],
                    sot_for=own["shots_on_target"],sot_against=other["shots_on_target"],possession_for=own["possession"])
        key=(row["scenario"],row["seed"])
        assert (side,row["arm"]) not in blocks[key]
        assert row["status"]=="ok" and row["input_contract_verified"]
        blocks[key][side,row["arm"]]=values
    assert len(blocks)==16 and all(len(block)==8 for block in blocks.values())
    def equal(a,b):
        np.testing.assert_allclose(a,b,rtol=1e-12,atol=1e-12)
    raw_p={}
    for metric in METRICS:
        cells=[]
        for index,scenario in enumerate(SCENARIOS):
            vector=[]
            for seed in manifest["seeds"][index*8:(index+1)*8]:
                block=blocks[scenario,seed]
                vector.append(sum(coef*block[side,arm][metric]/2 for side in (0,1) for arm,coef in COEFFICIENTS.items()))
            cells.append(np.asarray(vector))
        variance=sum(c.var(ddof=1)/32 for c in cells)
        mean=sum(c.mean()/2 for c in cells)
        terms=[c.var(ddof=1)/32 for c in cells]
        if variance:
            df=variance**2/sum(v*v/7 for v in terms)
            width=t.isf(.025,df)*sqrt(variance)
            p=2*t.sf(abs(mean)/sqrt(variance),df)
        else:
            width=0.;p=float(mean==0)
        target=archived["primary"] if metric=="xgd" else archived["secondary"][metric]
        equal(mean,target["mean"]);equal(p,target["p"])
        equal([mean-width,mean+width],target["ci"])
        rng=np.random.default_rng(int.from_bytes(sha256(b"TACT-001-P0/bootstrap-v1").digest()[:8],"little"))
        samples=np.zeros(20000)
        for values in cells:
            for offset in range(0,20000,256):
                length=min(256,20000-offset)
                draw=rng.choice(values,size=(length,8),replace=True)
                samples[offset:offset+length]+=draw.sum(axis=1)/16
        equal(np.quantile(samples,[.025,.975]),target["bootstrap_ci"])
        for scenario,values in zip(SCENARIOS,cells):
            equal(values.std(ddof=1),target["context"][scenario]["sd"])
            equal(values.std(ddof=1)*sqrt(7/chi2.ppf(.05,7)),target["context"][scenario]["sd_upper95"])
        if metric!="xgd":
            raw_p[metric]=float(p)
        else:
            pooled=sqrt(sum(c.var(ddof=1) for c in cells)/2)
            equal(pooled,target["pooled_within_context_sd"])
            equal(pooled*sqrt(14/chi2.ppf(.05,14)),target["pooled_sd_upper95"])
    previous=0.
    for rank,name in enumerate(sorted(raw_p,key=raw_p.get)):
        previous=max(previous,min(1.,(10-rank)*raw_p[name]))
        equal(previous,archived["secondary"][name]["p_holm"])
    context=archived["primary"]["context"]
    for row in archived["confirmation_planning"]:
        for field,sd_key in (("observed_sd","sd"),("upper95_each_sd","sd_upper95")):
            plan=row[field]
            sds=[context[s][sd_key] for s in SCENARIOS]
            def power(n):
                terms=[value**2/(4*n) for value in sds]
                var=sum(terms)
                df=var**2/sum(v*v/(n-1) for v in terms)
                cutoff=t.isf(.025,df)
                nc=row["effect_xgd_did"]/sqrt(var)
                return float(nct.cdf(-cutoff,df,nc)+nct.sf(cutoff,df,nc))
            n=plan["n_per_scenario"]
            assert power(n)>=.9 and (n==2 or power(n-1)<.9)
            assert plan["total_seed_blocks"]==2*n and plan["matches"]==16*n
            equal(power(n),plan["power_at_n"])
    print("Verified all 11 contrasts, 11 t/bootstrap intervals, Holm family, SD bounds and six sample-size minima from public rows.")


if __name__=="__main__":
    verify()

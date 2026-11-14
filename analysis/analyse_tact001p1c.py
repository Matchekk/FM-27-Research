"""Frozen P1C direct paired-points precision pilot. No native execution."""
from hashlib import sha256
from pathlib import Path
import sys
import numpy as np
from scipy.stats import chi2,nct,t
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.core import config_hash,schedule
from research.native import read,rows,require,write
from research.stats import estimate,holm
from analyse_tact001p1b import FACTORS,CONTEXTS,PLAUSIBILITY,endpoints,matrix as source_matrix
ARMS=("D00","D15")
SECONDARY=("xgd","gf","ga","xgf","xga")
METRICS=("points",*SECONDARY,*PLAUSIBILITY)
SCHEDULER_SEED=2026111404
BOOTSTRAPS=20000
BOOT_SEED=int.from_bytes(sha256(b"TACT-001-P1C/bootstrap-v1").digest()[:8],"little")

def matrix():return [r for r in source_matrix() if r["id"] in ARMS]

def validate_design(c):
    d=c["design"]
    require(c["experiment_id"]=="TACT-001-P1C" and c["metrics"]["primary"]=="points","Wrong pilot/endpoint")
    require(d["matrix"]==matrix() and d["matrix_sha256"]==config_hash(matrix()) and d["factors"]==list(FACTORS),"Frozen candidate matrix mismatch")
    require([a["id"] for a in d["arms"]]==list(ARMS) and d["control_arm"]=="D00","D15 only vs D00")
    require(d["n_blocks"]==64 and d["sides"]==[0,1] and [s["id"] for s in d["scenarios"]]==list(CONTEXTS),"Sample/context mismatch")
    require(c["budget"]["max_matches"]==512 and c["budget"]["max_workers"]==4,"Budget mismatch")

def checked(data,r):
    validate_design(r["config"]);expected={j["key"]:j for j in schedule(r)}
    cube=np.empty((2,64,2,2,len(METRICS)));seen=set()
    for row in data:
        require(row["key"] in expected and row["key"] not in seen,"Unexpected/duplicate job")
        j=expected[row["key"]];seen.add(row["key"])
        require(row["status"]=="ok" and row.get("input_contract_verified") is True and row.get("profile_fields_verified")==1058 and 0<row["finish_tick"]<47996,"Unverified match")
        require(all(row.get(k)==v for k,v in j["identity"].items()) and all(row.get(k)==j[k] for k in ("setup_sha256","config_sha256","scenario","seed","arm")) and row["tested_side"]==j["side"],"Identity/input/seed drift")
        a=ARMS.index(j["arm"]);level=matrix()[a]["levels"]
        require(row.get("design_matrix_sha256")==config_hash(matrix()) and row.get("factor_levels")==level and row.get("native_factor_bits")=={f["code"]:f["high_bit"] if level[f["code"]]==1 else 0 for f in FACTORS},"Native candidate mismatch")
        h=CONTEXTS.index(j["scenario"]);i=r["seeds"][h*64:(h+1)*64].index(j["seed"])
        values=endpoints(row);cube[h,i,j["side"],a]=[values[m] for m in METRICS]
    require(seen==set(expected) and np.isfinite(cube).all(),"Incomplete blocks: technical status only")
    return cube

def summarize(v):
    cells=v.mean(axis=2);z=estimate(list(cells),resamples=BOOTSTRAPS,bootstrap_seed=BOOT_SEED)
    z["context"]={h:dict(mean=float(cells[k].mean()),sd=float(cells[k].std(ddof=1)),home_mean=float(v[k,:,0].mean()),away_mean=float(v[k,:,1].mean()),home_sd=float(v[k,:,0].std(ddof=1)),away_sd=float(v[k,:,1].std(ddof=1)),side_covariance=float(np.cov(v[k].T)[0,1])) for k,h in enumerate(CONTEXTS)}
    z["pooled_within_context_sd"]=float(np.sqrt(cells.var(axis=1,ddof=1).mean()))
    loo=[float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(64)]
    z["leave_one_out"]=dict(range=[min(loo),max(loo)],max_change=max(abs(x-z["mean"]) for x in loo))
    return z

def properties(sds,n,effect=.15):
    v=np.array(sds)**2/(4*n);se=float(np.sqrt(v.sum()))
    df=float(v.sum()**2/(v*v/(n-1)).sum());cut=t.isf(.025,df)
    power=float(nct.cdf(-cut,df,effect/se)+nct.sf(cut,df,effect/se))
    return dict(se=se,df=df,full_ci_width=float(2*cut*se),power=power)

def minimum(sds,effect=None,width=None):
    def ok(n):
        z=properties(sds,n,effect or .15)
        return z["power"]>=.9 if effect else z["full_ci_width"]<=width
    lo,hi=1,2
    while not ok(hi):hi*=2
    while hi-lo>1:
        mid=(hi+lo)//2
        if ok(mid):hi=mid
        else:lo=mid
    return hi

def planning(sd,n=64):
    upper=[float(s*np.sqrt((n-1)/chi2.ppf(.025,n-1))) for s in sd]
    cases={"observed":list(sd),"simultaneous95_normal_model_upper":upper,"bounded_points_sd3":[3.,3.]}
    return dict(assumptions="Fixed equal contexts, equal new n per context, paired side means; noncentral Welch-t planning approximation. Chi-square simultaneous upper bounds assume normal seed contrasts (discrete points violate exact normality). SD3 is distribution-free range bound, not exact t-power assurance.",
        cases={name:dict(sd=s,at_64=properties(s,64),power90=[dict(effect=e,n_per_context=(k:=minimum(s,effect=e)),independent_blocks=2*k,matches=8*k) for e in (.10,.15,.20)],precision=[dict(full_width=w,n_per_context=(k:=minimum(s,width=w)),independent_blocks=2*k,matches=8*k) for w in (.20,.30)]) for name,s in cases.items()})

def analyse(data,r):
    cube=checked(data,r);v=cube[:,:,:,1]-cube[:,:,:,0]
    results={m:summarize(v[:,:,:,k]) for k,m in enumerate(METRICS[:6])}
    for m,p in zip(SECONDARY,holm([results[m]["p"] for m in SECONDARY]),strict=True):results[m].update(p_holm=p,reject_holm=p<=.05)
    primary=results["points"];width=primary["ci"][1]-primary["ci"][0]
    signal=bool(primary["mean"]>=.15 and primary["ci"][0]>0 and width<=.30 and all(x["mean"]>0 for x in primary["context"].values()))
    blocks=[dict(context=h,seed=r["seeds"][j*64+i],contrasts={m:float(v[j,i,:,k].mean()) for k,m in enumerate(METRICS)}) for j,h in enumerate(CONTEXTS) for i in range(64)]
    return dict(experiment_id="TACT-001-P1C",evidence="independent_seed_precision_pilot_in_existing_synthetic_context",n_matches=512,independent_seed_blocks=128,
        primary=primary,secondary={m:results[m] for m in SECONDARY},adequate_preregistered_signal=signal,
        recommendation="Separately design external-context confirmation; no automatic execution" if signal else "Switch to new roles and OOP structures; do not indefinitely retest this instruction package",
        general_career_transfer_confirmed=False,candidate_changed=False,
        actual_arm_means={h:{a:{m:float(cube[j,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)},
        planning=planning([primary["context"][h]["sd"] for h in CONTEXTS]),bootstrap=dict(resamples=BOOTSTRAPS,seed=BOOT_SEED)),blocks

if __name__=="__main__":
    folder=ROOT/"data/tact-001-p1c";result,blocks=analyse(rows(folder/"main.jsonl"),read(folder/"manifest.json"));write(folder/"effects.json",result)
    import json
    (folder/"block-contrasts.jsonl").write_text("".join(json.dumps(r)+"\n" for r in blocks),encoding="utf8")

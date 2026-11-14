"""Paired complete-block inference; confidence intervals never imply universality."""
from collections import defaultdict
from math import isfinite, sqrt

import numpy as np
from scipy.stats import nct, t

from .native import require


def metrics(row):
    require(row["status"] == "ok" and row.get("engine_readback") is True, "Failed/unverified observation")
    score, teams, side = row["score"], row["team_statistics"], row["tested_side"]
    require(type(side) is int and side in (0,1) and len(score)==len(teams)==2, "Invalid side/result")
    require(all(type(v) is int and v >= 0 for v in score), "Invalid goals")
    for team in teams:
        require(all(type(team[k]) in (int,float) and isfinite(team[k]) for k in
                    ("xg","shots","shots_on_target","passes","completed_passes","possession")), "Missing/nonfinite statistics")
        require(team["xg"] >= 0 and 0 <= team["shots_on_target"] <= team["shots"] and
                0 <= team["completed_passes"] <= team["passes"] and 0 <= team["possession"] <= 1, "Implausible statistics")
    require(abs(sum(x["possession"] for x in teams)-1) < 1e-6, "Invalid possession sum")
    gf, ga = score[side],score[1-side]
    xgf,xga = teams[side]["xg"],teams[1-side]["xg"]
    return dict(points=3 if gf>ga else int(gf==ga), gf=gf, ga=ga, xgf=xgf, xga=xga, xgd=xgf-xga)


def estimate(cells, alpha=.05, bootstrap_seed=1729, resamples=10000):
    """Equal scenario weights; each input contains independent seed-cluster means."""
    require(cells and 0 < alpha < 1 and type(resamples) is int and resamples > 0, "Invalid inference settings")
    arrays = [np.asarray(c, dtype=float) for c in cells]
    require(all(a.ndim==1 and len(a)>=2 and np.isfinite(a).all() for a in arrays), "Need two complete finite seed blocks per scenario")
    weights = np.repeat(1/len(arrays),len(arrays))
    mean = float(sum(w*a.mean() for w,a in zip(weights,arrays)))
    variances = [float(w*w*a.var(ddof=1)/len(a)) for w,a in zip(weights,arrays)]
    variance = sum(variances)
    if variance:
        df = variance**2/sum(v*v/(len(a)-1) for v,a in zip(variances,arrays))
        se = sqrt(variance)
        width = float(t.ppf(1-alpha/2,df)*se)
        p = float(2*t.sf(abs(mean/se),df))
    else:
        df,se,width,p = None,0.,0.,float(mean==0)
    rng = np.random.default_rng(bootstrap_seed)
    boot = np.zeros(resamples)
    for weight,values in zip(weights,arrays):
        for start in range(0,resamples,256):
            size = min(256,resamples-start)
            boot[start:start+size] += weight*values[rng.integers(len(values),size=(size,len(values)))].mean(axis=1)
    return dict(mean=mean, se=se, df=df, ci=[mean-width,mean+width], p=p, alpha=alpha,
                bootstrap_ci=np.quantile(boot,[alpha/2,1-alpha/2]).tolist(),
                n_seed_blocks=sum(map(len,arrays)), n_scenarios=len(arrays),
                weighting="equal_scenarios_then_equal_seeds; sides averaged within seed")


def holm(probabilities):
    require(all(type(p) in (int,float) and isfinite(p) and 0<=p<=1 for p in probabilities), "Invalid p-value")
    result, previous = [None]*len(probabilities),0.
    for rank,index in enumerate(sorted(range(len(probabilities)),key=lambda i:probabilities[i])):
        previous = max(previous,min(1.,probabilities[index]*(len(probabilities)-rank)))
        result[index] = previous
    return result


def required_n(effect, sd, power=.9, alpha=.05):
    require(all(isfinite(x) for x in (effect,sd,power,alpha)) and effect>0 and sd>0 and
            .5<power<1 and 0<alpha<1, "Invalid power assumptions")
    def achieved(n):
        cutoff = t.isf(alpha/2,n-1)
        noncentrality = sqrt(n)*effect/sd
        return nct.cdf(-cutoff,n-1,noncentrality)+nct.sf(cutoff,n-1,noncentrality)
    lo,hi=1,2
    while achieved(hi)<power:
        hi*=2
        require(hi<=10000000, "Unrealistic sample requirement")
    while hi-lo>1:
        mid=(lo+hi)//2
        if achieved(mid)>=power:
            hi=mid
        else:
            lo=mid
    return hi


def paired_cells(observations, expected_jobs, treatment, endpoint="xgd"):
    """Refuse duplicates, failed attempts, incomplete sides and missing arms."""
    expected = {(j["scenario"],j["seed"],j["side"],j["arm"]):j for j in expected_jobs}
    require(len(expected)==len(expected_jobs), "Duplicate scheduled match")
    indexed={}
    for row in observations:
        key=(row["scenario"],row["seed"],row["tested_side"],row["arm"])
        require(key in expected and key not in indexed, "Unexpected/duplicate observation")
        require(row["setup_sha256"]==expected[key]["setup_sha256"] and
                row["config_sha256"]==expected[key]["config_sha256"], "Observation/registration mismatch")
        require(all(row.get(k)==v for k,v in expected[key].get("identity",{}).items()), "Observation identity drift")
        indexed[key]=metrics(row)
    require(indexed.keys()==expected.keys(), "Incomplete blocks; no silent exclusions")
    cells=defaultdict(lambda:defaultdict(list))
    for scenario,seed,side,arm in expected:
        if arm==treatment:
            cells[scenario][seed].append(indexed[scenario,seed,side,treatment][endpoint]-indexed[scenario,seed,side,"baseline"][endpoint])
    require(cells, "Treatment absent")
    return [[float(np.mean(by_seed[seed])) for seed in sorted(by_seed)] for _,by_seed in sorted(cells.items())]

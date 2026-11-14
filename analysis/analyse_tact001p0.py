"""Frozen TACT-001-P0 difference-in-differences analysis and variance planning."""
from collections import defaultdict
from hashlib import sha256
from math import ceil, sqrt
from pathlib import Path
import sys

import numpy as np
from scipy.stats import chi2, nct, t

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research.core import schedule
from research.native import require
from research.stats import estimate, holm, metrics

EXPERIMENT="TACT-001-P0"
ARMS=("baseline","press","line","combined")
SCENARIOS=("high_press","deep_block")
PRIMARY="xgd"
SECONDARY=("points","gf","ga","xgf","xga","shots_for","shots_against","sot_for","sot_against","possession_for")
BOOTSTRAPS=20000
BOOTSTRAP_SEED=int.from_bytes(sha256(b"TACT-001-P0/bootstrap-v1").digest()[:8],"little")


def endpoints(row):
    result=metrics(row)
    side=row["tested_side"]
    own,other=row["team_statistics"][side],row["team_statistics"][1-side]
    result.update(shots_for=own["shots"],shots_against=other["shots"],sot_for=own["shots_on_target"],
                  sot_against=other["shots_on_target"],possession_for=own["possession"])
    return result


def checked(observations,receipt):
    jobs=schedule(receipt)
    expected={(j["scenario"],j["seed"],j["side"],j["arm"]):j for j in jobs}
    require(len(expected)==128,"Pilot must have exactly 128 scheduled main matches")
    indexed={}
    for row in observations:
        key=(row["scenario"],row["seed"],row["tested_side"],row["arm"])
        require(key in expected and key not in indexed,"Unexpected or duplicate main result")
        job=expected[key]
        require(row["status"]=="ok" and row.get("input_contract_verified") is True and
                0<row["finish_tick"]<47996,"Unverified main result")
        require(row["setup_sha256"]==job["setup_sha256"] and row["config_sha256"]==job["config_sha256"] and
                all(row.get(k)==v for k,v in job["identity"].items()),"Main identity/input mismatch")
        indexed[key]=endpoints(row)
    require(set(indexed)==set(expected),"Incomplete main blocks: technical reporting only")
    return indexed


def contrast_cells(indexed,seeds,metric):
    cells=[]
    for number,scenario in enumerate(SCENARIOS):
        values=[]
        for seed in seeds[number*8:(number+1)*8]:
            side_effects=[]
            for side in (0,1):
                y={arm:indexed[scenario,seed,side,arm][metric] for arm in ARMS}
                side_effects.append(y["combined"]-y["press"]-y["line"]+y["baseline"])
            values.append(float(np.mean(side_effects)))
        cells.append(np.asarray(values))
    return cells


def stratified_n(effect,sds,alpha=.05,target=.9):
    """Balanced two-context Welch/noncentral-t planning approximation."""
    require(effect>0 and all(sd>0 for sd in sds),"Positive planning effect/SD required")
    def power(n):
        terms=[sd*sd/(4*n) for sd in sds]
        variance=sum(terms)
        df=variance*variance/sum(v*v/(n-1) for v in terms)
        cutoff=t.isf(alpha/2,df)
        nc=effect/sqrt(variance)
        return float(nct.cdf(-cutoff,df,nc)+nct.sf(cutoff,df,nc))
    lo,hi=1,2
    while power(hi)<target:
        hi*=2
        require(hi<1000000,"Planning grid exceeds supported limit")
    while hi-lo>1:
        mid=(lo+hi)//2
        if power(mid)>=target:
            hi=mid
        else:
            lo=mid
    return dict(n_per_scenario=hi,total_seed_blocks=2*hi,matches=16*hi,
                power_at_n=power(hi),alpha=alpha,target_power=target)


def analyse(observations,receipt):
    indexed=checked(observations,receipt)
    seeds=receipt["seeds"]
    results={}
    cells_by_metric={}
    for metric in (PRIMARY,*SECONDARY):
        cells=contrast_cells(indexed,seeds,metric)
        cells_by_metric[metric]=cells
        results[metric]=estimate(cells,bootstrap_seed=BOOTSTRAP_SEED,resamples=BOOTSTRAPS)
        results[metric]["context"]={scenario:dict(n=len(values),mean=float(values.mean()),sd=float(values.std(ddof=1)),
              sd_upper95=float(values.std(ddof=1)*sqrt(7/chi2.ppf(.05,7))))
              for scenario,values in zip(SCENARIOS,cells,strict=True)}
    for metric,adjusted in zip(SECONDARY,holm([results[m]["p"] for m in SECONDARY]),strict=True):
        results[metric].update(p_holm=adjusted,reject_holm=adjusted<=.05)
    primary=results[PRIMARY]
    cells=cells_by_metric[PRIMARY]
    within_sd=sqrt(sum(7*float(c.var(ddof=1)) for c in cells)/14)
    sd_upper=within_sd*sqrt(14/chi2.ppf(.05,14))
    primary.update(pooled_within_context_sd=within_sd,pooled_sd_upper95=sd_upper,
                   sd_assumptions="Normal within-context contrasts; pooled bound additionally assumes common variance")
    planning=[]
    sd=[primary["context"][s]["sd"] for s in SCENARIOS]
    upper=[primary["context"][s]["sd_upper95"] for s in SCENARIOS]
    if all(value>0 for value in sd):
        for effect in (.10,.15,.20):
            planning.append(dict(effect_xgd_did=effect,observed_sd=stratified_n(effect,sd),
                                 upper95_each_sd=stratified_n(effect,upper)))
    # Marginal arm means are descriptions, never a winner-selection rule.
    arm_means={arm:{m:float(np.mean([values[m] for key,values in indexed.items() if key[-1]==arm]))
               for m in ("xgd","points","gf","ga")} for arm in ARMS}
    return dict(experiment_id=EXPERIMENT,n_matches=128,independent_seed_blocks=16,contexts=2,
                primary=primary,secondary={m:results[m] for m in SECONDARY},
                contrast="(combined - press - line + baseline), sides averaged within seed; contexts weighted 1/2",
                bootstrap=dict(resamples=BOOTSTRAPS,seed=BOOTSTRAP_SEED,unit="complete seed contrast within scenario"),
                confirmation_planning=planning,
                planning_caveat="Two individual one-sided 95% SD bounds are not a joint 95% bound; noncentral-t planning is approximate, not achieved pilot power.",
                arm_means_descriptive=arm_means,evidence="exploratory_variance_pilot",winner_selected=False)

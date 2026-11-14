"""Constrained DoE and bounded model-guided proposals, without simulation side effects."""
from hashlib import sha256
from itertools import combinations, product

import numpy as np

from .core import config_hash
from .native import require

IP4231 = sorted(("GK","DR","DCR","DCL","DL","DMR","DML","AMR","AMC","AML","ST"))


def validate_4231(scenario, server, side=0):
    normalized=server.validate_scenario(scenario)
    require(sorted(c["position"] for c in normalized["teams"][side]["phases"][0])==IP4231,
            "Search class requires 4-2-3-1 in possession")
    return normalized


def fractional_design(names):
    """2^(5-1), E=ABCD, resolution V: main and two-factor effects separable."""
    require(len(names)==len(set(names))==5, "Resolution V design needs five distinct factors")
    return [dict(zip(names,(*levels,int(np.prod(levels))),strict=True)) for levels in product((-1,1),repeat=4)]


def features(candidate, names):
    values=[candidate[k] for k in names]
    return [1.,*values,*(a*b for a,b in combinations(values,2))]


def propose(observed, candidates, names, limit=4, ridge=1., penalty=1.96):
    """Rank a finite legal pool by regularized mean minus model uncertainty.

    Observations are discovery-only seed-block estimates. Predictions do not confirm effects.
    """
    require(observed and 1<=limit<=4 and ridge>0 and len(candidates)<=256, "Invalid bounded search")
    require(all(o.get("split")=="discovery" and o["se"]>0 for o in observed), "Held-out data cannot train search")
    x=np.asarray([features(o["factors"],names) for o in observed],dtype=float)
    y=np.asarray([o["mean"] for o in observed],dtype=float)
    weights=1/np.square([o["se"] for o in observed])
    require(np.isfinite(x).all() and np.isfinite(y).all() and np.isfinite(weights).all(), "Nonfinite search data")
    regularizer=np.eye(x.shape[1])*ridge
    regularizer[0,0]=0
    inv=np.linalg.inv(x.T@(weights[:,None]*x)+regularizer)
    beta=inv@(x.T@(weights*y))
    seen={config_hash(o["factors"]) for o in observed}
    ranked=[]
    for candidate in candidates:
        key=config_hash(candidate)
        if key in seen:
            continue
        seen.add(key)
        vector=np.asarray(features(candidate,names),dtype=float)
        mean=float(vector@beta)
        se=float(np.sqrt(max(0,vector@inv@vector)))
        ranked.append(dict(factors=candidate, predicted_mean=mean, model_se=se, utility=mean-penalty*se,
                           evidence="exploratory_prediction; validate robustness before selection"))
    return sorted(ranked,key=lambda r:(-r["utility"],config_hash(r["factors"])))[:limit]

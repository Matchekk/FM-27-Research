"""Recompute public aggregate associations from the private TRAIN005-A capture."""
import argparse
from datetime import date
import itertools
import json
from pathlib import Path
import sqlite3

import numpy as np
import scipy
from scipy import stats


BASE = Path(__file__).resolve().parents[1]
PLAN = BASE / "manifests" / "association-plan.json"
NAMES = ("age", "gap", "ca", "pa", "candidate", "delta")


def correlations(x, y):
    if len(x) < 2 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return dict(n=len(x), pearson=None, spearman=None)
    return dict(n=len(x), pearson=float(np.corrcoef(x, y)[0, 1]),
                spearman=float(np.corrcoef(stats.rankdata(x), stats.rankdata(y))[0, 1]))


def holm(p):
    p = np.asarray(p)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    adjusted[order] = np.minimum(1, np.maximum.accumulate(p[order] * np.arange(len(p), 0, -1)))
    return adjusted


def read_pairs(conn, plan):
    career, start, end = (plan[k] for k in ("career", "start", "end"))
    snapshot = list(conn.execute("SELECT day, build FROM snapshot WHERE career=? ORDER BY day", (career,)))
    if not snapshot or snapshot[0][0] != start or snapshot[-1][0] != end:
        raise ValueError("Archived endpoints required")
    if any(build != plan["build"] for _, build in snapshot):
        raise ValueError("Mixed or unexpected build")
    selected = list(conn.execute("""
        SELECT a.age, a.pa-a.ca, a.ca, a.pa, a.candidate, b.ca-a.ca, a.position, a.club
          FROM observation a JOIN observation b USING(career,uid,birth)
         WHERE a.career=? AND a.day=? AND b.day=? AND a.age<28 AND a.position<>'GK'
         ORDER BY a.uid,a.birth
    """, (career, start, end)))
    if not selected:
        raise ValueError("No identity-matched outfield pairs")
    columns = list(zip(*selected, strict=True))
    values = {k: np.array(v, dtype=float) for k, v in zip(NAMES, columns[:6], strict=True)}
    return values, np.array(columns[6]), np.array(columns[7])


def design(values, pos, include_candidate=True):
    age = values["age"] - 20
    gap = (values["gap"] - 20) / 10
    ca = (values["ca"] - 100) / 10
    columns = {"intercept": np.ones(len(pos)), "age_year": age, "gap_10": gap, "ca_10": ca,
               "age_year_x_gap_10": age * gap}
    for c in ((1, 2, 4, 5) if include_candidate else ()):
        is_category = values["candidate"] == c
        columns[f"byte_{c}_vs_3"] = is_category
        columns[f"byte_{c}_vs_3_x_gap_10"] = is_category * gap
    for p in np.unique(pos):
        if p != "DC":
            columns[f"position_{p}_vs_DC"] = pos == p
    return np.column_stack(list(columns.values())), list(columns)


def adjusted(values, pos, clubs=None, *, include_candidate=True, extra_columns=None):
    x, labels = design(values, pos, include_candidate)
    if extra_columns:
        x = np.column_stack([x, *extra_columns.values()])
        labels.extend(extra_columns)
    y = values["delta"]
    beta, _, rank, _ = np.linalg.lstsq(x, y, rcond=None)
    if rank != x.shape[1]:
        raise ValueError("Rank-deficient design")
    errors = y - x @ beta
    terms = {name: {"coefficient": float(b)} for name, b in zip(labels, beta, strict=True)}
    result = {"n": len(y), "coefficients": terms, "descriptive_r_squared": float(1 - errors@errors/np.sum((y-np.mean(y))**2))}
    if clubs is None:
        return result
    unique, idx = np.unique(clubs.astype(int), return_inverse=True)
    g, n, k = len(unique), len(y), len(labels)
    if g < 2 or n <= k:
        raise ValueError("Insufficient clubs or players")
    per_club = np.zeros((g, k))
    np.add.at(per_club, idx, errors[:, None] * x)
    bread = np.linalg.inv(x.T @ x)
    covariance = (bread @ per_club.T) @ (per_club @ bread) * (g / (g-1)) * ((n-1) / (n-k))
    se = np.sqrt(np.diag(covariance))
    width = stats.t.ppf(0.975, df=g-1) * se
    corrected = holm(2*stats.t.sf(abs(beta[1:]/se[1:]), df=g-1))
    for i, label in enumerate(labels):
        terms[label]["club_conditional_pointwise_95ci"] = [float(beta[i]-width[i]), float(beta[i]+width[i])]
        if i:
            terms[label]["holm_p"] = float(corrected[i-1])
    result["baseline_clubs"] = g
    return result


def partial(valuemap, positions, name):
    """Partial Pearson for age or gap, using CA, position and the other exposure."""
    controls = [np.ones(len(positions)), valuemap["ca"],
                valuemap["gap" if name == "age" else "age"]]
    controls.extend(positions == p for p in np.unique(positions)[1:])
    matrix = np.column_stack(controls)
    paired = np.column_stack((valuemap[name], valuemap["delta"]))
    residual = paired - matrix @ np.linalg.lstsq(matrix, paired, rcond=None)[0]
    return float(np.corrcoef(residual.T)[0, 1])


def club_bootstrap(x, y, clubs, draws=999):
    """Percentile intervals. Within-replicate Pearson and tie-adjusted Spearman via counts."""
    _, idx = np.unique(clubs.astype(int), return_inverse=True)
    xvalues, xc = np.unique(x, return_inverse=True)
    yvalues, yc = np.unique(y, return_inverse=True)
    shape = (len(xvalues), len(yvalues))
    cell = xc * shape[1] + yc
    g = int(idx.max()) + 1
    group_sizes = np.ones(g)/g
    rng = np.random.default_rng(49153)
    estimates = []
    for _ in range(draws):
        weight = rng.multinomial(g, group_sizes)[idx]
        table = np.bincount(cell, weights=weight, minlength=shape[0]*shape[1]).reshape(shape)
        wx, wy = table.sum(axis=1), table.sum(axis=0)
        if np.count_nonzero(wx) < 2 or np.count_nonzero(wy) < 2:
            continue
        rr = []
        for a, b in ((xvalues,yvalues), (wx.cumsum()-wx/2, wy.cumsum()-wy/2)):
            ac = a - np.average(a, weights=wx)
            bc = b - np.average(b, weights=wy)
            rr.append(float((ac @ table @ bc) / np.sqrt((wx @ (ac**2)) * (wy @ (bc**2)))))
        estimates.append(rr)
    ci = np.quantile(estimates, [0.025,0.975], axis=0) if estimates else None
    return dict(correlations(x,y), baseline_clubs=g, bootstrap_draws=draws, defined_draws=len(estimates),
                pearson_95ci=None if ci is None else ci[:,0].tolist(),
                spearman_95ci=None if ci is None else ci[:,1].tolist())


def run(conn, plan):
    v, pos, clubs = read_pairs(conn, plan)
    valid = np.isin(v["candidate"], [1,2,3,4,5])
    known = np.array([c is not None for c in clubs])
    eligible = np.ones(len(pos), dtype=bool)
    def pairs(group, names=NAMES):
        out = {}
        for x, y in itertools.combinations(names, 2):
            rows = group & valid if "candidate" in (x, y) else group
            out[x + "_" + y] = correlations(v[x][rows], v[y][rows])
        return out
    groups = {"age_lt18":v["age"]<18, "age_18_20":(v["age"]>=18)&(v["age"]<=20),
              "age_21_23":(v["age"]>=21)&(v["age"]<=23), "age_24_27":v["age"]>=24}
    groups.update({"position_"+p:pos==p for p in np.unique(pos)})
    fits = {}
    for name, mask in (("all_paired",valid),("verified_club_subset",valid & known)):
        fits[name] = adjusted({k: col[mask] for k, col in v.items()}, pos[mask],
                              clubs[mask] if name == "verified_club_subset" else None)
    conditional = {}
    for k in NAMES[:-1]:
        mask = valid & known if k=="candidate" else known
        conditional[k] = club_bootstrap(v[k][mask], v["delta"][mask], clubs[mask])
    return {
        "plan": "association-plan.json", "build": plan["build"], "root_careers": 1,
        "paired_distinct_outfield_players_under_28": len(pos), "complete_player_seasons": 0,
        "days": (date.fromisoformat(plan["end"])-date.fromisoformat(plan["start"])).days,
        "numpy": np.__version__, "scipy": scipy.__version__, "baseline_club_missing": int(sum(~known)),
        "baseline_candidate_exclusions_for_byte_analyses": int(sum(~valid)),
        "delta_distribution": {str(int(k)):int(n) for k,n in zip(*np.unique(v["delta"], return_counts=True), strict=True)},
        "correlations": pairs(eligible), "verified_club_subset_correlations": conditional,
        "within_groups": {g: {k: t for k,t in pairs(mask).items() if k.endswith("_delta")} for g,mask in groups.items()},
        "partial_pearson_delta": {k:partial(v,pos,k) for k in ("age","gap")}, "adjusted":fits,
        "career_cluster_95ci": None, "seasonal_effect":None, "causal_ate":None,
    }


if __name__ == "__main__":
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("database", type=Path)
    path = args.parse_args().database
    with sqlite3.connect(path.resolve().as_uri()+"?mode=ro", uri=True) as db:
        print(json.dumps(run(db,json.loads(PLAN.read_text())), indent=2, allow_nan=False))

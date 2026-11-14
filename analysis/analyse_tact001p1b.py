"""Frozen negative-half-fraction discovery analysis; refuse incomplete blocks."""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import sys

import numpy as np
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.core import config_hash, schedule
from research.discovery import fractional_design
from research.native import read, require, rows, write
from research.stats import estimate, holm, metrics

NAMES=tuple("ABCDE")
CONTEXTS=("high_press","deep_block")
ARMS=tuple(f"D{i:02d}" for i in range(16))
SECONDARY=("points","gf","ga","xgf","xga")
PLAUSIBILITY=("shots_for","shots_against","sot_for","sot_against","possession_for")
METRICS=("xgd",*SECONDARY,*PLAUSIBILITY)
FACTORS=(
 dict(code="A",group="TriggerPress",group_id=10,phase="OOP",low_id=1313689463,high_id=2000905329,high_bit=66,label="More Often"),
 dict(code="B",group="DefensiveLine",group_id=9,phase="OOP",low_id=894978671,high_id=1329018200,high_bit=57,label="Higher"),
 dict(code="C",group="Tempo",group_id=21,phase="IP",low_id=1496610426,high_id=1345339954,high_bit=47,label="Higher"),
 dict(code="D",group="PassingDirectness",group_id=1,phase="IP",low_id=1483944022,high_id=1146434657,high_bit=3,label="Shorter"),
 dict(code="E",group="AttackingWidth",group_id=4,phase="IP",low_id=1951095402,high_id=1244744824,high_bit=51,label="Wider"))
BOOTSTRAPS=20000
BOOT_SEED=int.from_bytes(sha256(b"TACT-001-P1B/bootstrap-v1").digest()[:8],"little")
SCHEDULER_SEED=2026111402


def matrix():
    return [dict(id=arm,levels=row) for arm,row in zip(ARMS,fractional_design(NAMES,fraction=-1),strict=True)]


def validate_design(config):
    d=config["design"]
    require(d["fraction"]==-1 and d["generator"]=="E=-A*B*C*D" and d["matrix"]==matrix(),"Negative-half design matrix mismatch")
    require(d["matrix_sha256"]==config_hash(matrix()) and d["factors"]==list(FACTORS),"Factor/catalog/design identity mismatch")
    require([a["id"] for a in d["arms"]]==list(ARMS) and d["control_arm"]=="D00", "Design ID/control mismatch")
    require(d["n_blocks"]==32 and d["sides"]==[0,1] and [s["id"] for s in d["scenarios"]]==list(CONTEXTS),"P1B sample/context mismatch")
    require(config["budget"]["max_matches"]==2048 and config["budget"]["max_workers"]==4,"P1B budget mismatch")
    return np.array([[r["levels"][n] for n in NAMES] for r in matrix()])


def coefficients():
    X=np.array([[r["levels"][n] for n in NAMES] for r in matrix()])
    main={name:X[:,i]/8 for i,name in enumerate(NAMES)}
    interactions={NAMES[i]+NAMES[j]:X[:,i]*X[:,j]/4 for i,j in combinations(range(5),2)}
    return main,interactions


def endpoints(row):
    result=metrics(row);s=row["tested_side"]
    a,b=row["team_statistics"][s],row["team_statistics"][1-s]
    result.update(shots_for=a["shots"],shots_against=b["shots"],sot_for=a["shots_on_target"],
                  sot_against=b["shots_on_target"],possession_for=a["possession"])
    return result


def checked(data,receipt):
    validate_design(receipt["config"])
    expected={j["key"]:j for j in schedule(receipt)}
    require(len(expected)==2048,"Exactly 2048 main jobs required")
    cube=np.empty((2,32,2,16,len(METRICS)));seen=set()
    for row in data:
        require(row["key"] in expected and row["key"] not in seen,"Unexpected/duplicate match")
        job=expected[row["key"]];seen.add(row["key"])
        require(row["status"]=="ok" and row.get("input_contract_verified") is True and
                row.get("profile_fields_verified")==1058 and 0<row["finish_tick"]<47996,"Unverified main match")
        require(all(row.get(k)==v for k,v in job["identity"].items()) and
                row["setup_sha256"]==job["setup_sha256"] and row["config_sha256"]==job["config_sha256"],"Match identity/setup mismatch")
        require(row["scenario"]==job["scenario"] and row["seed"]==job["seed"] and
                row["arm"]==job["arm"] and row["tested_side"]==job["side"],"Match seed/side/arm mismatch")
        ai=ARMS.index(job["arm"]);levels=matrix()[ai]["levels"]
        require(row.get("design_matrix_sha256")==config_hash(matrix()) and row.get("factor_levels")==levels and
                row.get("native_factor_bits")=={f["code"]:f["high_bit"] if levels[f["code"]]==1 else 0 for f in FACTORS},
                "Native factor/design/analysis mismatch")
        h=CONTEXTS.index(job["scenario"]);i=receipt["seeds"][h*32:(h+1)*32].index(job["seed"])
        values=endpoints(row)
        cube[h,i,job["side"],ai]=[values[m] for m in METRICS]
    require(seen==set(expected) and np.isfinite(cube).all(),"Incomplete seed blocks: technical reporting only")
    return cube


def summarize(side_values,simultaneous=False):
    cells=side_values.mean(axis=2)
    result=estimate(list(cells),resamples=BOOTSTRAPS,bootstrap_seed=BOOT_SEED)
    if simultaneous:
        width=float(t.isf(.005,result["df"])*result["se"]) if result["df"] else 0.
        result["ci99_bonferroni5"]=[result["mean"]-width,result["mean"]+width]
    result["context"]={name:dict(mean=float(cells[h].mean()),sd=float(cells[h].std(ddof=1)),
        home_mean=float(side_values[h,:,0].mean()),away_mean=float(side_values[h,:,1].mean()),
        home_sd=float(side_values[h,:,0].std(ddof=1)),away_sd=float(side_values[h,:,1].std(ddof=1)),
        side_covariance=float(np.cov(side_values[h].T)[0,1])) for h,name in enumerate(CONTEXTS)}
    loo=[float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(32)]
    result["leave_one_out"]=dict(mean_range=[min(loo),max(loo)],max_abs_change=max(abs(v-result["mean"]) for v in loo))
    return result


def select_candidates(cube):
    """Frozen minimax-context rule; no winner confidence intervals from selection data."""
    contrasts=cube[:,:,:,:,0]-cube[:,:,:,0:1,0]
    means=contrasts.mean(axis=(1,2))
    eligible=[dict(design_id=ARMS[a],levels=matrix()[a]["levels"],context_gains=dict(zip(CONTEXTS,means[:,a].tolist())),
                   worst_context_gain=float(means[:,a].min()),equal_context_gain=float(means[:,a].mean()))
              for a in range(1,16) if (means[:,a]>0).all()]
    return sorted(eligible,key=lambda v:(-v["worst_context_gain"],-v["equal_context_gain"],v["design_id"]))[:2]


def analyse(data,receipt):
    cube=checked(data,receipt);main,interactions=coefficients()
    primary={};secondary={};interaction={};plausibility={};block_rows=[]
    for name,coef in main.items():
        values=np.einsum("hisam,a->hism",cube,coef)
        primary[name]=summarize(values[:,:,:,0],True)
        secondary[name]={m:summarize(values[:,:,:,METRICS.index(m)]) for m in SECONDARY}
        plausibility[name]={m:dict(mean=float(values[:,:,:,METRICS.index(m)].mean()),
            context_means=dict(zip(CONTEXTS,values[:,:,:,METRICS.index(m)].mean(axis=(1,2)).tolist()))) for m in PLAUSIBILITY}
        for h,c in enumerate(CONTEXTS):
            for i,seed in enumerate(receipt["seeds"][h*32:(h+1)*32]):
                block_rows.append(dict(contrast=name,context=c,seed=seed,value=float(values[h,i,:,0].mean())))
    for name,coef in interactions.items():
        v=np.einsum("hisa,a->his",cube[:,:,:,:,0],coef)
        interaction[name]=summarize(v)
        for h,c in enumerate(CONTEXTS):
            for i,seed in enumerate(receipt["seeds"][h*32:(h+1)*32]):
                block_rows.append(dict(contrast=name,context=c,seed=seed,value=float(v[h,i].mean())))
    for family in (primary,interaction):
        for name,p in zip(family,holm([r["p"] for r in family.values()]),strict=True):
            family[name].update(p_holm=p,reject_holm=p<=.05)
    sec=[(a,m) for a in NAMES for m in SECONDARY]
    for (a,m),p in zip(sec,holm([secondary[a][m]["p"] for a,m in sec]),strict=True):
        secondary[a][m].update(p_holm=p,reject_holm=p<=.05)
    tau=read(ROOT/"data/tact-001-p1a/design-comparison.json")["orthogonal_noise_tau2"]
    transfer={n:{h:dict(observed_variance=primary[n]["context"][h]["sd"]**2,
                      predicted_variance=tau[h]/4,ratio=primary[n]["context"][h]["sd"]**2/(tau[h]/4)) for h in CONTEXTS} for n in NAMES}
    arm_means={h:{arm:{m:float(cube[j,:,:,a,k].mean()) for k,m in enumerate(METRICS)}
                     for a,arm in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)}
    covariance={h:np.cov(cube[j].mean(axis=1)[:,:,0].T).tolist() for j,h in enumerate(CONTEXTS)}
    return dict(experiment_id="TACT-001-P1B",evidence="exploratory_discovery",n_matches=2048,independent_seed_blocks=64,
        primary=primary,interactions_exploratory=interaction,secondary=secondary,plausibility_descriptive=plausibility,
        arm_means=arm_means,arm_covariance_xgd=covariance,variance_transfer=transfer,
        candidates_exploratory=select_candidates(cube),winner_confirmed=False,
        alias_warning="I=-ABCDE: mains aliased negatively with four-way terms; pair DoDs with three-way terms; no higher-order identification.",
        bootstrap=dict(resamples=BOOTSTRAPS,seed=BOOT_SEED,unit="complete seed block within context")),block_rows


if __name__=="__main__":
    folder=ROOT/"data/tact-001-p1b"
    result,blocks=analyse(rows(folder/"main.jsonl"),read(folder/"manifest.json"))
    write(folder/"effects.json",result)
    import json
    (folder/"block-contrasts.jsonl").write_text("".join(json.dumps(r)+"\n" for r in blocks),encoding="utf8")

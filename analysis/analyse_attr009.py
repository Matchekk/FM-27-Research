"""Frozen complete-block ATTR-009 raw-dose contrast; no native calls."""
from hashlib import sha256
from pathlib import Path
import sys
import numpy as np
from scipy.stats import chi2, nct, t
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.attr009 import ARMS, CONTEXTS, COEFFICIENTS, SECONDARY, matrix
from research.core import config_hash, schedule
from research.native import read, require, rows, write
from research.stats import estimate, holm, metrics

METRICS = ("xgd", *SECONDARY)
BOOTSTRAPS = 20000
BOOT_SEED = int.from_bytes(sha256(b"ATTR-009-Bridge/bootstrap-v1").digest()[:8], "little")
SCHEDULER_SEED = 2026111409


def validate_design(c):
    d, b, s = c["design"], c["budget"], c["science"]
    require(c["experiment_id"] == "ATTR-009-Bridge" and c["metrics"]["primary"] == "xgd", "Experiment/primary drift")
    require(d["matrix"] == matrix() and d["matrix_sha256"] == config_hash(matrix()), "Mask/raw design drift")
    require([a["id"] for a in d["arms"]] == list(ARMS) and d["n_blocks"] == 16 and
            d["sides"] == [0, 1] and [h["id"] for h in d["scenarios"]] == list(CONTEXTS), "Cell/count drift")
    require(s["contrast_coefficients"] == list(COEFFICIENTS) and
            s["secondary_endpoints"] == list(SECONDARY) and s["family_size"] == 5, "Contrast/family drift")
    require(b["max_matches"] == 384 and b["max_technical_attempts"] == 33 and
            b["max_workers"] == 4 and b["timeout_seconds"] == 90 and
            b["total_native_wall_seconds"] == 600 and b["absolute_study_wall_seconds"] == 1200, "Budget drift")


def checked(data, receipt):
    validate_design(receipt["config"])
    expected = {j["key"]: j for j in schedule(receipt)}
    require(len(expected) == 384, "Exactly384 scheduled matches required")
    cube = np.full((2, 16, 2, 6, 6), np.nan)
    seen = set()
    for row in data:
        require(row["key"] in expected and row["key"] not in seen, "Unexpected/duplicate observation")
        j = expected[row["key"]]; seen.add(row["key"])
        require(row.get("input_contract_verified") is True and row.get("profile_fields_verified") == 1058 and
                row.get("native_roles_verified") == 44 and row.get("native_pi_groups_verified") == 748 and
                row.get("native_pi_cells_verified") == 44 and row.get("native_raw_dose_verified") is True and
                row.get("design_matrix_sha256") == config_hash(matrix()) and
                0 < row["finish_tick"] < 47996, "Input gate missing")
        require(all(row.get(k) == v for k, v in j["identity"].items()) and
                all(row.get(k) == j[k] for k in ("scenario", "seed", "arm", "setup_sha256", "config_sha256")) and
                row["tested_side"] == j["side"], "Identity/setup/seed drift")
        h = CONTEXTS.index(j["scenario"])
        i = receipt["seeds"][h*16:(h+1)*16].index(j["seed"])
        values = metrics(row)
        cube[h, i, j["side"], ARMS.index(j["arm"])] = [values[m] for m in METRICS]
    require(seen == set(expected) and np.isfinite(cube).all(), "Incomplete blocks: technical status only")
    return cube


def summarize(value):
    cells = value.mean(axis=2)
    result = estimate(list(cells), resamples=BOOTSTRAPS, bootstrap_seed=BOOT_SEED)
    result["context"] = {h: dict(mean=float(cells[k].mean()), sd=float(cells[k].std(ddof=1)),
        sd_upper95_normal_model=float(cells[k].std(ddof=1)*np.sqrt(15/chi2.ppf(.05,15))),
        side0_sd=float(value[k,:,0].std(ddof=1)), side1_sd=float(value[k,:,1].std(ddof=1)),
        side_covariance=float(np.cov(value[k].T)[0,1])) for k,h in enumerate(CONTEXTS)}
    loo = [float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(16)]
    result["leave_one_out"] = dict(range=[min(loo),max(loo)],max_change=max(abs(x-result["mean"]) for x in loo))
    return result


def future_planning(sd):
    def case(values):
        def properties(n, effect):
            v = np.asarray(values)**2/(4*n); variance = float(v.sum())
            if not variance: return dict(full_width=0., power=1.)
            df = float(variance**2/(v*v/(n-1)).sum()); se=np.sqrt(variance); cutoff=t.isf(.025,df)
            return dict(full_width=float(2*cutoff*se),power=float(nct.cdf(-cutoff,df,effect/se)+nct.sf(cutoff,df,effect/se)))
        cases=[]
        for effect in (.2,.3):
            lo,hi=1,2
            while properties(hi,effect)["power"]<.9:
                hi*=2;require(hi<=10000000,"Unrealistic sample requirement")
            while hi-lo>1:
                mid=(hi+lo)//2
                if properties(mid,effect)["power"]>=.9:hi=mid
                else:lo=mid
            cases.append(dict(effect=effect,seeds_per_context=hi,independent_blocks=2*hi,matches=24*hi,**properties(hi,effect)))
        return dict(sd=values,power90=cases)
    upper=[float(s*np.sqrt(15/chi2.ppf(.025,15))) for s in sd]
    return dict(assumptions="conditional equal-context noncentral Welch approximation; normal-model SD bounds; new seeds required",
                observed=case(sd),simultaneous95_sd_upper=case(upper))


def analyse(data, receipt):
    cube=checked(data,receipt)
    contrasts=np.einsum("hisam,a->hism",cube,np.asarray(COEFFICIENTS))
    primary=summarize(contrasts[:,:,:,0])
    secondary={m:summarize(contrasts[:,:,:,METRICS.index(m)]) for m in SECONDARY}
    for key,p in zip(secondary,holm([s["p"] for s in secondary.values()]),strict=True):
        secondary[key].update(p_holm=p,reject_holm=p<=.05)
    blocks=[dict(scenario=h,seed=receipt["seeds"][j*16+i],contrast="mask_x_relative_attribute",endpoint=m,
                 value=float(contrasts[j,i,:,k].mean())) for j,h in enumerate(CONTEXTS) for i in range(16) for k,m in enumerate(METRICS)]
    return dict(experiment_id="ATTR-009-Bridge",n_matches=384,independent_seed_blocks=32,
        primary=primary,secondary=secondary,planning=future_planning([primary["context"][h]["sd"] for h in CONTEXTS]),
        arm_means={h:{a:{m:float(cube[j,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)},
        global_ranking_claimed=False,mechanism_decomposition_identified=False,career_transfer_confirmed=False,
        raw_intervention="60->80; no FM in-game display calibration",bootstrap=dict(seed=BOOT_SEED,resamples=BOOTSTRAPS)),blocks


if __name__ == "__main__":
    import json
    folder=ROOT/"data/attr-009-bridge"
    result,blocks=analyse(rows(folder/"main.jsonl"),read(folder/"manifest.json"))
    write(folder/"effects.json",result)
    (folder/"block-contrasts.jsonl").write_text("".join(json.dumps(r)+"\n" for r in blocks),encoding="utf8")

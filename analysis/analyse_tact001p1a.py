"""Offline, exploratory P0 reanalysis and conditional precision/cost forecasts.

No native runner, game API, seed reservation or process launcher is imported.
"""
from hashlib import sha256
from itertools import product
from math import sqrt
from pathlib import Path
import json

import numpy as np
from scipy.stats import chi2, nct, t, trim_mean

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/tact-001-p0"
DEST=ROOT/"data/tact-001-p1a"
CONTEXTS=("high_press","deep_block")
ARMS=("baseline","press","line","combined")
METRICS=("xgd","gf","ga","gd","points")
CONTRASTS={
    "press_isolated":(-1,1,0,0),
    "line_isolated":(-1,0,1,0),
    "combined":(-1,0,0,1),
    "interaction":(1,-1,-1,1),
    "press_marginal":(-.5,.5,-.5,.5),
    "line_marginal":(-.5,-.5,.5,.5),
}
BOOTSTRAPS=20000
BOOT_SEED=2026111401


def read(path):
    return json.loads(Path(path).read_text(encoding="utf8"))


def text_digest(path):
    """Git-canonical LF text hash, independent of checkout core.autocrlf."""
    return sha256(Path(path).read_bytes().replace(b"\r\n",b"\n")).hexdigest()


def save(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+"\n",encoding="utf8")


def load():
    manifest=read(SOURCE/"manifest.json")
    rows=[json.loads(line) for line in (SOURCE/"main.jsonl").read_text(encoding="utf8").splitlines()]
    if len(rows)!=128:
        raise ValueError("Expected 128 complete P0 observations")
    cube=np.empty((2,8,2,4,5))
    seen=set()
    for row in rows:
        h=CONTEXTS.index(row["scenario"]);side=row["tested_side"];arm=ARMS.index(row["arm"])
        i=manifest["seeds"][h*8:(h+1)*8].index(row["seed"])
        key=(h,i,side,arm)
        if key in seen or row["status"]!="ok" or not row["input_contract_verified"]:
            raise ValueError("Duplicate/invalid P0 observation")
        for field,value in manifest["config"]["identity"].items():
            if row.get(field)!=value:
                raise ValueError("P0 identity mismatch")
        if row["setup_sha256"]!=manifest["config"]["design"]["setups"][row["scenario"]][str(side)][row["arm"]]:
            raise ValueError("P0 setup mismatch")
        seen.add(key)
        own,other=row["team_statistics"][side],row["team_statistics"][1-side]
        gf,ga=row["score"][side],row["score"][1-side]
        cube[key]=[own["xg"]-other["xg"],gf,ga,gf-ga,3 if gf>ga else int(gf==ga)]
    if len(seen)!=128 or not np.isfinite(cube).all():
        raise ValueError("Incomplete P0 cube")
    return manifest,cube


def estimate(cells,alpha=.05):
    """Fixed context weights 1/2; independent complete seed contrasts within context."""
    values=[np.asarray(c,dtype=float) for c in cells]
    mean=float(sum(c.mean()/2 for c in values))
    terms=[float(c.var(ddof=1)/(4*len(c))) for c in values]
    variance=sum(terms)
    if variance:
        df=variance**2/sum(v*v/(len(c)-1) for v,c in zip(terms,values))
        half=float(t.isf(alpha/2,df)*sqrt(variance))
        p=float(2*t.sf(abs(mean)/sqrt(variance),df))
    else:
        df=None;half=0.;p=float(mean==0)
    return dict(mean=mean,se=sqrt(variance),df=df,ci95=[mean-half,mean+half],p=p)


def forecast(variances,counts,alpha=.05,effect=.2):
    terms=[float(v/(4*n)) for v,n in zip(variances,counts)]
    variance=sum(terms)
    if variance==0:
        return dict(variance=0.,se=0.,half_width=0.,power=1.)
    df=variance**2/sum(v*v/(n-1) for v,n in zip(terms,counts))
    cutoff=float(t.isf(alpha/2,df));nc=effect/sqrt(variance)
    power=float(nct.cdf(-cutoff,df,nc)+nct.sf(cutoff,df,nc))
    return dict(variance=variance,se=sqrt(variance),df=df,half_width=cutoff*sqrt(variance),
                power=power,alpha=alpha,effect=effect)


def allocation(variances,budget,cost,min_per_context=8,optimal=False):
    """Integer n minimises fixed-weight variance, without changing context weights."""
    total=budget//cost
    if total<2*min_per_context:
        raise ValueError("Budget below minimum context replication")
    if optimal:
        first=min(range(min_per_context,total-min_per_context+1),
                  key=lambda n:variances[0]/n+variances[1]/(total-n))
    else:
        first=total//2
    counts=[first,total-first]
    return dict(counts=counts,seed_blocks=total,matches=total*cost,unspent_matches=budget-total*cost,
                **forecast(variances,counts))


def fractional_v():
    """Negative half-fraction E=-ABCD includes the all-standard/low anchor."""
    return np.array([(*levels,-int(np.prod(levels))) for levels in product((-1,1),repeat=4)],dtype=int)


def audit_archive(manifest):
    """Read the entire public P0 archive; verify historic technical accounting."""
    for path in SOURCE.glob("*.json"):
        read(path)
    rows={path.name:[json.loads(s) for s in path.read_text(encoding="utf8").splitlines()]
          for path in SOURCE.glob("*.jsonl")}
    technical=rows["technical.jsonl"];accounting=rows["job-accounting.jsonl"]
    assert len(technical)==23 and len(accounting)==152
    assert len({r["key"] for r in accounting})==152
    assert sum(r["status"]=="ok" for r in accounting)==151
    assert sum(r["status"]=="expected_rejection" for r in accounting)==1
    plan=read(SOURCE/"seed-plan.json")
    assert plan["main_seeds"]==manifest["seeds"]
    assert not set(plan["main_seeds"])&set(plan["technical_seeds"])
    groups={}
    for row in technical:
        assert row["status"]=="ok" and row["input_contract_verified"] and row["profile_fields_verified"]==1058
        assert row["seed"] in plan["technical_seeds"]
        assert all(row[key]==value for key,value in manifest["config"]["identity"].items())
        assert row["setup_sha256"]==manifest["config"]["design"]["setups"][row["scenario"]][str(row["tested_side"])][row["arm"]]
        key=(row["scenario"],row["tested_side"],row["arm"])
        groups.setdefault(key,[]).append(row)
    repeats=0
    for group in groups.values():
        for row in group[1:]:
            assert all(row[key]==group[0][key] for key in ("score","finish_tick","team_statistics","seed","setup_sha256"))
            repeats+=1
    assert len(groups)==16 and repeats==7
    diff=read(SOURCE/"binary-diff-audit.json")
    assert diff["passed"] and all(r["undeclared_changes"]==0 for r in diff["comparisons"])
    run=read(SOURCE/"run-summary.json");budget=read(SOURCE/"budget.json")
    assert run["holdout_matches"]==0 and run["excluded_matches"]==0 and run["retries"]==0
    assert abs(run["charged_native_wall_seconds"]-budget["charged_seconds"])<1e-9
    return dict(main_matches=128,technical_matches=23,expected_negative_rejections=1,
                independent_main_blocks=16,exact_repeats=7,accounted_jobs=152,
                historical_charged_child_seconds=budget["charged_seconds"],holdout_matches=0)


def cv_grid(covariance,coef,budget=1000):
    """Finite independent calibration mean; its uncertainty and match cost count."""
    c=np.asarray(coef,dtype=float)
    vd=np.array([float(c@s@c) for s in covariance])
    vb=np.array([float(s[0,0]) for s in covariance])
    cov=np.array([float(c@s[:,0]) for s in covariance])
    paired_cost=2*int(np.count_nonzero(c))
    ordinary=allocation(vd,budget,paired_cost,optimal=True)
    results=[]
    for ratio in (.25,.5,1,2,4,8):
        beta=cov/vb*ratio/(1+ratio)
        residual=vd-2*beta*cov+beta*beta*vb
        effective=residual+beta*beta*vb/ratio
        # Continuous planning approximation, rounded DOWN; cost never exceeds budget.
        n_total=budget/(paired_cost+2*ratio)
        fraction=np.sqrt(effective)/np.sqrt(effective).sum()
        counts=np.floor(n_total*fraction).astype(int)
        calibration=np.ceil(counts*ratio).astype(int)
        while paired_cost*counts.sum()+2*calibration.sum()>budget:
            counts[np.argmax(counts)]-=1
            calibration=np.ceil(counts*ratio).astype(int)
        if min(counts)<2 or min(calibration)<2:
            continue
        cost=int(paired_cost*counts.sum()+2*calibration.sum())
        actual_var=float(sum(residual/(4*counts)+beta*beta*vb/(4*calibration)))
        results.append(dict(calibration_ratio=ratio,paired_blocks=counts.tolist(),calibration_blocks=calibration.tolist(),
            beta=beta.tolist(),matches=cost,se=sqrt(actual_var),variance=actual_var,
            variance_ratio_to_ordinary=actual_var/ordinary["variance"],
            assumptions="P0 covariance transfers, beta frozen before new data, independent new calibration sample; approximate integer allocation"))
    return dict(ordinary_optimally_stratified=ordinary,alternatives=results,
                oracle_known_mean_max_r2=(cov*cov/(vd*vb)).tolist(),
                caveat="Oracle gain excludes unavailable known baseline means; finite-calibration costs above are the realistic comparator.")


def reanalyse(manifest,cube):
    # All methods below reuse ONLY the 16 P0 discovery blocks; none is confirmatory.
    contrasts=np.einsum("hisam,ca->hicsm",cube,np.array(list(CONTRASTS.values())))
    # shape: context, seed, contrast, side, metric
    avg=contrasts.mean(axis=3)
    rng=np.random.default_rng(BOOT_SEED)
    indices=[rng.integers(8,size=(BOOTSTRAPS,8)) for _ in CONTEXTS]
    results={};pvalues=[];keys=[];influence=[];dependence={}
    covariance=[np.cov(cube[h].mean(axis=1)[:,:,0].T) for h in range(2)]
    for ci,name in enumerate(CONTRASTS):
        results[name]={}
        for mi,metric in enumerate(METRICS):
            cells=avg[:,:,ci,mi]
            value=estimate(cells)
            bootstrap=sum(cells[h][indices[h]].mean(axis=1)/2 for h in (0,1))
            value["bootstrap_ci95"]=np.quantile(bootstrap,[.025,.975]).tolist()
            value["context"]={context:dict(mean=float(cells[h].mean()),sd=float(cells[h].std(ddof=1)),
                sd_ci95_normal_assumption=(cells[h].std(ddof=1)*np.sqrt(7/chi2.ppf([.975,.025],7))).tolist(),
                home_sd=float(contrasts[h,:,ci,0,mi].std(ddof=1)),away_sd=float(contrasts[h,:,ci,1,mi].std(ddof=1)),
                home_mean=float(contrasts[h,:,ci,0,mi].mean()),away_mean=float(contrasts[h,:,ci,1,mi].mean()))
                for h,context in enumerate(CONTEXTS)}
            leave=[]
            for h in (0,1):
                for i in range(8):
                    changed=[cells[0],cells[1]]
                    changed[h]=np.delete(changed[h],i)
                    e=estimate(changed)
                    leave.append(e["mean"])
                    if metric=="xgd":
                        influence.append(dict(contrast=name,context=CONTEXTS[h],seed=manifest["seeds"][h*8+i],
                            full_mean=value["mean"],leave_one_out_mean=e["mean"],change=e["mean"]-value["mean"],ci95=e["ci95"]))
            value["leave_one_out"]=dict(mean_range=[min(leave),max(leave)],max_abs_change=max(abs(x-value["mean"]) for x in leave))
            # Sensitivities have different location estimands, not a license to trim data.
            value["robust_sensitivity"]=dict(median_context_average=float(sum(np.median(c)/2 for c in cells)),
                trimmed20_context_average=float(sum(trim_mean(c,.2)/2 for c in cells)),
                caveat="Median/trimmed location differs from the arithmetic mean; no mean-variance gain claimed.")
            results[name][metric]=value;pvalues.append(value["p"]);keys.append((name,metric))
        c=np.array(CONTRASTS[name]);cell_info={}
        for h,context in enumerate(CONTEXTS):
            by_side=contrasts[h,:,ci,:,0]
            S=np.cov(by_side.T)
            paired=float(S.sum()/4);independent=float(np.trace(S)/4)
            paired_arms=float(c@covariance[h]@c)
            independent_arms=float((c*c)@np.diag(covariance[h]))
            cell_info[context]=dict(side_covariance=float(S[0,1]),side_correlation=float(np.corrcoef(by_side.T)[0,1]),
                paired_side_variance=paired,independent_side_counterfactual_variance=independent,
                paired_to_independent_side_variance=paired/independent,
                paired_arm_variance=paired_arms,independent_arm_counterfactual_variance=independent_arms,
                paired_to_independent_arm_variance=paired_arms/independent_arms)
        dependence[name]=cell_info
        dependence[name]["outcome_correlations"]=dict(zip(CONTEXTS,
            [np.corrcoef(avg[h,:,ci,:][:,[0,3,4]].T).tolist() for h in (0,1)]))
    previous=0.
    for rank,index in enumerate(np.argsort(pvalues)):
        previous=max(previous,min(1.,(len(pvalues)-rank)*pvalues[index]))
        name,metric=keys[index]
        results[name][metric]["p_holm30_exploratory"]=previous
    # Block fixed effects: all 16 seed intercepts + context-specific side/P/L/PL.
    design=[];outcome=[]
    for h,i,side,arm in product(range(2),range(8),range(2),range(4)):
        row=np.zeros(24);row[h*8+i]=1
        p=arm in (1,3);line=arm in (2,3)
        row[16+h*4:20+h*4]=[side,p,line,p*line]
        design.append(row);outcome.append(cube[h,i,side,arm,0])
    coef=np.linalg.lstsq(np.asarray(design),outcome,rcond=None)[0]
    block_model={"press_isolated":float((coef[17]+coef[21])/2),"line_isolated":float((coef[18]+coef[22])/2),
                 "interaction":float((coef[19]+coef[23])/2)}
    arm_means={context:{arm:dict(zip(METRICS,cube[h,:,:,a,:].mean(axis=(0,1)).tolist()))
               for a,arm in enumerate(ARMS)} for h,context in enumerate(CONTEXTS)}
    return dict(exploratory=True,contrasts=results,dependence=dependence,arm_means=arm_means,
        arm_covariance_xgd={name:matrix.tolist() for name,matrix in zip(CONTEXTS,covariance)},
        arm_correlation_xgd={name:np.corrcoef(cube[h].mean(axis=1)[:,:,0].T).tolist() for h,name in enumerate(CONTEXTS)},
        block_model=dict(estimates=block_model,independent_clusters=16,naive_match_n_forbidden=128,
                         interpretation="Same point estimates as complete paired contrasts; no additional independent n or proven variance reduction.")),influence,avg,covariance


def design_comparison(analysis,avg,covariance):
    alternatives={};noise=[]
    for h,S in enumerate(covariance):
        tau=float((np.trace(S)-S.sum()/4)/3)
        noise.append(tau)
    for ci,name in enumerate(CONTRASTS):
        variances=avg[:,:,ci,0].var(axis=1,ddof=1)
        cost=8 if name in ("interaction","press_marginal","line_marginal") else 4
        balanced=allocation(variances,1000,cost)
        optimal=allocation(variances,1000,cost,optimal=True)
        fraction=float(np.sqrt(variances[0])/np.sqrt(variances).sum())
        rng=np.random.default_rng(BOOT_SEED+ci)
        boot_sd=np.array([avg[h,rng.integers(8,size=(BOOTSTRAPS,8)),ci,0].std(axis=1,ddof=1) for h in (0,1)])
        denominator=boot_sd.sum(axis=0)
        valid=denominator>0
        fractions=boot_sd[0,valid]/denominator[valid]
        alternatives[name]=dict(cost_per_seed_block=cost,balanced_1000=balanced,optimal_1000=optimal,
            optimal_high_press_fraction=fraction,variance_saved_fraction=1-optimal["variance"]/balanced["variance"],
            optimal_fraction_bootstrap_range95=np.quantile(fractions,[.025,.975]).tolist(),
            allocation_uncertainty_note="Descriptive resampling range from eight blocks/context, not validated future efficiency or a coverage guarantee.",
            information_per_1000=1000/(optimal["matches"]*optimal["variance"]))
    # Independent side strata retain the same fixed target weights 1/4 each.
    side_options={}
    for ci,name in enumerate(CONTRASTS):
        cells=analysis["contrasts"][name]["xgd"]["context"]
        vars4=np.array([cells[h][key]**2 for h in CONTEXTS for key in ("home_sd","away_sd")])
        side_cost=4 if name in ("interaction","press_marginal","line_marginal") else 2
        total=1000//side_cost
        counts=np.repeat(total//4,4);counts[:total%4]+=1
        variance=float(sum(vars4/counts)/16)
        side_options[name]=dict(independent_seed_side_blocks=int(counts.sum()),counts=counts.tolist(),
                                matches=int(counts.sum()*side_cost),se=sqrt(variance),
                                variance_ratio_to_paired_sides=variance/alternatives[name]["balanced_1000"]["variance"],
                                caveat="Counterfactual from P0 marginal variances; independent side seeds were not executed.")
    # Transfer assumption: future factorial contrast noise is exchangeable in the
    # subspace orthogonal to the intercept; tau2 is estimated from P0 only.
    comparisons=[]
    for budget in (512,1024,2048):
        n=budget//64  # 16 cells x 2 sides x 2 equally sampled contexts
        pred=forecast(np.array(noise)/4,[n,n],alpha=.01,effect=.2)
        marginal=forecast(np.array(noise)/4,[n,n],alpha=.05,effect=.2)
        sensitivity={str(k):forecast(np.array(noise)*k/4,[n,n],alpha=.01,effect=.2) for k in (.5,1.,2.,4.)}
        comparisons.append(dict(budget_matches=budget,seed_blocks=2*n,blocks_per_context=n,
            marginal95=marginal,bonferroni5=pred,variance_transfer_sensitivity=sensitivity,
            main_effects=5,two_factor_alias_contrasts=10,
            information_per_1000_per_main=1000/(budget*pred["variance"])))
    # Required future sample size under the explicit tau transfer model.
    requirements=[]
    for multiplier,effect in product((1,2,4),(.1,.15,.2,.3)):
        n=2
        while forecast(np.array(noise)*multiplier/4,[n,n],alpha=.01,effect=effect)["power"]<.9:
            n+=1
        requirements.append(dict(variance_multiplier=multiplier,effect=effect,blocks_per_context=n,
                                 seed_blocks=2*n,matches=64*n))
    sequential={};adaptive={}
    for name in ("press_isolated","line_isolated"):
        v=avg[:,:,list(CONTRASTS).index(name),0].var(axis=1,ddof=1)
        sequential[name]=dict(five_separate_two_arm_tests=allocation(v,200,4),
                              six_arm_shared_anchor=allocation(v,1000,12),
                              note="Estimates isolated effects at a frozen anchor, not five-factor marginal effects; new factors have no measured variance.")
    for name in ("press_isolated","line_isolated","combined"):
        v=avg[:,:,list(CONTRASTS).index(name),0].var(axis=1,ddof=1)
        adaptive[name]=forecast(v,[4,4])
    full_factorial=[dict(main_matches=budget,blocks_per_context=budget//128,
        main_effect=forecast(np.array(noise)/8,[budget//128]*2,alpha=.01,effect=.2)) for budget in (1024,2048)]
    return dict(exploratory_forecasts=True,known_contrasts=alternatives,independent_side_seed_options=side_options,
        control_variates={name:cv_grid(covariance,CONTRASTS[name]) for name in ("press_isolated","line_isolated","combined","interaction")},
        orthogonal_noise_tau2=dict(zip(CONTEXTS,noise)),doe_forecasts=comparisons,
        conditional_90_power_requirements=dict(alpha_per_test=.01,transfer_assumption=True,rows=requirements),
        sequential_screening_at_1000=sequential,full_factorial_forecasts=full_factorial,
        adaptive_new_candidate_round_precision=dict(assumed_blocks_per_context=4,
            analogues=adaptive,note="Unselected two-arm uncertainty using P0 contrast SDs; not surrogate predictive accuracy or valid post-selection inference."),
        warning="New tempo/directness/width variances, higher-order aliases and candidate-selection performance are unmeasured. Forecasts are not demonstrated gains.")


def main():
    manifest,cube=load()
    archive_audit=audit_archive(manifest)
    analysis,influence,avg,covariance=reanalyse(manifest,cube)
    designs=design_comparison(analysis,avg,covariance)
    # Reproduce P0 independently; do not write into its archive.
    prior=read(SOURCE/"effects.json")["primary"]
    now=analysis["contrasts"]["interaction"]["xgd"]
    np.testing.assert_allclose([now["mean"],now["p"],*now["ci95"]],
                               [prior["mean"],prior["p"],*prior["ci"]],rtol=1e-12,atol=1e-12)
    source_paths=sorted(SOURCE.glob("*"))
    document_paths=sorted((ROOT/"experiments").glob("TACT-001-P0-*.md"))
    code_paths=[ROOT/"analysis"/name for name in ("analyse_tact001p0.py","verify_tact001p0.py","run_tact001p0.py","export_tact001p0.py","report_tact001p0.py")]
    code_paths.append(ROOT/"research/specs/TACT-001-P0.json")
    fingerprints={p.relative_to(ROOT).as_posix():text_digest(p) for p in [*source_paths,*document_paths,*code_paths] if p.is_file()}
    save(DEST/"source-manifest.json",dict(source_commit="873799a4eb4f233d2b894a579e53e409f64140fb",sha256=fingerprints,
        hash_policy="SHA256 of UTF-8 text with CRLF normalized to Git-canonical LF; game binary hashes remain raw SHA256",
        historical_archive_audit=archive_audit,analysis_sha256=text_digest(__file__),
        source_matches=128,source_independent_blocks=16,native_matches_started=0,new_seeds_reserved=0,
        bootstrap_resamples=BOOTSTRAPS,bootstrap_seed=BOOT_SEED,all_new_analyses_exploratory=True))
    save(DEST/"exploratory-effects.json",analysis)
    save(DEST/"design-comparison.json",designs)
    (DEST/"seed-influence.jsonl").write_text("".join(json.dumps(row,allow_nan=False)+"\n" for row in influence),encoding="utf8")
    save(DEST/"resolution-v-design.json",dict(factors=["pressing","defensive_line","tempo","directness","width"],
         generator="E=-A*B*C*D",defining_relation="I=-ABCDE",levels=fractional_v().tolist(),executed=False,seeds=[]))
    print("P0 primary reproduced; wrote exploratory reanalysis and conditional design forecasts. Native matches: 0.")


if __name__=="__main__":
    main()

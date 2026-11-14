"""Complete paired-block split-field analysis, independent of native execution."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import chi2,nct,t

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from analysis.split004_design import (EXPERIMENT,ARMS,CONTEXTS,OBSERVER_HOST,COEFFICIENTS,
    SECONDARY,SECONDARY_PAIRS,DESCRIPTIVE,treatment,validate_design)
from research.core import schedule
from research.native import require
from research.stats import estimate,holm,metrics

METRICS=('xgd',*SECONDARY)
BOOTSTRAPS=20000
BOOT_SEED=int.from_bytes(sha256(b'MECH-004-SPLIT-R0/bootstrap-v1').digest()[:8],'little')
SCHEDULER_SEED=2026111423
AUDIT_BOOLS=('input_verified','seed_verified','split_start_verified','stamina60_verified','pressing_verified','controls_verified')


def check_descriptive(row,tr):
    values=row['descriptive'];missing=row['descriptive_missing_reasons']
    require(set(values)==set(DESCRIPTIVE) and type(missing) is dict,'Descriptive family drift')
    absent={k for k,v in values.items() if v is None}
    allowed={'finished_condition_cache89_mean','finished_sharpness_cache8a_mean'}
    require(absent<=allowed and set(missing)==absent and all(type(v) is str and v.strip() for v in missing.values()),
            'Missing descriptive observations require explicit reasons; no silent zero')
    for stage in ('prepared','first'):
        require(type(values[f'{stage}_tf33_matches_frozen_d00']) is bool and values[f'{stage}_tf33_matches_frozen_d00'] is True and
                values[f'{stage}_condition_cache89_mean']==100,
                'Initial native cache/rawTF control differs')
    count=values['finished_tf33_distinct_hashes']
    require(type(count) is int and 1<=count<=10,'Ten actor rawTF patterns include all-zero as one pattern')
    for key,value in values.items():
        if key in ('prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00','finished_tf33_distinct_hashes') or value is None:continue
        require(type(value) in (int,float) and np.isfinite(value),'Nonfinite/malformed descriptive value')
        if '_cache' in key:require(0<=value<=255,'Runtime cache byte mean outside physical bounds')
    return values


def checked(data,receipt):
    validate_design(receipt['config'],executable=True)
    expected={j['key']:j for j in schedule(receipt)}
    require(len(expected)==512,'Exactly512 main jobs required')
    cube=np.full((2,32,2,4,len(METRICS)),np.nan);seen=set()
    for row in data:
        key=row['job_id'];require(key in expected and key not in seen,'Unexpected/duplicate main observation')
        j=expected[key];seen.add(key);tr=treatment(j['arm']);audit=row['native_audit']
        require(row['experiment_id']==EXPERIMENT and row['status']=='ok' and type(row['seed']) is int and type(row['team_side']) is int and
                row['identity']==j['identity'] and row['observer_host_sha256']==OBSERVER_HOST and
                row['context']==j['scenario'] and row['team_side']==j['side'] and
                all(row[k]==j[k] for k in ('seed','arm','setup_sha256','config_sha256')),'Identity/seed/setup/context/side mismatch')
        require(all(audit.get(k) is True for k in AUDIT_BOOLS) and all(type(audit[k]) is int for k in (
                'attribute_values_verified','profile_fields_verified','phase_cells_verified','pi_groups_verified','c90_raw','c7a_raw','pressing_bit')) and
                audit['attribute_values_verified']==3174 and
                audit['profile_fields_verified']==1058 and audit['phase_cells_verified']==44 and audit['pi_groups_verified']==748 and
                audit['c90_raw']==tr['c90_raw'] and audit['c7a_raw']==tr['c7a_raw'] and audit['pressing_bit']==0,
                'Native input/start-package audit missing or wrong')
        result=row['result'];require(type(result['tick']) is int and 0<result['tick']<47996 and
            type(result['clock']) is int and result['clock']>=0,'Missing/nonnatural finish')
        check_descriptive(row,tr)
        values=metrics(dict(status=row['status'],engine_readback=True,tested_side=row['team_side'],
            score=result['score'],team_statistics=result['team_statistics']))
        h=CONTEXTS.index(j['scenario']);i=receipt['seeds'][h*32:(h+1)*32].index(j['seed'])
        cube[h,i,j['side'],ARMS.index(j['arm'])]=[values[m] for m in METRICS]
    require(seen==set(expected) and np.isfinite(cube).all(),'Incomplete blocks: publish technical status only')
    return cube


def summarize(value):
    cells=value.mean(axis=2)
    out=estimate(list(cells),resamples=BOOTSTRAPS,bootstrap_seed=BOOT_SEED)
    out['context']={h:dict(mean=float(cells[k].mean()),sd=float(cells[k].std(ddof=1)),
        sd_upper95_normal_model=float(cells[k].std(ddof=1)*np.sqrt(31/chi2.ppf(.05,31))),
        side0_mean=float(value[k,:,0].mean()),side1_mean=float(value[k,:,1].mean()),
        side0_sd=float(value[k,:,0].std(ddof=1)),side1_sd=float(value[k,:,1].std(ddof=1)),
        side_covariance=float(np.cov(value[k].T)[0,1])) for k,h in enumerate(CONTEXTS)}
    loo=[float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(32)]
    out['leave_one_out']=dict(range=[min(loo),max(loo)],max_change=max(abs(v-out['mean']) for v in loo))
    return out


def future_planning(sd):
    require(len(sd)==2 and all(np.isfinite(s) and s>=0 for s in sd),'Two nonnegative finite context SDs required')
    def case(values):
        def properties(n,effect):
            parts=np.asarray(values)**2/(4*n);variance=float(parts.sum())
            if not variance:return dict(full_width=0.,power=1.)
            df=float(variance**2/(parts*parts/(n-1)).sum());se=np.sqrt(variance);cut=t.isf(.025,df)
            # Symmetry P(T_nc < -cut)=P(T_-nc > cut) avoids SciPy's
            # negative-tail CDF NaNs for some small-df noncentralities.
            power=float(nct.sf(cut,df,-effect/se)+nct.sf(cut,df,effect/se))
            require(np.isfinite(power) and 0<=power<=1,'Nonfinite prospective power')
            return dict(full_width=float(2*cut*se),power=power)
        plan=[]
        for effect in (.2,.3):
            lo,hi=1,2
            while properties(hi,effect)['power']<.9:
                hi*=2;require(hi<=10000000,'Unrealistic future requirement')
            while hi-lo>1:
                mid=(lo+hi)//2
                if properties(mid,effect)['power']>=.9:hi=mid
                else:lo=mid
            plan.append(dict(effect=effect,seeds_per_context=hi,independent_blocks=2*hi,matches=16*hi,**properties(hi,effect)))
        return dict(sd=[float(s) for s in values],power90=plan)
    upper=[float(s*np.sqrt(31/chi2.ppf(.025,31))) for s in sd]
    return dict(assumptions='Conditional noncentral-Welch planning with new seeds in the two existing contexts; joint95 SD upper bounds assume normal seed contrasts, each97.5percent/df31. No automatic followup.',
        observed=case(sd),simultaneous95_sd_upper=case(upper))


def describe(data):
    out={}
    for h in CONTEXTS:
        out[h]={}
        for arm in ARMS:
            group=sorted((r for r in data if r['context']==h and r['arm']==arm),key=lambda r:r['job_id']);table={}
            for key in DESCRIPTIVE:
                values=[r['descriptive'][key] for r in group if r['descriptive'][key] is not None]
                reasons=Counter(r['descriptive_missing_reasons'][key] for r in group if r['descriptive'][key] is None)
                table[key]=dict(observed=len(values),missing=sum(reasons.values()),missing_reasons=dict(reasons),
                    mean=float(np.mean(values)) if values else None,min=min(values) if values else None,max=max(values) if values else None)
            out[h][arm]=table
    return dict(interpretation='Descriptive raw/cache quantities only: no pvalues, UI, consumer or mediation interpretation.',by_context_arm=out)


def analyse(data,receipt):
    data=list(data)
    cube=checked(data,receipt)
    contrasts={name:np.einsum('hisam,a->hism',cube,np.asarray(weights)) for name,weights in COEFFICIENTS.items()}
    primary=summarize(contrasts['ATTRIBUTION'][:,:,:,0])
    secondary={f'{name}:{metric}':summarize(contrasts[name][:,:,:,METRICS.index(metric)]) for name,metric in SECONDARY_PAIRS}
    for key,p in zip(secondary,holm([v['p'] for v in secondary.values()]),strict=True):secondary[key].update(p_holm=p,reject_holm=p<=.05)
    blocks=[dict(context=h,seed=receipt['seeds'][j*32+i],contrast=name,endpoint=metric,
                 value=float(contrasts[name][j,i,:,METRICS.index(metric)].mean()))
        for name,metric in [('ATTRIBUTION','xgd'),*SECONDARY_PAIRS] for j,h in enumerate(CONTEXTS) for i in range(32)]
    return dict(experiment_id=EXPERIMENT,n_matches=512,independent_seed_blocks=64,primary_contrast='ATTRIBUTION',primary=primary,
        secondary=secondary,planning=future_planning([primary['context'][h]['sd'] for h in CONTEXTS]),descriptive=describe(data),
        arm_means={h:{a:{m:float(cube[j,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)},
        practical_reference=.2,desired_full_ci_width=.5,bootstrap=dict(seed=BOOT_SEED,resamples=BOOTSTRAPS),
        intervention='C90 high-minus-low effect minus C7A high-minus-low effect = HL-LH; independently preserved original start fields, stamina60 fixed',
        exploratory_context_and_side_only=True,ui_scale_calibrated=False,consumer_semantics_validated=False,
        mediation_identified=False,career_transfer_confirmed=False,winner_selected=False),blocks

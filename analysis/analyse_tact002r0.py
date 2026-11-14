"""Preregistered TACT-002-R0 full ST x AMC factorial analysis; no native calls."""
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
from analyse_tact001p1b import CONTEXTS,PLAUSIBILITY,endpoints
ARMS=('R00','R10','R01','R11')
FACTORS=(dict(code='ST',position='ST',phase=0,low_role='CentreForward',low_flags=2048,high_role='DeepLyingForward',high_flags=1024),
         dict(code='AMC',position='AMC',phase=0,low_role='AttackingMidfielder',low_flags=512,high_role='SecondStriker',high_flags=2199023255552))
SECONDARY=('points','gf','ga','xgf','xga')
SECONDARY_PAIRS=(('AMC','xgd'),('STxAMC','xgd'),*(('ST',m) for m in SECONDARY))
METRICS=('xgd',*SECONDARY,*PLAUSIBILITY)
COEFFICIENTS={'ST':(-.5,.5,-.5,.5),'AMC':(-.5,-.5,.5,.5),'STxAMC':(1.,-1.,-1.,1.)}
BOOTSTRAPS=20000
BOOT_SEED=int.from_bytes(sha256(b'TACT-002-R0/bootstrap-v1').digest()[:8],'little')
SCHEDULER_SEED=2026111406

def matrix():
    return [dict(id=a,levels={'ST':st,'AMC':amc}) for a,(st,amc) in zip(ARMS,((-1,-1),(1,-1),(-1,1),(1,1)),strict=True)]

def wanted_flags(arm):
    levels=matrix()[ARMS.index(arm)]['levels']
    return {f['code']:f['high_flags'] if levels[f['code']]==1 else f['low_flags'] for f in FACTORS}

def validate_design(c):
    d=c['design'];b=c['budget'];s=c['science']
    require(c['experiment_id']=='TACT-002-R0' and c['metrics']['primary']=='xgd','Wrong experiment/primary')
    require(d['matrix']==matrix() and d['matrix_sha256']==config_hash(matrix()) and d['factors']==list(FACTORS),'Role design mismatch')
    require([a['id'] for a in d['arms']]==list(ARMS) and d['control_arm']=='R00','Wrong arm order/control')
    require(d['n_blocks']==32 and d['sides']==[0,1] and [h['id'] for h in d['scenarios']]==list(CONTEXTS),'Sample/context mismatch')
    require(s['primary_contrast']=='ST' and s['secondary_contrasts']==[list(p) for p in SECONDARY_PAIRS] and s['secondary_family_size']==7,'Contrast/family mismatch')
    require(b['max_matches']==512 and b['max_technical_attempts']==33 and b['max_workers']==4 and b['timeout_seconds']==90 and b['total_native_wall_seconds']==900 and b['absolute_study_wall_seconds']==1800,'Budget mismatch')

def checked(data,r):
    validate_design(r['config']);expected={j['key']:j for j in schedule(r)}
    require(len(expected)==512,'Exactly512 jobs required');cube=np.empty((2,32,2,4,len(METRICS)));seen=set()
    for row in data:
        require(row['key'] in expected and row['key'] not in seen,'Unexpected/duplicate match');j=expected[row['key']];seen.add(row['key'])
        require(row['status']=='ok' and row.get('input_contract_verified') is True and row.get('profile_fields_verified')==1058 and 0<row['finish_tick']<47996,'Unverified main match')
        require(all(row.get(k)==v for k,v in j['identity'].items()) and all(row.get(k)==j[k] for k in ('setup_sha256','config_sha256','scenario','seed','arm')) and row['tested_side']==j['side'],'Identity/setup/seed mismatch')
        a=ARMS.index(j['arm']);level=matrix()[a]['levels']
        require(row.get('factor_levels')==level and row.get('native_role_flags')==wanted_flags(j['arm']) and row.get('design_matrix_sha256')==config_hash(matrix()) and row.get('native_roles_verified')==44 and row.get('native_pi_cells_verified')==44 and row.get('native_pi_groups_verified')==748,'Native roles/PI/design mismatch')
        h=CONTEXTS.index(j['scenario']);i=r['seeds'][h*32:(h+1)*32].index(j['seed']);values=endpoints(row)
        cube[h,i,j['side'],a]=[values[m] for m in METRICS]
    require(seen==set(expected) and np.isfinite(cube).all(),'Incomplete blocks: technical status only')
    return cube

def summarize(v):
    cells=v.mean(axis=2);z=estimate(list(cells),resamples=BOOTSTRAPS,bootstrap_seed=BOOT_SEED)
    z['context']={h:dict(mean=float(cells[k].mean()),sd=float(cells[k].std(ddof=1)),side0_mean=float(v[k,:,0].mean()),side1_mean=float(v[k,:,1].mean()),side0_sd=float(v[k,:,0].std(ddof=1)),side1_sd=float(v[k,:,1].std(ddof=1)),side_covariance=float(np.cov(v[k].T)[0,1])) for k,h in enumerate(CONTEXTS)}
    loo=[float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(32)]
    z['leave_one_out']=dict(range=[min(loo),max(loo)],max_change=max(abs(x-z['mean']) for x in loo))
    return z

def future_planning(sd):
    # Conditional fixed equal-context noncentral Welch-t approximation, not observed power.
    upper=[float(s*np.sqrt(31/chi2.ppf(.025,31))) for s in sd]
    def properties(s,n,e):
        v=np.array(s)**2/(4*n);variance=float(v.sum())
        if not variance:return dict(full_width=0.,power=1.)
        df=float(variance**2/(v*v/(n-1)).sum());se=np.sqrt(variance);cut=t.isf(.025,df)
        return dict(full_width=float(2*cut*se),power=float(nct.cdf(-cut,df,e/se)+nct.sf(cut,df,e/se)))
    def minimum(s,e):
        lo,hi=1,2
        while properties(s,hi,e)['power']<.9:
            hi*=2;require(hi<=10000000,'Unrealistic future sample requirement')
        while hi-lo>1:
            mid=(hi+lo)//2
            if properties(s,mid,e)['power']>=.9:hi=mid
            else:lo=mid
        return hi
    return dict(assumptions='New equal-context seeds, current variance only; noncentral Welch-t approximation. Joint95 normal-model SD upper bounds use each97.5% chi-square bound. No transfer guarantee or automatic execution.',
        cases={label:dict(sd=s,power90=[dict(effect=e,seeds_per_context=(n:=minimum(s,e)),independent_blocks=2*n,matches=16*n) for e in (.2,.3)]) for label,s in [('observed',sd),('simultaneous95_normal_model_upper',upper)]})

def analyse(data,r):
    cube=checked(data,r);contrasts={k:np.einsum('hisam,a->hism',cube,np.asarray(c)) for k,c in COEFFICIENTS.items()}
    primary=summarize(contrasts['ST'][:,:,:,0]);secondary={f'{c}:{m}':summarize(contrasts[c][:,:,:,METRICS.index(m)]) for c,m in SECONDARY_PAIRS}
    for key,p in zip(secondary,holm([v['p'] for v in secondary.values()]),strict=True):secondary[key].update(p_holm=p,reject_holm=p<=.05)
    blocks=[dict(context=h,seed=r['seeds'][j*32+i],contrast=c,endpoint='xgd',value=float(v[j,i,:,0].mean())) for c,v in contrasts.items() for j,h in enumerate(CONTEXTS) for i in range(32)]
    return dict(experiment_id='TACT-002-R0',evidence='preregistered_role_variance_pilot_in_synthetic_discovery_context',n_matches=512,independent_seed_blocks=64,primary_contrast='ST',primary=primary,secondary=secondary,
        actual_arm_means={h:{a:{m:float(cube[j,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)},
        contrast_covariance_xgd={h:np.cov(np.stack([v[j,:,:,0].mean(axis=1) for v in contrasts.values()])).tolist() for j,h in enumerate(CONTEXTS)},
        planning=future_planning([primary['context'][h]['sd'] for h in CONTEXTS]),practical_screening_effect=.3,desired_full_ci_width=.5,
        winner_selected=False,optimal_tactic_confirmed=False,career_transfer_confirmed=False,bootstrap=dict(seed=BOOT_SEED,resamples=BOOTSTRAPS)),blocks

if __name__=='__main__':
    import json
    folder=ROOT/'data/tact-002-r0';z,b=analyse(rows(folder/'main.jsonl'),read(folder/'manifest.json'));write(folder/'effects.json',z)
    (folder/'block-contrasts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in b),encoding='utf8')

"""Frozen ST role package x raw54 Jumping Reach interaction; no CA claims."""
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import numpy as np
from scipy.stats import t, nct, chi2

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.native import require, read, rows
from research.stats import estimate, holm, metrics

ARMS=('A','B','C','D');CONTEXTS=('high_press','deep_block');N=256
WEIGHTS={'INTERACTION':(1.,-1.,-1.,1.),'JR_CF':(-1.,1.,0.,0.),'JR_DLF':(0.,0.,-1.,1.),
         'ROLE':(-.5,-.5,.5,.5),'JR':(-.5,.5,-.5,.5)}
METRICS=('xgd','points','gf','ga','xgf','xga')
BOOT_SEED=2026111540
PUB=ROOT/'data/player-development-001-role'

def planning():
    anchors={}
    # No performance data from the new study are inspected for this choice.
    for sd in (.6,1.,1.2,1.5):
        se=sd/np.sqrt(2*N);df=2*N-2;cut=t.isf(.025,df)
        anchors[str(sd)]=dict(block_sd=sd,full95width=float(2*cut*se),
            power_for_point15=float(nct.cdf(-cut,df,.15/se)+nct.sf(cut,df,.15/se)))
    prior=read(ROOT/'data/tact-002-r0/effects.json')['secondary']['STxAMC:xgd']
    return dict(assumptions='Equal independent context-seed blocks; normal Welch approximation; role x role is only a variance anchor for role x attribute, never a guarantee.',
        sensitivity=anchors,prior_role_interaction_sd={h:prior['context'][h]['sd'] for h in CONTEXTS},
        n_per_context=N,independent_blocks=2*N,matches=16*N,practical_reference=.15,desired_full95width=.20,
        stop='4096 scientific calls, no interim outcomes or outcome-dependent expansion.')

def checked(data):
    plan=read(PUB/'main-plan.json');f=read(PUB/'inputs.json');seeds=read(PUB/'seed-plan.json')['main_seeds']
    expected={j['key']:j for j in plan};require(len(data)==len(expected)==4096,'Complete4096 required')
    cube=np.full((2,N,2,4,6),np.nan);seen=set()
    for row in data:
        k=row['job_id'];require(k in expected and k not in seen,'Unexpected/duplicate job');seen.add(k);j=expected[k]
        require(row['status']=='ok' and row['experiment_id']=='PD-ROLE-001' and row['identity']==f['identity'] and
            row['seed']==j['seed'] and row['context']==j['scenario'] and row['arm']==j['arm'] and row['team_side']==j['side'] and
            row['setup_sha256']==f['setups'][f"{j['scenario']}-{j['side']}"][j['arm']] and row['config_sha256']==f['configs_sha256'],
            'Result identity mismatch')
        require(row['returncode']==0 and all(row['native_audit'][key] is True for key in
                ('input_verified','start_state_verified','controls_verified','game_rules_verified')),'Native gate missing')
        require([row['native_audit'][k] for k in ('attribute_values_verified','profile_fields_verified','phase_cells_verified','pi_groups_verified')]
                ==[3174,1058,44,748],'Readback coverage drift')
        h=CONTEXTS.index(j['scenario']);i=seeds[h*N:(h+1)*N].index(j['seed']);r=row['result']
        require(type(r['tick']) is int and 0<r['tick']<47996,'Nonnatural finish')
        m=metrics(dict(status='ok',engine_readback=True,tested_side=j['side'],score=r['score'],team_statistics=r['team_statistics']))
        cube[h,i,j['side'],ARMS.index(j['arm'])]=[m[x] for x in METRICS]
    require(np.isfinite(cube).all(),'Missing values: no imputation')
    return cube

def analyse(data):
    cube=checked(data);seed_values={k:np.einsum('hisam,a->hism',cube,v).mean(axis=2) for k,v in WEIGHTS.items()}
    def summary(values):
        out=estimate(list(values),resamples=20000,bootstrap_seed=BOOT_SEED)
        out['context']={h:dict(mean=float(values[i].mean()),sd=float(values[i].std(ddof=1))) for i,h in enumerate(CONTEXTS)}
        return out
    primary=summary(seed_values['INTERACTION'][:,:,0])
    # Five metric interactions and the predeclared high_press minus deep_block
    # interaction contrast form ONE Holm6 family.
    secondary={f'INTERACTION:{m}':summary(seed_values['INTERACTION'][:,:,METRICS.index(m)]) for m in METRICS[1:]}
    v=seed_values['INTERACTION'][:,:,0]
    context=estimate([2*v[0],-2*v[1]],resamples=20000,bootstrap_seed=BOOT_SEED)
    secondary['CONTEXT_DIFFERENCE:xgd']=context
    for key,p in zip(secondary,holm([v['p'] for v in secondary.values()]),strict=True):secondary[key]['p_holm']=p
    descriptive={k:{m:summary(values[:,:,l]) for l,m in enumerate(METRICS)} for k,values in seed_values.items() if k!='INTERACTION'}
    primary.update(practical_reference=.15,full_ci_width=primary['ci'][1]-primary['ci'][0],
        excludes_effects_outside_point15=primary['ci'][0]>-.15 and primary['ci'][1]<.15)
    seeds=read(PUB/'seed-plan.json')['main_seeds']
    contrasts=[dict(context=h,seed=seeds[i*N+j],interaction_xgd=float(seed_values['INTERACTION'][i,j,0]))
               for i,h in enumerate(CONTEXTS) for j in range(N)]
    return dict(experiment_id='PD-ROLE-001',n_matches=4096,independent_blocks=512,primary=primary,secondary=secondary,
        descriptive_only=descriptive,arm_means={h:{a:{m:float(cube[i,:,:,k,l].mean()) for l,m in enumerate(METRICS)}
        for k,a in enumerate(ARMS)} for i,h in enumerate(CONTEXTS)},bootstrap_resamples=20000,bootstrap_seed=BOOT_SEED),contrasts

def independent_check(data,effects):
    """Separate scalar reconstruction: original score/xG -> dictionary -> Welch.

    Does not use checked(), metrics(), einsum(), estimate() or the stored cube.
    Same analyst; independent arithmetic implementation, no separate-person claim.
    """
    from math import fsum,sqrt
    groups=defaultdict(dict)
    for r in data:
        s=r['team_side'];stats=r['result']['team_statistics']
        key=(r['context'],r['seed']);cell=(s,r['arm'])
        require(cell not in groups[key],'Duplicate independent cell')
        groups[key][cell]=stats[s]['xg']-stats[1-s]['xg']
    by=defaultdict(list)
    for (h,seed),d in groups.items():
        require(set(d)==set((s,a) for s in (0,1) for a in ARMS),'Incomplete independent block')
        by[h].append(fsum((d[s,'D']-d[s,'C'])-(d[s,'B']-d[s,'A']) for s in (0,1))/2)
    means=[];variances=[]
    for h in CONTEXTS:
        v=by[h];require(len(v)==256,'Independent count mismatch')
        mean=fsum(v)/len(v);means.append(mean)
        variances.append(fsum((x-mean)**2 for x in v)/(len(v)-1)/(4*len(v)))
    mean=fsum(means)/2;variance=fsum(variances);se=sqrt(variance)
    df=variance**2/fsum(x*x/255 for x in variances);width=t.ppf(.975,df)*se
    result=dict(mean=mean,se=se,df=df,ci=[mean-width,mean+width],p=float(2*t.sf(abs(mean/se),df)),blocks=len(groups),matches=len(data))
    for k in ('mean','se','df','p'):require(abs(result[k]-effects['primary'][k])<1e-10,'Independent numerical mismatch '+k)
    require(np.allclose(result['ci'],effects['primary']['ci'],rtol=0,atol=1e-10),'Independent CI mismatch')
    result['passed']=True
    return result

if __name__=='__main__':
    if '--planning' in sys.argv:print(json.dumps(planning(),indent=2));sys.exit(0)
    data=rows(PUB/'main.jsonl');effects,contrasts=analyse(data)
    independent=independent_check(data,effects)
    (PUB/'effects.json').write_text(json.dumps(effects,allow_nan=False,indent=2)+'\n',encoding='utf8')
    (PUB/'independent-recalculation.json').write_text(json.dumps(independent,indent=2)+'\n',encoding='utf8')
    (PUB/'seed-contrasts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in contrasts),encoding='utf8')
    print(json.dumps(effects['primary'],indent=2))

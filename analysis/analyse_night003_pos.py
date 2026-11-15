"""Two fixed positional groups: difference of marginal sharpness benefits."""
from collections import defaultdict
from pathlib import Path
from math import fsum,sqrt
import json
import sys
import numpy as np
from scipy.stats import t,nct,chi2
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.native import read,rows,require
from research.stats import metrics,estimate,holm
PUB=ROOT/'data/night-003-sharppos'
CONTEXTS=('high_press','deep_block');ARMS=('ATTACK_LOW','DEFENCE_LOW');N=512
METRICS=('xgd','points','gf','ga','xgf','xga');BOOT=2026111504

def planning():
    data=rows(ROOT/'data/mech-002-sharpness-p0/main.jsonl');groups=defaultdict(dict)
    for r in data:
        if r['arm'] not in ('S70-P0','S100-P0'):continue
        result=r['result'];s=r['team_side'];stats=result['team_statistics']
        groups[r['context'],r['seed'],s][r['arm']]=stats[s]['xg']-stats[1-s]['xg']
    by=defaultdict(list);block=defaultdict(list)
    for (h,seed,side),d in groups.items():block[h,seed].append(d['S100-P0']-d['S70-P0'])
    for (h,seed),d in block.items():require(len(d)==2,'Historical side pair missing');by[h].append(sum(d)/2)
    sd=np.array([np.std(by[h],ddof=1) for h in CONTEXTS]);out={}
    for upper in (False,True):
        values=sd*np.sqrt(31/chi2.ppf(.025,31)) if upper else sd
        parts=values**2/(4*N);v=parts.sum();se=np.sqrt(v);df=v*v/(parts*parts/(N-1)).sum();cut=t.isf(.025,df)
        out['joint95_SD_upper' if upper else 'observed']=dict(sd=values.tolist(),full95width=float(2*cut*se),
            power={str(e):float(nct.sf(cut,df,e/se)+nct.sf(cut,df,-e/se)) for e in (.1,.15,.2)})
    return dict(n_per_context=N,blocks=2*N,matches=8*N,anchors=out,
        source='MECH002 S100-P0 minus S70-P0, side means,32seeds per fixed context; ten-player contrast only a variance proxy for new two-player group contrast.')

def checked(data):
    f=read(PUB/'inputs.json');plan=read(PUB/'main-plan.json');seeds=read(PUB/'seed-plan.json')['main_seeds']
    expected={j['key']:j for j in plan};seen=set();cube=np.full((2,N,2,2,6),np.nan)
    require(len(expected)==len(data)==4096,'Complete4096 required')
    for r in data:
        k=r['job_id'];require(k in expected and k not in seen,'Unexpected/duplicate row');seen.add(k);j=expected[k]
        label=f"{j['scenario']}-{j['side']}"
        require(r['experiment_id']=='N3-SHARPPOS-C1' and r['status']=='ok' and r['identity']==f['identity'] and
                r['seed']==j['seed'] and r['team_side']==j['side'] and r['context']==j['scenario'] and r['arm']==j['arm'] and
                r['setup_sha256']==f['setups'][label][j['arm']] and r['config_sha256']==f['configs_sha256'],'Identity drift')
        a=r['native_audit']
        require(all(a[k] is True for k in ('input_verified','start_state_verified','controls_verified','game_rules_verified')) and
                a['target_start_slots']==([8,10] if j['arm']=='ATTACK_LOW' else [2,3]) and
                [a[k] for k in ('attribute_values_verified','profile_fields_verified','phase_cells_verified','pi_groups_verified')]==[3174,1058,44,748],
                'Native group gate missing')
        result=r['result'];require(r['returncode']==0 and 0<result['tick']<47996,'Native finish missing')
        m=metrics(dict(status='ok',engine_readback=True,tested_side=j['side'],score=result['score'],team_statistics=result['team_statistics']))
        h=CONTEXTS.index(j['scenario']);i=seeds[h*N:(h+1)*N].index(j['seed'])
        cube[h,i,j['side'],ARMS.index(j['arm'])]=[m[x] for x in METRICS]
    require(np.isfinite(cube).all(),'Incomplete cube')
    return cube

def analyse(data):
    cube=checked(data);v=(cube[:,:,:,1,:]-cube[:,:,:,0,:]).mean(axis=2)
    def summary(a):
        out=estimate(list(a),resamples=20000,bootstrap_seed=BOOT)
        out['context']={h:dict(mean=float(a[i].mean()),sd=float(a[i].std(ddof=1))) for i,h in enumerate(CONTEXTS)}
        return out
    primary=summary(v[:,:,0]);secondary={m:summary(v[:,:,i]) for i,m in enumerate(METRICS) if i}
    secondary['CONTEXT_DIFFERENCE:xgd']=estimate([2*v[0,:,0],-2*v[1,:,0]],resamples=20000,bootstrap_seed=BOOT)
    for k,p in zip(secondary,holm([r['p'] for r in secondary.values()]),strict=True):secondary[k]['p_holm']=p
    primary.update(practical_reference=.15,full_ci_width=primary['ci'][1]-primary['ci'][0],
                   excludes_effects_outside_point15=primary['ci'][0]>-.15 and primary['ci'][1]<.15)
    effects=dict(experiment_id='N3-SHARPPOS-C1',n_matches=4096,independent_blocks=1024,primary=primary,secondary=secondary,
        arm_means={h:{a:{m:float(cube[i,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for i,h in enumerate(CONTEXTS)},
        interpretation='DEFENCE_LOW minus ATTACK_LOW = (common-high minus attack-low) minus (common-high minus defence-low). Separate absolute group benefits unidentifiable; fixed actors and roles, no universal position rule.',
        bootstrap_resamples=20000,bootstrap_seed=BOOT)
    return effects,v

def independent(data,effects):
    grouped=defaultdict(dict)
    for r in data:
        s=r['team_side'];stats=r['result']['team_statistics'];k=(r['context'],r['seed'])
        require((s,r['arm']) not in grouped[k],'Duplicate scalar cell')
        grouped[k][s,r['arm']]=stats[s]['xg']-stats[1-s]['xg']
    by=defaultdict(list)
    for (h,seed),d in grouped.items():
        require(len(d)==4,'Four scalar cells required')
        by[h].append(fsum(d[s,'DEFENCE_LOW']-d[s,'ATTACK_LOW'] for s in (0,1))/2)
    means=[];parts=[]
    for h in CONTEXTS:
        d=by[h];require(len(d)==N,'Wrong scalar n');m=fsum(d)/N;means.append(m)
        parts.append(fsum((x-m)**2 for x in d)/(N-1)/(4*N))
    m=fsum(means)/2;var=fsum(parts);se=sqrt(var)
    if var:
        df=var**2/fsum(x*x/(N-1) for x in parts);w=t.ppf(.975,df)*se;p=float(2*t.sf(abs(m/se),df))
    else:df=None;w=0.;p=float(m==0)
    out=dict(mean=m,se=se,df=df,ci=[m-w,m+w],p=p,matches=len(data),blocks=len(grouped))
    for k in ('mean','se','df','p'):
        require(out[k]==effects['primary'][k] if out[k] is None else abs(out[k]-effects['primary'][k])<1e-10,'Scalar mismatch '+k)
    require(np.allclose(out['ci'],effects['primary']['ci'],rtol=0,atol=1e-10),'Scalar CI mismatch')
    return dict(passed=True,**out)

if __name__=='__main__':
    if '--planning' in sys.argv:print(json.dumps(planning(),indent=2));sys.exit(0)
    data=rows(PUB/'main.jsonl');effects,v=analyse(data);check=independent(data,effects)
    (PUB/'effects.json').write_text(json.dumps(effects,indent=2,allow_nan=False)+'\n',encoding='utf8')
    (PUB/'independent-recalculation.json').write_text(json.dumps(check,indent=2)+'\n',encoding='utf8')
    seeds=read(PUB/'seed-plan.json')['main_seeds']
    (PUB/'seed-contrasts.jsonl').write_text(''.join(json.dumps(dict(context=h,seed=seeds[i*N+j],contrast_xgd=float(v[i,j,0])))+'\n'
        for i,h in enumerate(CONTEXTS) for j in range(N)),encoding='utf8')
    print(json.dumps(effects['primary'],indent=2))

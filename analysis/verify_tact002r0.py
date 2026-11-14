"""Independent public TACT-002-R0 reconstruction; no analysis/runner imports."""
from hashlib import sha256
from pathlib import Path
import json
import numpy as np
from scipy.stats import t,chi2,nct
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/tact-002-r0'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf8').splitlines() if s.strip()]
def canonical(x):return sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def verify():
    if not (DATA/'manifest.json').exists():print('R0 awaits registration; no scientific result claimed.');return
    r=read(DATA/'manifest.json');c=r['config'];assert canonical(c)==r['config_sha256']
    for name,v in read(DATA/'historical-archive.json')['sha256'].items():assert sha256((ROOT/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest()==v,name
    if not (DATA/'effects.json').exists():
        assert not (DATA/'run-summary.json').exists() or not read(DATA/'run-summary.json')['scientific_series_complete']
        print('R0 historical archive intact; awaiting complete512-match series.');return
    z=read(DATA/'effects.json');contexts=['high_press','deep_block'];arms=['R00','R10','R01','R11'];metrics=['xgd','points','gf','ga','xgf','xga'];cube=np.empty((2,32,2,4,6));seen=set()
    levels=[dict(ST=-1,AMC=-1),dict(ST=1,AMC=-1),dict(ST=-1,AMC=1),dict(ST=1,AMC=1)]
    assert c['design']['matrix']==[dict(id=a,levels=l) for a,l in zip(arms,levels)]
    expected_flags=[dict(ST=2048,AMC=512),dict(ST=1024,AMC=512),dict(ST=2048,AMC=2199023255552),dict(ST=1024,AMC=2199023255552)]
    for row in rows(DATA/'main.jsonl'):
        h=contexts.index(row['scenario']);a=arms.index(row['arm']);s=row['tested_side'];i=r['seeds'][h*32:(h+1)*32].index(row['seed']);key=(h,i,s,a)
        assert key not in seen;seen.add(key)
        assert row['key']==f"{contexts[h]}-{row['seed']}-{s}-{arms[a]}" and row['status']=='ok' and row['engine_readback'] and row['input_contract_verified']
        assert row['profile_fields_verified']==1058 and row['native_roles_verified']==44 and row['native_pi_cells_verified']==44 and row['native_pi_groups_verified']==748
        assert row['factor_levels']==levels[a] and row['native_role_flags']==expected_flags[a] and row['design_matrix_sha256']==canonical(c['design']['matrix'])
        assert row['config_sha256']==r['config_sha256'] and all(row[k]==v for k,v in c['identity'].items()) and row['setup_sha256']==c['design']['setups'][contexts[h]][str(s)][arms[a]] and 0<row['finish_tick']<47996
        gf,ga=row['score'][s],row['score'][1-s];x,y=[row['team_statistics'][v]['xg'] for v in (s,1-s)]
        cube[key]=[x-y,3 if gf>ga else int(gf==ga),gf,ga,x,y]
    assert len(seen)==512 and np.isfinite(cube).all()
    coef={'ST':[-.5,.5,-.5,.5],'AMC':[-.5,-.5,.5,.5],'STxAMC':[1.,-1.,-1.,1.]}
    values={name:sum(v*cube[:,:,:,a] for a,v in enumerate(weights)).mean(axis=2) for name,weights in coef.items()}
    seed=int.from_bytes(sha256(b'TACT-002-R0/bootstrap-v1').digest()[:8],'little');rng=np.random.default_rng(seed);indices=[rng.integers(32,size=(20000,32)) for _ in contexts]
    def check(v,record):
        mean=float(v.mean());pieces=v.var(axis=1,ddof=1)/128;variance=float(pieces.sum());se=np.sqrt(variance)
        df=variance**2/(pieces**2/31).sum() if variance else None;half=t.isf(.025,df)*se if variance else 0.;p=float(2*t.sf(abs(mean/se),df)) if variance else float(mean==0)
        np.testing.assert_allclose([record['mean'],record['se'],record['p'],*record['ci']],[mean,se,p,mean-half,mean+half],atol=1e-11)
        boot=(v[0][indices[0]].mean(axis=1)+v[1][indices[1]].mean(axis=1))/2;np.testing.assert_allclose(record['bootstrap_ci'],np.quantile(boot,[.025,.975]),atol=1e-11)
        for h,label in enumerate(contexts):np.testing.assert_allclose([record['context'][label]['mean'],record['context'][label]['sd']],[v[h].mean(),v[h].std(ddof=1)],atol=1e-11)
        return p
    check(values['ST'][:,:,0],z['primary']);pairs=[('AMC','xgd'),('STxAMC','xgd'),*(('ST',m) for m in metrics[1:])]
    assert c['science']['secondary_contrasts']==[list(p) for p in pairs]
    family=[(check(values[a][:,:,metrics.index(m)],z['secondary'][a+':'+m]),z['secondary'][a+':'+m]['p_holm']) for a,m in pairs];ordered=sorted(family)
    for i,(_,adjusted) in enumerate(ordered):np.testing.assert_allclose(adjusted,min(1,max((7-j)*ordered[j][0] for j in range(i+1))))
    blocks=rows(DATA/'block-contrasts.jsonl');assert len(blocks)==192
    for row in blocks:
        h=contexts.index(row['context']);i=r['seeds'][h*32:(h+1)*32].index(row['seed']);np.testing.assert_allclose(row['value'],values[row['contrast']][h,i,0],atol=1e-11)
    plan=read(DATA/'seed-plan.json');assert len(set(plan['seeds']))==67 and len(plan['main_seeds'])==64 and plan['main_seeds']==r['seeds'] and not set(plan['seeds'])&set(read(DATA/'excluded-seeds.json'))
    assert canonical(read(DATA/'excluded-seeds.json'))==plan['excluded_seed_set_sha256']
    old=read(ROOT/'data/tact-001-p1b/inputs.json')
    for h in contexts:
        for side in ('0','1'):assert c['design']['setups'][h][side]['R00']==old['setups'][h][side]['D00']
    jobs=rows(DATA/'job-accounting.jsonl');assert len(jobs)==545 and len({x['key'] for x in jobs})==545 and all(x['reserved'] for x in jobs)
    assert sum(x['kind']=='main' and x['status']=='ok' for x in jobs)==512 and sum(x['kind']=='technical' and x['status']=='ok' for x in jobs)==32 and sum(x['status']=='expected_rejection' for x in jobs)==1
    tech=rows(DATA/'technical.jsonl');assert len(tech)==32
    for h in contexts:
        for side in (0,1):
            for arm in arms:
                pair=[x for x in tech if (x['scenario'],x['tested_side'],x['arm'])==(h,side,arm)];assert len(pair)==2
                for field in ('seed','score','finish_tick','team_statistics','setup_sha256'):assert pair[0][field]==pair[1][field]
    sd=values['ST'][:,:,0].std(axis=1,ddof=1)
    for name,case in z['planning']['cases'].items():
        want=sd if name=='observed' else sd*np.sqrt(31/chi2.ppf(.025,31));np.testing.assert_allclose(case['sd'],want)
        for row in case['power90']:
            n=row['seeds_per_context'];assert row['matches']==16*n and row['independent_blocks']==2*n
            def power(q):
                v=want**2/(4*q);variance=v.sum()
                if not variance:return 1.
                se=np.sqrt(variance);df=variance**2/(v*v/(q-1)).sum();cut=t.isf(.025,df)
                return nct.cdf(-cut,df,row['effect']/se)+nct.sf(cut,df,row['effect']/se)
            assert power(n)>=.9 and (n==2 or power(n-1)<.9)
    budget=read(DATA/'budget.json');assert not budget['halted'] and budget['active'] is None and budget['charged_seconds']<900 and budget['within_fixed_deadline'] and budget['elapsed_study_window_seconds']<1800 and len(budget['reserved'])==545
    assert all(o['returncode']==0 and not o['timed_out'] for o in budget['operations'])
    assert not z['winner_selected'] and not z['optimal_tactic_confirmed'] and not z['career_transfer_confirmed']
    print('Verified R0:512rows,8contrasts/t/bootstrap,Holm7,192blockcontrasts,545attempts,seed/input/archive/budget checks.')
if __name__=='__main__':verify()

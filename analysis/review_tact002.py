"""Separate reviewer reconstruction for TACT-002-R0. Never imports project analysis."""
from argparse import ArgumentParser
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import numpy as np
from scipy.stats import chi2,nct,t

ROOT=Path(__file__).resolve().parents[1]

def read(path):return json.loads(path.read_text(encoding='utf8'))
def rows(path):return [json.loads(s) for s in path.read_text(encoding='utf8').splitlines() if s.strip()]
def digest(value):return sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def review(folder):
    if not (folder/'effects.json').exists():
        assert not (folder/'run-summary.json').exists() or not read(folder/'run-summary.json')['scientific_series_complete'], 'Complete status without results'
        print('Reviewer: results absent; no performance claim or native operation.');return
    receipt=read(folder/'manifest.json');cfg=receipt['config'];result=read(folder/'effects.json');status=read(folder/'run-summary.json')
    assert status['scientific_series_complete'] and cfg['experiment_id']=='TACT-002-R0'
    assert digest(cfg)==receipt['config_sha256']
    contexts=['high_press','deep_block'];arms=['R00','R10','R01','R11'];metrics=['xgd','points','gf','ga','xgf','xga']
    assert cfg['design']['n_blocks']==32 and cfg['design']['sides']==[0,1] and [a['id'] for a in cfg['design']['arms']]==arms
    assert len(receipt['seeds'])==len(set(receipt['seeds']))==64
    levels=[dict(ST=-1,AMC=-1),dict(ST=1,AMC=-1),dict(ST=-1,AMC=1),dict(ST=1,AMC=1)]
    assert cfg['design']['matrix']==[dict(id=a,levels=l) for a,l in zip(arms,levels)]
    cells={};all_rows=rows(folder/'main.jsonl')
    for row in all_rows:
        h=row['scenario'];s=row['tested_side'];a=row['arm'];seed=row['seed'];j=contexts.index(h)
        assert seed in receipt['seeds'][j*32:(j+1)*32] and type(s) is int and s in (0,1) and a in arms
        key=(h,seed,s,a);assert key not in cells and row['key']==f'{h}-{seed}-{s}-{a}'
        assert row['status']=='ok' and row['engine_readback'] and row['input_contract_verified'] and 0<row['finish_tick']<47996
        assert all(row[k]==v for k,v in cfg['identity'].items()) and row['config_sha256']==receipt['config_sha256']
        assert row['setup_sha256']==cfg['design']['setups'][h][str(s)][a]
        assert row['factor_levels']==levels[arms.index(a)] and row['design_matrix_sha256']==digest(cfg['design']['matrix'])
        assert row['profile_fields_verified']==1058 and row['native_roles_verified']==row['native_pi_cells_verified']==44 and row['native_pi_groups_verified']==748
        assert row['native_role_flags']==dict(ST=1024 if a in ('R10','R11') else 2048,AMC=2199023255552 if a in ('R01','R11') else 512)
        goals=row['score'];assert len(goals)==2 and all(type(g) is int and g>=0 for g in goals)
        gf,ga=goals[s],goals[1-s];x,y=[row['team_statistics'][k]['xg'] for k in (s,1-s)]
        assert np.isfinite([x,y]).all() and min(x,y)>=0
        cells[key]=np.array([x-y,3 if gf>ga else int(gf==ga),gf,ga,x,y],float)
    assert len(cells)==len(all_rows)==512
    sides={c:[] for c in ('ST','AMC','STxAMC')}
    for j,h in enumerate(contexts):
        by={c:[] for c in sides}
        for seed in receipt['seeds'][j*32:(j+1)*32]:
            q={c:[] for c in sides}
            for s in (0,1):
                y00,y10,y01,y11=[cells[h,seed,s,a] for a in arms]
                q['ST'].append(((y10-y00)+(y11-y01))/2)
                q['AMC'].append(((y01-y00)+(y11-y10))/2)
                q['STxAMC'].append((y11-y01)-(y10-y00))
            for c in sides:by[c].append(q[c])
        for c in sides:sides[c].append(by[c])
    sides={c:np.array(v) for c,v in sides.items()};values={c:v.mean(axis=2) for c,v in sides.items()}
    rng=np.random.default_rng(int.from_bytes(sha256(b'TACT-002-R0/bootstrap-v1').digest()[:8],'little'))
    ix=[rng.integers(32,size=(20000,32)) for _ in contexts]
    checked=[]
    def compare(c,m,record):
        k=metrics.index(m);v=values[c][:,:,k];mean=float((v[0].mean()+v[1].mean())/2)
        pieces=v.var(axis=1,ddof=1)/(4*32);var=float(pieces.sum());se=np.sqrt(var)
        df=float(var*var/(pieces*pieces/31).sum()) if var else None
        half=float(t.isf(.025,df)*se) if var else 0.;prob=float(2*t.sf(abs(mean/se),df)) if var else float(mean==0)
        np.testing.assert_allclose([record['mean'],record['se'],record['p'],*record['ci']],[mean,se,prob,mean-half,mean+half],atol=1e-11,rtol=1e-11)
        boot=(v[0][ix[0]].mean(axis=1)+v[1][ix[1]].mean(axis=1))/2
        np.testing.assert_allclose(record['bootstrap_ci'],np.quantile(boot,[.025,.975]),atol=1e-11)
        for j,h in enumerate(contexts):
            rr=record['context'][h]
            np.testing.assert_allclose([rr['mean'],rr['sd'],rr['side0_mean'],rr['side1_mean'],rr['side_covariance']],[v[j].mean(),v[j].std(ddof=1),sides[c][j,:,0,k].mean(),sides[c][j,:,1,k].mean(),np.cov(sides[c][j,:,:,k].T)[0,1]],atol=1e-11)
        checked.append((c,m,mean,prob));return prob
    compare('ST','xgd',result['primary'])
    pairs=[('AMC','xgd'),('STxAMC','xgd'),('ST','points'),('ST','gf'),('ST','ga'),('ST','xgf'),('ST','xga')]
    assert cfg['science']['secondary_contrasts']==[list(v) for v in pairs] and len(result['secondary'])==7
    p=[compare(c,m,result['secondary'][c+':'+m]) for c,m in pairs]
    adjusted={};prior=0
    for rank,i in enumerate(sorted(range(7),key=lambda i:p[i])):
        prior=max(prior,min(1.,(7-rank)*p[i]));adjusted[i]=prior
    for i,(c,m) in enumerate(pairs):np.testing.assert_allclose(result['secondary'][c+':'+m]['p_holm'],adjusted[i],atol=1e-11)
    block=rows(folder/'block-contrasts.jsonl');assert len(block)==192
    for b in block:
        h=contexts.index(b['context']);i=receipt['seeds'][h*32:(h+1)*32].index(b['seed'])
        np.testing.assert_allclose(b['value'],values[b['contrast']][h,i,0],atol=1e-11)
    observed=values['ST'][:,:,0].std(axis=1,ddof=1)
    for name,case in result['planning']['cases'].items():
        sigma=observed if name=='observed' else observed*np.sqrt(31/chi2.ppf(.025,31))
        np.testing.assert_allclose(case['sd'],sigma)
        for r in case['power90']:
            def power(n):
                v=sigma*sigma/(4*n);var=v.sum()
                if not var:return 1.
                se=np.sqrt(var);df=var*var/(v*v/(n-1)).sum();cut=t.isf(.025,df)
                return nct.cdf(-cut,df,r['effect']/se)+nct.sf(cut,df,r['effect']/se)
            expected=next(n for n in range(2,100000) if power(n)>=.9)
            assert r['seeds_per_context']==expected and r['independent_blocks']==2*expected and r['matches']==16*expected
    jobs=rows(folder/'job-accounting.jsonl');assert len(jobs)==len({r['key'] for r in jobs})==545
    assert all(r['reserved'] for r in jobs) and sum(r['status']=='ok' and r['kind']=='main' for r in jobs)==512
    assert sum(r['status']=='ok' and r['kind']=='technical' for r in jobs)==32 and sum(r['status']=='expected_rejection' for r in jobs)==1
    plan=read(folder/'seed-plan.json');excluded=read(folder/'excluded-seeds.json')
    assert len(plan['technical_seeds'])==3 and plan['seeds']==plan['technical_seeds']+plan['main_seeds']
    assert len(set(plan['seeds']))==67 and not set(plan['seeds'])&set(excluded) and digest(excluded)==plan['excluded_seed_set_sha256'] and plan['main_seeds']==receipt['seeds']
    tech=rows(folder/'technical.jsonl');assert len(tech)==32
    for h in contexts:
        for s in (0,1):
            for a in arms:
                pair=[r for r in tech if (r['scenario'],r['tested_side'],r['arm'])==(h,s,a)];assert len(pair)==2
                assert all(pair[0][k]==pair[1][k] for k in ('seed','score','finish_tick','team_statistics','setup_sha256'))
    b=read(folder/'budget.json');assert not b['halted'] and b['active'] is None and b['charged_seconds']<900 and b['within_fixed_deadline'] and b['elapsed_study_window_seconds']<1800
    assert len(b['reserved'])==545 and len(b['operations'])==3
    for op,lease in zip(b['operations'],b['coordination_leases'],strict=True):
        assert op['returncode']==0 and not op['timed_out'] and lease['phase']==op['name'] and lease['workers']==4 and lease['experiment']=='TACT-002-R0'
        assert datetime.fromisoformat(lease['acquired_utc'])<=datetime.fromisoformat(op['start_utc'])
    assert result['n_matches']==512 and result['independent_seed_blocks']==64 and not result['winner_selected'] and not result['career_transfer_confirmed']
    print(json.dumps(dict(independent_review='passed',contrasts=checked,independent_blocks=64,attempts=545),ensure_ascii=False))

if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--data',type=Path,default=ROOT/'data/tact-002-r0');args=parser.parse_args();review(args.data)

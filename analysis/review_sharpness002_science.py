"""Independent raw-score algebra and software-only sharpness design review.

No native imports, save reads, seed allocation or registry mutation. Optional
private checks read only existing D00/R01 FM27CFG1 binaries, never an engine.
"""
from hashlib import sha256
from itertools import product
import json
from math import sqrt
from pathlib import Path
from statistics import fmean,variance,covariance
import struct
import sys

import numpy as np
from scipy.stats import chi2,nct,t

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
CONTEXTS=('high_press','deep_block')
ARMS=('S70-P0','S100-P0','S70-P1','S100-P1')
FAMILY=('SHARPNESS:points','SHARPNESS:gf','SHARPNESS:ga','SHARPNESS:xgf','SHARPNESS:xga',
        'PRESS:xgd','SHARPNESSxPRESS:xgd')
METRICS=('xgd','points','gf','ga','xgf','xga')
BOOT_SEED=int.from_bytes(sha256(b'MECH-002-SHARPNESS-P0/bootstrap-v1').digest()[:8],'little')


def raw_metrics(row):
    side=row['team_side'];result=row['result'];score=result['score'];teams=result['team_statistics']
    gf,ga=score[side],score[1-side];xgf,xga=teams[side]['xg'],teams[1-side]['xg']
    return dict(xgd=xgf-xga,points=3 if gf>ga else 1 if gf==ga else 0,gf=gf,ga=ga,xgf=xgf,xga=xga)


def synthetic():
    # Reuse only valid schema/identity scaffolding; overwrite all football scores
    # and xGs independently. This is manufactured software data, never FM evidence.
    from tests.test_sharpness002_design import receipt_and_data
    receipt,data=receipt_and_data()
    for row in data:
        h=CONTEXTS.index(row['context']);side=row['team_side'];sign=2*side-1
        i=receipt['seeds'][32*h:32*(h+1)].index(row['seed'])
        u=(i-15.5)/31;v=((7*i+3)%17-8)/8
        s=1 if row['arm'].startswith('S100') else -1;p=1 if row['arm'].endswith('P1') else -1
        xgf=2.5+.08*h+.07*side+(.12+.01*h+(.06+.02*h)*u+.015*sign+.03*v*sign)*s+(.16+.01*h+.09*v-.01*sign)*p+(.03+.01*u+.005*h)*s*p
        xga=1.4+.05*h-.04*side+(.015+(.02-.01*h)*u-.005*sign)*s+(-.02+.03*u+.015*sign)*p+.01*s*p
        row['result']['team_statistics'][side]['xg']=xgf
        row['result']['team_statistics'][1-side]['xg']=xga
        row['result']['score'][side]=(i+2*h+side+int(s==1)+2*int(p==1))%4
        row['result']['score'][1-side]=(3*i+h+2*side+int(p==1)+int(s==1)*int(p==1))%3
        row['test_origin']='independent_synthetic_not_fm'
    return receipt,data


def independently_group(data,receipt):
    indexed={}
    for row in data:
        key=(row['context'],row['seed'],row['team_side'],row['arm'])
        if key in indexed:raise ValueError('Duplicate synthetic block cell')
        indexed[key]=raw_metrics(row)
    output={}
    for name in ('SHARPNESS','PRESS','SHARPNESSxPRESS'):
        for metric in METRICS:
            contexts=[]
            for h,context in enumerate(CONTEXTS):
                sides=[[],[]]
                for seed in receipt['seeds'][32*h:32*(h+1)]:
                    for side in (0,1):
                        a,b,c,d=[indexed[context,seed,side,arm][metric] for arm in ARMS]
                        # Derived physical comparisons, independent of the source
                        # COEFFICIENTS/einsum implementation and its axis order.
                        value=((b-a)+(d-c))/2 if name=='SHARPNESS' else ((c-a)+(d-b))/2 if name=='PRESS' else (d-c)-(b-a)
                        sides[side].append(value)
                contexts.append(dict(sides=sides,blocks=[(a+b)/2 for a,b in zip(*sides)]))
            output[name+':'+metric]=contexts
    return output


def independently_summarize(contexts):
    values=[c['blocks'] for c in contexts];means=[fmean(v) for v in values]
    parts=[variance(v)/(4*len(v)) for v in values];v=sum(parts);mean=sum(means)/2
    if v:
        df=v*v/sum(part*part/(len(a)-1) for part,a in zip(parts,values))
        se=sqrt(v);half=float(t.isf(.025,df))*se;p=float(2*t.sf(abs(mean/se),df))
    else:df=None;se=half=0.;p=float(mean==0)
    rng=np.random.default_rng(BOOT_SEED)
    samples=[np.asarray(a)[rng.integers(0,len(a),size=(20000,len(a)))].mean(axis=1) for a in values]
    boot=(samples[0]+samples[1])/2
    loo=[(fmean(a[:i]+a[i+1:])+means[1-h])/2 for h,a in enumerate(values) for i in range(len(a))]
    return dict(mean=mean,se=se,df=df,p=p,ci=[mean-half,mean+half],
        bootstrap_ci=np.quantile(boot,[.025,.975]).tolist(),
        loo_range=[min(loo),max(loo)],loo_change=max(abs(x-mean) for x in loo),
        context_sd=[sqrt(variance(a)) for a in values],
        side_covariance=[covariance(*c['sides']) for c in contexts])


def independently_holm(values):
    ordered=sorted(values,key=values.get);result={};previous=0.
    for i,key in enumerate(ordered):
        previous=max(previous,min(1.,(len(ordered)-i)*values[key]));result[key]=previous
    return result


def audit_math():
    from analysis import analyse_sharpness002 as project
    receipt,data=synthetic();grouped=independently_group(data,receipt)
    independent={k:independently_summarize(grouped[k]) for k in ('SHARPNESS:xgd',*FAMILY)}
    result,blocks=project.analyse(data,receipt)
    published={'SHARPNESS:xgd':result['primary'],**result['secondary']}
    for key,expected in independent.items():
        got=published[key]
        for name in ('mean','se','p','ci','bootstrap_ci'):
            np.testing.assert_allclose(got[name],expected[name],rtol=1e-11,atol=1e-12,err_msg=key+'/'+name)
        if expected['df'] is not None:np.testing.assert_allclose(got['df'],expected['df'],rtol=1e-11)
        np.testing.assert_allclose(got['leave_one_out']['range'],expected['loo_range'],atol=1e-12)
        np.testing.assert_allclose(got['leave_one_out']['max_change'],expected['loo_change'],atol=1e-12)
        for h,context in enumerate(CONTEXTS):
            np.testing.assert_allclose(got['context'][context]['sd'],expected['context_sd'][h],atol=1e-12)
            np.testing.assert_allclose(got['context'][context]['sd_upper95_normal_model'],
                expected['context_sd'][h]*sqrt(31/chi2.ppf(.05,31)),atol=1e-12)
            np.testing.assert_allclose(got['context'][context]['side_covariance'],expected['side_covariance'][h],atol=1e-12)
    adjusted=independently_holm({k:independent[k]['p'] for k in FAMILY})
    for key,value in adjusted.items():np.testing.assert_allclose(result['secondary'][key]['p_holm'],value,atol=1e-12)
    for row in blocks:
        h=CONTEXTS.index(row['context']);i=receipt['seeds'][h*32:32*(h+1)].index(row['seed'])
        np.testing.assert_allclose(row['value'],grouped[row['contrast']+':'+row['endpoint']][h]['blocks'][i],atol=1e-12)
    assert len(blocks)==512 and result['n_matches']==512 and result['independent_seed_blocks']==64
    np.testing.assert_allclose(result['primary']['mean'],.22,atol=1e-12)
    np.testing.assert_allclose(result['secondary']['SHARPNESSxPRESS:xgd']['mean'],.09,atol=1e-12)
    return dict(software_data_only=True,primary=independent['SHARPNESS:xgd'],secondary_holm=adjusted,
                independent_blocks=64,raw_match_rows=512,derived_contrast_rows=512,new_native_matches=0)


def audit_private_inputs(central):
    from analysis.sharpness002_design import build_inputs
    central=Path(central);proof=[]
    published_d00=json.loads((central/'data/tact-001-p1b/inputs.json').read_text(encoding='utf8'))
    published_r01=json.loads((central/'data/mech-003-stamina/inputs.json').read_text(encoding='utf8'))
    configs=json.loads((central/'local/valid005-observer-v1/configs.json').read_text(encoding='utf8'))
    for context,side in product(CONTEXTS,(0,1)):
        assert [len(team['players']) for team in configs[f'{context}-{side}']['teams']]==[23,26]
        base=(central/f'local/valid005-observer-v1/inputs/{context}-{side}.bin').read_bytes()
        carrier=(central/f'local/mech-003-stamina/inputs/{context}-{side}-R01.bin').read_bytes()
        assert sha256(base).hexdigest()==published_d00['setups'][context][str(side)]['D00']
        assert sha256(carrier).hexdigest()==published_r01['setups'][context][str(side)]['R01']
        records=tuple(struct.iter_unpack('<5I',base[12:]));original=tuple(struct.iter_unpack('<5I',carrier[12:]))
        assert base[:8]==carrier[:8]==b'FM27CFG1' and base[8:12]==carrier[8:12] and len(records)==len(original)==5557
        stamina=[r for r in records if r[0]==1 and r[3]==52]
        assert len(stamina)==46 and all(r[4]==60 for r in stamina)
        assert {(r[1],r[2]) for r in stamina}==set(product((0,1),range(23)))
        lineup={(s,a):v for k,s,a,b,v in records if k==11 and b==0}
        affected={lineup[side,i] for i in range(1,11)};assert len(affected)==10
        restored=tuple((k,s,a,b,60) if k==1 and s==side and a in affected and b==52 else (k,s,a,b,v) for k,s,a,b,v in original)
        assert [(x,y) for x,y in zip(records,restored) if x!=y]==[
            ((2,side,10,0,1313689463),(2,side,10,0,2000905329))]
        outputs=build_inputs(base,carrier,side)
        for arm,payload in outputs.items():
            low=arm.startswith('S70');press=arm.endswith('P1')
            expected=[]
            for k,s,a,b,v in records:
                if low and k==15 and s==side and a in affected and b in (16,17):v=7000
                if press and (k,s,a,b)==(2,side,10,0):v=2000905329
                expected.append((k,s,a,b,v))
            wanted=base[:12]+b''.join(struct.pack('<5I',*r) for r in expected)
            assert payload==wanted and not any(r[0]==61 for r in expected)
            differences=sum(x!=y for x,y in zip(records,expected));assert differences==20*low+press
            assert all(r[4]==60 for r in expected if r[0]==1 and r[3]==52)
            proof.append(dict(context=context,side=side,arm=arm,changed_records=differences,
                              active_attribute_actors=46,sha256=sha256(payload).hexdigest()))
    return proof


def audit_planning():
    """Linear search independently checks the project's binary-search planning."""
    from analysis.analyse_sharpness002 import future_planning
    sd=(.8,1.2);result=future_planning(sd);checked=[]
    for key,multiplier in (('observed',1.),('simultaneous95_sd_upper',sqrt(31/chi2.ppf(.025,31)))):
        values=[s*multiplier for s in sd]
        np.testing.assert_allclose(result[key]['sd'],values,atol=1e-12)
        for entry,effect in zip(result[key]['power90'],(.2,.3),strict=True):
            for n in range(2,10000):
                components=[s*s/(4*n) for s in values];v=sum(components);se=sqrt(v)
                df=v*v/sum(part*part/(n-1) for part in components)
                cutoff=t.ppf(.975,df);noncentrality=effect/se
                power=nct.cdf(-cutoff,df,noncentrality)+1-nct.cdf(cutoff,df,noncentrality)
                if power>=.9:break
            else:raise AssertionError('Independent planning search bound reached')
            assert entry['effect']==effect and entry['seeds_per_context']==n
            assert entry['independent_blocks']==2*n and entry['matches']==16*n
            np.testing.assert_allclose(entry['power'],power,rtol=1e-11)
            np.testing.assert_allclose(entry['full_width'],2*cutoff*se,rtol=1e-11)
            checked.append(dict(case=key,effect=effect,n_per_context=n,matches=16*n,
                                full_width=float(2*cutoff*se),conditional_power=float(power)))
    return dict(assumed_software_context_sd=list(sd),plans=checked)


if __name__=='__main__':
    from argparse import ArgumentParser
    parser=ArgumentParser(description=__doc__);parser.add_argument('--private-root',type=Path);args=parser.parse_args()
    report=audit_math();report['planning_software_check']=audit_planning()
    if args.private_root:report['private_input_proof']=audit_private_inputs(args.private_root)
    print(json.dumps(report,indent=2))

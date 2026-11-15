"""Independent scalar reconstruction of NIGHT-003 Welch tests and Holm families.

No experiment-analysis, research.stats, NumPy, native process or outcome selection.
Original sanitized per-match scores/xG are the only measurement inputs.
Same analyst; independence refers to arithmetic, not an independent person.
"""
import argparse
from collections import defaultdict
from hashlib import sha256
import json
from math import fsum,isfinite,sqrt
from pathlib import Path
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
CONFIG={
    'structure':('night-003-sharpstruct','N3-SHARPSTRUCT-C1',('A','B','C','D'),(-1,1,1,-1),256),
    'positions':('night-003-sharppos','N3-SHARPPOS-C1',('ATTACK_LOW','DEFENCE_LOW'),(-1,1),512),
    'amc':('night-003-amcshift','N3-AMCSHIFT-C1',('BASE','AMC_LEFT'),(-1,1),256),
}
METRICS=('xgd','points','gf','ga','xgf','xga')
CONTEXTS=('high_press','deep_block')

def read(p):return json.loads(p.read_text(encoding='utf8'))
def lf_hash(p):return sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def scalar_summary(groups,weights=(.5,.5)):
    means=[];parts=[];ns=[]
    for values,w in zip(groups,weights,strict=True):
        n=len(values);require(n>=2,'Insufficient independent blocks')
        m=fsum(values)/n
        means.append(w*m);parts.append(w*w*fsum((x-m)**2 for x in values)/(n-1)/n);ns.append(n)
    mean=fsum(means);variance=fsum(parts);se=sqrt(variance)
    if variance:
        df=variance*variance/fsum(v*v/(n-1) for v,n in zip(parts,ns,strict=True))
        half=float(t.ppf(.975,df))*se;p=float(2*t.sf(abs(mean/se),df))
    else:df=None;half=0.;p=float(mean==0)
    return dict(mean=mean,se=se,df=df,ci=[mean-half,mean+half],p=p)

def require(ok,msg):
    if not ok:raise ValueError(msg)

def compare(actual,expected):
    for k in ('mean','se','df','p'):
        if actual[k] is None:require(expected[k] is None,'Unexpected scalar df')
        else:require(abs(actual[k]-expected[k])<1e-10,'Scalar mismatch '+k)
    require(all(abs(x-y)<1e-10 for x,y in zip(actual['ci'],expected['ci'],strict=True)),'Scalar CI mismatch')

def review(study):
    folder,identity,arms,weights,n=CONFIG[study];p=ROOT/'data'/folder
    data=[json.loads(s) for s in (p/'main.jsonl').read_text(encoding='utf8').splitlines()]
    plan={j['key']:j for j in read(p/'main-plan.json')};expected=read(p/'effects.json')
    require(len(data)==len(plan)==4*n*len(arms),'Entire declared match sample required')
    seen=set();blocks=defaultdict(dict)
    for row in data:
        key=row['job_id'];require(key in plan and key not in seen,'Unexpected/duplicate job');seen.add(key);j=plan[key]
        require(row['status']=='ok' and row['experiment_id']==identity and row['returncode']==0 and
                (row['context'],row['seed'],row['team_side'],row['arm'])==
                (j['scenario'],j['seed'],j['side'],j['arm']),'Independent observation mismatch')
        side=row['team_side'];result=row['result'];score=result['score'];stats=result['team_statistics']
        gf,ga=score[side],score[1-side];xgf,xga=stats[side]['xg'],stats[1-side]['xg']
        require(all(isfinite(x) for x in (gf,ga,xgf,xga)),'Nonfinite raw outcome')
        values=(xgf-xga,3 if gf>ga else int(gf==ga),gf,ga,xgf,xga)
        block=blocks[row['context'],row['seed']];cell=side,row['arm']
        require(cell not in block,'Duplicate scalar cell');block[cell]=values
    by=defaultdict(list)
    for (h,seed),block in blocks.items():
        require(set(block)=={(s,a) for s in (0,1) for a in arms},'Incomplete independent block')
        by[h].append(tuple(fsum(w*block[s,a][k] for s in (0,1) for a,w in zip(arms,weights,strict=True))/2
                           for k in range(6)))
    require(set(by)==set(CONTEXTS) and all(len(by[h])==n for h in CONTEXTS),'Independent block count drift')
    estimates={metric:scalar_summary([[v[k] for v in by[h]] for h in CONTEXTS]) for k,metric in enumerate(METRICS)}
    compare(estimates['xgd'],expected['primary'])
    secondary={('INTERACTION:'+m if study=='structure' else m):estimates[m] for m in METRICS[1:]}
    secondary['CONTEXT_DIFFERENCE:xgd']=scalar_summary([[v[0] for v in by[h]] for h in CONTEXTS],(1.,-1.))
    require(set(secondary)==set(expected['secondary']) and len(secondary)==6,'Exactly declared Holm6 family')
    running=0.
    for rank,key in enumerate(sorted(secondary,key=lambda k:secondary[k]['p'])):
        running=max(running,min(1.,(6-rank)*secondary[key]['p']));secondary[key]['p_holm']=running
    for key,value in secondary.items():
        compare(value,expected['secondary'][key])
        require(abs(value['p_holm']-expected['secondary'][key]['p_holm'])<1e-10,'Independent Holm mismatch')
    return dict(experiment_id=identity,passed=True,matches=len(data),independent_blocks=len(blocks),
        primary=estimates['xgd'],secondary=secondary,formal_estimands_checked=7,
        measurement_lf_sha256=lf_hash(p/'main.jsonl'),review_source_lf_sha256=lf_hash(Path(__file__)),
        method='Separate scalar score/xG reconstruction, fixed paired blocks, Welch moments and independent Holm6; same analyst, no independent-person claim. Bootstrap checked by frozen reproducibility tests separately.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('study',choices=(*CONFIG,'all'));args=parser.parse_args()
    for study in CONFIG if args.study=='all' else (args.study,):
        result=review(study);p=ROOT/'data'/CONFIG[study][0]/'independent-statistics-review.json'
        p.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf8')
        print(json.dumps({k:result[k] for k in ('experiment_id','passed','matches','independent_blocks','formal_estimands_checked')}))

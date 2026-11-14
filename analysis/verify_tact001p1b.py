"""Independent public-row reconstruction; no runner/analysis imports or native calls."""
from hashlib import sha256
from pathlib import Path
import json

import numpy as np
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/tact-001-p1b"


def read(path):return json.loads(path.read_text(encoding="utf8"))


def verify():
    if not (DATA/"effects.json").exists():
        print("P1B results not yet available; independent verifier awaits complete series.");return
    r=read(DATA/"manifest.json");c=r["config"];result=read(DATA/"effects.json")
    rows=[json.loads(s) for s in (DATA/"main.jsonl").read_text(encoding="utf8").splitlines()]
    contexts=["high_press","deep_block"];arms=[f"D{i:02d}" for i in range(16)]
    names=list("ABCDE");endpoints=["xgd","points","gf","ga","xgf","xga","shots_for","shots_against","sot_for","sot_against","possession_for"]
    cube=np.empty((2,32,2,16,11));seen=set()
    levels=np.array([[v["levels"][n] for n in names] for v in c["design"]["matrix"]])
    assert np.array_equal(levels[0],[-1]*5) and len(set(map(tuple,levels)))==16
    assert np.all(levels.prod(axis=1)==-1)
    for row in rows:
        h=contexts.index(row["scenario"]);a=arms.index(row["arm"]);s=row["tested_side"]
        i=r["seeds"][h*32:(h+1)*32].index(row["seed"]);key=(h,i,s,a)
        assert key not in seen and row["status"]=="ok" and row["input_contract_verified"]
        assert row["setup_sha256"]==c["design"]["setups"][contexts[h]][str(s)][arms[a]]
        assert row["factor_levels"]==dict(zip(names,levels[a].tolist()))
        assert all(row[k]==v for k,v in c["identity"].items())
        gf,ga=row["score"][s],row["score"][1-s];o,b=row["team_statistics"][s],row["team_statistics"][1-s]
        cube[key]=[o["xg"]-b["xg"],3 if gf>ga else int(gf==ga),gf,ga,o["xg"],b["xg"],o["shots"],b["shots"],o["shots_on_target"],b["shots_on_target"],o["possession"]]
        seen.add(key)
    assert len(seen)==2048 and np.isfinite(cube).all()
    bootstrap_seed=int.from_bytes(sha256(b"TACT-001-P1B/bootstrap-v1").digest()[:8],"little")
    rng=np.random.default_rng(bootstrap_seed)
    indices=[rng.integers(32,size=(20000,32)) for _ in contexts]
    families=[[],[],[]]
    block_rows={}
    def check(coef,metric,record,family,label):
        # Direct scalar cell sum, no einsum or shared contrast implementation.
        by_side=sum(float(coef[a])*cube[:,:,:,a,metric] for a in range(16))
        values=(by_side[:,:,0]+by_side[:,:,1])/2
        mu=float((values[0].mean()+values[1].mean())/2)
        v=values.var(axis=1,ddof=1)/(4*32);se=float(np.sqrt(sum(v)))
        df=float(sum(v)**2/sum(v*v/31)) if se else None
        half=float(t.isf(.025,df)*se) if se else 0.
        prob=float(2*t.sf(abs(mu/se),df)) if se else float(mu==0)
        np.testing.assert_allclose([record["mean"],record["se"],record["p"],*record["ci"]],[mu,se,prob,mu-half,mu+half],atol=1e-11,rtol=1e-11)
        boot=(values[0][indices[0]].mean(axis=1)+values[1][indices[1]].mean(axis=1))/2
        np.testing.assert_allclose(record["bootstrap_ci"],np.quantile(boot,[.025,.975]),atol=1e-11)
        if "ci99_bonferroni5" in record:
            h99=float(t.isf(.005,df)*se) if se else 0.
            np.testing.assert_allclose(record["ci99_bonferroni5"],[mu-h99,mu+h99],atol=1e-11)
        for h,name in enumerate(contexts):
            z=record["context"][name]
            np.testing.assert_allclose([z["mean"],z["sd"],z["side_covariance"]],
                [values[h].mean(),values[h].std(ddof=1),np.cov(by_side[h].T)[0,1]],atol=1e-11)
            if metric==0:
                for i,seed in enumerate(r["seeds"][h*32:(h+1)*32]):block_rows[label,name,seed]=float(values[h,i])
        families[family].append((prob,record["p_holm"]))
    for j,n in enumerate(names):
        coef=np.where(levels[:,j]==1,1/8,-1/8)
        check(coef,0,result["primary"][n],0,n)
        for k,m in enumerate(endpoints[1:6],1):check(coef,k,result["secondary"][n][m],2,n+"_"+m)
        for k in range(j+1,5):
            label=n+names[k];coef2=np.where(levels[:,j]==levels[:,k],1/4,-1/4)
            check(coef2,0,result["interactions_exploratory"][label],1,label)
    for family in families:
        ordered=sorted(family)
        for i,(prob,adjusted) in enumerate(ordered):
            expected=min(1.,max((len(ordered)-j)*ordered[j][0] for j in range(i+1)))
            np.testing.assert_allclose(adjusted,expected,atol=1e-11)
    published=[json.loads(s) for s in (DATA/"block-contrasts.jsonl").read_text().splitlines()]
    assert len(published)==960
    for row in published:np.testing.assert_allclose(row["value"],block_rows[row["contrast"],row["context"],row["seed"]],atol=1e-11)
    gain=(cube[:,:,:,:,0]-cube[:,:,:,0:1,0]).mean(axis=(1,2))
    eligible=[a for a in range(1,16) if min(gain[:,a])>0]
    chosen=sorted(eligible,key=lambda a:(-min(gain[:,a]),-sum(gain[:,a])/2,arms[a]))[:2]
    assert [v["design_id"] for v in result["candidates_exploratory"]]==[arms[a] for a in chosen]
    archive=read(DATA/"historical-archive.json")
    for path,expected in archive["sha256"].items():assert sha256((ROOT/path).read_bytes().replace(b"\r\n",b"\n")).hexdigest()==expected,path
    counts=[json.loads(s) for s in (DATA/"job-accounting.jsonl").read_text().splitlines()]
    assert len(counts)==2121 and len({x["key"] for x in counts})==2121
    assert sum(x["status"]=="ok" for x in counts)==2120
    assert sum(x["status"]=="expected_rejection" for x in counts)==1
    budget=read(DATA/"budget.json");assert budget["charged_seconds"]<2400 and budget["within_fixed_deadline"] and not budget["halted"]
    print("Verified 2048 rows, 40 effect/t/bootstrap intervals, five simultaneous intervals, Holm5/10/25, 960 block contrasts, candidate rule, 2121 jobs and historical archive independently.")


if __name__=="__main__":verify()

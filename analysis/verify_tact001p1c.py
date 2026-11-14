"""Independent P1C public-data verifier. No runner/analyser imports, no native calls."""
from pathlib import Path
from hashlib import sha256
import json
import numpy as np
from scipy.stats import t,chi2,nct
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"data/tact-001-p1c"
def read(p):return json.loads(p.read_text(encoding="utf8"))
def rows(p):return [json.loads(s) for s in p.read_text(encoding="utf8").splitlines()]
def canonical(x):return sha256(json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False).encode()).hexdigest()
def verify():
    for name,value in read(DATA/"historical-archive.json")["sha256"].items():
        assert sha256((ROOT/name).read_bytes().replace(b"\r\n",b"\n")).hexdigest()==value,name
    if not (DATA/"effects.json").exists():
        assert not (DATA/"run-summary.json").exists() or not read(DATA/"run-summary.json")["scientific_series_complete"]
        print("P1C archive intact; awaiting complete pilot.");return
    r=read(DATA/"manifest.json");c=r["config"];z=read(DATA/"effects.json");seen=set();contexts=["high_press","deep_block"];arms=["D00","D15"];metrics=["points","xgd","gf","ga","xgf","xga"]
    assert canonical(c)==r["config_sha256"]
    data=rows(DATA/"main.jsonl");cube=np.empty((2,64,2,2,6))
    assert c["design"]["matrix"]==[dict(id="D00",levels=dict.fromkeys("ABCDE",-1)),dict(id="D15",levels=dict(A=1,B=1,C=1,D=1,E=-1))]
    for row in data:
        h=contexts.index(row["scenario"]);s=row["tested_side"];a=arms.index(row["arm"]);i=r["seeds"][h*64:(h+1)*64].index(row["seed"]);key=(h,i,s,a)
        assert key not in seen;seen.add(key)
        assert row["key"]==f"{contexts[h]}-{row['seed']}-{s}-{arms[a]}" and row["status"]=="ok"
        assert row["engine_readback"] and row["input_contract_verified"] and row["profile_fields_verified"]==1058 and 0<row["finish_tick"]<47996
        assert all(row[k]==v for k,v in c["identity"].items()) and row["config_sha256"]==r["config_sha256"]
        assert row["setup_sha256"]==c["design"]["setups"][contexts[h]][str(s)][arms[a]]
        levels=c["design"]["matrix"][a]["levels"]
        assert row["factor_levels"]==levels and row["design_matrix_sha256"]==canonical(c["design"]["matrix"])
        assert row["native_factor_bits"]=={f["code"]:f["high_bit"] if levels[f["code"]]==1 else 0 for f in c["design"]["factors"]}
        gf,ga=row["score"][s],row["score"][1-s];x,y=[row["team_statistics"][side]["xg"] for side in (s,1-s)]
        cube[key]=[3 if gf>ga else int(gf==ga),x-y,gf,ga,x,y]
    assert len(seen)==512 and np.isfinite(cube).all()
    values=(cube[:,:,0,1]-cube[:,:,0,0]+cube[:,:,1,1]-cube[:,:,1,0])/2
    rng=np.random.default_rng(int.from_bytes(sha256(b"TACT-001-P1C/bootstrap-v1").digest()[:8],"little"));idx=[rng.integers(64,size=(20000,64)) for _ in contexts];probs=[]
    for k,m in enumerate(metrics):
        record=z["primary"] if k==0 else z["secondary"][m]
        v=values[:,:,k];mu=float(v.mean());var=v.var(axis=1,ddof=1)/(4*64);se=float(np.sqrt(var.sum()));df=float(var.sum()**2/(var*var/63).sum())
        half=t.isf(.025,df)*se;p=float(2*t.sf(abs(mu/se),df))
        np.testing.assert_allclose([record["mean"],record["se"],record["df"],record["p"],*record["ci"]],[mu,se,df,p,mu-half,mu+half],atol=1e-11)
        boot=(v[0][idx[0]].mean(axis=1)+v[1][idx[1]].mean(axis=1))/2
        np.testing.assert_allclose(record["bootstrap_ci"],np.quantile(boot,[.025,.975]),atol=1e-11)
        for h,name in enumerate(contexts):
            np.testing.assert_allclose([record["context"][name]["mean"],record["context"][name]["sd"]],[v[h].mean(),v[h].std(ddof=1)],atol=1e-11)
        if k:probs.append((p,record["p_holm"]))
    ordered=sorted(probs)
    for i,(_,adjusted) in enumerate(ordered):np.testing.assert_allclose(adjusted,min(1,max((5-j)*ordered[j][0] for j in range(i+1))))
    primary=z["primary"];signal=primary["mean"]>=.15 and primary["ci"][0]>0 and primary["ci"][1]-primary["ci"][0]<=.30 and all(v["mean"]>0 for v in primary["context"].values())
    assert z["adequate_preregistered_signal"]==signal and not z["general_career_transfer_confirmed"] and not z["candidate_changed"]
    blocks=rows(DATA/"block-contrasts.jsonl");assert len(blocks)==128
    for b in blocks:
        h=contexts.index(b["context"]);i=r["seeds"][h*64:(h+1)*64].index(b["seed"])
        for k,m in enumerate(metrics):np.testing.assert_allclose(b["contrasts"][m],values[h,i,k],atol=1e-11)
    sd=values[:,:,0].std(axis=1,ddof=1)
    for name,case in z["planning"]["cases"].items():
        want=sd if name=="observed" else sd*np.sqrt(63/chi2.ppf(.025,63)) if name=="simultaneous95_normal_model_upper" else np.array([3.,3.])
        np.testing.assert_allclose(case["sd"],want)
        for row in case["power90"]+case["precision"]:
            n=row["n_per_context"];assert row["independent_blocks"]==2*n and row["matches"]==8*n
            def adequate(q):
                v=want**2/(4*q);se=np.sqrt(v.sum());df=v.sum()**2/(v*v/(q-1)).sum();cut=t.isf(.025,df)
                return nct.cdf(-cut,df,row["effect"]/se)+nct.sf(cut,df,row["effect"]/se)>=.9 if "effect" in row else 2*cut*se<=row["full_width"]
            assert adequate(n) and (n==2 or not adequate(n-1))
    plan=read(DATA/"seed-plan.json");assert len(set(plan["seeds"]))==131 and not set(plan["seeds"])&set(read(DATA/"excluded-seeds.json"))
    assert canonical(read(DATA/"excluded-seeds.json"))==plan["excluded_seed_set_sha256"]
    jobs=rows(DATA/"job-accounting.jsonl");assert len(jobs)==529 and len({x["key"] for x in jobs})==529 and all(x["reserved"] for x in jobs)
    assert sum(x["kind"]=="main" and x["status"]=="ok" for x in jobs)==512
    assert sum(x["kind"]=="technical" and x["status"]=="ok" for x in jobs)==16
    assert sum(x["status"]=="expected_rejection" for x in jobs)==1
    tech=rows(DATA/"technical.jsonl");assert len(tech)==16
    for h in contexts:
        for s in (0,1):
            for a in arms:
                pair=[x for x in tech if (x["scenario"],x["tested_side"],x["arm"])==(h,s,a)];assert len(pair)==2
                for field in ("score","finish_tick","team_statistics","seed","setup_sha256"):assert pair[0][field]==pair[1][field]
    budget=read(DATA/"budget.json");assert not budget["halted"] and budget["active"] is None and budget["charged_seconds"]<900 and budget["within_fixed_deadline"] and budget["elapsed_study_window_seconds"]<1800
    assert len(budget["reserved"])==529 and all(o["returncode"]==0 and not o["timed_out"] for o in budget["operations"])
    print("Verified P1C: 512 rows, six contrasts/t/bootstrap, Holm5, SD/power minima, 128 seed blocks, 529 attempts, unchanged historical archive.")
if __name__=="__main__":verify()

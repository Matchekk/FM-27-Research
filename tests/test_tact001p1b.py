"""P1B offline design, native encoding boundary, inference and deadline tests."""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from itertools import combinations
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import struct
import sys
import tempfile
import unittest

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from research.core import config_hash,schedule
from research.discovery import fractional_design
from research.native import read,write
from research.study_budget import DeadlineBudget
import analyse_tact001p1b as p
from run_tact001p1b import binary_audit,audit_contract
import run_tact001p1b as runner
from export_tact001p1b import FIELDS


def fixture():
    c=deepcopy(read(ROOT/"research/specs/TACT-001-P0.json"))
    c.update(experiment_id="TACT-001-P1B",status="registered",seed_namespace="TACT-001-P1B/test-only")
    c["budget"]["max_matches"]=2048
    c["design"].update(n_blocks=32,control_arm="D00",fraction=-1,generator="E=-A*B*C*D",matrix=p.matrix(),matrix_sha256=config_hash(p.matrix()),factors=list(p.FACTORS),
        arms=[dict(id=a,setup_sha256="a"*64) for a in p.ARMS],setups={h:{str(s):{a:config_hash([h,s,a]) for a in p.ARMS} for s in (0,1)} for h in p.CONTEXTS})
    c["preregistration"].update(commit="a"*40,document_sha256="d"*64,analysis_sha256="e"*64)
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(10000,10064)))
    data=[]
    for job in schedule(receipt):
        h=p.CONTEXTS.index(job["scenario"]);i=receipt["seeds"][h*32:(h+1)*32].index(job["seed"])
        X=p.matrix()[p.ARMS.index(job["arm"])]["levels"]
        beta={n:(j+1)*.1+.01*(i-15.5)+.01*h for j,n in enumerate(p.NAMES)}
        gamma={a+b:.02*(j+k+1)+.002*(i-15.5) for j,a in enumerate(p.NAMES) for k,b in enumerate(p.NAMES) if j<k}
        y=16+sum(beta[n]*X[n] for n in p.NAMES)+sum(v*X[n[0]]*X[n[1]] for n,v in gamma.items())+.3*job["side"]+i/50
        stat=dict(xg=1.,shots=25,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(stat),dict(stat)];teams[job["side"]]["xg"]+=y
        score=[0,0];score[job["side"]]=1
        data.append(dict(job,**job["identity"],status="ok",engine_readback=True,finish_tick=22000,
            input_contract_verified=True,profile_fields_verified=1058,tested_side=job["side"],score=score,team_statistics=teams,
            factor_levels=X,native_factor_bits={f["code"]:f["high_bit"] if X[f["code"]]==1 else 0 for f in p.FACTORS},design_matrix_sha256=config_hash(p.matrix())))
    return receipt,data


class FractionAndContractTests(unittest.TestCase):
    def test_completed_public_series_native_design_and_candidate_hashes(self):
        status=runner.PUBLIC/"run-summary.json"
        if not status.exists() or not read(status)["scientific_series_complete"]:return
        from research.native import rows
        receipt=read(runner.PUBLIC/"manifest.json")
        cube=p.checked(rows(runner.PUBLIC/"main.jsonl"),receipt)
        self.assertEqual(cube.shape,(2,32,2,16,11))
        self.assertEqual(read(status)["counts"],dict(technical=dict(ok=72,expected_rejection=1),main=dict(ok=2048)))
        effects=read(runner.PUBLIC/"effects.json")
        self.assertEqual(len(effects["primary"]),5);self.assertEqual(len(effects["interactions_exploratory"]),10)
        self.assertEqual(sum(map(len,effects["secondary"].values())),25)
        proposal=runner.PUBLIC/"candidates.json"
        if proposal.exists():
            candidates=read(proposal)["candidates"]
            self.assertLessEqual(len(candidates),2)
            self.assertEqual([x["design_id"] for x in candidates],[x["design_id"] for x in effects["candidates_exploratory"]])
            for c in candidates:
                for h in p.CONTEXTS:
                    for s in ("0","1"):
                        self.assertEqual(c["setup_sha256"][h][s],receipt["config"]["design"]["setups"][h][s][c["design_id"]])

    def test_real_public_native_technical_gate_and_archive_when_available(self):
        path=runner.PUBLIC/"technical-summary.json"
        if not path.exists():return
        gate=read(path);self.assertTrue(gate["passed"]);self.assertEqual(gate["readback_cells"],64)
        self.assertEqual(gate["negative"]["returncode"],108);self.assertEqual(len(gate["repeats"]),8)
        from research.native import rows
        data=rows(runner.PUBLIC/"technical.jsonl");self.assertEqual(len(data),72)
        grouped={}
        for row in data:
            self.assertEqual(row["status"],"ok");self.assertTrue(row["input_contract_verified"])
            self.assertEqual(row["profile_fields_verified"],1058)
            levels=p.matrix()[p.ARMS.index(row["arm"])]["levels"]
            self.assertEqual(row["factor_levels"],levels)
            self.assertEqual(row["native_factor_bits"],{f["code"]:f["high_bit"] if levels[f["code"]]==1 else 0 for f in p.FACTORS})
            grouped.setdefault((row["scenario"],row["tested_side"],row["arm"]),[]).append(row)
        self.assertEqual(len(grouped),64)
        for pair in grouped.values():
            if len(pair)==2:
                for key in ("score","finish_tick","team_statistics","setup_sha256","seed"):self.assertEqual(pair[0][key],pair[1][key])
        from hashlib import sha256
        for name,value in read(runner.PUBLIC/"historical-archive.json")["sha256"].items():
            self.assertEqual(sha256((ROOT/name).read_bytes().replace(b"\r\n",b"\n")).hexdigest(),value,name)

    def test_real_prepared_contract_matrix_and_native_binary_hashes_when_available(self):
        spec=ROOT/"research/specs/TACT-001-P1B.json"
        if not spec.exists():return
        c=read(spec);p.validate_design(c)
        public=read(runner.PUBLIC/"design-matrix.json")
        self.assertEqual(public["matrix"],c["design"]["matrix"])
        self.assertEqual(public["matrix_sha256"],c["design"]["matrix_sha256"])
        self.assertEqual(len(read(runner.PUBLIC/"binary-diff-audit.json")["audits"]),64)
        descriptors=read(runner.PUBLIC/"inputs.json")
        self.assertEqual(descriptors["setups"],c["design"]["setups"])
        runtime=ROOT/"local/runtime-v1114.6/source"
        if runtime.exists():
            for name,value in descriptors["runtime_source_sha256"].items():
                self.assertEqual(runner.source_hash(runtime/name),value,name)
        for h in p.CONTEXTS:
            for side in (0,1):
                baseline=read(ROOT/"data/tact-001-p0/inputs.json")["setups"][h][str(side)]["baseline"]
                self.assertEqual(c["design"]["setups"][h][str(side)]["D00"],baseline)
                for arm in p.ARMS:
                    key=f"{h}-{side}-{arm}"
                    self.assertEqual(descriptors["cell_overrides"][key]["levels"],p.matrix()[p.ARMS.index(arm)]["levels"])
                    binary=runner.LOCAL/"inputs"/(key+".bin")
                    if binary.exists():
                        from research.native import digest
                        self.assertEqual(digest(binary),c["design"]["setups"][h][str(side)][arm])

    def test_frozen_schedule_tech_coverage_and_export_boundary(self):
        receipt,_=fixture()
        self.assertEqual(runner.ordered_main(receipt),runner.ordered_main(receipt))
        self.assertEqual(len({j["key"] for j in runner.ordered_main(receipt)}),2048)
        self.assertEqual({j["scenario"] for j in runner.ordered_main(receipt)},set(p.CONTEXTS))
        with patch("run_tact001p1b.read",return_value=dict(technical_seeds=[1,2,3])):
            jobs=runner.technical_jobs()
        self.assertEqual(len(jobs),72)
        from collections import Counter
        counts=Counter((j["scenario"],j["side"],j["arm"]) for j in jobs)
        self.assertEqual(len(counts),64);self.assertEqual(sum(n==2 for n in counts.values()),8)
        self.assertEqual({a for (h,s,a),n in counts.items() if n==2},{"D00","D01"})
        self.assertTrue(all(j["seed"] in (1,2) for j in jobs))
        self.assertFalse(set(FIELDS)&{"config","binary","players","native_id","private_path","raw_log"})
        if (runner.PUBLIC/"seed-plan.json").exists():
            plan=read(runner.PUBLIC/"seed-plan.json")
            self.assertEqual(len(set(plan["seeds"])),67)
            self.assertFalse(set(plan["seeds"])&runner.historical(exclude_own=True))

    def test_explicit_negative_fraction_anchor_unique_orthogonal_resolution_v(self):
        X=np.array(list(map(lambda row:list(row.values()),fractional_design(p.NAMES,fraction=-1))))
        self.assertEqual(len(set(map(tuple,X))),16);np.testing.assert_array_equal(X[0],[-1]*5)
        np.testing.assert_array_equal(X[:,4],-X[:,:4].prod(axis=1))
        for order in range(1,5):
            for cols in combinations(range(5),order):self.assertEqual(np.prod(X[:,cols],axis=1).sum(),0)
        self.assertTrue(np.all(X.prod(axis=1)==-1))
        Y=np.array([list(row.values()) for row in fractional_design(p.NAMES)])
        np.testing.assert_array_equal(Y[:,4],Y[:,:4].prod(axis=1))
        for bad in (0,2,True,"-1"):
            with self.assertRaises(ValueError):fractional_design(p.NAMES,fraction=bad)

    def test_physical_main_and_pair_scaling_and_aliases(self):
        X=np.array([[r["levels"][n] for n in p.NAMES] for r in p.matrix()]);m,inter=p.coefficients()
        y=7+2*X[:,0]+3*X[:,0]*X[:,1]
        self.assertAlmostEqual(float(y@m["A"]),4)
        self.assertAlmostEqual(float(y@inter["AB"]),12)
        self.assertAlmostEqual(float(y@m["C"]),0)
        np.testing.assert_array_equal(X[:,0]*X[:,1],-X[:,2]*X[:,3]*X[:,4])

    def test_raw_binary_allows_only_assigned_factor_records(self):
        before=b"FM27CFG1"+struct.pack("<I",5)+b"".join(struct.pack("<5I",2,0,f["group_id"],0,f["low_id"]) for f in p.FACTORS)
        for row in p.matrix():
            after=before[:12]+b"".join(struct.pack("<5I",2,0,f["group_id"],0,f["high_id"] if row["levels"][f["code"]]==1 else f["low_id"]) for f in p.FACTORS)
            self.assertEqual(len(binary_audit(before,after,0,row["levels"])),sum(v==1 for v in row["levels"].values()))
            changed=bytearray(after);changed[-1]^=1
            with self.assertRaises(ValueError):binary_audit(before,bytes(changed),0,row["levels"])

    def test_contract_and_published_p1a_matrix_match_and_reject_sign_drift(self):
        receipt,_=fixture();p.validate_design(receipt["config"])
        original=read(ROOT/"data/tact-001-p1a/resolution-v-design.json")["levels"]
        self.assertEqual(original,[[r["levels"][n] for n in p.NAMES] for r in p.matrix()])
        c=deepcopy(receipt["config"]);c["design"]["fraction"]=1
        with self.assertRaises(ValueError):p.validate_design(c)

    def test_synthetic_known_effects_full_families_and_refuse_missing_or_native_drift(self):
        receipt,data=fixture();result,blocks=p.analyse(data,receipt)
        self.assertEqual(len(result["primary"]),5);self.assertEqual(len(result["interactions_exploratory"]),10)
        self.assertEqual(sum(map(len,result["secondary"].values())),25);self.assertEqual(len(blocks),960)
        for j,n in enumerate(p.NAMES):self.assertAlmostEqual(result["primary"][n]["mean"],2*((j+1)*.1+.005))
        for j,a in enumerate(p.NAMES):
            for k,b in enumerate(p.NAMES):
                if j<k:self.assertAlmostEqual(result["interactions_exploratory"][a+b]["mean"],4*.02*(j+k+1))
        with self.assertRaisesRegex(ValueError,"Incomplete"):p.checked(data[:-1],receipt)
        for field,value in (("native_factor_bits",{}),("factor_levels",{}),("design_matrix_sha256","0"*64),("seed",1)):
            broken=deepcopy(data);broken[0][field]=value
            with self.assertRaises(ValueError):p.checked(broken,receipt)

    def test_native_creator_flags_must_agree_with_design_not_only_json(self):
        receipt,data=fixture();r=data[0];job=dict(arm=r["arm"],side=0,config=dict(teams=[]))
        groups={f["group_id"]:dict(options=[dict(id=f["low_id"],native_bit=0),dict(id=f["high_id"],native_bit=f["high_bit"])]) for f in p.FACTORS}
        levels=p.matrix()[p.ARMS.index(r["arm"])]["levels"]
        selected={str(f["group_id"]):f["high_id"] if levels[f["code"]]==1 else f["low_id"] for f in p.FACTORS}
        job["config"]["teams"]=[dict(instructions=selected),dict(instructions=selected)]
        flags=sum(1<<f["high_bit"] for f in p.FACTORS if levels[f["code"]]==1)
        with tempfile.TemporaryDirectory() as temp:
            dump=Path(temp)/"dump.json";log=Path(temp)/"log.jsonl"
            write(dump,dict(teams=[dict(creator_hex=flags.to_bytes(16,"little").hex())]*2))
            log.write_text('{"event":"native_profile_bindings_verified","fields":1058}\n')
            lab=SimpleNamespace(server=SimpleNamespace(GROUPS=groups))
            self.assertEqual(audit_contract(lab,None,job,dict(dump=dump),log)["native_factor_bits"],{f["code"]:f["high_bit"] if levels[f["code"]]==1 else 0 for f in p.FACTORS})
            write(dump,dict(teams=[dict(creator_hex=(flags^(1<<47)).to_bytes(16,"little").hex())]*2))
            with self.assertRaisesRegex(ValueError,"instruction"):audit_contract(lab,None,job,dict(dump=dump),log)


class StudyDeadlineTests(unittest.TestCase):
    def test_deadline_not_reset_between_phases_or_reopen_and_caps_no_retry(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"budget.json";start=datetime(2026,11,14,tzinfo=timezone.utc)
            with patch("research.study_budget.utcnow",return_value=start):
                b=DeadlineBudget(path,seconds=30,wall_seconds=20,caps={"technical":1,"main":1})
                self.assertAlmostEqual(b.reserve("tech","technical",["t"]),15)
                b.finish(2.,0);deadline=b.load()["wall_deadline_utc"]
            with patch("research.study_budget.utcnow",return_value=start+timedelta(seconds=10)):
                b=DeadlineBudget(path,seconds=30,wall_seconds=20,caps={"technical":1,"main":1})
                self.assertAlmostEqual(b.reserve("main","main",["m"]),5)
                self.assertEqual(deadline,b.load()["wall_deadline_utc"]);b.finish(1.,0)
                with self.assertRaises(ValueError):b.reserve("retry","main",["m"])
            with patch("research.study_budget.utcnow",return_value=start+timedelta(seconds=21)):
                with self.assertRaisesRegex(ValueError,"UTC deadline"):b.reserve("another","main",[])

    def test_study_deadline_kills_dummy_child_and_keeps_attempt_consumed(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);b=DeadlineBudget(root/"b.json",seconds=30,wall_seconds=5.3)
            with self.assertRaises(ValueError):b.run("timeout","technical",["t"],[sys.executable,"-c","import time; time.sleep(10)"],ROOT,root/"out.txt")
            self.assertTrue(b.load()["halted"]);self.assertIn("t",b.load()["reserved"])


if __name__=="__main__":unittest.main()

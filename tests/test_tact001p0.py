from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from analyse_tact001p0 import analyse, contrast_cells, checked, SCENARIOS
from research.budget import NativeBudget
from research.core import config_hash, schedule
from research.native import read


def fixture():
    config=read(ROOT/"research/specs/TACT-001-P0.json")
    config["status"]="registered"
    config["preregistration"].update(commit="f"*40,document_sha256="d"*64,analysis_sha256="e"*64)
    seeds=read(ROOT/"data/tact-001-p0/seed-plan.json")["main_seeds"]
    receipt=dict(config=config,config_sha256=config_hash(config),seeds=seeds)
    data=[]
    for job in schedule(receipt):
        scenario=SCENARIOS.index(job["scenario"])
        index=seeds[scenario*8:(scenario+1)*8].index(job["seed"])
        p=job["arm"] in ("press","combined")
        line=job["arm"] in ("line","combined")
        interaction=1+2*scenario+index/10+(.2 if job["side"] else -.2)
        value=5+.4*p+.2*line+interaction*p*line
        team=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(team),dict(team)]
        teams[job["side"]]["xg"]=value
        row=dict(job,**job["identity"],tested_side=job["side"],status="ok",engine_readback=True,
                 input_contract_verified=True,finish_tick=22000,score=[0,0],team_statistics=teams)
        data.append(row)
    return receipt,data


class PilotContractTests(unittest.TestCase):
    def test_cell_hashes_follow_opponent_and_team_side(self):
        receipt,_=fixture()
        jobs=schedule(receipt)
        self.assertEqual(len(jobs),128)
        for job in jobs:
            self.assertEqual(job["setup_sha256"],receipt["config"]["design"]["setups"][job["scenario"]][str(job["side"])][job["arm"]])
        broken=deepcopy(receipt)
        broken["config"]["design"]["setups"]["high_press"]["0"].pop("line")
        broken["config_sha256"]=config_hash(broken["config"])
        with self.assertRaisesRegex(ValueError,"Incomplete cell"):
            schedule(broken)

    def test_interaction_direction_pairing_and_planning(self):
        receipt,data=fixture()
        indexed=checked(data,receipt)
        cells=contrast_cells(indexed,receipt["seeds"],"xgd")
        np.testing.assert_allclose(cells[0],np.arange(8)/10+1)
        np.testing.assert_allclose(cells[1],np.arange(8)/10+3)
        result=analyse(data,receipt)
        self.assertAlmostEqual(result["primary"]["mean"],2.35)
        self.assertEqual(result["primary"]["n_seed_blocks"],16)
        self.assertEqual(len(result["secondary"]),10)
        self.assertFalse(result["winner_selected"])
        self.assertGreaterEqual(result["confirmation_planning"][0]["observed_sd"]["total_seed_blocks"],
                                result["confirmation_planning"][-1]["observed_sd"]["total_seed_blocks"])
        self.assertTrue(all(row["upper95_each_sd"]["power_at_n"]>=.9 for row in result["confirmation_planning"]))

    def test_incomplete_drifted_or_unaudited_data_cannot_produce_effects(self):
        receipt,data=fixture()
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            analyse(data[:-1],receipt)
        data[0]["input_contract_verified"]=False
        with self.assertRaisesRegex(ValueError,"Unverified"):
            analyse(data,receipt)
        data[0]["input_contract_verified"]=True
        data[0]["engine_sha256"]="0"*64
        with self.assertRaisesRegex(ValueError,"mismatch"):
            analyse(data,receipt)


class DurableBudgetTests(unittest.TestCase):
    def test_new_process_view_does_not_reset_consumption_or_allow_retries(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"budget.json"
            budget=NativeBudget(path,seconds=30,caps={"technical":2,"main":1})
            budget.reserve("technical","technical",["a","b"])
            budget.finish(4.,0)
            reopened=NativeBudget(path,seconds=30,caps={"technical":2,"main":1})
            self.assertEqual(reopened.load()["charged_seconds"],4.)
            with self.assertRaisesRegex(ValueError,"already reserved"):
                reopened.reserve("retry","technical",["a"])
            with self.assertRaisesRegex(ValueError,"cap exceeded"):
                reopened.reserve("extra","technical",["c"])

    def test_interruption_and_failure_latch_survive_reopen(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"budget.json"
            budget=NativeBudget(path,seconds=30)
            budget.reserve("main","main",["job"])
            with self.assertRaisesRegex(ValueError,"Interrupted"):
                NativeBudget(path,seconds=30).reserve("new","main",["other"])
            budget.finish(1.,1)
            with self.assertRaisesRegex(ValueError,"Interrupted"):
                NativeBudget(path,seconds=30).reserve("new","main",["other"])

    def test_supervisor_executes_real_child_and_charges_wall_time(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            budget=NativeBudget(root/"budget.json",seconds=20)
            budget.run("probe","technical",[],[sys.executable,"-c","print('supervised child')"],ROOT,root/"out.txt")
            state=budget.load()
            self.assertGreater(state["charged_seconds"],0)
            self.assertIsNone(state["active"])
            self.assertIn("supervised child",(root/"out.txt").read_text())

    def test_hard_deadline_terminates_own_child_without_refunding_reservation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            budget=NativeBudget(root/"budget.json",seconds=5.3)
            with self.assertRaisesRegex(ValueError,"deadline"):
                budget.run("timeout","technical",["counted"],[sys.executable,"-c","import time;time.sleep(20)"],ROOT,root/"out.txt")
            state=budget.load()
            self.assertTrue(state["halted"])
            self.assertTrue(state["operations"][0]["timed_out"])
            self.assertIn("counted",state["reserved"])
            self.assertLess(state["charged_seconds"],5.3)


if __name__=="__main__":
    unittest.main()

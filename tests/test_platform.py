from copy import deepcopy
from itertools import combinations
from pathlib import Path
import tempfile
import unittest

import numpy as np
from scipy.stats import ttest_rel

from research.career import CONTROL_FIELDS, validate_checkpoints
from research.core import Registry, allocate, check_identity, config_hash, historical_seeds, schedule, validate, verify_artifacts
from research.discovery import fractional_design, features, propose
from research.native import read, write
from research.stats import estimate, holm, metrics, paired_cells, required_n

ROOT=Path(__file__).resolve().parents[1]


def contract(module="TACT"):
    identity=read(ROOT/"data/valid-002/validation-summary.json")["identity"]
    return dict(schema_version=1, experiment_id=module+"-900-test",module=module,kind="native",
        stage="technical",status="registered",hypothesis="Inputs reproduce",control="Baseline",
        intervention="Pressing",conditions="Controlled fixture",seed_namespace=module+"-900/technical",
        metrics=dict(primary="xgd",secondary=["gf","ga","points"]), identity=identity,
        design=dict(unit="seed_block",n_blocks=2,sides=[0,1],arms=[dict(id="baseline",setup_sha256="a"*64),
                    dict(id="press",setup_sha256="b"*64)],scenarios=[dict(id="standard",opponent="fixed",strength="equal",split="technical")]),
        science=dict(analysis="paired seed blocks",exclusions="None",negative_controls=["A/A"],readback_fields=["all"],
            stopping_rule="Fixed budget",selection_rule="No tactical selection",power_basis="Technical check only",
            multiple_testing="none",family_size=1,alpha=.05,power=None,min_effect=None),
        budget=dict(max_matches=8,max_workers=2,timeout_seconds=90),
        preregistration=dict(commit="f"*40,document_sha256="d"*64,analysis_sha256="e"*64))


def observation(job,value=0.):
    team=dict(xg=1.,shots=5,shots_on_target=2,passes=100,completed_passes=80,possession=.5)
    teams=[deepcopy(team),deepcopy(team)]
    teams[job["side"]]["xg"]+=value
    return dict(job,**job.get("identity",{}),status="ok",engine_readback=True,tested_side=job["side"],score=[0,0],team_statistics=teams)


class PlatformTests(unittest.TestCase):
    def test_registry_rejects_drafts_and_never_reuses_reserved_seeds(self):
        with tempfile.TemporaryDirectory() as temp:
            registry=Registry(Path(temp)/"registry")
            data=Path(temp)/"data"
            data.mkdir()
            config=contract()
            first=registry.register(config,data)
            other=deepcopy(config)
            other["experiment_id"]="TACT-901-test"
            second=registry.register(other,data) # identical namespace, but collisions must be skipped
            self.assertFalse(set(first["seeds"])&set(second["seeds"]))
            with self.assertRaisesRegex(ValueError,"already registered"):
                registry.register(config,data)
            other["status"]="draft"
            with self.assertRaisesRegex(ValueError,"Draft"):
                registry.register(other,data)

    def test_confirmation_registration_rejects_previously_seen_opponents(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            (root/"data").mkdir()
            registry=Registry(root/"registry")
            discovery=contract()
            discovery.update(stage="discovery",experiment_id="TACT-902-test")
            discovery["design"]["scenarios"][0]["split"]="discovery"
            discovery["science"].update(power=.9,min_effect=.1)
            registry.register(discovery,root/"data")
            confirm=deepcopy(discovery)
            confirm.update(stage="confirmation",experiment_id="TACT-903-test")
            confirm["design"]["scenarios"][0]["split"]="confirmation"
            confirm["metrics"]["primary"]="points"
            confirm["science"].update(frozen_candidate_sha256="b"*64,held_out_opponents=["fixed"],
                                      discovery_experiment_ids=["TACT-902-test"])
            with self.assertRaisesRegex(ValueError,"overlap"):
                registry.register(confirm,root/"data")
            confirm["design"]["scenarios"][0]["opponent"]="unseen"
            confirm["science"]["held_out_opponents"]=["unseen"]
            self.assertTrue(registry.register(confirm,root/"data")["seeds"])

    def test_every_module_draft_is_valid_and_cannot_run(self):
        specs=list((ROOT/"research/specs").glob("*.json"))
        self.assertEqual(len(specs),7)
        self.assertEqual({read(p)["module"] for p in specs},{"TACT","ATTR","TRAIN","SET","MECH"})
        for path in specs:
            value=read(path)
            validate(value)
            with self.assertRaisesRegex(ValueError,"Draft"):
                validate(value,executable=True)

    def test_historical_scan_includes_failures_and_pending_manifest_seeds(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            write(root/"manifest.json",dict(seeds={"confirmation":[123]},validation_seeds=[456]))
            (root/"failures.jsonl").write_text('{"seed":789,"status":"failed"}\n',encoding="utf8")
            self.assertTrue({0,123,456,789}<=historical_seeds(root))
        seeds=allocate("new-study/confirmation",10,historical_seeds(ROOT/"data"))
        self.assertEqual(len(set(seeds)),10)
        self.assertFalse(set(seeds)&historical_seeds(ROOT/"data"))

    def test_schedule_pairs_arms_and_sides_without_inflating_independent_n(self):
        config=contract()
        receipt=dict(config=config,config_sha256=config_hash(config),seeds=[1,2])
        jobs=schedule(receipt)
        self.assertEqual(len(jobs),8)
        actual=[observation(j, .4 if j["arm"]=="press" else 0) for j in jobs]
        cells=paired_cells(actual,jobs,"press")
        np.testing.assert_allclose(cells,[[.4,.4]])
        self.assertEqual(estimate(cells,resamples=50)["n_seed_blocks"],2)
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            paired_cells(actual[:-1],jobs,"press")
        with self.assertRaisesRegex(ValueError,"duplicate"):
            paired_cells(actual+[actual[0]],jobs,"press")
        actual[0]["status"]="failed"
        with self.assertRaisesRegex(ValueError,"Failed"):
            paired_cells(actual,jobs,"press")

    def test_estimate_matches_independent_scipy_paired_calculation(self):
        a=np.array([1.1,.3,.6,-.4,1.2])
        b=np.array([.1,.7,.2,-.3,.4])
        reference=ttest_rel(a,b)
        result=estimate([a-b],resamples=500)
        self.assertAlmostEqual(result["p"],reference.pvalue)
        np.testing.assert_allclose(result["ci"],list(reference.confidence_interval()))
        np.testing.assert_allclose(holm([.001,.02,.018,.6]),[.004,.054,.054,.6])
        self.assertGreater(required_n(.1,1.,.9),required_n(.2,1.,.9))
        with self.assertRaisesRegex(ValueError,"finite"):
            estimate([[1.,float("nan")]])

    def test_finishing_can_change_goals_without_changing_xgd(self):
        job=dict(side=0)
        a=observation(job)
        b=deepcopy(a)
        b["score"]=[2,0]
        self.assertEqual(metrics(a)["xgd"],metrics(b)["xgd"])
        self.assertNotEqual(metrics(a)["points"],metrics(b)["points"])

    def test_identity_drift_and_unvalidated_builds_fail_closed(self):
        expected=contract()["identity"]
        validation=dict(passed=True,identity=expected)
        check_identity(expected,expected,validation)
        for field in expected:
            changed=dict(expected,**{field:"changed"})
            with self.assertRaisesRegex(ValueError,"drift"):
                check_identity(expected,changed,validation)
        with self.assertRaisesRegex(ValueError,"not passed"):
            check_identity(expected,expected,dict(validation,passed=False))

    def test_registration_tampering_leakage_and_uncorrected_family_rejected(self):
        config=contract()
        for change in (dict(stage="confirmation"),dict(status="draft")):
            with self.assertRaises(ValueError):
                validate(dict(config,**change),executable=True)
        changed=deepcopy(config)
        changed["science"]["family_size"]=2
        with self.assertRaisesRegex(ValueError,"uncorrected"):
            validate(changed)
        receipt=dict(config=config,config_sha256="wrong",seeds=[1,2])
        with self.assertRaisesRegex(ValueError,"changed"):
            schedule(receipt)

    def test_artifact_verifier_refuses_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                verify_artifacts(Path(temp)/"inside",{"../other":"a"*64})

    def test_resolution_v_design_separates_all_main_and_pair_interactions(self):
        names=list("ABCDE")
        design=fractional_design(names)
        x=np.array([features(c,names) for c in design])
        self.assertEqual(x.shape,(16,16))
        np.testing.assert_allclose(x.T@x,16*np.eye(16))
        observed=[dict(factors=c,mean=.1*c["A"],se=.1,split="discovery") for c in design[:8]]
        suggestions=propose(observed,design,names,limit=2)
        self.assertEqual(len(suggestions),2)
        observed[0]["split"]="confirmation"
        with self.assertRaisesRegex(ValueError,"Held-out"):
            propose(observed,design,names)

    def test_career_adapter_detects_calendar_drift_and_missing_branches(self):
        checkpoint=dict.fromkeys(CONTROL_FIELDS,"a"*64)
        checkpoint.update(calendar_readback_verified=True,individual_exposure_verified=True,
                          checkpoint_sha256="b"*64,intervention_readback_sha256="c"*64,outcomes=dict(ca_change=1))
        data=[dict(checkpoint,replicate=1,arm=arm,week=week) for arm in ("baseline","intervention") for week in (0,6)]
        self.assertEqual(validate_checkpoints(data,["baseline","intervention"],[0,6])["branches"],2)
        with self.assertRaisesRegex(ValueError,"Incomplete"):
            validate_checkpoints(data[:-1],["baseline","intervention"],[0,6])
        data[-1]["calendar_sha256"]="drift"
        with self.assertRaisesRegex(ValueError,"drift"):
            validate_checkpoints(data,["baseline","intervention"],[0,6])


if __name__=="__main__":
    unittest.main()

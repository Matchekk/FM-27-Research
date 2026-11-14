"""Offline numeric contracts; no game/adapter initialization."""
from itertools import combinations
from pathlib import Path
from statistics import mean, variance
import json
import sys
import unittest

import numpy as np
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import analyse_tact001p1a as p1


class PrecisionAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest,cls.cube=p1.load()
        cls.effects=p1.read(p1.DEST/"exploratory-effects.json")
        cls.designs=p1.read(p1.DEST/"design-comparison.json")

    def test_independent_scalar_reconstruction_of_all_thirty_estimates(self):
        # Scalar arithmetic/statistics, independent of the einsum analysis path.
        for name,c in p1.CONTRASTS.items():
            for m,metric in enumerate(p1.METRICS):
                cells=[[mean(sum(c[a]*float(self.cube[h,i,s,a,m]) for a in range(4))
                             for s in range(2)) for i in range(8)] for h in range(2)]
                mu=mean(mean(x) for x in cells)
                terms=[variance(x)/32 for x in cells]
                v=sum(terms);df=v*v/sum(z*z/7 for z in terms)
                half=t.isf(.025,df)*v**.5
                actual=self.effects["contrasts"][name][metric]
                np.testing.assert_allclose([actual["mean"],actual["se"],*actual["ci95"]],
                                           [mu,v**.5,mu-half,mu+half],atol=1e-12)

    def test_historical_archive_fingerprints_and_zero_new_activity(self):
        receipt=p1.read(p1.DEST/"source-manifest.json")
        for path,digest in receipt["sha256"].items():
            self.assertEqual(p1.text_digest(ROOT/path),digest,path)
        self.assertEqual(p1.text_digest(p1.__file__),receipt["analysis_sha256"])
        self.assertEqual(p1.audit_archive(self.manifest),receipt["historical_archive_audit"])
        self.assertEqual(receipt["native_matches_started"],0)
        self.assertEqual(receipt["new_seeds_reserved"],0)
        self.assertFalse(p1.read(p1.DEST/"resolution-v-design.json")["executed"])
        self.assertEqual(p1.read(p1.DEST/"resolution-v-design.json")["seeds"],[])

    def test_negative_half_fraction_baseline_alias_sign_and_orthogonality(self):
        X=p1.fractional_v()
        self.assertEqual(X.shape,(16,5))
        self.assertTrue(any(np.all(row==-1) for row in X))
        self.assertTrue(np.all(X.prod(axis=1)==-1))
        columns=[np.ones(16),*X.T,*[X[:,i]*X[:,j] for i,j in combinations(range(5),2)]]
        np.testing.assert_array_equal(np.array(columns)@np.array(columns).T,16*np.eye(16))
        # AB is negatively aliased with CDE; main A with BCDE.
        np.testing.assert_array_equal(X[:,0]*X[:,1],-X[:,2]*X[:,3]*X[:,4])
        np.testing.assert_array_equal(X[:,0],-X[:,1]*X[:,2]*X[:,3]*X[:,4])

    def test_integer_allocation_minimizes_fixed_weight_variance(self):
        for v in ([9.,1.],[1.,9.],[2.,2.]):
            result=p1.allocation(v,1000,4,optimal=True)
            choices=[v[0]/n+v[1]/(250-n) for n in range(8,243)]
            self.assertAlmostEqual(result["variance"],min(choices)/4)
            self.assertEqual(sum(result["counts"])*4,1000)
        with self.assertRaises(ValueError):p1.allocation([1.,1.],20,4)

    def test_finite_calibration_cost_and_uncertainty_are_counted(self):
        covariance=[np.array(self.effects["arm_covariance_xgd"][h]) for h in p1.CONTEXTS]
        for name in ("press_isolated","interaction"):
            c=np.array(p1.CONTRASTS[name]);cost=2*np.count_nonzero(c)
            result=p1.cv_grid(covariance,c)
            for row in result["alternatives"]:
                self.assertLessEqual(row["matches"],1000)
                self.assertEqual(row["matches"],cost*sum(row["paired_blocks"])+2*sum(row["calibration_blocks"]))
                total=0.
                for S,n,m,b in zip(covariance,row["paired_blocks"],row["calibration_blocks"],row["beta"]):
                    residual=c@S@c-2*b*(c@S[:,0])+b*b*S[0,0]
                    total+=residual/(4*n)+b*b*S[0,0]/(4*m)
                self.assertAlmostEqual(row["variance"],total)

    def test_side_covariance_identity_block_model_and_leave_one_out(self):
        for name in p1.CONTRASTS:
            for h in p1.CONTEXTS:
                d=self.effects["dependence"][name][h]
                self.assertAlmostEqual(d["paired_side_variance"],
                    d["independent_side_counterfactual_variance"]+d["side_covariance"]/2)
            if name in self.effects["block_model"]["estimates"]:
                self.assertAlmostEqual(self.effects["block_model"]["estimates"][name],self.effects["contrasts"][name]["xgd"]["mean"])
        rows=[json.loads(x) for x in (p1.DEST/"seed-influence.jsonl").read_text().splitlines()]
        self.assertEqual(len(rows),96)
        for row in rows:
            c=np.array(p1.CONTRASTS[row["contrast"]]);h=p1.CONTEXTS.index(row["context"])
            cells=self.cube[:,:,:,:,0]@c
            cells=cells.mean(axis=2)
            i=self.manifest["seeds"][h*8:(h+1)*8].index(row["seed"])
            expected=(np.delete(cells[h],i).mean()+cells[1-h].mean())/2
            self.assertAlmostEqual(expected,row["leave_one_out_mean"])

    def test_power_minima_and_transfer_sensitivity(self):
        tau=np.array(list(self.designs["orthogonal_noise_tau2"].values()))
        for row in self.designs["conditional_90_power_requirements"]["rows"]:
            v=tau*row["variance_multiplier"]/4;n=row["blocks_per_context"]
            self.assertGreaterEqual(p1.forecast(v,[n,n],alpha=.01,effect=row["effect"])["power"],.9)
            self.assertLess(p1.forecast(v,[n-1,n-1],alpha=.01,effect=row["effect"])["power"],.9)
            self.assertEqual(row["matches"],n*64)
        for plan in self.designs["doe_forecasts"]:
            powers=[x["power"] for x in plan["variance_transfer_sensitivity"].values()]
            self.assertEqual(powers,sorted(powers,reverse=True))

    def test_followup_is_unexecuted_and_budget_families_are_consistent(self):
        plan=p1.read(p1.DEST/"next-study-plan.json")
        self.assertFalse(plan["execution_authorized"])
        self.assertEqual(plan["seeds_reserved"],[])
        self.assertEqual(plan["native_matches_started"],0)
        self.assertEqual([row["levels"] for row in plan["design"]],p1.fractional_v().tolist())
        for b in plan["budgets"]:
            self.assertEqual(b["main_matches"],b["main_blocks"]*32)
            self.assertEqual(b["main_blocks"],2*b["main_blocks_per_context"])
            self.assertEqual(b["maximum_match_attempts"],b["main_matches"]+73)
            self.assertEqual(b["maximum_full_matches"],b["main_matches"]+72)
        self.assertEqual(len(plan["primary_family"]["contrasts"]),5)
        self.assertEqual(len(plan["secondary_family"]["metrics"])*5,25)
        self.assertEqual(len(plan["interaction_family"]["contrasts"]),10)
        self.assertEqual(plan["factors"][3]["high"]["label"],"Shorter")


if __name__=="__main__":unittest.main()

from collections import defaultdict
from pathlib import Path
import unittest

from research.native import read, rows
from research.stats import metrics
from research.core import historical_seeds, schedule

ROOT=Path(__file__).resolve().parents[1]/"data/valid-002"


class ValidationEvidenceTests(unittest.TestCase):
    def test_platform_smoke_is_complete_disjoint_and_identical_aa(self):
        folder=ROOT.parent/"platform-smoke"
        self.assertTrue(folder.is_dir(), "Published native platform smoke is missing")
        receipt=read(folder/"manifest.json")
        matches=rows(folder/"matches.jsonl")
        planned=schedule(receipt)
        self.assertEqual({r["key"] for r in matches},{j["key"] for j in planned})
        prior=set()
        for path in ROOT.parent.iterdir():
            if path.is_dir() and path!=folder:
                prior.update(historical_seeds(path))
        self.assertFalse(set(receipt["seeds"])&prior)
        for seed in receipt["seeds"]:
            pair=[r for r in matches if r["seed"]==seed]
            self.assertEqual(len(pair),2)
            for key in ("setup_sha256","score","finish_tick","team_statistics"):
                self.assertEqual(pair[0][key],pair[1][key])
        self.assertTrue(read(folder/"summary.json")["all_aa_exact"])

    def test_published_native_results_reproduce_all_repeat_checks(self):
        summary=read(ROOT/"validation-summary.json")
        data=rows(ROOT/"matches.jsonl")
        self.assertEqual(len(data),42)
        grouped=defaultdict(list)
        for row in data:
            self.assertEqual(row["build"],summary["identity"]["build"])
            metrics(row)
            if row["technical_group"]=="core":
                grouped[row["arm"],row["seed"]].append(row)
        self.assertEqual(len(grouped),8)
        for group in grouped.values():
            self.assertEqual(len(group),2)
            for key in ("score","finish_tick","team_statistics"):
                self.assertEqual(group[0][key],group[1][key])
        self.assertTrue(summary["passed"])
        self.assertFalse(summary["career_fixture_validated"])


if __name__=="__main__":
    unittest.main()

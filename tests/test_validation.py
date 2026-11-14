from collections import defaultdict
from pathlib import Path
import unittest

from research.native import read, rows
from research.stats import metrics

ROOT=Path(__file__).resolve().parents[1]/"data/valid-002"


class ValidationEvidenceTests(unittest.TestCase):
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

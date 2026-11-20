import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
from contract_followup import outcome


class RetentionFollowup(unittest.TestCase):
    def test_signed_future_does_not_count_as_effective(self):
        base = {"contract_end": "2027-06-30", "scan_agrees_end": True,
                "contract_start": "2026-07-01", "owner_missing": False,
                "contract_owner": True, "future_spells": []}
        future = {"same_club": True, "has_terms": True, "start": "2027-07-01", "end": "2030-06-30"}
        changed = dict(base, future_spells=[future])
        self.assertEqual(outcome(base, changed, "2027-03-30", "2027-04-30"),
                         "future_same_club_terms_observed_not_started")
        effective = dict(base, contract_start="2027-07-01", contract_end="2030-06-30")
        self.assertEqual(outcome(base, effective, "2027-03-30", "2027-07-02"),
                         "later_end_confirmed_new_start_observed")
        self.assertEqual(outcome(base, None, "2027-03-30", "2027-04-30"),
                         "not_located_in_followup_club_inventory")

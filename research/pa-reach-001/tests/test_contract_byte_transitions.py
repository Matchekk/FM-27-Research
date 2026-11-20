from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "analysis"))
from contract_byte_transitions import change, classify, standardized_contrast


class ContractEvidenceTests(unittest.TestCase):
    def test_requires_later_confirmed_end_and_start_inside_open_closed_window(self):
        first,last="2027-03-30","2027-04-30"
        a=(1,3,"readable","2026-07-01","2027-06-30",())
        def terms(start,end,status="readable"):
            return (1,5,status,start,end,())
        self.assertEqual(classify(a,terms(last,"2028-06-30"),first,last),
                         "new_chain_start_and_later_confirmed_end")
        for start,end in [(first,"2028-06-30"),("2027-05-01","2028-06-30"),(last,"2027-06-30")]:
            self.assertEqual(classify(a,terms(start,end),first,last),"other_contract_date_change")
        self.assertEqual(classify(a,terms(last,"2028-06-30","end_not_independently_confirmed"),first,last),
                         "contract_evidence_missing")
        self.assertEqual(change(0,4),"zero_0_to_4")

    def test_club_and_initial_byte_must_have_common_support(self):
        d=standardized_contrast({(1,3):[2,1,4,1],(2,1):[3,2,0,0],(1,2):[0,0,1,1]})
        self.assertEqual(d["exposed_on_common_support"],2)
        self.assertEqual(d["clubs"],1)
        self.assertEqual(d["change_fraction_difference"],0.25)
        self.assertIsNone(d["career_cluster_95ci"])

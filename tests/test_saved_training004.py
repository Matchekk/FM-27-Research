from copy import deepcopy
import unittest

from analysis.audit_saved_training004 import audit


class SavedCalendarTests(unittest.TestCase):
    def report(self):
        return dict(profile='R2',snapshot_stable=True,probes=[
            dict(probe='open',coverage=dict(game_date_claim='2027-01-16')),
            dict(probe='training',status='observed',coverage=dict(rows=1,teams=[
                dict(team_code='T00',weeks=1,days=7,last_week='2027-01-18',
                     raw_session_counts={'0':2,'300':10,'999':9})]))])

    def test_unknown_codes_and_future_slots_never_become_completed_exposure(self):
        result=audit(self.report())
        self.assertEqual(result['total']['saved_slots'],21)
        self.assertEqual(result['total']['reader_labelled_slots'],12)
        self.assertEqual(result['unknown_code_counts'],{'999':9})
        self.assertTrue(result['teams'][0]['last_saved_week_after_parser_save_date'])
        self.assertIsNone(result['completed_session_exposure'])
        self.assertIsNone(result['individual_attendance'])
        self.assertFalse(result['ui_label_verified'])

    def test_failed_and_unbegun_training_do_not_imply_zero_slots(self):
        for status in ('failed','not_started'):
            report=self.report();report['probes'][1]['status']=status
            with self.assertRaises(ValueError):audit(report)

    def test_inconsistent_slot_denominator_is_rejected(self):
        report=self.report();report['probes'][1]['coverage']['teams'][0]['raw_session_counts']['0']=3
        with self.assertRaises(ValueError):audit(report)
        report=self.report();report['snapshot_stable']=False
        with self.assertRaises(ValueError):audit(report)


if __name__=='__main__':unittest.main()

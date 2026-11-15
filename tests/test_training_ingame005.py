"""Prevent errors encountered in live collection: identity, arm, date and missingness."""
from copy import deepcopy
from datetime import timedelta
import unittest

from analysis.training_ingame005 import START, summarize


def observation(arm, day, acc=14, pace=14, ca=134):
    return dict(experiment='TRAIN-005-INGAME', career_cluster='C001', player='P001',
                identity_verified=True, ca_measure='STORED_CA',
                attribute_resolution='ROUNDED_UI', arm=arm, elapsed_days=day,
                game_date=(START + timedelta(days=day)).isoformat(),
                acceleration_ui=acc, pace_ui=pace, stored_ca=ca, stored_pa=160,
                condition_ui=99, sharpness_ui=99, minutes_current_season=None,
                pilot_injury_days=None, focus_code=-1 if arm == 'A' else 9,
                profile_sha256='a' * 64, native_inventory_sha256='b' * 64)


class IngameTrainingTests(unittest.TestCase):
    def test_paired_contrast_direction_and_no_single_pair_ci(self):
        data = [observation('A', 0), observation('B', 0),
                observation('A', 56, 15, 14), observation('B', 56, 15, 16)]
        result = summarize(data)
        self.assertEqual(result['primary_contrast_B_minus_A'], 1)
        self.assertEqual(result['independent_career_clusters'], 1)
        self.assertEqual(result['complete_career_pairs'], 1)
        self.assertIsNone(result['confidence_interval'])
        self.assertIsNone(result['p_value'])

    def test_missing_or_incomplete_is_not_zero_effect(self):
        result = summarize([observation('A', 0), observation('A', 14, ca=135)])
        self.assertIsNone(result['primary_contrast_B_minus_A'])
        data = [observation('A', 0), observation('B', 0),
                observation('A', 56), observation('B', 56, acc=None)]
        result = summarize(data)
        self.assertIsNone(result['primary_contrast_B_minus_A'])
        self.assertIsNone(result['arms']['B']['delta_quickness_ui_at_last_observation'])

    def test_rejects_player_reordering_arm_swaps_and_wrong_clock(self):
        baseline = observation('A', 0)
        for key, value in [('identity_verified', False), ('focus_code', 9),
                           ('ca_measure', 'MODEL_RCA'), ('game_date', '2027-01-17')]:
            row = deepcopy(baseline)
            row[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                summarize([row])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            summarize([baseline, deepcopy(baseline)])
        with self.assertRaisesRegex(ValueError, 'baseline'):
            summarize([observation('A', 14)])


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from copy import deepcopy
from analysis.night003_pos import jobs,group_jobs,target_slots,audit_positional_start,ARMS
from analysis.analyse_night003_pos import planning
from research.startpolicy import encode_records

class PositionalSharpnessTest(unittest.TestCase):
    def test_fixed_group_sample_and_separation(self):
        p=jobs('main',list(range(1,1025)))
        self.assertEqual(len(p),4096)
        self.assertEqual(len({j['key'] for j in p}),4096)
        self.assertEqual(len(group_jobs(p)),1024)
        self.assertEqual(target_slots('ATTACK_LOW'),(8,10))
        self.assertEqual(target_slots('DEFENCE_LOW'),(2,3))
        self.assertFalse(set(target_slots(ARMS[0]))&set(target_slots(ARMS[1])))
    def test_smoke_is_sixteen_plus_negative(self):
        p=jobs('technical',[1025,1026,1027,1028])
        self.assertEqual(len(p),17)
        self.assertEqual([len(b) for b in group_jobs(p,technical=True)],[4,4,4,4,1])
    def test_difference_of_marginals_baseline_cancels(self):
        high,attack_low,defence_low=2.,1.7,1.9
        self.assertAlmostEqual((high-attack_low)-(high-defence_low),defence_low-attack_low)
    def test_planning_uses_archived_contrast(self):
        p=planning();self.assertEqual(p['matches'],4096)
        self.assertGreater(p['anchors']['observed']['power']['0.15'],.9)
    def test_identity_bound_gate_rejects_wrong_group_extra_actor_and_single_field(self):
        binary=encode_records([(11,s,i,0,i) for s in (0,1) for i in range(11)])
        evidence=[dict(event='native_passive_state',stage=stage) for stage in ('prepared','first_advance','finished')]
        players={}
        for s in (0,1):
            for i in range(23):
                affected=s==1 and i in (8,10);expected=7000 if affected else 10000
                cache=bytearray(16);cache[9]=100;cache[10]=70 if affected else 100
                players[s,i]=dict(side=s,roster_index=i,sharpness_raw=expected,sharpness_secondary_raw=expected,
                    condition_raw=10000,fatigue_raw=0,condition_accumulator_raw=1000000,sharpness_penalty_raw=0,
                    statistics_cache_region_hex=cache.hex())
        with patch('analysis.night003_pos.snapshot',return_value=players):
            audit_positional_start(evidence,binary,1,'ATTACK_LOW')
            with self.assertRaises(ValueError):audit_positional_start(evidence,binary,1,'DEFENCE_LOW')
        for key,field,value in (((1,7),'sharpness_raw',7000),((1,8),'sharpness_secondary_raw',10000),((0,8),'sharpness_raw',7000)):
            bad=deepcopy(players);bad[key][field]=value
            with patch('analysis.night003_pos.snapshot',return_value=bad):
                with self.assertRaises(ValueError):audit_positional_start(evidence,binary,1,'ATTACK_LOW')

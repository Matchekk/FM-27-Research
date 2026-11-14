"""Offline admission, frozen-seed and failure-accounting regressions."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from analysis import run_split004 as runner
from research.native import read, write


class SplitRunnerTests(unittest.TestCase):
    def test_seed_scan_excludes_own_nested_plan_but_retains_sibling_and_old(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);local=root/'local/night-002/split004'
            for path,seed in [(local/'seed-plan.json',11),
                    (root/'local/night-002/other/seed-plan.json',12),
                    (root/'data/old/seed-plan.json',13),
                    (root/'local/registry/OTHER.reserved.json',14)]:
                path.parent.mkdir(parents=True,exist_ok=True);write(path,dict(seeds=[seed]))
            public=root/'data/night-002-split004';public.mkdir()
            write(public/'seed-plan.json',dict(seeds=[11]))
            with patch.object(runner,'ROOT',root),patch.object(runner,'LOCAL',local), \
                 patch.object(runner,'PUBLIC',public),patch.object(runner,'REGISTRY',root/'local/registry'):
                prior=runner.previous_seeds()
            self.assertTrue({12,13,14}<=prior);self.assertNotIn(11,prior)

    def test_immediate_main_requires_own_global_child_and_utc_reserve(self):
        now=datetime(2026,11,14,23,tzinfo=timezone.utc)
        inner=dict(experiment=runner.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,
            wall_limit_seconds=5400,halted=False,charged_seconds=100.,active=None,
            wall_deadline_utc=(now+timedelta(seconds=1800)).isoformat())
        night=dict(charged_seconds=100.,active=dict(name=runner.EXPERIMENT+'/main',
            start_utc=now.isoformat(),child_deadline_utc=(now+timedelta(seconds=1000)).isoformat()))
        self.assertGreaterEqual(runner.main_remaining(inner,night,now),600)
        for source in ('own_charge','own_wall','outer_deadline','outer_charge','old_window'):
            a,b=deepcopy(inner),deepcopy(night)
            if source=='own_charge':a['charged_seconds']=301.
            elif source=='own_wall':a['wall_deadline_utc']=(now+timedelta(seconds=599)).isoformat()
            elif source=='outer_deadline':b['active']['child_deadline_utc']=(now+timedelta(seconds=599)).isoformat()
            elif source=='outer_charge':b['charged_seconds']=3001.
            else:a['wall_limit_seconds']=3600
            with self.subTest(source=source),self.assertRaises(ValueError):runner.main_remaining(a,b,now)

    def test_parent_reconciliation_requires_fixed_new_window_and_all_reservations(self):
        keys=[f'tech-{i}' for i in range(33)]
        op=dict(name='technical',kind='technical',keys=keys,elapsed_seconds=10.,returncode=0,timed_out=False,
            start_utc='2026-11-14T23:00:01+00:00',child_deadline_utc='2026-11-14T23:14:56+00:00')
        state=dict(experiment=runner.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,
            wall_limit_seconds=5400,halted=False,active=None,operations=[op],charged_seconds=10.,
            reserved={k:'technical' for k in keys},wall_start_utc='2026-11-14T23:00:00+00:00',
            wall_deadline_utc='2026-11-15T00:30:00+00:00')
        proof=dict(experiment_id=runner.EXPERIMENT,phase='technical',budget_sha256='a'*64,
            completed_utc='2026-11-14T23:00:12+00:00')
        self.assertTrue(runner.phase_budget_gate('technical',state,proof,'a'*64,dict(technical=keys)))
        for key,value in [('halted',True),('charged_seconds',0),('operations',[]),('wall_limit_seconds',3600)]:
            bad=deepcopy(state);bad[key]=value
            self.assertFalse(runner.phase_budget_gate('technical',bad,proof,'a'*64,dict(technical=keys)))
        self.assertFalse(runner.phase_budget_gate('technical',state,proof,'b'*64,dict(technical=keys)))

    def test_uncertain_cleanup_retains_pending_and_job_limit_three(self):
        from research.native_process005 import CleanupUnconfirmed
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);write(local/'private-host.json',dict(observer_host='never-executed.exe'))
            job=dict(key='negative-malformed',kind='negative',seed=None)
            with patch.object(runner,'LOCAL',local),patch.object(runner,'admission',return_value=30), \
                 patch('research.native_process005.contained_call',return_value=(0,.01)) as invoke, \
                 patch('research.native_process005.confirmed_cleanup',return_value=False):
                with self.assertRaises(CleanupUnconfirmed):
                    runner.native_job(job,'technical',[job['key']],dict(identity=dict(engine_sha256='a'*64)),lambda:None)
            self.assertTrue((local/'technical/jobs/negative-malformed/pending.json').exists())
            self.assertEqual(invoke.call_args.kwargs['max_processes'],3)
            self.assertEqual(invoke.call_args.kwargs['timeout'],90)

    def test_public_budget_has_no_tokens_or_private_unknown_fields(self):
        result=runner.safe_budget(dict(charged_seconds=2.,active=dict(token='secret',owner_pid=10,
            name='technical',kind='technical',keys=['allowed','private-id'],elapsed_seconds=None),
            operations=[],halted=False,private_path='private'),{'allowed'})
        self.assertEqual(result['active']['keys'],['allowed'])
        self.assertIsNone(result['active']['elapsed_seconds'])
        self.assertNotIn('secret',str(result));self.assertNotIn('private-id',str(result))


if __name__=='__main__':unittest.main()

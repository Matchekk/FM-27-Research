"""Offline admission, frozen-seed and failure-accounting regressions."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from threading import Barrier, Lock
import time

from analysis import run_stless003 as runner
from research.native import read, write


class StlessRunnerTests(unittest.TestCase):
    def test_low_budget_serial_dispatch_keeps_all_jobs_and_immutable_markers(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);active=0;peak=0;lock=Lock()
            jobs=[dict(key=f'job-{i}',seed=7) for i in range(8)]
            def invoke(job,on_start):
                nonlocal active,peak
                on_start()
                with lock:active+=1;peak=max(peak,active)
                time.sleep(.005)
                with lock:active-=1
                return dict(job_id=job['key'],status='ok',native_elapsed_seconds=1.)
            with patch.object(runner,'LOCAL',local):
                scheduler=runner.CallBudgetScheduler(local/'main/dispatch',invoke,lambda j:None)
                result=scheduler.run([jobs],dict(prior_native_call_seconds=3400.))
                proof=runner.call_envelope(dict(prior_native_call_seconds=3400.),reserve_new_claim=False)
            self.assertEqual(len(result),8);self.assertEqual(peak,1);self.assertEqual(scheduler.peak,1)
            self.assertEqual(len(list((local/'main/dispatch').glob('*.started.json'))),8)
            self.assertEqual(proof['recorded_native_call_seconds'],3408.);self.assertEqual(proof['unresolved_claims'],0)

    def test_parallel_block_finishes_before_gate_changes_to_serial(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);barrier=Barrier(4,timeout=2);lock=Lock();active=0;peak={0:0,1:0}
            blocks=[[dict(key=f'b{b}-job-{i}',seed=7,block=b) for i in range(8)] for b in (0,1)]
            def invoke(job,on_start):
                nonlocal active
                on_start();b=job['block']
                with lock:active+=1;peak[b]=max(peak[b],active)
                if b==0:barrier.wait()
                else:time.sleep(.005)
                with lock:active-=1
                return dict(job_id=job['key'],status='ok',native_elapsed_seconds=1.)
            # Gate refresh is before first block, after block0, after block1.
            proofs=[dict(recorded_native_call_seconds=v,unresolved_claims=0) for v in (100.,3400.,3408.)]
            audits=[]
            with patch.object(runner,'LOCAL',local),patch.object(runner,'call_envelope',side_effect=proofs):
                scheduler=runner.CallBudgetScheduler(local/'main/dispatch',invoke,lambda j:None,
                    lambda block:audits.append((block[0]['block'],active)))
                result=scheduler.run(blocks,dict(prior_native_call_seconds=100.))
            self.assertEqual(len(result),16);self.assertEqual(peak,{0:4,1:1});self.assertEqual(audits,[(0,0),(1,0)])

    def test_seed_scan_excludes_own_nested_plan_but_retains_sibling_and_old(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);local=root/'local/night-002/stless003'
            for path,seed in [(local/'seed-plan.json',11),
                    (root/'local/night-002/other/seed-plan.json',12),
                    (root/'data/old/seed-plan.json',13),
                    (root/'local/registry/OTHER.reserved.json',14)]:
                path.parent.mkdir(parents=True,exist_ok=True);write(path,dict(seeds=[seed]))
            public=root/'data/night-002-stless003';public.mkdir()
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
            self.assertEqual(invoke.call_args.kwargs['total_timeout'],30)

    def test_call_envelope_includes_prior_time_every_phase_and_inflight(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);directory=local/'technical/dispatch';directory.mkdir(parents=True)
            write(directory/'a.started.json',dict(job_id='a'))
            write(directory/'b.started.json',dict(job_id='b'))
            (directory/'ledger.jsonl').write_text('{"job_id":"a","status":"ok","native_elapsed_seconds":3.0}\n')
            with patch.object(runner,'LOCAL',local):
                proof=runner.call_envelope(dict(prior_native_call_seconds=100.))
                self.assertEqual(proof['recorded_native_call_seconds'],103.)
                self.assertEqual(proof['unresolved_claims'],1)
                self.assertEqual(proof['resulting_bound_seconds'],183.)
                with self.assertRaisesRegex(ValueError,'sum exhausted'):
                    runner.call_envelope(dict(prior_native_call_seconds=3550.))
            # Completion settles the40s reservation to actual3s without refunding
            # the prior100s or removing any immutable job marker.
            with (directory/'ledger.jsonl').open('a') as stream:
                stream.write('{"job_id":"b","status":"expected_rejection","native_elapsed_seconds":2.0}\n')
            with patch.object(runner,'LOCAL',local):
                self.assertEqual(runner.call_envelope(dict(prior_native_call_seconds=100.))['resulting_bound_seconds'],145.)

    def test_unknown_or_oversized_completed_call_prevents_new_claim(self):
        for change in ({'native_elapsed_seconds':None},{'native_elapsed_seconds':41.},{'status':'failed'}):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as temp:
                local=Path(temp);directory=local/'main/dispatch';directory.mkdir(parents=True)
                write(directory/'a.started.json',dict(job_id='a'))
                row=dict(job_id='a',status='ok',native_elapsed_seconds=3.);row.update(change)
                import json
                (directory/'ledger.jsonl').write_text(json.dumps(row)+'\n')
                with patch.object(runner,'LOCAL',local),self.assertRaises(ValueError):
                    runner.call_envelope(dict(prior_native_call_seconds=100.))

    def test_public_budget_has_no_tokens_or_private_unknown_fields(self):
        result=runner.safe_budget(dict(charged_seconds=2.,active=dict(token='secret',owner_pid=10,
            name='technical',kind='technical',keys=['allowed','private-id'],elapsed_seconds=None),
            operations=[],halted=False,private_path='private'),{'allowed'})
        self.assertEqual(result['active']['keys'],['allowed'])
        self.assertIsNone(result['active']['elapsed_seconds'])
        self.assertNotIn('secret',str(result));self.assertNotIn('private-id',str(result))


if __name__=='__main__':unittest.main()

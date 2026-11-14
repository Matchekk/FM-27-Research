"""Offline only: thread dispatch, readback selection and admission policy mocks."""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
import json
from pathlib import Path
import tempfile
import runpy
import stat
import sys
from threading import Barrier,Event
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch

from analysis import run_sharpness002 as runner
from analysis import sharpness002_runner as helper
from research.native import read,rows,write
from research.startpolicy import encode_records
from tests.test_passive_observer import fixture


def binary():
    return encode_records([(11,s,i,0,i) for s in (0,1) for i in range(11)])


def jobs(seed=7):
    return [dict(key=f'high_press-{seed}-{side}-{arm}',scenario='high_press',seed=seed,side=side,arm=arm)
            for side in (0,1) for arm in helper.ARMS]


class SharpnessColdTests(unittest.TestCase):
    def test_exact_eight_job_seed_blocks_and_technical_negative(self):
        main=jobs()+jobs(9)
        self.assertEqual([len(b) for b in helper.block_jobs(main)],[8,8])
        technical=[dict(j,side=0,key=j['key']+'-r'+str(i//4),repeat=i//4) for i,j in enumerate(jobs())]
        negative=dict(key='negative-malformed',kind='negative',seed=None)
        self.assertEqual([len(b) for b in helper.block_jobs(technical+[negative],technical=True)],[8,1])
        with self.assertRaises(ValueError):helper.block_jobs(main[:-1])
        with self.assertRaises(ValueError):helper.block_jobs(technical,technical=True)

    def test_four_claim_counter_is_exercised_without_processes(self):
        barrier=Barrier(4,timeout=2)
        with tempfile.TemporaryDirectory() as temp:
            def invoke(job,on_start):
                on_start();barrier.wait()
                return dict(job_id=job['key'],status='ok')
            scheduler=helper.ColdScheduler(Path(temp)/'dispatch',invoke,lambda j:None)
            result=scheduler.run(helper.block_jobs(jobs()))
            self.assertEqual(len(result),8);self.assertEqual(scheduler.peak,4)
            state=read(Path(temp)/'dispatch/dispatch-summary.json')
            self.assertEqual(state['peak_inflight_claims'],4)
            self.assertFalse(state['engine_pid_peak_measured'])
            self.assertEqual(state['active_claims'],0)

    def test_first_error_prevents_all_claims_after_stop_and_all_later_blocks(self):
        barrier=Barrier(4,timeout=2);released=Event();first=jobs();later=jobs(9)
        with tempfile.TemporaryDirectory() as temp:
            def invoke(job,on_start):
                on_start();barrier.wait()
                if job['key']==first[0]['key']:
                    released.set();raise ValueError('synthetic input mismatch')
                released.wait(2)
                return dict(job_id=job['key'],status='ok')
            scheduler=helper.ColdScheduler(Path(temp)/'dispatch',invoke,lambda j:None)
            with self.assertRaises(ValueError):scheduler.run([first,later])
            events=rows(Path(temp)/'dispatch/concurrency.jsonl')
            stop=next(i for i,r in enumerate(events) if r['event']=='stop')
            self.assertFalse(any(r['event']=='claimed' for r in events[stop+1:]))
            self.assertFalse(set(j['key'] for j in later)&scheduler.started)
            state=read(Path(temp)/'dispatch/dispatch-summary.json')
            self.assertTrue(state['stop']);self.assertLessEqual(state['peak_inflight_claims'],4)
            self.assertEqual(state['planned'],16)

    def test_admission_error_never_calls_invoker_and_retains_unbegun(self):
        with tempfile.TemporaryDirectory() as temp:
            invoke=Mock();scheduler=helper.ColdScheduler(Path(temp)/'dispatch',invoke,Mock(side_effect=ValueError('closed')))
            with self.assertRaises(ValueError):scheduler.run([jobs()])
            invoke.assert_not_called()
            self.assertEqual(read(Path(temp)/'dispatch/dispatch-summary.json')['claimed'],0)

    def test_raw_control_hash_and_fifteen_descriptive_fields(self):
        _,trace=fixture()
        for row in trace:
            if row.get('event')=='native_passive_state':
                for p in row['players']:
                    p['condition_accumulator_raw']=1000000
                    if p['statistics_cache_region_hex'] is not None:
                        raw=bytearray(16);raw[9]=100;raw[10]=70;p['statistics_cache_region_hex']=raw.hex()
                    if row['stage']=='finished':p['effectiveness_region_hex']='00'*33
        values,missing=helper.descriptive(trace,binary(),0)
        self.assertEqual(len(values),15);self.assertEqual(missing,{})
        self.assertEqual(values['prepared_condition_cache89_mean'],100.)
        self.assertEqual(values['first_sharpness_cache8a_mean'],70.)
        self.assertEqual(values['finished_tf33_distinct_hashes'],1)
        changed=deepcopy(trace);changed[5]['players'][1]['effectiveness_region_hex']='ff'*33
        self.assertNotEqual(helper.initial_controls(trace),helper.initial_controls(changed))

    def test_missing_finished_cache_has_reason_and_never_zero(self):
        _,trace=fixture();finished=next(r for r in trace if r.get('stage')=='finished')
        # General observer validator forbids missing first11 cache, so exercise a
        # valid absolute starting slot outside first11 using an own synthetic map.
        base=encode_records([(11,s,i,0,(i+3)%23) for s in (0,1) for i in range(11)])
        values,missing=helper.descriptive(trace,base,0)
        self.assertIsNone(values['finished_condition_cache89_mean'])
        self.assertIn('finished_condition_cache89_mean',missing)

    def test_main_requires_six_hundred_seconds_in_both_budgets_and_utc(self):
        now=datetime(2026,11,14,20,tzinfo=timezone.utc)
        inner=dict(experiment=helper.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,
            wall_limit_seconds=3600,halted=False,charged_seconds=100.,active=None,
            wall_deadline_utc=(now+timedelta(seconds=1800)).isoformat())
        night=dict(charged_seconds=100.,active=dict(name=helper.EXPERIMENT+'/main',
            start_utc=now.isoformat(),child_deadline_utc=(now+timedelta(seconds=1000)).isoformat()))
        self.assertGreaterEqual(runner.main_remaining(inner,night,now),600)
        for source in ('own_charge','own_wall','outer_deadline','outer_charge'):
            a,b=deepcopy(inner),deepcopy(night)
            if source=='own_charge':a['charged_seconds']=301.
            elif source=='own_wall':a['wall_deadline_utc']=(now+timedelta(seconds=599)).isoformat()
            elif source=='outer_deadline':b['active']['child_deadline_utc']=(now+timedelta(seconds=599)).isoformat()
            else:b['charged_seconds']=1201.
            with self.subTest(source=source),self.assertRaises(ValueError):runner.main_remaining(a,b,now)

    def test_per_job_unknown_cleanup_retains_own_marker_and_limit_three(self):
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

    def test_phase_budget_requires_exact_caps_keys_timing_and_parent_receipt(self):
        keys=[f'tech-{i}' for i in range(33)]
        op=dict(name='technical',kind='technical',keys=keys,elapsed_seconds=10.,returncode=0,timed_out=False,
            start_utc='2026-11-14T20:00:01+00:00',child_deadline_utc='2026-11-14T20:14:56+00:00')
        state=dict(experiment=helper.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,
            wall_limit_seconds=3600,halted=False,active=None,operations=[op],charged_seconds=10.,
            reserved={k:'technical' for k in keys},wall_start_utc='2026-11-14T20:00:00+00:00',
            wall_deadline_utc='2026-11-14T21:00:00+00:00')
        proof=dict(experiment_id=helper.EXPERIMENT,phase='technical',budget_sha256='a'*64,
            completed_utc='2026-11-14T20:00:12+00:00')
        self.assertTrue(runner.phase_budget_gate('technical',state,proof,'a'*64,dict(technical=keys)))
        for key,value in (('halted',True),('operations',[]),('charged_seconds',0),('active',{})):
            changed=deepcopy(state);changed[key]=value
            self.assertFalse(runner.phase_budget_gate('technical',changed,proof,'a'*64,dict(technical=keys)))
        self.assertFalse(runner.phase_budget_gate('technical',state,dict(proof,completed_utc='2026-11-14T21:00:01+00:00'),
                                                  'a'*64,dict(technical=keys)))
        shortened=deepcopy(state);shortened['operations'][0]['child_deadline_utc']='2026-11-14T20:00:06+00:00'
        self.assertFalse(runner.phase_budget_gate('technical',shortened,proof,'a'*64,dict(technical=keys)))

    def test_postsummary_parent_failure_never_exports_main_performance(self):
        from research.native import digest
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);local=root/'private';public=root/'public';public.mkdir()
            directory=local/'main/dispatch';directory.mkdir(parents=True)
            plan=[dict(key=f'main-{i}',seed=i+1) for i in range(512)]
            write(public/'main-job-plan.json',plan)
            write(public/'technical-job-plan.json',[dict(key=f'tech-{i}') for i in range(33)])
            (directory/'ledger.jsonl').write_text(''.join(json.dumps(dict(job_id=j['key'],status='ok'))+'\n' for j in plan))
            write(directory/'dispatch-summary.json',dict(planned=512))
            (directory/'concurrency.jsonl').write_text('{}\n')
            write(local/'main-summary.json',dict(passed=True,
                dispatch_summary_sha256=digest(directory/'dispatch-summary.json'),
                concurrency_ledger_sha256=digest(directory/'concurrency.jsonl')))
            write(local/'budget.json',dict(halted=True,active=None,charged_seconds=12.,
                operations=[dict(name='main',kind='main',keys=['D:/private/hidden'],elapsed_seconds=12.,
                    returncode=1,timed_out=False,token_sha256='PRIVATE-TOKEN',stdout='D:/private/log')]))
            with patch.object(runner,'LOCAL',local),patch.object(runner,'PUBLIC',public),patch.object(runner.subprocess,'Popen') as process:
                runner.export('main')
            process.assert_not_called()
            self.assertFalse(read(public/'main-summary.json')['passed'])
            self.assertFalse(read(public/'main-summary.json')['scientific_analysis_allowed'])
            self.assertFalse((public/'main.jsonl').exists())
            budget=read(public/'main-budget.json')
            self.assertIsNone(budget['charged_seconds']);self.assertEqual(budget['recorded_charged_seconds'],12.)
            self.assertNotIn('PRIVATE-TOKEN',json.dumps(budget));self.assertNotIn('D:/private',json.dumps(budget))

    def test_unconfirmed_cleanup_retains_global_lease_in_supervisor(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);public=root/'public';public.mkdir();local=root/'private';local.mkdir()
            pending=local/'technical/jobs/probe/pending.json';pending.parent.mkdir(parents=True);pending.write_text('{}')
            write(public/'technical-job-plan.json',[dict(key='probe')])
            budget=Mock();budget.path=local/'budget.json';budget.load.return_value=dict(active=None,halted=True)
            budget.run.side_effect=ValueError('child failed')
            lease=Mock(spec=runner.NativeLease);lease.acquire.return_value=lease
            lease.assert_owned.return_value=dict(schema=1,experiment=helper.EXPERIMENT,workers=4,owner_pid=1,acquired_utc='test')
            with patch.object(runner,'LOCAL',local),patch.object(runner,'PUBLIC',public), \
                 patch.object(runner,'publication_gate',return_value={}),patch.object(runner,'DeadlineBudget',return_value=budget), \
                 patch.object(runner,'NativeLease',return_value=lease):
                with self.assertRaises(ValueError):runner.supervise('technical','a'*40,1)
            lease.release.assert_not_called()
            self.assertTrue(read(local/'budget.json')['global_native_lease_retained'])

    def test_missing_real_tech17_release_blocks_before_codec_or_reservations(self):
        release=dict(experiment_id='MECH-002-STARTPOLICY-TECH-V1',passed=False)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with patch.object(runner,'PUBLIC',root/'public'),patch.object(runner,'LOCAL',root/'private'), \
                 patch.object(runner,'read',return_value=release),patch.object(runner,'design') as factory, \
                 patch.object(runner,'seed_plan') as seeds,patch.object(runner.subprocess,'Popen') as process:
                with self.assertRaises(ValueError):runner.prepare()
            factory.assert_not_called();seeds.assert_not_called();process.assert_not_called()
            self.assertFalse((root/'private').exists())

    def test_fresh_absent_cache_preserves_old_cache_and_checks_namespace_absence(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);old=root/'analysis/__pycache__/old.pyc';old.parent.mkdir(parents=True);old.write_bytes(b'own-old-cache')
            with patch.object(sys,'pycache_prefix',None),patch.object(sys,'dont_write_bytecode',False):
                prefix=runner.fresh_source_cache(root)
                self.assertEqual(sys.pycache_prefix,prefix);self.assertTrue(sys.dont_write_bytecode)
                self.assertFalse(Path(prefix).exists());self.assertEqual(old.read_bytes(),b'own-old-cache')
                (root/'analysis/__init__.pyc').write_bytes(b'own-namespace-shadow')
                with self.assertRaises(RuntimeError):runner.fresh_source_cache(root)
        self.assertIn('research/__init__.py',runner.CODE)

    def test_direct_entry_rejects_preloaded_project_modules(self):
        # runpy executes the direct source entry in this already-loaded test process.
        # No child process, game import or command dispatch can occur.
        with self.assertRaisesRegex(RuntimeError,'preloaded project modules'):
            runpy.run_path(str(Path(runner.__file__)),run_name='__main__')

    def test_first_main_rechecks_after_allowance_and_refreshes_waiting_calls(self):
        gate=helper.FirstMainCall();events=[]
        check=Mock(side_effect=lambda:events.append('600-check') or 650.)
        allowance=Mock(side_effect=lambda:events.append('fresh-allowance') or 700.)
        def operation(limit):events.append(('call',limit));return limit
        self.assertEqual(gate.invoke(operation,check,allowance),650.)
        self.assertEqual(events,['fresh-allowance','600-check',('call',650.)])
        allowance.side_effect=lambda:events.append('fresh-after-wait') or 590.
        self.assertEqual(gate.invoke(operation,check,allowance),590.)
        self.assertEqual(check.call_count,1);self.assertEqual(allowance.call_count,2)
        self.assertEqual(events[-2:],['fresh-after-wait',('call',590.)])

    def test_delayed_first_main_below600_makes_no_containment_attempt(self):
        from research.native import digest
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp);write(local/'private-host.json',dict(observer_host='never-executed.exe'))
            binary=local/'inputs/high_press-0-S70-P0.bin';binary.parent.mkdir();binary.write_bytes(b'own-test-input')
            job=dict(key='main-own-fixture',scenario='high_press',side=0,arm='S70-P0',seed=7,setup_sha256=digest(binary))
            with patch.object(runner,'LOCAL',local),patch.object(runner,'admission',return_value=850), \
                 patch.object(runner,'main_remaining',return_value=599), \
                 patch.object(runner,'read',return_value=dict(observer_host='never-executed.exe')), \
                 patch('research.native_process005.contained_call') as invoke:
                with self.assertRaises(ValueError):runner.native_job(job,'main',[job['key']],
                    dict(identity=dict(engine_sha256='a'*64)),lambda:None,helper.FirstMainCall())
            invoke.assert_not_called()
            self.assertFalse((local/'main/jobs/main-own-fixture/pending.json').exists())

    def test_artifact_snapshot_stats_once_skips_only_removed_files(self):
        regular=Mock();regular.stat.return_value=SimpleNamespace(st_mode=stat.S_IFREG,st_size=17)
        removed=Mock();removed.stat.side_effect=FileNotFoundError('own removed pending marker')
        directory=Mock();directory.stat.return_value=SimpleNamespace(st_mode=stat.S_IFDIR,st_size=4096)
        with patch.object(Path,'rglob',return_value=iter([regular,removed,directory])):
            self.assertEqual(runner.artifact_bytes(Path('own-fixture')),17)
        regular.stat.assert_called_once();removed.stat.assert_called_once();directory.stat.assert_called_once()
        denied=Mock();denied.stat.side_effect=PermissionError('own IO failure')
        with patch.object(Path,'rglob',return_value=iter([denied])):
            with self.assertRaises(PermissionError):runner.artifact_bytes(Path('own-fixture'))


if __name__=='__main__':unittest.main()

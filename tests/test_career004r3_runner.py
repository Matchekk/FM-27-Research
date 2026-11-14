"""Synthetic faults and harmless Python kernel children; never reads a game save."""
from contextlib import ExitStack,redirect_stderr,redirect_stdout
from datetime import datetime,timezone
from io import BytesIO,StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock,patch
import warnings

from analysis import run_career004r3 as m
from research.career_diag004r3 import TARGET_MESSAGE


def policy(memory=m.MEMORY):
    return dict(limit_flags=m.FLAGS,active_process_limit=1,process_memory_limit=memory,job_memory_limit=memory,
                peak_process_private_bytes=4096,peak_job_private_bytes=4096,kill_on_close=True,breakaway_allowed=False)


def proof(memory=m.MEMORY,clean=True):
    return dict(job_policy=policy(memory),cleanup_confirmed=clean,capsule_exit_confirmed=True,
                final_policy_verified=True,kernel_active_processes=0 if clean else None)


def release():
    return dict(experiment_id=m.EXPERIMENT,passed=True,director_proceed='published proceed',published_commit='a'*40,
                ci_run=1,review_document=m.REVIEW,review_sha256='b'*64,reviewed_contract_sha256='c'*64)


def write(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value))


class ReaderCheckError(Exception):pass
class UnknownBuildWarning(Warning):pass


def selection(section,block_start,block_end,layout):
    cursor=block_start+2
    raise ReaderCheckError('PRIVATE_NAME: '+TARGET_MESSAGE)


class FixedDateTime(datetime):
    @classmethod
    def now(cls,tz=None):return datetime(2026,11,14,20,tzinfo=timezone.utc)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);(self.root/'.git').mkdir()
        self.stack=ExitStack();self.addCleanup(self.stack.close);self.addCleanup(self.tmp.cleanup)
        self.stack.enter_context(patch.object(m,'ROOT',self.root))
        self.stack.enter_context(patch.object(m,'PUBLIC',self.root/'public'))

    def fake_run(self,*,gate_error=None,assign_error=None,clean=True):
        c=dict(code_sha256_lf={'analysis/run_career004r3.py':'c'*64})
        write(self.root/m.CONTRACT,c)
        self.stack.enter_context(patch.object(m,'verify_frozen'))
        gate=self.stack.enter_context(patch.object(m,'published_gate',return_value=release(),side_effect=gate_error))
        self.stack.enter_context(patch.object(m,'datetime',FixedDateTime))
        lease=Mock();self.stack.enter_context(patch.object(m,'NativeLease',return_value=SimpleNamespace(acquire=lambda:lease)))
        process=SimpleNamespace(stdin=Mock(),stdout=BytesIO(),pid=123,poll=Mock(return_value=0),wait=Mock(return_value=0))
        popen=self.stack.enter_context(patch.object(m.subprocess,'Popen',return_value=process))
        job=Mock(final_policy=None);job.policy.return_value=policy();job.assign.side_effect=assign_error;job.assign.return_value=policy()
        self.stack.enter_context(patch.object(m,'ReaderJob',return_value=job))
        def cleaned(*args):job.final_policy=policy();return proof(clean=clean)
        cleanup=self.stack.enter_context(patch.object(m,'_cleanup',side_effect=cleaned))
        snapshot=self.stack.enter_context(patch.object(m,'snapshot_receipt',side_effect=AssertionError('No snapshot IO in supervisor')))
        return lease,process,popen,gate,cleanup,snapshot

    def test_worktree_guard_before_hash_gate_or_process(self):
        (self.root/'.git').rmdir();(self.root/'.git').write_text('gitdir: synthetic')
        with patch.object(m,'snapshot_receipt') as snapshot,patch.object(m.subprocess,'Popen') as process,patch.object(m,'published_gate') as gate:
            with self.assertRaises(ValueError):m.run(self.root,self.root/'missing.json')
        snapshot.assert_not_called();process.assert_not_called();gate.assert_not_called()

    def test_release_failure_prevents_lease_snapshot_and_process(self):
        lease,process,popen,gate,cleanup,snapshot=self.fake_run(gate_error=ValueError('not published'))
        with self.assertRaises(ValueError):m.run(self.root,self.root/'release.json')
        popen.assert_not_called();snapshot.assert_not_called();cleanup.assert_not_called();lease.release.assert_not_called()

    def test_director_phrase_and_final_review_required_before_external_commands(self):
        write(self.root/'release.json',dict(experiment_id=m.EXPERIMENT,passed=True,director_proceed='later'))
        with patch.object(m.subprocess,'check_output') as command:
            with self.assertRaises(ValueError):m.published_gate({},self.root/'release.json')
            command.assert_not_called()

    def test_exact_published_ci_and_review_contract_binding(self):
        c=dict(code_sha256_lf={},documents_sha256_lf={},inputs_sha256_lf={})
        write(self.root/m.CONTRACT,c);contract_hash=m.normalized_hash(self.root/m.CONTRACT)
        review=self.root/m.REVIEW;review.parent.mkdir(parents=True,exist_ok=True);review.write_text('passed '+contract_hash)
        r=release();r.update(reviewed_contract_sha256=contract_hash,review_sha256=m.normalized_hash(review))
        write(self.root/'release.json',r)
        def command(args,**kwargs):
            if args[:3]==['git','remote','get-url']:return 'https://github.com/Matchekk/FM-27-Research.git\n'
            if args[0]=='gh':return json.dumps(dict(status='completed',conclusion='success',headSha='a'*40))
            if args[:2]==['git','show']:
                return json.dumps(c).encode() if args[2].endswith(':'+m.CONTRACT) else review.read_bytes()
            if args[:2]==['git','ls-remote']:return 'a'*40+'\trefs/heads/main\n'
            raise AssertionError(args)
        with patch.object(m.subprocess,'check_output',side_effect=command),patch.object(m.subprocess,'run'):
            self.assertEqual(m.published_gate(c,self.root/'release.json')['published_commit'],'a'*40)
        def wrong_ci(args,**kwargs):
            if args[0]=='gh':return json.dumps(dict(status='completed',conclusion='success',headSha='d'*40))
            return command(args,**kwargs)
        with patch.object(m.subprocess,'check_output',side_effect=wrong_ci),patch.object(m,'snapshot_receipt') as snapshot:
            with self.assertRaises(ValueError):m.published_gate(c,self.root/'release.json')
            snapshot.assert_not_called()
        write(self.root/'release.json',release())
        write(self.root/m.CONTRACT,{})
        with patch.object(m.subprocess,'check_output') as command:
            with self.assertRaises(ValueError):m.published_gate({},self.root/'release.json')
            command.assert_not_called()

    def test_assignment_failure_no_go_and_verified_cleanup_before_lease_release(self):
        lease,process,popen,gate,cleanup,snapshot=self.fake_run(assign_error=OSError('synthetic'))
        with redirect_stderr(StringIO()),redirect_stdout(StringIO()),self.assertRaises(OSError):m.run(self.root,self.root/'release.json')
        process.stdin.write.assert_not_called();cleanup.assert_called_once();lease.release.assert_called_once();snapshot.assert_not_called()
        completion=m.read(m.paths(self.root)['private']/'completion.json')
        self.assertFalse(completion['resources']['go_sent'])

    def test_cleanup_unknown_retains_lease_and_persistent_attempt(self):
        lease,process,popen,gate,cleanup,snapshot=self.fake_run(clean=False)
        with self.assertRaisesRegex(RuntimeError,'lease retained'):m.run(self.root,self.root/'release.json')
        lease.release.assert_not_called();self.assertTrue((m.paths(self.root)['private']/'attempt.json').exists())
        with self.assertRaises(ValueError):m.run(self.root,self.root/'release.json')
        self.assertEqual(popen.call_count,1);snapshot.assert_not_called()

    def test_no_save_hash_in_supervisor_and_total_artifact_counter_includes_completion(self):
        lease,process,popen,gate,cleanup,snapshot=self.fake_run()
        with redirect_stderr(StringIO()),redirect_stdout(StringIO()):self.assertEqual(m.run(self.root,self.root/'release.json'),20)
        snapshot.assert_not_called();lease.release.assert_called_once()
        private=m.paths(self.root)['private'];r=m.read(private/'completion.json')['resources']
        self.assertEqual(r['private_artifact_bytes'],sum(x.stat().st_size for x in private.iterdir()))
        self.assertEqual(popen.call_args.args[0][:3],[sys._base_executable,'-I','-S'])

    def test_monotonic_deadline_cleans_and_cannot_reopen_budget(self):
        lease,process,popen,gate,cleanup,snapshot=self.fake_run()
        process.poll.side_effect=[None,None,254]
        with patch.object(m.time,'monotonic',side_effect=[0,176,176]),redirect_stdout(StringIO()):
            self.assertEqual(m.run(self.root,self.root/'release.json'),20)
        resources=m.read(m.paths(self.root)['private']/'completion.json')['resources']
        self.assertEqual(resources['status'],'timeout');cleanup.assert_called_once();lease.release.assert_called_once()
        with self.assertRaises(ValueError):m.run(self.root,self.root/'release.json')
        self.assertEqual(popen.call_count,1);snapshot.assert_not_called()

    def test_output_and_metadata_bounds_before_disk_growth(self):
        folder=self.root/'bounded';folder.mkdir()
        out=m.BoundedOutput(BytesIO(b'x'*(m.BUDGET['stdout_bytes']+4096)),folder/'stdout.txt');out.start()
        self.assertTrue(out.finish());self.assertTrue(out.exceeded)
        self.assertEqual((folder/'stdout.txt').stat().st_size,m.BUDGET['stdout_bytes'])
        store=m.PrivateStore(folder,'child')
        with self.assertRaises(ValueError):store.write('warnings.json',{'private_message':'x'*(300*1024)})
        self.assertFalse((folder/'warnings.json').exists())

    def test_oversize_warning_is_explicit_failure_not_silently_truncated(self):
        state=dict(count=0,items=[],truncated=False)
        with self.assertRaises(RuntimeError):
            with m.capture_warnings(state):warnings.warn('x'*4096,UnknownBuildWarning)
        self.assertTrue(state['truncated']);self.assertTrue(state['items'][0]['truncated'])
        self.assertEqual(state['count'],1)

    def test_local_reader_proof_strict_policy_does_not_relax_native_helper(self):
        self.assertTrue(m.confirmed_reader_cleanup(proof()))
        for change in (dict(kernel_active_processes=False),dict(final_policy_verified=False),dict(capsule_exit_confirmed=False)):
            bad=proof();bad.update(change);self.assertFalse(m.confirmed_reader_cleanup(bad))
        for key,value in (('limit_flags',0x2008),('active_process_limit',3),('process_memory_limit',m.MEMORY+1),('breakaway_allowed',True)):
            bad=proof();bad['job_policy'][key]=value;self.assertFalse(m.confirmed_reader_cleanup(bad))

    def test_export_missing_and_invalid_never_restart_or_read_save(self):
        private=m.paths(self.root)['private'];private.mkdir(parents=True)
        (private/'attempt.json').write_text('{partial')
        (private/'events.jsonl').write_text(json.dumps(dict(stage=m.STAGES[2],status='started'))+'\n{bad\n')
        write(private/'completion.json',{'resources':{'elapsed_seconds':'PRIVATE_PATH'}})
        with patch.object(m,'snapshot_receipt') as snapshot,patch.object(m.subprocess,'Popen') as process:
            r=m.export(self.root)
        snapshot.assert_not_called();process.assert_not_called();self.assertIsNone(r['resources'])
        self.assertEqual(r['stages'][2]['status'],'started_unresolved');self.assertEqual(r['invalid_event_lines'],1)
        self.assertNotIn('PRIVATE_PATH',json.dumps(r));self.assertIsNone(r['reader_open_calls'])
        self.assertFalse(r['tactics_released']);self.assertIsNone(r['snapshot_stable'])

    def child_fixture(self):
        p=m.paths(self.root);p['private'].mkdir(parents=True)
        write(self.root/m.CONTRACT,{})
        contract_hash=m.normalized_hash(self.root/m.CONTRACT);r=release();r['reviewed_contract_sha256']=contract_hash
        write(p['private']/'attempt.json',dict(experiment_id=m.EXPERIMENT,supervisor_pid=os.getppid(),
                                             contract_sha256_lf=contract_hash,release=r))
        write(p['private']/'launch.json',dict(decoder_pid=os.getpid(),membership_verified_before_go=True))
        write(self.root/'local/global-readers/native-execution.lease.json',dict(owner_pid=os.getppid(),experiment=m.EXPERIMENT))
        self.stack.enter_context(patch.dict(os.environ,{'FM27_R3_ADMITTED':'1'}))
        self.stack.enter_context(patch.object(sys,'dont_write_bytecode',True))
        verify=self.stack.enter_context(patch.object(m,'verify_frozen'))
        save=SimpleNamespace(info=SimpleNamespace(game='FM27',build='27.0.1+2503222',section_schemas={'tactics_man':26}),close=Mock())
        save.tactics=Mock(side_effect=lambda:selection(b'..XYZ..',0,7,SimpleNamespace(taker_markers=(b'abc',b'def',b'ghi'))))
        def opened(path,strict):warnings.warn('PRIVATE_NAME',UnknownBuildWarning);return save
        module=SimpleNamespace(__version__='0.12.4',open=Mock(side_effect=opened))
        self.stack.enter_context(patch.object(m,'_load_official',return_value=(module,selection)))
        snapshot=self.stack.enter_context(patch.object(m,'snapshot_receipt',return_value=dict(sha256=m.SNAPSHOT_SHA,bytes=m.SNAPSHOT_BYTES)))
        return p,save,module,snapshot,verify

    def test_one_strict_open_one_tactics_original_error_close_and_posthash(self):
        p,save,module,snapshot,verify=self.child_fixture()
        with redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),20)
        module.open.assert_called_once_with(p['snapshot'],strict=True);save.tactics.assert_called_once();save.close.assert_called_once()
        self.assertEqual(snapshot.call_count,2)
        self.assertEqual(m.read(p['private']/'marker.json')['status'],'captured_final_target_failure')
        self.assertEqual(m.read(p['private']/'warnings.json')['count'],1)
        stages,_=m._events(p['private']/'events.jsonl')
        self.assertEqual(stages[3]['error_type'],'ReaderCheckError');self.assertEqual(stages[4]['status'],'observed')

    def test_source_gate_failure_never_touches_snapshot_or_save(self):
        p,save,module,snapshot,verify=self.child_fixture();verify.side_effect=ValueError('source drift')
        with redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),22)
        snapshot.assert_not_called();module.open.assert_not_called();save.tactics.assert_not_called()

    def test_initial_snapshot_drift_no_second_hash_or_save(self):
        p,save,module,snapshot,verify=self.child_fixture();snapshot.return_value=dict(sha256='0'*64,bytes=m.SNAPSHOT_BYTES)
        with redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),22)
        snapshot.assert_called_once();module.open.assert_not_called()
        self.assertFalse((p['private']/'snapshot-after.json').exists())

    def test_posthash_drift_retained_without_replacement_or_extra_reader(self):
        p,save,module,snapshot,verify=self.child_fixture()
        snapshot.side_effect=[dict(sha256=m.SNAPSHOT_SHA,bytes=m.SNAPSHOT_BYTES),dict(sha256='0'*64,bytes=m.SNAPSHOT_BYTES)]
        with redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),22)
        self.assertEqual(snapshot.call_count,2);module.open.assert_called_once();save.close.assert_called_once()
        self.assertEqual(m.read(p['private']/'snapshot-after.json')['sha256'],'0'*64)
        stages,_=m._events(p['private']/'events.jsonl');self.assertEqual(stages[4]['status'],'failed')

    def test_complete_synthetic_capture_requires_all_gates_and_keeps_failures(self):
        p,save,module,snapshot,verify=self.child_fixture()
        m.PrivateStore(p['private'],'parent').event(m.STAGES[0],'observed')
        with redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),20)
        resources=dict(status='child_failed',elapsed_seconds=1.0,within_wall_limit=True,wall_limit_seconds=180,
            reader_processes_started=1,child_returncode=20,retries=0,private_artifact_bytes=4096,stdout_bytes=100,
            go_sent=True,stdout_truncated=False,cleanup=proof())
        write(p['private']/'completion.json',dict(resources=resources))
        result=m.export(self.root)
        self.assertEqual(result['diagnostic_status'],'captured_expected_marker_failure')
        self.assertEqual(result['stages'][3]['status'],'failed');self.assertFalse(result['tactics_released'])
        self.assertNotIn('PRIVATE_NAME',json.dumps(result))
        (p['private']/'snapshot-after.json').unlink()
        self.assertEqual(m.export(self.root)['diagnostic_status'],'not_captured_or_not_technically_valid')

    def test_close_failure_and_ledger_io_failure_still_attempt_posthash(self):
        p,save,module,snapshot,verify=self.child_fixture();save.close.side_effect=OSError('synthetic close')
        original=m.PrivateStore.event
        def fail_start(store,stage,status,**details):
            if stage==m.STAGES[4] and status=='started':raise OSError('synthetic ledger')
            return original(store,stage,status,**details)
        with patch.object(m.PrivateStore,'event',fail_start),redirect_stderr(StringIO()):self.assertEqual(m.child(self.root),23)
        save.close.assert_called_once();self.assertEqual(snapshot.call_count,2)
        self.assertEqual(m.read(p['private']/'close.json')['status'],'failed')

    def test_public_marker_omits_absolute_offsets_and_all_private_strings(self):
        receipt=dict(status='captured_final_target_failure',section_bytes=100,block_start=10,block_end=90,cursor=20,
            cursor_relative_to_block=10,bytes_remaining_in_block=70,raw_values_captured=False,scan_performed=False,
            grammar_changed=False,failure_consistent_with_expected_marker_tests=True,private='PRIVATE_NAME',
            marker_checks=[dict(marker_index=0,expected_width_bytes=3,fully_inside_block=True,equals_expected_at_cursor=False)])
        result=m.public_marker(receipt)
        self.assertNotIn('block_start',result);self.assertNotIn('cursor',result);self.assertNotIn('PRIVATE_NAME',str(result))
        self.assertEqual(result['cursor_decile_in_block'],1);self.assertEqual(result['remaining_bytes_power2_upper'],128)
        receipt['marker_checks'][0]['equals_expected_at_cursor']=True
        with self.assertRaises(ValueError):m.public_marker(receipt)


@unittest.skipUnless(os.name=='nt','Windows harmless kernel tests')
class KernelReaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
    def launch(self,code,environment=None):
        p=subprocess.Popen([sys._base_executable,'-I','-S','-B','-c',code],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,env=environment)
        self.addCleanup(self.finish,p);return p
    def finish(self,p):
        if p.poll() is None:p.kill()
        p.wait(timeout=3)
        if p.stdout:p.stdout.close()
        if p.stdin and not p.stdin.closed:p.stdin.close()
    def clean(self,job,p,policy):
        result=m._cleanup(job,p,True,policy);result.update(job_policy=job.final_policy,final_policy_verified=job.final_policy is not None)
        self.assertTrue(m.confirmed_reader_cleanup(result,64*1024**2),result)
    def test_hard_memory_and_kernel_zero_before_close(self):
        p=self.launch("import sys;sys.stdin.readline();\ntry:\n a=bytearray(128*1024**2);print('BAD')\nexcept MemoryError:print('LIMITED')")
        job=m.ReaderJob(64*1024**2);policy=job.assign(p)
        try:
            p.stdin.write(b'go\n');p.stdin.close();p.wait(timeout=3)
            self.assertEqual(p.returncode,0);self.assertIn(b'LIMITED',p.stdout.read())
        finally:self.clean(job,p,policy)
    def test_early_bootstrap_no_script_read_before_go(self):
        script=self.root/'safe.py';marker=self.root/'admitted.txt'
        script.write_text(f'from pathlib import Path\nPath({str(marker)!r}).write_text("safe")\n')
        token='harmless-fixture';env={**os.environ,'FM27_R3_TOKEN_SHA256':m.sha256(token.encode()).hexdigest()}
        p=self.launch(m.BOOTSTRAP,env);self.assertFalse(marker.exists())
        job=m.ReaderJob(64*1024**2);policy=job.assign(p)
        try:
            packet=dict(token=token,script=str(script),central=str(self.root),site=str(self.root),runner_sha256=m.normalized_hash(script))
            p.stdin.write((json.dumps(packet)+'\n').encode());p.stdin.close();p.wait(timeout=3)
            self.assertEqual(p.returncode,0,p.stdout.read());self.assertTrue(marker.exists())
        finally:self.clean(job,p,policy)
    def test_one_process_limit_refuses_descendant(self):
        code=("import sys,subprocess;sys.stdin.readline();\ntry:\n subprocess.Popen([sys.executable,'-I','-S','-c','print(1)']);print('BAD')\nexcept OSError:print('REFUSED')")
        p=self.launch(code);job=m.ReaderJob(64*1024**2);policy=job.assign(p)
        try:
            p.stdin.write(b'go\n');p.stdin.close();p.wait(timeout=3)
            self.assertEqual(p.returncode,0);self.assertIn(b'REFUSED',p.stdout.read())
        finally:self.clean(job,p,policy)
    def test_kill_on_close_is_not_substituted_for_kernel_zero_proof(self):
        p=self.launch("import sys,time;sys.stdin.readline();print('READY',flush=True);time.sleep(30);print('BAD')")
        job=m.ReaderJob(64*1024**2);job.assign(p)
        p.stdin.write(b'go\n');p.stdin.close();self.assertEqual(p.stdout.readline().strip(),b'READY')
        job.close();p.wait(timeout=3);self.assertNotIn(b'BAD',p.stdout.read())
        self.assertFalse(m.confirmed_reader_cleanup(dict(job_policy=job.final_policy,capsule_exit_confirmed=True)))


if __name__=='__main__':unittest.main()

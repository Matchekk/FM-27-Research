"""Independent gate regressions. Only mocks and harmless temporary Python code."""
from contextlib import contextmanager,redirect_stdout,redirect_stderr
from datetime import datetime,timezone
from io import StringIO
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from analysis import run_career004r3 as m


@contextmanager
def synthetic_parent():
    from tests.test_career004r3_runner import RunnerTests
    case=RunnerTests();case.setUp()
    try:yield case
    finally:case.doCleanups()


class IndependentRunnerGates(unittest.TestCase):
    def test_expired_monotonic_window_after_assignment_never_sends_go(self):
        with synthetic_parent() as case:
            lease,process,popen,gate,cleanup,snapshot=case.fake_run()
            clock={'now':0.0};assigned=[]
            original=m.ReaderJob().assign
            def assign(p):
                assigned.append(True);clock['now']=176.0
                return original(p)
            with patch.object(m.ReaderJob(),'assign',side_effect=assign), \
                 patch.object(m.time,'monotonic',side_effect=lambda:clock['now']), \
                 redirect_stdout(StringIO()),redirect_stderr(StringIO()):
                try:m.run(case.root,case.root/'release.json')
                except Exception:pass
            self.assertEqual(assigned,[True]);self.assertEqual(popen.call_count,1)
            self.assertEqual(process.stdin.write.call_count,0,'No GO may be sent after the child window expired')
            cleanup.assert_called_once();lease.release.assert_called_once();snapshot.assert_not_called()

    def test_expired_absolute_deadline_after_assignment_never_sends_go(self):
        with synthetic_parent() as case:
            lease,process,popen,gate,cleanup,snapshot=case.fake_run()
            class Clock(datetime):
                current=datetime(2026,11,14,20,tzinfo=timezone.utc)
                @classmethod
                def now(cls,tz=None):return cls.current
            assigned=[];original=m.ReaderJob().assign
            def assign(p):
                assigned.append(True);Clock.current=datetime(2026,11,14,23,0,1,tzinfo=timezone.utc)
                return original(p)
            with patch.object(m.ReaderJob(),'assign',side_effect=assign), \
                 patch.object(m,'datetime',Clock),patch.object(m.time,'monotonic',return_value=0.0), \
                 redirect_stdout(StringIO()),redirect_stderr(StringIO()):
                try:m.run(case.root,case.root/'release.json')
                except Exception:pass
            self.assertEqual(assigned,[True]);self.assertEqual(popen.call_count,1)
            self.assertEqual(process.stdin.write.call_count,0,'No GO may be sent after the absolute deadline')
            cleanup.assert_called_once();lease.release.assert_called_once();snapshot.assert_not_called()

    def test_non_json_release_is_rejected_without_file_content_read(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with patch.object(m,'ROOT',root),patch.object(m,'read',return_value={}) as reader:
                with self.assertRaises(ValueError):m.published_gate({},root/'snapshot.fm')
            reader.assert_not_called()

    def test_oversize_release_is_rejected_before_json_content_read(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=root/m.RELEASE_METADATA['directory']/'release.json'
            release.parent.mkdir(parents=True);release.write_bytes(b' '*(64*1024+1))
            with patch.object(m,'ROOT',root),patch.object(m,'read',return_value={}) as reader:
                with self.assertRaises(ValueError):m.published_gate({},release)
            reader.assert_not_called()

    def test_malformed_nested_marker_keeps_exported_failure_and_all_stages(self):
        from tests.test_career004r3_runner import proof
        with synthetic_parent() as case:
            private,save,module,snapshot,verify=case.child_fixture()
            folder=private['private'];m.PrivateStore(folder,'parent').event(m.STAGES[0],'observed')
            with redirect_stderr(StringIO()):self.assertEqual(m.child(case.root),20)
            resources=dict(status='child_failed',elapsed_seconds=1.,within_wall_limit=True,wall_limit_seconds=180,
                reader_processes_started=1,child_returncode=20,retries=0,private_artifact_bytes=4096,
                stdout_bytes=100,go_sent=True,stdout_truncated=False,cleanup=proof())
            (folder/'completion.json').write_text(json.dumps(dict(resources=resources)))
            self.assertEqual(m.export(case.root)['diagnostic_status'],'captured_expected_marker_failure')
            marker=m.read(folder/'marker.json');marker['marker_checks']=[None]
            (folder/'marker.json').write_text(json.dumps(marker))
            count=snapshot.call_count
            with patch.object(m.subprocess,'Popen') as process:report=m.export(case.root)
            process.assert_not_called();self.assertEqual(snapshot.call_count,count)
            self.assertEqual(report['diagnostic_status'],'not_captured_or_not_technically_valid')
            self.assertEqual(len(report['stages']),5)
            self.assertIn(dict(receipt='marker.json',status='invalid_retained'),report['receipt_issues'])
            self.assertEqual(report['stages'][3]['status'],'failed')


@unittest.skipUnless(os.name=='nt','Windows harmless one-process job')
class IndependentBootstrapCache(unittest.TestCase):
    def test_bootstrap_executes_frozen_source_instead_of_existing_pyc(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);site=root/'site';site.mkdir();(root/'analysis').mkdir()
            (root/'local/night-001-career/readonly-r3').mkdir(parents=True)
            module=site/'frozen_example.py';original=b'value="ORIGINAL"\n';cached=b'value="CACHED!!"\n'
            self.assertEqual(len(original),len(cached))
            module.write_bytes(original);stamp=module.stat().st_mtime
            module.write_bytes(cached);os.utime(module,(stamp,stamp))
            # The adversarial cache is confined to this temporary module; do not
            # create the runner's deliberately absent global import-cache prefix.
            with patch.object(sys,'pycache_prefix',None):py_compile.compile(str(module),doraise=True)
            module.write_bytes(original);os.utime(module,(stamp,stamp))
            script=root/'analysis/run_career004r3.py'
            script.write_text('import frozen_example,sys\nprint(frozen_example.value,sys.dont_write_bytecode)\n')
            token='harmless-independent-fixture'
            env={**os.environ,'FM27_R3_TOKEN_SHA256':m.sha256(token.encode()).hexdigest()}
            process=subprocess.Popen([sys._base_executable,'-I','-S','-B','-c',m.BOOTSTRAP],
                stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,
                creationflags=subprocess.CREATE_NO_WINDOW)
            job=m.ReaderJob(64*1024**2);policy=None;assigned=False
            try:
                policy=job.assign(process);assigned=True
                packet=dict(token=token,script=str(script),central=str(root),site=str(site),runner_sha256=m.normalized_hash(script))
                process.stdin.write((json.dumps(packet)+'\n').encode());process.stdin.close()
                process.wait(timeout=4);output=process.stdout.read()
                self.assertEqual(process.returncode,0,output)
                self.assertEqual(output.strip(),b'ORIGINAL True')
                self.assertEqual(module.read_bytes(),original)
            finally:
                proof=m._cleanup(job,process,assigned,policy)
                proof.update(job_policy=job.final_policy,final_policy_verified=job.final_policy is not None)
                if process.stdout:process.stdout.close()
                self.assertTrue(m.confirmed_reader_cleanup(proof,64*1024**2),proof)


if __name__=='__main__':unittest.main()

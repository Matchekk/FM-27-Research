"""Independent boundary regressions; own temporary Python data, never FM."""
from datetime import datetime, timedelta, timezone
import importlib._bootstrap_external
import importlib.util
from hashlib import sha256
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from analysis import run_sharpness002 as runner

ROOT = Path(__file__).resolve().parents[1]


class SharpnessIndependentRunnerTests(unittest.TestCase):
    def test_immediate_first_main_gate_does_not_start_below600_or_repeat_on_later_calls(self):
        from analysis.sharpness002_runner import FirstMainCall
        gate = FirstMainCall(); operation = Mock(return_value=(0,.1))
        with self.assertRaises(ValueError): gate.invoke(operation,lambda:599.99,lambda:900.)
        operation.assert_not_called()
        check = Mock(return_value=605.)
        self.assertEqual(gate.invoke(operation,check,lambda:900.),(0,.1))
        self.assertEqual(gate.invoke(operation,Mock(side_effect=AssertionError('600s gate repeated after first call')),lambda:590.),(0,.1))
        check.assert_called_once(); self.assertEqual(operation.call_count,2)
        self.assertEqual([c.args for c in operation.call_args_list],[(605.,),(590.,)])
        self.assertEqual(gate.evidence['remaining_seconds'],605.)

    def test_actual_operation_over_child_deadline_is_not_reconciled_success(self):
        keys = [f'technical-{i}' for i in range(33)]
        state = dict(experiment=runner.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,
            wall_limit_seconds=3600,halted=False,active=None,charged_seconds=10.,reserved={k:'technical' for k in keys},
            wall_start_utc='2026-11-14T20:00:00+00:00',wall_deadline_utc='2026-11-14T21:00:00+00:00',
            operations=[dict(name='technical',kind='technical',keys=keys,elapsed_seconds=10.,returncode=0,timed_out=False,
                start_utc='2026-11-14T20:00:01+00:00',child_deadline_utc='2026-11-14T20:00:06+00:00')])
        proof = dict(experiment_id=runner.EXPERIMENT,phase='technical',budget_sha256='a'*64,
                     completed_utc='2026-11-14T20:00:20+00:00')
        self.assertFalse(runner.phase_budget_gate('technical',state,proof,'a'*64,dict(technical=keys)))

    def test_direct_entry_uses_source_despite_timestamp_valid_poisoned_helper_pyc(self):
        with tempfile.TemporaryDirectory(prefix='fm27-sharpness-cache-review-') as temporary:
            base = Path(temporary).resolve()
            self.assertTrue(base.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            (base/'.git').mkdir()
            # Copy only this project's source so imported observer helpers keep
            # their ROOT inside the same owned fixture; no upstream code/data.
            for directory in ('analysis','research'):
                (base/directory).mkdir()
                for source in (ROOT/directory).glob('*.py'):
                    shutil.copyfile(source,base/directory/source.name)
            helper = base/'analysis/sharpness002_runner.py'
            original = helper.read_bytes(); metadata = helper.stat()
            # Source bytes stay exact. Only an owned timestamp-valid cache differs.
            with patch.object(sys,'pycache_prefix',None):
                cache = Path(importlib.util.cache_from_source(str(helper)))
            cache.parent.mkdir()
            code = compile('raise RuntimeError("OWN_TEMP_HELPER_CACHE_EXECUTED")\n',str(helper),'exec')
            cache.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(
                code,int(metadata.st_mtime),metadata.st_size))
            env = dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1')
            completed = subprocess.run([sys.executable,'-B',str(base/'analysis/run_sharpness002.py'),'--help'],
                cwd=base,env=env,capture_output=True,text=True,timeout=15,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            self.assertEqual(helper.read_bytes(),original)
            self.assertEqual(completed.returncode,0,completed.stderr)
            self.assertNotIn('OWN_TEMP_HELPER_CACHE_EXECUTED',completed.stderr)

    def test_concurrent_pending_removal_does_not_break_artifact_admission(self):
        when = datetime(2026,11,14,20,tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory(prefix='fm27-sharpness-count-review-') as temporary:
            base = Path(temporary).resolve(); removed = base/'technical/jobs/earlier/pending.json'
            token = 'OWN_TEST_ONLY'
            state = dict(limits={'technical':33,'main':512},limit_seconds=900,wall_limit_seconds=3600,halted=False,
                wall_deadline_utc=(when+timedelta(seconds=1800)).isoformat(),
                active=dict(name='technical',kind='technical',keys=['new-job'],supervisor_pid=1,
                    token_sha256=sha256(token.encode()).hexdigest(),child_deadline_utc=(when+timedelta(seconds=800)).isoformat()))
            lease = dict(owner_pid=1,experiment=runner.EXPERIMENT,workers=4)
            original = Path.is_file
            # The directory snapshot/file predicate saw an earlier worker's file;
            # by the subsequent stat it has completed cleanup and unlinked it.
            def file_before_unlink(path): return path == removed or original(path)
            with patch.object(runner,'LOCAL',base), patch.object(runner,'read',side_effect=[state,lease]), \
                 patch.object(runner,'assert_night_admission'), patch.object(runner,'supervisor_alive',return_value=True), \
                 patch.dict(os.environ,{'TACT_P0_SUPERVISOR_TOKEN':token}), \
                 patch.object(runner.shutil,'disk_usage',return_value=SimpleNamespace(free=30*1024**3)), \
                 patch.object(runner,'datetime',wraps=datetime) as clock, \
                 patch.object(Path,'rglob',return_value=iter([removed])), patch.object(Path,'is_file',file_before_unlink):
                clock.now.return_value = when
                self.assertGreater(runner.admission('technical',['new-job']),0)

    def test_new_master_uses_source_despite_old_research_init_cache(self):
        master_root = Path(os.environ.get('FM_RESEARCH_MASTER_SOURCE_ROOT',ROOT)).resolve()
        with tempfile.TemporaryDirectory(prefix='fm27-master-cache-review-') as temporary:
            base = Path(temporary).resolve()
            self.assertTrue(base.is_relative_to(Path(tempfile.gettempdir()).resolve()))
            for directory in ('analysis','research'):
                (base/directory).mkdir()
                for source in (ROOT/directory).glob('*.py'):
                    shutil.copyfile(source,base/directory/source.name)
            shutil.copyfile(master_root/'analysis/night_supervise.py',base/'analysis/night_supervise.py')
            source = base/'research/__init__.py'; original = source.read_bytes(); metadata = source.stat()
            with patch.object(sys,'pycache_prefix',None):
                cache = Path(importlib.util.cache_from_source(str(source)))
            cache.parent.mkdir()
            code = compile('raise RuntimeError("OWN_TEMP_MASTER_CACHE_EXECUTED")\n',str(source),'exec')
            cache.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(code,int(metadata.st_mtime),metadata.st_size))
            completed = subprocess.run([sys.executable,'-B',str(base/'analysis/night_supervise.py'),'--help'],cwd=base,
                env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=15,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            self.assertEqual(completed.returncode,0,completed.stderr)
            self.assertNotIn('OWN_TEMP_MASTER_CACHE_EXECUTED',completed.stderr)
            self.assertEqual(source.read_bytes(),original)
            (base/'analysis/__init__.py').write_text('raise RuntimeError("OWN_TEMP_NAMESPACE_INIT_EXECUTED")\n')
            blocked = subprocess.run([sys.executable,'-B',str(base/'analysis/night_supervise.py'),'--help'],cwd=base,
                env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True,timeout=15,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            self.assertNotEqual(blocked.returncode,0)
            self.assertNotIn('OWN_TEMP_NAMESPACE_INIT_EXECUTED',blocked.stderr)


if __name__ == '__main__':
    unittest.main()

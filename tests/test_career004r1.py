from copy import deepcopy
from pathlib import Path
import os
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from analysis import audit_career004r1 as runner
from research.career_reader004r1 import (EXPECTED_SNAPSHOT,HardReaderJob,MEMORY_BYTES,
    PROFILE_V10,PROBES,compare_reports,coverage,layout_claim,ledger,load_profile,public_checks)


class ReaderProfileTests(unittest.TestCase):
    def test_passive_fallback_wrapper_returns_same_object_and_counts(self):
        value=object();draft=SimpleNamespace(read_summary=lambda container:value)
        version=SimpleNamespace(read_summary_facts=None)
        def install():version.read_summary_facts=lambda container:draft.read_summary(container)
        compat=SimpleNamespace(PROFILE=PROFILE_V10,install=install)
        module=SimpleNamespace(__version__='synthetic')
        modules={'desktop_save_draft':draft,'desktop_save_compat':compat,
                 'fmsave':module,'fmsave._version':version}
        with patch('research.career_reader004r1.importlib.import_module',side_effect=lambda name:modules[name]),patch.object(sys,'path',list(sys.path)):
            _,trace=load_profile('R1','synthetic-source','synthetic-site')
            self.assertIs(version.read_summary_facts(object()),value)
        self.assertEqual(trace,dict(summary_calls=1,draft_fallback_calls=1,draft_fallback_accepted=1,draft_fallback_exceptions=0))

    def test_structural_checks_preserve_advisory_failure_and_missing_denominator(self):
        gates=(SimpleNamespace(name='coverage_share',observed=None,minimum=.5,maximum=1.,passed=True,applied=False,advisory=True),
               SimpleNamespace(name='population_count',observed=2,minimum=5,maximum=None,passed=False,applied=True,advisory=True))
        result=public_checks(SimpleNamespace(reader='players',record_count=2,gates=gates,anomalies={'unresolved':1}))
        self.assertIsNone(result['gates'][0]['observed'])
        self.assertFalse(result['gates'][1]['passed']);self.assertTrue(result['gates'][1]['advisory'])
        self.assertFalse(result['native_semantics_verified'])

    def test_borrowed_layout_claim_keeps_actual_source_build_and_schema(self):
        value=SimpleNamespace(region='game_db',build='27.0.0+2486695',schema=4000,save_schema=4001)
        result=layout_claim(SimpleNamespace(_reader_layout=lambda _:value),'players')
        self.assertEqual(result['source_build'],'27.0.0+2486695')
        self.assertEqual((result['source_schema'],result['save_schema']),(4000,4001))

    def test_typed_injury_scope_requires_current_cohort_not_null_club(self):
        rows=[SimpleNamespace(kind=SimpleNamespace(name='HISTORY'),club_uid=5,player_uid=12),
              SimpleNamespace(kind=SimpleNamespace(name='TYPED'),club_uid=None,player_uid=12),
              SimpleNamespace(kind=SimpleNamespace(name='TYPED'),club_uid=None,player_uid=99)]
        r=coverage('injuries',rows,dict(managed_uid=5,managed_players={12}),None)
        self.assertEqual(r['historical_managed_club_records'],1)
        self.assertEqual(r['typed_current_cohort_records'],1)
        r=coverage('injuries',rows,{},None)
        self.assertIsNone(r['historical_managed_club_records']);self.assertIsNone(r['typed_current_cohort_records'])

    def test_unresolved_failure_warning_and_missing_are_all_preserved(self):
        events=[dict(probe='open',status='observed_with_warnings',coverage={'save_build':'27.0.1+2503222'},
                     warning_types=['UnknownBuildWarning'],warning_count=1,private_warnings=['PRIVATE_NAME']),
                dict(probe='managed_clubs',status='started')]
        r=ledger(events,'R2',{'status':'abandoned'},None)
        self.assertEqual(len(r['probes']),12)
        self.assertEqual(r['probes'][1]['status'],'started_unresolved')
        self.assertEqual(r['probes'][2]['status'],'not_started')
        self.assertNotIn('PRIVATE_NAME',str(r))
        for k in ('native_released','career_advance_released','replay_released','native_semantics_verified'):
            self.assertIs(r[k],False)

    def test_worktree_run_guard_prevents_save_hash_or_process(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'.git').write_text('gitdir: synthetic')
            with patch.object(runner,'ROOT',root),patch.object(runner,'digest') as hashed,patch.object(runner.subprocess,'Popen') as process:
                with self.assertRaises(ValueError):runner.run('R1',root,root/'no-release.json')
                hashed.assert_not_called();process.assert_not_called()

    def test_no_real_release_without_full_sha_and_successful_exact_ci(self):
        with tempfile.TemporaryDirectory() as temp:
            release=Path(temp)/'release.json'
            runner.write(release,dict(passed=True,profile='R1',published_commit='short',ci_run=1))
            with self.assertRaises(ValueError):runner.verify_release({'profile':'R1'},release)

    def test_other_central_root_rejected_before_release_or_snapshot_access(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'.git').mkdir()
            with patch.object(runner,'ROOT',root),patch.object(runner,'verify_frozen') as frozen, \
                 patch.object(runner,'digest') as hashed,patch.object(runner.subprocess,'Popen') as process:
                with self.assertRaises(ValueError):runner.run('R1',root/'elsewhere',root/'unused.json')
                frozen.assert_not_called();hashed.assert_not_called();process.assert_not_called()

    def test_crossreader_missing_is_not_agreement_or_independent_replicate(self):
        def report(profile):return dict(snapshot_sha256=EXPECTED_SNAPSHOT,snapshot_stable=True,profile=profile,
            probes=[dict(probe=p,status='not_started') for p in PROBES])
        r=compare_reports(report('R1'),report('R2'),{}, {})
        self.assertTrue(all(x['status']=='not_comparable_unavailable' for x in r['fields']))
        self.assertIsNone(r['independent_treatment_replicates_verified'])
        self.assertFalse(r['native_semantics_verified'])
        changed=report('R2');changed['snapshot_stable']=False
        with self.assertRaises(ValueError):compare_reports(report('R1'),changed,{}, {})

    def test_abandoned_export_never_opens_save_or_restarts_child(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);private=root/'local/night-001-career/readonly-r1'
            runner.write(private/'attempt.json',dict(release={'profile':'R1'},status='started'))
            runner.append(private/'events.jsonl',dict(probe='open',status='started'))
            with patch.object(runner,'PUBLIC',root/'public'),patch.object(runner,'digest') as hashed,patch.object(runner.subprocess,'Popen') as process:
                r=runner.export_status('R1',root)
                hashed.assert_not_called();process.assert_not_called()
            self.assertEqual(r['probes'][0]['status'],'started_unresolved')
            self.assertEqual(r['resources']['status'],'abandoned_or_unreconciled')


@unittest.skipUnless(os.name=='nt','Windows kernel job tests')
class WindowsHardJobTests(unittest.TestCase):
    def start(self,code):
        # Avoid Windows venv's redirector: only one OS reader process may enter the job.
        return subprocess.Popen([sys._base_executable,'-c',code],stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)

    def finish(self,p):
        if p.poll() is None:p.kill()
        p.wait(timeout=3)
        if p.stdout:p.stdout.close()
        if p.stdin and not p.stdin.closed:p.stdin.close()

    def test_kernel_memory_rejection_before_large_allocation(self):
        p=self.start("import sys;sys.stdin.readline();\ntry:\n a=bytearray(128*1024**2);print('BAD')\nexcept MemoryError:print('LIMITED')")
        self.addCleanup(self.finish,p)
        with HardReaderJob(64*1024**2) as job:
            proof=job.assign(p);self.assertEqual(proof['active_process_limit'],1)
            p.stdin.write(b'go\n');p.stdin.close();p.wait(timeout=5)
            self.assertEqual(p.returncode,0);self.assertIn(b'LIMITED',p.stdout.read())
            self.assertLessEqual(job.info()['peak_job_private_bytes'],64*1024**2)

    def test_kernel_kill_on_close_terminates_waiting_child(self):
        p=self.start("import sys,time;sys.stdin.readline();print('STARTED',flush=True);time.sleep(30);print('NATURAL_END')")
        self.addCleanup(self.finish,p)
        job=HardReaderJob();job.assign(p)
        p.stdin.write(b'go\n');p.stdin.close()
        self.assertEqual(p.stdout.readline().strip(),b'STARTED')
        job.close();p.wait(timeout=3)
        self.assertNotIn(b'NATURAL_END',p.stdout.read())


if __name__=='__main__':unittest.main()

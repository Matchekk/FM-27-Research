"""Copied public evidence only; no saves, upstream checkout or native execution."""
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from analysis.review_night001 import ROOT, audit_startpolicy_public


class StartpolicyPublicReviewTests(unittest.TestCase):
    def setUp(self):
        # A reviewer worktree can point explicitly at the director's public files.
        # Published CI uses its own repository data without an override.
        source = Path(os.environ.get('FM_RESEARCH_PUBLIC_TEST_ROOT', ROOT)).resolve()
        self.temp = tempfile.TemporaryDirectory(prefix='fm27-public-review-')
        self.root = Path(self.temp.name).resolve()
        self.assertTrue(self.root.is_relative_to(Path(tempfile.gettempdir()).resolve()))
        self.addCleanup(self.temp.cleanup)
        self.data = self.root/'data/mech-002-startpolicy-tech'; self.data.mkdir(parents=True)
        for name in ('inputs.json','seed-plan.json','job-plan.json','review-gate.json','registration.json',
                     'technical-summary.json','budget.json','measurements.jsonl','job-accounting.jsonl'):
            shutil.copyfile(source/'data/mech-002-startpolicy-tech'/name, self.data/name)
        # Read existing immutable Git objects; do not copy an upstream repository.
        gitdir = subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=source,text=True).strip()
        (self.root/'.git').write_text('gitdir: '+gitdir+'\n',encoding='utf8')

    def rows(self):
        return [json.loads(line) for line in (self.data/'measurements.jsonl').read_text().splitlines()]

    def put_rows(self, rows):
        (self.data/'measurements.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in rows),encoding='utf8')

    def test_actual_public_copy_passes_without_current_router_or_private_reads(self):
        current = self.root/'analysis/night_supervise.py'; current.parent.mkdir()
        current.write_text('raise RuntimeError("future current router must not be imported")\n')
        (self.root/'local').mkdir()
        before = {p.name:sha256(p.read_bytes()).hexdigest() for p in self.data.iterdir()}
        original = Path.open
        def public_only(path, *args, **kwargs):
            resolved = path.resolve()
            if resolved.is_relative_to(self.root):
                self.assertNotEqual(resolved.relative_to(self.root).parts[0], 'local')
            return original(path,*args,**kwargs)
        with patch.object(Path,'open',public_only):
            result = audit_startpolicy_public(self.root)
        self.assertTrue(result['public_startpolicy_verified'])
        self.assertEqual((result['full_matches'],result['aa_pairs'],result['initial_control_pairs']), (16,8,8))
        self.assertFalse(result['private_actor_logs_reconstructed_by_this_portable_check'])
        self.assertEqual(result['native_starts'],0)
        self.assertEqual(before,{p.name:sha256(p.read_bytes()).hexdigest() for p in self.data.iterdir()})

    def test_wrong_initial_cache_cannot_be_hidden_by_true_summary(self):
        values = self.rows(); values[0]['startpolicy_audit']['captures'][0]['target_cache8a'] = 69
        self.put_rows(values)
        with self.assertRaisesRegex(ValueError,'target/cache transfer'):
            audit_startpolicy_public(self.root)

    def test_actual_aa_score_mismatch_is_rejected(self):
        values = self.rows(); values[1]['result']['score'][0] += 1
        self.put_rows(values)
        with self.assertRaisesRegex(ValueError,'A/A outcomes/hash'):
            audit_startpolicy_public(self.root)

    def test_actual_seed_drift_is_rejected(self):
        values = self.rows(); values[0]['seed'] += 1
        self.put_rows(values)
        with self.assertRaisesRegex(ValueError,'job provenance/status'):
            audit_startpolicy_public(self.root)

    def test_budget_overrun_rejected_despite_success_flags(self):
        path = self.data/'budget.json'; value = json.loads(path.read_text())
        value['charged_seconds'] = value['recorded_charged_seconds'] = value['operations'][0]['elapsed_seconds'] = 180.1
        path.write_text(json.dumps(value),encoding='utf8')
        with self.assertRaisesRegex(ValueError,'actual time/accounting'):
            audit_startpolicy_public(self.root)

    def test_initial_control_failure_rejected_despite_true_summary(self):
        values = self.rows(); values[2]['controls']['initial_control_fields_and_raw_tf33_equal'] = False
        self.put_rows(values)
        with self.assertRaisesRegex(ValueError,'initial control proof'):
            audit_startpolicy_public(self.root)


if __name__ == '__main__':
    unittest.main()

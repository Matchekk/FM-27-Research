"""Offline metadata regressions; never validate or execute the external studies."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from analysis.audit_night_evidence import audit

ROOT = Path(__file__).resolve().parents[1]


class EvidenceAuditTests(unittest.TestCase):
    def setUp(self):
        directory = ROOT / 'data/night-001-evidence'
        self.registry = json.loads((directory / 'sources.json').read_text(encoding='utf8'))
        self.receipts = json.loads((directory / 'access-checks.json').read_text(encoding='utf8'))

    def test_actual_metadata_has_ten_sources_but_no_replications(self):
        result = audit(self.registry, self.receipts)
        self.assertEqual(result['sources'], 10)
        self.assertEqual(result['independent_replications_verified'], 0)
        self.assertFalse(result['scientific_claims_verified_by_this_schema_check'])
        self.assertEqual(len(result['unreachable_legacy_urls']), 2)

    def test_page_read_cannot_be_promoted_to_replication_or_native_audit(self):
        for key in ('locally_independently_reproduced', 'native_readbacks_audited', 'analysis_executed'):
            registry = deepcopy(self.registry)
            registry['sources'][0][key] = True
            with self.assertRaises(ValueError):
                audit(registry, self.receipts)
        for value in (False, 0.0, None, 1):
            registry = deepcopy(self.registry)
            registry['native_matches_started'] = value
            with self.assertRaises(ValueError):
                audit(registry, self.receipts)

    def test_placeholder_pld_cannot_become_real_sample_and_unknown_is_not_zero(self):
        for sample in (600, 0, True):
            registry = deepcopy(self.registry)
            registry['sources'][2]['author_reported_matches'] = sample
            with self.assertRaises(ValueError):
                audit(registry, self.receipts)

    def test_unreachable_source_or_hash_mismatch_is_not_verified_access(self):
        for status in (404, None):
            receipts = deepcopy(self.receipts)
            receipts['checks'][0]['status'] = status
            with self.assertRaises(ValueError):
                audit(self.registry, receipts)
        registry = deepcopy(self.registry)
        registry['sources'][0]['transport_body_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            audit(registry, self.receipts)

    def test_duplicate_source_and_mutable_github_revision_rejected(self):
        registry = deepcopy(self.registry)
        registry['sources'][1]['url'] = registry['sources'][0]['url']
        with self.assertRaises(ValueError):
            audit(registry, self.receipts)
        registry = deepcopy(self.registry)
        registry['sources'][7]['immutable_revision'] = 'main'
        with self.assertRaises(ValueError):
            audit(registry, self.receipts)

    def test_excessive_source_paraphrase_is_rejected(self):
        registry = deepcopy(self.registry)
        registry['sources'][0]['summary'] = 'word ' * 201
        with self.assertRaises(ValueError):
            audit(registry, self.receipts)


if __name__ == '__main__':
    unittest.main()

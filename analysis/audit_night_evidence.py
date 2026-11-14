"""Structural audit of NIGHT-001 sources, not verification of external claims.

Reads only our public metadata. No HTTP requests, native/runtime imports, save
files, seeds or registry writes. HTTP200 and a body hash never grant evidence.
"""
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ROLES = {'manufacturer_description', 'site_availability_snapshot',
         'secondary_author_guidance', 'external_exploratory_report'}
PARAPHRASE_FIELDS = ('title', 'summary', 'critical_assessment', 'research_action',
                    'uncertainty', 'author_reported_build', 'platform',
                    'public_code_inspection', 'retrieval_note')


def need(value, message):
    if not value:
        raise ValueError(message)


def http_url(value):
    url = urlsplit(value)
    need(url.scheme == 'https' and bool(url.netloc) and not url.username and not url.password,
         'Public HTTPS source URL required')


def positive_or_missing(value):
    need(value is None or type(value) is int and value > 0, 'Count must be positive or null')


def audit(registry, transport):
    need(registry['schema_version'] == transport['schema'] == 1, 'Schema version')
    need(registry['audit_id'] == 'NIGHT-001-EVIDENCE', 'Audit ID')
    need(all(type(registry[k]) is int and registry[k] == 0
             for k in ('native_matches_started', 'seeds_reserved', 'career_advances')),
         'This metadata audit cannot claim experiment execution')
    sources = registry['sources']
    need(6 <= len(sources) <= 10 and registry['source_count'] == len(sources), 'Source count')
    need(len({s['id'] for s in sources}) == len(sources), 'Duplicate source ID')
    need(len({s['url'] for s in sources}) == len(sources), 'Duplicate source URL')
    receipts = transport['checks']
    need(len({r['url'] for r in receipts}) == len(receipts), 'Duplicate HTTP receipt')
    by_url = {r['url']: r for r in receipts}
    words = {}
    for source in sources:
        http_url(source['url'])
        need(source['source_role'] in ROLES and source['source_family'], 'Source role/family')
        accessed = datetime.fromisoformat(source['accessed_utc'])
        need(accessed.utcoffset() == timedelta(0), 'UTC access timestamp required')
        need(source['locally_independently_reproduced'] is False and
             source['native_readbacks_audited'] is False and
             source['analysis_executed'] is False and
             type(source['raw_match_rows_audited']) is int and source['raw_match_rows_audited'] == 0,
             'Reading a page must not become a local scientific replication')
        for key in ('author_reported_matches', 'author_reported_configurations', 'author_reported_seeds'):
            positive_or_missing(source[key])
        segments = source['author_reported_match_segments']
        need(segments is None or isinstance(segments, list) and segments and
             all(type(n) is int and n > 0 for n in segments), 'Author segment counts')
        if source['source_role'] != 'external_exploratory_report':
            need(source['author_reported_matches'] is None and segments is None,
                 'Guidance/product/placeholder page is not a match sample')
        else:
            need(source['author_reported_matches'] is not None or segments is not None,
                 'Reported experiment needs clearly labelled reported counts')
        if source['immutable_revision'] is not None:
            need(re.fullmatch(r'[0-9a-f]{40}', source['immutable_revision']) is not None and
                 source['immutable_revision'] in source['url'], 'Pinned revision missing from URL')
        for key in ('author_engine_sha256', 'author_host_sha256'):
            need(source[key] is None or re.fullmatch(r'[0-9a-f]{64}', source[key]) is not None,
                 'Unknown hashes remain null')
        receipt = by_url.get(source['url'])
        need(receipt is not None and receipt['status'] == 200 and receipt['body_complete'] is True,
             'Inspected source needs its successful bounded access receipt')
        need(receipt['body_sha256'] == source['transport_body_sha256'] and
             re.fullmatch(r'[0-9a-f]{64}', source['transport_body_sha256']) is not None,
             'Transport hash mismatch')
        need(receipt['content_archived'] is False, 'No whole copyrighted article archive')
        words[source['id']] = sum(len(str(source.get(k) or '').split()) for k in PARAPHRASE_FIELDS)
        need(words[source['id']] <= 150, 'Reserve room below 200-word source budget for report references')
    return {'metadata_audit_passed': True, 'sources': len(sources),
            'source_roles': dict(Counter(s['source_role'] for s in sources)),
            'provenance_labels': len({s['source_family'] for s in sources}),
            'independent_replications_verified': 0,
            'unreachable_legacy_urls': [r['url'] for r in receipts if r['status'] == 404],
            'registry_paraphrase_words': words,
            'scientific_claims_verified_by_this_schema_check': False}


def main():
    directory = ROOT / 'data/night-001-evidence'
    registry = json.loads((directory / 'sources.json').read_text(encoding='utf8'))
    transport = json.loads((directory / 'access-checks.json').read_text(encoding='utf8'))
    print(json.dumps(audit(registry, transport), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

"""Independent NIGHT-001 dossier/provenance checks. Never starts a native host.

Private optional checks read only source/build/ledger metadata. They never open
or decode a .fm file, import a runtime server, reserve seeds or grant a release.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.passive_observer import file_hash, instrument_source


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def normalized_hash(path):
    return sha256(Path(path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def audit_public(root=ROOT):
    root = Path(root)
    observer = read(root/'data/night-001-observer/contract-draft.json')
    build = read(root/'data/night-001-observer/build-report.json')
    flow = read(root/'data/night-001-observer/static-dataflow.json')
    career = read(root/'data/night-001-career/coverage.json')
    blocker = read(root/'data/night-001-career/blocker.json')
    provenance = read(root/'data/night-001-career/run-provenance.json')
    sources = read(root/'data/night-001-evidence/sources.json')
    accesses = read(root/'data/night-001-evidence/access-checks.json')
    need(observer['full_match_plan'] == 16 and observer['native_cli_attempt_cap'] == 20 and
         observer['total_match_attempt_cap'] == 18 and observer['extra_loader_checks_cap'] == 2,
         'Observer attempt arithmetic drift')
    need(observer['seeds']['new_required'] == observer['seeds']['paired_input_cells'] == 4 and
         observer['seeds']['negative_only'] == 0, 'Technical seed units drift')
    need(observer['budget']['child_seconds'] == 180 and
         observer['budget']['fixed_UTC_window_seconds'] == 900 and
         observer['budget']['workers_selected'] == 1 and
         observer['budget']['no_progress_seconds'] == 90 and
         observer['budget']['retries'] == observer['budget']['replacement_seeds'] == 0,
         'Observer inner contract drift')
    need(build['observer_host_sha256'] == observer['required_identity']['observer_host_sha256'] and
         build['engine_sha256'] == flow['engine_sha256'] == observer['required_identity']['engine_sha256'],
         'Public build identities disagree')
    # Git may materialise CRLF in a reviewer worktree; the compiler consumed LF.
    need(build['observer_header_sha256'] == normalized_hash(root/'adapters/passive_observer_v1.h'),
         'Compiled/public observer header mismatch')
    need(build['native_starts'] == 0 and build['native_release_granted'] is False,
         'Build receipt cannot grant native release')
    probes = career['probes']
    need(len(probes) == 12 and probes[0] == dict(probe='open', status='failed', error_type='UnsupportedGameError') and
         all(p['status'] == 'not_started' for p in probes[1:]), 'R0 missing/failed slots changed')
    need(blocker['classification'] == 'exact_build_admission_failure_not_proof_of_changed_schema_grammar' and
         blocker['same_summary_schema_already_registered_for_older_build'] is True and
         blocker['error_claims']['build'] == '27.0.1+2503222' and blocker['error_claims']['schema'] == 31,
         'Reader admission failure overinterpreted')
    need(blocker['evidence_private_events_sha256'] == provenance['private_events_sha256'],
         'Reader failure receipt binding drift')
    for name, wanted in provenance['source_sha256'].items():
        need(normalized_hash(root/name) == wanted, 'Executed reader source drift')
    for flag in ('native_released', 'career_advance_released', 'replay_released',
                 'source_semantics_verified', 'ui_to_save_binding_verified',
                 'career_rng_independence_verified', 'individual_participation_verified'):
        need(career[flag] is False, 'R0 unsupported release/semantics')
    hashes = [v for k,v in career['snapshot'].items() if 'sha256' in k]
    need(len(set(hashes)) == 1 and career['snapshot']['stable_through_reader'] is True,
         'R0 snapshot stability proof drift')
    from analysis.audit_night_evidence import audit
    external = audit(sources, accesses)
    need(external['sources'] == 10 and external['independent_replications_verified'] == 0 and
         len(external['unreachable_legacy_urls']) == 2, 'Evidence accounting drift')
    return dict(public_dossier_consistent=True, external_pages=10,
                independent_external_replications_verified=0, career_probe_slots=12,
                career_failed=1, career_not_started=11, observer_full_match_plan=16,
                observer_total_probe_plan=20, observer_fresh_seed_plan=4,
                native_release_granted=False, main_release_granted=False)


def audit_private(observer_directory, career_directory, upstream):
    """Inspect only explicitly supplied own metadata/source directories."""
    observer_directory, career_directory, upstream = map(Path, (observer_directory, career_directory, upstream))
    public_build = read(ROOT/'data/night-001-observer/build-report.json')
    manifest = read(observer_directory/'build-manifest.json')
    for key in ('source_files_sha256', 'modified_host_source_sha256', 'observer_header_sha256',
                'private_compatibility_header_sha256', 'compiler_stdout_sha256', 'observer_host_sha256'):
        need(manifest[key] == public_build[key], 'Private/public build receipt mismatch')
    for name,key in [('FM27PassiveObserver.exe','observer_host_sha256'),
                     ('desktop_host.cpp','modified_host_source_sha256'),
                     ('passive_observer_v1.h','observer_header_sha256'),
                     ('engine_compat_profile.h','private_compatibility_header_sha256'),
                     ('compiler.stdout','compiler_stdout_sha256')]:
        need(file_hash(observer_directory/name) == manifest[key], 'Private build artifact mismatch')
    need(subprocess.check_output(['git','rev-parse','HEAD'],cwd=upstream,text=True).strip() == manifest['upstream_commit'],
         'Upstream revision mismatch')
    need(not subprocess.check_output(['git','status','--porcelain'],cwd=upstream,text=True).strip(), 'Upstream dirty')
    for name,wanted in manifest['source_files_sha256'].items():
        need(file_hash(upstream/'native'/name) == wanted, 'Original upstream source mismatch')
    source = (upstream/'native/desktop_host.cpp').read_bytes().decode('utf8')
    need(instrument_source(source).encode('utf8') == (observer_directory/'desktop_host.cpp').read_bytes(),
         'Compiled source has undeclared modifications')
    need(file_hash(upstream/'LICENSE') == manifest['license_sha256'], 'MIT provenance mismatch')
    flow = read(ROOT/'data/night-001-observer/static-dataflow.json')
    for name,wanted in flow['private_artifact_sha256'].items():
        need(file_hash(observer_directory.parent/'static-audit'/name) == wanted,
             'Static disassembly receipt mismatch')
    public = read(ROOT/'data/night-001-career/run-provenance.json')
    for name,key in [('events.jsonl','private_events_sha256'),('attempt.json','private_attempt_sha256')]:
        need(file_hash(career_directory/name) == public[key], 'Private career ledger mismatch')
    events = [json.loads(line) for line in (career_directory/'events.jsonl').read_text(encoding='utf8').splitlines()]
    need([(e['probe'],e['status']) for e in events] == [('open','started'),('open','failed')],
         'Unexpected R0 execution history')
    error = events[-1]['private_error']
    need('27.0.1+2503222, schema 31' in error and 'no supported layout' in error,
         'Original error does not support classification')
    # Metadata only: do not open/read/hash/decode snapshot.fm or any source save.
    need((career_directory/'snapshot.fm').stat().st_size == 147130636, 'Snapshot metadata mismatch')
    return dict(private_build_hashes_verified=True, exact_declared_source_transform_verified=True,
                upstream_clean=True, private_R0_ledger_hashes_verified=True,
                static_disassembly_hashes_verified=True,
                snapshot_size_metadata_verified=True, save_opened_or_decoded_by_reviewer=False,
                native_release_granted=False)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--observer-directory', type=Path)
    parser.add_argument('--career-directory', type=Path)
    parser.add_argument('--upstream', type=Path)
    args = parser.parse_args()
    report = audit_public()
    supplied = [args.observer_directory,args.career_directory,args.upstream]
    need(not any(supplied) or all(supplied), 'All three explicit private directories required')
    if all(supplied):
        report['private'] = audit_private(*supplied)
    print(json.dumps(report, indent=2))

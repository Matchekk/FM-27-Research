"""Prepare R3 from sources and retained JSON only. There is intentionally no run command."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.career_diag004r3 import VERSION,full_ledger,require,source_audit,source_hash
from research.career_readonly004 import write
from research.career_reader004r1 import EXPECTED_SNAPSHOT,MEMORY_BYTES,WHEEL_SHA,RELEASE_COMMIT,tree_hashes

PUBLIC=ROOT/'data/night-001-career-r3'
OWN=('research/career_diag004r3.py','analysis/prepare_career004r3.py','tests/test_career004r3.py')
DOC='experiments/VALID-004-career-readonly-R3-DIAG.md'


def read_json(path):
    require(Path(path).suffix=='.json','Only retained JSON is accepted')
    return json.loads(Path(path).read_text(encoding='utf8'))


def retained_audit(central):
    result={}
    for profile in ('R1','R2'):
        public=ROOT/f'data/night-001-career-r1/{profile}/coverage.json'
        private=Path(central)/f'local/night-001-career/readonly-{profile.lower()}'
        events_path=private/'events.jsonl';attempt_path=private/'attempt.json'
        events=[json.loads(line) for line in events_path.read_text(encoding='utf8').splitlines()]
        report=read_json(public);attempt=read_json(attempt_path)
        last={row['probe']:row for row in events}
        keys=('probe','status','coverage','checks','borrowed_layout','warning_types','warning_count','error_type')
        for row in report['probes']:
            old=last.get(row['probe'])
            expected={k:old[k] for k in keys if k in old} if old else dict(probe=row['probe'],status='not_started')
            if expected['status']=='started':expected['status']='started_unresolved'
            require(expected==row,'Retained public/private probe mismatch')
        require(report['snapshot_stable'] is True and report['snapshot_sha256']==EXPECTED_SNAPSHOT and
                attempt['snapshot_sha256_after']==EXPECTED_SNAPSHOT,'Retained stable snapshot receipt missing')
        failed=[r for r in events if r.get('status')=='failed']
        require(len(failed)==1,'Unexpected retained failure accounting')
        signature='nonempty training header entries' if profile=='R1' else "a block's set-piece marker is not where fmsave expects it"
        require(signature in failed[0]['private_error'],'Retained failure signature differs')
        training=next(r for r in report['probes'] if r['probe']=='training')
        aggregate=None
        if training['status']=='observed':
            teams=training['coverage']['teams']
            aggregate=dict(teams=len(teams),weeks=sum(x['weeks'] for x in teams),
                days=sum(x['days'] for x in teams),stored_slots=sum(sum(x['raw_session_counts'].values()) for x in teams),
                individual_attendance=None,session_coach_assignment=None,individual_focus=None,individual_intensity=None)
        result[profile]=dict(public_sha256=source_hash(public),private_events_sha256=source_hash(events_path),
            private_attempt_sha256=source_hash(attempt_path),public_private_rows_reconstructed=True,
            snapshot_receipt_stable=True,failed_probe=failed[0]['probe'],error_type=failed[0]['error_type'],
            failure_signature_matches_frozen_source=True,
            counts={s:sum(r['status']==s for r in report['probes']) for s in ('observed','observed_with_warnings','failed','not_started')},
            saved_training_aggregate=aggregate)
    return result


def prepare(central):
    central=Path(central);base=central/'local/night-001-career'
    require(not (base/'readonly-r3/attempt.json').exists(),'A real R3 attempt forbids preparation replacement')
    official=base/'reader0124/site/fmsave';runtime=central/'local/runtime-v1114.6/source'
    contracts={p:read_json(ROOT/f'data/night-001-career-r1/{p}-contract.json') for p in ('R1','R2')}
    require(contracts['R2']['reader']['wheel_sha256']==WHEEL_SHA and
            contracts['R2']['reader']['publishing_commit']==RELEASE_COMMIT,'Official wheel identity changed')
    require(tree_hashes(official)==contracts['R2']['reader']['source_sha256'],'Frozen official sources changed')
    require(tree_hashes(runtime/'vendor/fmsave')==contracts['R1']['reader']['source_sha256'],'Frozen vendor sources changed')
    require(all(source_hash(runtime/name)==value for name,value in contracts['R1']['reader']['runtime_sha256'].items()),
            'Frozen runtime sources changed')
    sources=source_audit(runtime/'vendor/fmsave',official,runtime/'desktop_save_compat.py')
    retained=retained_audit(central)
    write(PUBLIC/'source-audit.json',sources);write(PUBLIC/'retained-ledger-audit.json',retained)
    write(PUBLIC/'planned-ledger.json',full_ledger())
    config=dict(schema='valid004.r3.diagnostic-draft.v1',experiment_id='VALID-004-CAREER-R3-DIAG',version=VERSION,
        state='offline_prepared_not_executable_not_released',
        primary='bounded evidence at the final propagated official tactics marker failure; no layout repair',
        snapshot_sha256=EXPECTED_SNAPSHOT,snapshot_bytes=147130636,
        snapshot_source='already frozen R0 private copy only; not opened or hashed in this preparation',
        reader=dict(version='0.12.4',wheel_sha256=WHEEL_SHA,release_commit=RELEASE_COMMIT,
                    source_sha256=contracts['R2']['reader']['source_sha256']),
        code_sha256={name:source_hash(ROOT/name,True) for name in OWN},document=DOC,document_sha256=source_hash(ROOT/DOC,True),
        own_source_hash_normalization='CRLF_to_LF; package and private evidence hashes remain raw',
        private_field_contract={
            'section_bytes':dict(source='final target frame: len(section)',unit='bytes',native_verified=False),
            'block_start/block_end/cursor':dict(source='final target frame locals',unit='section-relative byte offsets',native_verified=False),
            'cursor_relative_to_block/bytes_remaining_in_block':dict(source='bounded offset arithmetic',unit='bytes',native_verified=False),
            'marker_index/expected_width_bytes':dict(source='unchanged layout.taker_markers at final target frame',unit='ordinal/bytes',native_verified=False),
            'fully_inside_block/equals_expected_at_cursor':dict(source='bounded range and exact original-position comparison',unit='boolean',native_verified=False)},
        budget=dict(wall_seconds=180,hard_process_private_bytes=MEMORY_BYTES,hard_job_private_bytes=MEMORY_BYTES,
                    actual_reader_processes=1,max_new_private_artifact_bytes=1024**2,retries=0,
                    native_starts=0,calendar_advances=0,seeds=0,deadline_utc='2026-11-14T23:00:00Z'),
        future_execution_gates=['separate supervisor implementation and final source freeze',
            'exact public commit with successful exact-SHA GitHub CI','independent published review',
            'explicit Director published proceed','exclusive reader lease and persistent once-only attempt marker',
            'Windows hard-job assignment before decoding, direct actual interpreter',
            'unchanged source and before/after snapshot hashes','all warnings and missing ledger retained'],
        prohibited=['marker scanning by diagnostic','marker alternatives or recovery','lenient or gate bypass',
                    'return-value substitution','R1/R2 retry','native/replay/calendar release'],
        native_semantics_verified=False,tactics_released=False,replay_released=False,
        training_effect_released=False,career_advance_released=False)
    write(PUBLIC/'R3-draft-contract.json',config)
    print(json.dumps(dict(status=config['state'],saved_training=retained['R2']['saved_training_aggregate'],
                         save_files_opened=0,reader_processes_started=0)))


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare',))
    parser.add_argument('--central',type=Path,required=True)
    args=parser.parse_args();prepare(args.central)

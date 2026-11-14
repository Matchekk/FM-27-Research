"""Independent NIGHT-001 dossier/provenance checks. Never starts a native host.

Private optional checks read only source/build/ledger metadata. They never open
or decode a .fm file, import a runtime server, reserve seeds or grant a release.
"""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import struct
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


def audit_career_runs(central, verify_private=False):
    """Reconcile completed R1/R2 receipts only. Never touches a .fm file."""
    central = Path(central)
    public = central/'data/night-001-career-r1'
    output = {}; bindings = []
    for profile in ('R1','R2'):
        report = read(public/profile/'coverage.json')
        resources = report['resources']; memory = resources['hard_memory_job']
        need(report['snapshot_stable'] is True and report['snapshot_sha256'] ==
             '1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d',
             'Unstable career snapshot receipt')
        need(resources['reader_processes_started'] == 1 and resources['retries'] == 0 and
             resources['within_wall_limit'] is True and 0 < resources['elapsed_seconds'] <= 180 and
             memory['process_memory_limit'] == memory['job_memory_limit'] == 3*1024**3 and
             memory['active_process_limit'] == 1 and memory['limit_flags'] & 0x2308 == 0x2308 and
             0 < memory['peak_job_private_bytes'] <= 3*1024**3, 'Reader resource receipts differ')
        need(len(report['probes']) == 12 and
             all(report[k] is False for k in ('native_semantics_verified','ui_to_save_binding_verified',
                 'career_rng_independence_verified','individual_participation_verified',
                 'native_released','career_advance_released','replay_released')), 'Unsupported career release')
        counts = dict(Counter(p['status'] for p in report['probes']))
        gates = [g for p in report['probes'] for c in p.get('checks',[]) for g in c['gates']]
        need(all(g['passed'] is True for g in gates), 'Unexpected failed observed reader gate')
        result = dict(statuses=counts, elapsed_seconds=resources['elapsed_seconds'],
                      peak_job_private_bytes=memory['peak_job_private_bytes'],
                      gates=len(gates), advisory_gates=sum(g['advisory'] for g in gates),
                      public_coverage_sha256=normalized_hash(public/profile/'coverage.json'),
                      public_coverage_raw_file_sha256=file_hash(public/profile/'coverage.json'))
        if verify_private:
            directory = central/f'local/night-001-career/readonly-{profile.lower()}'
            events = [json.loads(s) for s in (directory/'events.jsonl').read_text(encoding='utf8').splitlines()]
            last = {e['probe']:e for e in events}
            for probe in report['probes']:
                event = last.get(probe['probe'])
                need(probe['status'] == (event['status'] if event else 'not_started'), 'Private/public probe status drift')
                if event:
                    for key in ('coverage','checks','borrowed_layout','warning_types','warning_count','error_type'):
                        if key in probe:
                            need(probe[key] == event[key], 'Private/public coverage drift')
            attempt = read(directory/'attempt.json')
            need(attempt['resources'] == {k:v for k,v in resources.items() if k!='invalid_event_lines_retained'} and
                 attempt['snapshot_sha256_after'] == report['snapshot_sha256'], 'Private resource/snapshot receipt drift')
            expected_error = ('nonempty training header entries are not supported by this layout' if profile=='R1'
                              else "a block's set-piece marker is not where fmsave expects it")
            failures = [e for e in events if e['status']=='failed']
            need(len(failures)==1 and expected_error in failures[0]['private_error'], 'Failure classification drift')
            bindings.append(read(directory/'private-bindings.json'))
            result['private_sha256'] = {name:file_hash(directory/name) for name in
                ('events.jsonl','attempt.json','private-bindings.json','trace.json','setup.json')}
        output[profile] = result
    if verify_private:
        need(bindings[0] == bindings[1] and len(bindings[0]['team_ids']) == 4 and
             len(bindings[0]['managed_players']) == 77, 'Private identity binding/count drift')
    training = next(p for p in read(public/'R2/coverage.json')['probes'] if p['probe']=='training')['coverage']['teams']
    for team in training:
        need(team['days']==team['weeks']*7 and sum(team['raw_session_counts'].values())==team['days']*3,
             'Stored training-code accounting differs')
    output['stored_training'] = dict(records=len(training),weeks=sum(t['weeks'] for t in training),
        days=sum(t['days'] for t in training),raw_codes=sum(sum(t['raw_session_counts'].values()) for t in training),
        individual_participation_verified=False)
    cross = read(public/'cross-reader.json')
    output['cross_reader_statuses'] = dict(Counter(f['status'] for f in cross['fields']))
    output['cross_reader_sha256'] = normalized_hash(public/'cross-reader.json')
    output.update(save_opened_or_decoded=False,native_release_granted=False,career_advance_released=False)
    return output


def audit_observer_runs(central):
    """Independent direct raw-result/profile/stage reconstruction, no new host."""
    central=Path(central);public=central/'data/valid-005-observer-v1';local=central/'local/valid005-observer-v1'
    directory=local/'technical';frozen=read(public/'inputs.json');plan=read(public/'job-plan.json')
    registration=read(public/'registration.json');commit=registration['preregistration_commit']
    need(type(commit) is str and len(commit)==40 and all(c in '0123456789abcdef' for c in commit),'Full run commit missing')
    for name,wanted in frozen['code_sha256'].items():
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=central)
        need(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==wanted,'Historical frozen source blob differs')
    line_rows=lambda path:[json.loads(line) for line in path.read_text(encoding='utf8').splitlines() if line.strip()]
    ledger=line_rows(local/'ledger.jsonl');need(ledger==line_rows(public/'measurements.jsonl'),'Public/private observer ledger drift')
    need(len(ledger)==len(plan)==20 and len({r['key'] for r in ledger})==20,'Probe inventory drift')
    accounting=line_rows(public/'job-accounting.jsonl')
    need(len(accounting)==20 and all(a['key']==r['key'] and a['status']==r['status'] and a['reserved'] is True
                                  for a,r in zip(accounting,ledger,strict=True)),'Incomplete probe accounting')
    budget=read(public/'budget.json')
    need(budget['limits']=={'technical':20,'main':0} and budget['limit_seconds']==180 and
         budget['wall_limit_seconds']==900 and budget['active'] is None and budget['halted'] is False and
         budget['within_fixed_deadline'] is True and budget['cleanup_unconfirmed'] is False and
         len(budget['reserved'])==20 and [o['name'] for o in budget['operations']]==['prepare','technical'] and
         all(o['returncode']==0 and o['timed_out'] is False for o in budget['operations']) and
         abs(sum(o['elapsed_seconds'] for o in budget['operations'])-budget['charged_seconds'])<1e-8,
         'Observer cumulative budget differs')
    configs=read(local/'configs.json');groups={};states={};captures=0;profiles=0;attributes=0;artifacts={};stage_counts=[]
    from research.passive_observer import FIELDS,canonical_hash
    offsets={1:(0x79,1),9:(0xbb8,4),10:(0xbbc,4),19:(0x70,1),20:(0xca8,1),21:(0xca2,1),22:(0xca3,1)}
    offsets.update({f:(0x72+f-2,1) for f in range(2,9)})
    offsets.update({f:(a,2) for f,a in enumerate((0xc98,0xc8c,0xc96,0xc78,0xc8a,0xc90,0xc7a,0xc84),11)})
    for job,row in zip(plan,ledger,strict=True):
        need(all(row[k]==v for k,v in job.items()),'Job ledger identity drift')
        need(row['engine_sha256']==frozen['identity']['engine_sha256'] and row['host_sha256']==
             (frozen['identity']['adapter_host_sha256'] if job['mode']=='reference' else frozen['observer_host_sha256']),
             'Collector/engine row provenance differs')
        key=job['key'];proof=read(directory/(key+'.containment.json'));policy=proof['job_policy']
        need(proof['cleanup_confirmed'] is True and proof['capsule_exit_confirmed'] is True and
             type(proof['kernel_active_processes']) is int and proof['kernel_active_processes']==0 and
             policy['active_process_limit']==3 and policy['limit_flags']==0x2008 and
             policy['kill_on_close'] is True and policy['breakaway_allowed'] is False,'Unconfirmed native cleanup')
        for suffix in ('.jsonl','.input.json','.stdout','.process.json','.containment.json','.started.json'):
            path=directory/(key+suffix)
            if path.is_file():artifacts[path.name]=file_hash(path)
        if job['kind']=='image':
            need(row['status']=='ok' and row['returncode']==0,'Loader did not pass')
            evidence=line_rows(directory/(key+'.stdout'))
            need(len([e for e in evidence if e.get('event')=='native_engine_compatibility' and e['compatible'] is True])==1,
                 'Actual image compatibility missing')
            continue
        path=directory/(key+'.jsonl');need(file_hash(path)==row['raw_log_sha256'],'Native raw hash mismatch')
        evidence=line_rows(path)
        fingerprints=[e['sha256'] for e in evidence if e.get('event')=='native_image_fingerprint']
        need(fingerprints and set(fingerprints)=={frozen['identity']['engine_sha256']},'Actual native image fingerprint differs')
        def one(event):
            found=[e for e in evidence if e.get('event')==event]
            need(len(found)==1,'Missing/duplicate actual event: '+event)
            return found[0]
        if job['kind']=='negative':
            need(row['status']=='expected_rejection' and not any(e.get('event')=='natural_match_finished' for e in evidence),
                 'False negative rejection')
            expected='native_passive_observer_rejected' if job['mode']=='invalid_opt_in' else 'scenario_rejected'
            rejected=[e for e in evidence if e.get('event')==expected];need(len(rejected)==1,'Negative reason absent/ambiguous')
            need(row['returncode']==(252 if job['mode']=='invalid_opt_in' else 108),'Wrong negative exit')
            if job['mode']=='invalid_opt_in':need(rejected[0]['reason']=='invalid_opt_in','Wrong opt-in cause')
            continue
        need(row['status']=='ok' and row['returncode']==0,'Incomplete full match')
        seed=one('native_input_seed');need(seed['override'] is True and seed['effective_seed']==job['seed'],'Actual seed drift')
        need(one('native_scenario_readback_verified')['records']==5557 and
             one('native_scenario_readback_verified')['after_original_preparation'] is True,'Incomplete native input readback')
        natural=one('natural_match_finished');statistics=one('native_match_statistics')
        need(natural['full_match_completed'] is True and 0<natural['tick']<47996 and
             statistics['source']=='original_team_statistics','Natural/original endpoint missing')
        result=dict(seed=job['seed'],score=natural['score'],tick=natural['tick'],clock=natural['clock'],
            team_statistics=[{k:t[k] for k in ('xg','shots','shots_on_target','passes','completed_passes','possession','possession_ticks')}
                             for t in statistics['teams']])
        need(result==row['result'],'Published endpoint reconstruction differs')
        group=(job['context'],job['side']);groups.setdefault(group,[]).append(result)
        dump=read(directory/(key+'.input.json'));need(file_hash(directory/(key+'.input.json'))==row['input_dump_sha256'],'Input dump changed')
        config=configs[f'{job["context"]}-{job["side"]}'];need(len(dump['teams'])==2,'Roster source missing')
        for side,team in enumerate(config['teams']):
            actual=dump['teams'][side];need(actual['count']==len(actual['players'])==23,'Roster capacity drift')
            for got,wanted in zip(actual['players'],team['players'][:23],strict=True):
                need(got['id']==wanted['native_id'] and got['attributes']==wanted['attributes'],'Raw attribute/identity mismatch')
                attributes+=69
        binary=(local/'inputs'/f'{job["context"]}-{job["side"]}.bin').read_bytes()
        from analysis.run_observer005 import audit_input
        audit_input(evidence,dump,config,binary,read(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json'),frozen['oop_map'])
        for kind,side,slot,field,value in struct.iter_unpack('<5I',binary[12:]):
            if kind!=15:continue
            player=dump['teams'][side]['players'][slot]
            if field==0:need(bytes.fromhex(player['prefix_hex'])[0x6c:0x70]==struct.pack('<f',value/100),'Height mismatch')
            else:
                offset,size=offsets[field];raw=bytes.fromhex(player['prefix_hex'] if offset<0x80 else player['input_tail_hex'])
                start=offset if offset<0x80 else offset-0x4c5
                need(int.from_bytes(raw[start:start+size],'little')==value,'Native raw profile mismatch')
            profiles+=1
        observed=[e for e in evidence if e.get('event')=='native_passive_state']
        if job['mode'] in ('reference','observer_off'):need(not observed,'Off/reference emitted snapshots');continue
        need([s['stage'] for s in observed]==['prepared','first_advance','finished'],'Stage coverage differs')
        prepared,first,finish=observed
        need(prepared['tick']==0 and first['advance_ordinal']==1 and first['tick_before']==0 and
             first['requested_target']==first['tick']==1 and finish['tick']==natural['tick'] and
             finish['clock']==natural['clock'],'Actual first/finish timing drift')
        source={p['id']:p for t in dump['teams'] for p in t['players']};comparisons=[]
        for stage in observed:
            need(stage['seed']==job['seed'] and stage['match_version_raw']==0x1b000000 and len(stage['players'])==46,
                 'Stage seed/version/capacity drift')
            actors={p['id']:p for p in stage['players']};need(set(actors)==set(source),'Stage identity set drift')
            for identity,p in actors.items():
                tail=bytes.fromhex(source[identity]['input_tail_hex'])
                if stage['stage']=='prepared':
                    need(all(p[k]==struct.unpack_from('<H',tail,offset-0x4c5)[0] for k,offset in FIELDS.items()) and
                         p['effectiveness_region_hex']==tail[0xcba-0x4c5:0xcba-0x4c5+33].hex(),'Prepared bytes not dump-bound')
                need(p['statistics_cache_region_hex'] is not None or p['roster_index']>=11,'On-pitch missing cache')
            comparisons.append({i:tuple(p[k] for k in (*FIELDS,'condition_accumulator_raw','sharpness_penalty_raw','effectiveness_region_hex'))+
                (None if p['statistics_cache_region_hex'] is None else bytes.fromhex(p['statistics_cache_region_hex'])[9:11],)
                for i,p in actors.items()})
            stage_counts.append(dict(stage=stage['stage'],players=46,caches=sum(p['statistics_cache_region_hex'] is not None for p in actors.values()),
                nonzero_raw33=sum(any(bytes.fromhex(p['effectiveness_region_hex'])) for p in actors.values())))
            captures+=1
        states.setdefault(group,[]).append(comparisons)
    need(len(groups)==4 and all(len(v)==4 and all(r==v[0] for r in v) for v in groups.values()),'Four-mode outcome mismatch')
    need(len(states)==4 and all(len(v)==2 and v[0]==v[1] for v in states.values()),'Raw stage A/A mismatch')
    need(profiles==16*1058 and attributes==16*3174 and captures==24,'Readback coverage count mismatch')
    artifacts['ledger.jsonl']=file_hash(local/'ledger.jsonl')
    return dict(full_matches=16,exact_four_mode_groups=4,observer_traces=8,snapshots=captures,
        frozen_source_blobs_verified=len(frozen['code_sha256']),source_commit=commit,
        player_stage_records=captures*46,profile_values_verified=profiles,attribute_values_verified=attributes,
        cleanup_receipts_verified=20,private_artifact_files=len(artifacts),private_artifact_manifest_sha256=canonical_hash(artifacts),
        stage_counts=stage_counts,performance_inference=False,consumer_semantics_validated=False,
        ui_scale_calibrated=False,startpolicy_released=False,career_released=False,reviewer_native_starts=0)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--observer-directory', type=Path)
    parser.add_argument('--career-directory', type=Path)
    parser.add_argument('--upstream', type=Path)
    parser.add_argument('--career-runs-root', type=Path)
    parser.add_argument('--verify-private-career-runs', action='store_true')
    parser.add_argument('--observer-runs-root', type=Path)
    args = parser.parse_args()
    report = audit_public()
    supplied = [args.observer_directory,args.career_directory,args.upstream]
    need(not any(supplied) or all(supplied), 'All three explicit private directories required')
    if all(supplied):
        report['private'] = audit_private(*supplied)
    need(not args.verify_private_career_runs or args.career_runs_root, 'Explicit career-run root required')
    if args.career_runs_root:
        report['career_runs'] = audit_career_runs(args.career_runs_root,args.verify_private_career_runs)
    if args.observer_runs_root:
        report['observer_runs'] = audit_observer_runs(args.observer_runs_root)
    print(json.dumps(report, indent=2))

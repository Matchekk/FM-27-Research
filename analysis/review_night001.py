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


def audit_startpolicy_runs(central):
    """Reconstruct retained technical evidence; never starts a host or reserves seeds."""
    from datetime import datetime, timedelta
    from itertools import product
    central = Path(central).resolve()
    sys.path.insert(0, str(central))
    from analysis.run_observer005 import audit_input
    from research.passive_observer import FIELDS, canonical_hash
    public = central/'data/mech-002-startpolicy-tech'
    local = central/'local/mech-002-startpolicy-tech'
    directory = local/'technical'
    line_rows = lambda p: [json.loads(v) for v in p.read_text(encoding='utf8').splitlines() if v.strip()]
    frozen = read(public/'inputs.json'); registration = read(public/'registration.json')
    commit = registration['preregistration_commit']
    need(commit == '0744238cbcbd429dd59602f0470b18a1d9f52057', 'Unexpected startpolicy release')
    need(registration['code_sha256'] == frozen['code_sha256'], 'Registration source inventory drift')
    current_differences = []
    for name, wanted in frozen['code_sha256'].items():
        blob = subprocess.check_output(['git', 'show', commit+':'+name], cwd=central)
        need(sha256(blob.replace(b'\r\n', b'\n')).hexdigest() == wanted, 'Frozen Gitblob differs: '+name)
        if normalized_hash(central/name) != wanted: current_differences.append(name)
    need(normalized_hash(central/'analysis/run_observer005.py') == frozen['code_sha256']['analysis/run_observer005.py'],
         'Read-only input audit helper source drift')
    for name in ('inputs.json', 'seed-plan.json', 'job-plan.json', 'review-gate.json'):
        blob = subprocess.check_output(['git', 'show', commit+':data/mech-002-startpolicy-tech/'+name], cwd=central)
        need(blob.replace(b'\r\n', b'\n') == (public/name).read_bytes().replace(b'\r\n', b'\n'), 'Published input drift')
    need(registration['inputs_sha256'] == normalized_hash(public/'inputs.json') and
         registration['review_gate_sha256'] == normalized_hash(public/'review-gate.json'), 'Registration artifacts differ')
    seeds = read(public/'seed-plan.json')
    need(seeds == read(local/'seed-plan.json') == read(central/'local/registry/MECH-002-STARTPOLICY-TECH-V1.reserved.json'),
         'Seed reservation drift')
    need(len(seeds['seeds']) == len(set(seeds['seeds'])) == 4, 'Seed uniqueness differs')
    used = {0}
    def visit(value, context=False):
        if isinstance(value, dict):
            for key, child in value.items(): visit(child, context or key in ('seed','seeds','validation_seeds','effective_seed'))
        elif isinstance(value, list):
            for child in value: visit(child, context)
        elif context and type(value) is int: used.add(value)
    roots = [p for p in (central/'data').iterdir() if p.is_dir() and p != public]
    roots += [p for p in (central/'local').iterdir() if p.is_dir() and p != local and
              p.name.startswith(('valid','tact-','attr-','mech-','platform-smoke'))]
    for root in roots:
        for path in root.rglob('*.json*'):
            if path.suffix == '.json': visit(read(path))
            elif path.suffix == '.jsonl':
                for row in line_rows(path): visit(row)
    for path in (central/'local/registry').glob('*.json'):
        if path.name != 'MECH-002-STARTPOLICY-TECH-V1.reserved.json': visit(read(path))
    need(len(used) == seeds['excluded_seed_count'] == 2524 and canonical_hash(sorted(used)) == seeds['excluded_seed_set_sha256'] and
         not used.intersection(seeds['seeds']), 'Actual historical/reserved seed exclusion differs')
    expected_seeds = []; counter = 0
    while len(expected_seeds) < 4:
        candidate = int.from_bytes(sha256(f"{seeds['namespace']}/{counter}".encode()).digest()[:4], 'little'); counter += 1
        if candidate not in used and candidate not in expected_seeds: expected_seeds.append(candidate)
    need(expected_seeds == seeds['seeds'], 'Independent seed allocation reconstruction differs')
    plan = [dict(key=f'full-{context}-s{side}-sharp{level}-r{repeat}', kind='full', context=context,
                 side=side, level_raw=level, repeat=repeat, seed=seeds['seeds'][i])
            for i, (context, side) in enumerate(product(('high_press', 'deep_block'), (0, 1)))
            for level, repeat in product((10000, 7000), (0, 1))]
    plan.append(dict(key='negative-malformed', kind='negative', seed=None))
    need(plan == read(public/'job-plan.json'), 'Independently reconstructed job plan differs')
    ledger = line_rows(local/'ledger.jsonl')
    need(len(ledger) == 17 and ledger == line_rows(public/'measurements.jsonl'), 'Measurement ledger differs')
    accounting = line_rows(public/'job-accounting.jsonl')
    need(len(accounting) == 17 and len({r['key'] for r in ledger}) == 17, 'Attempt count/retry differs')
    budget = read(local/'budget.json'); reconciliation = read(local/'technical-reconciled.json')
    need(file_hash(local/'budget.json') == reconciliation['budget_sha256'] == read(public/'budget.json')['private_budget_sha256'],
         'Final budget reconciliation digest differs')
    need(budget['limits'] == {'technical':17, 'main':0} and budget['limit_seconds'] == 180 and
         budget['wall_limit_seconds'] == 900 and budget['active'] is None and budget['halted'] is False and
         budget['reserved'] == {j['key']:'technical' for j in plan} and len(budget['operations']) == 1,
         'Actual fixed budget/state differs')
    op = budget['operations'][0]; start = datetime.fromisoformat(budget['wall_start_utc'])
    deadline = datetime.fromisoformat(budget['wall_deadline_utc']); finish = datetime.fromisoformat(reconciliation['completed_utc'])
    need(op['name'] == op['kind'] == 'technical' and op['keys'] == [j['key'] for j in plan] and
         op['returncode'] == 0 and op['timed_out'] is False and
         0 < op['elapsed_seconds'] == budget['charged_seconds'] <= 180 and deadline-start == timedelta(seconds=900) and
         start <= datetime.fromisoformat(op['start_utc']) < finish <= deadline and
         (finish-datetime.fromisoformat(op['start_utc'])).total_seconds() >= op['elapsed_seconds'], 'Budget time/accounting differs')
    need(not (local/'native-cleanup-pending.json').exists() and
         not (central/'local/global-native/native-execution.lease.json').exists(), 'Unresolved native marker/lease')
    private_host = read(local/'private-host.json'); host = Path(private_host['observer_host'])
    build = read(private_host['build_manifest'])
    need(file_hash(host) == frozen['observer_host_sha256'] and file_hash(Path(private_host['build_manifest'])) == frozen['build_manifest_sha256'] and
         file_hash(host.parent/'desktop_host.cpp') == build['modified_host_source_sha256'] and
         file_hash(host.parent/'passive_observer_v1.h') == build['observer_header_sha256'] and
         normalized_hash(host.parent/'passive_observer_v1.h') == frozen['code_sha256']['adapters/passive_observer_v1.h'],
         'Actual host/header/modified-source build provenance differs')
    configs = read(local/'configs.json'); catalog = read(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json')
    need(file_hash(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json') == frozen['catalog_sha256'], 'Catalog drift')
    old = central/'local/valid005-observer-v1/inputs'
    binaries = {}; lineups = {}
    for context, side in product(('high_press', 'deep_block'), (0, 1)):
        label = f'{context}-{side}'; baseline = (old/(label+'.bin')).read_bytes()
        records = tuple(struct.iter_unpack('<5I', baseline[12:]))
        need(baseline[:8] == b'FM27CFG1' and len(records) == struct.unpack_from('<I', baseline, 8)[0] == 5557,
             'Original record count/format differs')
        lineup = {(s,a):v for k,s,a,b,v in records if k == 11 and b == 0}
        need(len(lineup) == 22, 'Absolute lineup incomplete')
        affected = {lineup[side,i] for i in range(1,11)}; lineups[label] = lineup, affected
        for level in (10000, 7000):
            name = label+f'-sharp{level}'; binary = (local/'inputs'/(name+'.bin')).read_bytes()
            after = tuple(struct.iter_unpack('<5I', binary[12:]))
            expected = tuple((k,s,a,b,level) if k == 15 and s == side and a in affected and b in (16,17) else (k,s,a,b,v)
                             for k,s,a,b,v in records)
            need(binary[:12] == baseline[:12] and after == expected and not any(r[0] == 61 for r in after) and
                 sha256(binary).hexdigest() == frozen['setups'][name], 'Unexpected intervention record/source difference')
            binaries[name] = binary
    offsets = {1:(0x79,1),9:(0xbb8,4),10:(0xbbc,4),19:(0x70,1),20:(0xca8,1),21:(0xca2,1),22:(0xca3,1)}
    offsets.update({f:(0x72+f-2,1) for f in range(2,9)})
    offsets.update({f:(a,2) for f,a in enumerate((0xc98,0xc8c,0xc96,0xc78,0xc8a,0xc90,0xc7a,0xc84),11)})
    artifacts = {}; traces = {}; results = {}; profile_count = 0; initial_caches = 0; transfers = 0; previous_end = None
    cache_counts = Counter(); finish_ranges = {k:[] for k in ('sharpness_raw','sharpness_secondary_raw','condition_accumulator_raw')}
    for job, row, account in zip(plan, ledger, accounting, strict=True):
        need(all(row[k] == v and account[k] == v for k,v in job.items()) and account['status'] == row['status'] and
             account['reserved'] is True and row['native_invocation_started'] is True, 'Incomplete job/accounting provenance')
        key = job['key']; proof = read(directory/(key+'.containment.json')); policy = proof['job_policy']
        process = read(directory/(key+'.process.json'))
        need(proof['cleanup_confirmed'] is proof['capsule_exit_confirmed'] is True and proof['kernel_active_processes'] == 0 and
             policy['active_process_limit'] == 3 and policy['limit_flags'] == 0x2008 and policy['kill_on_close'] is True and
             policy['breakaway_allowed'] is False and process['membership_verified_before_go'] is True,
             'Kernel cleanup/admission receipt differs')
        actual_start = datetime.fromisoformat(process['started_utc'])
        need(previous_end is None or previous_end <= actual_start, 'Native call timing intervals overlap')
        previous_end = actual_start+timedelta(seconds=proof['elapsed_seconds'])
        for suffix in ('.jsonl','.input.json','.stdout','.process.json','.containment.json','.started.json'):
            path = directory/(key+suffix)
            if path.is_file(): artifacts['technical/'+path.name] = file_hash(path)
        need(row['raw_log_sha256'] == file_hash(directory/(key+'.jsonl')) and
             row['stdout_sha256'] == file_hash(directory/(key+'.stdout')) and
             row['host_sha256'] == frozen['observer_host_sha256'] and
             row['engine_sha256'] == frozen['identity']['engine_sha256'], 'Raw artifact/host identity mismatch')
        evidence = line_rows(directory/(key+'.jsonl'))
        def one(name):
            values = [e for e in evidence if e.get('event') == name]
            need(len(values) == 1, 'Missing/duplicate native event: '+name)
            return values[0]
        need(one('native_image_fingerprint')['sha256'] == frozen['identity']['engine_sha256'], 'Actual DLL mismatch')
        if job['kind'] == 'negative':
            need(row['status'] == 'expected_rejection' and row['returncode'] == 108 and
                 one('scenario_rejected')['stage'] == 'initial' and not any(e.get('event') == 'natural_match_finished' for e in evidence),
                 'Negative cause/exit differs')
            continue
        need(row['status'] == 'ok' and row['returncode'] == 0, 'Failed full match')
        need(one('native_input_seed')['effective_seed'] == job['seed'] and one('native_input_seed')['override'] is True,
             'Actual seed differs')
        label = f"{job['context']}-{job['side']}"; name = label+f"-sharp{job['level_raw']}"; binary = binaries[name]
        need(row['setup_sha256'] == sha256(binary).hexdigest(), 'Actual scenario hash differs')
        dump = read(directory/(key+'.input.json'))
        need(file_hash(directory/(key+'.input.json')) == row['input_dump_sha256'], 'Dump hash differs')
        audit_input(evidence, dump, configs[label], binary, catalog, frozen['oop_map'])
        for kind, side, slot, field, value in struct.iter_unpack('<5I', binary[12:]):
            if kind != 15: continue
            p = dump['teams'][side]['players'][slot]
            if field == 0: need(bytes.fromhex(p['prefix_hex'])[0x6c:0x70] == struct.pack('<f', value/100), 'Native height differs')
            else:
                offset, size = offsets[field]; raw = bytes.fromhex(p['prefix_hex'] if offset < 0x80 else p['input_tail_hex'])
                at = offset if offset < 0x80 else offset-0x4c5
                need(int.from_bytes(raw[at:at+size], 'little') == value, 'Native profile differs')
            profile_count += 1
        natural = one('natural_match_finished'); stats = one('native_match_statistics')
        need(natural['full_match_completed'] is True and 0 < natural['tick'] < 47996 and stats['source'] == 'original_team_statistics',
             'Natural completion/source differs')
        result = dict(seed=job['seed'], score=natural['score'], tick=natural['tick'], clock=natural['clock'],
                      team_statistics=[{k:t[k] for k in ('xg','shots','shots_on_target','passes','completed_passes','possession','possession_ticks')}
                                       for t in stats['teams']])
        need(result == row['result'], 'Published result differs from native endpoint')
        results[key] = result; stages = [e for e in evidence if e.get('event') == 'native_passive_state']
        need([s['stage'] for s in stages] == ['prepared','first_advance','finished'] and stages[0]['tick'] == 0 and
             stages[1]['advance_ordinal'] == 1 and stages[1]['tick_before'] == 0 and stages[1]['requested_target'] == stages[1]['tick'] == 1 and
             stages[2]['tick'] == natural['tick'] and stages[2]['clock'] == natural['clock'], 'Actual stages/timing differ')
        source = {p['id']:p for t in dump['teams'] for p in t['players']}; lineup, affected = lineups[label]
        selected = []
        for stage in stages:
            need(stage['seed'] == job['seed'] and stage['match_version_raw'] == 0x1b000000 and len(stage['players']) == 46,
                 'Stage identity/version differs')
            actors = {p['id']:p for p in stage['players']}
            need(set(actors) == set(source) and {(p['side'],p['roster_index']) for p in actors.values()} == set(product((0,1), range(23))),
                 'Actor mapping/capacity differs')
            canonical_players = []
            for identity, p in sorted(actors.items()):
                cache = None if p['statistics_cache_region_hex'] is None else bytes.fromhex(p['statistics_cache_region_hex'])[9:11]
                need(len(bytes.fromhex(p['effectiveness_region_hex'])) == 33, 'TF storage length differs')
                if stage['stage'] == 'prepared':
                    tail = bytes.fromhex(source[identity]['input_tail_hex'])
                    need(all(p[k] == struct.unpack_from('<H', tail, offset-0x4c5)[0] for k,offset in FIELDS.items()) and
                         p['effectiveness_region_hex'] == tail[0xcba-0x4c5:0xcba-0x4c5+33].hex(), 'Prepared fields not input-dump-bound')
                if stage['stage'] != 'finished':
                    expected = job['level_raw'] if p['side'] == job['side'] and p['roster_index'] in affected else 10000
                    need(p['sharpness_raw'] == p['sharpness_secondary_raw'] == expected and p['condition_raw'] == 10000 and
                         p['fatigue_raw'] == p['sharpness_penalty_raw'] == 0 and p['condition_accumulator_raw'] == 1000000,
                         'Initial target/control raw fields differ')
                    if (p['side'], p['roster_index']) in {(s,lineup[s,i]) for s in (0,1) for i in range(11)}:
                        need(cache == bytes((100,expected//100)), 'Starting cache transfer differs'); initial_caches += 1
                    transfers += p['side'] == job['side'] and p['roster_index'] in affected
                else:
                    for k in finish_ranges: finish_ranges[k].append(p[k])
                canonical_players.append({k:p[k] for k in ('id','side','roster_index',*FIELDS,'condition_accumulator_raw',
                    'sharpness_penalty_raw','effectiveness_region_hex')} | {'cache89_8a': None if cache is None else cache.hex()})
            cache_counts[sum(p['statistics_cache_region_hex'] is not None for p in actors.values())] += 1
            selected.append({k:stage[k] for k in ('stage','advance_ordinal','tick_before','requested_target','tick','clock','seed','match_version_raw')} |
                            {'players':canonical_players})
        traces[key] = selected
    for context, side, level in product(('high_press','deep_block'),(0,1),(10000,7000)):
        prefix = f'full-{context}-s{side}-sharp{level}-r'
        need(results[prefix+'0'] == results[prefix+'1'] and traces[prefix+'0'] == traces[prefix+'1'], 'Exact A/A mismatch')
    for context, side, repeat in product(('high_press','deep_block'),(0,1),(0,1)):
        high = traces[f'full-{context}-s{side}-sharp10000-r{repeat}']; low = traces[f'full-{context}-s{side}-sharp7000-r{repeat}']
        for h, l in zip(high[:2], low[:2], strict=True):
            for p, q in zip(h['players'], l['players'], strict=True):
                need(all(p[k] == q[k] for k in ('id','side','roster_index','condition_raw','fatigue_raw','condition_accumulator_raw',
                     'sharpness_penalty_raw','effectiveness_region_hex')), 'Initial nonintervened control/TF33 mismatch')
    need(profile_count == 16928 and transfers == 320 and initial_caches == 704, 'Coverage count differs')
    for name in ('ledger.jsonl','budget.json','technical-reconciled.json','seed-plan.json','registration.json','configs.json','private-host.json'):
        artifacts[name] = file_hash(local/name)
    need(not list(directory.glob('*.failure.json')), 'Retained failed attempt exists')
    return dict(source_commit=commit, frozen_git_blobs_verified=len(frozen['code_sha256']), current_source_differences=current_differences,
        full_matches=16, attempts=17, aa_pairs=8, initial_control_pairs=8, negative_initial_108=1,
        snapshots=48, actor_stage_observations=2208, initial_snapshots=32, target_actor_stage_transfers=transfers,
        starter_initial_caches=initial_caches, profile_values_verified=profile_count, attribute_values_verified=50784,
        phase_cells_verified=704, pi_groups_verified=11968, cleanup_receipts=17, cache_counts=dict(cache_counts),
        charged_seconds=budget['charged_seconds'], private_budget_sha256=file_hash(local/'budget.json'),
        private_artifact_files=len(artifacts), private_artifact_manifest_sha256=canonical_hash(artifacts),
        finish_ranges={k:dict(min=min(v),max=max(v)) for k,v in finish_ranges.items()},
        all_seeds=seeds['seeds'], scientific_main_released=False, ui_scale_calibrated=False, career_released=False,
        reviewer_native_starts=0)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--observer-directory', type=Path)
    parser.add_argument('--career-directory', type=Path)
    parser.add_argument('--upstream', type=Path)
    parser.add_argument('--career-runs-root', type=Path)
    parser.add_argument('--verify-private-career-runs', action='store_true')
    parser.add_argument('--observer-runs-root', type=Path)
    parser.add_argument('--startpolicy-runs-root', type=Path)
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
    if args.startpolicy_runs_root:
        report['startpolicy_runs'] = audit_startpolicy_runs(args.startpolicy_runs_root)
    print(json.dumps(report, indent=2))

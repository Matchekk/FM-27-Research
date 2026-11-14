"""Seventeen centrally admitted technical probes; no scientific main route.

Preparation uses the historical offline codec, the unchanged readonly observer
host, and four externally reserved technical seeds. It never imports a server.
"""
from argparse import ArgumentParser
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis import run_observer005 as observer
from research.budget import atomic, supervisor_alive
from research.coordination import NativeLease
from research.core import config_hash, historical_seeds
from research.native import digest, event, read, require, rows, write
from research.night_control import assert_night_admission
from research.passive_observer import audit_trace, match_result
from analysis.startpolicy002_gate import (EXPERIMENT, CONTEXTS, LEVELS, audit_start_state,
    compile_cell, initial_control_equivalence, jobs, repeat_equivalence, technical_keys)
from research.study_budget import DeadlineBudget

LOCAL = ROOT/'local/mech-002-startpolicy-tech'
PUBLIC = ROOT/'data/mech-002-startpolicy-tech'
REGISTRY = ROOT/'local/registry'
RUNTIME = ROOT/'local/runtime-v1114.6'
OLD_LOCAL = ROOT/'local/valid005-observer-v1'
OLD_PUBLIC = ROOT/'data/valid-005-observer-v1'
DOCUMENT = 'experiments/MECH-002-startpolicy-tech.md'
REVIEW = 'docs/night-001/STARTPOLICY-002-REVIEW.md'
OBSERVER_REVIEW = 'docs/night-001/OBSERVER-RESULTS-REVIEW.md'
OBSERVER_COMMIT = '39b6af5422b160ae9bd4fa82d0c987c947f6916a'
OBSERVER_HOST = '58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
CODE = ('analysis/run_startpolicy002.py', 'analysis/startpolicy002_gate.py', 'analysis/audit_startpolicy002.py',
    'tests/test_startpolicy002.py', 'data/mech-002-startpolicy-tech/offline-source-audit.json',
    'analysis/run_observer005.py', 'analysis/night_supervise.py', 'research/startpolicy.py',
    'research/passive_observer.py', 'research/native_process005.py', 'research/night_control.py',
    'research/budget.py', 'research/study_budget.py', 'research/core.py', 'research/native.py',
    'research/coordination.py', 'adapters/passive_observer_v1.h', 'adapters/passive-observer-v1.patch',
    DOCUMENT, REVIEW, OBSERVER_REVIEW)
PUBLIC_FILES = ('inputs.json', 'seed-plan.json', 'job-plan.json', 'review-gate.json')
source_hash = observer.source_hash


def exclusive_json(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, allow_nan=False, indent=2); stream.write('\n')
        stream.flush(); os.fsync(stream.fileno())


def previous_seeds():
    used = {0}
    for path in (ROOT/'data').iterdir():
        if path.is_dir() and path != PUBLIC:
            used.update(historical_seeds(path))
    for path in REGISTRY.glob('*.json'):
        if path.name != EXPERIMENT+'.reserved.json':
            used.update(historical_seeds(path)); used.update(read(path).get('seeds', []))
    for path in (ROOT/'local').iterdir():
        if path.is_dir() and path != LOCAL and path.name.startswith(('valid', 'tact-', 'attr-', 'mech-', 'platform-smoke')):
            used.update(historical_seeds(path))
    return used


def seed_plan():
    value = read(REGISTRY/(EXPERIMENT+'.reserved.json'))
    require(value['experiment_id'] == EXPERIMENT and value['namespace'] == EXPERIMENT+'/technical-v1',
            'Wrong external seed reservation')
    jobs(value['seeds'])
    require(not set(value['seeds']) & previous_seeds(), 'Technical seeds collide with history/reservations')
    return value


def verify_observer_release():
    inputs = read(OLD_PUBLIC/'inputs.json'); registration = read(OLD_PUBLIC/'registration.json')
    summary = read(OLD_PUBLIC/'technical-summary.json')
    require(registration['preregistration_commit'] == OBSERVER_COMMIT and
            inputs['observer_host_sha256'] == OBSERVER_HOST, 'Original observer release identity differs')
    require(summary['passed'] is True and summary['full_matches'] == 16 and summary['loader_checks'] == 2
            and summary['negative_rejections'] == 2 and len(summary['equivalence']) == 4 and
            all(r['result_equivalence_verified'] is True for r in summary['equivalence']),
            'Completed original observer technical gate missing')
    for name in ('analysis/run_observer005.py', 'research/passive_observer.py', 'research/startpolicy.py',
                 'adapters/passive_observer_v1.h', 'adapters/passive-observer-v1.patch'):
        blob = subprocess.check_output(['git', 'show', OBSERVER_COMMIT+':'+name], cwd=ROOT)
        require(blob == (ROOT/name).read_bytes().replace(b'\r\n', b'\n'), 'Historical observer/codec source changed')
    return inputs


def release_hashes():
    return {name: source_hash(ROOT/name) for name in (
        'data/valid-005-observer-v1/inputs.json', 'data/valid-005-observer-v1/registration.json',
        'data/valid-005-observer-v1/technical-summary.json', OBSERVER_REVIEW)}


def prepare():
    require(not (PUBLIC/'inputs.json').exists() and not (LOCAL/'configs.json').exists(),
            'Prepared artifacts retained; no replacement/restart')
    prior = verify_observer_release(); reservation = seed_plan()
    private = read(OLD_LOCAL/'private-host.json'); host = Path(private['observer_host'])
    build = read(private['build_manifest'])
    require(digest(host) == prior['observer_host_sha256'] == OBSERVER_HOST and
            digest(private['build_manifest']) == prior['build_manifest_sha256'] and
            digest(host.parent/'desktop_host.cpp') == build['modified_host_source_sha256'] and
            digest(host.parent/'passive_observer_v1.h') == build['observer_header_sha256'] and
            source_hash(host.parent/'passive_observer_v1.h') == source_hash(ROOT/'adapters/passive_observer_v1.h'),
            'Unchanged observer binary/source/build receipts required')
    original = RUNTIME/'engine/fm27_native/FM27Simulator.exe'
    fixture = RUNTIME/'engine/fm27_native/fixtures/match.pkm'
    require(digest(original) == prior['identity']['adapter_host_sha256'] and
            digest(fixture) == prior['identity']['fixture_sha256'] and
            observer.fingerprint() == prior['identity']['resource_fingerprint'], 'Engine/resource/fixture drift')
    require(all(source_hash(RUNTIME/'source'/name) == value for name, value in prior['runtime_source_sha256'].items()),
            'Runtime tool source drift')
    configs = read(OLD_LOCAL/'configs.json')
    require(config_hash(configs) == prior['configs_sha256'], 'Historical D00 config drift')
    setups = {}; codec = {}; baseline_hashes = {}
    for context in CONTEXTS:
        for side in (0, 1):
            label = f'{context}-{side}'; baseline = OLD_LOCAL/'inputs'/(label+'.bin')
            require(digest(baseline) == prior['setups'][label], 'Historical D00 bytes changed')
            baseline_hashes[label] = digest(baseline)
            for level in LEVELS:
                payload, audit = compile_cell(baseline.read_bytes(), side, level)
                name = f'{label}-sharp{level}'
                path = LOCAL/'inputs'/(name+'.bin'); path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('xb') as stream: stream.write(payload)
                setups[name] = digest(path); codec[name] = audit
    exclusive_json(LOCAL/'configs.json', configs)
    exclusive_json(LOCAL/'private-host.json', private)
    exclusive_json(LOCAL/'seed-plan.json', reservation)
    exclusive_json(PUBLIC/'seed-plan.json', reservation)
    exclusive_json(PUBLIC/'job-plan.json', jobs(reservation['seeds']))
    exclusive_json(LOCAL/'technical-keys.json', technical_keys())
    exclusive_json(PUBLIC/'inputs.json', dict(schema='fm27.startpolicy002.inputs.v1', experiment_id=EXPERIMENT,
        identity=prior['identity'], observer_host_sha256=OBSERVER_HOST, build_manifest_sha256=prior['build_manifest_sha256'],
        observer_preregistration_commit=OBSERVER_COMMIT, observer_release_sha256=release_hashes(),
        setups=setups, baseline_setups=baseline_hashes, codec_audit=codec, configs_sha256=config_hash(configs),
        oop_map=prior['oop_map'], catalog_sha256=prior['catalog_sha256'], runtime_source_sha256=prior['runtime_source_sha256'],
        lease_module_sha256=prior['lease_module_sha256'], code_sha256={name: source_hash(ROOT/name) for name in CODE},
        seed_plan_sha256=source_hash(PUBLIC/'seed-plan.json'), job_plan_sha256=source_hash(PUBLIC/'job-plan.json'),
        max_workers=1, max_processes=3, logical_attempts=17, full_matches=16, negative_probes=1,
        progress_timeout_seconds=90, child_seconds=180, study_window_seconds=900,
        scientific_main_released=False, career_released=False))
    print('Prepared offline: sixteen full technical jobs and one malformed probe; no seeds allocated/native calls.')


def verify_frozen():
    value = read(PUBLIC/'inputs.json')
    require(value['experiment_id'] == EXPERIMENT and value['scientific_main_released'] is False,
            'Technical-only frozen contract required')
    require(all(source_hash(ROOT/name) == h for name, h in value['code_sha256'].items()), 'Frozen source changed')
    require(release_hashes() == value['observer_release_sha256'], 'Prior observer release changed')
    require(source_hash(PUBLIC/'seed-plan.json') == value['seed_plan_sha256'] and
            source_hash(PUBLIC/'job-plan.json') == value['job_plan_sha256'], 'Frozen job/seed plan changed')
    require(read(PUBLIC/'job-plan.json') == jobs(read(PUBLIC/'seed-plan.json')['seeds']), 'Job plan differs from declared matrix')
    require(read(PUBLIC/'seed-plan.json') == seed_plan(), 'External seed reservation changed')
    require(config_hash(read(LOCAL/'configs.json')) == value['configs_sha256'], 'Private config changed')
    require(all(digest(LOCAL/'inputs'/(name+'.bin')) == h for name, h in value['setups'].items()), 'Input binary drift')
    return value


def review_gate():
    value = read(PUBLIC/'review-gate.json')
    require(value['experiment_id'] == EXPERIMENT and value['approved_for_technical'] is True and
            value['inputs_sha256'] == source_hash(PUBLIC/'inputs.json') and
            value['review_sha256'] == source_hash(ROOT/REVIEW) and
            value['observer_results_review_sha256'] == source_hash(ROOT/OBSERVER_REVIEW), 'Independent technical approval missing/drifted')
    return value


def register(commit, ci_run):
    import re
    require(type(commit) is str and re.fullmatch('[0-9a-f]{40}', commit), 'Full published SHA required')
    require(type(ci_run) is int and ci_run > 0, 'Exact successful CI identifier required')
    value = verify_frozen(); review_gate(); observer.successful_ci(commit, ci_run)
    remote = subprocess.check_output(['git', 'ls-remote', 'origin', 'refs/heads/main'], cwd=ROOT, text=True).split()[0]
    for target in ('HEAD', remote):
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, target], cwd=ROOT, check=True, capture_output=True)
    verify_published(commit)
    exclusive_json(LOCAL/'registration.json', dict(experiment_id=EXPERIMENT, preregistration_commit=commit,
        ci_run=ci_run, inputs_sha256=source_hash(PUBLIC/'inputs.json'),
        review_gate_sha256=source_hash(PUBLIC/'review-gate.json'), code_sha256=value['code_sha256']))
    exclusive_json(PUBLIC/'registration.json', read(LOCAL/'registration.json'))


def verify_published(commit):
    for name in (*CODE, *(str(PUBLIC.relative_to(ROOT)/n).replace('\\', '/') for n in PUBLIC_FILES)):
        require(subprocess.check_output(['git', 'show', commit+':'+name], cwd=ROOT) ==
                (ROOT/name).read_bytes().replace(b'\r\n', b'\n'), 'Published artifact changed: '+name)


def clean_environment(identity):
    env = {k:v for k, v in os.environ.items() if not k.startswith('FM27_')}
    env.update(FM27_ENGINE_ROOT=str(RUNTIME/'engine'), FM27_GAME_ROOT=str(observer.GAME),
               FM27_EXPECTED_DLL_SHA256=identity['engine_sha256'], FM27_PASSIVE_OBSERVER_V1='1')
    return env


def native_call(command, env, log, output, on_start):
    from research.native_process005 import contained_call, confirmed_cleanup, CleanupUnconfirmed
    pending = LOCAL/'native-cleanup-pending.json'
    exclusive_json(pending, dict(operation=output.stem, started_utc=datetime.now(timezone.utc).isoformat()))
    try:
        result = contained_call(command, env, log, output, timeout=90, on_start=on_start, max_processes=3)
    except BaseException as error:
        if not confirmed_cleanup(output, expected_limit=3):
            raise CleanupUnconfirmed(dict(origin='startpolicy_wrapper', cause_type=type(error).__name__)) from error
        pending.unlink(); raise
    if not confirmed_cleanup(output, expected_limit=3):
        raise CleanupUnconfirmed(dict(origin='startpolicy_wrapper', cause_type='MissingConfirmedReceipt'))
    pending.unlink()
    return result


def assert_inner_admission():
    state = read(LOCAL/'budget.json'); active = state['active']
    require(state['experiment'] == EXPERIMENT and state['limits'] == {'technical':17, 'main':0} and
            state['limit_seconds'] == 180 and state['wall_limit_seconds'] == 900 and not state['halted'],
            'Inner budget identity/limits differ')
    require(active and active['name'] == 'technical' and active['kind'] == 'technical' and
            active['keys'] == technical_keys() and supervisor_alive(active['supervisor_pid']) and
            active['token_sha256'] == sha256(os.environ.get('TACT_P0_SUPERVISOR_TOKEN', '').encode()).hexdigest(),
            'No authenticated live inner supervisor')
    now = datetime.now(timezone.utc)
    require(now < datetime.fromisoformat(active['child_deadline_utc']) and
            now < datetime.fromisoformat(state['wall_deadline_utc']), 'Inner fixed deadline exhausted')
    lease = read(ROOT/'local/global-native/native-execution.lease.json')
    require(lease['owner_pid'] == active['supervisor_pid'] and lease['experiment'] == EXPERIMENT and lease['workers'] == 1,
            'One-worker global lease mismatch')


def audit_malformed(evidence, code):
    # Original host starts at "initial"; malformed magic returns before "records".
    require(type(code) is int and code == 108 and
            event(evidence, 'scenario_rejected')['stage'] == 'initial' and
            not any(e.get('event') == 'natural_match_finished' for e in evidence),
            'Malformed header was not rejected at the original initial stage')


def technical():
    frozen = verify_frozen(); review_gate(); registration = read(LOCAL/'registration.json')
    require(registration['inputs_sha256'] == source_hash(PUBLIC/'inputs.json') and
            registration['review_gate_sha256'] == source_hash(PUBLIC/'review-gate.json'), 'Registration drift')
    observer.successful_ci(registration['preregistration_commit'], registration['ci_run'])
    verify_published(registration['preregistration_commit'])
    private = read(LOCAL/'private-host.json'); host = Path(private['observer_host'])
    original = RUNTIME/'engine/fm27_native/FM27Simulator.exe'
    fixture = RUNTIME/'engine/fm27_native/fixtures/match.pkm'
    # Only the existing read-lease helper is imported; no server/initialize call.
    spec = importlib.util.spec_from_file_location('startpolicy_file_leases', RUNTIME/'source/desktop_engine.py')
    leases = importlib.util.module_from_spec(spec); spec.loader.exec_module(leases)
    for path in [*observer.resource_paths().values(), original, host, fixture, Path(private['build_manifest']),
                 host.parent/'desktop_host.cpp', host.parent/'passive_observer_v1.h',
                 LOCAL/'configs.json', RUNTIME/'source/tactics_ui/catalog.json', *LOCAL.glob('inputs/*.bin')]:
        leases.lease(path)
    try:
        require(digest(host) == frozen['observer_host_sha256'] and
                digest(original) == frozen['identity']['adapter_host_sha256'] and
                digest(fixture) == frozen['identity']['fixture_sha256'] and
                observer.fingerprint() == frozen['identity']['resource_fingerprint'] and
                digest(private['build_manifest']) == frozen['build_manifest_sha256'], 'Locked host/fixture/resource drift')
        build = read(private['build_manifest'])
        require(digest(host.parent/'desktop_host.cpp') == build['modified_host_source_sha256'] and
                digest(host.parent/'passive_observer_v1.h') == build['observer_header_sha256'] and
                source_hash(host.parent/'passive_observer_v1.h') == source_hash(ROOT/'adapters/passive_observer_v1.h'),
                'Locked build-source/header drift')
        require(all(digest(LOCAL/'inputs'/(name+'.bin')) == h for name,h in frozen['setups'].items()) and
                config_hash(read(LOCAL/'configs.json')) == frozen['configs_sha256'], 'Locked input/config drift')
        require(source_hash(RUNTIME/'source/desktop_engine.py') == frozen['lease_module_sha256'] and
                all(source_hash(RUNTIME/'source'/n) == h for n, h in frozen['runtime_source_sha256'].items()), 'Runtime source drift')
        require(digest(RUNTIME/'source/tactics_ui/catalog.json') == frozen['catalog_sha256'], 'Catalog drift')
        configs = read(LOCAL/'configs.json'); catalog = read(RUNTIME/'source/tactics_ui/catalog.json')
        evidence_by_cell = {}; directory = LOCAL/'technical'; directory.mkdir(exist_ok=False)
        for index, job in enumerate(read(PUBLIC/'job-plan.json')):
            assert_night_admission(ROOT, EXPERIMENT, 'technical', technical_keys())
            assert_inner_admission()
            require(sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file()) < 512*1024**2 and
                    shutil.disk_usage(LOCAL).free > 20*1024**3, 'Private disk/artifact limit')
            key = job['key']; log = directory/(key+'.jsonl'); dump = directory/(key+'.input.json'); out = directory/(key+'.stdout')
            row = dict(job, status='started', native_invocation_started=False)
            exclusive_json(directory/(key+'.started.json'), row)
            try:
                if job['kind'] == 'negative':
                    binary = LOCAL/'malformed.bin'
                    with binary.open('xb') as stream: stream.write(b'MECH002 INVALID INPUT')
                else:
                    label = f"{job['context']}-{job['side']}"
                    binary = LOCAL/'inputs'/f"{label}-sharp{job['level_raw']}.bin"
                command = [str(host), '--fixture', str(fixture), '--scenario-file', str(binary),
                           '--dump-input', str(dump), '--output', str(log), '--tick-step', '1']
                if job['seed'] is not None: command.extend(('--seed', str(job['seed'])))
                code, elapsed = native_call(command, clean_environment(frozen['identity']), log, out,
                    on_start=lambda: row.update(native_invocation_started=True))
                row.update(returncode=code, elapsed_seconds=elapsed, setup_sha256=digest(binary),
                           stdout_sha256=digest(out), host_sha256=digest(host),
                           engine_sha256=frozen['identity']['engine_sha256'])
                evidence = rows(log) if log.exists() else []
                if job['kind'] == 'negative':
                    audit_malformed(evidence, code)
                    row['status'] = 'expected_rejection'
                else:
                    require(code == 0 and dump.exists(), 'Full native probe failed')
                    native_dump = read(dump)
                    row.update(observer.audit_input(evidence, native_dump, configs[label], binary.read_bytes(), catalog, frozen['oop_map']))
                    row['passive_audit'] = audit_trace(evidence, native_dump, job['seed'])
                    baseline = (LOCAL/'inputs'/f'{label}-sharp10000.bin').read_bytes()
                    row['startpolicy_audit'] = audit_start_state(evidence, baseline, job['side'], job['level_raw'])
                    row.update(result=match_result(evidence, job['seed']), input_dump_sha256=digest(dump), status='ok')
                    evidence_by_cell[job['context'], job['side'], job['level_raw'], job['repeat']] = evidence
                    if job['repeat'] == 1:
                        row['aa'] = repeat_equivalence(evidence_by_cell[job['context'], job['side'], job['level_raw'], 0], evidence, job['seed'])
                    if job['level_raw'] == 7000:
                        row['controls'] = initial_control_equivalence(evidence_by_cell[job['context'], job['side'], 10000, job['repeat']], evidence)
                row['raw_log_sha256'] = digest(log) if log.exists() else None
            except BaseException as error:
                row.update(status='failed', error_type=type(error).__name__)
                exclusive_json(directory/(key+'.failure.json'), dict(detail=str(error)))
                raise
            finally:
                with (LOCAL/'ledger.jsonl').open('a', encoding='utf8') as stream:
                    stream.write(json.dumps(row, allow_nan=False)+'\n'); stream.flush(); os.fsync(stream.fileno())
            print(f'{index+1}/17 {key}: {row["status"]}', flush=True)
        exclusive_json(LOCAL/'technical-summary.json', dict(passed=True, full_matches=16, aa_pairs=8,
            negative_rejections=1, initial_control_pairs=8, raw_and_cache_transfer_verified=True,
            scientific_main_released=False, career_released=False, ui_scale_calibrated=False))
    finally:
        leases.close_leases()


def supervise():
    budget = DeadlineBudget(LOCAL/'budget.json', experiment=EXPERIMENT, seconds=180,
                            caps={'technical':17, 'main':0}, wall_seconds=900)
    require(not (LOCAL/'technical.lease.json').exists() and not (LOCAL/'technical.stdout').exists(), 'Retained phase: no retry')
    lease = NativeLease(ROOT/'local/global-native', EXPERIMENT, workers=1).acquire()
    try:
        owned = lease.assert_owned()
        exclusive_json(LOCAL/'technical.lease.json', {k:owned[k] for k in ('schema', 'experiment', 'workers', 'owner_pid', 'acquired_utc')})
        command = [sys.executable, str(Path(__file__).resolve()), 'technical', '--child']
        budget.run('technical', 'technical', technical_keys(), command, ROOT, LOCAL/'technical.stdout')
    finally:
        state = budget.load()
        if state['active'] or (LOCAL/'native-cleanup-pending.json').exists():
            state.update(halted=True, cleanup_unconfirmed=True, global_native_lease_retained=True); atomic(budget.path, state)
        else:
            lease.release()


def export():
    # Only aggregate known fields; no private IDs, argv, token, TF bytes or paths.
    ledger = rows(LOCAL/'ledger.jsonl') if (LOCAL/'ledger.jsonl').exists() else []
    require(len({r['key'] for r in ledger}) == len(ledger), 'Duplicate attempts')
    actual = {r['key']:r for r in ledger}
    plan = read(PUBLIC/'job-plan.json') if (PUBLIC/'job-plan.json').exists() else [dict(r, seed=None) for r in jobs([1,2,3,4])]
    require(not set(actual)-{j['key'] for j in plan}, 'Unexpected job ledger entry')
    budget = read(LOCAL/'budget.json') if (LOCAL/'budget.json').exists() else None
    unresolved = bool((LOCAL/'native-cleanup-pending.json').exists() or (budget and (budget['active'] or budget.get('cleanup_unconfirmed'))))
    output = []
    for job in plan:
        row = actual.get(job['key']); status = row['status'] if row else 'started_unresolved' if (LOCAL/'technical'/(job['key']+'.started.json')).exists() else 'not_started'
        output.append(dict(job, status=status, reserved=bool(budget and job['key'] in budget['reserved'])))
        if row and row.get('raw_log_sha256'):
            require(digest(LOCAL/'technical'/(job['key']+'.jsonl')) == row['raw_log_sha256'], 'Private raw evidence changed')
        if row and row.get('input_dump_sha256'):
            require(digest(LOCAL/'technical'/(job['key']+'.input.json')) == row['input_dump_sha256'], 'Private input dump changed')
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for name, value in (('measurements.jsonl', ledger), ('job-accounting.jsonl', output)):
        (PUBLIC/name).write_text(''.join(json.dumps(row, allow_nan=False)+'\n' for row in value), encoding='utf8')
    summary = read(LOCAL/'technical-summary.json') if (LOCAL/'technical-summary.json').exists() else dict(passed=False)
    summary.update(scientific_main_released=False, career_released=False)
    complete = (len(ledger) == 17 and sum(r['kind'] == 'full' and r['status'] == 'ok' for r in ledger) == 16 and
                sum(r['kind'] == 'negative' and r['status'] == 'expected_rejection' for r in ledger) == 1 and
                sum(r.get('aa',{}).get('exact_outcomes_and_identified_fields_equal') is True for r in ledger) == 8 and
                sum(r.get('controls',{}).get('initial_control_fields_and_raw_tf33_equal') is True for r in ledger) == 8)
    if not complete: summary.update(passed=False, technical_set_incomplete=True)
    if unresolved: summary.update(passed=False, cleanup_unconfirmed=True)
    write(PUBLIC/'technical-summary.json', summary)
    if budget:
        public = {k:budget[k] for k in ('experiment', 'limits', 'limit_seconds', 'charged_seconds', 'reserved', 'halted',
                    'wall_start_utc', 'wall_deadline_utc', 'wall_limit_seconds')}
        public.update(cleanup_unconfirmed=unresolved, charged_seconds_incomplete=unresolved,
                      global_native_lease_retained=bool(unresolved or budget.get('global_native_lease_retained')))
        write(PUBLIC/'budget.json', public)
    print(json.dumps(dict(passed=summary['passed'], resolved_jobs=len(ledger), total_jobs=17)))


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('prepare', 'register', 'technical', 'export', 'status'))
    parser.add_argument('--child', action='store_true'); parser.add_argument('--commit'); parser.add_argument('--ci-run', type=int)
    args = parser.parse_args()
    require((ROOT/'.git').is_dir(), 'Execute only from central checkout')
    if args.phase == 'export': export(); return
    if args.phase == 'status': print(json.dumps(read(LOCAL/'budget.json'), indent=2)); return
    if args.phase == 'register': register(args.commit, args.ci_run); return
    assert_night_admission(ROOT, EXPERIMENT, args.phase, [] if args.phase == 'prepare' else technical_keys())
    if args.phase == 'prepare':
        require(not args.child, 'No inert prepare child mode'); prepare(); return
    if args.child:
        assert_inner_admission()
        technical()
    else:
        supervise()


if __name__ == '__main__':
    main()

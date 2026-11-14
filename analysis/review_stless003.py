"""Read-only independent IP/OOP package verification; never starts native code.

Scientific inference is reconstructed directly from scores/xG. This module does
not import the producer analysis or research.stats. Optional private modes reuse
only low-level native readback audits against already-existing files.
"""
from argparse import ArgumentParser
import ast
from collections import Counter
from datetime import datetime, timedelta
from hashlib import sha256
from itertools import product
import json
from math import isclose, isfinite, sqrt
from pathlib import Path
import re
from statistics import covariance, fmean, variance
import subprocess
import sys

import numpy as np
from scipy.stats import chi2, nct, t

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
EXPERIMENT = 'TACT-003-STLESS-R0'
CONTEXTS = ('high_press', 'deep_block')
ARMS = ('I0-O0', 'I1-O0', 'I0-O1', 'I1-O1')
FAMILY = ('IP:xgd', 'OOP:xgd', 'INTERACTION:points',
          'INTERACTION:gf', 'INTERACTION:ga', 'INTERACTION:xgf', 'INTERACTION:xga')
ENDPOINTS = ('xgd', 'points', 'gf', 'ga', 'xgf', 'xga')
HOST = '58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
BOOT_SEED = int.from_bytes(sha256(b'TACT-003-STLESS-R0/bootstrap-v1').digest()[:8], 'little')
HASH = re.compile('[0-9a-f]{64}\\Z')
DESCRIPTIVE = tuple(f'{s}_{m}_mean' for s in ('prepared', 'first', 'finished')
    for m in ('condition_cache89', 'sharpness_cache8a')) + (
    'prepared_tf33_matches_frozen_d00', 'first_tf33_matches_frozen_d00',
    'finished_tf33_distinct_hashes', *(f'finished_{m}_mean' for m in (
    'condition_raw', 'sharpness_raw', 'sharpness_secondary_raw', 'fatigue_raw',
    'condition_accumulator_raw', 'sharpness_penalty_raw')))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path, normalized=False):
    value = Path(path).read_bytes()
    return sha256(value.replace(b'\r\n', b'\n') if normalized else value).hexdigest()


def read(path):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'Duplicate JSON field')
            result[key] = value
        return result
    def invalid(_):
        raise ValueError('Nonfinite JSON constant')
    decode = lambda value: json.loads(value, object_pairs_hook=pairs, parse_constant=invalid)
    path = Path(path)
    if path.suffix == '.jsonl':
        return [decode(line) for line in path.read_text(encoding='utf8').splitlines() if line.strip()]
    return decode(path.read_text(encoding='utf8'))


def number(value):
    return type(value) in (int, float) and isfinite(value)


def compare(actual, expected, label):
    if expected is None:
        need(actual is None, 'Stored undefined statistic differs: ' + label)
    elif type(expected) is bool:
        need(actual is expected, 'Stored Boolean differs: ' + label)
    elif type(expected) in (list, tuple):
        need(type(actual) in (list, tuple) and len(actual) == len(expected), 'Stored list differs: ' + label)
        for a, b in zip(actual, expected, strict=True):
            compare(a, b, label)
    else:
        need(number(actual) and number(expected) and isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12),
             'Stored statistic differs: ' + label)


def expected_jobs(receipt, seeds, phase):
    config = receipt['config']
    need(receipt['config_sha256'] == canonical(config) and config['experiment_id'] == EXPERIMENT and
         config['design']['n_blocks'] == 32 and config['design']['sides'] == [0, 1] and
         [a['id'] for a in config['design']['arms']] == list(ARMS) and
         [s['id'] for s in config['design']['scenarios']] == list(CONTEXTS), 'Manifest design/config differs')
    main, technical = seeds['main_seeds'], seeds['technical_seeds']
    need(len(main) == len(set(main)) == 64 and len(technical) == len(set(technical)) == 4 and
         len(set(main + technical)) == 68 and receipt['seeds'] == main and
         all(type(s) is int and 0 < s <= 0xffffffff for s in main + technical), 'Seed inventory differs')
    if phase == 'technical':
        return [dict(key=f'tech-{h}-s{s}-{a}-r{r}', scenario=h, side=s, arm=a, seed=technical[i], repeat=r)
            for i, (h, s) in enumerate(product(CONTEXTS, (0, 1))) for a, r in product(ARMS, (0, 1))] + [
            dict(key='negative-malformed', seed=None, kind='negative')]
    need(phase == 'main', 'Explicit phase required')
    jobs = [dict(key=f'{h}-{seed}-{s}-{a}', scenario=h, side=s, arm=a, seed=seed)
            for i, h in enumerate(CONTEXTS) for seed, s, a in product(main[i*32:(i+1)*32], (0, 1), ARMS)]
    return sorted(jobs, key=lambda j: sha256(j['key'].encode()).digest())


def raw_metrics(row):
    side = row['team_side'];result = row['result'];score = result['score'];teams = result['team_statistics']
    need(type(side) is int and side in (0, 1) and type(score) is list and len(score) == 2 and
         all(type(v) is int and 0 <= v <= 100 for v in score) and len(teams) == 2, 'Invalid score/side')
    need(type(result['tick']) is int and 0 < result['tick'] < 47996 and type(result['clock']) is int and
         result['clock'] >= 0, 'Missing natural finish')
    for team in teams:
        need(number(team['xg']) and team['xg'] >= 0 and number(team['possession']) and
             0 <= team['possession'] <= 1, 'Invalid xG/possession')
        for field in ('shots', 'shots_on_target', 'passes', 'completed_passes'):
            need(type(team[field]) is int and team[field] >= 0, 'Invalid native count')
        need(team['shots_on_target'] <= team['shots'] and team['completed_passes'] <= team['passes'],
             'Impossible native count relation')
    need(abs(sum(team['possession'] for team in teams) - 1) < 1e-6, 'Possession sum differs')
    gf, ga = score[side], score[1-side];xgf, xga = teams[side]['xg'], teams[1-side]['xg']
    return dict(xgd=xgf-xga, points=3 if gf > ga else int(gf == ga), gf=gf, ga=ga, xgf=xgf, xga=xga)


def check_rows(data, receipt, seeds, phase):
    config = receipt['config'];plan = expected_jobs(receipt, seeds, phase)
    expected = {j['key']: j for j in plan if j.get('kind') != 'negative'};seen = set()
    need(len(data) == len(expected), 'Incomplete match/seed blocks')
    for row in data:
        key = row['job_id'];need(key in expected and key not in seen, 'Duplicate/unexpected match cell');seen.add(key)
        job = expected[key];arm = ARMS.index(job['arm']);ip = arm in (1, 3);oop = arm in (2, 3)
        need(row['experiment_id'] == EXPERIMENT and row['status'] == 'ok' and row['context'] == job['scenario'] and
             row['team_side'] == job['side'] and row['seed'] == job['seed'] and row['arm'] == job['arm'] and
             row['config_sha256'] == receipt['config_sha256'] and row['identity'] == config['identity'] and
             row['setup_sha256'] == config['design']['setups'][job['scenario']][str(job['side'])][job['arm']] and
             row['observer_host_sha256'] == HOST, 'Identity/setup/seed/arm differs')
        audit = row['native_audit']
        need(all(audit.get(k) is True for k in ('input_verified', 'seed_verified', 'package_verified',
             'stamina60_verified', 'pressing_verified', 'controls_verified', 'start_state_verified', 'native_game_rules_verified')), 'Missing declared native audit')
        need(all(type(audit.get(k)) is int and audit[k] == value for k, value in (
            ('attribute_values_verified', 3174), ('profile_fields_verified', 1058), ('phase_cells_verified', 44),
            ('pi_groups_verified', 748), ('pressing_bit', 0))), 'Wrong native audit values')
        need(audit['ip_strikerless'] is ip and audit['oop_strikerless'] is oop, 'Wrong package audit values')
        values, missing = row['descriptive'], row['descriptive_missing_reasons']
        need(set(values) == set(DESCRIPTIVE) and set(missing) == {k for k, v in values.items() if v is None} and
             set(missing) <= {'finished_condition_cache89_mean', 'finished_sharpness_cache8a_mean'} and
             all(type(v) is str and v.strip() for v in missing.values()), 'Descriptive missing accounting differs')
        for stage in ('prepared', 'first'):
            need(values[stage + '_tf33_matches_frozen_d00'] is True and
                 values[stage + '_condition_cache89_mean'] == values[stage + '_sharpness_cache8a_mean'] == 100, 'Initial controls differ')
        for key, value in values.items():
            if value is None or type(value) is bool:continue
            need(number(value), 'Nonfinite descriptive value')
            if '_cache' in key:need(0 <= value <= 255, 'Cache mean outside byte bounds')
        need(type(values['finished_tf33_distinct_hashes']) is int and
             1 <= values['finished_tf33_distinct_hashes'] <= 10, 'RawTF hash denominator differs')
        raw_metrics(row)
    need(seen == set(expected), 'Incomplete match/seed blocks')
    return plan


def independently_group(data, receipt):
    indexed = {}
    for row in data:
        key = (row['context'], row['seed'], row['team_side'], row['arm'])
        need(key not in indexed, 'Duplicate independent block cell');indexed[key] = raw_metrics(row)
    need(len(indexed) == 512, 'Incomplete independent block cells')
    grouped = {}
    for name, endpoint in [('INTERACTION', 'xgd'), *[key.split(':') for key in FAMILY]]:
        contexts = []
        for h, context in enumerate(CONTEXTS):
            sides = [[], []]
            for seed, side in product(receipt['seeds'][h*32:(h+1)*32], (0, 1)):
                need(all((context, seed, side, arm) in indexed for arm in ARMS), 'Missing independent block cell')
                ll, hl, lh, hh = [indexed[context, seed, side, arm][endpoint] for arm in ARMS]
                value = (hh-lh)-(hl-ll) if name == 'INTERACTION' else ((hl-ll)+(hh-lh))/2 if name == 'IP' else ((lh-ll)+(hh-hl))/2
                sides[side].append(value)
            contexts.append(dict(sides=sides, blocks=[(a+b)/2 for a, b in zip(*sides, strict=True)]))
        grouped[name + ':' + endpoint] = contexts
    return grouped


def summarize(contexts):
    arrays = [c['blocks'] for c in contexts];means = list(map(fmean, arrays))
    parts = [variance(a)/(4*len(a)) for a in arrays];v = sum(parts);mean = sum(means)/2
    if v:
        df = v*v/sum(p*p/(len(a)-1) for p, a in zip(parts, arrays, strict=True))
        se = sqrt(v);half = float(t.isf(.025, df))*se;p = float(2*t.sf(abs(mean/se), df))
    else:df = None;se = half = 0.;p = float(mean == 0)
    rng = np.random.default_rng(BOOT_SEED)
    boot = sum(np.asarray(a)[rng.integers(len(a), size=(20000, len(a)))].mean(axis=1) for a in arrays)/2
    loo = [(fmean(a[:i] + a[i+1:]) + means[1-h])/2 for h, a in enumerate(arrays) for i in range(len(a))]
    contexts_out = {}
    for h, context in enumerate(CONTEXTS):
        a, b = contexts[h]['sides'];blocks = arrays[h];sd = sqrt(variance(blocks))
        contexts_out[context] = dict(mean=fmean(blocks), sd=sd,
            sd_upper95_normal_model=sd*sqrt(31/chi2.ppf(.05, 31)), side0_mean=fmean(a), side1_mean=fmean(b),
            side0_sd=sqrt(variance(a)), side1_sd=sqrt(variance(b)), side_covariance=covariance(a, b))
    return dict(mean=mean, se=se, df=df, ci=[mean-half, mean+half], p=p,
        bootstrap_ci=np.quantile(boot, [.025, .975]).tolist(), context=contexts_out,
        leave_one_out=dict(range=[min(loo), max(loo)], max_change=max(abs(x-mean) for x in loo)))


def holm(pvalues):
    adjusted = {};previous = 0.
    for rank, key in enumerate(sorted(pvalues, key=pvalues.get)):
        previous = max(previous, min(1., (len(pvalues)-rank)*pvalues[key]));adjusted[key] = previous
    return adjusted


def independent_planning(sd):
    result = {}
    for key, multiplier in (('observed', 1.), ('simultaneous95_sd_upper', sqrt(31/chi2.ppf(.025, 31)))):
        values = [s*multiplier for s in sd];entries = []
        for effect in (.2, .3):
            for n in range(2, 100001):
                parts = [s*s/(4*n) for s in values];v = sum(parts)
                if v:
                    se = sqrt(v);df = v*v/sum(p*p/(n-1) for p in parts);cut = t.isf(.025, df)
                    # Symmetry avoids SciPy's occasional NaN negative-tail CDF
                    # at large positive noncentrality in tiny synthetic designs.
                    power = float(nct.sf(cut, df, -effect/se)+nct.sf(cut, df, effect/se));width = float(2*cut*se)
                else:power = 1.;width = 0.
                if power >= .9:break
            else:raise ValueError('Independent future planning search limit exceeded')
            entries.append(dict(effect=effect, seeds_per_context=n, independent_blocks=2*n,
                                matches=16*n, full_width=width, power=power))
        result[key] = dict(sd=values, power90=entries)
    return result


def verify_stored_analysis(data, receipt, effects, blocks):
    grouped = independently_group(data, receipt)
    need(effects['experiment_id'] == EXPERIMENT and effects['n_matches'] == 512 and
         effects['independent_seed_blocks'] == 64 and effects['primary_contrast'] == 'INTERACTION' and
         set(effects['secondary']) == set(FAMILY), 'Stored sample/contrast family differs')
    need(effects['bootstrap'] == dict(seed=BOOT_SEED, resamples=20000) and effects['practical_reference'] == .2 and
         effects['desired_full_ci_width'] == .5 and effects['exploratory_context_and_side_only'] is True and
         all(effects[k] is False for k in (
         'ui_scale_calibrated', 'consumer_semantics_validated', 'mediation_identified', 'career_transfer_confirmed',
         'isolated_role_mechanism_identified', 'winner_selected')), 'Stored interpretation/analysis settings differ')
    independent = {key: summarize(value) for key, value in grouped.items()}
    adjusted = holm({key: independent[key]['p'] for key in FAMILY});expected_blocks = []
    for key, wanted in independent.items():
        got = effects['primary'] if key == 'INTERACTION:xgd' else effects['secondary'][key]
        for field in ('mean', 'se', 'df', 'p', 'ci', 'bootstrap_ci'):
            compare(got[field], wanted[field], key + '/' + field)
        need(got['n_seed_blocks'] == 64 and got['n_scenarios'] == 2 and got['alpha'] == .05,
             'Stored inferential unit differs')
        for field, value in wanted['leave_one_out'].items():compare(got['leave_one_out'][field], value, key + '/LOO')
        for h, context in enumerate(CONTEXTS):
            for field, value in wanted['context'][context].items():compare(got['context'][context][field], value, key + '/' + field)
            name, endpoint = key.split(':')
            expected_blocks.extend(dict(context=context, seed=receipt['seeds'][h*32+i], contrast=name,
                endpoint=endpoint, value=value) for i, value in enumerate(grouped[key][h]['blocks']))
        if key in FAMILY:
            compare(got['p_holm'], adjusted[key], key + '/Holm')
            need(got['reject_holm'] is (adjusted[key] <= .05), 'Stored Holm decision differs')
    planning = independent_planning([independent['INTERACTION:xgd']['context'][h]['sd'] for h in CONTEXTS])
    for key, wanted in planning.items():
        compare(effects['planning'][key]['sd'], wanted['sd'], 'planning/' + key)
        need(len(effects['planning'][key]['power90']) == 2, 'Stored planning family differs')
        for got, expected in zip(effects['planning'][key]['power90'], wanted['power90'], strict=True):
            for field, value in expected.items():compare(got[field], value, 'planning/' + field)
    need(len(blocks) == len(expected_blocks) == 512, 'Stored derived contrast row count differs')
    for actual, wanted in zip(blocks, expected_blocks, strict=True):
        need(set(actual) == set(wanted) and all(actual[k] == wanted[k] for k in ('context', 'seed', 'contrast', 'endpoint')),
             'Stored derived contrast identity/order differs')
        compare(actual['value'], wanted['value'], 'derived seed contrast')
    for context, arm in product(CONTEXTS, ARMS):
        selected = [r for r in data if r['context'] == context and r['arm'] == arm]
        need(len(selected) == 64, 'Stored arm denominator differs')
        metrics = [raw_metrics(r) for r in selected]
        for endpoint in ENDPOINTS:compare(effects['arm_means'][context][arm][endpoint], fmean(m[endpoint] for m in metrics), 'arm/' + endpoint)
        for field in DESCRIPTIVE:
            observed = [r['descriptive'][field] for r in selected if r['descriptive'][field] is not None]
            missing = Counter(r['descriptive_missing_reasons'][field] for r in selected if r['descriptive'][field] is None)
            got = effects['descriptive']['by_context_arm'][context][arm][field]
            need(got['observed'] == len(observed) and got['missing'] == sum(missing.values()) and
                 got['missing_reasons'] == dict(missing), 'Stored descriptive denominator differs')
            for name, value in (('mean', fmean(observed) if observed else None), ('min', min(observed) if observed else None),
                                ('max', max(observed) if observed else None)):
                compare(got[name], value, 'descriptive/' + field)
    return dict(independent_seed_blocks=64, derived_contrast_rows=512,
        primary=independent['INTERACTION:xgd'], secondary_holm=adjusted, stored_effects_verified=True,
        conditional_planning_verified=True)


def audit_accounting(public, phase, plan):
    summary = read(public / (phase + '-summary.json'));budget = read(public / (phase + '-budget.json'))
    accounting = read(public / (phase + '-job-accounting.jsonl'))
    need(len(accounting) == len(plan) and all(row == dict(job_id=job['key'], seed=job.get('seed'),
         status='expected_rejection' if job.get('kind') == 'negative' else 'ok', admission_error_type=None)
         for row, job in zip(accounting, plan, strict=True)), 'Public failed/incomplete job accounting')
    need(summary['passed'] is True and summary['complete'] is True and summary['budget_reconciled'] is True and
         summary['full_matches'] == (32 if phase == 'technical' else 512) and
         summary['negative_rejections'] == (1 if phase == 'technical' else 0) and
         summary['peak_inflight_claims'] == 4 and summary['engine_pid_peak_measured'] is False,
         'Public phase summary differs')
    need(budget['passed'] is True and budget['active'] is None and budget['halted'] is False and
         budget['limits'] == {'technical': 33, 'main': 512} and budget['limit_seconds'] == 900 and
         budget['wall_limit_seconds'] == 5400 and budget['charged_seconds_incomplete'] is False and
         number(budget['charged_seconds']) and 0 < budget['charged_seconds'] <= 900 and
         budget['recorded_charged_seconds'] == budget['charged_seconds'], 'Public budget differs')
    phases = ['technical'] if phase == 'technical' else ['technical', 'main']
    operations = budget['operations'];need([o['name'] for o in operations] == phases, 'Budget operation coverage differs')
    need(sum(o['elapsed_seconds'] for o in operations) == budget['charged_seconds'], 'Budget time refunded/different')
    start = datetime.fromisoformat(budget['wall_start_utc']);end = datetime.fromisoformat(budget['wall_deadline_utc'])
    finish = datetime.fromisoformat(budget['completed_utc'])
    need(all(v.utcoffset() == timedelta(0) for v in (start, end, finish)) and end-start == timedelta(seconds=5400) and
         start < finish <= end and finish <= datetime.fromisoformat('2026-11-15T07:00:00+00:00'), 'Budget fixed UTC evidence differs')
    for op in operations:
        wanted = expected_job_keys(public, op['name'])
        need(op['keys'] == wanted and op['kind'] == op['name'] and op['returncode'] == 0 and op['timed_out'] is False and
             number(op['elapsed_seconds']) and op['elapsed_seconds'] > 0, 'Budget operation/job reservation differs')
        begin = datetime.fromisoformat(op['start_utc']);deadline = datetime.fromisoformat(op['child_deadline_utc'])
        need(begin.utcoffset() == deadline.utcoffset() == timedelta(0) and
             start <= begin < deadline <= end and op['elapsed_seconds'] <= (deadline-begin).total_seconds() <= 900 and
             (finish-begin).total_seconds() >= op['elapsed_seconds'], 'Budget operation UTC evidence differs')
    return summary


def expected_job_keys(public, phase):
    return [j['key'] for j in read(public / (phase + '-job-plan.json'))]


def audit_public(root, phase):
    root = Path(root);public = root / 'data/night-002-stless003'
    receipt = read(public / 'manifest.json');seeds = read(public / 'seed-plan.json')
    data = read(public / ('technical.jsonl' if phase == 'technical' else 'main.jsonl'))
    plan = check_rows(data, receipt, seeds, phase);published_plan = read(public / (phase + '-job-plan.json'))
    need([j['key'] for j in published_plan] == [j['key'] for j in plan], 'Published job plan differs')
    for actual, wanted in zip(published_plan, plan, strict=True):
        need(all(actual.get(k) == v for k, v in wanted.items()), 'Published job assignment differs')
    for row in data:
        need(row['returncode'] == 0 and row['native_invocation_started'] is True and
             number(row['native_elapsed_seconds']) and 0 < row['native_elapsed_seconds'] <= 40 and
             all(type(row[k]) is str and HASH.fullmatch(row[k]) for k in
             ('stdout_sha256', 'raw_log_sha256', 'input_dump_sha256', 'containment_receipt_sha256')),
             'Public native artifact descriptors incomplete')
    summary = audit_accounting(public, phase, plan)
    frozen = read(public / 'inputs.json');prior = read(root / 'data/night-002-split004/native-call-time.json')
    need(prior['experiment_id'] == 'MECH-004-SPLIT-R0' and prior['terminal_closed'] is True and
         prior['scientific_series_complete'] is False and prior['complete_accounting'] is True and
         prior['planned_jobs'] == 545 and prior['calls'] == 257 and
         file_hash(root / 'data/night-002-split004/native-call-time.json', normalized=True) == frozen['prior_native_call_budget_sha256'] and
         prior['sum_native_elapsed_seconds'] == frozen['prior_native_call_seconds'], 'Closed first-study call charges differ')
    calls = summary['native_call_budget']
    need(calls['unresolved_claims'] == 0 and calls['limit_seconds'] == 3600 and
         number(calls['recorded_native_call_seconds']) and 0 < calls['recorded_native_call_seconds'] <= 3600 and
         calls['resulting_bound_seconds'] == calls['recorded_native_call_seconds'], 'Final call envelope differs')
    own_public_seconds = sum(r['native_elapsed_seconds'] for r in data)
    if phase == 'technical':
        negative_seconds = calls['recorded_native_call_seconds'] - frozen['prior_native_call_seconds'] - own_public_seconds
        need(0 < negative_seconds <= 40, 'Negative call elapsed is missing/outside envelope')
    else:
        tech_calls = read(public / 'technical-summary.json')['native_call_budget']['recorded_native_call_seconds']
        compare(calls['recorded_native_call_seconds'], tech_calls + own_public_seconds, 'final cumulative call seconds')
    result = dict(phase=phase, public_subset_verified=True, private_raw_evidence_verified=False,
                  native_start_authorized=False, match_rows=len(data), reviewer_native_starts=0)
    if phase == 'technical':
        indexed = {r['job_id']: r for r in data};aa = summary['aa_pairs']
        need(len(aa) == 16 and len({(v['context'], v['side'], v['arm']) for v in aa}) == 16,
             'Technical A/A coverage differs')
        for pair in aa:
            h, side, arm = pair['context'], pair['side'], pair['arm'];prefix = f'tech-{h}-s{side}-{arm}-r'
            left, right = indexed[prefix+'0'], indexed[prefix+'1']
            need(all(left[k] == right[k] for k in ('result', 'native_audit', 'descriptive', 'descriptive_missing_reasons')) and
                 pair['exact_outcomes_and_identified_fields_equal'] is True and HASH.fullmatch(pair['raw_state_sha256']) and
                 pair['result_sha256'] == canonical(dict(seed=left['seed'], **left['result'])), 'Technical A/A outcomes/descriptors differ')
        result['exact_public_aa_pairs'] = 16
    elif (public / 'effects.json').exists():
        result.update(verify_stored_analysis(data, receipt, read(public / 'effects.json'), read(public / 'seed-contrasts.jsonl')))
        provenance = read(public / 'analysis-provenance.json');registered = receipt['config']['preregistration']
        need(provenance['experiment_id'] == EXPERIMENT and provenance['native_calls'] == 0 and
             provenance['preregistration_commit'] == registered['commit'] and
             provenance['frozen_analysis_sha256'] == registered['analysis_sha256'] and
             provenance['command'] == 'python -B analysis/report_stless003.py', 'Analysis provenance identity differs')
        for name, field in (('main.jsonl', 'main_rows_sha256'), ('manifest.json', 'manifest_sha256'),
                ('effects.json', 'effects_sha256'), ('seed-contrasts.jsonl', 'seed_contrasts_sha256')):
            need(file_hash(public / name, normalized=True) == provenance[field], 'Analysis provenance artifact hash differs')
        need(file_hash(root / 'analysis/report_stless003.py', normalized=True) == provenance['report_source_sha256'],
             'Analysis report source differs')
        archived = subprocess.check_output(['git', 'show', registered['commit'] + ':analysis/analyse_stless003.py'], cwd=root)
        need(sha256(archived.replace(b'\r\n', b'\n')).hexdigest() == provenance['frozen_analysis_sha256'],
             'Original registered analysis source hash differs')
        result['analysis_provenance_verified'] = True
    return result


def audit_claim_envelopes(local, phase, ledger, baseline):
    """Replay claims/completions in immutable lock-serialized concurrency order."""
    indexed = {r['job_id']: r for r in ledger};active = set();done = set();recorded = baseline;claims = 0
    for event in read(local / phase / 'dispatch/concurrency.jsonl'):
        key = event['job_id'];kind = event['event']
        if kind == 'claimed':
            need(key in indexed and key not in active and key not in done, 'Unexpected/duplicate admitted claim')
            proof = read(local / phase / 'call-admissions' / (key + '.json'))
            need(proof['job_id'] == key and proof['unresolved_claims'] == len(active) and
                 proof['new_claim_envelope_seconds'] == 40 and proof['limit_seconds'] == 3600,
                 'Claim envelope identity/reservation differs')
            compare(proof['recorded_native_call_seconds'], recorded, 'claim recorded elapsed')
            compare(proof['resulting_bound_seconds'], recorded+40*(len(active)+1), 'claim inflight bound')
            need(proof['resulting_bound_seconds'] <= 3600 and len(active) < 4, 'Claim exceeds mission call bound')
            active.add(key);claims += 1
        elif kind == 'completed':
            need(key in active and key not in done, 'Unexpected/duplicate completed claim')
            elapsed = indexed[key]['native_elapsed_seconds']
            need(number(elapsed) and 0 < elapsed <= 40, 'Actual call exceeds claimed envelope')
            recorded += elapsed;active.remove(key);done.add(key)
        else:need(False, 'Failed/stopped concurrency trace')
        need(event['active_claims'] == len(active), 'Concurrency claim count differs')
    need(not active and done == set(indexed) and recorded <= 3600, 'Unreconciled/exceeded final call total')
    return dict(claims=claims, actual_cumulative_seconds=recorded,
                admission_bounds_replayed=True, absolute30second_policy_source_bound=True)


def audit_private(root, phase):
    """Existing file evidence only. Low-level input audit reuse is explicit."""
    from analysis.stless003_design import audit_job
    from analysis.startpolicy002_gate import repeat_equivalence
    from analysis.run_startpolicy002 import audit_malformed
    from research.native_process005 import confirmed_cleanup
    root = Path(root);public = root / 'data/night-002-stless003';local = root / 'local/night-002/stless003'
    report = audit_public(root, phase);frozen = read(public / 'inputs.json');receipt = read(public / 'manifest.json')
    for name, wanted in frozen['code_sha256'].items():
        path = (root / name).resolve()
        need(path.is_relative_to(root.resolve()) and file_hash(path, normalized=True) == wanted,
             'Private frozen source changed')
    tree=ast.parse((root/'analysis/run_stless003.py').read_text(encoding='utf8'))
    calls=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and
           isinstance(node.func,ast.Name) and node.func.id=='contained_call']
    need(len(calls)==1, 'Exactly one source-bound native containment call required')
    keywords={item.arg:item.value for item in calls[0].keywords}
    need(ast.dump(keywords['total_timeout'])==ast.dump(ast.parse('min(allowance,30)',mode='eval').body) and
         ast.literal_eval(keywords['max_processes'])==3 and ast.literal_eval(keywords['timeout'])==90,
         'Source-bound absolute30second/Job3 containment policy differs')
    plan = read(public / (phase + '-job-plan.json'));rows = read(local / phase / 'dispatch/ledger.jsonl')
    need(len(rows) == len(plan) and len({r['job_id'] for r in rows}) == len(rows), 'Private ledger coverage differs')
    indexed = {r['job_id']: r for r in rows};configs = read(local / 'configs.json')
    catalog = read(root / 'local/runtime-v1114.6/source/tactics_ui/catalog.json');logs = {};negative = 0
    for job in plan:
        key = job['key'];row = indexed[key];directory = local / phase / 'jobs' / key
        for name, field in (('native.stdout', 'stdout_sha256'), ('native.jsonl', 'raw_log_sha256'),
                ('native.containment.json', 'containment_receipt_sha256')):
            need(file_hash(directory / name) == row[field], 'Private artifact hash differs')
        need(confirmed_cleanup(directory / 'native.stdout', expected_limit=3) and not (directory / 'pending.json').exists(),
             'Private cleanup unconfirmed')
        evidence = read(directory / 'native.jsonl');logs[key] = evidence
        if job.get('kind') == 'negative':
            need(row['status'] == 'expected_rejection' and row['returncode'] == 108, 'Negative native exit differs')
            audit_malformed(evidence, 108);negative += 1;continue
        need(file_hash(directory / 'input.json') == row['input_dump_sha256'], 'Private input dump hash differs')
        payload = (local / 'inputs' / f"{job['scenario']}-{job['side']}-{job['arm']}.bin").read_bytes()
        need(sha256(payload).hexdigest() == row['setup_sha256'], 'Private input setup hash differs')
        actual = audit_job(evidence, read(directory / 'input.json'), dict(job, identity=frozen['identity'],
            config_sha256=receipt['config_sha256'], setup_sha256=row['setup_sha256']), payload,
            configs[f"{job['scenario']}-{job['side']}"][job['arm']], catalog, frozen['oop_map'],
            frozen['frozen_controls'][f"{job['scenario']}-{job['side']}"], frozen['observer_host_sha256'])
        for field in ('result', 'native_audit', 'descriptive', 'descriptive_missing_reasons'):
            need(row[field] == actual[field], 'Private reconstructed observation differs')
    need(read(public / ('technical.jsonl' if phase == 'technical' else 'main.jsonl')) ==
         [r for r in rows if r['status'] == 'ok'], 'Public/private ledger rows differ')
    if phase == 'technical':
        need(negative == 1, 'Private negative coverage differs');aa = []
        for h, side, arm in product(CONTEXTS, (0, 1), ARMS):
            prefix = f'tech-{h}-s{side}-{arm}-r'
            aa.append(dict(context=h, side=side, arm=arm,
                **repeat_equivalence(logs[prefix+'0'], logs[prefix+'1'], indexed[prefix+'0']['seed'])))
        order = lambda v: (v['context'], v['side'], v['arm'])
        need(sorted(aa, key=order) == sorted(read(public / 'technical-summary.json')['aa_pairs'], key=order),
             'Actual identified-state A/A provenance differs')
    need(not (root / 'local/global-native/native-execution.lease.json').exists(), 'Global native lease retained')
    public_budget = read(public / (phase + '-budget.json'));snapshot = local / (phase + '-budget.snapshot.json')
    state = read(snapshot);proof = read(local / (phase + '-reconciled.json'))
    need(file_hash(snapshot) == proof['budget_sha256'] == public_budget['budget_sha256'] and
         proof['completed_utc'] == public_budget['completed_utc'] and state['experiment'] == EXPERIMENT and
         state['active'] is None and state['halted'] is False and
         state['charged_seconds'] == public_budget['charged_seconds'], 'Private budget reconciliation differs')
    for actual, safe in zip(state['operations'], public_budget['operations'], strict=True):
        need(all(actual[k] == v for k, v in safe.items()), 'Private/public operation differs')
    outer = read(root / 'local/night-002/program-budget.json')
    need(outer['experiment'] == 'NIGHT-002' and outer['active'] is None and outer['halted'] is False and
         outer['limits'] == {'technical': 192, 'main': 2048} and outer['limit_seconds'] == 3600 and
         0 < outer['charged_seconds'] <= 3600 and outer['absolute_deadline_utc'] == '2026-11-15T07:00:00+00:00',
         'Private outer mission budget differs')
    relevant = [op for op in outer['operations'] if op['name'] == EXPERIMENT + '/' + phase]
    need(len(relevant) == 1 and relevant[0]['returncode'] == 0 and relevant[0]['timed_out'] is False and
         relevant[0]['keys'] == [EXPERIMENT + ':' + j['key'] for j in plan], 'Private outer phase reservation differs')
    baseline = frozen['prior_native_call_seconds']
    if phase == 'main':
        technical = read(local / 'technical/dispatch/ledger.jsonl')
        need(len(technical) == 33 and all(r['status'] in ('ok', 'expected_rejection') for r in technical),
             'Prior technical call accounting incomplete')
        baseline += sum(r['native_elapsed_seconds'] for r in technical)
    report['call_admission_replay'] = audit_claim_envelopes(local, phase, rows, baseline)
    compare(report['call_admission_replay']['actual_cumulative_seconds'],
            read(public / (phase + '-summary.json'))['native_call_budget']['recorded_native_call_seconds'],
            'private final actual call total')
    report.update(private_raw_evidence_verified=True, low_level_input_audit_reused=True,
                  private_matches_reaudited=len(rows)-negative, private_negative_rejections=negative)
    return report


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('public-technical', 'public-main', 'private-technical', 'private-main'))
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args();access, phase = args.mode.split('-')
    print(json.dumps((audit_private if access == 'private' else audit_public)(args.root, phase), indent=2))

"""Independent read-only round-3 checks; no project analysis/runner/stats imports.

Only own JSON, public numeric rows, static source text and explicitly addressed
private artifacts are read. No native process, server, registry or save decoder.
"""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
import importlib.metadata
import json
import math
from pathlib import Path
import statistics
import struct
import sys

import numpy as np
from scipy.stats import chi2, nct, t

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CONTEXTS = ('high_press', 'deep_block')
ARMS = ('OJ', 'OA', 'OP', 'SJ', 'SA', 'SP')
ENDPOINTS = ('xgd', 'points', 'gf', 'ga', 'xgf', 'xga')
BOOT_SEED = int.from_bytes(sha256(b'ATTR-009-Bridge/bootstrap-v1').digest()[:8], 'little')
POSITIONS = {'GK': 0, 'SW': 1, 'DL': 2, 'DCL': 3, 'DCR': 3, 'DR': 4,
             'DML': 5, 'DMR': 5, 'ML': 6, 'MCL': 7, 'MCR': 7, 'MR': 8,
             'AML': 9, 'AMC': 10, 'AMR': 11, 'ST': 12, 'WBL': 13, 'WBR': 14}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def rows(path):
    return [json.loads(line) for line in Path(path).read_text(encoding='utf8').splitlines() if line.strip()]


def hash_file(path, normalized=False):
    raw = Path(path).read_bytes()
    return sha256(raw.replace(b'\r\n', b'\n') if normalized else raw).hexdigest()


def canonical_hash(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def records(path):
    payload = Path(path).read_bytes()
    need(payload[:8] == b'FM27CFG1' and len(payload) >= 12, 'Scenario grammar/header')
    count = int.from_bytes(payload[8:12], 'little')
    need(len(payload) == 12 + count * 20, 'Scenario length')
    parsed = tuple(struct.iter_unpack('<5I', payload[12:]))
    rebuilt = b'FM27CFG1' + struct.pack('<I', count) + b''.join(struct.pack('<5I', *r) for r in parsed)
    need(rebuilt == payload, 'Independent binary roundtrip')
    return payload, parsed


def training_archive():
    """Direct rational arithmetic on all 660 original rows, never training002."""
    folder = ROOT / 'data/training'
    data = rows(folder / 'player-deltas.jsonl')
    keys = [(r['trial'], r['cohort'], r['subject'], r['checkpoint'], r['arm']) for r in data]
    need(len(data) == len(set(keys)) == 660, 'Training archive count/duplicates')
    exposure = read(folder / 'exposure.json')
    contrasts = []
    for trial, week, control, intervention in [('conditioning-heavy', 6, 'A', 'B'), ('conditioning-rest', 4, 'A', 'C')]:
        values = {}
        for arm in (control, intervention):
            sample = [r for r in data if (r['trial'], r['checkpoint'], r['arm']) == (trial, week, arm)]
            need(len(sample) == 22 and len({r['subject'] for r in sample}) == 22, 'Archive cohort')
            raw_sum = sum(Fraction(r['delta']['raw'][k]) for r in sample for k in ('acceleration', 'pace', 'agility', 'stamina'))
            values[arm] = (raw_sum / 88, sum(Fraction(r['delta']['ca']) for r in sample) / 22)
        endpoint = [r for r in exposure[trial] if r['checkpoint'] == week]
        need(len(endpoint) == 1, 'Cumulative exposure endpoint')
        contrasts.append(dict(trial=trial, week=week,
            index_difference_raw=float(values[intervention][0] - values[control][0]),
            ca_difference=float(values[intervention][1] - values[control][1]),
            index_fraction=str(values[intervention][0] - values[control][0]),
            exposure={a: dict(match_minutes=endpoint[0]['arms'][a]['recorded_minutes'],
                              injury_entries=endpoint[0]['arms'][a]['injury_events']) for a in (control, intervention)}))
    published = read(ROOT / 'data/train-002-technical/archive-diagnostic.json')
    for direct, exported in zip(contrasts, published['exploratory_descriptions'], strict=True):
        for key in ('index_difference_raw', 'ca_difference'):
            need(math.isclose(direct[key], exported[key], abs_tol=1e-12), 'Training independent arithmetic')
        need(direct['exposure'] == exported['observed_exposure_aggregates'], 'Training endpoint exposure')
    return dict(player_rows=660, trial_rows=dict(Counter(r['trial'] for r in data)),
                contrasts=contrasts, independent_replicates=None, individual_participation=None,
                injury_days=None, current_build_calibration=None)


def mech_baselines(central):
    """Independently parse full inputs and derive exact opt-in changes from lineup."""
    report = read(ROOT / 'data/mech-002/offline-report.json')
    results = []
    # Author codec is only the object under test; it performs no I/O/native import.
    from research.startpolicy import StartPolicy, encode_startpolicy, native_status
    need(native_status()['native_execution_allowed'] is False, 'MECH must stay blocked')
    for published in report['baselines']:
        payload, source = records(central / 'local/tact-002-r0/inputs' / published['name'])
        need(sha256(payload).hexdigest() == published['baseline_sha256'], 'MECH baseline hash')
        need(encode_startpolicy(source) == payload, 'MECH default identity')
        for side in (0, 1):
            need(encode_startpolicy(source, StartPolicy(side, 10000)) == payload, 'MECH full identity')
            lineup = {a: v for k, s, a, b, v in source if k == 11 and s == side}
            fieldplayers = {lineup[i] for i in range(1, 11)}
            expected = [((k, s, a, b, 7000) if k == 15 and s == side and a in fieldplayers and b in (16, 17)
                         else (k, s, a, b, v)) for k, s, a, b, v in source]
            binary = b'FM27CFG1' + struct.pack('<I', len(expected)) + b''.join(struct.pack('<5I', *r) for r in expected)
            need(binary == encode_startpolicy(source, StartPolicy(side, 7000)), 'MECH independent low codec')
            changed = [(a, b) for a, b in zip(source, expected, strict=True) if a != b]
            need(len(changed) == 20 and all(a[-1] == 10000 for a, _ in changed), 'MECH diff scope')
            need(sha256(binary).hexdigest() == published['sides'][side]['low_setup_sha256'], 'MECH low hash')
        results.append(dict(name=published['name'], sha256=sha256(payload).hexdigest(), records=len(source),
                            full_identical=True, low_changed_records_per_side=20))
    return results


def offline(central, game):
    expected = read(ROOT / 'data/mech-002/source-audit.json')['sha256']
    paths = {'engine_dll': game / 'fm_Data/Plugins/x86_64/game_plugin.dll',
             'native_host': central / 'local/runtime-v1114.6/engine/fm27_native/FM27Simulator.exe',
             'bundled_fixture': central / 'local/runtime-v1114.6/engine/fm27_native/fixtures/match.pkm'}
    identity = {}
    for name, path in paths.items():
        actual = hash_file(path)
        need(actual == expected[name], 'Current file identity drift: ' + name)
        identity[name] = actual
    resource_receipt = read(central/'docs/round3/identity.json')
    actual_resources = []
    for item in resource_receipt['resources']:
        name = item['path']
        path = game/'fm_Data/Plugins/x86_64'/Path(name).name if name == 'game_plugin.dll' or name.startswith('libs/') else game/name
        actual = hash_file(path)
        need(actual == item['sha256'], 'Resource file drift: ' + name)
        actual_resources.append(dict(path=name, sha256=actual))
    need(len(actual_resources) == 11 and canonical_hash(sorted(actual_resources, key=lambda r: r['path'])) == resource_receipt['resource_fingerprint'], 'Resource fingerprint')
    identity['resource_fingerprint'] = resource_receipt['resource_fingerprint']
    identity['catalog_sha256'] = hash_file(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json')
    need(identity['catalog_sha256'] == resource_receipt['sha256']['catalog'], 'Catalog identity')
    for name in ('fm27_tactics_server.py', 'fm27_profiles.py', 'desktop_execution.py',
                 'native/desktop_host.cpp', 'native/native_statistics.h', 'native/native_execution_experiment.h'):
        base = central / ('local/upstream/fm-tactics-lab' if name.startswith('native/') else 'local/runtime-v1114.6/source')
        need(hash_file(base / name) == expected[name], 'Inspected source drift: ' + name)
    package = importlib.metadata.distribution('fmsave')
    inventory = read(ROOT / 'data/train-002-technical/reader-inventory.json')
    need(package.version == inventory['version'] == '0.9.0', 'Reader version')
    for name, receipt in inventory['files'].items():
        need(hash_file(package.locate_file('fmsave') / name) == receipt['sha256'], 'Reader source drift')
    return dict(kind='independent_offline_preflight', identity=identity, fmsave=package.version,
                training=training_archive(), mech=mech_baselines(central),
                new_native_starts=0, seeds_reserved=0, career_advances=0,
                attr_native_released=False, mech_native_released=False, training_native_released=False)


def inference(strata, resamples=20000):
    """Two equally weighted contexts; seed-level complete side means."""
    need(len(strata) == 2 and all(len(x) >= 2 for x in strata), 'Two nonempty strata required')
    means = [statistics.mean(x) for x in strata]
    sd = [statistics.stdev(x) for x in strata]
    components = [s*s / len(x) / 4 for s, x in zip(sd, strata, strict=True)]
    variance = sum(components)
    mean = sum(means) / 2
    se = math.sqrt(variance)
    if se:
        df = variance**2 / sum(v*v/(len(x)-1) for v, x in zip(components, strata, strict=True))
        margin = float(t.ppf(.975, df)) * se
        p = float(2*t.sf(abs(mean/se), df))
    else:
        df, margin, p = None, 0., float(mean == 0)
    rng = np.random.default_rng(BOOT_SEED)
    bootstrap = np.zeros(resamples)
    for values in strata:
        array = np.asarray(values)
        indices = rng.integers(len(array), size=(resamples, len(array)))
        bootstrap += array[indices].mean(axis=1) / 2
    return dict(mean=mean, se=se, df=df, ci=[mean-margin, mean+margin], p=p,
                bootstrap_ci=np.quantile(bootstrap, [.025, .975]).tolist(),
                context_sd=sd, context_mean=means)


def holm5(probabilities):
    need(len(probabilities) == 5, 'Exactly five secondary tests')
    ordered = sorted(enumerate(probabilities), key=lambda pair: pair[1])
    corrected = [None] * 5
    maximum = 0.
    for rank, (index, p) in enumerate(ordered):
        need(math.isfinite(p) and 0 <= p <= 1, 'Invalid probability')
        maximum = max(maximum, min(1., (5-rank)*p))
        corrected[index] = maximum
    return corrected


def future_n(sd):
    def plan(scales, effect):
        def power(n):
            parts = [s*s/(4*n) for s in scales]
            variance = sum(parts)
            if not variance:
                return 1., 0.
            df = variance**2 / sum(v*v/(n-1) for v in parts)
            se = math.sqrt(variance)
            cutoff = t.ppf(.975, df)
            return float(nct.sf(cutoff, df, effect/se)+nct.cdf(-cutoff, df, effect/se)), float(2*cutoff*se)
        # A linear integer search independently verifies the author's binary minimum.
        for count in range(2, 10000001):
            achieved, width = power(count)
            if achieved >= .9:
                return dict(effect=effect, seeds_per_context=count, matches=24*count, power=achieved, full_width=width)
        raise ValueError('Planning search exhausted')
    upper = [s*math.sqrt(15/chi2.ppf(.025, 15)) for s in sd]
    return {name: [plan(scales, effect) for effect in (.2, .3)]
            for name, scales in [('observed', sd), ('simultaneous95_sd_upper', upper)]}


def raw_metrics(row):
    need(row.get('status') == 'ok' and row.get('engine_readback') is True, 'Failed/unverified row')
    side, score, stats = row['tested_side'], row['score'], row['team_statistics']
    need(type(side) is int and side in (0, 1) and len(score) == len(stats) == 2, 'Result shape')
    need(all(type(v) is int and v >= 0 for v in score), 'Goals invalid')
    for team in stats:
        need(all(type(team[k]) in (int, float) and math.isfinite(team[k]) for k in
                 ('xg', 'shots', 'shots_on_target', 'passes', 'completed_passes', 'possession')), 'Nonfinite result')
        need(team['xg'] >= 0 and 0 <= team['shots_on_target'] <= team['shots'] and
             0 <= team['completed_passes'] <= team['passes'] and 0 <= team['possession'] <= 1, 'Implausible result')
    need(abs(sum(s['possession'] for s in stats)-1) < 1e-6, 'Possession total')
    gf, ga = score[side], score[1-side]
    xgf, xga = stats[side]['xg'], stats[1-side]['xg']
    return (xgf-xga, 3 if gf > ga else int(gf == ga), gf, ga, xgf, xga)


def attr_results(directory):
    """Rebuild direct six-arm contrasts from raw scores/xG, without derived inputs."""
    directory = Path(directory)
    manifest = read(directory / 'manifest.json')
    config, seeds = manifest['config'], manifest['seeds']
    need(canonical_hash(config) == manifest['config_sha256'], 'Contract hash')
    need(len(seeds) == len(set(seeds)) == 32 and all(type(s) is int and s > 0 for s in seeds), 'Main seeds')
    expected = {(h, seed, side, arm) for j, h in enumerate(CONTEXTS) for seed in seeds[j*16:(j+1)*16]
                for side in (0, 1) for arm in ARMS}
    cells = {}
    for row in rows(directory / 'main.jsonl'):
        key = (row['scenario'], row['seed'], row['tested_side'], row['arm'])
        need(key in expected and key not in cells, 'Unexpected/duplicate main cell')
        h, seed, side, arm = key
        need(row['key'] == f'{h}-{seed}-{side}-{arm}', 'Main job key')
        need(row['setup_sha256'] == config['design']['setups'][h][str(side)][arm] and
             row['config_sha256'] == manifest['config_sha256'], 'Main setup/config')
        need(all(row.get(k) == v for k, v in config['identity'].items()), 'Main identity')
        need(0 < row['finish_tick'] < 47996, 'Natural completion')
        gates = dict(input_contract_verified=True, profile_fields_verified=1058, native_roles_verified=44,
                     native_pi_groups_verified=748, native_pi_cells_verified=44, native_raw_dose_verified=True)
        need(all(type(row.get(k)) is type(v) and row[k] == v for k, v in gates.items()), 'Native input gate')
        need(row['design_matrix_sha256'] == config['design']['matrix_sha256'], 'Matrix readback gate')
        cells[key] = raw_metrics(row)
    need(set(cells) == expected and len(cells) == 384, 'Incomplete blocks; no scientific analysis')
    all_blocks, by_endpoint = [], {m: [] for m in ENDPOINTS}
    for j, h in enumerate(CONTEXTS):
        strata = {m: [] for m in ENDPOINTS}
        for seed in seeds[j*16:(j+1)*16]:
            for k, endpoint in enumerate(ENDPOINTS):
                side_contrasts = []
                for side in (0, 1):
                    oj, oa, op, sj, sa, sp = [cells[h, seed, side, a][k] for a in ARMS]
                    side_contrasts.append((sj-(sa+sp)/2)-(oj-(oa+op)/2))
                value = sum(side_contrasts)/2
                strata[endpoint].append(value)
                all_blocks.append(dict(scenario=h, seed=seed, endpoint=endpoint, value=value))
        for endpoint in ENDPOINTS:
            by_endpoint[endpoint].append(strata[endpoint])
    effects = {m: inference(by_endpoint[m]) for m in ENDPOINTS}
    adjusted = holm5([effects[m]['p'] for m in ENDPOINTS[1:]])
    for endpoint, p in zip(ENDPOINTS[1:], adjusted, strict=True):
        effects[endpoint]['p_holm'] = p
    return dict(n_matches=384, independent_blocks=32, effects=effects,
                planning=future_n(effects['xgd']['context_sd']), blocks=all_blocks)


def one_event(data, name):
    found = [r for r in data if r.get('event') == name]
    need(len(found) == 1, 'Missing/duplicate event: ' + name)
    return found[0]


def attr_inputs(public, private, central):
    """Independent full-record input comparator and archive/registry seed audit."""
    public, private, central = map(Path, (public, private, central))
    contract, inputs, plan = [read(public/name) for name in ('contract.json', 'inputs.json', 'seed-plan.json')]
    original = read(central/'local/tact-001-p1b/configs.json')
    configs, manifest = read(private/'configs.json'), read(public/'mask-manifest.json')
    need(inputs['oop_map'] == [[0,1,2,3,4,9,5,6,7,8,10], [0,1,2,3,4,5,6,7,9,8,10]], 'Frozen OOP mapping')
    diffs = []
    for h in CONTEXTS:
        for side in (0, 1):
            base = original[f'{h}-{side}-D00']
            baseline_bytes, baseline_records = records(central/'local/tact-001-p1b/inputs'/f'{h}-{side}-D00.bin')
            for arm in ARMS:
                name = f'{h}-{side}-{arm}'
                expected = json.loads(json.dumps(base))
                need('away_tactic_pool' not in expected and 'experimental_execution' not in expected, 'Forbidden baseline key')
                changes = {}
                for logical in range(1, 11):
                    team = expected['teams'][side]
                    slot = team['lineup'][logical]
                    attrs = team['players'][slot]['attributes']
                    active = {POSITIONS[team['phases'][phase][logical]['position']] for phase in (0, 1)}
                    if arm[0] == 'S':
                        attrs[2:15] = [20 if i in active else 1 for i in range(2, 15)]
                    ability = {'J': 54, 'A': 49, 'P': 53}[arm[1]]
                    need(attrs[ability] == 60, 'Raw pre-dose')
                    attrs[ability] = 80
                    for i, (a, b) in enumerate(zip(base['teams'][side]['players'][slot]['attributes'], attrs, strict=True)):
                        if a != b:
                            changes[1, side, slot, i] = (a, b)
                need(configs[name] == expected, 'Full independent config differs: '+name)
                payload, actual = records(private/'inputs'/(name+'.bin'))
                expected_records = []
                for record in baseline_records:
                    expected_records.append((*record[:4], changes[record[:4]][1]) if record[:4] in changes else record)
                need(tuple(expected_records) == actual, 'Undeclared full binary record: '+name)
                need(len(actual) == 5557 and payload[:12] == baseline_bytes[:12], 'Record/header count')
                need(sha256(payload).hexdigest() == inputs['setups'][h][str(side)][arm] == contract['design']['setups'][h][str(side)][arm], 'Frozen input hash')
                declared = {(1, r['side'], r['roster_slot'], r['attribute']): (r['before'], r['after']) for r in manifest[name]['changes']}
                need(declared == changes, 'Declared mask change differs')
                for logical, binding in enumerate(manifest[name]['bindings']):
                    team = base['teams'][side]
                    need(binding['logical_slot'] == logical and binding['roster_slot'] == team['lineup'][logical] and
                         binding['ip_native_slot'] == logical and binding['oop_native_slot'] == inputs['oop_map'][side][logical], 'Manifest binding')
                    need(binding['active_rating_families'] == sorted({POSITIONS[team['phases'][p][logical]['position']] for p in (0, 1)}), 'Manifest active family')
                diffs.append(len(changes))
    used = {0}
    def collect(value, active=False):
        if isinstance(value, dict):
            for key, item in value.items():
                collect(item, active or key in ('seed', 'seeds', 'validation_seeds', 'effective_seed'))
        elif isinstance(value, list):
            for item in value:
                collect(item, active)
        elif active and type(value) is int:
            used.add(value)
    scanned = 0
    def scan(path):
        nonlocal scanned
        candidates = [path] if path.is_file() else list(path.rglob('*.json*'))
        for file in candidates:
            if file.suffix == '.json':
                collect(read(file)); scanned += 1
            elif file.suffix == '.jsonl':
                for row in rows(file):
                    collect(row)
                scanned += 1
    for folder in (central/'data').iterdir():
        if folder.is_dir() and folder.name != 'attr-009-bridge':
            scan(folder)
    for file in (central/'local/registry').glob('*.json'):
        if not file.name.startswith('ATTR-009-Bridge'):
            scan(file)
    for folder in (central/'local').iterdir():
        if folder.is_dir() and folder.name != 'attr-009-bridge' and folder.name.startswith(('valid', 'tact-', 'mech-', 'attr-', 'platform-smoke')):
            scan(folder)
    excluded = read(public/'excluded-seeds.json')
    need(set(excluded) == used and len(excluded) == len(used) == plan['excluded_seed_count'], 'Independent historical exclusion set')
    need(canonical_hash(sorted(used)) == plan['excluded_seed_set_sha256'], 'Exclusion hash')
    need(len(plan['seeds']) == len(set(plan['seeds'])) == 34 and not used.intersection(plan['seeds']), 'Fresh unique seeds')
    need(plan['seeds'] == plan['technical_seeds'] + plan['main_seeds'] and len(plan['technical_seeds']) == 2 and len(plan['main_seeds']) == 32, 'Seed phases')
    need(read(central/'local/registry/ATTR-009-Bridge.reserved.json') == plan, 'Reservation identity')
    for name, expected in contract['execution']['code_sha256'].items():
        need(hash_file(central/name, True) == expected, 'Frozen author code drift')
    for name, expected in contract['execution']['artifacts'].items():
        need(hash_file(public/name, True) == expected, 'Frozen public artifact drift')
    return dict(cells=24, records_per_cell=5557, min_attribute_changes=min(diffs), max_attribute_changes=max(diffs),
                undeclared_binary_changes=0, historical_seed_count=len(used), historical_json_files_scanned=scanned,
                fresh_main_seeds=32, fresh_technical_seeds=2, namespace_collision=False,
                full_matches_started_by_review=0, native_gate_passed=False)


def technical(public, private, central):
    """Read every actual technical log/dump, compare directly to frozen configs."""
    public, private = Path(public), Path(private)
    inputs, plan = read(public/'inputs.json'), read(public/'seed-plan.json')
    configs = read(private/'configs.json')
    catalog = read(central/'local/runtime-v1114.6/source/tactics_ui/catalog.json')
    roles = {r['id']: int(r['flags']) for r in catalog['roles']}
    positions = {r['id']: r['mask'] for r in catalog['positions']}
    pi_options = {int(g['id']): {o['id'] for o in g['options'] if o['id']} for g in catalog['player_instructions']}
    expected = {f'tech-{h}-{s}-{a}-r{repeat}': (h, s, a, plan['technical_seeds'][CONTEXTS.index(h)])
                for h in CONTEXTS for s in (0, 1) for a in ARMS
                for repeat in (range(2) if a in ('OJ', 'SJ') else range(1))}
    ledgers = [r for p in (private/'technical').glob('part-*/ledger.jsonl') for r in rows(p)]
    need(len(ledgers) == 32 and {r['key'] for r in ledgers} == set(expected), 'Technical coverage')
    for row in ledgers:
        h, side, arm, seed = expected[row['key']]
        name = f'{h}-{side}-{arm}'
        config = configs[name]
        raw_metrics(row)
        need(row['seed'] == seed and row['tested_side'] == side and row['arm'] == arm, 'Technical seed/binding')
        paths = list((private/'technical').glob('part-*/'+row['key']+'.jsonl'))
        need(len(paths) == 1, 'Technical log uniqueness')
        log = paths[0]
        need(hash_file(log) == row['raw_log_sha256'] and hash_file(log.with_suffix('.input.json')) == row['input_dump_sha256'], 'Evidence hash')
        evidence, dump = rows(log), read(log.with_suffix('.input.json'))
        need(not any(r.get('event') in ('native_execution_probe', 'experimental_engine_version') for r in evidence), 'Forbidden execution')
        receipt = one_event(evidence, 'native_scenario_readback_verified')
        need(receipt['after_original_preparation'] is True, 'After preparation required')
        payload, recs = records(private/'inputs'/(name+'.bin'))
        need(receipt['records'] == len(recs) and sha256(payload).hexdigest() == inputs['setups'][h][str(side)][arm], 'Native record/setup')
        need(len([r for r in recs if r[0] == 15]) == one_event(evidence, 'native_profile_bindings_verified')['fields'] == 1058, 'Profile field count')
        need(one_event(evidence, 'native_player_tactic_bindings_verified') == dict(event='native_player_tactic_bindings_verified', players=22, phases=2), 'Actual native binding')
        seed_receipt = one_event(evidence, 'native_input_seed')
        need(seed_receipt['override'] is True and seed_receipt['effective_seed'] == seed, 'Effective seed')
        finished = one_event(evidence, 'natural_match_finished')
        need(finished['full_match_completed'] is True and finished['tick'] == row['finish_tick'] and
             finished['score'] == row['score'], 'Natural native result')
        stats_receipt = one_event(evidence, 'native_match_statistics')
        need(stats_receipt['source'] == 'original_team_statistics', 'Native statistics source')
        for s, team_stats in enumerate(stats_receipt['teams']):
            need(team_stats['side'] == s and all(team_stats[k] == value for k, value in row['team_statistics'][s].items()), 'Native statistics values')
        # Direct raw profile decoding, independent of the host's success counter.
        tail_offsets = {9: (0xbb8, 4), 10: (0xbbc, 4), 19: (0x70, 1),
                        20: (0xca8, 1), 21: (0xca2, 1), 22: (0xca3, 1)}
        tail_offsets.update({field: (offset, 2) for field, offset in enumerate(
            (0xc98, 0xc8c, 0xc96, 0xc78, 0xc8a, 0xc90, 0xc7a, 0xc84), 11)})
        tail_offsets[1] = (0x79, 1)
        tail_offsets.update({field: (0x72+field-2, 1) for field in range(2, 9)})
        for kind, s, slot, field, value in recs:
            if kind != 15:
                continue
            player = dump['teams'][s]['players'][slot]
            if field == 0:
                need(bytes.fromhex(player['prefix_hex'])[0x6c:0x70] == struct.pack('<f', value/100), 'Native height profile')
            else:
                offset, length = tail_offsets[field]
                blob = bytes.fromhex(player['prefix_hex']) if offset < 0x80 else bytes.fromhex(player['input_tail_hex'])
                start = offset if offset < 0x80 else offset-0x4c5
                need(int.from_bytes(blob[start:start+length], 'little') == value, 'Native raw profile field')
        phases = [e for e in evidence if e.get('event') == 'native_phase_configuration']
        need(len(phases) == 4 and {(e['side'], e['phase']) for e in phases} == {(s, p) for s in (0, 1) for p in (0, 1)}, 'Actual phase receipt coverage')
        for phase_receipt in phases:
            s, phase = phase_receipt['side'], phase_receipt['phase']
            need(len(phase_receipt['players']) == 11, 'Actual phase players')
            for logical, actor in enumerate(phase_receipt['players']):
                cell = config['teams'][s]['phases'][phase][logical]
                native_slot = inputs['oop_map'][s][logical] if phase else logical
                native_pi = dump['teams'][s]['personal_instructions'][phase][native_slot]
                need(actor['slot'] == logical and actor['position'] == positions[cell['position']] and
                     int(actor['role']) == roles[cell['role']] | int(cell['duty']) and
                     actor['instruction_flags'] == native_pi['flags'], 'Actual MATCH_PLAYER phase binding')
        for s in (0, 1):
            observed, wanted = dump['teams'][s], config['teams'][s]
            need(observed['side'] == s and observed['count'] == 23 and len(observed['players']) == 23, 'Roster capacity')
            for observed_player, target in zip(observed['players'], wanted['players'][:23], strict=True):
                need(observed_player['id'] == target['native_id'] and observed_player['attributes'] == target['attributes'], 'All native attributes')
            for phase in (0, 1):
                for logical, cell in enumerate(wanted['phases'][phase]):
                    slot = inputs['oop_map'][s][logical] if phase else logical
                    blob = bytes.fromhex(observed['tactical_slots'][phase][slot])
                    need(struct.unpack_from('<I', blob)[0] == positions[cell['position']], 'Phase position')
                    need(struct.unpack_from('<Q', blob, 64)[0] == roles[cell['role']] | int(cell['duty']), 'Role/duty')
                    pi = observed['personal_instructions'][phase][slot]
                    need(pi['target_player'] == cell['target_player'] and pi['target_position'] == cell['target_position'], 'PI targets')
                    need(len(cell['instructions']) == 17, 'PI group coverage')
                    for group, choice in cell['instructions'].items():
                        active = {v for v in pi_options[int(group)] if int(pi['flags']) >> v & 1}
                        need(active == ({choice} if choice else set()), 'PI value')
        # Independent declared mask from logical positions and lineup, not author manifest.
        for logical in range(1, 11):
            team = config['teams'][side]
            slot = team['lineup'][logical]
            attrs = dump['teams'][side]['players'][slot]['attributes']
            active = {POSITIONS[team['phases'][phase][logical]['position']] for phase in (0, 1)}
            need(attrs[:2] == [0, 0], 'GK/Sweeper untouched')
            need(attrs[2:15] == [20 if arm[0] == 'O' or i in active else 1 for i in range(2, 15)], 'Independent mask union')
            need([attrs[i] for i in (54, 49, 53)] == [80 if arm[1] == a else 60 for a in 'JAP'], 'Independent raw dose')
    for h in CONTEXTS:
        for side in (0, 1):
            for arm in ('OJ', 'SJ'):
                pair = [r for r in ledgers if r['key'].startswith(f'tech-{h}-{side}-{arm}-')]
                need(len(pair) == 2 and all(pair[0][k] == pair[1][k] for k in ('score', 'finish_tick', 'team_statistics', 'setup_sha256', 'seed')), 'A/A repeat')
    negative = read(private/'negative-attempt.json')
    need(negative['status'] == 'expected_rejection' and negative['returncode'] == 108, 'Negative rejection')
    need(hash_file(private/'negative.jsonl') == negative['raw_log_sha256'], 'Negative log hash')
    need(not any(r.get('event') == 'natural_match_finished' for r in rows(private/'negative.jsonl')), 'Negative natural finish')
    startups = list((private/'technical').glob('part-*/worker_sessions/*/startup_receipt.json'))
    need(len(startups) == 4, 'Four actual worker startups')
    hashes = set()
    for path in startups:
        receipt = read(path)
        need(receipt['host_sha256'] == inputs['identity']['adapter_host_sha256'] and
             receipt['dll_sha256'] == inputs['identity']['engine_sha256'], 'Worker host/engine startup')
        hashes.add(hash_file(path))
        lifetime = read(path.with_name('lifetime.json'))
        need(lifetime['returncode'] == 0 and lifetime['completed'] == lifetime['expected'] == 8 and lifetime['failure'] is None, 'Worker completion')
    need({r['startup_receipt_sha256'] for r in ledgers} == hashes, 'All worker startup evidence bound')
    return dict(matches=32, readback_cells=24, exact_aa_pairs=8, negative_exit=108,
                native_attribute_values=32*46*69, profile_fields=32*1058, phase_cells=32*44,
                pi_groups=32*748, independent_native_execution=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=('offline', 'inputs', 'technical', 'results'))
    parser.add_argument('--public', type=Path, default=ROOT/'data/attr-009-bridge')
    parser.add_argument('--central', type=Path, default=ROOT)
    parser.add_argument('--game', type=Path)
    parser.add_argument('--private', type=Path)
    args = parser.parse_args()
    if args.phase == 'offline':
        parser.error('--game is required for offline identity checks') if args.game is None else None
        result = offline(args.central, args.game)
    elif args.phase == 'inputs':
        result = attr_inputs(args.public, args.private or args.central/'local/attr-009-bridge', args.central)
    elif args.phase == 'technical':
        result = technical(args.public, args.private or args.central/'local/attr-009-bridge', args.central)
    else:
        result = attr_results(args.public)
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, indent=2))


if __name__ == '__main__':
    main()

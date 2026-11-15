"""Pinned external RCA software audit; never measures actual FM27 CA costs."""
import argparse
import copy
import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = ('https://raw.githubusercontent.com/shlk20/fm27-scout-code/'
              '084d7f0a18ac790d7c4087c5b6bdff008186d4fa/apps/desktop/src/lib/ca.ts')
SOURCE_SHA = '13fe8593b297f0ea5047967ed75c08b71118f730bbb63f48f9db344f1982721b'
PROFILE_SHA = '31c1efc4da93fb23ec380b8a6e6c3b5956fb3290e5a51bc39d836bb1fc42f3b9'
FAMILIES = ('gk', 'dl', 'dc', 'wbl', 'dm', 'ml', 'mc', 'aml', 'amc', 'stc')
TARGETS = ('acceleration', 'pace', 'jumping_reach', 'stamina', 'anticipation',
           'finishing', 'strength', 'agility', 'reflexes')
SLOTS = ('gk', 'sw', 'dl', 'dc', 'dr', 'dm', 'ml', 'mc', 'mr', 'aml', 'amc',
         'amr', 'stc', 'wbl', 'wbr')
FEET = ((5, 100), (50, 100), (100, 100))


class ExportQualityError(ValueError):
    def __init__(self, rows, failures):
        self.rows = rows
        self.failures = failures
        super().__init__('Export has missing or unverified numeric inputs')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def source_keys(path):
    data = Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest() != SOURCE_SHA:
        raise ValueError('Pinned calculator hash mismatch')
    table = data.decode().split('const ATTRIBUTE_WEIGHTS:')[1].split('\n};', 1)[0]
    keys = re.findall(r'^  (\w+): \[', table, re.M)
    if len(keys) != 40 or len(set(keys)) != 40:
        raise ValueError('Unexpected attribute schema')
    return keys


def request(keys, family, feet, multi=False):
    positions = dict.fromkeys(SLOTS, 0)
    positions[family] = 20
    if multi:
        positions['dc' if family == 'mc' else 'mc'] = 20
    return dict(attributes=dict.fromkeys(keys, 60), positions=positions,
                left_foot=feet[0], right_foot=feet[1], position='AUTO')


def matrix(keys):
    requests, metadata = [], []
    for family in FAMILIES:
        for feet in FEET:
            for multi in (False, True):
                for attribute in TARGETS:
                    for level in (8, 12, 17):
                        before = request(keys, family, feet, multi)
                        before['attributes'][attribute] = level * 5
                        original_hash = digest(before)
                        after = copy.deepcopy(before)
                        after['attributes'][attribute] += 5
                        if digest(before) != original_hash:
                            raise ValueError('Original changed')
                        if any(before[k] != after[k] for k in before if k != 'attributes'):
                            raise ValueError('Control drift')
                        changed = [k for k in keys if before['attributes'][k] != after['attributes'][k]]
                        if changed != [attribute]:
                            raise ValueError('Not a single attribute intervention')
                        requests.extend((before, after))
                        metadata.append(dict(family=family.upper(), feet=list(feet),
                            additional_position=('DC' if family == 'mc' else 'MC') if multi else None,
                            attribute=attribute, from_level=level, to_level=level+1,
                            before_sha256=original_hash, after_sha256=digest(after)))
    return requests, metadata


def evaluate(source, requests):
    run = subprocess.run(['node', str(ROOT / 'analysis/run_rca002.mjs'), str(source.resolve())],
        input=json.dumps(requests, allow_nan=False), text=True, capture_output=True, check=True)
    values = json.loads(run.stdout)
    if len(values) != len(requests):
        raise ValueError('Missing source outputs')
    return values


def summarize(rows):
    if len(rows) != 1620 or len({r['after_sha256'] for r in rows}) != 1539:
        raise ValueError('Incomplete or duplicate intervention matrix')
    seen, unique = set(), []
    for row in rows:
        if row['after_sha256'] not in seen:
            unique.append(row)
        seen.add(row['after_sha256'])
    groups = {}
    for r in unique:
        key = (r['family'], tuple(r['feet']), r['additional_position'], r['attribute'])
        groups.setdefault(key, []).append(r['delta_model_rca'])
    deltas = [r['delta_model_rca'] for r in unique]
    base = [r for r in rows if r['feet'] == [5, 100] and r['additional_position'] is None]
    return dict(planned_cells=len(rows), interventions=len(unique), alias_repetitions=len(rows)-len(unique), unique_level_triplets=len(groups),
        level_dependent_triplets=sum(len(set(v)) > 1 for v in groups.values()),
        delta_range=[min(deltas), max(deltas)], zero_deltas=deltas.count(0),
        negative_deltas=sum(v < 0 for v in deltas),
        outputs_at_ceiling=sum(r['before']['estimated_ca'] == 200 or r['after']['estimated_ca'] == 200 for r in unique),
        source_iteration_counts=sorted({r[s]['iterations'] for r in rows for s in ('before', 'after')}),
        base_single_position_weakfoot5=[dict(position=r['family'], attribute=r['attribute'],
            level=r['from_level'], before=r['before']['estimated_ca'], after=r['after']['estimated_ca'],
            delta=r['delta_model_rca']) for r in base],
        uncertainty='Deterministic finite grid. No sampling CI; unknown transfer/model error.',
        actual_ca_costs_identified=False, editor_rca_gold_validated=False)


def normalize(s):
    return re.sub('[^a-z0-9]', '', s.lower())


def profiles(path, keys):
    blob = path.read_bytes()
    if hashlib.sha256(blob).hexdigest() != PROFILE_SHA:
        raise ValueError('Profile source hash mismatch')
    reader = csv.DictReader(io.StringIO(blob.decode('utf-8-sig')))
    headers = {normalize(h): h for h in reader.fieldnames}
    if len(headers) != len(reader.fieldnames):
        raise ValueError('Duplicate columns')
    rows, failures, seen = [], [], set()
    for number, row in enumerate(reader, 2):
        uid = row[headers['uniqueid']]
        if not uid or uid in seen:
            raise ValueError('Missing or duplicate player')
        seen.add(uid)
        try:
            attrs = {key: float(row[headers[normalize(key)]]) for key in keys}
            feet = [float(row[headers[name]]) for name in ('leftfoot', 'rightfoot')]
            ca = float(row[headers['ca']])
            if row[headers['position']] != 'GK' or not 1 <= ca <= 200:
                raise ValueError('Invalid position/CA')
            if any(not np.isfinite(x) or not 1 <= x <= 20 for x in [*attrs.values(), *feet]):
                raise ValueError('Invalid attribute/foot')
            req = request(keys, 'gk', [f*5 for f in feet])
            req['attributes'] = {k: v*5 for k, v in attrs.items()}
            rows.append(dict(request=req, ca=ca,
                split_key=hashlib.sha256(('PD-CA-001/player-split/v1:' + uid).encode()).hexdigest()))
        except (KeyError, ValueError) as exc:
            failures.append(dict(row_number=number, reason=str(exc)))
    if len(rows) != 109 or failures:
        raise ExportQualityError(len(seen), failures)
    return sorted(rows, key=lambda r: r['split_key'])


def metrics(errors):
    errors = np.asarray(errors)
    return dict(n=len(errors), mae=float(np.abs(errors).mean()),
        rmse=float(np.sqrt(np.square(errors).mean())), bias=float(errors.mean()),
        max_absolute_error=float(np.abs(errors).max()),
        fraction_within={str(k): float((np.abs(errors) <= k).mean()) for k in (1, 3, 5)})


def export_diagnostic(source, path, keys):
    try:
        rows = profiles(path, keys)
    except ExportQualityError as exc:
        return dict(evidence='BLOCKED_NUMERIC_FOOT_INPUT_UNAVAILABLE', rows=exc.rows,
            eligible_rows=0, failures=exc.failures, source_sha256=PROFILE_SHA,
            source_evaluations=0, mae=None, bias=None, conditional95_interval=None,
            reason='Feet are qualitative labels. No verified numeric mapping; no midpoint imputation.',
            actual_ca_costs_identified=False)
    outputs = evaluate(source, [r['request'] for r in rows])
    errors = np.array([o['estimated_ca']-r['ca'] for o, r in zip(outputs, rows, strict=True)])
    old = json.loads((ROOT / 'data/player-development-001-ca/profile-diagnostic.json').read_text())
    model = old['models']['W']['coefficients']
    # Reuse the original source weight parser; never refit the old proxy.
    from analysis.ca_efficiency001 import load_table
    table, _ = load_table(ROOT / 'local/player-development-001/sources/ca_costs.csv')
    weighted = [sum(w*r['request']['attributes'][normalize(a) if normalize(a) in keys else
        next(k for k in keys if normalize(k) == normalize(a))]/5 for a, w in table['GK'].items()) for r in rows]
    old_errors = np.array([model['intercept']+model['slope']*v-r['ca'] for v, r in zip(weighted, rows, strict=True)])
    difference = np.abs(errors[80:])-np.abs(old_errors[80:])
    draws = np.random.default_rng(2026111502).integers(29, size=(20000, 29))
    return dict(evidence='EXPLORATORY_PREVIOUSLY_SEEN_EXPORT_NOT_RCA_GOLD', rows=109, failures=[],
        source_sha256=PROFILE_SHA, full_export=metrics(errors), old29=metrics(errors[80:]),
        frozen_old_proxy_old29=metrics(old_errors[80:]),
        mae_difference_new_minus_old29=float(difference.mean()),
        conditional95_mae_difference=np.quantile(difference[draws].mean(axis=1), [.025, .975]).tolist(),
        bootstrap=dict(unit='previously seen diagnostic player', seed=2026111502, resamples=20000),
        assumptions=['raw=5*display', 'GK20; unknown secondary ratings assumed0',
                     'export CA is not RCA gold', 'no refit; old109 already seen'],
        actual_ca_costs_identified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--profiles', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    keys = source_keys(args.source)
    requests, rows = matrix(keys)
    results = evaluate(args.source, requests)
    seen = set()
    for i, row in enumerate(rows):
        row['before'], row['after'] = results[2*i:2*i+2]
        row['delta_model_rca'] = row['after']['estimated_ca']-row['before']['estimated_ca']
        row['repeated_request_alias'] = row['after_sha256'] in seen
        seen.add(row['after_sha256'])
    args.output.mkdir(parents=True, exist_ok=True)
    def write(name, value):
        (args.output/name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf8', newline='\n')
    (args.output/'model-interventions.jsonl').write_text(''.join(json.dumps(r, sort_keys=True)+'\n' for r in rows), encoding='utf8', newline='\n')
    write('summary.json', summarize(rows))
    write('manifest.json', dict(experiment='CA-002', source_url=SOURCE_URL, source_sha256=SOURCE_SHA,
        node=subprocess.check_output(['node', '--version'], text=True).strip(),
        attribute_keys=keys, constructed_profile=dict(all_other_attributes=60, raw_per_display=5,
        age='not an input', personality='not an input'), source_code_published=False,
        requests=len(requests), source_evaluations=2*len(requests), aa_mismatches=0,
        mutations=0, exclusions=0, native_calls=0, true_ca_cost_observations=0,
        model_matrix_sha256=hashlib.sha256((args.output/'model-interventions.jsonl').read_bytes()).hexdigest()))
    if args.profiles:
        write('export-diagnostic.json', export_diagnostic(args.source, args.profiles, keys))
    print(json.dumps({k: v for k, v in summarize(rows).items() if not isinstance(v, list)}))


if __name__ == '__main__':
    main()

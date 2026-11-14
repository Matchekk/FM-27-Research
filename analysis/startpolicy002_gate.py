"""Offline gates for original pre-preparation sharpness records, never a setter.

The historical codec and readonly observer are imported unchanged. Raw storage,
runtime cache transfer and actual football-performance effects remain distinct.
"""
from itertools import product

from research.passive_observer import canonical_hash, match_result, snapshot
from research.startpolicy import StartPolicy, decode_records, encode_records, encode_startpolicy, require

EXPERIMENT = 'MECH-002-STARTPOLICY-TECH-V1'
CONTEXTS = ('high_press', 'deep_block')
LEVELS = (10000, 7000)
REPEATS = (0, 1)
SCHEMA = 'fm27.startpolicy002.tech.v1'


def technical_keys():
    return [f'full-{context}-s{side}-sharp{level}-r{repeat}'
            for context, side, level, repeat in product(CONTEXTS, (0, 1), LEVELS, REPEATS)] + ['negative-malformed']


def jobs(seeds):
    require(type(seeds) is list and len(seeds) == 4 and len(set(seeds)) == 4 and
            all(type(s) is int and 0 < s <= 0xffffffff for s in seeds), 'Exactly four new uint32 seeds')
    full = [dict(key=f'full-{context}-s{side}-sharp{level}-r{repeat}', kind='full',
                 context=context, side=side, level_raw=level, repeat=repeat, seed=seeds[i])
            for i, (context, side) in enumerate(product(CONTEXTS, (0, 1)))
            for level, repeat in product(LEVELS, REPEATS)]
    return full + [dict(key='negative-malformed', kind='negative', seed=None)]


def compile_cell(payload, side, level):
    """Record-level encoding only; no in-place binary patch or native call."""
    source = decode_records(payload)
    require(len(source) == 5557, 'Only historical D00 complete record layout')
    require(not any(row[0] == 61 for row in source), 'Execution records forbidden')
    require(encode_records(source) == payload, 'Default codec changed baseline bytes')
    high = encode_startpolicy(source, StartPolicy(side, 10000))
    require(high == payload == encode_startpolicy(source), 'High/default byte identity failed')
    result = encode_startpolicy(source, StartPolicy(side, level))
    altered = decode_records(result)
    changes = [(before, after) for before, after in zip(source, altered, strict=True) if before != after]
    expected = 0 if level == 10000 else 20
    require(len(changes) == expected and all(a[:4] == b[:4] and a[0:2] == (15, side)
            and a[3] in (16, 17) and a[4] == 10000 and b[4] == 7000 for a, b in changes),
            'Unexpected intervention record differences')
    return result, dict(default_and_high_byte_identical=True, changed_records=len(changes),
                        record_count=len(source), execution_records=0)


def lineup_slots(payload):
    records = decode_records(payload)
    entries = [(s, a, v) for k, s, a, b, v in records if k == 11 and b == 0]
    lineups = {(s, a): v for s, a, v in entries}
    require(len(entries) == 22, 'Duplicate/missing absolute lineup record')
    require(set(lineups) == {(s, i) for s in (0, 1) for i in range(11)}, 'Complete absolute lineup required')
    require(all(len({lineups[s, i] for i in range(11)}) == 11 for s in (0, 1)), 'Duplicate starting slot')
    return lineups


def cache_bytes(player):
    require(player['statistics_cache_region_hex'] is not None, 'Starting actor runtime cache missing')
    raw = bytes.fromhex(player['statistics_cache_region_hex'])
    return raw[9], raw[10]  # Runtime stats +0x89 / +0x8a; sampled region starts +0x80.


def audit_start_state(evidence, baseline, side, level):
    """Run only after full native input + audit_trace gates; exact raw start gate.

    No finished-state clamp is required or introduced. All finish observations
    remain descriptive. Cache70 is not labelled calibrated career/UI sharpness.
    """
    require(type(side) is int and side in (0, 1) and type(level) is int and level in LEVELS, 'Unknown start arm')
    lineups = lineup_slots(baseline)
    affected = {lineups[side, i] for i in range(1, 11)}
    starters = {(s, lineups[s, i]) for s in (0, 1) for i in range(11)}
    captures = [row for row in evidence if row.get('event') == 'native_passive_state']
    require([r['stage'] for r in captures] == ['prepared', 'first_advance', 'finished'], 'Three captures required')
    checks = []
    for row in captures:
        players = snapshot(row)
        require({(p['side'], p['roster_index']) for p in players.values()} ==
                {(s, i) for s in (0, 1) for i in range(23)}, 'Only bundled23/23 rosters')
        if row['stage'] == 'finished':
            continue
        affected_count = 0
        for p in players.values():
            key = p['side'], p['roster_index']
            expected = level if p['side'] == side and p['roster_index'] in affected else 10000
            require(p['sharpness_raw'] == p['sharpness_secondary_raw'] == expected,
                    'Sharpness intervention did not survive original preparation/first advance')
            require(p['condition_raw'] == 10000 and p['fatigue_raw'] == 0 and
                    p['condition_accumulator_raw'] == 1000000 and p['sharpness_penalty_raw'] == 0,
                    'Uncontrolled initial condition/fatigue/accumulator/penalty')
            if key in starters:
                condition, sharpness = cache_bytes(p)
                require(condition == 100 and sharpness == (expected+50)//100,
                        'Actual starting actor cache89/8a does not carry the declared start state')
            affected_count += p['side'] == side and p['roster_index'] in affected
        require(affected_count == 10, 'Exactly ten target outfield actors required')
        checks.append(dict(stage=row['stage'], players_verified=46, changed_outfield_actors=10,
                           starter_caches_verified=22, target_cache8a=(level+50)//100,
                           capture_sha256=canonical_hash(row)))
    return dict(schema=SCHEMA, start_raw_and_cache_transfer_verified=True, captures=checks,
                postprep_setter_used=False, ongoing_clamp_used=False, execution_used=False,
                ui_scale_calibrated=False, causal_match_performance_released=False,
                scientific_main_released=False, career_released=False)


def repeat_equivalence(first, second, seed):
    require(match_result(first, seed) == match_result(second, seed), 'Exact A/A outcomes differ')
    def selected(evidence):
        values = []
        for row in evidence:
            if row.get('event') != 'native_passive_state':
                continue
            bound = snapshot(row)
            values.append(dict(stage=row['stage'], advance_ordinal=row['advance_ordinal'],
                tick_before=row['tick_before'], requested_target=row['requested_target'], tick=row['tick'],
                clock=row['clock'], seed=row['seed'], match_version_raw=row['match_version_raw'],
                players=[{k:p[k] for k in ('id', 'side', 'roster_index', 'condition_raw', 'sharpness_raw',
                    'sharpness_secondary_raw', 'fatigue_raw', 'condition_accumulator_raw',
                    'sharpness_penalty_raw', 'effectiveness_region_hex')} |
                    {'cache89_8a': cache_bytes(p) if p['statistics_cache_region_hex'] is not None else None}
                    for _, p in sorted(bound.items())]))
        return values
    left, right = selected(first), selected(second)
    require(len(left) == 3 and left == right, 'Identified raw-state A/A fields differ')
    return dict(exact_outcomes_and_identified_fields_equal=True,
                raw_state_sha256=canonical_hash(left), result_sha256=canonical_hash(match_result(first, seed)))


def initial_control_equivalence(high, low):
    """Raw TF33 equality only; zero bytes do not mean zero UI familiarity."""
    def selected(evidence):
        return {r['stage']: snapshot(r) for r in evidence if r.get('event') == 'native_passive_state'
                and r['stage'] in ('prepared', 'first_advance')}
    left, right = selected(high), selected(low)
    require(set(left) == set(right) == {'prepared', 'first_advance'}, 'Initial stage pair missing')
    for stage in left:
        require(set(left[stage]) == set(right[stage]), 'Identity changed between sharpness arms')
        for identity, p in left[stage].items():
            q = right[stage][identity]
            require(all(p[k] == q[k] for k in ('side', 'roster_index', 'condition_raw', 'fatigue_raw',
                    'condition_accumulator_raw', 'sharpness_penalty_raw', 'effectiveness_region_hex')),
                    'Initial non-sharpness control/raw TF33 differs')
    return dict(initial_control_fields_and_raw_tf33_equal=True,
                raw_tf33_has_no_validated_ui_familiarity_label=True)

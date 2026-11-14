"""Strict offline parser for an own passive host observer, never a release gate.

No server, native process, registry, game writer or UI imports. The offsets are
source-derived storage observations; engine consumer semantics remain separate.
"""
from hashlib import sha256
import json
from pathlib import Path
import struct
import math

VERSION = 'fm27.passive-observer.v1'
ENGINE = '8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340'
STAGES = ('prepared', 'first_advance', 'finished')
FIELDS = {'condition_raw': 0xc8a, 'sharpness_raw': 0xc90,
          'sharpness_secondary_raw': 0xc7a, 'fatigue_raw': 0xc84}
REGIONS = {'effectiveness_region_hex': (0xcba, 33),
           'runtime_near_morale_region_hex': (0x1df0, 0x70)}
EXTRA_FIELDS = {'condition_accumulator_raw': (0x1c74, 4), 'sharpness_penalty_raw': (0x1aa6, 2)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical_hash(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path):
    with Path(path).open('rb') as stream:
        from hashlib import file_digest
        return file_digest(stream, 'sha256').hexdigest()


def _int(value, low=0, high=0xffffffff):
    require(type(value) is int and low <= value <= high, 'Exact bounded integer required')


def _hex(value, size):
    require(type(value) is str and len(value) == 2*size and
            all(c in '0123456789abcdef' for c in value), 'Exact lowercase hex region required')
    return bytes.fromhex(value)


def read_rows(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    def constant(_):
        raise ValueError('Non-finite JSON constant')
    return [json.loads(line, object_pairs_hook=pairs, parse_constant=constant)
            for line in Path(path).read_text(encoding='utf8').splitlines() if line.strip()]


def snapshot(row):
    keys = {'event', 'schema', 'stage', 'advance_ordinal', 'tick_before', 'requested_target',
            'tick', 'clock', 'seed', 'match_version_raw', 'players'}
    require(type(row) is dict and set(row) == keys, 'Observer snapshot fields differ')
    require(row['event'] == 'native_passive_state' and row['schema'] == VERSION and
            row['stage'] in STAGES, 'Unknown observer schema/stage')
    for key in ('advance_ordinal', 'tick_before', 'requested_target', 'tick', 'seed', 'match_version_raw'):
        _int(row[key])
    _int(row['clock'], -0x80000000, 0x7fffffff)
    require(0 < row['seed'] and row['tick'] < 47996, 'Seed or native tick outside scope')
    require(type(row['players']) is list, 'Players array required')
    bound = {}; slots = {0: set(), 1: set()}
    for player in row['players']:
        require(type(player) is dict and set(player) == {'side', 'roster_index', 'id', *FIELDS, *REGIONS,
                                                       *EXTRA_FIELDS, 'statistics_cache_region_hex'},
                'Player observation fields differ')
        side, slot, identity = player['side'], player['roster_index'], player['id']
        _int(side, 0, 1); _int(slot, 0, 25); _int(identity, 1)
        require(identity not in bound and slot not in slots[side], 'Duplicate player or roster slot')
        bound[identity] = player; slots[side].add(slot)
        for key in FIELDS:
            _int(player[key], 0, 65535)
        for key, (_, length) in REGIONS.items():
            _hex(player[key], length)
        for key, (_, length) in EXTRA_FIELDS.items():
            _int(player[key], 0, 2**(8*length)-1)
        if player['statistics_cache_region_hex'] is not None:
            _hex(player['statistics_cache_region_hex'], 0x10)
        require(slot >= 11 or player['statistics_cache_region_hex'] is not None,
                'Current on-pitch runtime statistics cache unavailable')
    require(all(11 <= len(s) <= 26 and s == set(range(len(s))) for s in slots.values()),
            'Incomplete or unsupported roster capacity')
    return bound


def prepared_dump(dump):
    """Decode four actual actor fields and raw33 bytes from an existing input dump."""
    require(type(dump) is dict and type(dump.get('teams')) is list and len(dump['teams']) == 2,
            'Two-team private input dump required')
    bound = {}
    for side, team in enumerate(dump['teams']):
        _int(team['count'], 11, 26)
        require(team['side'] == side and type(team['side']) is int and
                team['count'] == len(team['players']) == 23, 'Only validated bundled23/23 context')
        for slot, player in enumerate(team['players']):
            _int(player['id'], 1)
            _int(player['index'], 0, 25)
            require(player['id'] not in bound and player['index'] == slot, 'Dump identity/index mismatch')
            tail = _hex(player['input_tail_hex'], 0x81b)
            observed = dict(side=side, roster_index=slot, id=player['id'])
            for key, offset in FIELDS.items():
                observed[key] = struct.unpack_from('<H', tail, offset-0x4c5)[0]
            observed['effectiveness_region_hex'] = tail[0xcba-0x4c5:0xcba-0x4c5+33].hex()
            bound[player['id']] = observed
    return bound


def audit_trace(evidence, dump, expected_seed, expected_records=5557, expected_version=0x1b000000):
    """Validate actual trace structure and cross-bind prepared bytes.

    Success is still NOT host/engine/consumer calibration or native release.
    A separate published16-match equivalence and provenance review is required.
    """
    _int(expected_seed, 1); _int(expected_records, 1); _int(expected_version, 1)
    require(type(evidence) is list and all(type(r) is dict for r in evidence), 'Event array required')
    forbidden = {'native_passive_observer_rejected', 'experimental_engine_version',
                 'native_execution_context_bound', 'native_execution_probe'}
    require(not any(row.get('event') in forbidden for row in evidence), 'Forbidden intervention/rejection event')
    def one(name):
        found = [(i, row) for i, row in enumerate(evidence) if row.get('event') == name]
        require(len(found) == 1, 'Missing/duplicate event: '+name)
        return found[0]
    seed_index, seed = one('native_input_seed')
    _int(seed['effective_seed'], 1)
    require(seed['override'] is True and seed['effective_seed'] == expected_seed, 'Uncontrolled seed')
    readback_index, readback = one('native_scenario_readback_verified')
    _int(readback['records'], 1)
    require(readback['after_original_preparation'] is True and readback['records'] == expected_records,
            'Missing original-preparation input proof')
    require(one('native_profile_bindings_verified')[1]['fields'] == 1058, 'Incomplete profile bindings')
    binding = one('native_player_tactic_bindings_verified')[1]
    require(binding['players'] == 22 and binding['phases'] == 2, 'Missing actual actor phase binding')
    captures = [(i, row) for i, row in enumerate(evidence) if row.get('event') == 'native_passive_state']
    require(len(captures) == 3 and [r['stage'] for _, r in captures] == list(STAGES), 'Three ordered captures required')
    bound = [snapshot(row) for _, row in captures]
    require(all(row['seed'] == expected_seed for _, row in captures), 'Snapshot seed mismatch')
    require(all(set(rows) == set(bound[0]) for rows in bound), 'Roster identity drift')
    for identities in bound:
        require(all(identities[i]['side'] == bound[0][i]['side'] for i in bound[0]), 'Cross-team identity drift')
    prepared, first, finished = [r for _, r in captures]
    require(seed_index < readback_index < captures[0][0], 'Prepared stage ordering differs')
    require(prepared['advance_ordinal'] == 0 and prepared['tick_before'] == prepared['tick'] == prepared['requested_target'],
            'Prepared snapshot falsely claims progress')
    require(first['advance_ordinal'] == 1 and first['tick_before'] == prepared['tick'] and
            first['requested_target'] == first['tick_before']+1 and first['tick'] > first['tick_before'],
            'Actual first tick-step1 call not proved')
    require(finished['advance_ordinal'] >= first['advance_ordinal'] and finished['tick'] >= first['tick'],
            'Finish precedes first advance')
    require(len({row['match_version_raw'] for _, row in captures}) == 1, 'Match version changed')
    require(prepared['match_version_raw'] == expected_version, 'Declared Kind62 match version not observed')
    finish_index, natural = one('natural_match_finished')
    require(finish_index > captures[2][0] and natural['full_match_completed'] is True and
            natural['tick'] == finished['tick'] and natural['clock'] == finished['clock'], 'Finish not naturally bound')
    expected = prepared_dump(dump)
    require(set(expected) == set(bound[0]), 'Prepared dump identity set differs')
    for identity, fields in expected.items():
        require(all(bound[0][identity][k] == v for k, v in fields.items()), 'Prepared profile/raw record differs')
    summary = []
    for stage, players in zip(STAGES, bound, strict=True):
        entry = dict(stage=stage, players=len(players),
                     profile_values=len(players)*len(FIELDS), raw_effectiveness_bytes=len(players)*33,
                     runtime_cache_players=sum(p['statistics_cache_region_hex'] is not None for p in players.values()),
                     capture_sha256=canonical_hash(next(r for _, r in captures if r['stage'] == stage)))
        entry['side'] = []
        for side in (0, 1):
            group = [p for p in players.values() if p['side'] == side]
            entry['side'].append(dict(side=side, count=len(group), **{
                k:dict(min=min(p[k] for p in group), max=max(p[k] for p in group),
                       mean=sum(p[k] for p in group)/len(group)) for k in FIELDS}))
        summary.append(entry)
    return dict(schema=VERSION, structurally_verified=True, captures=summary,
                identity_binding_verified=True, fields_are_raw_storage_observations=True,
                match_version_raw=prepared['match_version_raw'], sampler_version_threshold=0x1a080018,
                sampler_version_threshold_met=prepared['match_version_raw']>=0x1a080018,
                new_effectiveness_consumer_execution_proven=False,
                consumer_semantics_validated=False, ui_scale_calibrated=False,
                startpolicy_released=False, career_released=False, native_release_granted=False)


def match_result(evidence, expected_seed):
    """Exact observational equivalence target, without interpreting new raw fields."""
    def one(name):
        matches = [r for r in evidence if r.get('event') == name]
        require(len(matches) == 1, 'Missing/duplicate result event: '+name)
        return matches[0]
    seed = one('native_input_seed')
    _int(seed['effective_seed'], 1)
    require(seed['override'] is True and seed['effective_seed'] == expected_seed, 'Result seed mismatch')
    natural = one('natural_match_finished')
    _int(natural['tick'], 1, 47995); _int(natural['clock'], -0x80000000, 0x7fffffff)
    require(natural['full_match_completed'] is True and 0 < natural['tick'] < 47996,
            'Natural finish missing')
    require(type(natural['score']) is list and len(natural['score']) == 2, 'Two scores required')
    for value in natural['score']:
        _int(value, 0, 100)
    statistics = one('native_match_statistics')
    require(statistics['source'] == 'original_team_statistics' and
            [r['side'] for r in statistics['teams']] == [0, 1], 'Original statistics required')
    keys = ('xg', 'shots', 'shots_on_target', 'passes', 'completed_passes', 'possession', 'possession_ticks')
    teams = []
    for row in statistics['teams']:
        require(all(type(row[k]) in (int, float) and math.isfinite(row[k]) for k in keys), 'Nonfinite statistic')
        require(row['xg'] >= 0 and 0 <= row['shots_on_target'] <= row['shots'] and
                0 <= row['completed_passes'] <= row['passes'] and 0 <= row['possession'] <= 1,
                'Implausible statistic')
        teams.append({k:row[k] for k in keys})
    require(abs(sum(t['possession'] for t in teams)-1) < 1e-6, 'Possession sum differs')
    return dict(seed=expected_seed, score=natural['score'], tick=natural['tick'],
                clock=natural['clock'], team_statistics=teams)


def equivalence(evidence_by_mode, expected_seed):
    modes = ('reference', 'observer_off', 'observer_on', 'observer_on_repeat')
    require(type(evidence_by_mode) is dict and set(evidence_by_mode) == set(modes), 'Four fixed modes required')
    results = {mode:match_result(evidence_by_mode[mode], expected_seed) for mode in modes}
    require(all(value == results['reference'] for value in results.values()), 'Passive/default result drift')
    for mode in ('reference', 'observer_off'):
        require(not any(r.get('event') == 'native_passive_state' for r in evidence_by_mode[mode]),
                'Observer-off unexpectedly captured state')
    for mode in ('observer_on', 'observer_on_repeat'):
        observed = [r for r in evidence_by_mode[mode] if r.get('event') == 'native_passive_state']
        require([r['stage'] for r in observed] == list(STAGES), 'Observer-on capture coverage differs')
    a = [snapshot(r) for r in evidence_by_mode['observer_on'] if r.get('event') == 'native_passive_state']
    b = [snapshot(r) for r in evidence_by_mode['observer_on_repeat'] if r.get('event') == 'native_passive_state']
    for x, y in zip(a, b, strict=True):
        require(set(x) == set(y), 'A/A captured identities differ')
        for identity in x:
            require(all(x[identity][k] == y[identity][k] for k in (*FIELDS, *EXTRA_FIELDS, 'effectiveness_region_hex')),
                    'A/A identified raw fields differ')
            def cache(p):
                raw=p['statistics_cache_region_hex']
                return None if raw is None else bytes.fromhex(raw)[9:11]
            require(cache(x[identity]) == cache(y[identity]), 'A/A runtime cache bytes89/8a differ')
    return dict(result_equivalence_verified=True, modes=list(modes),
                result_sha256=canonical_hash(results['reference']), native_release_granted=False,
                interpretation='Four exact natural outcomes; full provenance/input/snapshot gates remain separate')


def instrument_source(source, enabled=True):
    """Small deterministic source transformation; source-disabled is byte-identical."""
    require(type(source) is str and type(enabled) is bool, 'Source text and explicit bool required')
    if not enabled:
        return source
    edits = (
        ('#include "native_execution_experiment.h"', '#include "native_execution_experiment.h"\n#include "passive_observer_v1.h"'),
        ('    source_generation_install(match);', '    passive_observer_options();\n    source_generation_install(match);'),
        ('    desktop_initial_state_snapshot(match);', '    desktop_initial_state_snapshot(match);\n    passive_observer_snapshot(match,"prepared",0,*(int*)(match+0x154ec),*(int*)(match+0x154ec));'),
        ('        if(flags&4){', '        if(flags&4){\n            passive_observer_snapshot(match,"finished",iteration,tick,tick);'),
        ('        if(after==tick){fprintf(log_file,"{\\"event\\":\\"native_match_stalled\\",\\"tick\\":%d}\\n",tick);fflush(log_file);desktop_finish_and_exit(91);}',
         '        if(after==tick){fprintf(log_file,"{\\"event\\":\\"native_match_stalled\\",\\"tick\\":%d}\\n",tick);fflush(log_file);desktop_finish_and_exit(91);}\n        if(iteration==0)passive_observer_snapshot(match,"first_advance",1,tick,target);'),
    )
    require('passive_observer_v1.h' not in source, 'Already instrumented; no repeated application')
    result = source
    for old, new in edits:
        require(result.count(old) == 1, 'Pinned source callsite drift')
        result = result.replace(old, new)
    return result

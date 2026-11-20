"""Bounded cold A/A and dose-readback acceptance for the released Steam host."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.coordination import NativeLease
from research.core import allocate, historical_seeds
from research.native import NativeLab, digest, event, read, require, rows, write
from research.startpolicy import decode_records

DOC = ROOT / 'docs/meta-validation-001'
PRIVATE = ROOT / 'local/meta-validation-001'
PLAN = DOC / 'technical-plan.json'
REG = ROOT / 'local/registry/META-VALIDATION-001-TECH.reserved.json'
HOST = 'e3a1cbf8a8678de3aa077fdb077d1b408680bb566293cecf70a003cbdb8dce07'
DLL = 'd12202dd01c3911d4c4e55e778f37b2251ffb10f9cf8cecc3b9ec08ece622c6b'
FIXTURE = '39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6'


def setups(server, settings):
    base = deepcopy(server.DEFAULT)
    base['match_importance'] = settings['importance']
    for team in base['teams']:
        team['roster_size'] = settings['roster_size']
    jr = next(a['id'] for a in server.CATALOG['attributes'] if a['name'] == 'JumpingReach')
    configurations = {}
    for position, slot in settings['technical_slots'].items():
        first_records = None
        for raw in settings['technical_raw_JR']:
            config = deepcopy(base)
            team = config['teams'][0]
            index = team['lineup'][slot]
            team['players'][index]['attributes'][jr] = raw
            config = server.validate_scenario(config)
            blob = server.encode_scenario(config, absolute=True)
            records = decode_records(blob)
            target = (1, 0, index, jr, raw)
            require(records.count(target) == 1, 'JR record absent or repeated')
            if first_records is None:
                first_records = records
            else:
                require([b for a,b in zip(first_records, records, strict=True) if a != b] == [target],
                        'More than the targeted JR dose changed')
            configurations[f'{position}-{raw}'] = (config, blob, {
                'position': position, 'slot': slot, 'jr_index': jr, 'raw': raw,
                'phase_positions': [phase[slot]['position'] for phase in team['phases']],
                'phase_roles': [phase[slot]['role'] for phase in team['phases']],
                'setup_sha256': hashlib.sha256(blob).hexdigest(),
            })
    return configurations


def reserve():
    require(not PLAN.exists() and not REG.exists(), 'Reservation already exists')
    used = historical_seeds(ROOT / 'data') | historical_seeds(REG.parent)
    def collect(value, active=False):
        if isinstance(value, dict):
            for key, sub in value.items():
                collect(sub, active or 'seed' in key.lower())
        elif isinstance(value, list):
            for item in value:
                collect(item, active)
        elif active and type(value) is int:
            used.add(value)
    for path in [*REG.parent.glob('*.json'), *(ROOT / 'data').rglob('*seed*.json')]:
        collect(read(path))
    name = 'META-VALIDATION-001/technical-B'
    seeds = allocate(name, 1, used)
    with REG.open('x', encoding='utf8') as f:
        json.dump(dict(namespace=name, seeds=seeds, prior_unique=len(used)), f)
    return seeds[0]


def run_one(server, engine, fixture, directory, name, config, blob, cell, seed):
    from desktop_warm_batch import DesktopWarmRunner, inspect_saved_run
    directory.mkdir(exist_ok=False)
    binary = directory / 'setup.bin'
    binary.write_bytes(blob)
    task = dict(variant=name, seed=seed, scenario=config, config=binary, path=directory/'raw.jsonl',
                dump=directory/'input.json', fixture=fixture, event_details=False,
                position_names={p['mask']:p['id'] for p in server.POSITIONS.values()})
    runner = DesktopWarmRunner(engine, workers=1, retries=0, timeout=90)
    calls = []
    try:
        runner.run([task], calls.append)
    finally:
        write(directory/'callbacks.json', calls)
        write(directory/'sessions.json', runner.session_diagnostics)
    require(len(calls) == 1 and calls[0].get('verified') is True, 'Incomplete native call')
    r = calls[0]
    require(r['engine_dll_sha256'] == DLL and r['collector_sha256'] == HOST, 'Provenance mismatch')
    checked = inspect_saved_run(directory, r, config)
    require(checked['seed']['override'] and checked['seed']['effective_seed'] == seed, 'Seed mismatch')
    evidence = rows(task['path'])
    receipt = event(evidence, 'native_scenario_readback_verified')
    require(receipt['after_original_preparation'] and receipt['records'] == len(decode_records(blob)),
            'Incomplete prepared readback')
    bindings = event(evidence, 'native_player_tactic_bindings_verified')
    require((bindings['players'],bindings['phases']) == (22,2), 'Lineup mismatch')
    auditor = NativeLab.__new__(NativeLab)
    auditor.server = server
    auditor.audit_dump(task['dump'], config)
    ps = event(evidence, 'native_profile_bindings_verified')['fields']
    st = event(evidence, 'native_match_statistics')
    require(st['source'] == 'original_team_statistics', 'Unexpected statistics source')
    require(len(runner.session_diagnostics) == 1 and not runner.session_diagnostics[0].get('warning'),
            'Worker cleanup unconfirmed')
    return dict(key=name, seed=seed, side=0, **cell, score=checked['result']['score'],
                tick=checked['result']['tick'], xg=[t['xg'] for t in st['teams']],
                stats_sha256=hashlib.sha256(json.dumps(st,sort_keys=True).encode()).hexdigest(),
                profile_readbacks=ps, records=receipt['records'], raw_sha256=digest(task['path']),
                input_dump_sha256=digest(task['dump']), startup_sha256=r['startup_receipt_sha256'],
                seconds=r['native_elapsed_seconds'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['prepare','technical'])
    parser.add_argument('game', type=Path)
    args = parser.parse_args()
    runtime = PRIVATE/'runtime'
    engine = runtime/'engine'
    fixture = engine/'fm27_native/fixtures/match.pkm'
    require(digest(args.game/'fm_Data/Plugins/x86_64/game_plugin.dll') == DLL and
            digest(engine/'fm27_native/FM27Simulator.exe') == HOST and digest(fixture) == FIXTURE,
            'Input identity mismatch')
    os.environ.update(FM27_ENGINE_ROOT=str(engine), FM27_GAME_ROOT=str(args.game.resolve()),
                      FM27_DESKTOP_DATA=str(PRIVATE/'lab-data'))
    sys.path.insert(0,str(runtime/'source'))
    import fm27_tactics_server as server
    status = server.ENGINE_COMPATIBILITY
    settings = read(DOC/'profile-config.json')
    require(status['original_build_verified'] and status['can_simulate'] and
            status['adapter_version'] == settings['build'] and status['actual_dll_sha256'] == DLL,
            'Adapter rejects installed build')
    configurations = setups(server, settings)
    base = dict(build=settings['build'], engine=DLL, host=HOST, fixture=FIXTURE,
                resource=status['resource_fingerprint'], profile=status['profile'], release='v1118.1',
                cells={k:v[2] for k,v in configurations.items()}, repeats=2)
    if args.phase == 'prepare':
        with NativeLease(ROOT/'local/global-native','META-VALIDATION-001 seed allocation'):
            seed = reserve()
            write(PLAN, dict(**base, seeds=[seed]))
        return
    plan = read(PLAN)
    seed, = read(REG)['seeds']
    require(plan == dict(**base,seeds=[seed]), 'Registered plan has changed')
    git_plan = subprocess.check_output(['git','show','HEAD:docs/meta-validation-001/technical-plan.json'],cwd=ROOT)
    require(json.loads(git_plan) == plan, 'Plan not committed')
    with NativeLease(ROOT/'local/global-native','META-VALIDATION-001-TECH',1):
        out = PRIVATE/'technical'
        out.mkdir(exist_ok=False)
        for key,(config,blob,cell) in configurations.items():
            pair = []
            for repeat in (1,2):
                name = f'{key}-r{repeat}'
                row = run_one(server,engine,fixture,out/name,name,config,blob,cell,seed)
                with (out/'ledger.jsonl').open('a',encoding='utf8') as f:
                    f.write(json.dumps(row)+'\n')
                pair.append(row)
            for field in ('score','tick','stats_sha256','setup_sha256'):
                require(pair[0][field] == pair[1][field], 'A/A mismatch: '+field)
            print(key,'A/A passed',flush=True)


if __name__ == '__main__':
    main()

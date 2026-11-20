"""Reconstruct the technical acceptance from public rows or original private receipts."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
from statistics import mean

DOC = Path(__file__).resolve().parents[1] / 'docs/meta-validation-001'


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding='utf8').splitlines()]


def check(ok, message):
    if not ok:
        raise ValueError(message)


def goals(score, side):
    check(type(side) is int and side in (0, 1), 'Missing or invalid team side')
    check(isinstance(score, list) and len(score) == 2 and
          all(type(v) is int and v >= 0 for v in score), 'Invalid or missing score')
    return score[side] - score[1-side]


def pair_value(a, b, scores):
    """One G and V per frozen player pair. Keys are (fixture, side, seed)."""
    check(set(a) == set(b) and a, 'Missing paired context')
    check(set(scores) == {'v2.0', 'v2.1'}, 'Unexpected models')
    signs = {}
    for model, values in scores.items():
        check(len(values) == 2 and all(type(v) in (int,float) and isfinite(v) for v in values),
              'Missing model score')
        signs[model] = int(values[0] > values[1]) - int(values[0] < values[1])
    d = mean(goals(a[key], key[1]) - goals(b[key], key[1]) for key in a)
    v = (signs['v2.1'] - signs['v2.0']) * d
    return dict(D=d, V=v, G=v/2)


def curvature(gd):
    check(set(gd) == {7, 9, 16, 19} and all(type(v) in (int,float) and isfinite(v)
          for v in gd.values()), 'Incomplete dose block')
    return (gd[19] - gd[16])/3 - (gd[9] - gd[7])/2


def audit(plan, measurements):
    expected = {f'{key}-r{i}':cell for key,cell in plan['cells'].items()
                for i in range(1,plan['repeats'] + 1)}
    check(Counter(r['key'] for r in measurements) == Counter(expected.keys()),
          'Duplicate, missing or unknown job')
    lookup = {r['key']:r for r in measurements}
    for key, cell in expected.items():
        r = lookup[key]
        check(all(r[k] == v for k,v in cell.items()), 'Wrong slot, dose, phase or setup')
        check(r['seed'] == plan['seeds'][0] and r['side'] == 0 and
              r['fixture_sha256'] == plan['fixture'] and r['engine_sha256'] == plan['engine'] and
              r['host_sha256'] == plan['host'], 'Wrong fixture, build, seed or side')
        check(r['kind'] == 'technical' and r['actor_verified'] is True and r['cleanup_verified'] is True,
              'Invalid purpose, actor or cleanup')
        check(r['actor_token'] == 'fixture-'+cell['position'], 'Unregistered technical actor')
        check(r['position_rating'] == {'ST':1, 'CB':17}[cell['position']],
              'Original positional rating differs')
        goals(r['score'],r['side'])
        check(len(r['xg']) == 2 and all(type(v) in (int,float) and isfinite(v) and v >= 0 for v in r['xg']),
              'Missing expected goals')
    for key in plan['cells']:
        a, b = lookup[key+'-r1'], lookup[key+'-r2']
        for field in ('setup_sha256','score','xg','tick','stats_sha256','actor_token'):
            check(a[field] == b[field], 'Non-deterministic A/A or identity drift')
    for pos in ('CB','ST'):
        check(len({r['actor_token'] for r in measurements if r['position']==pos}) == 1,
              'Identity changed across doses')
    return dict(technical_matches=len(measurements), exact_aa_pairs=len(plan['cells']),
                independent_technical_seeds=len(set(r['seed'] for r in measurements)),
                scientific_matches=0, scientific_pairs=0)


def rebuild(plan, private):
    results = []
    # Each cell is independently reconstructed from its own worker's original outputs.
    actors = {}
    for ledger in lines(private/'ledger.jsonl'):
        name = ledger['key']
        cell = plan['cells'][name.rsplit('-r',1)[0]]
        folder = private/name
        log = lines(folder/'raw.jsonl')
        def event(label):
            row, = (r for r in log if r['event'] == label)
            return row
        finish = event('natural_match_finished')
        check(finish['full_match_completed'] and finish['score'] == ledger['score'] and
              finish['tick'] == ledger['tick'], 'Finish differs')
        seed = event('native_input_seed')
        check(seed['override'] and seed['effective_seed'] == ledger['seed'], 'Seed differs')
        stats = event('native_match_statistics')
        check([v['xg'] for v in stats['teams']] == ledger['xg'] and
              sha256(json.dumps(stats,sort_keys=True).encode()).hexdigest() == ledger['stats_sha256'],
              'Statistics differ')
        cb, = load(folder/'callbacks.json')
        check(cb['seed'] == ledger['seed'] and cb['engine_dll_sha256'] == plan['engine'] and
              cb['collector_sha256'] == plan['host'] and cb['verified'], 'Wrong worker provenance')
        session, = load(folder/'sessions.json')
        check(session['returncode'] == 0 and session['steam_session_cleanup']['ok'] and
              session['completed'] == session['expected'] == 1, 'Job accounting or cleanup differs')
        manifest, = folder.rglob('manifest.txt')
        check(sha256(manifest.read_bytes()).hexdigest() == session['manifest_sha256'], 'Worker plan drift')
        protocol, count, fixture, setup, output, worker_seed, prepared = manifest.read_text(
            encoding='utf-8-sig').splitlines()
        check(protocol == 'FM27DW2' and count == '1' and int(worker_seed) == ledger['seed']
              and sha256(Path(fixture).read_bytes()).hexdigest() == plan['fixture']
              and [Path(p).resolve() for p in (setup,output,prepared)] ==
              [(folder/p).resolve() for p in ('setup.bin','raw.jsonl','input.json')], 'Worker input differs')
        for filename, key in [('raw.jsonl','raw_sha256'),('input.json','input_dump_sha256'),
                              ('setup.bin','setup_sha256'),(cb['startup_receipt'],'startup_sha256')]:
            check(sha256((folder/filename).read_bytes()).hexdigest() == ledger[key], 'Evidence digest mismatch')
        teams = load(folder/'input.json')['teams']
        check([len(t['players']) for t in teams] == [23,23], 'Unexpected roster size')
        actor = teams[0]['players'][cell['slot']]
        pos = cell['position']
        rating = actor['attributes'][{'ST':12,'CB':3}[pos]]
        check(actor['index'] == cell['slot'] and actor['attributes'][cell['jr_index']] == cell['raw'],
              'Original starter or dose differs')
        # Compare every roster identity and ability, masking only the targeted byte.
        actor['attributes'][cell['jr_index']] = None
        signature = [(p['id'],p['person_key'],p['attributes']) for t in teams for p in t['players']]
        check(actors.setdefault(pos, signature) == signature, 'Unplanned roster change')
        results.append(dict(**ledger,kind='technical',actor_verified=True,actor_token='fixture-'+pos,
                            position_rating=rating,cleanup_verified=True,fixture_sha256=plan['fixture'],
                            engine_sha256=plan['engine'],host_sha256=plan['host']))
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private', type=Path, help='Recompute and compare to published rows')
    args = parser.parse_args()
    plan = load(DOC/'technical-plan.json')
    records = lines(DOC/'technical-matches.jsonl')
    if args.private:
        check(rebuild(plan,args.private) == records, 'Private reconstruction differs from public rows')
    print(json.dumps(audit(plan,records),indent=2))

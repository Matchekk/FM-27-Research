"""Single allowlisted outer supervisor for the independent NIGHT-002 mission."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
import os
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
if __name__ == '__main__' and any(name in ('research', 'analysis') or
        name.startswith(('research.', 'analysis.')) for name in sys.modules):
    raise RuntimeError('Native coordinator requires unimported project packages')
_cache = ROOT / 'local/night-002/import-cache' / uuid4().hex
if _cache.exists() or _cache.is_symlink():
    raise RuntimeError('Import cache prefix must be absent')
if any((ROOT / name).exists() or (ROOT / name).is_symlink() for name in
       ('analysis/__init__.py', 'analysis/__init__.pyc', 'analysis.py', 'analysis.pyc')):
    raise RuntimeError('Expected analysis namespace without initializer or shadow module')
sys.pycache_prefix = str(_cache)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from research.native import read, require
from research.night002_control import Night002Budget, assert_night002_admission, assert_artifact_limit

STUDY = 'MECH-004-SPLIT-R0'
ROUTES = {STUDY: 'analysis/run_split004.py'}
ARMS = ('C90L-C7AL', 'C90H-C7AL', 'C90L-C7AH', 'C90H-C7AH')
CONTEXTS = ('high_press', 'deep_block')


def validate_phase_keys(study, phase, keys):
    require(study in ROUTES and phase in ('technical', 'main'), 'Unknown NIGHT-002 route/phase')
    require(type(keys) is list and all(type(k) is str and k and len(k) <= 200 for k in keys) and
            len(keys) == len(set(keys)), 'Explicit unique ordered job-key list required')
    if phase == 'technical':
        expected = [f'tech-{context}-s{side}-{arm}-r{repeat}'
                    for context in CONTEXTS for side in (0, 1) for arm in ARMS for repeat in (0, 1)]
        require(keys == expected + ['negative-malformed'], 'Split pilot requires exactly32+1 technical keys')
        return
    pattern = r'(high_press|deep_block)-([1-9][0-9]*)-([01])-(C90L-C7AL|C90H-C7AL|C90L-C7AH|C90H-C7AH)'
    parsed = [re.fullmatch(pattern, key) for key in keys]
    require(len(keys) == 512 and all(parsed), 'Split pilot requires exactly512 main jobs')
    groups = {}
    for match in parsed:
        context, seed, side, arm = match.groups()
        require(int(seed) <= 0xffffffff, 'Invalid split seed')
        groups.setdefault((context, seed), set()).add((side, arm))
    cells = set(product(('0', '1'), ARMS))
    require(len(groups) == 64 and all(value == cells for value in groups.values()) and
            all(sum(h == context for h, _ in groups) == 32 for context in CONTEXTS) and
            len({seed for _, seed in groups}) == 64 and
            keys == sorted(keys, key=lambda key: sha256(key.encode()).digest()),
            'Split main needs64 distinct complete seed blocks in registered schedule order')


def parse_cli(argv):
    parser = ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('command', choices=('run', 'admitted', 'status'))
    parser.add_argument('--study', choices=tuple(ROUTES))
    parser.add_argument('--phase', choices=('technical', 'main'))
    parser.add_argument('--keys-file', type=Path)
    split = argv.index('--') if '--' in argv else len(argv)
    return parser.parse_args(argv[:split]), argv[split + 1:]


def validate_inner_arguments(arguments):
    """Only concrete publication evidence can be forwarded to a study route."""
    require(type(arguments) is list and len(arguments) == 4 and
            set(arguments[::2]) == {'--publication', '--ci-run'},
            'Only explicit publication and CI arguments may be forwarded')
    values = dict(zip(arguments[::2], arguments[1::2], strict=True))
    require(re.fullmatch('[0-9a-f]{40}', values['--publication']) and
            re.fullmatch('[1-9][0-9]*', values['--ci-run']),
            'Full publication SHA and positive CI run required')


def main(argv=None):
    args, arguments = parse_cli(sys.argv[1:] if argv is None else argv)
    local = ROOT / 'local/night-002'
    if args.command == 'status':
        import json
        state = read(local / 'program-budget.json')
        public = {k: state[k] for k in ('charged_seconds', 'limit_seconds',
                  'absolute_deadline_utc', 'halted')}
        public['active_operation'] = state['active'].get('name') if state['active'] else None
        print(json.dumps(public, indent=2))
        return
    require((ROOT / '.git').is_dir(), 'Execution only from central checkout')
    require(args.study and args.phase and args.keys_file is not None, 'Explicit study/phase/keys required')
    require(args.keys_file.resolve().is_relative_to(ROOT), 'Job keys must be repository-local')
    keys = read(args.keys_file)
    validate_phase_keys(args.study, args.phase, keys)
    validate_inner_arguments(arguments)
    require((ROOT / ROUTES[args.study]).is_file(), 'Selected study runner is not yet integrated')
    assert_artifact_limit(ROOT)
    if args.command == 'admitted':
        os.environ['NIGHT002_PROGRAM_TOKEN'] = os.environ.get('TACT_P0_SUPERVISOR_TOKEN', '')
        assert_night002_admission(ROOT, args.study, args.phase, keys)
        command = [sys.executable, str(ROOT / ROUTES[args.study]), args.phase, *arguments]
        raise SystemExit(subprocess.run(command, cwd=ROOT,
                         creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).returncode)
    budget = Night002Budget(local / 'program-budget.json')
    command = [sys.executable, str(Path(__file__).resolve()), 'admitted', '--study', args.study,
               '--phase', args.phase, '--keys-file', str(args.keys_file.resolve())]
    if arguments:
        command.extend(('--', *arguments))
    output = local / (args.study + '-' + args.phase + '.stdout')
    require(not output.exists(), 'Retained program stdout: no retry/overwrite')
    budget.run(args.study + '/' + args.phase, args.phase,
               [args.study + ':' + key for key in keys], command, ROOT, output)
    assert_artifact_limit(ROOT)
    print(output.read_text(encoding='utf8', errors='replace')[-3000:])
    print('NIGHT-002 charged seconds:', budget.load()['charged_seconds'], '/', budget.seconds)


if __name__ == '__main__':
    main()

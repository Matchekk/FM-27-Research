"""Admit one explicitly routed native study phase under the shared night budget."""
from argparse import ArgumentParser
from pathlib import Path
import os
import subprocess
import sys
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[1]
# A new source epoch must not import timestamp-valid old project bytecode.
# Do not delete shared caches: use a fresh absent prefix and forbid writes.
if __name__=='__main__' and any(name in ('research','analysis') or name.startswith(('research.','analysis.')) for name in sys.modules):
    raise RuntimeError('Direct native coordinator requires unimported project packages')
_cache=ROOT/'local/night-001/import-cache'/uuid4().hex
if _cache.exists() or _cache.is_symlink():raise RuntimeError('Import cache prefix must be absent')
if any((ROOT/name).exists() or (ROOT/name).is_symlink() for name in
       ('analysis/__init__.py','analysis/__init__.pyc','analysis.py','analysis.pyc')):
    raise RuntimeError('Expected analysis namespace without package initializer or shadow module')
sys.pycache_prefix=str(_cache);sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT))
from research.native import read, require
from research.night_control import NightBudget, assert_night_admission

ROUTES={
    'VALID-005-OBSERVER-V1':'analysis/run_observer005.py',
    'MECH-003-STAMINA-R0':'analysis/run_mech003.py',
    'MECH-002-STARTPOLICY-TECH-V1':'analysis/run_startpolicy002.py',
    'MECH-002-SHARPNESS-P0':'analysis/run_sharpness002.py',
}


def validate_phase_keys(study,phase,keys):
    require(len(keys)==len(set(keys)),'Duplicate program operation keys')
    if study=='MECH-002-STARTPOLICY-TECH-V1':
        require(phase!='main','Startpolicy route is a technical gate, with no main authorization')
        if phase=='technical':
            expected=[f'full-{context}-s{side}-sharp{level}-r{repeat}'
                for context in ('high_press','deep_block') for side in (0,1)
                for level in (10000,7000) for repeat in (0,1)]+['negative-malformed']
            require(keys==expected,'Startpolicy requires the exact seventeen technical keys')
    if study=='MECH-002-SHARPNESS-P0':
        if phase=='technical':
            expected=[f'tech-{context}-s{side}-{arm}-r{repeat}'
                for context in ('high_press','deep_block') for side in (0,1)
                for arm in ('S70-P0','S100-P0','S70-P1','S100-P1') for repeat in (0,1)]+['negative-malformed']
            require(keys==expected,'Sharpness pilot requires exactly32 full technical jobs and one negative')
        elif phase=='main':
            # The registration still binds actual seed values and setup hashes.
            # This outer boundary independently rejects incomplete/expanded blocks.
            import re
            from hashlib import sha256
            from itertools import product
            parsed=[re.fullmatch(r'(high_press|deep_block)-([1-9][0-9]*)-([01])-(S70-P0|S100-P0|S70-P1|S100-P1)',key) for key in keys]
            require(len(keys)==512 and all(parsed),'Sharpness pilot requires exactly512 declared main jobs')
            groups={}
            for match in parsed:
                context,seed,side,arm=match.groups()
                require(int(seed)<=0xffffffff,'Invalid sharpness seed')
                groups.setdefault((context,seed),set()).add((side,arm))
            cells=set(product(('0','1'),('S70-P0','S100-P0','S70-P1','S100-P1')))
            require(len(groups)==64 and all(value==cells for value in groups.values()) and
                    all(sum(h==context for h,_ in groups)==32 for context in ('high_press','deep_block')) and
                    len({seed for _,seed in groups})==64 and
                    keys==sorted(keys,key=lambda key:sha256(key.encode()).digest()),
                    'Sharpness main requires64 distinct complete seed blocks in registered schedule order')
    if phase=='prepare':
        expected=['loader-check-image-prepare'] if study=='MECH-003-STAMINA-R0' else []
        require(keys==expected,'Preparation must reserve its actual declared native probes')
    else:require(bool(keys),'Execution phase needs nonempty explicit reservations')


def parse_cli(argv):
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('run','admitted','status'))
    parser.add_argument('--study',choices=tuple(ROUTES))
    parser.add_argument('--phase',choices=('prepare','technical','main'))
    parser.add_argument('--keys-file',type=Path)
    split=argv.index('--') if '--' in argv else len(argv)
    return parser.parse_args(argv[:split]),argv[split+1:]


def main(argv=None):
    args,arguments=parse_cli(sys.argv[1:] if argv is None else argv)
    if args.command=='status':
        import json
        state=read(ROOT/'local/night-001/program-budget.json')
        print(json.dumps({k:state[k] for k in ('charged_seconds','limit_seconds','absolute_deadline_utc','halted')},indent=2))
        return
    require((ROOT/'.git').is_dir(),'Program execution only from central checkout')
    require(args.study and args.phase,'Explicit study/phase required')
    if args.keys_file:
        require(args.keys_file.resolve().is_relative_to(ROOT),'Job-key file must be repository-local')
    keys=read(args.keys_file) if args.keys_file else []
    require(type(keys) is list and all(type(k) is str and k and len(k)<=200 for k in keys),
            'Explicit unique job-key JSON list required')
    require(args.phase=='prepare' or args.keys_file is not None,'Non-preparation phase needs explicit match reservations')
    validate_phase_keys(args.study,args.phase,keys)
    require(not any(a in ('--child','--study-supervisor','--capsule') for a in arguments),'Cannot inject an inner child mode')
    require((ROOT/ROUTES[args.study]).is_file(),'Selected study runner is not yet integrated; no budget admission')
    if args.command=='admitted':
        # The original token exists only in this authenticated process environment.
        # No token is printed, passed in argv or exported in a public receipt.
        os.environ['NIGHT_PROGRAM_TOKEN']=os.environ.get('TACT_P0_SUPERVISOR_TOKEN','')
        assert_night_admission(ROOT,args.study,args.phase,keys)
        command=[sys.executable,str(ROOT/ROUTES[args.study]),args.phase,*arguments]
        raise SystemExit(subprocess.run(command,cwd=ROOT,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)).returncode)
    local=ROOT/'local/night-001'
    budget=NightBudget(local/'program-budget.json')
    command=[sys.executable,str(Path(__file__).resolve()),'admitted','--study',args.study,'--phase',args.phase]
    if args.keys_file:command.extend(('--keys-file',str(args.keys_file.resolve())))
    if arguments:command.extend(('--',*arguments))
    output=local/(args.study+'-'+args.phase+'.stdout')
    require(not output.exists(),'Retained program stdout: no retry/overwrite')
    budget.run(args.study+'/'+args.phase,'main' if args.phase=='main' else 'technical',
               [args.study+':'+key for key in keys],command,ROOT,output)
    print(output.read_text(encoding='utf8',errors='replace')[-3000:])
    print('Program charged seconds:',budget.load()['charged_seconds'],'/',budget.seconds)


if __name__=='__main__':main()

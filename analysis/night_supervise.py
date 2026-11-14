"""Admit one explicitly routed native study phase under the shared night budget."""
from argparse import ArgumentParser
from pathlib import Path
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read, require
from research.night_control import NightBudget, assert_night_admission

ROUTES={
    'VALID-005-OBSERVER-V1':'analysis/run_observer005.py',
    'MECH-003-STAMINA-R0':'analysis/run_mech003.py',
    'MECH-002-STARTPOLICY-TECH-V1':'analysis/run_startpolicy002.py',
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

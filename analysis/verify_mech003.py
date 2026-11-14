"""Portable public verification; private native receipts need independent review."""
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime, timedelta
from itertools import product
from math import isclose
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.stamina003 import EXPERIMENT, ARMS, CONTEXTS, PROCESS_CAPS,probe_jobs,matrix, treatment
from research.core import config_hash, schedule
from research.native import read, rows, require
from research.stats import metrics
from analyse_mech003 import analyse, validate_design
from run_mech003 import source_hash


def same(actual, expected):
    """Floating arithmetic tolerances, exact structural/integer identity."""
    if isinstance(expected,dict):
        require(isinstance(actual,dict) and set(actual)==set(expected),'Result object fields differ')
        for key,value in expected.items():same(actual[key],value)
    elif isinstance(expected,list):
        require(isinstance(actual,list) and len(actual)==len(expected),'Result list differs')
        for a,b in zip(actual,expected,strict=True):same(a,b)
    elif type(expected) is float:
        require(type(actual) in (int,float) and isclose(actual,expected,rel_tol=1e-11,abs_tol=1e-12),'Result arithmetic differs')
    else:require(type(actual) is type(expected) and actual==expected,'Result value differs')


def verify_complete_budget(budget, technical_keys, main_keys):
    require(budget['experiment']==EXPERIMENT and budget['limits']==PROCESS_CAPS and
            budget['limit_seconds']==600 and budget['wall_limit_seconds']==1200 and
            budget['active'] is None and budget['halted'] is False,'Completed budget limits/state differ')
    operations=budget['operations'];require([o['name'] for o in operations]==['prepare','technical','main'],
                                           'Unexpected/repeated phases')
    expected={'prepare':['loader-check-image-prepare'],
              'technical':['loader-check-image-technical','worker-capabilities-technical',*technical_keys],
              'main':['loader-check-image-main','worker-capabilities-main',*main_keys]}
    reserved={k:'main' if phase=='main' else 'technical' for phase,keys in expected.items() for k in keys}
    require(budget['reserved']==reserved,'Completed reservation keys differ')
    total=sum(o['elapsed_seconds'] for o in operations)
    require(0<=total<600 and isclose(total,budget['charged_seconds'],rel_tol=1e-11,abs_tol=1e-9),
            'Childtime accounting differs/exceeds cap')
    start=datetime.fromisoformat(budget['wall_start_utc']);deadline=datetime.fromisoformat(budget['wall_deadline_utc'])
    require(start.tzinfo is not None and deadline==start+timedelta(seconds=1200),'Fixed UTC deadline differs')
    for operation in operations:
        began=datetime.fromisoformat(operation['start_utc']);ended=began+timedelta(seconds=operation['elapsed_seconds'])
        require(operation['returncode']==0 and operation['timed_out'] is False and
                len(operation['keys'])==len(set(operation['keys'])) and set(operation['keys'])==set(expected[operation['name']]) and
                operation['kind']==('main' if operation['name']=='main' else 'technical') and
                0<=operation['elapsed_seconds'] and start<=began<=ended<=deadline,
                'Phase execution/budget receipt differs')
    require(budget['within_fixed_deadline'] is True,'Completed deadline flag false')


def verify_containment(proofs):
    require(set(proofs)=={'prepare','technical','main','negative'},'Missing process containment phases')
    for phase,proof in proofs.items():
        policy=proof['job_policy']
        require(proof['schema']=='fm27.contained-call.v1' and proof['cleanup_confirmed'] is True and
                proof['capsule_exit_confirmed'] is True and type(proof['kernel_active_processes']) is int and
                proof['kernel_active_processes']==0 and policy['active_process_limit']==(3 if phase=='negative' else 10) and
                policy['limit_flags']==0x2008 and policy['kill_on_close'] is True and policy['breakaway_allowed'] is False,
                'Unconfirmed kernel process-tree cleanup')


def verify(directory):
    receipt=read(directory/'manifest.json');c=receipt['config'];validate_design(c)
    require(receipt['config_sha256']==config_hash(c),'Receipt hash drift')
    plan=read(directory/'seed-plan.json');excluded=set(read(directory/'excluded-seeds.json'))
    require(len(plan['main_seeds'])==64 and len(plan['technical_seeds'])==2 and
            len(plan['seeds'])==len(set(plan['seeds']))==66 and plan['main_seeds']==receipt['seeds'] and
            set(plan['seeds'])==set(plan['technical_seeds']+plan['main_seeds']) and
            all(type(s) is int and 0<s<=0xffffffff for s in plan['seeds']) and
            not set(plan['seeds'])&excluded,'Seed count/identity/collision')
    require(plan['excluded_seed_count']==len(excluded) and config_hash(sorted(excluded))==plan['excluded_seed_set_sha256'],'Exclusion commitment drift')
    require(read(directory/'design-matrix.json')['matrix']==matrix(),'Public matrix differs')
    for name,sha in c['execution']['artifacts'].items():require(source_hash(directory/name)==sha,'Frozen input differs:'+name)
    for name,sha in c['execution']['code_sha256'].items():require(source_hash(ROOT/name)==sha,'Frozen source differs:'+name)
    archive=read(directory/'historical-archive.json')
    require(all(source_hash(ROOT/name)==sha for name,sha in archive['sha256'].items()),'Historical archive differs')
    expected={j['key']:j for j in schedule(receipt)}
    technical={f'tech-{h}-{s}-{a}-r{repeat}':dict(seed=plan['technical_seeds'][CONTEXTS.index(h)],scenario=h,side=s,arm=a)
               for h,s,a,repeat in product(CONTEXTS,(0,1),ARMS,(0,1))}
    summary=read(directory/'run-summary.json') if (directory/'run-summary.json').exists() else None
    if summary:
        account=rows(directory/'job-accounting.jsonl')
        require(len(account)==len({r['key'] for r in account})==550 and
                {r['key'] for r in account}==set(expected)|set(technical)|{'negative-binary'}|{j['key'] for j in probe_jobs()},'Incomplete accounting')
        calculated={kind:dict(Counter(r['status'] for r in account if r['kind']==kind)) for kind in ('technical','main')}
        require(calculated==summary['counts'],'Accounting summary differs')
        if summary['technical_gate_passed']:
            tech=rows(directory/'technical.jsonl');require(len(tech)==len({r['key'] for r in tech})==32,'Technical measurements incomplete')
            grouped={}
            for row in tech:
                require(row['key'] in technical,'Unexpected technical row');j=technical[row['key']];tr=treatment(j['arm'])
                require(row['status']=='ok' and row['engine_readback'] is True and row['experiment_id']==EXPERIMENT and
                        row['seed']==j['seed'] and row['scenario']==j['scenario'] and row['tested_side']==j['side'] and row['arm']==j['arm'] and
                        all(row.get(k)==v for k,v in c['identity'].items()) and
                        row['setup_sha256']==c['design']['setups'][j['scenario']][str(j['side'])][j['arm']] and
                        row['config_sha256']==receipt['config_sha256'],'Technical provenance mismatch')
                require(row['native_stamina_values']==[tr['stamina_raw']]*10 and row['native_pressing_bit']==tr['pressing_bit'] and
                        row['profile_fields_verified']==1058 and row['native_attribute_values_verified']==3174 and
                        row['native_roles_verified']==row['native_pi_cells_verified']==44 and row['native_pi_groups_verified']==748,
                        'Technical input gate differs')
                metrics(row);grouped.setdefault((j['scenario'],j['side'],j['arm']),[]).append(row)
            require(len(grouped)==16 and all(len(pair)==2 and all(pair[0][k]==pair[1][k] for k in
                    ('score','finish_tick','team_statistics','setup_sha256','seed')) for pair in grouped.values()),'A/A repeats differ')
            require(read(directory/'negative-control.json')['status']=='expected_rejection','Negative rejection absent')
        if summary['scientific_series_complete']:
            verify_complete_budget(read(directory/'budget.json'),list(technical)+['negative-binary'],list(expected))
            verify_containment(read(directory/'phase-containment.json'))
            launches=rows(directory/'host-starts.jsonl')
            require(len(launches)==74 and len({(r['phase'],r['key']) for r in launches})==74,'Host launch accounting differs')
            require(Counter((r['phase'],r['kind']) for r in launches)==Counter({
                ('prepare','loader'):1,('technical','loader'):1,('main','loader'):1,
                ('technical','capabilities'):1,('main','capabilities'):1,
                ('technical','worker_start'):4,('main','worker_start'):64,('technical','negative'):1}),
                'Native host launch inventory differs')
            data=rows(directory/'main.jsonl');effects,blocks=analyse(data,receipt)
            same(read(directory/'effects.json'),effects);same(rows(directory/'block-contrasts.jsonl'),blocks)
            require(calculated['main']=={'ok':514} and calculated['technical']=={'ok':35,'expected_rejection':1},'Final job states incomplete')
    return dict(contract_verified=True,planned_main_matches=512,independent_main_blocks=64,
                completed=bool(summary and summary['scientific_series_complete']),native_starts_by_verifier=0)


if __name__=='__main__':
    import json
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'data/mech-003-stamina');args=parser.parse_args()
    print(json.dumps(verify(args.directory),sort_keys=True))

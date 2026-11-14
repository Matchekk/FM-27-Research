"""Portable public ATTR-009 contract, archive, accounting and result verification."""
from argparse import ArgumentParser
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.attr009 import ARMS,CONTEXTS,matrix
from research.core import config_hash,schedule
from research.native import read,rows,require
from analyse_attr009 import analyse,validate_design
from run_attr009 import source_hash


def verify(directory):
    r=read(directory/'manifest.json');c=r['config'];validate_design(c)
    require(r['config_sha256']==config_hash(c),'Contract receipt drift')
    require(read(directory/'design-matrix.json')['matrix']==matrix(),'Public matrix drift')
    plan=read(directory/'seed-plan.json');excluded=set(read(directory/'excluded-seeds.json'))
    require(len(plan['main_seeds'])==32 and len(plan['technical_seeds'])==2 and
            len(plan['seeds'])==len(set(plan['seeds']))==34 and
            not set(plan['seeds'])&excluded and plan['main_seeds']==r['seeds'],'Seed overlap/count drift')
    require(config_hash(sorted(excluded))==plan['excluded_seed_set_sha256'],'Exclusion commitment drift')
    require(set(c['design']['setups'])==set(CONTEXTS) and len(schedule(r))==384,'Discovery schedule drift')
    for n,v in c['execution']['artifacts'].items():require(source_hash(directory/n)==v,'Frozen artifact drift:'+n)
    for n,v in c['execution']['code_sha256'].items():require(source_hash(ROOT/n)==v,'Frozen code drift:'+n)
    archive=read(directory/'historical-archive.json')
    require(all(source_hash(ROOT/n)==v for n,v in archive['sha256'].items()),'Historical archive changed')
    summary=read(directory/'run-summary.json')if(directory/'run-summary.json').exists()else None
    if summary and summary['scientific_series_complete']:
        data=rows(directory/'main.jsonl');effects,_=analyse(data,r)
        require(effects==read(directory/'effects.json'),'Published effects fail deterministic reconstruction')
        account=rows(directory/'job-accounting.jsonl')
        require(len(account)==417 and len({x['key']for x in account})==417,'Accounting count/duplicate')
        require(sum(x['kind']=='main'and x['status']=='ok'for x in account)==384,'Main accounting incomplete')
        require(sum(x['kind']=='technical'and x['status']=='ok'for x in account)==32,'Technical accounting incomplete')
        require(read(directory/'negative-control.json')['status']=='expected_rejection','Negative not rejected')
    return dict(contract_verified=True,main_matches=384,independent_blocks=32,
                completed=bool(summary and summary['scientific_series_complete']),native_processes_started_by_verifier=0)


if __name__=='__main__':
    import json
    p=ArgumentParser(description=__doc__);p.add_argument('--directory',type=Path,default=ROOT/'data/attr-009-bridge');a=p.parse_args()
    print(json.dumps(verify(a.directory),sort_keys=True))

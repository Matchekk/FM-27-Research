"""Reproduce the preregistered split analysis from released public match rows."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.pycache_prefix=str(ROOT/'local/night-002/analysis-cache'/uuid4().hex)
sys.dont_write_bytecode=True
from research.native import read,require,rows
from analysis.run_observer005 import source_hash
from analysis.analyse_split004 import analyse


def save(path,text):
    if path.exists():
        require(path.read_text(encoding='utf8')==text,'Released analysis changed: '+path.name)
    else:
        with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(text)


def main():
    public=ROOT/'data/night-002-split004'
    summary=read(public/'main-summary.json')
    require(summary['passed'] is True and summary['scientific_analysis_allowed'] is True,
            'A fully reconciled main release is required')
    receipt=read(public/'manifest.json');frozen=read(public/'inputs.json')
    require(all(source_hash(ROOT/n)==h for n,h in frozen['code_sha256'].items()),
            'Analysis source epoch differs from preregistration')
    value,contrasts=analyse(rows(public/'main.jsonl'),receipt)
    effects=json.dumps(value,indent=2,allow_nan=False)+'\n'
    lines=''.join(json.dumps(row,sort_keys=True,allow_nan=False)+'\n' for row in contrasts)
    save(public/'effects.json',effects);save(public/'seed-contrasts.jsonl',lines)
    provenance=dict(experiment_id='MECH-004-SPLIT-R0',preregistration_commit=receipt['config']['preregistration']['commit'],
        frozen_analysis_sha256=source_hash(ROOT/'analysis/analyse_split004.py'),
        report_source_sha256=source_hash(Path(__file__)),
        main_rows_sha256=source_hash(public/'main.jsonl'),manifest_sha256=source_hash(public/'manifest.json'),
        effects_sha256=sha256(effects.encode()).hexdigest(),seed_contrasts_sha256=sha256(lines.encode()).hexdigest(),
        command='python -B analysis/report_split004.py',native_calls=0)
    save(public/'analysis-provenance.json',json.dumps(provenance,indent=2)+'\n')
    print(json.dumps(dict(matches=value['n_matches'],blocks=value['independent_seed_blocks'],
        primary=value['primary'],secondary={k:{x:v[x] for x in ('mean','ci','p_holm')} for k,v in value['secondary'].items()}),indent=2))


if __name__=='__main__':main()

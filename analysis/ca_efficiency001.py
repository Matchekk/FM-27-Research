"""Reference-weight scenarios only: never infer true CA or PA from a table."""
import argparse
import csv
from hashlib import sha256
import io
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_table(path):
    blob=Path(path).read_bytes()
    reader=csv.DictReader(io.StringIO(blob.decode('utf-8-sig')))
    if reader.fieldnames!=['Position','Attribute','CA cost']:
        raise ValueError('Expected the declared reference-table columns')
    table={}
    for row in reader:
        if set(row)!=set(reader.fieldnames) or any(v is None for v in row.values()):
            raise ValueError('Malformed table row')
        position,attribute=row['Position'].strip(),row['Attribute'].strip()
        value=float(row['CA cost'])
        if not position or not attribute or not math.isfinite(value) or value<=0 or not value.is_integer():
            raise ValueError('Positive integer reference weights required')
        if attribute in table.setdefault(position,{}):raise ValueError('Duplicate table cell')
        table[position][attribute]=int(value)
    if not table:raise ValueError('Empty table')
    return table,sha256(blob).hexdigest()

def optimize_increments(weights,values,room,budget):
    """Exact bounded integer knapsack in REFERENCE UNITS, not actual CA.

    The separable linear scenario assumes each next point has the same table
    weight and benefit. Neither assumption is a measured FM27 mechanism.
    """
    if type(budget) is not int or budget<0:raise ValueError('Nonnegative integer budget required')
    if not weights or set(weights)!=set(values) or set(weights)!=set(room):raise ValueError('Complete matching attributes required')
    if any(type(w) is not int or w<=0 for w in weights.values()):raise ValueError('Positive integer reference costs required')
    if any(type(r) is not int or not 0<=r<=19 for r in room.values()):raise ValueError('Explicit feasible attribute room required')
    if any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in values.values()):raise ValueError('Finite nonnegative proxy benefits required')
    states={0:(0.,{})}
    for attribute in sorted(weights):
        nxt={}
        for spent,(value,allocation) in states.items():
            for count in range(min(room[attribute],(budget-spent)//weights[attribute])+1):
                cost=spent+count*weights[attribute];gain=value+count*values[attribute]
                if cost not in nxt or gain>nxt[cost][0]:nxt[cost]=(gain,{**allocation,attribute:count})
        states=nxt
    spent,(value,allocation)=max(states.items(),key=lambda kv:(kv[1][0],-kv[0]))
    return dict(status='MODELED_REFERENCE_UNITS_ONLY',spent_reference_units=spent,budget_reference_units=budget,
                proxy_gain=value,increments=allocation,actual_ca_spent=None,expected_match_gain=None)

def audit(path):
    table,digest=load_table(path)
    # Published v0.1 is a scouting index, not an outcome-calibrated estimator.
    model=json.loads((ROOT/'research/meta_score_v01_weights.json').read_text(encoding='utf8'))
    return dict(status='REFERENCE_TABLE_AUDIT_NOT_CA_CALIBRATION',source_sha256=digest,
        source='https://github.com/jamiebolden/fm-scoring/blob/b5928ba2b9aba3c4c40a8f32118401eafb6f4c99/docs/ca_costs_fm27.csv',
        cells=sum(map(len,table.values())),positions={p:dict(listed_attributes=len(w),sum_reference_weights=sum(w.values()),
            minimum=min(w.values()),maximum=max(w.values())) for p,w in table.items()},
        actual_marginal_ca_identified=False,nonlinearity_identified=False,independent_real_profiles=0,
        holdout_mae=None,holdout_bias=None,calibration=None,
        note='A repeated weight at levels8 and17 is a model assumption, not evidence of equal engine costs. Missing cells remain unknown, never zero.',
        meta_score_baseline=model['model_id'])

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('table',type=Path)
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    result=audit(args.table)
    table,_=load_table(args.table)
    # Explicit illustrative ST scenario, no fictional player used as validation.
    attributes=('Acceleration','Pace','Jumping Reach','Finishing')
    result['illustrative_ST_scenario']=dict(start_display_level=12,max_display_level=20,
        benefit='v0.1 ST score numerator units; not match outcomes',
        **optimize_increments({a:table['ST'][a] for a in attributes},
            dict(zip(attributes,(19,21,16,8))),{a:8 for a in attributes},20))
    output=json.dumps(result,allow_nan=False,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(output,encoding='utf8')
    else:print(output)

if __name__=='__main__':main()

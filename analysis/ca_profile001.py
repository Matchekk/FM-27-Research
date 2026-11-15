"""Exploratory prediction of exported CA fields; no causal CA cost claim."""
import argparse
import csv
from hashlib import sha256
import io
import json
from math import fsum,isfinite,sqrt
from pathlib import Path
import re
import numpy as np
from analysis.ca_efficiency001 import load_table

ROOT=Path(__file__).resolve().parents[1]
SALT='PD-CA-001/player-split/v1:'
PROFILE_URL='https://raw.githubusercontent.com/SebastianFoder/fm-scoutreporter/3144dd0a45eb4f994230700c8faee64d33665273/packages/core/fixtures/attribute-fm27-hidden.csv'

def key(value):return re.sub('[^a-z0-9]','',value.lower())

def parse_profiles(path,weights):
    blob=Path(path).read_bytes();reader=csv.DictReader(io.StringIO(blob.decode('utf-8-sig')))
    header=reader.fieldnames or []
    if len({key(h) for h in header})!=len(header):raise ValueError('Duplicate normalized columns')
    columns={key(h):h for h in header}
    required={'uniqueid','position','ca',*(key(a) for a in weights)}
    if not required<=set(columns):raise ValueError('Missing required profile columns')
    profiles=[];failures=[];seen=set();count=0
    for number,row in enumerate(reader,start=2):
        count+=1;uid=(row.get(columns['uniqueid']) or '').strip()
        if not uid:failures.append(dict(row_number=number,reason='missing_identity'));continue
        if uid in seen:raise ValueError('Duplicate player identity: no split or model allowed')
        seen.add(uid)
        try:
            if row[columns['position']].strip()!='GK':raise ValueError('not_GK')
            ca=float(row[columns['ca']]);attributes={a:float(row[columns[key(a)]]) for a in weights}
            if not isfinite(ca) or not 1<=ca<=200:raise ValueError('invalid_CA')
            if any(not isfinite(v) or not 1<=v<=20 for v in attributes.values()):raise ValueError('invalid_attribute')
        except (ValueError,TypeError,KeyError) as error:
            reason=str(error) if str(error) in ('not_GK','invalid_CA','invalid_attribute') else 'missing_or_nonnumeric_value'
            failures.append(dict(row_number=number,reason=reason));continue
        profiles.append(dict(split_key=sha256((SALT+uid).encode()).hexdigest(),y=ca,
            weighted=fsum(weights[a]*v for a,v in attributes.items()),unweighted=fsum(attributes.values())/len(attributes)))
    return profiles,dict(rows=count,valid=len(profiles),failures=failures,source_sha256=sha256(blob).hexdigest())

def split(profiles):
    if len(profiles)!=109 or len({p['split_key'] for p in profiles})!=109:raise ValueError('Exactly109 distinct eligible profiles required')
    ordered=sorted(profiles,key=lambda p:p['split_key'])
    return ordered[:80],ordered[80:]

def fit(x,y):
    if len(x)!=len(y) or len(x)<2 or not all(isfinite(v) for v in [*x,*y]):raise ValueError('Invalid regression sample')
    mx,my=fsum(x)/len(x),fsum(y)/len(y)
    sxx=fsum((v-mx)**2 for v in x)
    if not sxx:raise ValueError('Constant predictor')
    slope=fsum((a-mx)*(b-my) for a,b in zip(x,y,strict=True))/sxx
    return dict(intercept=my-slope*mx,slope=slope)

def predict(model,x):return np.array([model['intercept']+model['slope']*v for v in x])

def error_summary(errors,indices):
    errors=np.asarray(errors,dtype=float)
    def interval(values):return np.quantile(values,[.025,.975]).tolist()
    return dict(mae=float(np.abs(errors).mean()),rmse=float(np.sqrt(np.square(errors).mean())),bias=float(errors.mean()),
        conditional95_intervals=dict(mae=interval(np.abs(errors)[indices].mean(axis=1)),
            rmse=interval(np.sqrt(np.square(errors)[indices].mean(axis=1))),bias=interval(errors[indices].mean(axis=1))))

def analyse(profile_path,table_path):
    table,table_hash=load_table(table_path);profiles,quality=parse_profiles(profile_path,table['GK'])
    training,holdout=split(profiles)
    ytrain=np.array([p['y'] for p in training]);ytest=np.array([p['y'] for p in holdout])
    indices=np.random.default_rng(2026111541).integers(29,size=(20000,29))
    models={};errors={};independent={}
    for label,field in (('W','weighted'),('U','unweighted')):
        xtrain=[p[field] for p in training];xtest=[p[field] for p in holdout]
        model=fit(xtrain,list(ytrain));train_pred=predict(model,xtrain);test_pred=predict(model,xtest)
        # Independent numerical solver, not the centered scalar fit above.
        coefficients=np.linalg.lstsq(np.column_stack([np.ones(80),xtrain]),ytrain,rcond=None)[0]
        discrepancy=max(abs(coefficients[0]-model['intercept']),abs(coefficients[1]-model['slope']))
        if discrepancy>1e-9:raise ValueError('Independent OLS reconstruction mismatch')
        independent[label]=dict(max_coefficient_difference=float(discrepancy),passed=True)
        errors[label]=test_pred-ytest
        models[label]=dict(coefficients=model,train_mae=float(np.abs(train_pred-ytrain).mean()),
            train_rmse=float(np.sqrt(np.square(train_pred-ytrain).mean())),
            holdout=error_summary(errors[label],indices),
            holdout_calibration_observed_CA_on_prediction=fit(list(test_pred),list(ytest)))
    errors['C']=np.repeat(ytrain.mean(),29)-ytest
    models['C']=dict(coefficients=dict(constant=float(ytrain.mean())),holdout=error_summary(errors['C'],indices))
    delta=np.abs(errors['W'])-np.abs(errors['U'])
    return dict(experiment_id='PD-CA-001',evidence='EXPLORATORY_RETROSPECTIVE_PUBLIC_EXPORT_DIAGNOSTIC',
        source_url=PROFILE_URL,profile_source_sha256=quality['source_sha256'],table_sha256=table_hash,
        native_build_independently_verified=False,real_game_gold_profiles=0,profile_rows=quality['rows'],eligible_rows=quality['valid'],
        missing_or_excluded=quality['failures'],train_players=80,holdout_players=29,identity_overlap=0,
        source_contexts='One public fixture file; save/club contexts unknown; no save-cluster holdout possible',
        coverage=dict(exported_ca_range=[min(p['y'] for p in profiles),max(p['y'] for p in profiles)],
            train_ca_range=[float(ytrain.min()),float(ytrain.max())],holdout_ca_range=[float(ytest.min()),float(ytest.max())],
            attribute_columns=len(table['GK']),sum_reference_weights=sum(table['GK'].values())),
        split=dict(salt=SALT,method='Sorted SHA256(salt+UniqueID), first80 train; remaining29 diagnostic holdout',
            membership_sha256=sha256('|'.join(p['split_key'] for p in sorted(profiles,key=lambda p:p['split_key'])).encode()).hexdigest()),
        primary=dict(estimand='Holdout MAE(W) minus MAE(U), exported CA units; negative favors W',
            difference=float(delta.mean()),conditional95_interval=np.quantile(delta[indices].mean(axis=1),[.025,.975]).tolist()),
        models=models,independent_ols_reconstruction=independent,bootstrap=dict(resamples=20000,seed=2026111541,unit='holdout player',
            limitation='Conditional on fixed training sample/split and exchangeability within this export; excludes training and save/club uncertainty'),
        actual_marginal_costs_identified=False,nonlinear_costs_identified=False,pa_forecast_validated=False,
        warning='Author already analyzed all109 profiles. This retrospective split is not a newly collected independent validation cohort. Predicting an export field does not identify causal attribute costs.')

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('profiles',type=Path);parser.add_argument('table',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=analyse(args.profiles,args.table)
    args.output.write_text(json.dumps(result,allow_nan=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(n=result['eligible_rows'],primary=result['primary'],weighted_holdout=result['models']['W']['holdout'])))

if __name__=='__main__':main()

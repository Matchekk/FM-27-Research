"""Preregistered complete-block Stamina x pressing pilot; no native calls."""
from hashlib import sha256
from pathlib import Path
import sys
import numpy as np
from scipy.stats import chi2, nct, t

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.stamina003 import (EXPERIMENT, ARMS, CONTEXTS, COEFFICIENTS,
                                 SECONDARY, SECONDARY_PAIRS, matrix, treatment)
from research.core import config_hash, schedule
from research.native import read, rows, require, write
from research.stats import estimate, holm, metrics

METRICS = ('xgd', *SECONDARY)
BOOTSTRAPS = 20000
BOOT_SEED = int.from_bytes(sha256(b'MECH-003-STAMINA-R0/bootstrap-v1').digest()[:8], 'little')
SCHEDULER_SEED = 2026111413


def validate_design(c):
    d, b, s = c['design'], c['budget'], c['science']
    require(c['experiment_id'] == EXPERIMENT and c['module'] == 'MECH' and c['metrics']['primary'] == 'xgd' and
            c['metrics']['secondary'] == list(SECONDARY), 'Experiment/primary drift')
    require(d['matrix'] == matrix() and d['matrix_sha256'] == config_hash(matrix()), 'Matrix drift')
    require([a['id'] for a in d['arms']] == list(ARMS) and d['control_arm'] == 'R00' and
            d['n_blocks'] == 32 and d['sides'] == [0, 1] and
            [h['id'] for h in d['scenarios']] == list(CONTEXTS), 'Sample/context drift')
    require(s['primary_contrast'] == 'STAMINA' and s['contrast_coefficients'] == {k:list(v) for k,v in COEFFICIENTS.items()} and
            s['secondary_contrasts'] == [list(x) for x in SECONDARY_PAIRS] and s['family_size'] == 7 and
            s['multiple_testing'] == 'holm' and s['alpha'] == .05 and s['power'] == .9 and
            s['min_effect'] == .3 and s['desired_full_ci_width'] == .5,
            'Contrast/family drift')
    require(s['context_weights'] == s['side_weights'] == [.5, .5] and s['bootstrap_resamples'] == BOOTSTRAPS, 'Aggregation drift')
    require(b['max_matches'] == 512 and b['max_technical_attempts'] == 33 and b['max_workers'] == 4 and
            b['timeout_seconds'] == 90 and b['total_native_wall_seconds'] == 600 and
            b['absolute_study_wall_seconds'] == 1200 and b['raw_artifact_limit_bytes'] == 2*1024**3 and
            b['disk_reserve_bytes'] == 20*1024**3, 'Budget drift')


def checked(data, receipt):
    validate_design(receipt['config'])
    expected = {j['key']:j for j in schedule(receipt)}
    require(len(expected) == 512, 'Exactly512 jobs required')
    cube = np.full((2, 32, 2, 4, len(METRICS)), np.nan)
    seen = set()
    for row in data:
        require(row['key'] in expected and row['key'] not in seen, 'Unexpected/duplicate match')
        j = expected[row['key']]; seen.add(row['key']); tr = treatment(j['arm'])
        require(row.get('experiment_id') == EXPERIMENT and row.get('input_contract_verified') is True and
                row.get('profile_fields_verified') == 1058 and row.get('native_attribute_values_verified') == 3174 and
                row.get('native_roles_verified') == row.get('native_pi_cells_verified') == 44 and
                row.get('native_pi_groups_verified') == 748 and row.get('native_stamina_values') == [tr['stamina_raw']]*10 and
                row.get('native_pressing_bit') == tr['pressing_bit'] and row.get('factor_levels') == tr['levels'] and
                row.get('design_matrix_sha256') == config_hash(matrix()) and 0 < row['finish_tick'] < 47996,
                'Native input gate missing')
        require(all(row.get(k) == v for k,v in j['identity'].items()) and
                all(row.get(k) == j[k] for k in ('setup_sha256','config_sha256','scenario','seed','arm')) and
                row['tested_side'] == j['side'], 'Identity/setup/seed drift')
        h = CONTEXTS.index(j['scenario'])
        i = receipt['seeds'][h*32:(h+1)*32].index(j['seed'])
        values = metrics(row)
        cube[h,i,j['side'],ARMS.index(j['arm'])] = [values[m] for m in METRICS]
    require(seen == set(expected) and np.isfinite(cube).all(), 'Incomplete blocks: technical status only')
    return cube


def summarize(value):
    cells = value.mean(axis=2)
    result = estimate(list(cells), resamples=BOOTSTRAPS, bootstrap_seed=BOOT_SEED)
    result['context'] = {h:dict(mean=float(cells[k].mean()), sd=float(cells[k].std(ddof=1)),
        sd_upper95_normal_model=float(cells[k].std(ddof=1)*np.sqrt(31/chi2.ppf(.05,31))),
        side0_mean=float(value[k,:,0].mean()), side1_mean=float(value[k,:,1].mean()),
        side0_sd=float(value[k,:,0].std(ddof=1)), side1_sd=float(value[k,:,1].std(ddof=1)),
        side_covariance=float(np.cov(value[k].T)[0,1])) for k,h in enumerate(CONTEXTS)}
    loo = [float((np.delete(cells[h],i).mean()+cells[1-h].mean())/2) for h in (0,1) for i in range(32)]
    result['leave_one_out'] = dict(range=[min(loo),max(loo)], max_change=max(abs(x-result['mean']) for x in loo))
    return result


def future_planning(sd):
    def case(values):
        def properties(n,effect):
            v = np.asarray(values)**2/(4*n); variance=float(v.sum())
            if not variance:return dict(full_width=0.,power=1.)
            df=float(variance**2/(v*v/(n-1)).sum()); se=np.sqrt(variance); cut=t.isf(.025,df)
            return dict(full_width=float(2*cut*se),power=float(nct.cdf(-cut,df,effect/se)+nct.sf(cut,df,effect/se)))
        result=[]
        for effect in (.2,.3):
            lo,hi=1,2
            while properties(hi,effect)['power'] < .9:
                hi*=2;require(hi<=10000000,'Unrealistic future requirement')
            while hi-lo > 1:
                mid=(lo+hi)//2
                if properties(mid,effect)['power'] >= .9:hi=mid
                else:lo=mid
            result.append(dict(effect=effect,seeds_per_context=hi,independent_blocks=2*hi,matches=16*hi,**properties(hi,effect)))
        return dict(sd=values,power90=result)
    upper=[float(s*np.sqrt(31/chi2.ppf(.025,31))) for s in sd]
    return dict(assumptions='New seeds in the two existing equal-weight contexts; conditional noncentral Welch approximation; joint95 normal-model SD upper bounds; no automatic study.',
                observed=case(sd),simultaneous95_sd_upper=case(upper))


def analyse(data, receipt):
    cube=checked(data,receipt)
    contrasts={name:np.einsum('hisam,a->hism',cube,np.asarray(weights)) for name,weights in COEFFICIENTS.items()}
    primary=summarize(contrasts['STAMINA'][:,:,:,0])
    secondary={f'{name}:{metric}':summarize(contrasts[name][:,:,:,METRICS.index(metric)]) for name,metric in SECONDARY_PAIRS}
    for key,p in zip(secondary,holm([v['p'] for v in secondary.values()]),strict=True):
        secondary[key].update(p_holm=p,reject_holm=p<=.05)
    blocks=[dict(scenario=h,seed=receipt['seeds'][j*32+i],contrast=name,endpoint=metric,
                 value=float(contrasts[name][j,i,:,METRICS.index(metric)].mean()))
            for name,metric in [('STAMINA','xgd'),*SECONDARY_PAIRS] for j,h in enumerate(CONTEXTS) for i in range(32)]
    return dict(experiment_id=EXPERIMENT,n_matches=512,independent_seed_blocks=64,primary_contrast='STAMINA',
        primary=primary,secondary=secondary,planning=future_planning([primary['context'][h]['sd'] for h in CONTEXTS]),
        arm_means={h:{a:{m:float(cube[j,:,:,k,l].mean()) for l,m in enumerate(METRICS)} for k,a in enumerate(ARMS)} for j,h in enumerate(CONTEXTS)},
        mechanism_decomposition_identified=False,career_transfer_confirmed=False,global_attribute_ranking_claimed=False,
        raw_intervention='Stamina52 raw80-minus40 at ten starting outfield players; no FM UI calibration; no raw60 baseline comparison',
        practical_effect=.3,desired_full_ci_width=.5,bootstrap=dict(seed=BOOT_SEED,resamples=BOOTSTRAPS)),blocks


if __name__ == '__main__':
    import json
    folder=ROOT/'data/mech-003-stamina'
    z,blocks=analyse(rows(folder/'main.jsonl'),read(folder/'manifest.json'))
    write(folder/'effects.json',z)
    (folder/'block-contrasts.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in blocks),encoding='utf8')

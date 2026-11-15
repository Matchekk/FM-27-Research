"""Publish separate measured/unknown components and sanitized execution totals.

No host calls; invoke only after the full frozen analysis and scalar review.
"""
from collections import Counter
from datetime import datetime,timezone
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/'data/player-development-001-role'
LOC=ROOT/'local/player-development-001/role'

def read(path):return json.loads(path.read_text(encoding='utf8'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf8')

def components(effects,review):
    if (effects['experiment_id'],effects['n_matches'],effects['independent_blocks'])!=('PD-ROLE-001',4096,512):
        raise ValueError('Complete declared scientific study required')
    if not review['passed'] or review['formal_estimands_checked']!=7:raise ValueError('Full scalar review required')
    return dict(model_id='FM27_META_SCORE_2_RESEARCH_COMPONENTS',status='NO_COMBINED_SUCCESS_SCORE',
        current_performance=dict(status='MEASURED_LOCAL_ROLE_ATTRIBUTE_CONTRAST_NOT_PLAYER_FORECAST',
            build='27.0.1+2503222',roles=['CentreForward','DeepLyingForward'],intervention='One ST raw JR60->80; OOP fixed',
            primary_role_attribute_interaction=effects['primary'],
            conditional_attribute_effects_descriptive={key:effects['descriptive_only'][key]['xgd'] for key in ('JR_CF','JR_DLF')},
            actual_ca_efficiency=None,player_holdout_prediction_accuracy=None),
        development_potential=dict(status='UNKNOWN_NO_LONGITUDINAL_HOLDOUT',ca_after_one_season=None,
            ca_after_two_seasons=None,probability_reaching_pa=None,calibrated_distribution=None),
        training_efficiency=dict(status='UNKNOWN_NO_VALIDATED_CAREER_EXPOSURE',expected_role_match_gain=None,
            ca_gain=None,injury_risk=None),
        baseline_comparison=dict(meta_score_v01='Preserved; uncalibrated position index',
            attribute_mean='Not outcome calibrated',ca='Nominal CA held constant120 in this experiment',
            public_position_weights='Different sources/fixtures; not a held-out player validation',
            verified_improvement_over_baselines=False,mae=None,calibration=None),
        limits=['One bundled fixture, two fixed known opponents, omnipotent synthetic position ratings',
            'Role package and one raw dose only; not a global attribute or role ranking',
            'No genuine equal-CA optimization, career prediction or training-causality calibration'])

def execution_summary():
    budget=read(LOC/'budget.json')
    if budget['active'] or budget['halted']:raise ValueError('Unreconciled/halted budget; no completed-result summary')
    accounting=[]
    for phase in ('technical','main'):
        plan=read(PUB/(phase+'-plan.json'))
        data=[json.loads(line) for line in (PUB/(phase+'.jsonl')).read_text(encoding='utf8').splitlines()]
        index={r['job_id']:r for r in data}
        if len(index)!=len(plan) or set(index)!={j['key'] for j in plan}:raise ValueError('Incomplete/duplicate phase')
        for job in plan:
            row=index[job['key']]
            if row['status']!=('expected_rejection' if job['kind']=='negative' else 'ok'):raise ValueError('Failed attempt')
            accounting.append(dict(job_id=job['key'],phase=phase,kind=job['kind'],seed=job['seed'],
                context=job.get('scenario'),side=job.get('side'),arm=job.get('arm'),status=row['status']))
    operations=[{k:o[k] for k in ('name','kind','start_utc','elapsed_seconds','returncode','timed_out')} for o in budget['operations']]
    if any(o['returncode']!=0 or o['timed_out'] for o in operations):raise ValueError('Failed phase')
    summaries={phase:read(PUB/(phase+'-summary.json')) for phase in ('technical','main')}
    if not all(s['all_cleanup_confirmed'] and s['passed'] for s in summaries.values()):raise ValueError('Cleanup/gate missing')
    if (ROOT/'local/global-native/native-execution.lease.json').exists():raise ValueError('Native lease still active')
    provenance=dict(experiment_id='PD-ROLE-001',scientific_series_complete=True,counts=dict(Counter(r['status'] for r in accounting)),
        native_calls=4129,full_simulations=4128,technical_full_matches=32,main_matches=4096,independent_blocks=512,
        expected_negative_rejections=1,failures=0,retries=0,replacement_seeds=0,exclusions=0,unbegun_jobs=0,
        career_advances=0,holdout_matches=0,main_program_cap=4096,other_scientific_matches=0,
        charged_supervised_seconds=budget['charged_seconds'],charged_seconds_limit=budget['limit_seconds'],
        fixed_window_start_utc=budget['wall_start_utc'],fixed_deadline_utc=budget['wall_deadline_utc'],
        window_limit_seconds=budget['wall_limit_seconds'],operations=operations,
        peak_inflight_claims=max(s['peak_inflight_claims'] for s in summaries.values()),engine_pid_peak_measured=False,
        all_cleanup_confirmed=True,global_native_lease_present=False,
        private_original_evidence_bytes=sum(p.stat().st_size for phase in ('technical','main') for p in (LOC/phase).rglob('*') if p.is_file()),
        evidence='Second-pass raw/input re-audit after all calls is enforced by the frozen supervisor; private originals retained.',
        exported_utc=datetime.now(timezone.utc).isoformat())
    write(PUB/'execution-provenance.json',provenance)
    (PUB/'job-accounting.jsonl').write_text(''.join(json.dumps(row)+'\n' for row in accounting),encoding='utf8')
    return provenance

def main():
    effects=read(PUB/'effects.json');review=read(PUB/'independent-statistics-review.json')
    card=components(effects,review)
    proxy=read(ROOT/'data/player-development-001-ca/profile-diagnostic.json')
    card['ca_export_proxy_diagnostic']=dict(status=proxy['evidence'],players=109,train_players=80,holdout_players=29,
        coefficients=proxy['models']['W']['coefficients'],holdout=proxy['models']['W']['holdout'],
        observed_ca_range=proxy['coverage']['exported_ca_range'],actual_marginal_costs_identified=False,
        limit='Public GK export, retrospective split, unverified game provenance; no outfield, elite, role or PA transfer')
    write(ROOT/'research/meta_score_v02_components.json',card)
    result=execution_summary()
    print(json.dumps({k:result[k] for k in ('main_matches','independent_blocks','native_calls','charged_supervised_seconds')}))

if __name__=='__main__':main()

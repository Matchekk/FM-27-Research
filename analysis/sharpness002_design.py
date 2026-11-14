"""Pure intentions/contracts for a separate sharpness start-package pilot.

No runner, server import, memory setter, seed allocation or file mutation exists
here. An unchanged original record codec is reused only as an offline compiler.
"""
from itertools import product
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.core import config_hash,validate
from research.startpolicy import StartPolicy,decode_records,encode_records,encode_startpolicy,require

EXPERIMENT='MECH-002-SHARPNESS-P0'
CONTEXTS=('high_press','deep_block')
ARMS=('S70-P0','S100-P0','S70-P1','S100-P1')
LEVELS=((-1,-1),(1,-1),(-1,1),(1,1))
OBSERVER_HOST='58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
PRESS_IDS=(1313689463,2000905329)
COEFFICIENTS={'SHARPNESS':(-.5,.5,-.5,.5),'PRESS':(-.5,-.5,.5,.5),'SHARPNESSxPRESS':(1.,-1.,-1.,1.)}
SECONDARY=('points','gf','ga','xgf','xga')
SECONDARY_PAIRS=(*(('SHARPNESS',m) for m in SECONDARY),('PRESS','xgd'),('SHARPNESSxPRESS','xgd'))
DESCRIPTIVE=tuple(f'{stage}_{metric}_mean' for stage in ('prepared','first','finished')
    for metric in ('condition_cache89','sharpness_cache8a'))+(
    'prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00','finished_tf33_distinct_hashes',
    *(f'finished_{field}_mean' for field in ('condition_raw','sharpness_raw','sharpness_secondary_raw',
       'fatigue_raw','condition_accumulator_raw','sharpness_penalty_raw')))
HASH=re.compile('[0-9a-f]{64}\\Z')


def matrix():
    return [dict(id=a,levels={'SHARPNESS':s,'PRESS':p},sharpness_raw=10000 if s==1 else 7000,
        pressing_id=PRESS_IDS[int(p==1)],pressing_bit=66 if p==1 else 0)
        for a,(s,p) in zip(ARMS,LEVELS,strict=True)]


def treatment(arm):
    require(arm in ARMS,'Unknown sharpness/pressing arm')
    return matrix()[ARMS.index(arm)]


def build_inputs(d00_bytes,more_bytes,tested_side):
    """Restore original R01 raw40 stamina, then compile only declared changes."""
    require(type(tested_side) is int and tested_side in (0,1),'Invalid tested side')
    base,more=decode_records(d00_bytes),decode_records(more_bytes)
    require(len(base)==len(more)==5557 and not any(r[0]==61 for r in (*base,*more)),
            'Only frozen D00 record layout, no execution records')
    lineups={(s,a):v for k,s,a,b,v in base if k==11 and b==0}
    require(len([r for r in base if r[0]==11])==22 and set(lineups)==set(product((0,1),range(11))),
            'Absolute roster/lineup bindings missing')
    require(all(len({lineups[s,i] for i in range(11)})==11 for s in (0,1)),'Duplicate starting actor')
    affected={lineups[tested_side,i] for i in range(1,11)}
    stamina=[(s,a,v) for k,s,a,b,v in base if k==1 and b==52]
    require(len(stamina)==46 and {(s,a) for s,a,_ in stamina}==
            {(s,a) for s in (0,1) for a in range(23)} and all(v==60 for _,_,v in stamina),
            'Exactly46 active encoded D00 stamina60 records,23 per side, required')
    restored=[];changed=0
    for row in more:
        k,s,a,b,v=row
        if k==1 and s==tested_side and a in affected and b==52:
            require(v==40,'Original R01 must contain exactly the declared raw40 stamina')
            row=(k,s,a,b,60);changed+=1
        restored.append(row)
    require(changed==10,'Exactly ten R01 stamina values must be restored')
    differences=[(a,b) for a,b in zip(base,restored,strict=True) if a!=b]
    require(differences==[((2,tested_side,10,0,PRESS_IDS[0]),(2,tested_side,10,0,PRESS_IDS[1]))],
            'Restored MoreOften carrier differs from D00 beyond one pressing record')
    require(encode_records(base)==d00_bytes and encode_startpolicy(base,StartPolicy(tested_side,10000))==d00_bytes,
            'Explicit high start package must be byte-identical to D00')
    result={}
    for arm in ARMS:
        tr=treatment(arm);records=restored if tr['pressing_bit'] else base
        result[arm]=encode_startpolicy(records,StartPolicy(tested_side,tr['sharpness_raw']))
    return result


def technical_jobs(seeds):
    require(type(seeds) is list and len(seeds)==len(set(seeds))==4 and
            all(type(s) is int and 0<s<=0xffffffff for s in seeds),'Four separate new technical seeds required')
    jobs=[dict(key=f'tech-{h}-s{s}-{a}-r{r}',job_id=f'tech-{h}-s{s}-{a}-r{r}',scenario=h,context=h,
        side=s,team_side=s,arm=a,seed=seeds[i],repeat=r,kind='full')
        for i,(h,s) in enumerate(product(CONTEXTS,(0,1))) for a,r in product(ARMS,(0,1))]
    return jobs+[dict(key='negative-malformed',job_id='negative-malformed',kind='negative',seed=None)]


def contract_definition(identity=None,setups=None):
    c=dict(schema_version=1,experiment_id=EXPERIMENT,module='MECH',kind='native',stage='discovery',status='draft',
        hypothesis='The verified raw10000 versus raw7000 original twenty-record start package changes mean xGD over two pressing levels.',
        control='S70-P0: tested starting ten outfield actors raw7000 in both original sharpness profile fields16/17; Standard pressing.',
        intervention='Full2x2 raw7000/10000 start package and Standard/MoreOften pressing; original stamina60 in all46 active encoded player records. No assigned value is claimed for unencoded carrier slots.',
        conditions='Frozen D00 IP4231/OOP4411, phases/roles/PI/profiles/positions/GK/bench/opponent/management unchanged except twenty sharpness values and one pressing value. Bundled fixture; no warmworker, Kind61, new setter or clamp.',
        seed_namespace=EXPERIMENT+'/main-v1',identity=identity,
        metrics=dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),
        design=dict(unit='seed_block',n_blocks=32,sides=[0,1],control_arm=ARMS[0],matrix=matrix(),matrix_sha256=config_hash(matrix()),
            arms=[dict(id=a,setup_sha256=config_hash({h:{s:v[a] for s,v in by.items()} for h,by in setups.items()}) if setups is not None else None) for a in ARMS],setups=setups,
            scenarios=[dict(id=h,opponent=h,strength='Frozen identical synthetic D00 roster strength',split='discovery') for h in CONTEXTS]),
        science=dict(alpha=.05,power=.9,min_effect=.3,desired_full_ci_width=.5,multiple_testing='holm',family_size=7,
            primary_contrast='SHARPNESS',contrast_coefficients={k:list(v) for k,v in COEFFICIENTS.items()},
            secondary_contrasts=[list(v) for v in SECONDARY_PAIRS],context_weights=[.5,.5],side_weights=[.5,.5],bootstrap_resamples=20000,
            analysis='Marginal high-minus-low xGD; paired complete seed blocks, equal contexts, Welch95 and stratified full-block bootstrap20000. Exactly Holm7 secondary. Context/side/leave-one-out/descriptive only exploratory.',
            exclusions='None. Any input/identity/seed/native error stops; no replacement, retry or silent zero. Only complete512 main observations allow effect estimates.',
            negative_controls=['Four fresh technical seeds,32 full matches/16 exact A/A pairs','One malformed binary: exit108 plus unique scenario_rejected, no natural finish'],
            readback_fields=['All3174attributes/1058profile fields/44phase cells/748PIgroups','Original raw C90/C7A plus actual starter cache89/8A prepared and first advance','Stamina60, press0/66, seed/setup/actor identity, frozen nonsharpness controls and rawTF33','Natural finished score/xG/statistics'],
            stopping_rule='512main plus32technical and1negative; one cold supervisor,max4workers90s;900childsec/3600UTCfrom first native technical;main admission>=600sec remaining own/global child/UTC allowance;NIGHT1800sec+23UTC;stop first failed gate.',
            selection_rule='No candidate/winner/holdout/career/UI/consumer/fatigue-mediation claim; total effect of the verified original start package only.',
            power_basis='Unknown contrast variance; practical reference .30xGD and desired full95width .50, no90%power guarantee. Future new-seed planning for .20/.30 using observed SD and simultaneous normal-model95upper SD bounds.'),
        budget=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
            absolute_study_wall_seconds=3600,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
            raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',
            global_child_seconds=1800,global_deadline_utc='2026-11-14T23:00:00+00:00'),
        native_spec=dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,profile_fields=[16,17],
            raw_levels=[7000,10000],stamina_index=52,stamina_raw=60,encoded_stamina_records=46,kind61_allowed=False,new_setter_allowed=False,
            ongoing_clamp_allowed=False,ui_scale_calibrated=False,consumer_semantics_validated=False),
        seed_plan=dict(main_blocks=64,technical_seeds=4,total_new_seeds=68,technical_namespace=EXPERIMENT+'/technical-v1',
            technical_seeds_reserved=None,main_seeds_reserved=None,
            excluded_sources=['All historical/technical/failed/previously reserved namespaces and pending global registry entries',
                'All four MECH-002-STARTPOLICY-TECH-V1 seeds','All64 unused terminal MECH-003-STAMINA-R0 main seeds',
                'All holdout seed metadata; do not open or simulate holdout opponents']),
        gates=dict(tech17=dict(experiment_id='MECH-002-STARTPOLICY-TECH-V1',passed=False,independently_released=False,
            release_commit=None,ci_run=None,summary_sha256=None,review_sha256=None)),
        preregistration=dict(commit=None,document='experiments/MECH-002-sharpness-pilot.md',document_sha256=None,
            analysis='analysis/analyse_sharpness002.py',analysis_sha256=None),execution=None)
    validate_design(c)
    return c


def validate_design(c,executable=False):
    validate(c,executable=executable)
    d,b,s=c['design'],c['budget'],c['science']
    require(c['experiment_id']==EXPERIMENT and c['module']=='MECH' and c['stage']=='discovery' and
        c['metrics']==dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),'Experiment/endpoints drift')
    require(d['matrix']==matrix() and d['matrix_sha256']==config_hash(matrix()) and d['n_blocks']==32 and
        d['sides']==[0,1] and d['control_arm']==ARMS[0] and [a['id'] for a in d['arms']]==list(ARMS) and
        [h['id'] for h in d['scenarios']]==list(CONTEXTS),'Factorial/context/sample drift')
    require(s['primary_contrast']=='SHARPNESS' and s['contrast_coefficients']=={k:list(v) for k,v in COEFFICIENTS.items()} and
        s['secondary_contrasts']==[list(v) for v in SECONDARY_PAIRS] and s['family_size']==7 and s['multiple_testing']=='holm' and
        s['alpha']==.05 and s['power']==.9 and s['min_effect']==.3 and s['desired_full_ci_width']==.5 and
        s['bootstrap_resamples']==20000 and s['context_weights']==s['side_weights']==[.5,.5],'Scientific contrast/family drift')
    require(b==dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
        absolute_study_wall_seconds=3600,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
        raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',
        global_child_seconds=1800,global_deadline_utc='2026-11-14T23:00:00+00:00'),'Resource/admission drift')
    require(c['native_spec']==dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,profile_fields=[16,17],
        raw_levels=[7000,10000],stamina_index=52,stamina_raw=60,encoded_stamina_records=46,kind61_allowed=False,new_setter_allowed=False,
        ongoing_clamp_allowed=False,ui_scale_calibrated=False,consumer_semantics_validated=False),'Native intervention drift')
    require(c['seed_namespace']==EXPERIMENT+'/main-v1' and
        c['seed_plan']['technical_namespace']==EXPERIMENT+'/technical-v1' and
        c['seed_plan']['main_blocks']==64 and c['seed_plan']['technical_seeds']==4 and
        c['seed_plan']['total_new_seeds']==68,'Seed design/namespace drift')
    g=c['gates']['tech17']
    require(g['experiment_id']=='MECH-002-STARTPOLICY-TECH-V1','Wrong prerequisite study')
    if executable:
        require(g['passed'] is True and g['independently_released'] is True and type(g['ci_run']) is int and g['ci_run']>0 and
            type(g['release_commit']) is str and re.fullmatch('[0-9a-f]{40}',g['release_commit']) and
            all(type(g[k]) is str and HASH.fullmatch(g[k]) for k in ('summary_sha256','review_sha256')),
            'TECH17 actual completion and independent published release required')
        e=c['execution']
        require(type(e) is dict and e.get('runner')=='analysis/run_sharpness002.py' and e.get('kind')=='cold_direct_cli' and
            type(e.get('workers')) is int and e['workers']==4 and type(e.get('max_processes_per_job')) is int and
            e['max_processes_per_job']==3 and type(e.get('code_sha256')) is dict and e['code_sha256'] and
            all(type(v) is str and HASH.fullmatch(v) for v in e['code_sha256'].values()) and
            all(type(e.get(k)) is str and HASH.fullmatch(e[k]) for k in ('input_manifest_sha256','seed_plan_sha256')),
            'Frozen cold-direct runner/input/seed provenance missing')
    return c

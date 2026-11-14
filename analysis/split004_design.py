"""Frozen intentions and readback gates for separately varied sharpness fields.

No process, seed allocation, server import, native setter or file mutation.
The original record setters and passive observer remain unchanged.
"""
from itertools import product
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.core import config_hash, validate
from research.startpolicy import StartPolicy, decode_records, encode_records, encode_startpolicy, require
from research.passive_observer import audit_trace, canonical_hash, match_result, snapshot
from research.native import event
from analysis import run_observer005 as observer
from analysis.sharpness002_runner import initial_controls, descriptive, repeat_equivalence
from analysis.startpolicy002_gate import lineup_slots, cache_bytes

EXPERIMENT = 'MECH-004-SPLIT-R0'
CONTEXTS = ('high_press', 'deep_block')
ARMS = ('C90L-C7AL', 'C90H-C7AL', 'C90L-C7AH', 'C90H-C7AH')
LEVELS = ((-1,-1), (1,-1), (-1,1), (1,1))
OBSERVER_HOST = '58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
COEFFICIENTS = {'ATTRIBUTION': (0.,1.,-1.,0.), 'C90':(-.5,.5,-.5,.5),
                'C7A':(-.5,-.5,.5,.5), 'INTERACTION':(1.,-1.,-1.,1.)}
SECONDARY = ('points','gf','ga','xgf','xga')
SECONDARY_PAIRS = (('C90','xgd'),('C7A','xgd'),('INTERACTION','xgd'),
                   *(('ATTRIBUTION',m) for m in SECONDARY))
DESCRIPTIVE = tuple(f'{stage}_{metric}_mean' for stage in ('prepared','first','finished')
    for metric in ('condition_cache89','sharpness_cache8a')) + (
    'prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00','finished_tf33_distinct_hashes',
    *(f'finished_{field}_mean' for field in ('condition_raw','sharpness_raw','sharpness_secondary_raw',
       'fatigue_raw','condition_accumulator_raw','sharpness_penalty_raw')))
HASH = re.compile('[0-9a-f]{64}\\Z')


def matrix():
    return [dict(id=arm, levels={'C90':a,'C7A':b},c90_raw=10000 if a==1 else 7000,
                 c7a_raw=10000 if b==1 else 7000)
            for arm,(a,b) in zip(ARMS,LEVELS,strict=True)]


def treatment(arm):
    require(arm in ARMS,'Unknown split arm')
    return matrix()[ARMS.index(arm)]


def build_inputs(d00_bytes, side):
    """Write only each declared original profile field for ten bound starters."""
    require(type(side) is int and side in (0,1),'Invalid tested side')
    records = decode_records(d00_bytes)
    require(len(records)==5557 and not any(r[0]==61 for r in records),'Only original D00 record layout')
    # Existing strict validator proves complete standard baseline profiles/lineups.
    require(encode_startpolicy(records,StartPolicy(side,10000))==d00_bytes,'Nonstandard D00 baseline')
    slots = lineup_slots(d00_bytes)
    targets = {slots[side,i] for i in range(1,11)}
    stamina = [(s,a,v) for k,s,a,b,v in records if k==1 and b==52]
    require(len(stamina)==46 and {(s,a) for s,a,_ in stamina}==set(product((0,1),range(23)))
            and all(v==60 for _,_,v in stamina),'Exactly46 encoded stamina60 values required')
    require([(s,a,b,v) for k,s,a,b,v in records if k==2 and s==side and a==10]==
            [(side,10,0,1313689463)],'Standard pressing on tested side required')
    result = {}
    for arm in ARMS:
        tr = treatment(arm)
        changed = tuple((k,s,a,b,tr['c90_raw'] if b==16 else tr['c7a_raw'])
            if k==15 and s==side and a in targets and b in (16,17) else (k,s,a,b,v)
            for k,s,a,b,v in records)
        differences = [(a,b) for a,b in zip(records,changed,strict=True) if a!=b]
        expected = {(15,side,a,f,v) for a in targets for f,v in ((16,tr['c90_raw']),(17,tr['c7a_raw'])) if v!=10000}
        require({b for _,b in differences}==expected and len(differences)==len(expected)
                and all(a[:4]==b[:4] and a[4]==10000 for a,b in differences),'Undeclared record mutation')
        result[arm] = encode_records(changed)
    require(result[ARMS[-1]]==d00_bytes,'High/high must equal D00 bytes')
    return result


def technical_jobs(seeds):
    require(type(seeds) is list and len(seeds)==len(set(seeds))==4 and
            all(type(s) is int and 0<s<=0xffffffff for s in seeds),'Four new technical seeds required')
    jobs = [dict(key=f'tech-{h}-s{s}-{a}-r{r}',job_id=f'tech-{h}-s{s}-{a}-r{r}',
        scenario=h,context=h,side=s,team_side=s,arm=a,seed=seeds[i],repeat=r,kind='full')
        for i,(h,s) in enumerate(product(CONTEXTS,(0,1))) for a,r in product(ARMS,(0,1))]
    return jobs + [dict(key='negative-malformed',job_id='negative-malformed',kind='negative',seed=None)]


def audit_split_state(evidence,binary,side,c90,c7a):
    """Require independent raw survival; runtime cache is observed, never imposed."""
    require(type(side) is int and side in (0,1) and c90 in (7000,10000) and c7a in (7000,10000),
            'Invalid split state')
    slots = lineup_slots(binary);targets={slots[side,i] for i in range(1,11)}
    captures = [r for r in evidence if r.get('event')=='native_passive_state']
    require([r['stage'] for r in captures]==['prepared','first_advance','finished'],'Three captures required')
    checks = []
    for row in captures[:2]:
        bound = snapshot(row)
        require({(p['side'],p['roster_index']) for p in bound.values()}==set(product((0,1),range(23))),
                'Exactly46 original active actor bindings required')
        cache = []
        for p in bound.values():
            target = p['side']==side and p['roster_index'] in targets
            require(p['sharpness_raw']==(c90 if target else 10000) and
                    p['sharpness_secondary_raw']==(c7a if target else 10000),
                    'Independent raw fields collapsed or failed to transfer')
            require(p['condition_raw']==10000 and p['fatigue_raw']==0 and
                    p['condition_accumulator_raw']==1000000 and p['sharpness_penalty_raw']==0,
                    'Nonsharpness starting control changed')
            if (p['side'],p['roster_index']) in {(s,slots[s,i]) for s in (0,1) for i in range(11)}:
                condition,sharpness=cache_bytes(p)
                require(condition==100,'Starting condition cache changed')
                if target:cache.append(sharpness)
        require(len(cache)==10,'Ten observed target cache bytes required')
        checks.append(dict(stage=row['stage'],players_verified=46,target_actors=10,
            target_cache8a_values=cache,capture_sha256=canonical_hash(row)))
    return dict(independent_raw_transfer_verified=True,c90_raw=c90,c7a_raw=c7a,
                snapshots=checks,cache_mapping_assumed=False,ui_scale_calibrated=False)


def audit_job(evidence,dump,job,binary,config,catalog,oop_map,frozen_controls,observer_sha256):
    require(observer_sha256==OBSERVER_HOST,'Observer host drift')
    require(event(evidence,'native_image_fingerprint')['sha256']==job['identity']['engine_sha256'],
            'Loaded engine drift')
    require(event(evidence,'native_engine_compatibility')['compatible'] is True and
            event(evidence,'windows_load_returned')['success'] is True,'Native loader gate failed')
    phases = [r for r in evidence if r.get('event')=='native_phase_configuration']
    require(len(phases)==4 and {(r['side'],r['phase']) for r in phases}==set(product((0,1),(0,1))),
            'All native phase receipts required')
    checked=observer.audit_input(evidence,dump,config,binary,catalog,oop_map)
    audit_trace(evidence,dump,job['seed'])
    tr=treatment(job['arm']);audit_split_state(evidence,binary,job['side'],tr['c90_raw'],tr['c7a_raw'])
    require(all(type(p['attributes'][52]) is int and p['attributes'][52]==60
                for team in dump['teams'] for p in team['players']),'Stamina60 changed')
    require(config['teams'][job['side']]['instructions']['10']==1313689463,
            'Only Standard pressing on tested side allowed')
    require(initial_controls(evidence)==frozen_controls,'Initial nonsharpness/rawTF33 controls changed')
    values,missing=descriptive(evidence,binary,job['side'])
    return dict(job_id=job['key'],experiment_id=EXPERIMENT,context=job['scenario'],team_side=job['side'],
        seed=job['seed'],arm=job['arm'],status='ok',config_sha256=job['config_sha256'],
        setup_sha256=job['setup_sha256'],identity=job['identity'],observer_host_sha256=observer_sha256,
        result={k:v for k,v in match_result(evidence,job['seed']).items() if k!='seed'},
        native_audit=dict(input_verified=True,seed_verified=True,split_start_verified=True,
            stamina60_verified=True,pressing_verified=True,controls_verified=True,
            attribute_values_verified=checked['attribute_values_verified'],profile_fields_verified=checked['profile_fields_verified'],
            phase_cells_verified=checked['phase_cells_verified'],pi_groups_verified=checked['pi_groups_verified'],
            c90_raw=tr['c90_raw'],c7a_raw=tr['c7a_raw'],pressing_bit=0),
        descriptive=values,descriptive_missing_reasons=missing)


def contract_definition(identity=None,setups=None):
    c = dict(schema_version=1,experiment_id=EXPERIMENT,module='MECH',kind='native',stage='discovery',status='draft',
        hypothesis='The C90 high-minus-low xGD effect differs from the C7A high-minus-low effect in independently preserved original start fields.',
        control=ARMS[0]+': both original profile fields7000 in ten tested starting outfield actors; Standard pressing.',
        intervention='Full2x2 original C90(field16) and C7A(field17), each7000/10000 before original preparation. No new setter, clamp or postpreparation write.',
        conditions='Frozen D00 IP4231/OOP4411, both known discovery opponents/sides, original management. Only the declared ten or twenty raw sharpness records change; all46 encoded stamina values60.',
        seed_namespace=EXPERIMENT+'/main-v1',identity=identity,
        metrics=dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),
        design=dict(unit='seed_block',n_blocks=32,sides=[0,1],control_arm=ARMS[0],matrix=matrix(),matrix_sha256=config_hash(matrix()),
            arms=[dict(id=a,setup_sha256=config_hash({h:{s:v[a] for s,v in by.items()} for h,by in setups.items()}) if setups else None) for a in ARMS],
            setups=setups,scenarios=[dict(id=h,opponent=h,strength='Frozen identical synthetic D00 roster strength',split='discovery') for h in CONTEXTS]),
        science=dict(alpha=.05,power=.9,min_effect=.2,desired_full_ci_width=.5,multiple_testing='holm',family_size=8,
            primary_contrast='ATTRIBUTION',contrast_coefficients={k:list(v) for k,v in COEFFICIENTS.items()},
            secondary_contrasts=[list(v) for v in SECONDARY_PAIRS],context_weights=[.5,.5],side_weights=[.5,.5],bootstrap_resamples=20000,
            analysis='Primary C90 marginal effect minus C7A marginal effect = HL-LH xGD. Complete paired seed blocks; equal sides/contexts; Welch95 and stratified block bootstrap20000. Exactly Holm8 secondary tests.',
            exclusions='None. Any raw collapse, input/identity/seed/native failure stops; no replacement, retry or zero imputation. Only complete512 main observations allow scientific effect estimates.',
            negative_controls=['32 technical full matches, all16 cells twice,16 exact A/A pairs','One malformed binary: unique scenario_rejected and exit108, no natural finish'],
            readback_fields=['All3174attributes/1058profile fields/44phase cells/748PIgroups','C90 and C7A separately after preparation and first advance','Ten target cache8A bytes observed empirically; no field-to-cache mapping assumed','Stamina60, Standard pressing, all initial nonsharpness/rawTF33 controls','Natural finish, actual score and original team statistics'],
            stopping_rule='32technical+1negative then independently published technical release/CI before512main. Own900childsec/5400UTCsec, four cold workers90s; first main needs600s own/global child/UTC remaining. Global NIGHT0023600childsec/15Nov07Z. Any failure terminal for this study.',
            selection_rule='No winner, UI calibration, consumer attribution, real-career transfer or automatic sample increase. A field effect is a total effect of the raw start intervention, not proof of an internal consumer.',
            power_basis='Unknown split contrast variance.64blocks: Welch full95width≈0.50/0.75 at equal context SD1/1.5. Practical reference0.20xGD; desired full95width0.50. This is a variance pilot with no90%power guarantee.'),
        budget=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
            absolute_study_wall_seconds=5400,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
            raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',
            global_child_seconds=3600,global_deadline_utc='2026-11-15T07:00:00+00:00'),
        native_spec=dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,profile_fields=[16,17],raw_levels=[7000,10000],
            stamina_index=52,stamina_raw=60,encoded_stamina_records=46,kind61_allowed=False,new_setter_allowed=False,
            ongoing_clamp_allowed=False,ui_scale_calibrated=False,consumer_semantics_validated=False,cache_mapping_assumed=False),
        seed_plan=dict(main_blocks=64,technical_seeds=4,total_new_seeds=68,technical_namespace=EXPERIMENT+'/technical-v1',
            technical_seeds_reserved=None,main_seeds_reserved=None),
        # These immutable preregistration flags record the pending state. Actual
        # later transfer/main release is separate published evidence, never a
        # retroactive rewrite of this registered scientific contract.
        gates=dict(independent_fields_native_verified=False,technical_independently_released=False),
        preregistration=dict(commit=None,document='experiments/MECH-004-split-preregistration.md',document_sha256=None,
            analysis='analysis/analyse_split004.py',analysis_sha256=None),execution=None)
    validate_design(c)
    return c


def validate_design(c,executable=False):
    validate(c,executable=executable)
    d,b,s=c['design'],c['budget'],c['science']
    require(c['experiment_id']==EXPERIMENT and c['module']=='MECH' and c['stage']=='discovery' and
            c['metrics']==dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),
            'Experiment/endpoint drift')
    require(d['matrix']==matrix() and d['matrix_sha256']==config_hash(matrix()) and d['n_blocks']==32
            and d['sides']==[0,1] and d['control_arm']==ARMS[0] and [a['id'] for a in d['arms']]==list(ARMS)
            and [h['id'] for h in d['scenarios']]==list(CONTEXTS),'Design/sample drift')
    require(s['primary_contrast']=='ATTRIBUTION' and s['contrast_coefficients']=={k:list(v) for k,v in COEFFICIENTS.items()}
            and s['secondary_contrasts']==[list(v) for v in SECONDARY_PAIRS] and s['family_size']==8 and s['multiple_testing']=='holm'
            and s['alpha']==.05 and s['power']==.9 and s['min_effect']==.2 and s['desired_full_ci_width']==.5
            and s['bootstrap_resamples']==20000 and s['context_weights']==s['side_weights']==[.5,.5],
            'Scientific contrast/family drift')
    require(b==dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
        absolute_study_wall_seconds=5400,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
        raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',global_child_seconds=3600,
        global_deadline_utc='2026-11-15T07:00:00+00:00'),'Budget drift')
    require(c['native_spec']==dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,profile_fields=[16,17],raw_levels=[7000,10000],
        stamina_index=52,stamina_raw=60,encoded_stamina_records=46,kind61_allowed=False,new_setter_allowed=False,
        ongoing_clamp_allowed=False,ui_scale_calibrated=False,consumer_semantics_validated=False,cache_mapping_assumed=False),
        'Native intervention drift')
    require(c['seed_namespace']==EXPERIMENT+'/main-v1' and c['seed_plan']['technical_namespace']==EXPERIMENT+'/technical-v1'
            and [c['seed_plan'][k] for k in ('main_blocks','technical_seeds','total_new_seeds')]==[64,4,68],
            'Seed namespace/count drift')
    if executable:
        e=c['execution']
        require(type(e) is dict and e.get('runner')=='analysis/run_split004.py' and e.get('kind')=='cold_direct_cli'
                and type(e.get('workers')) is int and e['workers']==4 and type(e.get('max_processes_per_job')) is int
                and e['max_processes_per_job']==3 and type(e.get('code_sha256')) is dict and e['code_sha256']
                and all(type(v) is str and HASH.fullmatch(v) for v in e['code_sha256'].values())
                and all(type(e.get(k)) is str and HASH.fullmatch(e[k]) for k in ('input_manifest_sha256','seed_plan_sha256')),
                'Frozen execution provenance required')
    return c

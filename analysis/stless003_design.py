"""Own bounded IP/OOP package compiler and technical gates, no native execution."""
from copy import deepcopy
from itertools import product
from pathlib import Path
import re
import struct
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.core import config_hash,validate
from research.startpolicy import StartPolicy,decode_records,encode_records,encode_startpolicy,require
from research.passive_observer import audit_trace,match_result
from research.native import event
from analysis import run_observer005 as observer
from analysis.sharpness002_runner import initial_controls,descriptive,repeat_equivalence
from analysis.startpolicy002_gate import audit_start_state,lineup_slots

EXPERIMENT='TACT-003-STLESS-R0'
CONTEXTS=('high_press','deep_block')
ARMS=('I0-O0','I1-O0','I0-O1','I1-O1')
LEVELS=((-1,-1),(1,-1),(-1,1),(1,1))
OBSERVER_HOST='58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32'
COEFFICIENTS={'INTERACTION':(1.,-1.,-1.,1.),'IP':(-.5,.5,-.5,.5),'OOP':(-.5,-.5,.5,.5)}
SECONDARY=('points','gf','ga','xgf','xga')
SECONDARY_PAIRS=(('IP','xgd'),('OOP','xgd'),*(('INTERACTION',m) for m in SECONDARY))
DESCRIPTIVE=tuple(f'{stage}_{metric}_mean' for stage in ('prepared','first','finished')
    for metric in ('condition_cache89','sharpness_cache8a'))+(
    'prepared_tf33_matches_frozen_d00','first_tf33_matches_frozen_d00','finished_tf33_distinct_hashes',
    *(f'finished_{field}_mean' for field in ('condition_raw','sharpness_raw','sharpness_secondary_raw',
       'fatigue_raw','condition_accumulator_raw','sharpness_penalty_raw')))
HASH=re.compile('[0-9a-f]{64}\\Z')


def matrix():
    return [dict(id=arm,levels={'IP':ip,'OOP':oop},ip_strikerless=ip==1,oop_strikerless=oop==1)
            for arm,(ip,oop) in zip(ARMS,LEVELS,strict=True)]


def treatment(arm):
    require(arm in ARMS,'Unknown strikerless package arm')
    return matrix()[ARMS.index(arm)]


def validate_cells(config,side,catalog):
    """Static original-catalog legality only; not a native legality receipt."""
    require(type(side) is int and side in (0,1),'Invalid tested side')
    require(config.get('rules')=='game' and config.get('fixture')=='bundled_match_pkm',
            'Original game rules and bundled fixture required')
    require('experimental_execution' not in config and 'away_tactic_pool' not in config,'Experimental controls forbidden')
    positions={p['id']:p['mask'] for p in catalog['positions']};roles={r['id']:r for r in catalog['roles']}
    team=config['teams'][side]
    require(len(team['phases'])==2,'Two phases required')
    for phase,cells in enumerate(team['phases']):
        require(len(cells)==11 and len({c['position'] for c in cells})==11,'Eleven distinct occupied positions required')
        require(sum(c['position']=='GK' for c in cells)==1,'Exactly one keeper required')
        cb=sum(bool(positions[c['position']]&16) for c in cells);dm=sum(bool(positions[c['position']]&128) for c in cells)
        key=f'{3 if cb>=3 else 0}:{int(dm==1)}'
        for cell in cells:
            require(cell['role'] in roles and roles[cell['role']]['phase']==phase and
                    cell['role'] in catalog['role_eligibility_context'][key][cell['position']][phase],
                    'Static original role/position/formation eligibility failed')
    return config


def build_configs(base_config,side,catalog):
    validate_cells(base_config,side,catalog)
    team=base_config['teams'][side]
    require([(team['phases'][p][i]['position'],team['phases'][p][i]['role']) for p,i in ((0,8),(0,10),(1,8),(1,10))]==
            [('AMC','AttackingMidfielder'),('ST','CentreForward'),('AMC','OPAttackingMidfielder'),('ST','OPCentreForward')],
            'Original D00 actor slots8/10 and roles required')
    require(team['lineup']==list(range(11)),'Original identity-preserving D00 lineup required')
    for slot in (8,10):
        attributes=team['players'][team['lineup'][slot]]['attributes']
        require(len(attributes)==69 and attributes[:15]==[0,0]+[20]*13,
                'Affected D00 field actors must retain omnipotent position ratings')
    for p,i in ((0,8),(0,10),(1,8),(1,10)):
        c=team['phases'][p][i]
        require(type(c['duty']) in (int,str) and c['duty'] in (0,'0') and all(type(v) is int and v==0 for v in c['instructions'].values())
                and c['target_player']==255 and c['target_position']==0,'Original explicit duty/PI controls required')
    configs={}
    for arm in ARMS:
        tr=treatment(arm);config=deepcopy(base_config);phases=config['teams'][side]['phases']
        if tr['ip_strikerless']:
            phases[0][8]['position']='AMCL'
            phases[0][10].update(position='AMCR',role='SecondStriker')
        if tr['oop_strikerless']:
            phases[1][8]['position']='AMCL'
            phases[1][10].update(position='AMCR',role='OPAttackingMidfielder')
        validate_cells(config,side,catalog)
        restored=deepcopy(config)
        for p,i in ((0,8),(0,10),(1,8),(1,10)):
            for key in ('position','role'):restored['teams'][side]['phases'][p][i][key]=team['phases'][p][i][key]
        require(restored==base_config,'Unexpected nonpackage config mutation')
        configs[arm]=config
    require(configs[ARMS[0]]==base_config,'Control config differs from D00')
    return configs


def build_inputs(d00_bytes,side,base_config,catalog,oop_map):
    """Compile only explicit Kind4 role and Kind5 position records in place."""
    configs=build_configs(base_config,side,catalog);source=decode_records(d00_bytes)
    require(len(source)==5557 and not any(r[0]==61 for r in source),'Only original D00 complete records')
    require(encode_startpolicy(source,StartPolicy(side,10000))==d00_bytes,'Controlled D00 start profiles required')
    require([(s,a,b,v) for k,s,a,b,v in source if k==13]==[(0,0,0,1),(1,0,0,1)],
            'Original native game-constraint checks must remain active')
    require(type(oop_map) is list and len(oop_map)==2 and all(type(x) is list and all(type(v) is int for v in x)
            and sorted(x)==list(range(11)) for x in oop_map),
            'Original OOP actor permutation required')
    stamina=[(s,a,v) for k,s,a,b,v in source if k==1 and b==52]
    require(len(stamina)==46 and {(s,a) for s,a,_ in stamina}==set(product((0,1),range(23)))
            and all(v==60 for _,_,v in stamina),'Exactly46 original stamina60 records required')
    positions={p['id']:p['mask'] for p in catalog['positions']};roles={r['id']:int(r['flags']) for r in catalog['roles']}
    attributes={(s,a,b):v for k,s,a,b,v in source if k==1}
    require(len([r for r in source if r[0]==1])==len(attributes)==3174 and
            set(attributes)==set(product((0,1),range(23),range(69))) and
            all(attributes[s,a,b]==base_config['teams'][s]['players'][a]['attributes'][b] for s,a,b in attributes),
            'Complete original69attribute vectors must match both baseline teams')
    require(sum(r[0]==4 for r in source)==sum(r[0]==5 for r in source)==44,'Complete original phase role/position records required')
    for s,team in enumerate(base_config['teams']):
        for phase,cells in enumerate(team['phases']):
            for slot,cell in enumerate(cells):
                native=16*phase+(oop_map[s][slot] if phase else slot);flags=roles[cell['role']]
                require(source.count((4,s,native,flags>>32,flags&0xffffffff))==1 and
                        source.count((5,s,native,0,positions[cell['position']]))==1,
                        'Original actor phase records do not match baseline config/permutation')
    output={}
    for arm,config in configs.items():
        replacements={}
        for phase,slot in ((0,8),(0,10),(1,8),(1,10)):
            original=base_config['teams'][side]['phases'][phase][slot];updated=config['teams'][side]['phases'][phase][slot]
            native=16*phase+(oop_map[side][slot] if phase else slot)
            if original['position']!=updated['position']:
                replacements[(5,side,native,0,positions[original['position']])]=(5,side,native,0,positions[updated['position']])
            if original['role']!=updated['role']:
                a,b=roles[original['role']],roles[updated['role']]
                replacements[(4,side,native,a>>32,a&0xffffffff)]=(4,side,native,b>>32,b&0xffffffff)
        require(all(source.count(row)==1 for row in replacements),'Missing/duplicate original package record')
        changed=tuple(replacements.get(row,row) for row in source)
        differences=[(a,b) for a,b in zip(source,changed,strict=True) if a!=b]
        require(dict(differences)==replacements and len(differences)==len(replacements),'Undeclared package record mutation')
        output[arm]=encode_records(changed)
    require(output[ARMS[0]]==d00_bytes,'I0-O0 control must be byte-identical D00')
    return output


def technical_jobs(seeds):
    require(type(seeds) is list and len(seeds)==len(set(seeds))==4 and
            all(type(s) is int and 0<s<=0xffffffff for s in seeds),'Four new separate technical seeds required')
    full=[dict(key=f'tech-{h}-s{s}-{a}-r{r}',job_id=f'tech-{h}-s{s}-{a}-r{r}',scenario=h,context=h,
        side=s,team_side=s,arm=a,seed=seeds[i],repeat=r,kind='full')
        for i,(h,s) in enumerate(product(CONTEXTS,(0,1))) for a,r in product(ARMS,(0,1))]
    return full+[dict(key='negative-malformed',job_id='negative-malformed',kind='negative',seed=None)]


def audit_job(evidence,dump,job,binary,config,catalog,oop_map,frozen_controls,observer_sha256):
    require(observer_sha256==OBSERVER_HOST,'Observer host drift')
    require(event(evidence,'native_image_fingerprint')['sha256']==job['identity']['engine_sha256'],'Loaded engine drift')
    require(event(evidence,'native_engine_compatibility')['compatible'] is True and
            event(evidence,'windows_load_returned')['success'] is True,'Native loader gate failed')
    require(not any(r.get('event') in ('invalid_role_context','scenario_rejected') for r in evidence),'Native game legality failed')
    require([(s,a,b,v) for k,s,a,b,v in decode_records(binary) if k==13]==[(0,0,0,1),(1,0,0,1)],
            'Original native game constraints not enabled in admitted bytes')
    phases=[r for r in evidence if r.get('event')=='native_phase_configuration']
    require(len(phases)==4 and {(r['side'],r['phase']) for r in phases}==set(product((0,1),(0,1))),
            'All phase receipts required')
    validate_cells(config,job['side'],catalog)
    checked=observer.audit_input(evidence,dump,config,binary,catalog,oop_map)
    audit_trace(evidence,dump,job['seed']);audit_start_state(evidence,binary,job['side'],10000)
    require(initial_controls(evidence)==frozen_controls,'Initial nonsharpness/rawTF33 controls changed')
    require(all(type(p['attributes'][52]) is int and p['attributes'][52]==60 for team in dump['teams'] for p in team['players']),
            'Stamina60 changed')
    tr=treatment(job['arm']);team=config['teams'][job['side']]
    expected=[('AMCL','AttackingMidfielder'),('AMCR','SecondStriker')] if tr['ip_strikerless'] else [('AMC','AttackingMidfielder'),('ST','CentreForward')]
    require([(team['phases'][0][i]['position'],team['phases'][0][i]['role']) for i in (8,10)]==expected,'IP package drift')
    expected=[('AMCL','OPAttackingMidfielder'),('AMCR','OPAttackingMidfielder')] if tr['oop_strikerless'] else [('AMC','OPAttackingMidfielder'),('ST','OPCentreForward')]
    require([(team['phases'][1][i]['position'],team['phases'][1][i]['role']) for i in (8,10)]==expected,'OOP package drift')
    require(team['instructions']['10']==1313689463,'Standard tested-side pressing required')
    values,missing=descriptive(evidence,binary,job['side'])
    return dict(job_id=job['key'],experiment_id=EXPERIMENT,context=job['scenario'],team_side=job['side'],seed=job['seed'],arm=job['arm'],
        status='ok',config_sha256=job['config_sha256'],setup_sha256=job['setup_sha256'],identity=job['identity'],observer_host_sha256=observer_sha256,
        result={k:v for k,v in match_result(evidence,job['seed']).items() if k!='seed'},
        native_audit=dict(input_verified=True,seed_verified=True,package_verified=True,stamina60_verified=True,
            pressing_verified=True,controls_verified=True,start_state_verified=True,native_game_rules_verified=True,
            attribute_values_verified=checked['attribute_values_verified'],profile_fields_verified=checked['profile_fields_verified'],
            phase_cells_verified=checked['phase_cells_verified'],pi_groups_verified=checked['pi_groups_verified'],
            ip_strikerless=tr['ip_strikerless'],oop_strikerless=tr['oop_strikerless'],pressing_bit=0),
        descriptive=values,descriptive_missing_reasons=missing)


def contract_definition(identity=None,setups=None):
    c=dict(schema_version=1,experiment_id=EXPERIMENT,module='TACT',kind='native',stage='discovery',status='draft',
        hypothesis='The xGD effect of the declared strikerless IP4240 package differs between classic OOP4411 and the declared OOP4420 package.',
        control='I0-O0 is original D00: IP4231 and OOP4411, actor8AM/OPAM and actor10CF/OPCF.',
        intervention='Full2x2 IP4231/4240 and OOP4411/4420 packages. IP4240 moves actor8AMC toAMCL with sameAM role, actor10ST toAMCR/SecondStriker. OOP4420 moves corresponding original actors toAMCL/AMCR, bothOPAttackingMidfielder.',
        conditions='All original69attributes,23profile fields per actor, lineup identities/capacities, explicitPI/duties, team instructions, other eight outfield roles, keeper, bank, opponents and management fixed. Original game constraints active. No isolated role/formation/consumer interpretation.',
        seed_namespace=EXPERIMENT+'/main-v1',identity=identity,
        metrics=dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),
        design=dict(unit='seed_block',n_blocks=32,sides=[0,1],control_arm=ARMS[0],matrix=matrix(),matrix_sha256=config_hash(matrix()),
            arms=[dict(id=a,setup_sha256=config_hash({h:{s:v[a] for s,v in by.items()} for h,by in setups.items()}) if setups else None) for a in ARMS],setups=setups,
            scenarios=[dict(id=h,opponent=h,strength='Frozen identical synthetic D00 roster strength',split='discovery') for h in CONTEXTS]),
        science=dict(alpha=.05,power=.9,min_effect=.2,desired_full_ci_width=.5,multiple_testing='holm',family_size=7,
            primary_contrast='INTERACTION',contrast_coefficients={k:list(v) for k,v in COEFFICIENTS.items()},
            secondary_contrasts=[list(v) for v in SECONDARY_PAIRS],context_weights=[.5,.5],side_weights=[.5,.5],bootstrap_resamples=20000,
            analysis='Primary physical difference-of-differences INTERACTION xGD coefficients1,-1,-1,1. Side means within complete seeds; fixed equal contexts; Welch95 and stratified20000 block bootstrap. Exactly Holm7 secondary.',
            exclusions='None. Any failed input/identity/seed/native/rawTF33 gate stops. No retries, replacement seeds or silent zero. Only complete512 main observations allow effect estimation.',
            negative_controls=['32technical full matches, all16 cells twice,16 exact A/A pairs','One malformed binary exit108 plus unique scenario_rejected and no natural finish','Static illegal role/position and undeclared-mutation rejection'],
            readback_fields=['Native original role-position game constraints','All3174attributes/1058profile fields/44phase cells/748PIgroups','Corresponding original actor bindings in both phases using side-specific OOP permutation','Raw/start cache and nonsharpness/rawTF33 controls equal D00 after preparation and first advance','Natural full finish and original actual score/team statistics'],
            stopping_rule='32technical+1negative then independently published release and successfulCI before512main. Own900childsec/5400UTCsec,max4coldworkers; each call absolute30s with40s reserved elapsed envelope. First main requires600s own/global child/UTC remaining. Existing NIGHT0023600whole-phasechildsec/15Nov07Z remains intact; additionally all-call elapsed sum plus inflight reservations must not exceed3600s. Any failed gate terminal.',
            selection_rule='No winner or universal strikerless recommendation. Total IP/OOP package interaction only; formation, role, intrinsic role instructions and movement are not individually isolated. No holdout or automatic increase.',
            power_basis='Unknown package interaction SD.64blocks with equal-context SD0.6/1/1.5 imply full95width0.300/0.500/0.750 and power0.747/0.350/0.183 for0.20. Pilot, not guaranteed90percentpower.'),
        budget=dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
            absolute_study_wall_seconds=5400,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
            raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',
            global_child_seconds=3600,global_deadline_utc='2026-11-15T07:00:00+00:00',
            per_call_absolute_timeout_seconds=30,per_call_reserved_envelope_seconds=40,
            global_native_call_elapsed_limit_seconds=3600),
        native_spec=dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,changed_record_kinds=[4,5],changed_actor_slots=[8,10],
            stamina_index=52,stamina_raw=60,encoded_stamina_records=46,original_game_constraints_required=True,
            kind61_allowed=False,new_setter_allowed=False,ongoing_clamp_allowed=False,ui_scale_calibrated=False,
            consumer_semantics_validated=False,isolated_role_mechanism_identified=False),
        seed_plan=dict(main_blocks=64,technical_seeds=4,total_new_seeds=68,technical_namespace=EXPERIMENT+'/technical-v1',
            technical_seeds_reserved=None,main_seeds_reserved=None),
        gates=dict(native_package_verified=False,technical_independently_released=False),
        preregistration=dict(commit=None,document='experiments/TACT-003-stless-preregistration.md',document_sha256=None,
            analysis='analysis/analyse_stless003.py',analysis_sha256=None),execution=None)
    validate_design(c)
    return c


def validate_design(c,executable=False):
    validate(c,executable=executable);d,b,s=c['design'],c['budget'],c['science']
    require(c['experiment_id']==EXPERIMENT and c['module']=='TACT' and c['stage']=='discovery' and
        c['metrics']==dict(primary='xgd',secondary=list(SECONDARY),plausibility=list(DESCRIPTIVE)),'Experiment/endpoint drift')
    require(d['matrix']==matrix() and d['matrix_sha256']==config_hash(matrix()) and d['n_blocks']==32 and d['sides']==[0,1]
        and d['control_arm']==ARMS[0] and [a['id'] for a in d['arms']]==list(ARMS) and [h['id'] for h in d['scenarios']]==list(CONTEXTS),
        'Package design/sample drift')
    require(s['primary_contrast']=='INTERACTION' and s['contrast_coefficients']=={k:list(v) for k,v in COEFFICIENTS.items()}
        and s['secondary_contrasts']==[list(v) for v in SECONDARY_PAIRS] and s['family_size']==7 and s['multiple_testing']=='holm'
        and s['alpha']==.05 and s['power']==.9 and s['min_effect']==.2 and s['desired_full_ci_width']==.5
        and s['bootstrap_resamples']==20000 and s['context_weights']==s['side_weights']==[.5,.5],'Scientific contrast/family drift')
    require(b==dict(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=900,
        absolute_study_wall_seconds=5400,wall_start_policy='first_native_technical',minimum_main_admission_seconds=600,
        raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3,worker_mode='cold',global_child_seconds=3600,
        global_deadline_utc='2026-11-15T07:00:00+00:00',per_call_absolute_timeout_seconds=30,
        per_call_reserved_envelope_seconds=40,global_native_call_elapsed_limit_seconds=3600),'Resource/admission drift')
    require(c['native_spec']==dict(observer_host_sha256=OBSERVER_HOST,record_count=5557,changed_record_kinds=[4,5],changed_actor_slots=[8,10],
        stamina_index=52,stamina_raw=60,encoded_stamina_records=46,original_game_constraints_required=True,kind61_allowed=False,
        new_setter_allowed=False,ongoing_clamp_allowed=False,ui_scale_calibrated=False,consumer_semantics_validated=False,
        isolated_role_mechanism_identified=False),'Native package drift')
    require(c['seed_namespace']==EXPERIMENT+'/main-v1' and c['seed_plan']['technical_namespace']==EXPERIMENT+'/technical-v1'
        and [c['seed_plan'][k] for k in ('main_blocks','technical_seeds','total_new_seeds')]==[64,4,68],'Seed design drift')
    if executable:
        e=c['execution'];require(type(e) is dict and e.get('runner')=='analysis/run_stless003.py' and e.get('kind')=='cold_direct_cli'
            and type(e.get('workers')) is int and e['workers']==4 and type(e.get('max_processes_per_job')) is int
            and e['max_processes_per_job']==3 and type(e.get('code_sha256')) is dict and e['code_sha256']
            and all(type(v) is str and HASH.fullmatch(v) for v in e['code_sha256'].values())
            and all(type(e.get(k)) is str and HASH.fullmatch(e[k]) for k in ('input_manifest_sha256','seed_plan_sha256')),
            'Frozen execution provenance required')
    return c

"""Synthetic invariants only; this suite never imports a runtime server or host."""
from copy import deepcopy
from collections import Counter
from itertools import product
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import json, os, struct, subprocess, sys, tempfile, unittest
import numpy as np
from scipy.stats import nct, t

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from research.stamina003 import *
from research.core import config_hash, schedule
from research.native import read, rows, write
import analyse_mech003 as analysis
import run_mech003 as runner
import export_mech003 as exporter
from verify_mech003 import same,verify_complete_budget,verify_containment

OOP_MAP=[[0,1,2,3,4,9,5,6,7,8,10],[0,1,2,3,4,5,6,7,9,8,10]]


def base():
    ip=['GK','DR','DCR','DCL','DL','DMR','DML','AMR','AMC','AML','ST']
    oop=['GK','DR','DCR','DCL','DL','MCR','MCL','MR','AMC','ML','ST']
    teams=[]
    for side in (0,1):
        players=[dict(native_id=1000+side*100+i,name='own_synthetic',attributes=[0,0]+[20]*13+[60]*54,native_profile={}) for i in range(23+3*side)]
        phases=[[dict(position=p,role='Role' if phase==0 else 'OPRole',duty='0',
                     instructions={str(g):0 for g in range(17)},target_player=255,target_position=0) for p in positions]
                for phase,positions in enumerate((ip,oop))]
        teams.append(dict(roster_size=23,players=players,lineup=list(range(11)),phases=phases,instructions={'10':PRESS_IDS[0]}))
    return dict(rules='game',fixture='bundled_match_pkm',teams=teams)


def fixture():
    c=deepcopy(read(ROOT/'research/specs/TACT-002-R0.json'))
    c.update(experiment_id=EXPERIMENT,module='MECH',status='registered',test_origin='own_synthetic_only')
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['native_process_plan']=runner.contract_definition()['native_process_plan']
    c['budget'].update(max_matches=512,max_workers=4,timeout_seconds=90,max_technical_attempts=33,total_native_wall_seconds=600,
                       absolute_study_wall_seconds=1200,raw_artifact_limit_bytes=2*1024**3,disk_reserve_bytes=20*1024**3)
    c['science'].update(primary_contrast='STAMINA',multiple_testing='holm',desired_full_ci_width=.5,contrast_coefficients={k:list(v) for k,v in COEFFICIENTS.items()},
                         secondary_contrasts=[list(x) for x in SECONDARY_PAIRS],family_size=7,
                         context_weights=[.5,.5],side_weights=[.5,.5],bootstrap_resamples=20000)
    c['design'].update(n_blocks=32,control_arm='R00',matrix=matrix(),matrix_sha256=config_hash(matrix()),
        arms=[dict(id=a,setup_sha256='d'*64) for a in ARMS],
        setups={h:{str(s):{a:config_hash([h,s,a]) for a in ARMS} for s in (0,1)} for h in CONTEXTS})
    receipt=dict(config=c,config_sha256=config_hash(c),seeds=list(range(10000,10064)));data=[]
    for j in schedule(receipt):
        tr=treatment(j['arm']);h=CONTEXTS.index(j['scenario']);i=receipt['seeds'][h*32:(h+1)*32].index(j['seed'])
        sta,press=tr['levels']['STAMINA'],tr['levels']['PRESS'];side=j['side']
        y=5+(.10+.01*h+.005*(i-15.5)+.04*(2*side-1))*sta+(.20+.01*h+.003*(i-15.5))*press+.03*sta*press+.1*side
        statistics=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5)
        teams=[dict(statistics),dict(statistics)];teams[side]['xg']+=y
        score=[0,0];score[side]=int(sta==1)
        data.append(dict(j,**j['identity'],experiment_id=EXPERIMENT,status='ok',engine_readback=True,tested_side=side,
            finish_tick=22000,score=score,team_statistics=teams,input_contract_verified=True,profile_fields_verified=1058,
            native_attribute_values_verified=3174,native_roles_verified=44,native_pi_cells_verified=44,native_pi_groups_verified=748,
            native_stamina_values=[tr['stamina_raw']]*10,native_pressing_bit=tr['pressing_bit'],factor_levels=tr['levels'],
            design_matrix_sha256=config_hash(matrix())))
    return receipt,data


def fake_native(config):
    pis={g:dict(options=[dict(id=0),dict(id=g+1)]) for g in range(17)}
    names=list(dict.fromkeys(cell['position'] for t in config['teams'] for ph in t['phases'] for cell in ph))
    positions={p:dict(mask=1<<i) for i,p in enumerate(names)}
    roles={'Role':dict(flags=1024),'OPRole':dict(flags=2048)}
    server=SimpleNamespace(PIS=pis,POSITIONS=positions,ROLES=roles,OOP_MAP=OOP_MAP,
        GROUPS={10:dict(options=[dict(id=PRESS_IDS[0],native_bit=0),dict(id=PRESS_IDS[1],native_bit=66)])})
    dump=dict(teams=[])
    for side,t in enumerate(config['teams']):
        tr_high=t['instructions']['10']==PRESS_IDS[1]
        dt=dict(creator_hex=(int(tr_high)*(1<<66)).to_bytes(64,'little').hex(),tactical_slots=[[None]*11 for _ in range(2)],personal_instructions=[[None]*11 for _ in range(2)],
                players=[dict(attributes=list(p['attributes'])) for p in t['players'][:23]])
        for phase,cells in enumerate(t['phases']):
            for i,cell in enumerate(cells):
                slot=OOP_MAP[side][i] if phase else i;raw=bytearray(128)
                struct.pack_into('<I',raw,0,positions[cell['position']]['mask']);struct.pack_into('<Q',raw,64,roles[cell['role']]['flags'])
                dt['tactical_slots'][phase][slot]=raw.hex()
                dt['personal_instructions'][phase][slot]=dict(flags='0',target_player=255,target_position=0)
        dump['teams'].append(dt)
    return SimpleNamespace(server=server),dump


class Stamina003Tests(unittest.TestCase):
    @unittest.skipUnless(os.name=='nt','Windows CommandLineToArgvW and actual Popen audit shape')
    def test_real_windows_popen_audit_none_and_quoted_commandline(self):
        command=[runner.base_python(),'-c','pass','path with spaces','embedded"quote','tail\\','two spaces \\"q"']
        script="""
import json,subprocess,sys
from research.stamina003 import parse_popen_event
events=[]
def audit(name,args):
    if name=='subprocess.Popen':
        path,argv=parse_popen_event(args)
        events.append(dict(executable_was_none=args[0] is None,argv_was_string=isinstance(args[1],str),path=str(path),argv=argv))
sys.addaudithook(audit)
subprocess.run(json.loads(sys.argv[1]),check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(json.dumps(events))
"""
        result=subprocess.run([sys.executable,'-c',script,json.dumps(command)],cwd=ROOT,capture_output=True,text=True,check=True)
        events=json.loads(result.stdout);self.assertEqual(len(events),1)
        self.assertTrue(events[0]['executable_was_none']);self.assertTrue(events[0]['argv_was_string'])
        self.assertEqual(events[0]['argv'],command);self.assertEqual(Path(events[0]['path']).resolve(),Path(command[0]).resolve())
        with tempfile.TemporaryDirectory(prefix='mech audit ') as temp:
            host=Path(temp)/'own synthetic host.exe';dll=Path(temp)/'own image with spaces.dll';ledger=Path(temp)/'starts.jsonl'
            hook=HostLaunchAudit('prepare',host,ledger,lambda:None,dll)
            hook('subprocess.Popen',(None,subprocess.list2cmdline([str(host),'--check-image',str(dll)]),None,{}))
            self.assertEqual(hook.require_complete(),{'loader':1})
            for bad in ([str(host),'--check-image',str(dll),'--extra'],[str(host),'--check-image',str(dll)+'-wrong']):
                with self.assertRaises(ValueError):hook('subprocess.Popen',(None,subprocess.list2cmdline(bad),None,{}))

    def test_capability_preflight_is_real_once_and_strict_before_matches(self):
        from types import ModuleType
        value=dict(protocol=2,max_jobs=1000000,execution_context_reset=True,per_match_resource_release=True)
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);write(root/'fm27_native/adapter_version.json',dict(version='own-test',reference_dll_sha256='own-dll',
                native_worker_protocol=2,execution_context_reset=True,session_scope='remaining_batch_lane',max_worker_jobs=1000000))
            lab=SimpleNamespace(root=root,identity=dict(adapter_host_sha256='own-host',build='own-test',engine_sha256='own-dll'))
            module=ModuleType('desktop_warm_batch');calls=[]
            class FakeRunner:
                _capabilities_cache={}
                def __init__(self,*args,**kwargs):
                    calls.append((args,kwargs));self._capabilities_cache['own-host']=deepcopy(value)
                    self.host_sha256='own-host';self.capabilities=self._capabilities_cache['own-host'];self.counted_sessions=True
            module.DesktopWarmRunner=FakeRunner
            with patch.dict(sys.modules,{'desktop_warm_batch':module}),patch.object(runner,'LOCAL',root):
                expected=runner.preflight_capabilities(lab,'technical')
                self.assertEqual(calls[0][1],dict(workers=4,retries=0,timeout=90))
                for _ in range(4):runner.require_cached_capabilities(lab,expected)
                self.assertEqual(len(calls),1)
                self.assertTrue(read(root/'technical.capabilities-check.json')['checked_before_first_match'])
                with self.assertRaises(ValueError):runner.preflight_capabilities(lab,'technical')
                self.assertEqual(len(calls),1)
                FakeRunner._capabilities_cache['own-host']={}
                with self.assertRaises(ValueError):runner.require_cached_capabilities(lab,expected)
                with self.assertRaises(ValueError):runner.preflight_capabilities(lab,'prepare')
                def fallback(self,*args,**kwargs):
                    self._capabilities_cache['own-host']={};self.host_sha256='own-host'
                    self.capabilities={};self.counted_sessions=False
                FakeRunner._capabilities_cache={}
                with patch.object(FakeRunner,'__init__',fallback):
                    with self.assertRaises(ValueError):runner.preflight_capabilities(lab,'main')
                self.assertFalse((root/'main.capabilities-check.json').exists())
        for bad in ({},None,dict(value,protocol=1),dict(value,protocol=2.),dict(value,max_jobs=True),
                    dict(value,max_jobs=64),dict(value,execution_context_reset=False),dict(value,per_match_resource_release=1)):
            with self.assertRaises(ValueError):runner.check_capability_values(bad)

    def test_capability_gate_failure_precedes_every_match(self):
        receipt=dict(config=dict(identity={}))
        frozen=dict(oop_map=[],catalog_sha256='own-catalog',runtime_source_sha256={})
        lab=SimpleNamespace(server=SimpleNamespace(OOP_MAP=[]),runtime=Path('own-runtime'),identity={},run=unittest.mock.Mock())
        with patch.object(runner,'read',side_effect=[receipt,{},frozen]),patch.object(runner,'published_registration'),patch.object(runner,'verify_code'),patch.object(runner,'check_identity'),patch.object(runner,'digest',return_value='own-catalog'),patch.object(runner,'preflight_capabilities',side_effect=ValueError('Missing actual capabilities')),patch.object(runner,'technical_jobs') as jobs:
            with self.assertRaises(ValueError):runner.execute(lab,'technical',None)
            lab.run.assert_not_called();jobs.assert_not_called()

    def test_negative_binary_requires_rejection_cause_and_exact_exit(self):
        evidence=[dict(event='scenario_rejected')]
        runner.audit_negative_binary(evidence,108)
        for rows_,code in (([],108),(evidence,0),(evidence+evidence,108),
                           (evidence+[dict(event='natural_match_finished')],108)):
            with self.assertRaises(ValueError):runner.audit_negative_binary(rows_,code)

    def test_public_containment_requires_kernel_zero_and_capsule_exit(self):
        proofs={phase:dict(schema='fm27.contained-call.v1',cleanup_confirmed=True,capsule_exit_confirmed=True,
            kernel_active_processes=0,job_policy=dict(active_process_limit=3 if phase=='negative' else 10,
            limit_flags=0x2008,kill_on_close=True,breakaway_allowed=False)) for phase in ('prepare','technical','main','negative')}
        verify_containment(proofs)
        for field,value in (('kernel_active_processes',1),('kernel_active_processes',False),('cleanup_confirmed',False),('capsule_exit_confirmed',False)):
            bad=deepcopy(proofs);bad['main'][field]=value
            with self.assertRaises(ValueError):verify_containment(bad)

    def test_prepare_publication_checks_exact_ci_and_all_source_blobs(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);public=root/'data/mech-003-stamina';public.mkdir(parents=True)
            files=('own.py','experiments/MECH-003-stamina-preregistration.md','data/mech-003-stamina/contract-draft.json','docs/REVIEW.md')
            original={name:b'own synthetic fixture\n' for name in files}
            for name,data in original.items():(root/name).parent.mkdir(parents=True,exist_ok=True);(root/name).write_bytes(data)
            gate=dict(passed=True,published_commit='a'*40,ci_run=42,independent_review_document='docs/REVIEW.md',independent_review_sha256=runner.source_hash(root/'docs/REVIEW.md'))
            write(public/'prepare-gate.json',gate)
            def output(args,**kwargs):
                if args[0]=='gh':return json.dumps(dict(status='completed',conclusion='success',headSha='a'*40))
                if args[1]=='ls-remote':return 'a'*40+'\trefs/heads/main\n'
                if args[1]=='show':return original[args[2].split(':',1)[1]]
                raise AssertionError(args)
            with patch.object(runner,'ROOT',root),patch.object(runner,'PUBLIC',public),patch.object(runner,'CODE',('own.py',)),patch.object(runner.subprocess,'check_output',side_effect=output),patch.object(runner.subprocess,'run'):
                self.assertTrue(runner.check_prepare_publication()['passed'])
                (root/'own.py').write_bytes(b'unpublished change')
                with self.assertRaises(ValueError):runner.check_prepare_publication()

    def test_loader_capability_keys_and_warm_host_limits_are_separate(self):
        self.assertEqual(len(probe_jobs()),5)
        self.assertEqual(PROCESS_CAPS,{'technical':36,'main':514})
        self.assertEqual(runner.phase_keys('prepare'),['loader-check-image-prepare'])
        with patch.object(runner,'read',return_value=dict(technical_seeds=[123,456])):
            self.assertEqual(len(runner.phase_keys('technical')),35)
        with tempfile.TemporaryDirectory() as temp:
            host=Path(temp)/'FM27Simulator.exe';ledger=Path(temp)/'hosts.jsonl';calls=[]
            hook=HostLaunchAudit('technical',host,ledger,lambda:calls.append(True))
            hook('subprocess.Popen',(str(host),[str(host),'--check-image','own-synthetic.dll'],None,{}))
            hook('subprocess.Popen',(str(host),[str(host),'--worker-capabilities'],None,{}))
            for i in range(4):hook('subprocess.Popen',(str(host),[str(host),'--worker-manifest',str(Path(temp)/f'{i}.manifest'),
                '--output',str(Path(temp)/f'{i}.log'),'--tick-step','1','--cancel-event','Local\\FM27MatchCancel_123_'+'0'*32],None,{}))
            with hook.negative_capsule(runner.base_python()):
                hook('subprocess.Popen',(runner.base_python(),[runner.base_python(),'-I',str(ROOT/'research/native_process005.py'),'--capsule'],None,{}))
                hook.negative_permission()
            self.assertEqual(hook.require_complete()['worker_start'],4)
            self.assertEqual(len(rows(ledger)),7);self.assertEqual(len(calls),7)
            for argv in ([str(host),'--worker-manifest','5'],[str(host),'--check-image','x'],[str(host),'--output','x']):
                with self.assertRaises(ValueError):hook('subprocess.Popen',(str(host),argv,None,{}))

    def test_unknown_cleanup_retains_lease_and_durable_marker(self):
        class Budget:
            def load(self):return dict(active=None,halted=False,operations=[])
            def run(self,*args):raise RuntimeError('synthetic child failure')
        for confirmed in (False,True):
            with tempfile.TemporaryDirectory() as temp:
                lease=SimpleNamespace(acquire=lambda:None,assert_owned=lambda:dict(schema=1,experiment=EXPERIMENT,
                    workers=4,owner_pid=123,acquired_utc='synthetic'),release=unittest.mock.Mock())
                with patch.object(runner,'LOCAL',Path(temp)),patch.object(runner,'assert_master'),patch.object(runner,'NativeLease',return_value=lease),patch.object(runner,'phase_cleanup_confirmed',return_value=confirmed):
                    with self.assertRaises(RuntimeError):runner.run_supervised_phase(Budget(),'prepare',['loader-check-image-prepare'],[])
                self.assertEqual(lease.release.call_count,int(confirmed))
                self.assertEqual((Path(temp)/'native-cleanup-pending.json').exists(),not confirmed)
        with tempfile.TemporaryDirectory() as temp:
            lease=SimpleNamespace(acquire=lambda:None,assert_owned=lambda:dict(schema=1,experiment=EXPERIMENT,
                workers=4,owner_pid=123,acquired_utc='synthetic'),release=unittest.mock.Mock())
            budget=SimpleNamespace(load=lambda:dict(active=None,halted=False,operations=[]),run=lambda *args:None)
            with patch.object(runner,'LOCAL',Path(temp)),patch.object(runner,'assert_master'),patch.object(runner,'NativeLease',return_value=lease),patch.object(runner,'phase_cleanup_confirmed',return_value=False):
                with self.assertRaises(RuntimeError):runner.run_supervised_phase(budget,'prepare',['loader-check-image-prepare'],[])
            lease.release.assert_not_called()

    def test_whole_phase_capsule_precedes_runtime_and_uses_base_interpreter(self):
        from types import ModuleType
        capsule=ModuleType('research.native_process005');calls=[]
        capsule.contained_call=lambda *args,**kwargs:(calls.append((args,kwargs)) or (0,.1))
        args=SimpleNamespace(phase='prepare',runtime=Path('own-runtime'),game=Path('own-game'))
        with patch.dict(sys.modules,{'research.native_process005':capsule}),patch.object(runner,'remaining_seconds',return_value=100.),patch.object(runner,'NativeLab') as native:
            runner.run_contained_child(args)
            native.assert_not_called()
        positional,keywords=calls[0]
        self.assertEqual(positional[0][0],runner.base_python());self.assertIn('--child',positional[0])
        self.assertEqual(positional[1]['MECH003_CONTAINED_STUDY'],'1')
        self.assertEqual(keywords,dict(timeout=None,total_timeout=100.,max_processes=10))

    def test_prepare_without_published_gate_never_constructs_native_or_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'.git').mkdir()
            with patch.object(runner,'ROOT',root),patch.object(runner,'assert_master'),patch.object(runner,'check_prepare_publication',side_effect=ValueError('No published release')),patch.object(sys,'argv',['run_mech003.py','prepare']),patch.object(runner,'NativeLab') as native,patch.object(runner,'DeadlineBudget') as budget:
                with self.assertRaises(ValueError):runner.main()
                native.assert_not_called();budget.assert_not_called()

    def test_complete_public_budget_requires_real_keys_fixed_deadline_and_charge(self):
        from datetime import datetime,timedelta,timezone
        start=datetime(2026,11,14,20,tzinfo=timezone.utc)
        operations=[dict(name=name,kind='main' if name=='main' else 'technical',keys=keys,
            start_utc=(start+timedelta(seconds=i*10)).isoformat(),elapsed_seconds=1.,returncode=0,timed_out=False)
            for i,(name,keys) in enumerate((('prepare',['loader-check-image-prepare']),('technical',['loader-check-image-technical','worker-capabilities-technical','t','negative-binary']),('main',['loader-check-image-main','worker-capabilities-main','m'])))]
        budget=dict(experiment=EXPERIMENT,limits=PROCESS_CAPS,limit_seconds=600,wall_limit_seconds=1200,
            active=None,halted=False,charged_seconds=3.,operations=operations,
            reserved={'loader-check-image-prepare':'technical','loader-check-image-technical':'technical','worker-capabilities-technical':'technical','t':'technical','negative-binary':'technical','loader-check-image-main':'main','worker-capabilities-main':'main','m':'main'},wall_start_utc=start.isoformat(),
            wall_deadline_utc=(start+timedelta(seconds=1200)).isoformat(),within_fixed_deadline=True)
        verify_complete_budget(budget,['t','negative-binary'],['m'])
        for field,value in (('charged_seconds',2.),('wall_deadline_utc',(start+timedelta(seconds=1201)).isoformat()),
                            ('reserved',{'replacement':'main'}),('halted',True)):
            bad=deepcopy(budget);bad[field]=value
            with self.assertRaises(ValueError):verify_complete_budget(bad,['t','negative-binary'],['m'])

    def test_published_draft_matches_the_only_contract_factory(self):
        draft=read(ROOT/'data/mech-003-stamina/contract-draft.json')
        self.assertEqual(draft,runner.contract_definition())
        self.assertIsNone(draft['identity']);self.assertIsNone(draft['execution'])
        self.assertIsNone(draft['design']['setups'])
        self.assertTrue(all(a['setup_sha256'] is None for a in draft['design']['arms']))
        analysis.validate_design(draft)

    def test_full_four_cell_matrix_and_physical_contrasts(self):
        self.assertEqual(len({c['id'] for c in matrix()}),4)
        x=np.asarray([[r['levels']['STAMINA'],r['levels']['PRESS']] for r in matrix()])
        self.assertTrue(np.array_equal(x.T@x,4*np.eye(2)))
        self.assertEqual([c['stamina_raw'] for c in matrix()],[40,80,40,80])
        self.assertEqual(len(SECONDARY_PAIRS),7)
        receipt,data=fixture();result,blocks=analysis.analyse(data,receipt)
        self.assertAlmostEqual(result['primary']['mean'],.21)
        self.assertAlmostEqual(result['secondary']['PRESS:xgd']['mean'],.41)
        self.assertAlmostEqual(result['secondary']['STAMINAxPRESS:xgd']['mean'],.12)
        self.assertEqual(len(blocks),512);self.assertEqual(result['independent_seed_blocks'],64)
        self.assertFalse(result['mechanism_decomposition_identified'])

    def test_only_stamina_and_one_pressing_group_change_both_sides(self):
        for side,arm in product((0,1),ARMS):
            original=base();changed,changes=apply_arm(original,side,arm);reset=deepcopy(changed)
            for change in changes:reset['teams'][side]['players'][change['roster_slot']]['attributes'][52]=60
            reset['teams'][side]['instructions']['10']=PRESS_IDS[0]
            self.assertEqual(reset,original);self.assertEqual(len(changes),10)
            self.assertEqual(changed['teams'][1-side],original['teams'][1-side])
            self.assertEqual(changed['teams'][side]['players'][0],original['teams'][side]['players'][0])
            self.assertEqual(changed['teams'][side]['players'][11:],original['teams'][side]['players'][11:])
            self.assertEqual(changed['teams'][side]['phases'],original['teams'][side]['phases'])

    def test_lineup_binding_not_roster_first_ten_and_away_tail_preserved(self):
        b=base();b['teams'][1]['lineup'][1:3]=[12,1]
        changed,changes=apply_arm(b,1,'R10')
        self.assertIn(12,[r['roster_slot'] for r in changes]);self.assertNotIn(2,[r['roster_slot'] for r in changes])
        self.assertEqual(changed['teams'][1]['players'][23:],b['teams'][1]['players'][23:])

    def test_invalid_side_pool_execution_or_nonbaseline_ability_rejected(self):
        for side in (True,-1,2):
            with self.assertRaises(ValueError):apply_arm(base(),side,'R00')
        for key in ('away_tactic_pool','experimental_execution'):
            b=base();b[key]={}
            with self.assertRaises(ValueError):apply_arm(b,0,'R00')
        b=base();b['teams'][0]['players'][1]['attributes'][49]=80
        with self.assertRaises(ValueError):apply_arm(b,0,'R00')

    def test_exact_binary_dose_and_pressing_diff_only(self):
        records=[(1,1,i,52,60) for i in range(1,11)]+[(2,1,10,0,PRESS_IDS[0]),(15,1,1,16,10000)]
        def encode(r):return b'FM27CFG1'+struct.pack('<I',len(r))+b''.join(struct.pack('<5I',*v) for v in r)
        _,changes=apply_arm(base(),1,'R11')
        after=[(k,s,a,b,80 if k==1 else PRESS_IDS[1] if k==2 else v) for k,s,a,b,v in records]
        self.assertEqual(audit_binary(encode(records),encode(after),1,'R11',changes)['changed_records'],11)
        after[-1]=(15,1,1,16,7000)
        with self.assertRaises(ValueError):audit_binary(encode(records),encode(after),1,'R11',changes)

    def test_actual_phase_pi_audit_requires_dose_and_receipts(self):
        config,_=apply_arm(base(),1,'R11');lab,dump=fake_native(config)
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp);write(path/'dump.json',dump)
            evidence=[dict(event='native_profile_bindings_verified',fields=1058),dict(event='native_player_tactic_bindings_verified',players=22,phases=2)]
            (path/'log.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in evidence),encoding='utf8')
            result=audit_contract(lab,{},dict(config=config,side=1,arm='R11'),dict(dump=path/'dump.json'),path/'log.jsonl')
            self.assertEqual(result['native_pi_groups_verified'],748);self.assertEqual(result['native_stamina_values'],[80]*10)
            dump['teams'][1]['personal_instructions'][1][OOP_MAP[1][5]]['target_player']=3;write(path/'dump.json',dump)
            with self.assertRaises(ValueError):audit_contract(lab,{},dict(config=config,side=1,arm='R11'),dict(dump=path/'dump.json'),path/'log.jsonl')

    def test_missing_duplicate_failed_seed_or_readback_drift_prevents_science(self):
        r,data=fixture()
        for corrupt in ('missing','duplicate','failed','seed','dose','contract'):
            bad=deepcopy(data)
            if corrupt=='missing':bad.pop()
            elif corrupt=='duplicate':bad[-1]=deepcopy(bad[0])
            elif corrupt=='failed':bad[0]['status']='failed'
            elif corrupt=='seed':bad[0]['seed']+=1000
            elif corrupt=='dose':bad[0]['native_stamina_values']=[81]*10
            else:bad[0]['input_contract_verified']=False
            with self.subTest(corrupt=corrupt),self.assertRaises(ValueError):analysis.checked(bad,r)

    def test_budget_holm_and_matrix_changes_are_rejected(self):
        receipt,_=fixture()
        for key,value in (('max_matches',1024),('max_technical_attempts',34),('total_native_wall_seconds',601)):
            c=deepcopy(receipt['config']);c['budget'][key]=value
            with self.assertRaises(ValueError):analysis.validate_design(c)
        c=deepcopy(receipt['config']);c['science']['family_size']=8
        with self.assertRaises(ValueError):analysis.validate_design(c)

    def test_technical_schedule_has_sixteen_exact_aa_pairs(self):
        with patch.object(runner,'read',return_value=dict(technical_seeds=[123,456])):
            jobs=runner.technical_jobs()
        self.assertEqual(len(jobs),32);self.assertEqual(len({r['key'] for r in jobs}),32)
        counts=Counter((r['scenario'],r['side'],r['arm']) for r in jobs)
        self.assertEqual(len(counts),16);self.assertEqual(set(counts.values()),{2})

    def test_worktree_and_missing_master_fail_before_any_native_or_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'.git').write_text('worktree',encoding='utf8')
            with patch.object(runner,'ROOT',root),patch.object(sys,'argv',['run_mech003.py','prepare']),patch.object(runner,'NativeLab') as native,patch.object(runner,'DeadlineBudget') as budget:
                with self.assertRaises(ValueError):runner.main()
                native.assert_not_called();budget.assert_not_called()
            (root/'.git').unlink();(root/'.git').mkdir()
            with patch.object(runner,'ROOT',root),patch.object(sys,'argv',['run_mech003.py','prepare']),patch.object(runner,'assert_master',side_effect=ValueError('No master')),patch.object(runner,'NativeLab') as native,patch.object(runner,'DeadlineBudget') as budget:
                with self.assertRaises(ValueError):runner.main()
                native.assert_not_called();budget.assert_not_called()

    def test_reentry_or_retained_phase_never_overwrites_lease_proof(self):
        class Budget:
            def load(self):return dict(active=None,halted=False,operations=[])
            def run(self,*args):raise AssertionError('No child allowed')
        with tempfile.TemporaryDirectory() as temp,patch.object(runner,'LOCAL',Path(temp)):
            p=Path(temp)/'technical.lease.json';p.write_bytes(b'original')
            with self.assertRaises(ValueError):runner.run_supervised_phase(Budget(),'technical',[],[])
            self.assertEqual(p.read_bytes(),b'original')

    def test_prepare_failure_accounts_all550_slots_before_and_after_seeds(self):
        with tempfile.TemporaryDirectory() as temp:
            local=Path(temp)/'private';public=Path(temp)/'public';local.mkdir()
            budget=dict(experiment=EXPERIMENT,limits=PROCESS_CAPS,limit_seconds=600,charged_seconds=1.,reserved={},halted=True,active=None,operations=[],wall_start_utc='2026-11-14T17:00:00+00:00',wall_deadline_utc='2026-11-14T17:20:00+00:00',wall_limit_seconds=1200)
            write(local/'budget.json',budget)
            with patch.object(exporter,'LOCAL',local),patch.object(exporter,'PUBLIC',public):exporter.export()
            account=rows(public/'job-accounting.jsonl');self.assertEqual(len(account),550)
            self.assertTrue(all(r['status']=='not_started' and r['seed'] is None for r in account))
            write(local/'seed-plan.json',dict(main_seeds=list(range(1000,1064)),technical_seeds=[2001,2002]))
            with patch.object(exporter,'LOCAL',local),patch.object(exporter,'PUBLIC',public):exporter.export()
            self.assertEqual(len({r['seed'] for r in rows(public/'job-accounting.jsonl') if r['kind']=='main' and 'probe' not in r}),64)
            self.assertFalse((public/'effects.json').exists())

    def test_float_comparison_tolerates_roundoff_but_not_inference_change(self):
        same({'v':[.1+.2,3]},{'v':[.3,3]})
        with self.assertRaises(ValueError):same({'v':[.301,3]},{'v':[.3,3]})
        self.assertFalse({'native_id','person_key','config','path','name'}&set(exporter.FIELDS))

    def test_future_power_uses_new_blocks_and_correct_sixteen_n_cost(self):
        planning=analysis.future_planning([.8,1.2])
        for name in ('observed','simultaneous95_sd_upper'):
            values=np.asarray(planning[name]['sd'])
            def power(n,effect):
                parts=values**2/(4*n);variance=parts.sum();df=variance**2/(parts**2/(n-1)).sum()
                threshold=t.isf(.025,df);shift=effect/np.sqrt(variance)
                return float(nct.cdf(-threshold,df,shift)+nct.sf(threshold,df,shift))
            for case in planning[name]['power90']:
                n=case['seeds_per_context'];effect=case['effect']
                self.assertEqual(case['matches'],16*n);self.assertEqual(case['independent_blocks'],2*n)
                self.assertGreaterEqual(power(n,effect),.9)
                if n>2:self.assertLess(power(n-1,effect),.9)

    def test_technical_ci_requires_published_independent_review_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);public=root/'data';public.mkdir();review=root/'docs'/'TECH.md';review.parent.mkdir()
            review.write_text('OWN SYNTHETIC REVIEW ONLY\n',encoding='utf8');write(public/'technical-summary.json',dict(passed=True))
            gate=dict(passed=True,published_commit='a'*40,ci_run=1,independent_review_document='docs/TECH.md',independent_review_sha256=runner.source_hash(review))
            write(public/'technical-gate.json',gate)
            def output(args,**kwargs):
                if args[0]=='gh':return json.dumps(dict(status='completed',conclusion='success',headSha='a'*40))
                if args[1]=='ls-remote':return 'a'*40+'\trefs/heads/main\n'
                if args[1]=='show' and args[2].endswith('technical-summary.json'):return (public/'technical-summary.json').read_bytes().replace(b'\r\n',b'\n')
                if args[1]=='show' and args[2].endswith('docs/TECH.md'):return review.read_bytes().replace(b'\r\n',b'\n')
                raise AssertionError(args)
            with patch.object(runner,'ROOT',root),patch.object(runner,'PUBLIC',public),patch.object(runner.subprocess,'check_output',side_effect=output),patch.object(runner.subprocess,'run'):
                self.assertTrue(runner.check_technical_publication()['passed'])
                gate['independent_review_sha256']='0'*64;write(public/'technical-gate.json',gate)
                with self.assertRaises(ValueError):runner.check_technical_publication()


if __name__=='__main__':unittest.main()

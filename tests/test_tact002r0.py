"""Offline physical contrasts, role-record restrictions, PI audits and lease wiring."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import json,struct,sys,tempfile,unittest
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from research.core import config_hash,schedule
from research.native import read,write
from research.coordination import NativeLease,LeaseBusy
from research.study_budget import DeadlineBudget
import analyse_tact002r0 as p
import run_tact002r0 as runner
from export_tact002r0 import FIELDS

def fixture():
    c=deepcopy(read(ROOT/'research/specs/TACT-001-P1B.json'));c.update(experiment_id='TACT-002-R0',status='registered')
    c['preregistration'].update(commit='a'*40,document_sha256='b'*64,analysis_sha256='c'*64)
    c['metrics']['primary']='xgd';c['budget'].update(max_matches=512,max_workers=4,max_technical_attempts=33,total_native_wall_seconds=900,absolute_study_wall_seconds=1800)
    c['science'].update(primary_contrast='ST',secondary_contrasts=[list(v) for v in p.SECONDARY_PAIRS],secondary_family_size=7)
    c['design'].update(n_blocks=32,control_arm='R00',matrix=p.matrix(),matrix_sha256=config_hash(p.matrix()),factors=list(p.FACTORS),arms=[dict(id=a,setup_sha256='a'*64) for a in p.ARMS],setups={h:{str(s):{a:config_hash([h,s,a]) for a in p.ARMS} for s in (0,1)} for h in p.CONTEXTS})
    r=dict(config=c,config_sha256=config_hash(c),seeds=list(range(10000,10064)));data=[]
    for j in schedule(r):
        h=p.CONTEXTS.index(j['scenario']);i=r['seeds'][h*32:(h+1)*32].index(j['seed']);a=p.ARMS.index(j['arm']);levels=p.matrix()[a]['levels'];side=j['side']
        y=5+(.10+.01*h+.005*(i-15.5))*levels['ST']+(.2+.01*h+.003*(i-15.5))*levels['AMC']+.03*levels['ST']*levels['AMC']+.1*side
        stat=dict(xg=1.,shots=20,shots_on_target=10,passes=100,completed_passes=80,possession=.5);teams=[dict(stat),dict(stat)];teams[side]['xg']+=y
        score=[0,0];score[side]=1 if a%2 else 0
        data.append(dict(j,**j['identity'],status='ok',engine_readback=True,tested_side=side,finish_tick=22000,score=score,team_statistics=teams,input_contract_verified=True,profile_fields_verified=1058,native_roles_verified=44,native_pi_cells_verified=44,native_pi_groups_verified=748,factor_levels=levels,native_role_flags=p.wanted_flags(j['arm']),design_matrix_sha256=config_hash(p.matrix())))
    return r,data

def fake_native():
    roles={f[k+'_role']:dict(flags=f[k+'_flags'],phase=0) for f in p.FACTORS for k in ('low','high')};roles.update(Dummy=dict(flags=4,phase=0),OPDummy=dict(flags=8,phase=1))
    names=['GK','DR','DCR','DCL','DL','DMR','DML','AMR','AMC','AML','ST']
    cells=[dict(position=n,role='Dummy',duty='0',instructions={str(g):0 for g in range(17)},target_player=255,target_position=0) for n in names]
    cells[8]['role']='AttackingMidfielder';cells[10]['role']='CentreForward'
    config=dict(rules='game',fixture='bundled_match_pkm',teams=[dict(instructions={},phases=[deepcopy(cells),[dict(c,role='OPDummy') for c in deepcopy(cells)]]) for _ in range(2)])
    positions=[dict(id=n,mask=16 if n in ('DCR','DCL') else 128 if n in ('DMR','DML') else 1) for n in names]
    catalog=dict(roles=[dict(id=k,**v) for k,v in roles.items()],positions=positions,role_eligibility_context={'0:0':{'ST':[['CentreForward','DeepLyingForward'],[]],'AMC':[['AttackingMidfielder','SecondStriker'],[]]}})
    pis={g:dict(options=[dict(id=0),dict(id=g+1)]) for g in range(17)}
    server=SimpleNamespace(ROLES=roles,GROUPS={},PIS=pis,OOP_MAP=[list(range(11)),list(range(11))])
    return config,catalog,server

class RolePilotTests(unittest.TestCase):
    def test_physical_main_and_interaction_scaling(self):
        r,data=fixture();z,blocks=p.analyse(data,r)
        self.assertAlmostEqual(z['primary']['mean'],.21);self.assertAlmostEqual(z['secondary']['AMC:xgd']['mean'],.41);self.assertAlmostEqual(z['secondary']['STxAMC:xgd']['mean'],.12)
        self.assertEqual(len(z['secondary']),7);self.assertEqual(len(blocks),192);self.assertFalse(z['winner_selected'])
        self.assertEqual(z['independent_seed_blocks'],64)
    def test_incomplete_duplicate_drift_or_unverified_cells_refused(self):
        r,data=fixture()
        for bad in (data[:-1],data+[data[0]]):
            with self.assertRaises(ValueError):p.checked(bad,r)
        for k,v in [('seed',1),('native_role_flags',{}),('native_pi_groups_verified',747),('engine_sha256','b'*64),('setup_sha256','b'*64),('factor_levels',{})]:
            bad=deepcopy(data);bad[0][k]=v
            with self.assertRaises(ValueError):p.checked(bad,r)
    def test_only_declared_role_records_can_change(self):
        base=struct.pack('<III',1,1,3)+b''.join(struct.pack('<5I',*x) for x in [(4,0,10,0,2048),(4,0,8,0,512),(3,0,0,0,4)])
        alt=base[:12]+b''.join(struct.pack('<5I',*x) for x in [(4,0,10,0,1024),(4,0,8,512,0),(3,0,0,0,4)])
        self.assertEqual(len(runner.binary_audit(base,alt,0,dict(ST=1,AMC=1),dict(ST=10,AMC=8))),2)
        broken=alt[:-4]+struct.pack('<I',5)
        with self.assertRaises(ValueError):runner.binary_audit(base,broken,0,dict(ST=1,AMC=1),dict(ST=10,AMC=8))
    def test_catalog_eligibility_and_d00_purity(self):
        base,catalog,_=fake_native();changed,slots=runner.apply_roles(base,0,dict(ST=1,AMC=1),catalog)
        self.assertEqual(slots,dict(ST=10,AMC=8));self.assertEqual(changed['teams'][0]['phases'][0][8]['role'],'SecondStriker')
        self.assertEqual(base['teams'][0]['phases'][0][8]['role'],'AttackingMidfielder')
        bad=deepcopy(catalog);bad['role_eligibility_context']['0:0']['ST'][0].remove('DeepLyingForward')
        with self.assertRaises(ValueError):runner.apply_roles(base,0,dict(ST=1,AMC=1),bad)
        bad=deepcopy(base);bad['teams'][0]['phases'][0][10]['instructions']['0']=1
        with self.assertRaises(ValueError):runner.apply_roles(bad,0,dict(ST=1,AMC=1),catalog)
    def test_audit_all44_role_and_pi_cells_not_just_treated_positions(self):
        base,catalog,server=fake_native();config,_=runner.apply_roles(base,0,dict(ST=1,AMC=1),catalog);teams=[]
        for team in config['teams']:
            phases=[]
            for ph in team['phases']:
                values=[]
                for cell in ph:
                    raw=bytearray(72);struct.pack_into('<Q',raw,64,server.ROLES[cell['role']]['flags']);values.append(raw.hex())
                phases.append(values)
            teams.append(dict(creator_hex=bytes(16).hex(),tactical_slots=phases,personal_instructions=[[dict(flags='0',target_player=255,target_position=0) for _ in range(11)] for _ in range(2)]))
        with tempfile.TemporaryDirectory() as temp:
            dump=Path(temp)/'d.json';log=Path(temp)/'l.jsonl';write(dump,dict(teams=teams));log.write_text('{"event":"native_profile_bindings_verified","fields":1058}\n')
            got=runner.audit_contract(SimpleNamespace(server=server),None,dict(config=config,side=0,arm='R11'),dict(dump=dump),log)
            self.assertEqual(got['native_pi_groups_verified'],748)
            teams[1]['personal_instructions'][1][4]['flags']='2';write(dump,dict(teams=teams))
            with self.assertRaisesRegex(ValueError,'PI group'):runner.audit_contract(SimpleNamespace(server=server),None,dict(config=config,side=0,arm='R11'),dict(dump=dump),log)
    def test_technical_schedule_is32_full_jobs_with16_repeat_pairs(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);write(folder/'seed-plan.json',dict(technical_seeds=[11,12,13]))
            with patch.object(runner,'LOCAL',folder):jobs=runner.technical_jobs()
            self.assertEqual(len(jobs),32);self.assertEqual(len({(j['scenario'],j['side'],j['arm']) for j in jobs}),16)
            self.assertEqual({j['arm'] for j in jobs},set(p.ARMS))
    def test_lease_encloses_persistent_budget_and_limits_not_reset(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);budget=DeadlineBudget(folder/'budget.json',experiment='TACT-002-R0',seconds=900,caps={'technical':33,'main':512},wall_seconds=1800)
            with NativeLease(folder/'global','TACT-002-R0',workers=4):
                with self.assertRaises(LeaseBusy):NativeLease(folder/'global','VALID-003').acquire()
                budget.reserve('technical','technical',['t']);budget.finish(.1,0)
            with self.assertRaises(ValueError):budget.reserve('retry','technical',['t'])
            self.assertEqual(budget.load()['reserved'],{'t':'technical'})
    def test_repeated_or_retained_phase_preserves_budget_and_original_lease_without_child(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);local=folder/'study';local.mkdir()
            budget=DeadlineBudget(local/'budget.json',experiment='TACT-002-R0',seconds=900,caps={'technical':33,'main':512},wall_seconds=1800)
            with patch.object(runner,'ROOT',folder),patch.object(runner,'LOCAL',local):
                # A real ordinary Python child, never a native application.
                runner.run_supervised_phase(budget,'prepare',[],[sys.executable,'-c',"print('offline only')"])
                old_budget=budget.path.read_bytes();old_proof=(local/'prepare.lease.json').read_bytes()
                with patch.object(runner.subprocess,'Popen') as child:
                    with self.assertRaisesRegex(ValueError,'already attempted'):runner.run_supervised_phase(budget,'prepare',[],[sys.executable,'-c','raise SystemExit(99)'])
                    child.assert_not_called()
                self.assertEqual(budget.path.read_bytes(),old_budget);self.assertEqual((local/'prepare.lease.json').read_bytes(),old_proof)
                # A crash between exclusive proof creation and budget.run likewise
                # leaves a retained proof that cannot be replaced on the next call.
                retained=local/'technical.lease.json';retained.write_bytes(b'original retained evidence')
                with patch.object(runner.subprocess,'Popen') as child:
                    with self.assertRaisesRegex(ValueError,'Retained phase lease'):runner.run_supervised_phase(budget,'technical',['t'],[sys.executable,'-c','raise SystemExit(99)'])
                    child.assert_not_called()
                self.assertEqual(budget.path.read_bytes(),old_budget);self.assertEqual(retained.read_bytes(),b'original retained evidence')
                self.assertFalse((folder/'local/global-native/native-execution.lease.json').exists())
    def test_exact_published_gate_ci_commit_required_before_main(self):
        with tempfile.TemporaryDirectory() as temp:
            folder=Path(temp);write(folder/'technical-gate.json',dict(passed=True,published_commit='a'*40,ci_run=123))
            with patch.object(runner,'PUBLIC',folder):
                for ci in (dict(status='in_progress',conclusion='',headSha='a'*40),dict(status='completed',conclusion='failure',headSha='a'*40),dict(status='completed',conclusion='success',headSha='b'*40)):
                    with patch.object(runner.subprocess,'check_output',return_value=json.dumps(ci)):
                        with self.assertRaises(ValueError):runner.check_technical_publication()
                with patch.object(runner.subprocess,'check_output',return_value=json.dumps(dict(status='completed',conclusion='success',headSha='a'*40))):
                    self.assertTrue(runner.check_technical_publication()['passed'])
    def test_public_export_whitelist_has_no_native_player_ids(self):
        self.assertIn('native_role_flags',FIELDS);self.assertNotIn('config',FIELDS);self.assertNotIn('players',FIELDS);self.assertNotIn('native_id',FIELDS)

if __name__=='__main__':unittest.main()

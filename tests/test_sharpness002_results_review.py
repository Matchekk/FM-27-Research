"""Independent reviewer fixtures; all native-looking evidence is manufactured."""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from pathlib import Path
import json
import struct
import tempfile
import unittest
from unittest.mock import patch

from analysis import review_sharpness002_results as review
from tests.test_sharpness002_design import binary_fixture
from tests.test_passive_observer import fixture as observer_fixture


def manufactured_match():
    base,_,_=binary_fixture(0);binary,lineups=review.expected_input(base,0,'S70-P1')
    source=review.records(binary);dump,evidence=observer_fixture()
    cell=dict(position='P',role='R',duty=0,target_player=0,target_position=0,
              instructions={str(i):0 for i in range(17)})
    config=dict(teams=[dict(mentality=0,instructions={'10':2000905329 if side==0 else 1313689463},
        phases=[[deepcopy(cell) for _ in range(11)] for _ in range(2)],
        players=[dict(native_id=1+100*side+i) for i in range(23)]) for side in (0,1)])
    catalog=dict(roles=[dict(id='R',flags=0)],positions=[dict(id='P',mask=1)],
        team_instructions=[dict(id=10,options=[dict(id=1313689463,native_bit=0),dict(id=2000905329,native_bit=66)])],
        player_instructions=[dict(id=i,options=[dict(id=0)]) for i in range(17)])
    offsets={0:(0x6c,4),1:(0x79,1),9:(0xbb8,4),10:(0xbbc,4),19:(0x70,1),20:(0xca8,1),21:(0xca2,1),22:(0xca3,1)}
    offsets.update({i:(0x72+i-2,1) for i in range(2,9)})
    offsets.update({i:(off,2) for i,off in enumerate((0xc98,0xc8c,0xc96,0xc78,0xc8a,0xc90,0xc7a,0xc84),11)})
    for side,team in enumerate(dump['teams']):
        creator=bytearray(128)
        if side==0:creator[66//8]|=1<<(66%8)
        team.update(creator_hex=creator.hex(),tactical_slots=[[None]*11 for _ in range(2)],
            personal_instructions=[[dict(target_player=0,target_position=0,flags=0) for _ in range(11)] for _ in range(2)])
        for phase in (0,1):
            for i in range(11):
                raw=bytearray(72);struct.pack_into('<I',raw,0,1);team['tactical_slots'][phase][i]=raw.hex()
        for i,p in enumerate(team['players']):
            attrs=[None]*69;prefix=bytearray(128);tail=bytearray.fromhex(p['input_tail_hex'])
            for kind,s,slot,field,value in source:
                if s!=side or slot!=i:continue
                if kind==1:attrs[field]=value
                elif kind==15:
                    offset,size=offsets[field];target=prefix if offset<128 else tail;at=offset if offset<128 else offset-0x4c5
                    target[at:at+size]=struct.pack('<f',value/100) if field==0 else value.to_bytes(size,'little')
            p.update(attributes=attrs,prefix_hex=prefix.hex(),input_tail_hex=tail.hex())
    targets={lineups[0,i] for i in range(1,11)};controls={}
    for row in evidence:
        if row.get('event')!='native_passive_state':continue
        for p in row['players']:
            raw=7000 if p['side']==0 and p['roster_index'] in targets else 10000
            p.update(sharpness_raw=raw,sharpness_secondary_raw=raw,condition_accumulator_raw=1000000)
            if (p['side'],p['roster_index']) in {(s,lineups[s,i]) for s in (0,1) for i in range(11)}:
                cache=bytearray(16);cache[9]=100;cache[10]=raw//100;p['statistics_cache_region_hex']=cache.hex()
        if row['stage']!='finished':
            fields=('id','side','roster_index','condition_raw','fatigue_raw','condition_accumulator_raw','sharpness_penalty_raw','effectiveness_region_hex')
            controls[row['stage']]=review.canonical([{k:p[k] for k in fields} for p in sorted(row['players'],key=lambda p:p['id'])])
    evidence[:0]=[dict(event='native_image_fingerprint',sha256='a'*64),dict(event='native_engine_compatibility',compatible=True),
                  dict(event='windows_load_returned',success=True)]
    evidence[3:3]=[dict(event='native_phase_configuration',side=s,phase=p) for s,p in ((0,0),(0,1),(1,0),(1,1))]
    job=dict(key='own-synthetic',side=0,seed=123,arm='S70-P1',identity=dict(engine_sha256='a'*64))
    return evidence,dump,job,binary,config,catalog,[list(range(11)),list(range(11))],controls


class SharpnessResultReviewer(unittest.TestCase):
    def test_seed_namespaces_exclusions_and_allocation_are_independent(self):
        excluded={0,12,14};main=review.deterministic_candidates(review.EXPERIMENT+'/main-v1',64,excluded)
        tech=review.deterministic_candidates(review.EXPERIMENT+'/technical-v1',4,excluded|set(main))
        plan=dict(experiment_id=review.EXPERIMENT,namespace=review.EXPERIMENT+'/main-v1',technical_namespace=review.EXPERIMENT+'/technical-v1',
            main_seeds=main,technical_seeds=tech,seeds=main+tech,excluded_seed_count=3,excluded_seed_set_sha256=review.canonical(sorted(excluded)))
        self.assertEqual(review.audit_seed_plan(plan,excluded)['distinct_seeds'],68)
        for edit in ('historical','ordering','namespace','hash'):
            bad=deepcopy(plan)
            if edit=='historical':bad['seeds'][0]=bad['main_seeds'][0]=12
            elif edit=='ordering':bad['seeds'].reverse()
            elif edit=='namespace':bad['technical_namespace']+='/changed'
            else:bad['excluded_seed_set_sha256']='0'*64
            with self.subTest(edit=edit),self.assertRaises(ValueError):review.audit_seed_plan(bad,excluded)

    def test_json_duplicate_nonfinite_and_protected_files_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'own.json'
            for text in ('{"a":1,"a":2}','{"a":NaN}'):
                path.write_text(text,encoding='utf8')
                with self.assertRaises(ValueError):review.read(path)
            with self.assertRaises(ValueError):review.file_sha(Path(tmp)/'never-open.fm')

    def test_synthetic_native_input_and_all_raw_stages_reconstruct(self):
        args=manufactured_match();result=review.audit_raw_match(*args)
        self.assertEqual(result['native_audit']['attribute_values_verified'],3174)
        self.assertEqual(result['native_audit']['profile_fields_verified'],1058)
        self.assertEqual(result['native_audit']['phase_cells_verified'],44)
        self.assertEqual(result['native_audit']['pi_groups_verified'],748)
        self.assertEqual(result['descriptive']['first_sharpness_cache8a_mean'],70)
        self.assertEqual(result['actor_stage_observations'],138)
        self.assertNotIn('players',result);self.assertNotIn('id',result)

    def test_native_raw_missing_changed_identity_field_phase_or_seed_blocks(self):
        for edit in ('attribute','profile','role','pi','raw','cache','tf','seed','duplicate'):
            args=list(deepcopy(manufactured_match()));evidence,dump,job,_,_,_,_,_=args
            snap=next(r for r in evidence if r.get('stage')=='first_advance')
            if edit=='attribute':dump['teams'][0]['players'][0]['attributes'][52]=59
            elif edit=='profile':dump['teams'][0]['players'][0]['prefix_hex']='ff'*128
            elif edit=='role':dump['teams'][0]['tactical_slots'][1][0]='00'*72
            elif edit=='pi':dump['teams'][0]['personal_instructions'][0][0]['target_player']=7
            elif edit=='raw':snap['players'][0]['sharpness_secondary_raw']=8000
            elif edit=='cache':snap['players'][0]['statistics_cache_region_hex']=None
            elif edit=='tf':snap['players'][0]['effectiveness_region_hex']='00'*33
            elif edit=='seed':snap['seed']=124
            else:snap['players'][-1]=deepcopy(snap['players'][0])
            with self.subTest(edit=edit),self.assertRaises(ValueError):review.audit_raw_match(*args)

    def test_exact_kernel_three_zero_membership_and_errors(self):
        policy=dict(active_process_limit=3,limit_flags=0x2008,kill_on_close=True,breakaway_allowed=False)
        process=dict(schema='fm27.contained-call.v1',job_policy=policy,membership_verified_before_go=True)
        proof=dict(schema='fm27.contained-call.v1',job_policy=policy,cleanup_confirmed=True,capsule_exit_confirmed=True,
            kernel_active_processes=0,host_start_permission_sent=True,elapsed_seconds=1.,error_type=None)
        review.audit_cleanup(proof,process)
        for change in (dict(kernel_active_processes=1),dict(cleanup_confirmed=False),dict(error_type='TimeoutError'),
                       dict(job_policy=dict(policy,active_process_limit=10))):
            with self.subTest(change=change),self.assertRaises(ValueError):review.audit_cleanup(dict(proof,**change),process)

    def test_claims_retries_stop_and_missing_completions(self):
        when='2026-11-14T20:00:00+00:00';events=[dict(event='claimed',job_id=str(i),active_claims=i+1,peak_claims=i+1,utc=when) for i in range(4)]
        events += [dict(event='completed',job_id=str(i),active_claims=3-i,peak_claims=4,utc=when) for i in range(4)]
        self.assertEqual(review.audit_concurrency(events,set('0123'))['peak_inflight_claims'],4)
        for changed in (events[:-1],events+[events[0]],
                        [dict(event='stop',job_id='stop',active_claims=0,peak_claims=0,utc=when)]+events):
            with self.assertRaises(ValueError):review.audit_concurrency(changed,set('0123'))

    def test_parent_budget_charge_caps_utc_and_exact_attempts(self):
        jobs=[dict(key=f'own-{i}') for i in range(33)]
        op=dict(name='technical',kind='technical',keys=[j['key'] for j in jobs],returncode=0,timed_out=False,
            elapsed_seconds=10.,start_utc='2026-11-14T20:00:01+00:00',child_deadline_utc='2026-11-14T20:14:56+00:00')
        state=dict(experiment=review.EXPERIMENT,limits={'technical':33,'main':512},limit_seconds=900,wall_limit_seconds=3600,
            halted=False,active=None,operations=[op],charged_seconds=10.,reserved={j['key']:'technical' for j in jobs},
            wall_start_utc='2026-11-14T20:00:00+00:00',wall_deadline_utc='2026-11-14T21:00:00+00:00')
        proof=dict(experiment_id=review.EXPERIMENT,phase='technical',budget_sha256='a'*64,completed_utc='2026-11-14T20:00:12+00:00')
        self.assertEqual(review.audit_budget(state,proof,'a'*64,'technical',{'technical':jobs})['charged_seconds'],10.)
        for edit in ('refund','retry','halted','wall','parent'):
            bad=deepcopy(state);receipt=deepcopy(proof)
            if edit=='refund':bad['charged_seconds']=0.
            elif edit=='retry':bad['operations'].append(deepcopy(op))
            elif edit=='halted':bad['halted']=True
            elif edit=='wall':bad['wall_deadline_utc']='2026-11-14T22:00:00+00:00'
            else:receipt['budget_sha256']='b'*64
            with self.subTest(edit=edit),self.assertRaises(ValueError):review.audit_budget(bad,receipt,'a'*64,'technical',{'technical':jobs})

    def test_publication_requires_exact_successful_ci_and_source_bytes(self):
        commit='a'*40
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'own.py').write_text('OWN\n',encoding='utf8')
            run=dict(head_sha=commit,status='completed',conclusion='success',updated_at='2026-11-14T20:00:00Z')
            def command(args,**kwargs):return b'OWN\n' if args[0]=='git' else json.dumps(run)
            with patch.object(review.subprocess,'check_output',side_effect=command):
                self.assertTrue(review.verify_publication(root,commit,1,['own.py'])['ci_verified'])
                run['head_sha']='b'*40
                with self.assertRaises(ValueError):review.verify_publication(root,commit,1,['own.py'])

    def test_incomplete_unbegun_phase_has_no_pass_or_effect_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):review.audit_phase(Path(tmp),'main')

    def public_projection_fixture(self):
        path=Path(__file__).resolve().parents[1]/'data/mech-002-sharpness-p0/technical-evidence-review.json'
        evidence=review.read(path)
        seeds=[next(r['seed'] for r in evidence['jobs'] if r['context']==h and r['team_side']==s)
               for h in review.CONTEXTS for s in (0,1)]
        plan=review.expected_jobs(dict(technical_seeds=seeds));rows=[]
        for row in evidence['jobs']:
            if row['kind']=='negative':continue
            rows.append(dict(job_id=row['job_id'],result=row['result'],native_audit=row['native_audit'],
                input_dump_sha256=row['input_dump_sha256'],setup_sha256=row['input_setup_sha256'],
                containment_receipt_sha256=row['containment_sha256'],raw_log_sha256=row['raw_log_sha256'],stdout_sha256=row['stdout_sha256']))
        return evidence,rows,plan,evidence['summary']['inputs_sha256']

    def test_actual_public_33_job_projection_has_explicit_negative_and_no_private_fields(self):
        evidence,rows,plan,sha=self.public_projection_fixture()
        result=review.audit_public_projection(evidence,rows,plan,sha)
        self.assertEqual(result['jobs_verified'],33);self.assertEqual(result['aa_pairs'],16)
        self.assertFalse(result['private_raw_evidence_verified_by_this_public_check'])
        self.assertLess(review.utc(evidence['publication']['ci_completed_utc']),
                        min(review.utc(j['claimed_utc']) for j in evidence['jobs']))

    def test_public_projection_rejects_missing_failed_private_or_nonrepeatable_claims(self):
        for edit in ('missing','negative_exit','private','cleanup','aa'):
            evidence,rows,plan,sha=deepcopy(self.public_projection_fixture())
            if edit=='missing':evidence['jobs'].pop()
            elif edit=='negative_exit':evidence['jobs'][-1]['returncode']=0
            elif edit=='private':evidence['jobs'][0]['private_path']='PRIVATE-DO-NOT-EXPORT'
            elif edit=='cleanup':evidence['jobs'][0]['kernel_active_processes']=1
            else:evidence['jobs'][0]['raw_state_aa_signature_sha256']='0'*64
            with self.subTest(edit=edit),self.assertRaises(ValueError):review.audit_public_projection(evidence,rows,plan,sha)


if __name__=='__main__':unittest.main()

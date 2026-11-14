"""Prepare R1/R2 without save access; run one profile only after published release."""
from argparse import ArgumentParser
from datetime import datetime,timedelta,timezone
from hashlib import sha256
import json
import importlib.metadata
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import sysconfig
import time
import warnings
import zipfile

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.career_reader004r1 import (EXPECTED_SNAPSHOT,HardReaderJob,MEMORY_BYTES,
    PROBES,PROFILES,PROFILE_V10,RELEASE_COMMIT,VERSION,WALL_SECONDS,WHEEL_SHA,
    compare_reports,coverage,current_checks,field_contract,file_hash,layout_claim,ledger,load_profile,require,tree_hashes)
from research.career_readonly004 import digest,write
from research.coordination import NativeLease

PUBLIC=ROOT/'data/night-001-career-r1'
CODE=('research/career_reader004r1.py','analysis/audit_career004r1.py',
      'research/career_readonly004.py','research/coordination.py')
DOCS={'R1':'experiments/VALID-004-career-readonly-R1.md','R2':'experiments/VALID-004-career-readonly-R2.md'}


def read(path):return json.loads(Path(path).read_text(encoding='utf8'))


def append(path,row):
    with Path(path).open('a',encoding='utf8') as stream:
        stream.write(json.dumps(row,ensure_ascii=False,allow_nan=False,default=str)+'\n')
        stream.flush();os.fsync(stream.fileno())


def paths(central):
    base=Path(central)/'local/night-001-career'
    return dict(snapshot=base/'readonly/snapshot.fm',runtime=Path(central)/'local/runtime-v1114.6/source',
                isolated=base/'reader0124/site',wheel=base/'reader0124/fmsave-0.12.4-py3-none-any.whl',
                preparation=base/'reader0124/preparation.json')


def prepare(central):
    """Metadata/source inspection only. Do not open/hash the saved-game snapshot here."""
    p=paths(central);base=Path(central)/'local/night-001-career'
    require(not any((base/f'readonly-{profile.lower()}/attempt.json').exists() for profile in PROFILES),
            'A retained real attempt forbids preparation changes')
    artifact=read(p['preparation'])
    require(artifact['version']=='0.12.4' and artifact['wheel_sha256']==WHEEL_SHA and
            artifact['release_commit']==RELEASE_COMMIT and artifact['install_no_deps'],
            'Isolated package preparation metadata differs')
    require(file_hash(p['wheel'])==WHEEL_SHA,'Isolated wheel drift')
    with zipfile.ZipFile(p['wheel']) as wheel:
        expected={n[len('fmsave/'):]:sha256(wheel.read(n)).hexdigest() for n in wheel.namelist()
                  if n.startswith('fmsave/') and n.endswith('.py')}
    require(tree_hashes(p['isolated']/'fmsave')==expected,'Installed source differs from official wheel')
    source={n:file_hash(ROOT/n,True) for n in CODE}
    base_site=Path(sysconfig.get_paths()['purelib'])
    require(importlib.metadata.version('fmsave')=='0.9.0','Protected base distribution version drift')
    launcher=dict(kind='direct_base_executable_with_frozen_venv_site',
                  executable_sha256=file_hash(sys._base_executable),
                  base_reader_source_sha256=tree_hashes(base_site/'fmsave'))
    vendor=tree_hashes(p['runtime']/'vendor/fmsave')
    require(bool(vendor) and bool(launcher['base_reader_source_sha256']) and bool(expected),
            'Empty reader source inventory')
    runtime={n:file_hash(p['runtime']/n) for n in ('desktop_save_compat.py','desktop_save_draft.py')}
    for profile in PROFILES:
        config=dict(schema=1,experiment_id=f'VALID-004-CAREER-{profile}',profile=profile,version=VERSION,
          status='prepared_not_released',hypothesis='Versioned read-only parser coverage and cross-reader consistency on one unchanged save; no causal effect.',
          primary='complete ordered12probe status ledger; structural checks and warnings retained',
          probes=list(PROBES),snapshot_sha256=EXPECTED_SNAPSHOT,
          snapshot_source='previously frozen approved R0 private snapshot only',
          budget=dict(wall_seconds=180,hard_process_private_bytes=MEMORY_BYTES,
                      hard_job_private_bytes=MEMORY_BYTES,max_reader_processes=1,retries=0,
                      max_new_private_artifact_bytes=512*1024**2,
                      program_deadline_utc='2026-11-14T23:00:00+00:00'),
          policy=dict(strict=True,stop_on_first_exception=True,stop_on_blocking_integrity=True,
                      warnings_require_review=True,coverage_is_not_native_validation=True,
                      no_save_write=True,no_calendar_advance=True,no_native=True,no_seeds=True),
          document=DOCS[profile],document_sha256=file_hash(ROOT/DOCS[profile],True),
          code_sha256=source,field_contract=field_contract(),launcher=launcher,
          reader=dict(package='fmsave',profile=PROFILE_V10 if profile=='R1' else 'official_pypi_0.12.4',
                      package_version='0.9.0' if profile=='R1' else '0.12.4',
                      reported_version_basis='distribution_metadata_not_vendored_source_release' if profile=='R1' else 'official_wheel_metadata_and_source_hashes',
                      source_sha256=vendor if profile=='R1' else expected,
                      runtime_sha256=runtime if profile=='R1' else {},
                      wheel_sha256=WHEEL_SHA if profile=='R2' else None,
                      publishing_commit=RELEASE_COMMIT if profile=='R2' else None,
                      decompression_policy={'frame_cap_bytes':768*1024**2,'total_cap_bytes':1536*1024**2,
                          'summary_draft_fallback':'observe_calls_and_acceptance'} if profile=='R1' else
                          {'max_part_expansion':64,'max_save_expansion':32,'small_part_allowance_bytes':64*1024**2,
                           'fixed_package_caps':None,'outer_hard_job_cap_bytes':MEMORY_BYTES}),
          native_released=False,career_advance_released=False,replay_released=False)
        write(PUBLIC/f'{profile}-contract.json',config)
    write(PUBLIC/'isolated-package-preparation.json',artifact)
    print('Prepared two contracts/source manifests; no save opened.')


def verify_frozen(c,central):
    require(c['profile'] in PROFILES and c['version']==VERSION,'Profile identity drift')
    require(c['snapshot_sha256']==EXPECTED_SNAPSHOT and c['budget']['wall_seconds']==180 and
            c['budget']['hard_process_private_bytes']==MEMORY_BYTES and
            c['budget']['hard_job_private_bytes']==MEMORY_BYTES,'Input/budget drift')
    require(all(file_hash(ROOT/n,True)==v for n,v in c['code_sha256'].items()),'Frozen own code changed')
    require(file_hash(ROOT/c['document'],True)==c['document_sha256'],'Frozen contract document changed')
    require(file_hash(sys._base_executable)==c['launcher']['executable_sha256'],'Python interpreter changed')
    base_site=Path(sysconfig.get_paths()['purelib'])
    # A direct-base child receives the venv site through the explicit environment.
    if os.environ.get('FM_READER_BASE_SITE'):base_site=Path(os.environ['FM_READER_BASE_SITE'])
    require(tree_hashes(base_site/'fmsave')==c['launcher']['base_reader_source_sha256'],
            'Protected base reader source changed')
    p=paths(central)
    package=p['runtime']/'vendor/fmsave' if c['profile']=='R1' else p['isolated']/'fmsave'
    require(tree_hashes(package)==c['reader']['source_sha256'],'Frozen reader source changed')
    require(all(file_hash(p['runtime']/n)==v for n,v in c['reader']['runtime_sha256'].items()),'Runtime profile changed')
    if c['profile']=='R2':require(file_hash(p['wheel'])==WHEEL_SHA,'Official package wheel changed')


def verify_release(c,release_path):
    release=read(release_path)
    require(release.get('passed') is True and release.get('profile')==c['profile'],'Missing profile release')
    commit=release.get('published_commit','');require(re.fullmatch(r'[0-9a-f]{40}',commit),'Full published commit required')
    require(type(release.get('ci_run')) is int and release['ci_run']>0,'Exact CI run required')
    ci=read_ci(release['ci_run'])
    require(ci==dict(status='completed',conclusion='success',headSha=commit),'Exact published CI not successful')
    relative=f'data/night-001-career-r1/{c["profile"]}-contract.json'
    original=json.loads(subprocess.check_output(['git','show',commit+':'+relative],cwd=ROOT))
    require(original==c,'Published reader contract differs')
    for name,h in c['code_sha256'].items():
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==h,'Published own code differs')
    document=subprocess.check_output(['git','show',commit+':'+c['document']],cwd=ROOT)
    require(sha256(document.replace(b'\r\n',b'\n')).hexdigest()==c['document_sha256'],'Published preregistration differs')
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]
    subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=ROOT,check=True)
    report=release['review_document'];review_path=(ROOT/report).resolve()
    require(ROOT in review_path.parents and not Path(report).is_absolute(),'Unsafe review path')
    require(file_hash(review_path,True)==release['review_sha256'],'Review proof changed')
    blob=subprocess.check_output(['git','show',commit+':'+report],cwd=ROOT)
    require(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==release['review_sha256'],'Review not in exact published release')
    return release


def read_ci(run):
    return json.loads(subprocess.check_output(['gh','run','view',str(run),'--json','status,conclusion,headSha'],cwd=ROOT,text=True,timeout=30))


def child(profile,central,private):
    token=sys.stdin.readline().strip()
    require(token and sha256(token.encode()).hexdigest()==os.environ.get('FM_READER_TOKEN_SHA256'),
            'Parent job assignment handshake missing')
    require(read(private/'attempt.json')['supervisor_pid']==os.getppid(),'Reader parent identity differs')
    config=read(PUBLIC/f'{profile}-contract.json');verify_frozen(config,central)
    p=paths(central);events=private/'events.jsonl';events.touch(exist_ok=False)
    try:
        module,trace=load_profile(profile,p['runtime'],p['isolated'])
        require(module.__version__==config['reader']['package_version'],'Loaded package version differs')
        write(private/'setup.json',dict(status='profile_loaded',package_version=module.__version__,
                                        entry_sha256=file_hash(module.__file__)))
    except Exception as error:
        write(private/'setup.json',dict(status='profile_load_failed',error_type=type(error).__name__))
        raise
    context={};save=None;info=None
    try:
        for name in PROBES:
            append(events,dict(probe=name,status='started'))
            caught=[]
            try:
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    if name=='open':
                        save=module.open(p['snapshot'],strict=True);info=save.info;value=None
                    else:value=getattr(save,name)()
                checks=[] if name=='open' else current_checks(save,name)
                if any(g['applied'] and not g['passed'] and not g['advisory'] for ck in checks for g in ck['gates']):
                    append(events,dict(probe=name,status='failed',error_type='BlockingReaderChecks',checks=checks,
                        warning_types=[type(w.message).__name__ for w in caught],warning_count=len(caught)))
                    break
                result=coverage(name,value,context,info)
                append(events,dict(probe=name,status='observed_with_warnings' if caught else 'observed',
                    coverage=result,checks=checks,borrowed_layout=None if name=='open' else layout_claim(save,name),
                    warning_types=[type(w.message).__name__ for w in caught],warning_count=len(caught),
                    private_warnings=[str(w.message) for w in caught]))
            except Exception as error:
                append(events,dict(probe=name,status='failed',error_type=type(error).__name__,
                    checks=current_checks(save,name,error),warning_types=[type(w.message).__name__ for w in caught],
                    warning_count=len(caught),private_warnings=[str(w.message) for w in caught],private_error=str(error)))
                break
            finally:
                write(private/'trace.json',trace)
                write(private/'private-bindings.json',{k:sorted(v) if isinstance(v,set) else v for k,v in context.items()})
    finally:
        if save is not None:save.close()


def collected_events(private):
    events=[];invalid=0
    path=Path(private)/'events.jsonl'
    if path.exists():
        for line in path.read_text(encoding='utf8').splitlines():
            try:events.append(json.loads(line))
            except json.JSONDecodeError:invalid+=1
    return events,invalid


def export_status(profile,central):
    """Reconcile retained ledgers only; never touch/open the save or start a process."""
    private=Path(central)/f'local/night-001-career/readonly-{profile.lower()}'
    state=read(private/'attempt.json');events,invalid=collected_events(private)
    resources=state.get('resources',dict(status='abandoned_or_unreconciled',wall_limit_seconds=180,
        hard_memory_job=None,reader_processes_started=None,retries=0))
    resources={**resources,'invalid_event_lines_retained':invalid}
    final_hash=state.get('snapshot_sha256_after')
    report=ledger(events,profile,resources,final_hash==EXPECTED_SNAPSHOT if final_hash else None)
    report['snapshot_sha256']=final_hash;report['release']=state['release']
    report['trace']=read(private/'trace.json') if (private/'trace.json').exists() else None
    report['profile_setup']=read(private/'setup.json') if (private/'setup.json').exists() else None
    write(private/'result.json',report);write(PUBLIC/profile/'coverage.json',report)
    return report


def run(profile,central,release_path):
    require((ROOT/'.git').is_dir(),'Real-save passes only from central checkout after publication')
    require(Path(central).resolve()==ROOT.resolve(),'Real-save passes require the exact central checkout')
    c=read(PUBLIC/f'{profile}-contract.json');verify_frozen(c,central)
    release=verify_release(c,release_path)
    now=datetime.now(timezone.utc);deadline=datetime.fromisoformat(c['budget']['program_deadline_utc'])
    require(now+timedelta(seconds=185)<deadline,'Insufficient remaining midnight budget for a complete pass')
    p=paths(central);private=Path(central)/f'local/night-001-career/readonly-{profile.lower()}'
    require(not (private/'attempt.json').exists(),'Retained attempt: no retry or overwrite')
    with NativeLease(Path(central)/'local/global-readers',f'VALID-004-CAREER-{profile}',workers=1) as lease:
        private.mkdir(parents=True,exist_ok=True)
        began=time.monotonic();marker=private/'attempt.json'
        start=dict(profile=profile,status='started',start_utc=now.isoformat(),
                   max_seconds=180,hard_private_bytes=MEMORY_BYTES,release=release,supervisor_pid=os.getpid(),
                   lease={k:v for k,v in lease.assert_owned().items() if k in ('owner_pid','acquired_utc','experiment')})
        with marker.open('x',encoding='utf8') as stream:
            json.dump(start,stream,indent=2);stream.flush();os.fsync(stream.fileno())
        token=secrets.token_hex(24);status='completed';process=None;job_proof=None;returncode=None;failure=None
        try:
            require(digest(p['snapshot'])==EXPECTED_SNAPSHOT,'Private frozen snapshot changed')
            with HardReaderJob() as job,(private/'stdout.txt').open('xb') as output:
                site=sysconfig.get_paths()['purelib']
                environment={**os.environ,'FM_READER_TOKEN_SHA256':sha256(token.encode()).hexdigest(),
                    'FM_READER_BASE_SITE':site,'PYTHONPATH':site,'PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
                environment.pop('PYTHONHOME',None)
                process=subprocess.Popen([sys._base_executable,str(Path(__file__).resolve()),'child','--profile',profile,
                    '--central',str(central),'--private',str(private)],cwd=ROOT,stdin=subprocess.PIPE,
                    stdout=output,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW,
                    env=environment)
                job_proof=job.assign(process)
                process.stdin.write((token+'\n').encode());process.stdin.close()
                allowance=180-(time.monotonic()-began)-2
                require(allowance>0,'Reader deadline exhausted before decode')
                until=time.monotonic()+allowance
                while process.poll() is None:
                    remaining=until-time.monotonic()
                    if remaining<=0:
                        status='timeout';process.kill();break
                    if sum(x.stat().st_size for x in private.rglob('*') if x.is_file())>512*1024**2:
                        status='artifact_cap';process.kill();break
                    try:process.wait(timeout=min(.25,remaining))
                    except subprocess.TimeoutExpired:pass
                returncode=process.wait(timeout=2)
                if returncode and status=='completed':status='child_failed'
                job_proof=job.info()
        except Exception as error:
            failure=error;status='supervisor_failed'
            if process is not None:
                if process.poll() is None:process.kill()
                returncode=process.wait(timeout=2)
        try:final_hash=digest(p['snapshot'])
        except OSError:final_hash=None;status='snapshot_unreadable_after_pass'
        elapsed=time.monotonic()-began
        resources=dict(status=status,child_returncode=returncode,elapsed_seconds=elapsed,wall_limit_seconds=180,
            hard_memory_job=job_proof,supervisor_error_type=type(failure).__name__ if failure else None,retries=0,
            reader_processes_started=int(process is not None),within_wall_limit=elapsed<=180)
        write(marker,{**start,'status':'finished' if failure is None else 'failed','resources':resources,
                      'snapshot_sha256_after':final_hash})
        report=export_status(profile,central)
        print(json.dumps(dict(profile=profile,resources=resources,statuses={x['probe']:x['status'] for x in report['probes']}),indent=2))
        if failure is not None:raise failure


def compare(central):
    a=read(PUBLIC/'R1/coverage.json');b=read(PUBLIC/'R2/coverage.json')
    base=Path(central)/'local/night-001-career'
    left=read(base/'readonly-r1/private-bindings.json') if (base/'readonly-r1/private-bindings.json').exists() else {}
    right=read(base/'readonly-r2/private-bindings.json') if (base/'readonly-r2/private-bindings.json').exists() else {}
    report=compare_reports(a,b,left,right)
    write(PUBLIC/'cross-reader.json',report)
    print(json.dumps({k:report[k] for k in ('kind','source_snapshots','independent_treatment_replicates_verified')}))


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare','run','child','export-status','compare'))
    parser.add_argument('--profile',choices=PROFILES)
    parser.add_argument('--central',type=Path,default=ROOT)
    parser.add_argument('--release',type=Path)
    parser.add_argument('--private',type=Path)
    args=parser.parse_args()
    if args.phase=='prepare':prepare(args.central)
    elif args.phase=='child':child(args.profile,args.central,args.private)
    elif args.phase=='export-status':
        require(args.profile is not None,'Profile required');print(json.dumps(export_status(args.profile,args.central)))
    elif args.phase=='compare':compare(args.central)
    else:
        require(args.profile is not None and args.release is not None,'Profile and published release are required')
        run(args.profile,args.central,args.release)

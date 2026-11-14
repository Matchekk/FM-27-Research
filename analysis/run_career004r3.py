"""One gated read-only R3 diagnostic. Preparation/tests never open a saved game."""
from argparse import ArgumentParser
from contextlib import contextmanager
import ctypes
from ctypes import wintypes
from datetime import datetime,timedelta,timezone
from hashlib import file_digest,sha256
import importlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import sysconfig
import threading
import time
import traceback
import uuid
import warnings
import zipfile

def isolate_project_imports(root):
    """Read source instead of pre-existing pyc; never delete or create a cache."""
    private=(Path(root)/'local/night-001-career').resolve()
    prefix=(private/'import-cache'/uuid.uuid4().hex).resolve()
    if not prefix.is_relative_to(private) or prefix.exists() or prefix.is_symlink():
        raise RuntimeError('Fresh private import-cache prefix is not safely absent')
    sys.pycache_prefix=str(prefix);sys.dont_write_bytecode=True
    return prefix


ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__' and any(n=='research' or n.startswith('research.') for n in sys.modules):
    raise RuntimeError('Direct source entry requires no preloaded research modules')
IMPORT_CACHE_PREFIX=isolate_project_imports(ROOT)
sys.path.insert(0,str(ROOT))
from research.career_diag004r3 import STAGES,observe_final_call,require,source_hash
from research.coordination import NativeLease
from research.native_process005 import _WindowsJob,_Extended,_cleanup

EXPERIMENT='VALID-004-CAREER-R3-DIAG'
VERSION='career-marker-runner-v2'
SNAPSHOT_SHA='1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d'
SNAPSHOT_BYTES=147130636
WHEEL_SHA='2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa'
MEMORY=3*1024**3
ARTIFACT_CAP=1024**2
FLAGS=0x2308
BUDGET=dict(wall_seconds=180,cleanup_reserve_seconds=5,hard_process_private_bytes=MEMORY,
    hard_job_private_bytes=MEMORY,actual_reader_processes=1,max_new_private_artifact_bytes=ARTIFACT_CAP,
    stdout_bytes=64*1024,stage_ledger_bytes=64*1024,parent_metadata_bytes=128*1024,
    child_metadata_bytes=256*1024,retries=0,deadline_utc='2026-11-14T23:00:00Z')
POLICY=dict(strict=True,one_open=True,one_tactics_call=True,exception_identity_preserved=True,
            expected_warning_categories={'UnknownBuildWarning':1},
            expected_marker_widths=[3,3,3],
            import_cache_policy='fresh_absent_private_UUID_prefix_before_project_imports; no_bytecode_writes',
            pre_go_deadline_recheck=True,utc_cleanup_reserve_in_loop=True,
            no_v10=True,no_recovery=True,no_extra_probes=True,no_retry=True)
RELEASE_METADATA=dict(directory='local/night-001-career/releases',suffix='.json',max_bytes=64*1024,
                      resolve_before_read=True)
PUBLIC=ROOT/'data/night-001-career-r3'
CONTRACT='data/night-001-career-r3/final-contract.json'
REVIEW='docs/night-001/CAREER-R3-RUNNER-REVIEW.md'
DOCUMENTS=('experiments/VALID-004-career-readonly-R3-DIAG.md',
           'experiments/VALID-004-career-readonly-R3-RUN.md')
CODE=('analysis/run_career004r3.py','research/__init__.py','research/career_diag004r3.py',
      'research/coordination.py','research/native_process005.py','tests/test_career004r3_runner.py')
INPUTS=('data/night-001-career-r1/R2-contract.json','data/night-001-career-r3/R3-draft-contract.json',
        'requirements-lock.txt')
SAFE_CODE=re.compile(r'[A-Za-z_][A-Za-z0-9_]{0,80}\Z')
HEX=re.compile(r'[0-9a-f]{64}\Z')

# -I -S disables site hooks before the job/GO boundary. No fmsave/research import
# and no saved-game access exists in this short bootstrap.
BOOTSTRAP="""import sys,json,os,hmac,hashlib,ctypes,uuid
from ctypes import wintypes
from pathlib import Path
line=sys.stdin.buffer.readline(16385)
if not line or len(line)>16384:raise SystemExit(231)
p=json.loads(line)
if set(p)!={'token','script','central','site','runner_sha256'}:raise SystemExit(231)
if not hmac.compare_digest(hashlib.sha256(p['token'].encode()).hexdigest(),os.environ.get('FM27_R3_TOKEN_SHA256','')):raise SystemExit(231)
k=ctypes.WinDLL('kernel32',use_last_error=True);k.GetCurrentProcess.restype=wintypes.HANDLE
k.IsProcessInJob.argtypes=[wintypes.HANDLE,wintypes.HANDLE,ctypes.POINTER(wintypes.BOOL)]
k.IsProcessInJob.restype=wintypes.BOOL;member=wintypes.BOOL()
if not k.IsProcessInJob(k.GetCurrentProcess(),None,ctypes.byref(member)) or not member.value:raise SystemExit(231)
private=(Path(p['central'])/'local/night-001-career').resolve()
prefix=(private/'import-cache'/uuid.uuid4().hex).resolve()
if not prefix.is_relative_to(private) or prefix.exists() or prefix.is_symlink():raise SystemExit(231)
sys.pycache_prefix=str(prefix);sys.dont_write_bytecode=True
import runpy
with open(p['script'],'rb') as s:code=s.read()
if hashlib.sha256(code.replace(b'\\r\\n',b'\\n')).hexdigest()!=p['runner_sha256']:raise SystemExit(231)
sys.path.insert(0,p['site']);os.environ['FM27_R3_BASE_SITE']=p['site'];os.environ['FM27_R3_ADMITTED']='1'
sys.argv=[p['script'],'child','--central',p['central']]
runpy.run_path(p['script'],run_name='__main__')
"""


def read(path):return json.loads(Path(path).read_text(encoding='utf8'))


def normalized_hash(path):
    return sha256(Path(path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()


def byte_hash(path):
    with Path(path).open('rb') as stream:return file_digest(stream,'sha256').hexdigest()


def source_tree(root):
    root=Path(root)
    return {p.relative_to(root).as_posix():byte_hash(p) for p in sorted(root.rglob('*.py'))}


def dependency_files(site):
    site=Path(site)
    return {x.relative_to(site).as_posix():byte_hash(x) for x in sorted((site/'backports/zstd').rglob('*'))
            if x.is_file() and x.suffix in ('.py','.pyd')}


def base_metadata(site):
    return {name:byte_hash(Path(site)/name) for name in (
        'fmsave-0.9.0.dist-info/METADATA','backports_zstd-1.8.0.dist-info/METADATA')}


def snapshot_receipt(path):
    """Called only by the admitted hard-job child, never by prepare/run/export."""
    return dict(sha256=byte_hash(path),bytes=Path(path).stat().st_size)


def paths(central):
    base=Path(central)/'local/night-001-career'
    return dict(snapshot=base/'readonly/snapshot.fm',private=base/'readonly-r3',
        isolated=base/'reader0124/site',wheel=base/'reader0124/fmsave-0.12.4-py3-none-any.whl')


def _encoded(value):return (json.dumps(value,allow_nan=False,indent=2)+'\n').encode()


class PrivateStore:
    """Partitioned hard writer bounds; no raw game objects or save copies."""
    PARENT={'attempt.json','launch.json','completion.json'}
    CHILD={'child-setup.json','snapshot-before.json','snapshot-after.json','marker.json','close.json','warnings.json'}
    def __init__(self,directory,role):
        self.directory=Path(directory);self.role=role
        require(role in ('parent','child'),'Unknown private writer')
    def write(self,name,value):
        allowed=self.PARENT if self.role=='parent' else self.CHILD
        require(name in allowed,'Unregistered private output')
        payload=_encoded(value)
        cap=BUDGET['parent_metadata_bytes'] if self.role=='parent' else BUDGET['child_metadata_bytes']
        used=sum((self.directory/n).stat().st_size for n in allowed if (self.directory/n).exists())
        require(used+len(payload)<=cap,'Private metadata budget exceeded')
        with (self.directory/name).open('xb') as stream:
            stream.write(payload);stream.flush();os.fsync(stream.fileno())
    def event(self,stage,status,**details):
        require(stage in STAGES and status in ('started','observed','failed','blocked'),'Unknown stage event')
        payload=(json.dumps(dict(stage=stage,status=status,**details),allow_nan=False)+'\n').encode()
        path=self.directory/'events.jsonl'
        require((path.stat().st_size if path.exists() else 0)+len(payload)<=BUDGET['stage_ledger_bytes'],
                'Stage ledger budget exceeded')
        with path.open('ab') as stream:stream.write(payload);stream.flush();os.fsync(stream.fileno())


class ReaderJob:
    """Analysis-only memory extension; frozen native helper policy stays unchanged."""
    def __init__(self,memory=MEMORY):
        require(type(memory) is int and 32*1024**2<=memory<=MEMORY,'Invalid reader memory cap')
        self.job=_WindowsJob(1);self.memory=memory;self.final_policy=None
        try:
            data=_Extended();data.basic.flags=FLAGS;data.basic.active_limit=1
            data.process_memory=memory;data.job_memory=memory
            if not self.job.k.SetInformationJobObject(self.job.handle,9,ctypes.byref(data),ctypes.sizeof(data)):
                raise ctypes.WinError(ctypes.get_last_error())
            self.policy()
        except BaseException:self.job.close();raise
    def policy(self):
        data=_Extended()
        if not self.job.k.QueryInformationJobObject(self.job.handle,9,ctypes.byref(data),ctypes.sizeof(data),None):
            raise ctypes.WinError(ctypes.get_last_error())
        require(data.basic.flags==FLAGS and data.basic.active_limit==1 and
                data.process_memory==self.memory and data.job_memory==self.memory,'Reader kernel policy differs')
        return dict(limit_flags=int(data.basic.flags),active_process_limit=1,
            process_memory_limit=int(data.process_memory),job_memory_limit=int(data.job_memory),
            peak_process_private_bytes=int(data.peak_process_memory),peak_job_private_bytes=int(data.peak_job_memory),
            kill_on_close=True,breakaway_allowed=False)
    def assign(self,process):
        k=self.job.k
        if not k.AssignProcessToJobObject(self.job.handle,int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        member=wintypes.BOOL()
        if not k.IsProcessInJob(int(process._handle),self.job.handle,ctypes.byref(member)):
            raise ctypes.WinError(ctypes.get_last_error())
        require(bool(member.value),'Reader not in specific owning job')
        return self.policy()
    def accounting(self):return self.job.accounting()
    def terminate(self):return self.job.terminate()
    def close(self):
        try:self.final_policy=self.policy()
        finally:self.job.close()


def confirmed_reader_cleanup(proof,memory=MEMORY):
    if not isinstance(proof,dict):return False
    p=proof.get('job_policy',{})
    return (isinstance(p,dict) and proof.get('cleanup_confirmed') is True and proof.get('final_policy_verified') is True and
        proof.get('capsule_exit_confirmed') is True and type(proof.get('kernel_active_processes')) is int and
        proof['kernel_active_processes']==0 and type(p.get('limit_flags')) is int and p['limit_flags']==FLAGS and
        type(p.get('active_process_limit')) is int and p['active_process_limit']==1 and
        type(p.get('process_memory_limit')) is int and p['process_memory_limit']==memory and
        type(p.get('job_memory_limit')) is int and p['job_memory_limit']==memory and
        p.get('kill_on_close') is True and p.get('breakaway_allowed') is False)


def prepare(central):
    """Sources, wheel and metadata only; NEVER hash/stat/open the snapshot here."""
    p=paths(central);require(not (p['private']/'attempt.json').exists(),'Retained R3 attempt forbids changes')
    r2=read(ROOT/INPUTS[0]);site=Path(sysconfig.get_paths()['purelib'])
    require(importlib.metadata.version('fmsave')=='0.9.0','Protected base version changed')
    require(importlib.metadata.version('backports.zstd')=='1.8.0','Pinned decompressor version changed')
    require(byte_hash(p['wheel'])==WHEEL_SHA,'Official wheel changed')
    official=source_tree(p['isolated']/'fmsave')
    require(len(official)==86 and official==r2['reader']['source_sha256'],'Official86-source inventory differs')
    require(source_tree(site/'fmsave')==r2['launcher']['base_reader_source_sha256'],'Protected base reader changed')
    require(byte_hash(sys._base_executable)==r2['launcher']['executable_sha256'],'Protected base interpreter changed')
    dependencies=dependency_files(site)
    require(dependencies and any(n.endswith('.pyd') for n in dependencies),'Pinned decompressor code missing')
    metadata='fmsave-0.12.4.dist-info/METADATA';metadata_hash=byte_hash(p['isolated']/metadata)
    with zipfile.ZipFile(p['wheel']) as wheel:
        require(sha256(wheel.read(metadata)).hexdigest()==metadata_hash,'Isolated metadata differs from wheel')
    c=dict(schema='valid004.r3.final-run-contract.v1',experiment_id=EXPERIMENT,version=VERSION,
        state='prepared_unreleased_no_real_attempt',snapshot_sha256=SNAPSHOT_SHA,snapshot_bytes=SNAPSHOT_BYTES,
        stages=list(STAGES),budget=BUDGET,policy_release_metadata=RELEASE_METADATA,
        reader=r2['reader'],isolated_metadata_sha256=metadata_hash,
        code_sha256_lf={n:normalized_hash(ROOT/n) for n in CODE},
        documents_sha256_lf={n:normalized_hash(ROOT/n) for n in DOCUMENTS},
        inputs_sha256_lf={n:normalized_hash(ROOT/n) for n in INPUTS},
        base=dict(executable_sha256=byte_hash(sys._base_executable),package_version='0.9.0',
                  decompressor_version='1.8.0',distribution_metadata_sha256=base_metadata(site),
                  fmsave_source_sha256=source_tree(site/'fmsave'),decompressor_files_sha256=dependencies),
        required_review_document=REVIEW,director_gate='published proceed',
        source_normalization='Own code/documents/input text CRLF_to_LF; foreign sources/wheel/executable raw SHA256',
        policy=POLICY,
        native_semantics_verified=False,tactics_released=False,replay_released=False,
        training_effect_released=False,career_advance_released=False)
    PUBLIC.mkdir(parents=True,exist_ok=True)
    (ROOT/CONTRACT).write_bytes(_encoded(c))
    verify_frozen(c,central)
    print('Prepared final R3 contract; no snapshot stat/hash/open and no decoder process.')


def verify_frozen(c,central):
    require(sys.dont_write_bytecode is True and sys.pycache_prefix and
            Path(sys.pycache_prefix).resolve().is_relative_to((ROOT/'local/night-001-career').resolve()) and
            not Path(sys.pycache_prefix).exists() and not Path(sys.pycache_prefix).is_symlink(),
            'Fresh absent source-import prefix required')
    require(c['experiment_id']==EXPERIMENT and c['version']==VERSION and c['budget']==BUDGET and c['policy']==POLICY and
            c['policy_release_metadata']==RELEASE_METADATA and
            c['snapshot_sha256']==SNAPSHOT_SHA and c['snapshot_bytes']==SNAPSHOT_BYTES and
            c['stages']==list(STAGES) and c['required_review_document']==REVIEW,'Final contract identity/budget drift')
    require(set(c['code_sha256_lf'])==set(CODE) and set(c['documents_sha256_lf'])==set(DOCUMENTS) and
            set(c['inputs_sha256_lf'])==set(INPUTS),'Incomplete source/document freeze')
    for key in ('code_sha256_lf','documents_sha256_lf','inputs_sha256_lf'):
        require(all(normalized_hash(ROOT/n)==h for n,h in c[key].items()),'Frozen own source/text changed')
    r2=read(ROOT/INPUTS[0]);p=paths(central)
    require(c['reader']==r2['reader'] and c['reader']['package_version']=='0.12.4' and
            c['reader']['wheel_sha256']==WHEEL_SHA,'Wrong official reader contract')
    require(len(c['reader']['source_sha256'])==86 and
            source_tree(p['isolated']/'fmsave')==c['reader']['source_sha256'],'Official reader source drift')
    require(byte_hash(p['wheel'])==WHEEL_SHA,'Official wheel drift')
    require(byte_hash(p['isolated']/'fmsave-0.12.4.dist-info/METADATA')==c['isolated_metadata_sha256'],'Isolated metadata drift')
    require(byte_hash(sys._base_executable)==c['base']['executable_sha256'],'Base interpreter drift')
    site=Path(os.environ.get('FM27_R3_BASE_SITE',sysconfig.get_paths()['purelib']))
    require(source_tree(site/'fmsave')==c['base']['fmsave_source_sha256'],'Protected base package drift')
    require(dependency_files(site)==c['base']['decompressor_files_sha256'],'Decompressor drift')
    require(base_metadata(site)==c['base']['distribution_metadata_sha256'],'Pinned base metadata drift')


def published_gate(c,release_path):
    release_file=Path(release_path).resolve()
    release_base=(ROOT/RELEASE_METADATA['directory']).resolve()
    require(release_file.is_relative_to(release_base) and release_file!=release_base and
            release_file.suffix.lower()==RELEASE_METADATA['suffix'],'Release must be JSON in the fixed private release directory')
    require(release_file.is_file() and 0<release_file.stat().st_size<=RELEASE_METADATA['max_bytes'],'Release metadata size invalid')
    release=read(release_file);commit=release.get('published_commit','')
    require(release.get('experiment_id')==EXPERIMENT and release.get('passed') is True and
            release.get('director_proceed')=='published proceed','Director release missing')
    require(re.fullmatch(r'[0-9a-f]{40}',commit) and type(release.get('ci_run')) is int and release['ci_run']>0,
            'Full commit and exact CI required')
    contract_hash=normalized_hash(ROOT/CONTRACT)
    require(release.get('review_document')==REVIEW and release.get('reviewed_contract_sha256')==contract_hash,
            'Separate final-runner review binding missing')
    require(HEX.fullmatch(release.get('review_sha256','')) and
            normalized_hash(ROOT/REVIEW)==release['review_sha256'],'Final review changed')
    require(contract_hash in (ROOT/REVIEW).read_text(encoding='utf8'),'Review must name exact final contract SHA256')
    remote_url=subprocess.check_output(['git','remote','get-url','origin'],cwd=ROOT,text=True).strip()
    require(remote_url=='https://github.com/Matchekk/FM-27-Research.git','Unexpected publication remote')
    ci=json.loads(subprocess.check_output(['gh','run','view',str(release['ci_run']),'--json','status,conclusion,headSha'],cwd=ROOT,text=True,timeout=30))
    require(ci==dict(status='completed',conclusion='success',headSha=commit),'Exact published CI not successful')
    original=json.loads(subprocess.check_output(['git','show',commit+':'+CONTRACT],cwd=ROOT))
    require(original==c,'Published final contract differs')
    files={**c['code_sha256_lf'],**c['documents_sha256_lf'],**c['inputs_sha256_lf'],REVIEW:release['review_sha256']}
    for name,h in files.items():
        blob=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)
        require(sha256(blob.replace(b'\r\n',b'\n')).hexdigest()==h,'Published source/review differs')
    remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=ROOT,text=True).split()[0]
    subprocess.run(['git','merge-base','--is-ancestor',commit,remote],cwd=ROOT,check=True)
    return {k:release[k] for k in ('experiment_id','passed','director_proceed','published_commit','ci_run',
                                 'review_document','review_sha256','reviewed_contract_sha256')}


@contextmanager
def capture_warnings(state):
    def caught(message,category,filename,lineno,file=None,line=None):
        state['count']+=1
        if len(state['items'])>=32:
            state['truncated']=True;raise RuntimeError('Warning capture budget exceeded')
        raw=str(message).encode('utf8');text=raw[:2048].decode('utf8',errors='replace')
        truncated=len(raw)>2048 or len(json.dumps(text).encode())>4096
        if len(json.dumps(text).encode())>4096:text=text[:256]
        state['items'].append(dict(category=category.__name__,private_message=text,truncated=truncated))
        if truncated:state['truncated']=True;raise RuntimeError('Oversize warning retained with explicit truncation')
    with warnings.catch_warnings():
        warnings.simplefilter('always');warnings.showwarning=caught
        yield


def _load_official(p):
    require(not any(n=='fmsave' or n.startswith('fmsave.') for n in sys.modules),'Fresh decoder required')
    sys.path.insert(0,str(p['isolated']))
    module=importlib.import_module('fmsave')
    require(module.__version__=='0.12.4' and Path(module.__file__).resolve().is_relative_to(p['isolated'].resolve()),
            'Wrong isolated reader import')
    target=importlib.import_module('fmsave.readers.tactics')._read_selection_part
    require(not any(n in sys.modules for n in ('desktop_save_compat','desktop_save_draft','desktop_engine','desktop_host','fm27_tactics_server')),
            'Forbidden runtime/native import')
    return module,target


def child(central):
    require(os.environ.get('FM27_R3_ADMITTED')=='1','Job/GO admission missing')
    require(sys.dont_write_bytecode is True,'Decoder bytecode writes must be disabled')
    require((ROOT/'.git').is_dir() and Path(central).resolve()==ROOT.resolve(),'Central checkout required')
    p=paths(central);store=PrivateStore(p['private'],'child');attempt=read(p['private']/'attempt.json')
    lease=read(Path(central)/'local/global-readers/native-execution.lease.json')
    launch=read(p['private']/'launch.json')
    require(attempt['supervisor_pid']==os.getppid()==lease['owner_pid'] and lease['experiment']==EXPERIMENT,
            'Live supervisor/lease identity differs')
    require(attempt['contract_sha256_lf']==normalized_hash(ROOT/CONTRACT) and
            attempt['release']['director_proceed']=='published proceed' and attempt['experiment_id']==EXPERIMENT and
            attempt['release']['experiment_id']==EXPERIMENT and attempt['release']['passed'] is True and
            launch['decoder_pid']==os.getpid() and launch['membership_verified_before_go'] is True,
            'Attempt admission differs')
    c=read(ROOT/CONTRACT);save=None;code=0;open_calls=0;tactics_calls=0;receipt={};input_validated=False
    warn=dict(count=0,items=[],truncated=False);close=dict(save_opened=False,attempted=False,status='not_needed_no_save')
    try:
        try:
            verify_frozen(c,central)
            with capture_warnings(warn):module,target=_load_official(p)
        except BaseException as error:
            store.write('child-setup.json',dict(status='failed',error_type=type(error).__name__))
            raise
        store.write('child-setup.json',dict(status='verified_official_reader',package_version=module.__version__))
        store.event(STAGES[1],'started')
        try:
            before=snapshot_receipt(p['snapshot'])
            store.write('snapshot-before.json',before)
            require(before==dict(sha256=SNAPSHOT_SHA,bytes=SNAPSHOT_BYTES),'Frozen snapshot identity differs')
        except BaseException as error:store.event(STAGES[1],'failed',error_type=type(error).__name__);raise
        input_validated=True;store.event(STAGES[1],'observed')
        store.event(STAGES[2],'started')
        try:
            with capture_warnings(warn):
                open_calls+=1;save=module.open(p['snapshot'],strict=True)
                require(save.info.game=='FM27' and save.info.build=='27.0.1+2503222' and
                        save.info.section_schemas.get('tactics_man')==26,'Saved metadata identity differs')
        except BaseException as error:store.event(STAGES[2],'failed',error_type=type(error).__name__);raise
        store.event(STAGES[2],'observed')
        store.event(STAGES[3],'started')
        try:
            with capture_warnings(warn):
                tactics_calls+=1;observe_final_call(save.tactics,target,receipt)
        except BaseException as error:
            store.event(STAGES[3],'failed',error_type=type(error).__name__)
            raise
        else:store.event(STAGES[3],'observed')
    except BaseException:
        traceback.print_exc();code=20
    finally:
        finalization_errors=[]
        def record(method,*args,**kwargs):
            try:method(*args,**kwargs)
            except BaseException as error:finalization_errors.append(type(error).__name__);traceback.print_exc()
        record(store.event,STAGES[4],'started')
        if save is not None:
            close.update(save_opened=True,attempted=True)
            try:
                with capture_warnings(warn):save.close()
                close['status']='closed'
            except BaseException as error:
                close.update(status='failed',error_type=type(error).__name__);traceback.print_exc();code=21
        after=None;after_error=None
        if input_validated:
            try:
                after=snapshot_receipt(p['snapshot'])
                store.write('snapshot-after.json',after)
                require(after==dict(sha256=SNAPSHOT_SHA,bytes=SNAPSHOT_BYTES),'Snapshot changed during diagnostic')
            except BaseException as error:after_error=type(error).__name__;traceback.print_exc();code=22
        else:after_error='InitialIdentityNotVerified';code=22
        record(store.write,'close.json',{**close,'reader_open_calls':open_calls,'tactics_calls':tactics_calls})
        if receipt:record(store.write,'marker.json',receipt)
        record(store.write,'warnings.json',warn)
        if close['status']=='failed' or after_error or finalization_errors:
            record(store.event,STAGES[4],'failed',error_type=after_error or close.get('error_type') or finalization_errors[0])
        else:record(store.event,STAGES[4],'observed')
        if finalization_errors:code=23
    return code


class BoundedOutput:
    def __init__(self,pipe,path):
        self.pipe,self.path=pipe,Path(path);self.exceeded=False;self.error_type=None;self.bytes=0
        self.thread=threading.Thread(target=self.pump,daemon=True)
    def pump(self):
        try:
            with self.path.open('xb') as output:
                while True:
                    chunk=self.pipe.read(4096)
                    if not chunk:break
                    left=BUDGET['stdout_bytes']-self.bytes
                    output.write(chunk[:left]);output.flush();self.bytes+=min(left,len(chunk))
                    if len(chunk)>left:self.exceeded=True;break
        except BaseException as error:self.error_type=type(error).__name__
    def start(self):self.thread.start()
    def finish(self):
        self.thread.join(timeout=.5)
        return not self.thread.is_alive() and self.error_type is None


def run(central,release_path):
    require((ROOT/'.git').is_dir() and Path(central).resolve()==ROOT.resolve(),'Run only from central checkout')
    c=read(ROOT/CONTRACT);verify_frozen(c,central);release=published_gate(c,release_path)
    now=datetime.now(timezone.utc);deadline=datetime.fromisoformat(BUDGET['deadline_utc'].replace('Z','+00:00'))
    require(now+timedelta(seconds=185)<deadline,'Insufficient remaining program deadline')
    p=paths(central);require(not p['private'].exists(),'Retained R3 directory: no retry or replacement')
    lease=NativeLease(Path(central)/'local/global-readers',EXPERIMENT,workers=1).acquire()
    process=None;job=None;assigned=False;proof=None;policy=None;output=None;returncode=None
    status='completed';failure=None;began=time.monotonic();go=False;store=None
    try:
        p['private'].mkdir(parents=True,exist_ok=False);store=PrivateStore(p['private'],'parent')
        store.write('attempt.json',dict(experiment_id=EXPERIMENT,supervisor_pid=os.getpid(),start_utc=now.isoformat(),
            contract_sha256_lf=normalized_hash(ROOT/CONTRACT),release=release,budget=BUDGET))
        store.event(STAGES[0],'observed')
        job=ReaderJob();policy=job.policy();token=secrets.token_hex(32)
        environment={**os.environ,'FM27_R3_TOKEN_SHA256':sha256(token.encode()).hexdigest(),'PYTHONDONTWRITEBYTECODE':'1'}
        for key in ('PYTHONHOME','PYTHONPATH','FM27_R3_ADMITTED','FM27_R3_BASE_SITE'):environment.pop(key,None)
        process=subprocess.Popen([sys._base_executable,'-I','-S','-B','-c',BOOTSTRAP],env=environment,cwd=ROOT,
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
        policy=job.assign(process);assigned=True
        store.write('launch.json',dict(decoder_pid=process.pid,membership_verified_before_go=True,job_policy=policy))
        output=BoundedOutput(process.stdout,p['private']/'stdout.txt');output.start()
        site=sysconfig.get_paths()['purelib']
        packet=dict(token=token,script=str(Path(__file__).resolve()),central=str(central),site=site,
                    runner_sha256=c['code_sha256_lf']['analysis/run_career004r3.py'])
        admission_monotonic=time.monotonic();admission_utc=datetime.now(timezone.utc)
        until=min(began+BUDGET['wall_seconds']-BUDGET['cleanup_reserve_seconds'],
                  admission_monotonic+(deadline-admission_utc).total_seconds()-BUDGET['cleanup_reserve_seconds'])
        require(admission_monotonic<until,
                'Reader admission deadline expired before GO')
        process.stdin.write((json.dumps(packet)+'\n').encode());process.stdin.flush();process.stdin.close();go=True
        while process.poll() is None:
            if time.monotonic()>=until or datetime.now(timezone.utc)>=deadline-timedelta(seconds=BUDGET['cleanup_reserve_seconds']):
                status='timeout';break
            if output.exceeded or output.error_type:status='output_cap_or_io_failure';break
            if sum(x.stat().st_size for x in p['private'].iterdir() if x.is_file())>ARTIFACT_CAP:
                status='artifact_cap';break
            time.sleep(.01)
        if process.poll() is not None:
            returncode=process.wait()
            if returncode and status=='completed':status='child_failed'
    except BaseException as error:failure=error;status='supervisor_failed'
    finally:
        if job is not None:
            proof=_cleanup(job,process,assigned,policy)
            proof['final_policy_verified']=job.final_policy is not None
            if job.final_policy is not None:proof['job_policy']=job.final_policy
        else:
            proof=dict(cleanup_confirmed=process is None,capsule_exit_confirmed=process is None,
                       kernel_active_processes=0 if process is None else None,job_policy=None)
        clean=confirmed_reader_cleanup(proof) if job is not None else process is None
        if process is not None:
            returncode=process.poll()
            if output is not None and not output.finish():status='output_completion_unconfirmed'
            if output is not None and output.exceeded:status='output_cap'
            if process.stdout is not None and (output is None or not output.thread.is_alive()):process.stdout.close()
        elapsed=time.monotonic()-began
        resources=dict(status=status,elapsed_seconds=elapsed,within_wall_limit=elapsed<=180,wall_limit_seconds=180,
            reader_processes_started=int(process is not None),go_sent=go,child_returncode=returncode,retries=0,
            private_artifact_bytes=sum(x.stat().st_size for x in p['private'].iterdir() if x.is_file()) if p['private'].exists() else 0,
            stdout_bytes=output.bytes if output else 0,stdout_truncated=output.exceeded if output else False,
            stdout_error_type=output.error_type if output else None,cleanup=proof,
            supervisor_error_type=type(failure).__name__ if failure else None)
        try:
            if output is not None and output.thread.is_alive():resources['private_artifact_bytes']=None
            elif store is not None:
                base_bytes=resources['private_artifact_bytes']
                for _ in range(8):
                    total=base_bytes+len(_encoded(dict(resources=resources)))
                    if resources['private_artifact_bytes']==total:break
                    resources['private_artifact_bytes']=total
            if store is not None:store.write('completion.json',dict(resources=resources))
        finally:
            if clean:lease.release()
        if not clean:raise RuntimeError('Reader cleanup unconfirmed; exclusive lease retained') from failure
    report=export(central)
    print(json.dumps(dict(status=report['execution_status'],stages=report['stages'],resources=report['resources'])))
    if failure is not None:raise failure
    return 0 if report['diagnostic_status']=='captured_expected_marker_failure' else 20


def _events(path):
    latest={};invalid=0
    if path.exists():
        if path.stat().st_size>BUDGET['stage_ledger_bytes']:
            return [dict(stage=s,status='unknown_retained_ledger_oversize') for s in STAGES],1
        for line in path.read_text(encoding='utf8').splitlines():
            try:
                row=json.loads(line)
                require(row['stage'] in STAGES and row['status'] in ('started','observed','failed','blocked'),'Invalid stage event')
                if 'error_type' in row:require(SAFE_CODE.fullmatch(row['error_type']),'Invalid error code')
                old=latest.get(row['stage'])
                require(old is None or old['status']=='started' and row['status']!='started','Repeated or reset stage')
                latest[row['stage']]={k:row[k] for k in ('stage','status','error_type') if k in row}
            except (ValueError,KeyError,TypeError):invalid+=1
    rows=[]
    for name in STAGES:
        row=dict(latest.get(name,dict(stage=name,status='not_started')))
        if row['status']=='started':row['status']='started_unresolved'
        rows.append(row)
    return rows,invalid


def _optional(private,name,issues):
    path=private/name
    if not path.exists():issues.append(dict(receipt=name,status='missing'));return None
    try:
        require(path.stat().st_size<=BUDGET['child_metadata_bytes'],'Oversize retained JSON')
        value=read(path);require(isinstance(value,dict),'Non-object receipt')
        return value
    except (ValueError,OSError):issues.append(dict(receipt=name,status='invalid_retained'));return None


def public_marker(receipt):
    if not isinstance(receipt,dict):return None
    status=receipt.get('status')
    require(status in ('captured_final_target_failure','non_target_error','observer_rejected_frame','no_final_exception'),
            'Unknown diagnostic code')
    result=dict(status=status)
    if status=='captured_final_target_failure':
        values={k:receipt.get(k) for k in ('section_bytes','block_start','block_end','cursor',
                                         'cursor_relative_to_block','bytes_remaining_in_block')}
        require(all(type(x) is int and 0<=x<=512*1024**2 for x in values.values()),'Diagnostic offsets out of bounds')
        require(values['block_start']<=values['cursor']<=values['block_end']<=values['section_bytes'] and
                values['cursor_relative_to_block']==values['cursor']-values['block_start'] and
                values['bytes_remaining_in_block']==values['block_end']-values['cursor'],'Diagnostic bounds inconsistent')
        checks=[]
        for item in receipt.get('marker_checks',[]):
            require(type(item.get('marker_index')) is int and 0<=item['marker_index']<4 and
                    type(item.get('expected_width_bytes')) is int and 1<=item['expected_width_bytes']<=16 and
                    type(item.get('fully_inside_block')) is bool and type(item.get('equals_expected_at_cursor')) is bool,
                    'Invalid marker comparisons')
            checks.append({k:item[k] for k in ('marker_index','expected_width_bytes','fully_inside_block','equals_expected_at_cursor')})
        require(1<=len(checks)<=4,'Marker denominator missing')
        require([r['marker_index'] for r in checks]==list(range(len(checks))),'Duplicated or incomplete marker indices')
        # Exact private offsets never leave the private receipt. Only bounded distances.
        require(receipt.get('raw_values_captured') is False and receipt.get('grammar_changed') is False and
                receipt.get('scan_performed') is False and receipt.get('failure_consistent_with_expected_marker_tests') is True and
                not any(x['equals_expected_at_cursor'] for x in checks),'Marker evidence contradicts failure policy')
        block_bytes=values['block_end']-values['block_start']
        remaining=values['bytes_remaining_in_block']
        result.update(section_bytes=values['section_bytes'],block_bytes=block_bytes,
            cursor_decile_in_block=min(10,(10*values['cursor_relative_to_block']//block_bytes)) if block_bytes else None,
            remaining_bytes_power2_upper=2**((remaining-1).bit_length()) if remaining else 0,
            marker_checks=checks,grammar_changed=False,scan_performed=False)
    return result


def public_resources(resources):
    require(isinstance(resources,dict),'Missing resource object')
    states=('completed','timeout','output_cap_or_io_failure','artifact_cap','child_failed','supervisor_failed',
            'output_completion_unconfirmed','output_cap')
    require(resources.get('status') in states,'Invalid resource status')
    result={}
    for key in ('elapsed_seconds','wall_limit_seconds','reader_processes_started','child_returncode','retries',
                'private_artifact_bytes','stdout_bytes'):
        value=resources.get(key)
        require(value is None or type(value) in (int,float) and math.isfinite(value),'Non-numeric resource field')
        if key!='elapsed_seconds':require(value is None or type(value) is int,'Count is not an integer')
        if key!='child_returncode':require(value is None or 0<=value<=2**63-1,'Negative resource count')
        result[key]=value
    for key in ('within_wall_limit','go_sent','stdout_truncated'):
        value=resources.get(key);require(type(value) is bool,'Invalid resource boolean');result[key]=value
    result['status']=resources['status'];proof=resources.get('cleanup')
    result['cleanup_confirmed']=confirmed_reader_cleanup(proof);policy=proof.get('job_policy') if isinstance(proof,dict) else None
    if policy is not None:
        require(isinstance(policy,dict),'Invalid job policy')
        numeric=('limit_flags','active_process_limit','process_memory_limit','job_memory_limit',
                 'peak_process_private_bytes','peak_job_private_bytes')
        require(all(type(policy.get(k)) is int and 0<=policy[k]<=2**63-1 for k in numeric),'Non-numeric kernel policy')
        require(type(policy.get('kill_on_close')) is bool and type(policy.get('breakaway_allowed')) is bool,'Invalid kernel policy flags')
        result['job_policy']={k:policy[k] for k in numeric+('kill_on_close','breakaway_allowed')}
    else:result['job_policy']=None
    return result


def export(central):
    """Retained JSON only: never hash/open a save, restart a child, or reconcile lease."""
    private=paths(central)['private'];issues=[];attempt=_optional(private,'attempt.json',issues)
    stages,invalid=_events(private/'events.jsonl');completion=_optional(private,'completion.json',issues)
    before=_optional(private,'snapshot-before.json',issues);after=_optional(private,'snapshot-after.json',issues)
    marker_receipt=_optional(private,'marker.json',issues);close=_optional(private,'close.json',issues)
    setup=_optional(private,'child-setup.json',issues)
    setup_summary=None
    if setup is not None:
        try:
            require(setup.get('status') in ('verified_official_reader','failed'),'Invalid child setup status')
            setup_summary=dict(status=setup['status'])
            if setup['status']=='failed':
                require(SAFE_CODE.fullmatch(setup['error_type']),'Invalid child setup code')
                setup_summary['error_type']=setup['error_type']
            else:
                require(setup.get('package_version')=='0.12.4','Wrong setup package')
                setup_summary['package_version']='0.12.4'
        except (ValueError,TypeError,KeyError):setup_summary=None;issues.append(dict(receipt='child-setup.json',status='invalid_retained'))
    try:marker=public_marker(marker_receipt)
    except (ValueError,TypeError,KeyError):marker=None;issues.append(dict(receipt='marker.json',status='invalid_retained'))
    warn=_optional(private,'warnings.json',issues);resources=completion.get('resources') if isinstance(completion,dict) else None
    stable=before==after==dict(sha256=SNAPSHOT_SHA,bytes=SNAPSHOT_BYTES) if before is not None and after is not None else None
    summary=None
    if resources is not None:
        try:summary=public_resources(resources)
        except (ValueError,TypeError,KeyError):resources=None;issues.append(dict(receipt='completion.json',status='invalid_retained'))
    categories=None
    if warn is not None:
        try:
            require(type(warn.get('count')) is int and 0<=warn['count']<=33 and type(warn.get('truncated')) is bool,
                    'Malformed warning ledger')
            categories={}
            for item in warn.get('items',[]):
                require(SAFE_CODE.fullmatch(item['category']),'Invalid warning category')
                categories[item['category']]=categories.get(item['category'],0)+1
            require(sum(categories.values())==warn['count'] or warn['truncated'],'Warning denominator missing')
        except (ValueError,TypeError,KeyError):warn=None;categories=None;issues.append(dict(receipt='warnings.json',status='invalid_retained'))
    release=None;contract_hash=None
    if attempt is not None:
        try:
            old=attempt['release'];contract_hash=attempt['contract_sha256_lf']
            require(re.fullmatch(r'[0-9a-f]{40}',old['published_commit']) and type(old['ci_run']) is int and old['ci_run']>0 and
                    all(HEX.fullmatch(h) for h in (old['review_sha256'],old['reviewed_contract_sha256'],contract_hash)) and
                    old['reviewed_contract_sha256']==contract_hash and attempt['experiment_id']==EXPERIMENT,
                    'Invalid publication hashes')
            release={k:old[k] for k in ('published_commit','ci_run','review_sha256','reviewed_contract_sha256')}
        except (ValueError,TypeError,KeyError):contract_hash=None;issues.append(dict(receipt='attempt.json',status='invalid_retained'))
    open_calls=close.get('reader_open_calls') if close else None;tactics_calls=close.get('tactics_calls') if close else None
    if type(open_calls) is not int or open_calls not in (0,1):open_calls=None
    if type(tactics_calls) is not int or tactics_calls not in (0,1):tactics_calls=None
    complete=all(r['status'] in ('observed','failed','blocked') for r in stages) and invalid==0 and not issues
    captured=(marker is not None and marker['status']=='captured_final_target_failure' and stable is True and
        [r['expected_width_bytes'] for r in marker['marker_checks']]==POLICY['expected_marker_widths'] and
        close is not None and close.get('status')=='closed' and resources is not None and
        confirmed_reader_cleanup(resources.get('cleanup')) and resources.get('within_wall_limit') is True and
        resources.get('status')=='child_failed' and resources.get('child_returncode')==20 and invalid==0 and
        warn is not None and warn['truncated'] is False and categories=={'UnknownBuildWarning':1} and
        open_calls==tactics_calls==1 and resources.get('reader_processes_started')==1 and resources.get('go_sent') is True and
        resources.get('private_artifact_bytes') is not None and resources['private_artifact_bytes']<=ARTIFACT_CAP and
        resources.get('stdout_truncated') is False and resources.get('retries')==0 and not issues and
        [r['status'] for r in stages]==['observed','observed','observed','failed','observed'] and
        stages[3].get('error_type')=='ReaderCheckError')
    report=dict(experiment_id=EXPERIMENT,version=VERSION,
        execution_status='accounted' if complete and resources is not None else 'incomplete_or_abandoned',
        diagnostic_status='captured_expected_marker_failure' if captured else 'not_captured_or_not_technically_valid',
        stages=stages,invalid_event_lines=invalid,receipt_issues=issues,child_setup=setup_summary,resources=summary,snapshot_stable=stable,
        snapshot_sha256=SNAPSHOT_SHA if stable else None,marker=marker,
        warnings=None if warn is None else dict(count=warn['count'],categories=categories,truncated=warn['truncated']),
        reader_open_calls=open_calls,tactics_calls=tactics_calls,
        native_starts=0,calendar_advances=0,seeds_reserved=0,native_semantics_verified=False,
        tactics_released=False,replay_released=False,training_effect_released=False,career_advance_released=False,
        release=release,contract_sha256_lf=contract_hash,
        evidence_sha256={n:byte_hash(private/n) for n in sorted(PrivateStore.PARENT|PrivateStore.CHILD|{'events.jsonl','stdout.txt'})
                         if (private/n).is_file() and (private/n).stat().st_size<=ARTIFACT_CAP})
    PUBLIC.mkdir(parents=True,exist_ok=True);(PUBLIC/'run-status.json').write_bytes(_encoded(report))
    return report


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('phase',choices=('prepare','run','child','export'))
    parser.add_argument('--central',type=Path,required=True)
    parser.add_argument('--release',type=Path)
    args=parser.parse_args()
    if args.phase=='prepare':prepare(args.central)
    elif args.phase=='child':raise SystemExit(child(args.central))
    elif args.phase=='export':print(json.dumps(export(args.central)))
    else:
        require(args.release is not None,'Published Director release required')
        raise SystemExit(run(args.central,args.release))

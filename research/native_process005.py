"""Windows-kernel process containment for centrally budgeted native calls.

Only the harmless base-Python capsule starts before job assignment. A private
stdin/token gate admits the real command after verified kill-on-close, process
limit and membership. No engine, game, server, registry or UI imports exist here.
"""
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
from hashlib import sha256
import hmac
import json
import math
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

SCHEMA = 'fm27.contained-call.v1'
FLAGS = 0x2000 | 0x8  # KILL_ON_JOB_CLOSE | ACTIVE_PROCESS; no breakaway flags.
TOKEN_ENV = '_FM27_CAPSULE_TOKEN_SHA256'
ADMITTED_ENV = 'FM27_CONTAINED_CALL_V1'


class CleanupUnconfirmed(RuntimeError):
    """Caller must retain its lease/budget crash marker and start nothing else."""
    def __init__(self, evidence):
        self.evidence = evidence
        super().__init__('Kernel process-tree cleanup could not be confirmed; retain execution lease')


class ProcessTreeIncomplete(RuntimeError):
    """Command parent exited while descendants remained; cleanup was performed."""


def _require(ok, message):
    if not ok:
        raise ValueError(message)


class _Basic(ctypes.Structure):
    _fields_ = [('process_time',ctypes.c_int64),('job_time',ctypes.c_int64),
        ('flags',wintypes.DWORD),('min_ws',ctypes.c_size_t),('max_ws',ctypes.c_size_t),
        ('active_limit',wintypes.DWORD),('affinity',ctypes.c_size_t),
        ('priority',wintypes.DWORD),('scheduling',wintypes.DWORD)]


class _IO(ctypes.Structure):
    _fields_ = [(k,ctypes.c_uint64) for k in ('reads','writes','others','read_bytes','write_bytes','other_bytes')]


class _Extended(ctypes.Structure):
    _fields_ = [('basic',_Basic),('io',_IO),('process_memory',ctypes.c_size_t),
        ('job_memory',ctypes.c_size_t),('peak_process_memory',ctypes.c_size_t),('peak_job_memory',ctypes.c_size_t)]


class _Accounting(ctypes.Structure):
    _fields_ = [(k,ctypes.c_int64) for k in ('user','kernel','period_user','period_kernel')]+[
        ('page_faults',wintypes.DWORD),('total_processes',wintypes.DWORD),
        ('active_processes',wintypes.DWORD),('terminated_processes',wintypes.DWORD)]


class _WindowsJob:
    def __init__(self, limit=3):
        _require(os.name == 'nt', 'Windows kernel job required')
        _require(type(limit) is int and 1 <= limit <= 10, 'Invalid internal process limit')
        self.limit,self.handle = limit,None
        self.k = ctypes.WinDLL('kernel32',use_last_error=True)
        k=self.k
        k.CreateJobObjectW.argtypes=[ctypes.c_void_p,wintypes.LPCWSTR];k.CreateJobObjectW.restype=wintypes.HANDLE
        k.SetInformationJobObject.argtypes=[wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD];k.SetInformationJobObject.restype=wintypes.BOOL
        k.QueryInformationJobObject.argtypes=[wintypes.HANDLE,ctypes.c_int,ctypes.c_void_p,wintypes.DWORD,ctypes.c_void_p];k.QueryInformationJobObject.restype=wintypes.BOOL
        k.AssignProcessToJobObject.argtypes=[wintypes.HANDLE,wintypes.HANDLE];k.AssignProcessToJobObject.restype=wintypes.BOOL
        k.IsProcessInJob.argtypes=[wintypes.HANDLE,wintypes.HANDLE,ctypes.POINTER(wintypes.BOOL)];k.IsProcessInJob.restype=wintypes.BOOL
        k.TerminateJobObject.argtypes=[wintypes.HANDLE,wintypes.UINT];k.TerminateJobObject.restype=wintypes.BOOL
        k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
        self.handle=k.CreateJobObjectW(None,None)  # unnamed, noninheritable handle
        if not self.handle:raise ctypes.WinError(ctypes.get_last_error())
        try:
            info=_Extended();info.basic.flags=FLAGS;info.basic.active_limit=limit
            if not k.SetInformationJobObject(self.handle,9,ctypes.byref(info),ctypes.sizeof(info)):
                raise ctypes.WinError(ctypes.get_last_error())
            self.policy()
        except BaseException:
            self.close();raise

    def policy(self):
        info=_Extended()
        if not self.k.QueryInformationJobObject(self.handle,9,ctypes.byref(info),ctypes.sizeof(info),None):
            raise ctypes.WinError(ctypes.get_last_error())
        _require(info.basic.flags == FLAGS and info.basic.active_limit == self.limit,
                 'Kernel job limits differ; no permission to start command')
        return dict(limit_flags=int(info.basic.flags),active_process_limit=int(info.basic.active_limit),
                    kill_on_close=True,breakaway_allowed=False,memory_limit_claimed=False)

    def assign(self, process):
        if not self.k.AssignProcessToJobObject(self.handle,int(process._handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        member=wintypes.BOOL()
        if not self.k.IsProcessInJob(int(process._handle),self.handle,ctypes.byref(member)):
            raise ctypes.WinError(ctypes.get_last_error())
        _require(member.value != 0, 'Capsule not in the specific owning job')
        return self.policy()

    def accounting(self):
        value=_Accounting()
        if not self.k.QueryInformationJobObject(self.handle,1,ctypes.byref(value),ctypes.sizeof(value),None):
            raise ctypes.WinError(ctypes.get_last_error())
        return dict(kernel_active_processes=int(value.active_processes),
                    kernel_total_processes=int(value.total_processes),
                    kernel_total_terminated_processes=int(value.terminated_processes))

    def terminate(self):
        if not self.k.TerminateJobObject(self.handle,254):
            raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:
            if not self.k.CloseHandle(self.handle):raise ctypes.WinError(ctypes.get_last_error())
            self.handle=None


def _write_json(path, value):
    # Exclusive files: retain even a partial receipt; never repair an old attempt.
    with Path(path).open('x',encoding='utf8',newline='\n') as stream:
        json.dump(value,stream,allow_nan=False,indent=2);stream.write('\n')
        stream.flush();os.fsync(stream.fileno())


def _progress_signature(path):
    try:
        value=path.stat()
    except FileNotFoundError:
        return None
    return value.st_size,value.st_mtime_ns


def _cleanup(job, process, assigned, policy):
    proof=dict(schema=SCHEMA,job_policy=policy,capsule_started=process is not None,
        capsule_exit_confirmed=process is None,cleanup_confirmed=False,
        kernel_active_processes=None,terminate_job_succeeded=False,kill_close_fallback=False,
        cleanup_error_types=[])
    deadline=time.monotonic()+3
    if process is not None and process.stdin is not None:
        try:process.stdin.close()
        except BaseException as error:
            if type(error).__name__ not in proof['cleanup_error_types']:
                proof['cleanup_error_types'].append(type(error).__name__)
    try:job.terminate();proof['terminate_job_succeeded']=True
    except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
    # Before assignment, no GO was sent and the capsule can only wait/read stdin.
    if process is not None and not assigned and process.poll() is None:
        try:process.kill()
        except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
    if process is not None:
        try:process.wait(timeout=max(.01,deadline-time.monotonic()));proof['capsule_exit_confirmed']=True
        except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
    while time.monotonic()<deadline:
        try:
            proof.update(job.accounting())
            if proof['kernel_active_processes']==0 and proof['capsule_exit_confirmed']:
                proof['cleanup_confirmed']=True;break
        except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
        time.sleep(.01)
    if not proof['cleanup_confirmed']:proof['kill_close_fallback']=True
    try:job.close()
    except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
    # Closing an unconfirmed job is a safety fallback, NOT proof of zero processes.
    if not proof['cleanup_confirmed'] and process is not None:
        try:process.wait(timeout=1);proof['capsule_exit_confirmed']=True
        except BaseException as error:proof['cleanup_error_types'].append(type(error).__name__)
    return proof


def confirmed_cleanup(output, expected_limit=None):
    try:proof=json.loads(Path(output).with_suffix('.containment.json').read_text(encoding='utf8'))
    except (OSError,ValueError):return False
    if not isinstance(proof,dict):return False
    policy=proof.get('job_policy')
    if not isinstance(policy,dict):return False
    limit=policy.get('active_process_limit')
    return (proof.get('schema')==SCHEMA and proof.get('cleanup_confirmed') is True and
        proof.get('capsule_exit_confirmed') is True and type(proof.get('kernel_active_processes')) is int and
        proof['kernel_active_processes']==0 and type(limit) is int and 3<=limit<=10 and
        (expected_limit is None or limit==expected_limit) and policy.get('limit_flags')==FLAGS and
        policy.get('kill_on_close') is True and policy.get('breakaway_allowed') is False)


def contained_call(command,env,log,output,timeout=90,on_start=None,*,max_processes=3,total_timeout=None):
    """Return only after kernel-zero + capsule exit; retain receipts on every path.

    timeout is no-progress time for `log`; None disables it when a finite
    total_timeout bounds a whole study. Individual engine workers still need
    their own90s progress watchdog. max_processes counts all processes, not workers.
    """
    _require(os.name=='nt','Windows kernel containment is mandatory')
    _require(type(max_processes) is int and 3<=max_processes<=10,'Process cap must be an integer3..10')
    for value in (timeout,total_timeout):
        _require(value is None or (type(value) in (int,float) and math.isfinite(value) and value>0),
                 'Positive finite timeout or None required')
    _require(timeout is not None or total_timeout is not None,'At least one execution deadline required')
    _require(isinstance(command,(list,tuple)) and command and all(type(s) is str and s and '\0' not in s for s in command),
             'Explicit nonempty argument list required')
    output,log=Path(output),Path(log)
    receipt=output.with_suffix('.process.json');final=output.with_suffix('.containment.json')
    _require(not receipt.exists() and not final.exists(),'Retained containment evidence: no restart')
    base=getattr(sys,'_base_executable',None)
    _require(base and Path(base).is_file(),'Direct base Python required; no venv redirector')
    began=time.monotonic();process=None;assigned=False;policy=None;proof=None;failure=None;go=False
    job=_WindowsJob(max_processes)
    try:
        policy=job.policy()
        with output.open('xb') as stream:
            token=secrets.token_hex(32)
            capsule_env=dict(env);capsule_env[TOKEN_ENV]=sha256(token.encode()).hexdigest()
            process=subprocess.Popen([base,'-I',str(Path(__file__).resolve()),'--capsule'],
                env=capsule_env,stdin=subprocess.PIPE,stdout=stream,stderr=subprocess.STDOUT,
                creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
            policy=job.assign(process);assigned=True
            _write_json(receipt,dict(schema=SCHEMA,capsule_pid=process.pid,
                started_utc=datetime.now(timezone.utc).isoformat(),job_policy=policy,
                membership_verified_before_go=True,host_start_permission_sent=False))
            packet=json.dumps(dict(token=token,command=list(command),cwd=env.get('FM27_ENGINE_ROOT'))).encode()+b'\n'
            process.stdin.write(packet);process.stdin.flush();process.stdin.close();go=True
            if on_start is not None:on_start()
            progress=time.monotonic();signature=None
            while process.poll() is None:
                now=time.monotonic()
                if total_timeout is not None and now-began>total_timeout:raise TimeoutError('Contained total deadline exceeded')
                if timeout is not None:
                    current=_progress_signature(log)
                    if current is not None and current!=signature:signature=current;progress=now
                    if now-progress>timeout:raise TimeoutError('Contained command progress deadline exceeded')
                time.sleep(.02)
            code=process.wait()
            if total_timeout is not None and time.monotonic()-began>total_timeout:
                raise TimeoutError('Contained total deadline exceeded')
            # Permit accounting to settle after a normal process exit, not a live orphan.
            settle=time.monotonic()+.1
            while job.accounting()['kernel_active_processes'] and time.monotonic()<settle:time.sleep(.01)
            orphan=job.accounting()['kernel_active_processes']>0
            proof=_cleanup(job,process,assigned,policy)
            if not proof['cleanup_confirmed']:raise CleanupUnconfirmed(proof)
            if orphan:raise ProcessTreeIncomplete('Command parent exited with retained descendants; terminated whole job')
    except BaseException as error:
        failure=error
    finally:
        if proof is None:proof=_cleanup(job,process,assigned,policy)
        proof.update(host_start_permission_sent=go,elapsed_seconds=time.monotonic()-began,
                     error_type=type(failure).__name__ if failure else None)
        try:_write_json(final,proof)
        except BaseException as error:
            proof['receipt_error_type']=type(error).__name__
            if failure is None:failure=error
    if not proof['cleanup_confirmed']:raise CleanupUnconfirmed(proof) from failure
    if failure is not None:
        if isinstance(failure,CleanupUnconfirmed):raise failure
        try:failure.containment_evidence=proof
        except BaseException:pass
        raise failure
    return code,time.monotonic()-began


def _capsule():
    # No host launch before this one private packet. EOF/invalid packets simply exit.
    line=sys.stdin.buffer.readline(128*1024+1)
    if not line or len(line)>128*1024:return 234
    try:
        packet=json.loads(line)
        if set(packet)!={'token','command','cwd'}:return 234
        token=packet['token'];expected=os.environ.get(TOKEN_ENV,'')
        if type(token) is not str or not hmac.compare_digest(sha256(token.encode()).hexdigest(),expected):return 234
        command=packet['command']
        if not isinstance(command,list) or not command or any(type(s) is not str or not s or '\0'in s for s in command):return 234
        k=ctypes.WinDLL('kernel32',use_last_error=True)
        k.GetCurrentProcess.restype=wintypes.HANDLE
        k.IsProcessInJob.argtypes=[wintypes.HANDLE,wintypes.HANDLE,ctypes.POINTER(wintypes.BOOL)]
        k.IsProcessInJob.restype=wintypes.BOOL;member=wintypes.BOOL()
        if not k.IsProcessInJob(k.GetCurrentProcess(),None,ctypes.byref(member)) or not member.value:return 234
        env=dict(os.environ);env.pop(TOKEN_ENV,None);env[ADMITTED_ENV]='1'
        host=subprocess.Popen(command,env=env,cwd=packet['cwd'],stdin=subprocess.DEVNULL,
            stdout=sys.stdout,stderr=sys.stderr,creationflags=subprocess.CREATE_NO_WINDOW,close_fds=True)
        return host.wait()
    except BaseException:
        return 235


if __name__=='__main__':
    if sys.argv[1:]!=['--capsule']:raise SystemExit('Internal capsule only; import contained_call')
    raise SystemExit(_capsule())

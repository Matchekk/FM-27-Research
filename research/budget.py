"""Persistent attempt caps and a supervised cumulative native-wall-time budget."""
from datetime import datetime, timezone, timedelta
import json
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import secrets
import time

from .native import read, require


def supervisor_alive(pid):
    if os.name!="nt":
        return os.getppid()==pid
    import ctypes
    from ctypes import wintypes
    kernel=ctypes.WinDLL("kernel32",use_last_error=True)
    kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
    kernel.OpenProcess.restype=wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD]
    kernel.CloseHandle.argtypes=[wintypes.HANDLE]
    handle=kernel.OpenProcess(0x100000,False,pid)
    if not handle:
        return False
    try:
        return kernel.WaitForSingleObject(handle,0)==258
    finally:
        kernel.CloseHandle(handle)


def atomic(path, value):
    path=Path(path)
    temporary=path.with_suffix(path.suffix+".pending")
    with temporary.open("w",encoding="utf8",newline="\n") as stream:
        stream.write(json.dumps(value,allow_nan=False,indent=2)+"\n")
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


class NativeBudget:
    """Reservations are never refunded. An interrupted operation blocks new work.

    Charged time is whole supervised child wall time, conservatively including Python
    preparation/audits. Five seconds are reserved for process-tree termination.
    """
    def __init__(self,path,experiment="TACT-001-P0",seconds=900,caps=None):
        self.path=Path(path)
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.caps=caps or {"technical":24,"main":128}
        self.experiment,self.seconds=experiment,seconds
        if not self.path.exists():
            # Exclusive creation prevents a second initialiser from resetting a budget.
            with self.path.open("x",encoding="utf8") as stream:
                json.dump(dict(experiment=experiment,limits=self.caps,limit_seconds=seconds,
                               charged_seconds=0.,reserved={},operations=[],active=None,halted=False),stream)
                stream.flush()
                os.fsync(stream.fileno())
        self.load()

    def load(self):
        state=read(self.path)
        require(state["experiment"]==self.experiment and state["limits"]==self.caps and
                state["limit_seconds"]==self.seconds,"Existing budget identity/limits differ")
        return state

    def reserve(self,name,kind,keys):
        state=self.load()
        require(not state["active"] and not state["halted"],"Interrupted/failed native operation: execution blocked")
        require(name not in {o["name"] for o in state["operations"]},"Operation already attempted; no retry")
        require(len(set(keys))==len(keys),"Duplicate job reservations")
        prior=state["reserved"]
        require(not set(keys)&set(prior),"Job already reserved; no restart retry")
        require(kind in self.caps and sum(k==kind for k in prior.values())+len(keys)<=self.caps[kind],"Cumulative match cap exceeded")
        remaining=self.seconds-state["charged_seconds"]
        require(remaining>5,"Native time budget exhausted")
        start=datetime.now(timezone.utc)
        state["reserved"].update({key:kind for key in keys})
        state["active"]=dict(name=name,kind=kind,keys=keys,start_utc=start.isoformat(),
                             supervisor_pid=os.getpid(),child_deadline_utc=(start+timedelta(seconds=remaining-5)).isoformat())
        atomic(self.path,state)
        return remaining-5

    def finish(self,elapsed,returncode,timed_out=False):
        state=self.load()
        require(state["active"] is not None,"No reserved operation")
        operation=state["active"]
        operation.update(elapsed_seconds=elapsed,returncode=returncode,timed_out=timed_out)
        state["charged_seconds"]+=elapsed
        state["operations"].append(operation)
        state["active"]=None
        state["halted"]=timed_out or returncode!=0 or state["charged_seconds"]>=self.seconds
        atomic(self.path,state)

    def run(self,name,kind,keys,command,cwd,stdout):
        lock=self.path.with_suffix(".lock")
        lock.touch(exist_ok=False)
        process=None
        try:
            allowance=self.reserve(name,kind,keys)
            began=time.perf_counter()
            timed_out=False
            token=secrets.token_hex(32)
            state=self.load()
            state["active"]["token_sha256"]=sha256(token.encode()).hexdigest()
            atomic(self.path,state)
            with Path(stdout).open("wb") as stream:
                process=subprocess.Popen(command,cwd=cwd,stdout=stream,stderr=subprocess.STDOUT,
                    env={**os.environ,"TACT_P0_SUPERVISOR_TOKEN":token},
                    creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                state=self.load()
                state["active"]["supervised_pid"]=process.pid
                atomic(self.path,state)
                try:
                    process.wait(timeout=allowance)
                except subprocess.TimeoutExpired:
                    timed_out=True
                    if os.name=="nt":
                        subprocess.run(["taskkill","/PID",str(process.pid),"/T","/F"],capture_output=True,timeout=4)
                    else:
                        process.kill()
                    process.wait(timeout=4)
            self.finish(time.perf_counter()-began,process.returncode,timed_out)
            require(not timed_out and process.returncode==0,"Native operation failed or exceeded deadline; retained and halted")
        finally:
            # If the supervisor itself crashes or cannot reconcile its child, active
            # remains in the durable file. A new process then refuses execution.
            lock.unlink()

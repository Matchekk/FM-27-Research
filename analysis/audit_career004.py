"""Single bounded read-only audit of the explicitly approved Test FM Research save."""
from argparse import ArgumentParser
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import warnings

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.career_readonly004 import (PROBES,digest,public_report,section_summary,
    snapshot,source_inventory,summarize_probe,write)


def append(path,row):
    with Path(path).open('a',encoding='utf8') as stream:
        stream.write(json.dumps(row,ensure_ascii=False,allow_nan=False,default=str)+'\n')
        stream.flush();os.fsync(stream.fileno())


def child(private):
    import fmsave
    events=private/'events.jsonl';events.touch(exist_ok=False)
    context={};save=None
    append(events,dict(probe='open',status='started'))
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            save=fmsave.open(private/'snapshot.fm',strict=True)
        info=save.info
        append(events,dict(probe='open',status='ok',coverage=section_summary(info),
                          warning_types=[type(w.message).__name__ for w in caught]))
        for name in PROBES[1:]:
            append(events,dict(probe=name,status='started'))
            try:
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter('always')
                    value=getattr(save,name)()
                coverage=summarize_probe(name,value,context,info)
                append(events,dict(probe=name,status='ok',coverage=coverage,
                                  warning_types=[type(w.message).__name__ for w in caught]))
            except Exception as error:
                append(events,dict(probe=name,status='failed',error_type=type(error).__name__,
                                  private_error=str(error)))
    except Exception as error:
        append(events,dict(probe='open',status='failed',error_type=type(error).__name__,
                          private_error=str(error)))
    finally:
        if save is not None:save.close()


def private_bytes(pid):
    """Observe only our own Python child, never the Football Manager process."""
    import ctypes
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD),
                  *[(name,ctypes.c_size_t) for name in ('PeakWorkingSetSize','WorkingSetSize',
                  'QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage',
                  'QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage')]]
    kernel=ctypes.WinDLL('kernel32',use_last_error=True);psapi=ctypes.WinDLL('psapi',use_last_error=True)
    kernel.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];kernel.OpenProcess.restype=wintypes.HANDLE
    kernel.CloseHandle.argtypes=[wintypes.HANDLE];kernel.CloseHandle.restype=wintypes.BOOL
    psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    psapi.GetProcessMemoryInfo.restype=wintypes.BOOL
    handle=kernel.OpenProcess(0x410,False,pid)
    if not handle:return None
    try:
        info=Counters();info.cb=ctypes.sizeof(info)
        if not psapi.GetProcessMemoryInfo(handle,ctypes.byref(info),info.cb):return None
        return int(info.PrivateUsage)
    finally:kernel.CloseHandle(handle)


def run(source,private,public):
    began=time.monotonic();started=datetime.now(timezone.utc).isoformat()
    private.mkdir(parents=True,exist_ok=True)
    # This durable marker is never removed/refunded, including failed preparation.
    marker=private/'attempt.json'
    with marker.open('x',encoding='utf8') as stream:
        json.dump(dict(status='started',start_utc=started,max_seconds=180,
                       max_observed_private_bytes=1536*1024**2,probes=list(PROBES)),stream,indent=2)
        stream.flush();os.fsync(stream.fileno())
    inventory=source_inventory()
    receipt=snapshot(source,private/'snapshot.fm','Test FM Research.fm')
    write(private/'snapshot-receipt.json',receipt)
    status='source_drift';returncode=None;peak=0;child_started=False
    if receipt['stable'] and time.monotonic()-began>=180:status='timeout_before_reader'
    elif receipt['stable']:
        if os.name!='nt':raise ValueError('This real-save runner requires its Windows memory observer')
        with (private/'stdout.txt').open('xb') as output:
            process=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--child','--private',str(private)],
                cwd=ROOT,stdout=output,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
            child_started=True;status='completed'
            while process.poll() is None:
                observed=private_bytes(process.pid)
                if observed is None:
                    if process.poll() is not None:break
                    status='memory_observer_failed';process.kill();break
                peak=max(peak,observed)
                if observed>1536*1024**2:status='memory_cap';process.kill();break
                if time.monotonic()-began>180:status='timeout';process.kill();break
                if sum(p.stat().st_size for p in private.rglob('*') if p.is_file())>1024**3:
                    status='artifact_cap';process.kill();break
                time.sleep(.2)
            returncode=process.wait(timeout=5)
            if returncode and status=='completed':status='child_failed'
            if time.monotonic()-began>180 and status=='completed':status='deadline_exceeded'
    resources=dict(status=status,start_utc=started,elapsed_seconds=time.monotonic()-began,
        max_seconds=180,child_started=child_started,child_returncode=returncode,
        max_observed_private_bytes=peak,private_bytes_limit=1536*1024**2,
        memory_observation_interval_seconds=.2,hard_kernel_memory_limit=False,
        retries=0,reader_processes_started=int(child_started))
    events=[]
    path=private/'events.jsonl'
    if path.exists():
        for line in path.read_text(encoding='utf8').splitlines():
            try:events.append(json.loads(line))
            except json.JSONDecodeError:resources['partial_event_line_retained']=True
    final_hash=digest(source)
    result=public_report(events,receipt,inventory,resources,final_hash)
    write(private/'attempt.json',dict(resources=resources,snapshot=receipt))
    write(public/'coverage.json',result)
    print(json.dumps(dict(experiment_id=result['experiment_id'],resources=resources,
                         stable=result['snapshot']['stable_through_reader'],
                         statuses={p['probe']:p['status'] for p in result['probes']}),indent=2))


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path)
    parser.add_argument('--private',type=Path,required=True)
    parser.add_argument('--public',type=Path,default=ROOT/'data/night-001-career')
    parser.add_argument('--child',action='store_true')
    args=parser.parse_args()
    if args.child:child(args.private)
    else:
        parser.error('--source is required') if args.source is None else None
        run(args.source,args.private,args.public)

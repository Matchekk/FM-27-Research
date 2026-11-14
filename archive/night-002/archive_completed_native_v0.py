"""Lossless storage compaction of completed MECH004 evidence; no native calls.

Frozen inputs, runner, budgets and measurements remain untouched. Restore all
original paths before export/review. Archives and hash journals stay private.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from zipfile import ZipFile,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native_process005 import confirmed_cleanup

FILES=('input.json','native-exit.json','native.containment.json','native.jsonl','native.process.json','native.stdout')


def check(value,message):
    if not value:raise ValueError(message)


def digest(path):return sha256(Path(path).read_bytes()).hexdigest()


def below(path,base):
    path=Path(path);base=Path(base).resolve()
    check(not path.is_symlink() and path.resolve().is_relative_to(base),'Evidence path escaped study')
    check(not (getattr(path.lstat(),'st_file_attributes',0)&0x400),'Reparse evidence forbidden')
    return path


def ledger(path):
    data=path.read_bytes();end=data.rfind(b'\n')
    return [json.loads(line) for line in data[:end+1].splitlines()] if end>=0 else []


def archive(base,limit=32):
    base=Path(base).resolve();directory=base/'completed-archives';directory.mkdir(exist_ok=True)
    candidates=[]
    for row in ledger(base/'dispatch/ledger.jsonl'):
        key=row['job_id']
        check(re.fullmatch(r'(high_press|deep_block)-[1-9][0-9]*-[01]-C90[LH]-C7A[LH]',key),'Unexpected completed key')
        job=base/'jobs'/key
        if not job.exists():continue
        if row['status']!='ok':continue
        below(job,base)
        check(not (job/'pending.json').exists() and {p.name for p in job.iterdir()}==set(FILES),
              'Only exactly completed regular job files may be compacted')
        check(confirmed_cleanup(job/'native.stdout',expected_limit=3),'Kernel cleanup unconfirmed')
        for name,field in (('input.json','input_dump_sha256'),('native.jsonl','raw_log_sha256'),
                           ('native.stdout','stdout_sha256'),('native.containment.json','containment_receipt_sha256')):
            check(digest(below(job/name,base))==row[field],'Original ledger/evidence hash mismatch')
        files=[job/name for name in FILES]+[base/'dispatch'/(key+suffix) for suffix in ('.started.json','.admitted.json')]
        for path in files:below(path,base);check(path.is_file(),'Missing regular original')
        candidates.append((key,files))
        if len(candidates)==limit:break
    if not candidates:return 0
    count=len(list(directory.glob('batch-*.json')))
    target=directory/f'batch-{count:04d}.zip';journal=directory/f'batch-{count:04d}.json'
    entries={str(p.relative_to(base)).replace('\\','/'):digest(p) for _,files in candidates for p in files}
    with ZipFile(target,'x',compression=ZIP_DEFLATED,compresslevel=1) as archive_file:
        for relative in entries:archive_file.write(base/relative,arcname=relative)
    with ZipFile(target) as archive_file:
        check(archive_file.testzip() is None and set(archive_file.namelist())==set(entries),'Archive CRC/coverage mismatch')
        for relative,wanted in entries.items():
            check(sha256(archive_file.read(relative)).hexdigest()==wanted,'Archive byte hash mismatch')
    proof=dict(schema='night002.lossless-completed-evidence.v1',jobs=[key for key,_ in candidates],
        archive_sha256=digest(target),entries=entries,original_bytes=sum((base/n).stat().st_size for n in entries),
        archive_bytes=target.stat().st_size,ledger_native_calls_retained=True,source_and_budget_changed=False)
    with journal.open('x',encoding='utf8',newline='\n') as stream:json.dump(proof,stream,indent=2);stream.write('\n')
    # Only exact independently hashed files are unlinked. No recursive delete.
    for relative,wanted in entries.items():
        path=below(base/relative,base);check(digest(path)==wanted,'Original changed after archive verification');path.unlink()
    for key,_ in candidates:below(base/'jobs'/key,base).rmdir()
    return len(candidates)


def restore(base):
    base=Path(base).resolve();restored=0
    for journal in sorted((base/'completed-archives').glob('batch-*.json')):
        proof=json.loads(journal.read_text());target=journal.with_suffix('.zip')
        check(digest(target)==proof['archive_sha256'],'Retained archive hash changed')
        with ZipFile(target) as archive_file:
            check(archive_file.testzip() is None and set(archive_file.namelist())==set(proof['entries']),
                  'Restore archive CRC/coverage mismatch')
            for relative,wanted in proof['entries'].items():
                check(not Path(relative).is_absolute() and '..' not in Path(relative).parts and
                      relative.startswith(('jobs/','dispatch/')),'Unsafe restore member')
                path=base/relative;check(path.resolve().is_relative_to(base),'Restore path escaped')
                content=archive_file.read(relative);check(sha256(content).hexdigest()==wanted,'Restore bytes differ')
                if path.exists():check(digest(below(path,base))==wanted,'Existing original differs')
                else:
                    path.parent.mkdir(parents=True,exist_ok=True)
                    with path.open('xb') as stream:stream.write(content)
                    check(digest(below(path,base))==wanted,'Restored original hash differs')
                restored+=1
    return restored


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('action',choices=('archive','restore'))
    parser.add_argument('--limit',type=int,default=32);args=parser.parse_args()
    base=ROOT/'local/night-002/split004/main'
    if args.action=='restore':
        state=json.loads((ROOT/'local/night-002/program-budget.json').read_text())
        check(state['active'] is None,'Do not restore while native phase is active')
        print('Byte-verified original files restored:',restore(base))
    else:
        check(1<=args.limit<=128,'Bounded archive batch required')
        print('Completed jobs losslessly compacted:',archive(base,args.limit))

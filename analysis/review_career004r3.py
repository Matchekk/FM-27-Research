"""Independent R3 source/retained-JSON review; never opens a save or imports fmsave."""
from argparse import ArgumentParser
import ast
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]


def need(ok,message):
    if not ok:raise ValueError(message)


def read(path):return json.loads(Path(path).read_text(encoding='utf8'))


def file_hash(path,lf=False):
    raw=Path(path).read_bytes()
    return sha256(raw.replace(b'\r\n',b'\n') if lf else raw).hexdigest()


def tree(path):return ast.parse(Path(path).read_text(encoding='utf8'))


def function(path,name):
    return next(n for n in tree(path).body if isinstance(n,ast.FunctionDef) and n.name==name)


def ast_hash(node):return sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()


def prefix(node):
    for i,statement in enumerate(node.body):
        if isinstance(statement,ast.For) and isinstance(statement.iter,ast.Attribute) and statement.iter.attr=='taker_markers':
            return ast.Module(body=node.body[:i+1],type_ignores=[])
    raise ValueError('Original marker loop absent')


def layout(path):
    return next(n.value for n in tree(path).body if isinstance(n,ast.Assign) and
                any(isinstance(t,ast.Name) and t.id=='TACTICS' for t in n.targets))


def markers(package):
    package=Path(package);base=layout(package/'_layouts/fm26_26_3_2.py')
    later=layout(package/'_layouts/fm27_27_0_0.py')
    need(isinstance(later,ast.Call) and isinstance(later.func,ast.Name) and later.func.id=='replace' and
         len(later.args)==1 and isinstance(later.args[0],ast.Name) and later.args[0].id=='FM26_TACTICS',
         'FM27 layout ancestry changed')
    need(not any(k.arg=='taker_markers' for k in later.keywords),'FM27 marker override appeared')
    values=next(k.value for k in base.keywords if k.arg=='taker_markers')
    result=[]
    for value in values.elts:
        if isinstance(value,ast.Constant) and type(value.value) is bytes:result.append(value.value)
        else:
            need(isinstance(value,ast.Call) and isinstance(value.func,ast.Attribute) and
                 isinstance(value.func.value,ast.Name) and value.func.value.id=='bytes' and
                 value.func.attr=='fromhex' and len(value.args)==1 and not value.keywords,
                 'Nonliteral marker declaration')
            result.append(bytes.fromhex(ast.literal_eval(value.args[0])))
    return tuple(result)


def independent_inventory(package):
    fields={}
    for path,names in [('models/training.py',('TrainingDay','TrainingWeek','TrainingSchedule','TeamTraining','MentoringGroup')),
                       ('models/players.py',('Player',)),
                       ('models/staff.py',('Staff','StaffList','StaffAttributes','StaffPreferences'))]:
        classes={n.name:n for n in tree(Path(package)/path).body if isinstance(n,ast.ClassDef)}
        for name in names:
            fields[name]=[n.target.id for n in classes[name].body if isinstance(n,ast.AnnAssign) and
                          isinstance(n.target,ast.Name) and not n.target.id.isupper()]
    save=next(n for n in tree(Path(package)/'_save.py').body if isinstance(n,ast.ClassDef) and n.name=='Save')
    methods=[n.name for n in save.body if isinstance(n,ast.FunctionDef) and not n.name.startswith('_')]
    return fields,methods


def audit_sources(root,central):
    root,central=Path(root),Path(central)
    draft=read(root/'data/night-001-career-r3/R3-draft-contract.json')
    report=read(root/'data/night-001-career-r3/source-audit.json')
    official=central/'local/night-001-career/reader0124/site/fmsave'
    vendor=central/'local/runtime-v1114.6/source/vendor/fmsave'
    manifests={p:read(root/f'data/night-001-career-r1/{p}-contract.json') for p in ('R1','R2')}
    for profile,package in [('R1',vendor),('R2',official)]:
        actual={p.relative_to(package).as_posix():file_hash(p) for p in package.rglob('*.py')}
        need(actual==manifests[profile]['reader']['source_sha256'],'Frozen package source drift')
    need(draft['reader']['source_sha256']==manifests['R2']['reader']['source_sha256'],'R3/R2 source declarations differ')
    need(draft.get('own_source_hash_normalization')==
         'CRLF_to_LF; package and private evidence hashes remain raw','Own-source hash policy not explicit')
    for name,reported in report['functions'].items():
        left=function(vendor/'readers/tactics.py',name);right=function(official/'readers/tactics.py',name)
        need(ast_hash(left)==reported['vendor_ast_sha256'] and ast_hash(right)==reported['official_ast_sha256'],
             'Function AST report differs')
        need((ast_hash(left)==ast_hash(right)) is reported['identical_ast'],'Function equality differs')
    need(ast_hash(prefix(function(vendor/'readers/tactics.py','_read_selection_part')))==
         ast_hash(prefix(function(official/'readers/tactics.py','_read_selection_part'))), 'Marker prefixes differ')
    declared=markers(official)
    need(declared==markers(vendor) and [len(m) for m in declared]==[3,3,3],'Marker declaration mismatch')
    fields,methods=independent_inventory(official)
    need(fields==report['official_model_fields'] and methods==report['official_public_save_methods'],'Typed API inventory differs')
    need(not any('focus' in n or 'intensity' in n or 'attendance' in n for n in fields['Player']),
         'Additional player training fields require review')
    need(set(fields['TrainingDay'])=={'day','sessions'},'Day model interpretation changed')
    need('training' in methods and 'mentoring' in methods and not any('rng' in n or 'attendance' in n for n in methods),
         'Public API gap interpretation changed')
    own=[]
    for name,wanted in draft['code_sha256'].items():
        need(file_hash(root/name,True)==wanted,'LF-normalized draft own-source mismatch')
        own.append(dict(path=name,lf_sha256=wanted,raw_matches_draft=file_hash(root/name)==wanted))
    need(file_hash(root/draft['document'],True)==draft['document_sha256'],'LF-normalized draft document mismatch')
    plan=read(root/'data/night-001-career-r3/planned-ledger.json')
    need(len(plan['stages'])==5 and all(x['status']=='not_started' for x in plan['stages']) and
         plan['reader_processes_started']==0 and not plan['tactics_released'],'Offline ledger release drift')
    return dict(source_inventory_verified=True,official_python_files=len(draft['reader']['source_sha256']),
                marker_widths=[len(m) for m in declared],typed_model_classes=len(fields),
                public_save_methods=len(methods),own_source_lf_bindings=own,
                execution_supervisor_implemented=False,reader_execution_released=False)


def audit_retained(root,central):
    root,central=Path(root),Path(central);result={}
    for profile in ('R1','R2'):
        path=root/f'data/night-001-career-r1/{profile}/coverage.json';public=read(path)
        folder=central/f'local/night-001-career/readonly-{profile.lower()}'
        events=[json.loads(line) for line in (folder/'events.jsonl').read_text(encoding='utf8').splitlines()]
        latest={e['probe']:e for e in events}
        for row in public['probes']:
            old=latest.get(row['probe'])
            if old is None:need(row==dict(probe=row['probe'],status='not_started'),'Unbegun row changed')
            else:
                expected={k:old[k] for k in ('probe','status','coverage','checks','borrowed_layout','warning_types','warning_count','error_type') if k in old}
                if expected['status']=='started':expected['status']='started_unresolved'
                need(expected==row,'Independent private/public row reconstruction differs')
        counts=dict(Counter(p['status'] for p in public['probes']))
        need(sum(counts.values())==12 and counts['failed']==1,'Probe accounting differs')
        result[profile]=dict(statuses=counts,private_events_sha256=file_hash(folder/'events.jsonl'),
                             public_lf_sha256=file_hash(path,True))
        if profile=='R2':
            teams=next(x for x in latest.values() if x['probe']=='training')['coverage']['teams']
            total=dict(teams=len(teams),weeks=sum(x['weeks'] for x in teams),days=sum(x['days'] for x in teams),
                       stored_slots=sum(sum(x['raw_session_counts'].values()) for x in teams))
            need(total==dict(teams=4,weeks=155,days=1085,stored_slots=3255),'Training ledger aggregate differs')
            result['saved_training']=total
    return result


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--central',type=Path,required=True)
    parser.add_argument('--verify-private-json',action='store_true');args=parser.parse_args()
    output=dict(sources=audit_sources(ROOT,args.central),save_opened_or_hashed=False,decoder_started=False,native_started=False)
    if args.verify_private_json:output['retained']=audit_retained(ROOT,args.central)
    print(json.dumps(output,indent=2))

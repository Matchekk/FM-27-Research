"""Offline source audit and passive final-exception diagnostics; no save opener."""
import ast
from hashlib import sha256
from pathlib import Path

VERSION='career-marker-diagnostic-draft-v1'
TARGET_MESSAGE="a block's set-piece marker is not where fmsave expects it"
STAGES=('published_source_and_release_gates','snapshot_before','open',
        'tactics_final_call','close_and_snapshot_after')
MAX_TRACEBACK_FRAMES=64
MAX_MARKERS=4
MAX_MARKER_BYTES=16


def require(ok,message):
    if not ok:raise ValueError(message)


def source_hash(path, normalized=False):
    path=Path(path)
    require(path.suffix in ('.py','.md','.json','.jsonl'),'Only source and retained JSON may be inspected')
    raw=path.read_bytes()
    return sha256(raw.replace(b'\r\n',b'\n') if normalized else raw).hexdigest()


def _tree(path):return ast.parse(Path(path).read_text(encoding='utf8'))


def _function(path,name):
    return next(n for n in _tree(path).body if isinstance(n,ast.FunctionDef) and n.name==name)


def _fingerprint(node):return sha256(ast.dump(node,include_attributes=False).encode()).hexdigest()


def _marker_prefix(node):
    result=[]
    for statement in node.body:
        result.append(statement)
        if isinstance(statement,ast.For) and isinstance(statement.iter,ast.Attribute) and statement.iter.attr=='taker_markers':
            return ast.Module(body=result,type_ignores=[])
    raise ValueError('Expected marker grammar not found')


def _assignment(path,name):
    return next(n.value for n in _tree(path).body if isinstance(n,ast.Assign) and
                any(isinstance(t,ast.Name) and t.id==name for t in n.targets))


def _keyword(call,name):return next(k.value for k in call.keywords if k.arg==name)


def _literal_bytes(node):
    if isinstance(node,ast.Constant) and isinstance(node.value,bytes):return node.value
    require(isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and
            isinstance(node.func.value,ast.Name) and node.func.value.id=='bytes' and
            node.func.attr=='fromhex' and len(node.args)==1 and not node.keywords,
            'Only literal layout byte declarations are supported')
    return bytes.fromhex(ast.literal_eval(node.args[0]))


def declared_markers(package):
    """Read the literal FM26 base used by the FM27 replace declaration; never execute it."""
    package=Path(package)
    base=_assignment(package/'_layouts/fm26_26_3_2.py','TACTICS')
    later=_assignment(package/'_layouts/fm27_27_0_0.py','TACTICS')
    require(isinstance(later,ast.Call) and isinstance(later.func,ast.Name) and
            later.func.id=='replace' and isinstance(later.args[0],ast.Name) and
            later.args[0].id=='FM26_TACTICS','Unrecognized FM27 layout inheritance')
    require(not any(k.arg=='taker_markers' for k in later.keywords),'FM27 overrides marker declaration')
    return tuple(_literal_bytes(n) for n in _keyword(base,'taker_markers').elts)


def model_fields(package,relative,classes):
    tree=_tree(Path(package)/relative);result={}
    for name in classes:
        node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==name)
        result[name]=[n.target.id for n in node.body if isinstance(n,ast.AnnAssign) and
                      isinstance(n.target,ast.Name) and not n.target.id.isupper()]
    return result


def source_audit(vendor,official,compat):
    vendor,official=Path(vendor),Path(official)
    functions={}
    for name in ('_read_selection_part','_read_selector_list','_read_text','_block_starts','_stored_block_starts'):
        a=_function(vendor/'readers/tactics.py',name);b=_function(official/'readers/tactics.py',name)
        functions[name]=dict(vendor_ast_sha256=_fingerprint(a),official_ast_sha256=_fingerprint(b),
                             identical_ast=_fingerprint(a)==_fingerprint(b))
    a=_marker_prefix(_function(vendor/'readers/tactics.py','_read_selection_part'))
    b=_marker_prefix(_function(official/'readers/tactics.py','_read_selection_part'))
    markers=declared_markers(official)
    fields={}
    for relative,classes in (
        ('models/training.py',('TrainingDay','TrainingWeek','TrainingSchedule','TeamTraining','MentoringGroup')),
        ('models/players.py',('Player',)),
        ('models/staff.py',('Staff','StaffList','StaffAttributes','StaffPreferences'))):
        fields.update(model_fields(official,relative,classes))
    save=next(n for n in _tree(official/'_save.py').body if isinstance(n,ast.ClassDef) and n.name=='Save')
    methods=[n.name for n in save.body if isinstance(n,ast.FunctionDef) and not n.name.startswith('_')]
    return dict(schema='valid004.r3.source-audit.v1',functions=functions,
        selection_prefix_through_marker_identical_ast=_fingerprint(a)==_fingerprint(b),
        inherited_marker_declarations_equal=declared_markers(vendor)==markers,
        marker_widths=[len(x) for x in markers],
        v10_compat_mentions_taker_markers='taker_markers' in Path(compat).read_text(encoding='utf8'),
        official_model_fields=fields,official_public_save_methods=methods,
        interpretation='source declarations and retained parser claims only',
        native_semantics_verified=False)


def marker_evidence(error,target_code):
    """Inspect only the propagated error's exact parser frame; no scans or new parsing."""
    if type(error).__name__!='ReaderCheckError' or TARGET_MESSAGE not in str(error):
        return dict(status='non_target_error',target_frame_observed=False)
    tb=error.__traceback__;frames=[];count=0
    while tb is not None:
        count+=1;require(count<=MAX_TRACEBACK_FRAMES,'Traceback exceeds diagnostic bound')
        if tb.tb_frame.f_code is target_code:frames.append(tb.tb_frame)
        tb=tb.tb_next
    require(len(frames)==1,'Target frame absent or ambiguous')
    values=frames[0].f_locals
    section=values['section'];layout=values['layout']
    start,end,cursor=(values[n] for n in ('block_start','block_end','cursor'))
    require(type(section) is bytes and all(type(n) is int for n in (start,end,cursor)),
            'Unexpected parser frame types')
    require(0<=start<=cursor<=end<=len(section),'Invalid parser bounds')
    markers=layout.taker_markers
    require(type(markers) is tuple and 1<=len(markers)<=MAX_MARKERS and
            all(type(m) is bytes and 1<=len(m)<=MAX_MARKER_BYTES for m in markers),
            'Unexpected marker shape')
    checks=[]
    for i,expected in enumerate(markers):
        complete=cursor+len(expected)<=end
        checks.append(dict(marker_index=i,expected_width_bytes=len(expected),
                           fully_inside_block=complete,
                           equals_expected_at_cursor=section[cursor:cursor+len(expected)]==expected))
    return dict(status='captured_final_target_failure',target_frame_observed=True,
        section_bytes=len(section),block_start=start,block_end=end,cursor=cursor,
        cursor_relative_to_block=cursor-start,bytes_remaining_in_block=end-cursor,
        marker_checks=checks,
        failure_consistent_with_expected_marker_tests=not any(x['equals_expected_at_cursor'] for x in checks),
        raw_values_captured=False,scan_performed=False,grammar_changed=False)


def observe_final_call(operation,selection_reader,receipt,*args,**kwargs):
    """Transparent outer call boundary: retain the identical return value or exception.

    This does not replace any fmsave function. The caller owns the private receipt;
    it must not publish it. Upstream's internally caught candidate errors stay internal.
    """
    require(type(receipt) is dict and not receipt,'Fresh private receipt required')
    try:
        result=operation(*args,**kwargs)
    except Exception as original:
        try:receipt.update(marker_evidence(original,selection_reader.__code__))
        except Exception as observer_error:
            receipt.update(status='observer_rejected_frame',observer_error_type=type(observer_error).__name__)
        raise
    else:
        receipt.update(status='no_final_exception',target_frame_observed=False)
        return result


def full_ledger(events=()):
    by_stage={}
    for event in events:
        require(event['stage'] in STAGES and event['stage'] not in by_stage,'Unknown or duplicate stage')
        require(event['status'] in ('started','observed','failed','blocked'),'Unknown stage status')
        row={k:event[k] for k in ('stage','status','error_type') if k in event}
        if row['status']=='started':row['status']='started_unresolved'
        by_stage[row['stage']]=row
    return dict(version=VERSION,execution_status='retained_stage_events_resources_missing' if by_stage else 'offline_preparation_no_reader_execution',
        stages=[by_stage.get(s,dict(stage=s,status='not_started')) for s in STAGES],
        native_starts=0,calendar_advances=0,seeds_reserved=0,reader_processes_started=None if by_stage else 0,
        native_semantics_verified=False,tactics_released=False,replay_released=False,
        training_effect_released=False,career_advance_released=False)

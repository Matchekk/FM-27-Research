"""Offline, fail-closed accounting proof for the seventeen startpolicy probes."""
from datetime import datetime, timedelta
import math

from analysis.startpolicy002_gate import EXPERIMENT, technical_keys

RECONCILIATION = 'fm27.startpolicy002.reconciled.v1'


def number(value):
    try:
        return type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        return False


def utc(value):
    if type(value) is not str:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() == timedelta(0) else None


def _time(value):
    parsed = utc(value)
    return parsed.isoformat() if parsed else None


def _safe_operation(value):
    if type(value) is not dict:
        return dict(operation_record_malformed=True)
    keys = value.get('keys')
    known = technical_keys()
    return dict(name='technical' if value.get('name') == 'technical' else None,
        kind='technical' if value.get('kind') == 'technical' else None,
        keys=[k for k in keys if type(k) is str and k in known] if type(keys) is list else None,
        unrecognized_key_count=sum(type(k) is not str or k not in known for k in keys) if type(keys) is list else None,
        start_utc=_time(value.get('start_utc')), child_deadline_utc=_time(value.get('child_deadline_utc')),
        elapsed_seconds=value.get('elapsed_seconds') if number(value.get('elapsed_seconds')) else None,
        returncode=value.get('returncode') if type(value.get('returncode')) is int else None,
        timed_out=value.get('timed_out') if type(value.get('timed_out')) is bool else None)


def budget_evidence(budget, reconciliation, budget_sha256, unresolved):
    """A failed/missing operation is never success or an elapsed-time zero.

    Return an independent gate plus a redacted public receipt. Unknown fields,
    tokens, supervisor environment and private path strings are never copied.
    """
    reasons = []
    def check(condition, reason):
        if not condition:
            reasons.append(reason)
    valid = type(budget) is dict
    b = budget if valid else {}
    keys = technical_keys(); limits = b.get('limits'); reserved = b.get('reserved'); operations = b.get('operations')
    check(valid, 'missing_or_malformed_budget')
    check(b.get('experiment') == EXPERIMENT, 'budget_identity')
    check(type(limits) is dict and limits == {'technical':17,'main':0} and
          all(type(v) is int for v in limits.values()), 'attempt_caps')
    check(type(b.get('limit_seconds')) is int and b['limit_seconds'] == 180 and
          type(b.get('wall_limit_seconds')) is int and b['wall_limit_seconds'] == 900, 'time_caps')
    check('active' in b and b['active'] is None, 'active_or_unreconciled_operation')
    check(b.get('halted') is False, 'budget_halted_or_unknown')
    check(not unresolved and not b.get('cleanup_unconfirmed') and not b.get('global_native_lease_retained'), 'cleanup_unconfirmed')
    check(type(reserved) is dict and set(reserved) == set(keys) and
          all(v == 'technical' for v in reserved.values()), 'reservation_refund_retry_or_mismatch')
    single = type(operations) is list and len(operations) == 1 and type(operations[0]) is dict
    check(single, 'missing_duplicate_or_unaccounted_operation')
    op = operations[0] if single else {}
    check(op.get('name') == op.get('kind') == 'technical' and op.get('keys') == keys, 'operation_identity_keys')
    check(type(op.get('returncode')) is int and op['returncode'] == 0 and op.get('timed_out') is False,
          'operation_failed_or_timed_out')
    elapsed = op.get('elapsed_seconds'); charged = b.get('charged_seconds')
    charges = number(elapsed) and elapsed > 0 and number(charged) and charged > 0 and charged == elapsed
    check(charges, 'missing_or_unreconciled_time_charge')
    check(charges and elapsed <= 180 and charged <= 180, 'actual_child_time_exceeded_or_unknown')
    start = utc(b.get('wall_start_utc')); end = utc(b.get('wall_deadline_utc'))
    op_start = utc(op.get('start_utc')); child_end = utc(op.get('child_deadline_utc'))
    times = all(v is not None for v in (start,end,op_start,child_end))
    check(times and end-start == timedelta(seconds=900), 'fixed_utc_window_missing_or_changed')
    check(times and start <= op_start < child_end <= end and (child_end-op_start).total_seconds() <= 180,
          'operation_deadline_outside_caps')
    receipt = reconciliation if type(reconciliation) is dict else {}
    completed = utc(receipt.get('completed_utc'))
    check(receipt.get('schema') == RECONCILIATION and receipt.get('experiment_id') == EXPERIMENT and
          receipt.get('phase') == 'technical' and receipt.get('budget_sha256') == budget_sha256 and
          type(budget_sha256) is str and len(budget_sha256) == 64, 'missing_or_mismatched_final_reconciliation')
    check(times and number(elapsed) and 0 < elapsed <= 180 and completed is not None and
          (completed-op_start).total_seconds() >= elapsed and completed <= end,
          'actual_finish_outside_utc_window_or_unknown')
    accounting_complete = bool(single and charges and times and 'active' in b and b['active'] is None)
    result = dict(passed=not reasons, reasons=reasons, accounting_reconciled=accounting_complete,
                  final_reconciliation_present=bool(receipt), attempt_limit=17, child_limit_seconds=180, wall_limit_seconds=900)
    public = dict(experiment=EXPERIMENT,
        limits={k:limits.get(k) if type(limits.get(k)) is int else None for k in ('technical','main')} if type(limits) is dict else None,
        limit_seconds=b.get('limit_seconds') if type(b.get('limit_seconds')) is int else None,
        charged_seconds=charged if accounting_complete else None,
        recorded_charged_seconds=charged if number(charged) else None,
        reserved={k:reserved[k] if reserved[k] == 'technical' else None for k in keys if k in reserved} if type(reserved) is dict else None,
        unrecognized_reserved_key_count=len(set(reserved)-set(keys)) if type(reserved) is dict else None,
        halted=b.get('halted') if type(b.get('halted')) is bool else None,
        wall_start_utc=_time(b.get('wall_start_utc')), wall_deadline_utc=_time(b.get('wall_deadline_utc')),
        wall_limit_seconds=b.get('wall_limit_seconds') if type(b.get('wall_limit_seconds')) is int else None,
        active=_safe_operation(b['active']) if b.get('active') is not None else None,
        operations=[_safe_operation(o) for o in operations] if type(operations) is list else None,
        completed_utc=completed.isoformat() if completed else None,
        private_budget_sha256=budget_sha256,
        actual_study_window_seconds=(completed-start).total_seconds() if completed and start else None,
        cleanup_unconfirmed=bool(unresolved or b.get('cleanup_unconfirmed')),
        global_native_lease_retained=True if unresolved or b.get('global_native_lease_retained') else False if not reasons else None,
        charged_seconds_incomplete=not accounting_complete, acceptance=result)
    return result, public

"""SET-V0 offline contract parser. No native event mapping is validated.

Only own, explicitly synthetic contract traces are parsed. Neither caller flags
nor a familiar raw event name can enable native performance measurements.
"""
from copy import deepcopy
from hashlib import sha256
import json
from math import isfinite
import re

SCHEMA = "SET-V0-synthetic-v1"
TYPES = ("corner", "free_kick", "throw_in")
COUNTER_MS = 10000
_ID = re.compile(r"[A-Za-z0-9_-]{1,80}\Z")
_FIELDS = {
    "award": {"award_id", "setpiece_type", "side"},
    "select": {"award_id", "view_side", "routine_sha256"},
    "execute": {"award_id", "execution_id", "contact_verified", "legal", "repeat_of", "reason"},
    "abort": {"award_id", "reason"},
    "possession": {"side", "controlled"},
    "shot": {"shot_id", "side", "xg", "counted_in_final_xg"},
    "goal": {"goal_id", "side", "shot_id", "own_goal"},
    "cancel_goal": {"goal_id", "reason"},
    "stoppage": set(), "period_end": set(), "match_end": set(),
}


class TraceError(ValueError):
    """A contract trace is incomplete, ambiguous or internally inconsistent."""


def _require(value, message):
    if not value:
        raise TraceError(message)


def _identity(value):
    _require(type(value) is str and _ID.fullmatch(value), "Invalid pseudonymous ID")
    return value


def _side(value):
    _require(type(value) is int and value in (0, 1), "Invalid side")
    return value


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def capability_manifest():
    """Actual implementation capabilities, not caller-provided validation flags."""
    required = ["execution_contact", "final_legality", "clock_mapping", "shot_xg", "final_shot_xg_status", "controlled_possession", "final_goal_status"]
    return dict(schema_version=1, adapter="SET-V0-offline-v1", synthetic_schema=SCHEMA,
        synthetic_parser_implemented=True, native_mapping_implemented=False,
        native_validated=False, performance_ready=False,
        native_capabilities={name: False for name in required},
        native_source_mapping_sha256=None, native_schema_sha256=None,
        native_clock_mapping_sha256=None, native_gate_sha256=None,
        required_native_evidence="Versioned source/schema/clock mapping plus independently validated native gold cases; absent in V0")


def inspect_native_rows(records):
    """Diagnostic counts only. Selection messages never become exposures."""
    _require(type(records) is list and all(type(r) is dict for r in records), "Expected raw record list")
    selected = [r for r in records if r.get("event") == "native_setpiece_selected"]
    return dict(status="unresolved_native_mapping", native_validated=False, performance_ready=False,
        exposures=None, attribution=None, missing_capabilities=list(capability_manifest()["native_capabilities"]),
        diagnostics=dict(raw_records=len(records), selection_messages=len(selected),
            selection_ticks=len({r["tick"] for r in selected if type(r.get("tick")) is int}),
            invalid_selection_ticks=sum(type(r.get("tick")) is not int for r in selected),
            selection_is_execution=False),
        reason="No trusted native execution/clock/shot/possession adapter or gate exists")


def parse_trace(trace):
    """Parse a complete synthetic trace; native-looking inputs stay unresolved.

    Normalized event time is integer milliseconds within each period. The
    counter window is [turnover, turnover+10000ms); a shot at exactly 10s is out.
    Goal attribution follows the shot snapshot, even if its final register/VAR
    decision arrives after the chain closes. Native source mapping is absent.
    """
    _require(type(trace) is dict, "Expected trace object")
    if trace.get("origin") != "synthetic":
        records = trace.get("events", [])
        return inspect_native_rows(records)
    _require(set(trace) == {"schema", "origin", "match_id", "clock", "final_score", "events"}, "Unknown/missing trace field")
    _require(trace["schema"] == SCHEMA and trace["clock"] == "synthetic_period_milliseconds", "Unvalidated schema/clock")
    _identity(trace["match_id"])
    score = trace["final_score"]
    _require(type(score) is list and len(score) == 2 and all(type(v) is int and v >= 0 for v in score), "Invalid final score")
    events = trace["events"]
    _require(type(events) is list and events, "Complete event stream required")
    awards, executions, shots, goals = {}, {}, {}, {}
    active = None
    ids = set()
    period, last_ms, ended_period, ended_match = 1, -1, False, False
    selection_count = 0

    def pending(award_id):
        _identity(award_id)
        _require(award_id in awards and awards[award_id]["status"] == "pending", "Award absent or already closed")
        return awards[award_id]

    def snapshot():
        return deepcopy(active)

    for index, e in enumerate(events):
        _require(type(e) is dict and type(e.get("type")) is str and e["type"] in _FIELDS, "Unknown event kind")
        kind = e["type"]
        _require(set(e) == {"id", "type", "period", "ms"} | _FIELDS[kind], "Unknown/missing event field")
        _identity(e["id"])
        _require(e["id"] not in ids and not ended_match, "Duplicate event ID or event after match end")
        ids.add(e["id"])
        _require(type(e["period"]) is int and 1 <= e["period"] <= 4 and type(e["ms"]) is int and e["ms"] >= 0, "Invalid period clock")
        if e["period"] != period:
            _require(ended_period and e["period"] == period + 1, "Unannounced period transition")
            period, last_ms, ended_period = e["period"], -1, False
        _require(not ended_period and e["ms"] >= last_ms, "Clock regressed or period already ended")
        last_ms = e["ms"]
        if active and active["phase"] == "counter" and e["ms"] - active["start_ms"] >= COUNTER_MS:
            active = None
        if kind == "award":
            aid = _identity(e["award_id"])
            _require(aid not in awards and not any(a["status"] == "pending" for a in awards.values()), "Duplicate or unresolved previous award")
            _require(e["setpiece_type"] in TYPES, "Unknown standard type")
            awards[aid] = dict(type=e["setpiece_type"], side=_side(e["side"]), status="pending")
            active = None
        elif kind == "select":
            pending(e["award_id"]); _side(e["view_side"])
            _require(type(e["routine_sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", e["routine_sha256"]), "Invalid routine hash")
            selection_count += 1  # both views and repeated sampling remain diagnostics
        elif kind == "abort":
            a = pending(e["award_id"])
            _require(e["reason"] in ("cancelled", "period_end", "superseded"), "Unknown abort reason")
            a["status"] = "aborted"
        elif kind == "execute":
            a = pending(e["award_id"]); xid = _identity(e["execution_id"])
            _require(xid not in executions and e["contact_verified"] is True and type(e["legal"]) is bool, "Execution lacks unique contact/legal proof")
            repeat = e["repeat_of"]
            if repeat is not None:
                _identity(repeat)
                _require(repeat in executions and executions[repeat]["award_id"] == e["award_id"] and not executions[repeat]["legal"], "Invalid repeat reference")
            _require(e["reason"] == ("legal" if e["legal"] else "repeat"), "Unresolved final legality")
            executions[xid] = dict(award_id=e["award_id"], type=a["type"], side=a["side"], legal=e["legal"])
            if e["legal"]:
                a["status"] = "executed"
                active = dict(execution_id=xid, origin_side=a["side"], owner_side=a["side"], phase="attack", start_ms=e["ms"])
        elif kind == "possession":
            side = _side(e["side"])
            _require(type(e["controlled"]) is bool, "Possession control state missing")
            if active and e["controlled"] and side != active["owner_side"]:
                if active["phase"] == "attack":
                    active.update(owner_side=side, phase="counter", start_ms=e["ms"])
                else:
                    active = None
        elif kind == "shot":
            sid = _identity(e["shot_id"]); side = _side(e["side"])
            _require(sid not in shots and type(e["xg"]) in (int, float) and 0 <= e["xg"] <= 1 and isfinite(e["xg"]), "Invalid shot/xG")
            _require(type(e["counted_in_final_xg"]) is bool, "Final shot-xG inclusion status missing")
            _require(active is None or side == active["owner_side"], "Shot side contradicts controlled possession")
            shots[sid] = dict(side=side, xg=float(e["xg"]), counted=e["counted_in_final_xg"], context=snapshot())
        elif kind == "goal":
            gid = _identity(e["goal_id"]); side = _side(e["side"])
            _require(gid not in goals and type(e["own_goal"]) is bool, "Duplicate/invalid goal")
            sid = e["shot_id"]
            if sid is not None:
                _identity(sid)
                _require(sid in shots and shots[sid]["side"] == side and not any(g["shot_id"] == sid for g in goals.values()), "Missing/contradictory/duplicate goal shot")
                context = deepcopy(shots[sid]["context"])
            else:
                _require(e["own_goal"], "Non-own goal requires shot provenance")
                context = snapshot()
            goals[gid] = dict(side=side, shot_id=sid, context=context, cancelled=False)
        elif kind == "cancel_goal":
            _identity(e["goal_id"])
            _require(e["goal_id"] in goals and not goals[e["goal_id"]]["cancelled"] and e["reason"] in ("VAR", "offside"), "Unknown/already cancelled goal")
            goals[e["goal_id"]]["cancelled"] = True
        elif kind in ("stoppage", "period_end", "match_end"):
            active = None
            if kind in ("period_end", "match_end"):
                _require(not any(a["status"] == "pending" for a in awards.values()), "Award has no final execution/abort status")
            ended_period = kind == "period_end"
            if kind == "match_end":
                _require(index == len(events) - 1, "Match end is not final")
                ended_match = True
    _require(ended_match, "Match end missing")
    actual = [sum(g["side"] == s and not g["cancelled"] for g in goals.values()) for s in (0, 1)]
    _require(actual == score, "Final goal register disagrees with score")
    legal = {x: v for x, v in executions.items() if v["legal"]}
    fields = ("executed", "xg_for", "xg_against", "counter_xg_against", "goals_for", "goals_against", "counter_goals_against")
    totals = {kind: {str(side): dict.fromkeys(fields, 0) for side in (0, 1)} for kind in TYPES}
    for e in legal.values():
        totals[e["type"]][str(e["side"])]["executed"] += 1
    for shot in shots.values():
        ctx = shot["context"]
        if ctx and shot["counted"]:
            e = legal[ctx["execution_id"]]; row = totals[e["type"]][str(e["side"])]
            own = shot["side"] == e["side"]
            row["xg_for" if own else "xg_against"] += shot["xg"]
            if not own and ctx["phase"] == "counter": row["counter_xg_against"] += shot["xg"]
    for goal in goals.values():
        ctx = goal["context"]
        if ctx and not goal["cancelled"]:
            e = legal[ctx["execution_id"]]; row = totals[e["type"]][str(e["side"])]
            own = goal["side"] == e["side"]
            row["goals_for" if own else "goals_against"] += 1
            if not own and ctx["phase"] == "counter": row["counter_goals_against"] += 1
    for kind, sides in totals.items():
        for s, row in sides.items():
            other = sides[str(1 - int(s))]
            row.update(defended=other["executed"], defensive_goals_conceded=other["goals_for"], defensive_xga=other["xg_for"], net_xg=row["xg_for"] - row["xg_against"])
    return dict(status="synthetic_contract_verified", origin="synthetic", native_validated=False, performance_ready=False,
        trace_sha256=sha256(_canonical(trace)).hexdigest(), events=len(events), selection_messages=selection_count,
        attempts=len(executions), illegal_attempts=len(executions)-len(legal), aborted_awards=sum(a["status"] == "aborted" for a in awards.values()),
        by_type=totals, final_score=actual, excluded_xg_shots=sum(not s["counted"] for s in shots.values()), cancelled_goals=sum(g["cancelled"] for g in goals.values()),
        attribution={"shots": {sid: shot["context"] for sid, shot in shots.items()}, "goals": {gid: goal["context"] for gid, goal in goals.items()}},
        warning="Own synthetic gold data only; no native execution/exposure/attribution source is validated")

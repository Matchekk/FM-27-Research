"""TRAIN-002 read-only normalized checkpoint diagnostics. No save decoder/executor.

Hash receipts establish byte identity, not the meaning of an extracted field.
There is deliberately no API which can release career execution in this module.
"""
from collections import Counter, defaultdict
from datetime import date
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

SHA = re.compile(r"[0-9a-f]{64}\Z")
CODE = re.compile(r"[A-Za-z0-9_-]{1,48}\Z")
INDEX = ("acceleration", "pace", "agility", "stamina")
GATES = ("current_build_reader_mapping", "raw_display_calibration",
         "career_rng_independence", "individual_session_participation",
         "coach_focus_intensity", "injury_intervals", "calendar_executor_audit")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def _object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def read_json(path):
    """Only JSON; bounded reads, duplicate keys and non-finite numbers rejected."""
    path = Path(path)
    require(path.suffix.lower() == ".json", "Normalized JSON required; not an FM save decoder")
    with path.open("rb") as stream:
        raw = stream.read(2_000_001)
    require(len(raw) <= 2_000_000, "Checkpoint exceeds 2 MB")
    def bad_constant(value):
        raise ValueError("Non-finite JSON number")
    return json.loads(raw, object_pairs_hook=_object, parse_constant=bad_constant)


def file_sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _keys(value, names):
    require(isinstance(value, dict) and set(value) == set(names), "Unexpected/missing fields")


def _code(value):
    require(isinstance(value, str) and CODE.fullmatch(value), "Anonymous local code required")


def _sha(value):
    require(isinstance(value, str) and SHA.fullmatch(value), "Invalid SHA256")


def _day(value):
    require(isinstance(value, str), "ISO date required")
    parsed = date.fromisoformat(value)
    require(parsed.isoformat() == value, "Canonical ISO date required")
    return parsed


def _number(value, low=None, high=None):
    require(type(value) in (int, float) and math.isfinite(value), "Finite number required, not bool")
    require((low is None or value >= low) and (high is None or value <= high), "Value outside declared bounds")


def measurement(value, unit, sources, *, numeric=False, bounds=(None, None)):
    """None is missing; values require a source byte receipt AND field locator.

    Locators are unverified extraction claims until a separately reviewed adapter
    binds them to actual source semantics. A receipt cannot grant a science gate.
    """
    if value is None:
        return False
    _keys(value, ("value", "unit", "source_sha256", "locator"))
    require(value["unit"] == unit, "Unit mismatch; no implicit conversion")
    require(value["source_sha256"] in sources, "Unresolved field source receipt")
    _code(value["locator"])
    require(value["value"] is not None, "Use null measurement for missing")
    if numeric:
        _number(value["value"], *bounds)
    elif unit == "sha256":
        _sha(value["value"])
    else:
        _code(value["value"])
    return True


def read_checkpoint(path, source_paths):
    """Validate an own-schema JSON export against explicitly supplied private sources.

    Never discovers private saves, imports fmsave, writes game data or advances time.
    source_paths maps expected sha256 to local path; paths never enter the result.
    """
    row = read_json(path)
    _keys(row, ("schema", "origin", "build", "decoder", "start_save_sha256",
                "checkpoint_save_sha256", "replicate", "arm", "day", "rng", "controls",
                "calendar", "participation", "players", "injuries"))
    require(row["schema"] == "train002.checkpoint.v1", "Unknown checkpoint schema")
    require(row["origin"] in ("synthetic", "unvalidated_export"), "No validated native mapper exists")
    require(isinstance(row["build"], str) and re.fullmatch(r"(?:\d+\.\d+\.\d+\+\d+|synthetic-build)", row["build"]), "Versioned build required")
    require(isinstance(row["decoder"], str) and row["decoder"], "Decoder missing")
    sources = set()
    for expected, local_path in source_paths.items():
        _sha(expected)
        require(file_sha256(local_path) == expected, "Source SHA256 mismatch")
        sources.add(expected)
    for name in ("start_save_sha256", "checkpoint_save_sha256"):
        _sha(row[name])
        require(row[name] in sources, "Save byte receipt missing")
    _code(row["replicate"])
    _code(row["arm"])
    now = _day(row["day"])
    missing = []
    measurement(row["rng"], "career_rng_stream", sources)
    if row["rng"] is None:
        missing.append("rng")
    _keys(row["controls"], ("coaches", "facilities", "roster", "opponents", "policy"))
    for key, val in row["controls"].items():
        if not measurement(val, "sha256", sources):
            missing.append("controls." + key)
        elif val is not None:
            _sha(val["value"])
    for group in ("calendar", "participation", "players", "injuries"):
        require(row[group] is None or isinstance(row[group], list), "List or explicit null required")
        if row[group] is None:
            missing.append(group)
    calendar = {}
    for slot in row["calendar"] or []:
        _keys(slot, ("day", "slot", "session"))
        _day(slot["day"])
        require(type(slot["slot"]) is int and slot["slot"] in (0, 1, 2), "Invalid training slot")
        key = (slot["day"], slot["slot"])
        require(key not in calendar, "Duplicate calendar slot")
        calendar[key] = slot["session"]
        if not measurement(slot["session"], "session_code", sources, numeric=True, bounds=(0, 65535)):
            missing.append("calendar.session")
    players = set()
    for player in row["players"] or []:
        _keys(player, ("subject", "attributes_raw", "attributes_display", "ca", "pa", "condition",
                       "sharpness", "fatigue", "match_minutes", "focus", "intensity"))
        _code(player["subject"])
        require(player["subject"] not in players, "Duplicate subject")
        players.add(player["subject"])
        for field, unit, bounds in (("ca", "ca_raw", (0, 200)), ("pa", "pa_raw", (0, 200)),
            ("condition", "condition_raw", (0, 10000)), ("sharpness", "sharpness_raw", (0, 10000)),
            ("fatigue", "fatigue_raw", (None, None)), ("match_minutes", "minutes", (0, None)),
            ("intensity", "intensity_raw", (None, None))):
            if not measurement(player[field], unit, sources, numeric=True, bounds=bounds):
                missing.append("players." + field)
        if not measurement(player["focus"], "focus_code", sources):
            missing.append("players.focus")
        for field, unit, bounds in (("attributes_raw", "attribute_raw", (1, 100)),
                                     ("attributes_display", "attribute_display", (1, 20))):
            if player[field] is None:
                missing.append("players." + field)
            else:
                require(isinstance(player[field], dict) and set(player[field]) == set(INDEX), "Four index fields required")
                for val in player[field].values():
                    if not measurement(val, unit, sources, numeric=True, bounds=bounds):
                        missing.append("players." + field)
    if not players:
        missing.append("cohort_empty")
    if not calendar:
        missing.append("calendar_empty")
    seen = set()
    for event in row["participation"] or []:
        _keys(event, ("subject", "day", "slot", "session", "status", "minutes", "coach"))
        require(event["subject"] in players, "Participation subject missing from cohort")
        key = (event["day"], event["slot"])
        require(key in calendar, "Participation not bound to calendar")
        require(_day(event["day"]) <= now, "Participation cannot be in the future")
        require((event["subject"], *key) not in seen, "Duplicate participation")
        seen.add((event["subject"], *key))
        for field, unit in (("session", "session_code"), ("status", "participation_status"), ("coach", "coach_code")):
            if not measurement(event[field], unit, sources, numeric=field == "session"):
                missing.append("participation." + field)
        if event["session"] and calendar[key]:
            require(event["session"]["value"] == calendar[key]["value"], "Participation session mismatch")
        if event["status"]:
            require(event["status"]["value"] in ("attended", "rest", "rehab", "cancelled", "absent"), "Unknown participation status")
        if not measurement(event["minutes"], "minutes", sources, numeric=True, bounds=(0, 1440)):
            missing.append("participation.minutes")
        elif event["status"] and event["status"]["value"] in ("absent", "cancelled", "rest"):
            require(event["minutes"]["value"] == 0, "Nonparticipation cannot have training minutes")
    if len(seen) < len(players) * len(calendar):
        missing.append("individual_session_coverage")
    injury_ids = set()
    for injury in row["injuries"] or []:
        _keys(injury, ("event", "subject", "start", "end", "end_kind", "cause", "source_sha256", "locator"))
        _code(injury["event"])
        require(injury["event"] not in injury_ids and injury["subject"] in players, "Duplicate injury or unknown subject")
        injury_ids.add(injury["event"])
        require(injury["source_sha256"] in sources, "Unresolved injury receipt")
        _code(injury["locator"])
        require(injury["cause"] in (None, "match", "training", "other"), "Unknown injury cause")
        start = _day(injury["start"]) if injury["start"] else None
        end = _day(injury["end"]) if injury["end"] else None
        require(injury["end_kind"] in (None, "observed_return", "expected_return"), "Unknown injury end semantics")
        require(start is None or start <= now, "Injury starts after checkpoint")
        require(start is None or end is None or end >= start, "Negative injury interval")
        require(injury["end_kind"] != "observed_return" or (end is not None and end <= now), "Future/missing actual return")
        if start is None or end is None or injury["end_kind"] != "observed_return":
            missing.append("injury_observed_interval")
    return {"schema": row["schema"], "origin": row["origin"], "build": row["build"],
            "checkpoint_sha256": file_sha256(path), "replicate": row["replicate"], "arm": row["arm"],
            "day": row["day"], "start_save_sha256": row["start_save_sha256"],
            "control_hash_claims": {k: v["value"] if v else None for k, v in row["controls"].items()},
            "claimed_rng_stream": row["rng"]["value"] if row["rng"] else None,
            "structurally_valid": True, "missing": sorted(set(missing)),
            "players": len(players), "scheduled_slots": len(calendar), "participation_rows": len(seen),
            "source_semantics_verified": False, "native_released": False, "career_released": False,
            "blocked_gates": list(GATES)}


def replicate_diagnostic(checkpoints):
    """Detect clone/control issues; differing claimed RNG labels never prove independence."""
    starts, rngs, groups = defaultdict(set), defaultdict(set), defaultdict(list)
    for row in checkpoints:
        groups[row["replicate"]].append(row)
        starts[row["start_save_sha256"]].add(row["replicate"])
        if row["claimed_rng_stream"]:
            rngs[row["claimed_rng_stream"]].add(row["replicate"])
    return {"declared_replicates": len(groups), "independent_replicates_verified": None,
            "start_clone_groups": sum(len(v) > 1 for v in starts.values()),
            "rng_label_clone_groups": sum(len(v) > 1 for v in rngs.values()),
            "within_pair_start_mismatch": sum(len({r["start_save_sha256"] for r in rows}) != 1 for rows in groups.values()),
            "within_pair_control_mismatch": sum(len({json.dumps(r["control_hash_claims"], sort_keys=True) for r in rows}) != 1 for rows in groups.values()),
            "rng_independence_verified": False, "career_released": False}


def calibration_diagnostic(pairs):
    """Describe absolute raw/display receipts; no assumed rounding or delta conversion.

    Caller data never establishes native mapping. Differing display for equal raw
    exposes a conflict; sparse observations do not establish a conversion curve.
    """
    cells = defaultdict(set)
    for raw, display in pairs:
        _number(raw, 1, 100)
        _number(display, 1, 20)
        cells[raw].add(display)
    return {"absolute_pairs": len(pairs), "distinct_raw_values": len(cells),
            "conflicting_raw_values": sorted(k for k, v in cells.items() if len(v) > 1),
            "mapping_validated": False, "conversion_formula": None,
            "reason": "Independent current-build raw/display source audit required"}


def historical_diagnostic(root):
    """Reconstruct archive-only descriptions without relabelling them as new trials."""
    folder = Path(root) / "data/training"
    manifest, exposure, aa = [read_json(folder / name) for name in ("manifest.json", "exposure.json", "repeatability.json")]
    rows = []
    with (folder / "player-deltas.jsonl").open(encoding="utf8") as stream:
        for line in stream:
            row = json.loads(line, object_pairs_hook=_object)
            require(isinstance(row["delta"]["raw"], dict), "Historic raw attributes absent")
            for key in INDEX:
                _number(row["delta"]["raw"][key])
            _number(row["delta"]["ca"])
            rows.append(row)
    keys = [(r["trial"], r["cohort"], r["subject"], r["checkpoint"], r["arm"]) for r in rows]
    require(len(keys) == len(set(keys)), "Duplicate historical player observation")
    contrasts = []
    for trial, week, arms in (("conditioning-heavy", 6, ("A", "B")), ("conditioning-rest", 4, ("A", "C"))):
        samples = [[r for r in rows if (r["trial"], r["checkpoint"], r["arm"]) == (trial, week, arm)] for arm in arms]
        require(all(len(v) == 22 for v in samples), "Historical endpoint cohort incomplete")
        means = [statistics.mean(statistics.mean(r["delta"]["raw"][k] for k in INDEX) for r in v) for v in samples]
        cas = [statistics.mean(r["delta"]["ca"] for r in v) for v in samples]
        # Historic rows are cumulative since baseline, not weekly increments.
        contexts = [c for c in exposure[trial] if c["checkpoint"] == week]
        require(len(contexts) == 1, "Historical exposure endpoint missing/duplicate")
        totals = {arm: {"match_minutes": contexts[0]["arms"][arm]["recorded_minutes"],
                         "injury_entries": contexts[0]["arms"][arm]["injury_events"]} for arm in arms}
        contrasts.append({"trial": trial, "week": week, "control": arms[0], "intervention": arms[1],
                          "index_mean_raw": means, "index_difference_raw": means[1] - means[0],
                          "ca_difference": cas[1] - cas[0], "observed_exposure_aggregates": totals})
    return {"origin": "historical_public_archive", "build": manifest["build"], "decoder": manifest["decoder"],
            "source_files_sha256": {name: file_sha256(folder / name) for name in ("manifest.json", "player-deltas.jsonl", "exposure.json", "repeatability.json")},
            "player_rows": len(rows), "trial_rows": dict(sorted(Counter(r["trial"] for r in rows).items())),
            "independent_treatment_replicates_verified": None,
            "individual_participation": None, "injury_days": None, "raw_display_calibration": None,
            "exploratory_descriptions": contrasts,
            "aa": {k: aa[k] for k in ("matched", "identicalRawAttributeProfiles", "identicalCA", "identicalCondition", "identicalSharpness")},
            "native_matches_started": 0, "calendar_advances": 0, "seeds_reserved": 0,
            "native_released": False, "career_released": False, "blocked_gates": list(GATES)}

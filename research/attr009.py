"""ATTR-009 intentions and strict offline comparators; no native process or grant.

Raw ability 60->80 is the intervention. Lab UI division by five is documented
separately; this module makes no claim about the FM career display scale.
"""
from copy import deepcopy
import struct

from .core import config_hash
from .native import require
from .validation003 import POSITION_INDEX, validate_attributes

EXPERIMENT = "ATTR-009-Bridge"
CONTEXTS = ("high_press", "deep_block")
ARMS = ("OJ", "OA", "OP", "SJ", "SA", "SP")
ABILITY = {"J": 54, "A": 49, "P": 53}
COEFFICIENTS = (-1., .5, .5, 1., -.5, -.5)
SECONDARY = ("points", "gf", "ga", "xgf", "xga")
POSITIONS = {**POSITION_INDEX, "MCL": 7, "MCR": 7}
RAW_BASE, RAW_HIGH = 60, 80


def matrix():
    return [dict(id=a, mask="omni" if a[0] == "O" else "specialized",
                 attribute=a[1], attribute_index=ABILITY[a[1]],
                 raw_before=RAW_BASE, raw_after=RAW_HIGH)
            for a in ARMS]


def bindings(team, side, oop_map):
    """Each logical phase cell belongs to lineup[i]; native OOP slot is mapped.

    Mapped native OOP slot must not be used to index the logical OOP cells again.
    The mapping is read from the frozen fixture and audited by the host binding
    receipt; caller-supplied arrays alone are intentions, never native evidence.
    """
    require(type(side) is int and side in (0, 1), "Invalid side")
    require(len(oop_map) == 2 and all(sorted(m) == list(range(11)) and
            all(type(v) is int for v in m) for m in oop_map), "OOP permutation missing")
    lineup = team["lineup"]
    require(len(lineup) == 11 and len(set(lineup)) == 11 and all(
        type(i) is int and 0 <= i < team["roster_size"] for i in lineup), "Invalid lineup")
    require(len(team["phases"]) == 2 and all(len(p) == 11 for p in team["phases"]), "Both phases required")
    result = []
    for i, roster in enumerate(lineup):
        ip, oop = (team["phases"][p][i]["position"] for p in (0, 1))
        require(ip in POSITIONS and oop in POSITIONS, "Unknown phase position")
        active = sorted({POSITIONS[ip], POSITIONS[oop]})
        require(active == [0] if i == 0 else min(active) >= 2, "GK/Sweeper policy differs")
        result.append(dict(logical_slot=i, roster_slot=roster, ip_position=ip,
                           oop_position=oop, ip_native_slot=i,
                           oop_native_slot=oop_map[side][i], active_rating_families=active))
    return result


def apply_arm(base, side, arm, oop_map):
    require(arm in ARMS, "Unknown arm")
    require(base.get("rules") == "game" and base.get("fixture") == "bundled_match_pkm", "Fixture/rules drift")
    require("experimental_execution" not in base and "away_tactic_pool" not in base,
            "Uniform pool/experimental execution forbidden, including disabled keys")
    result = deepcopy(base)
    team = result["teams"][side]
    # The bundled away carrier has26 serialized slots but only23 active inputs.
    # Preserve its three unused tail slots, never pad/trim or pretend they ran.
    require(team["roster_size"] == 23 and len(team["players"]) >= 23, "Controlled roster capacity drift")
    bound = bindings(team, side, oop_map)
    for cell in bound[1:]:
        player = team["players"][cell["roster_slot"]]
        values = player["attributes"]
        validate_attributes(values)
        require(values[:15] == [0, 0] + [20]*13, "Expected frozen omnipotent baseline")
        require(all(values[i] == RAW_BASE for i in ABILITY.values()), "Raw dose baseline differs")
        if arm[0] == "S":
            values[2:15] = [1]*13
            for index in cell["active_rating_families"]:
                values[index] = 20
        values[ABILITY[arm[1]]] = RAW_HIGH
        validate_attributes(values)
    # GK, bench, opponent, all profiles, tactics, phases and PI remain exact.
    changes = []
    for cell in bound[1:]:
        i = cell["roster_slot"]
        before, after = base["teams"][side]["players"][i]["attributes"], team["players"][i]["attributes"]
        for index, (a, b) in enumerate(zip(before, after, strict=True)):
            if a != b:
                changes.append(dict(side=side, roster_slot=i, attribute=index, before=a, after=b))
    return result, bound, changes


def audit_binary(before, after, changes):
    require(before[:12] == after[:12] and len(before) == len(after), "Binary header/count differs")
    require(len(before) >= 12 and (len(before)-12) % 20 == 0, "Invalid scenario record size")
    a = list(struct.iter_unpack("<5I", before[12:]))
    b = list(struct.iter_unpack("<5I", after[12:]))
    # Kind1 is the documented attribute record, a=roster index, b=attribute index.
    wanted = {((1, c["side"], c["roster_slot"], c["attribute"], c["before"]),
               (1, c["side"], c["roster_slot"], c["attribute"], c["after"])) for c in changes}
    actual = {(x, y) for x, y in zip(a, b, strict=True) if x != y}
    require(actual == wanted and len(actual) == len(changes), "Undeclared/missing binary change")
    return dict(changed_records=len(actual), undeclared_changes=0)


def raw_readback(before, after, config, side, arm, bound):
    """Check full native arrays and explicit raw dose against the baseline dump.

    This comparator does not itself prove sampling stage/build/seed. Those are
    required independent host receipts in the runner, never caller booleans.
    """
    evidence = []
    for s, team in enumerate(config["teams"]):
        observed = after["teams"][s]
        require(observed["side"] == s and observed["count"] == 23, "Native side/capacity differs")
        require([(p["id"], p["attributes"]) for p in observed["players"]] ==
                [(p["native_id"], p["attributes"]) for p in team["players"][:23]], "Native attributes/identities differ")
    for cell in bound[1:]:
        i = cell["roster_slot"]
        a, b = before["teams"][side]["players"][i], after["teams"][side]["players"][i]
        require(a["id"] == b["id"] and a["attributes"][ABILITY[arm[1]]] == RAW_BASE and
                b["attributes"][ABILITY[arm[1]]] == RAW_HIGH, "Missing native before/after dose")
        evidence.append(dict(roster_slot=i, attribute=ABILITY[arm[1]], before=RAW_BASE, after=RAW_HIGH))
    return dict(raw_dose=evidence, input_attribute_values=2*23*69,
                native_fm_display_calibrated=False, mechanism_decomposition_identified=False)


def capability_report():
    return dict(experiment_id=EXPERIMENT, native_validation_granted=False,
        raw_intervention=dict(base=RAW_BASE, high=RAW_HIGH, scale="native integer1..100",
                              lab_ui_formatter="raw/5; source-level display only",
                              fm_in_game_display_calibrated=False),
        passive_effectiveness=dict(status="unavailable_without_intervention",
            reason="execution_snapshot returns unless execution_active; enabling kind61 changes version/hooks and final records",
            mechanism_decomposition_identified=False),
        estimand="total mask x raw attribute intervention; no mediation claim",
        pending=["current identity", "native after-original-preparation masks/binding/dose readbacks",
                 "all69 attributes/23 profiles/roles/PI/seed", "32 full technical matches+1 negative",
                 "publication+CI+independent review"],
        design_sha256=config_hash(matrix()))

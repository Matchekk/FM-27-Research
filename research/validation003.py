"""Offline VALID-003 profile intentions and capacity-preserving context checks.

This module never imports the Tactics Lab, executes a host, decodes opaque PKM
bytes or grants native/replay approval. Native identifiers stay in private return
values; public_context() is the deliberately small publication boundary.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path


POSITION_INDEX = {
    "GK": 0, "SW": 1, "DL": 2, "DC": 3, "DCL": 3, "DCR": 3,
    "DR": 4, "DM": 5, "DML": 5, "DMR": 5, "ML": 6, "MC": 7,
    "MR": 8, "AML": 9, "AMC": 10, "AMR": 11, "ST": 12,
    "WBL": 13, "WBR": 14,
}
LEVELS = {"low": 40, "medium": 60, "high": 80}
# These are our declared synthetic interventions, not empirical FM strength weights.
BOOSTS = {
    "GK": (26, 27, 28, 29, 34, 36),
    "IV": (18, 20, 24, 35, 51, 54),
    "AV": (15, 20, 24, 49, 52, 53),
    "DM": (22, 24, 32, 33, 35, 43),
    "AM": (21, 22, 25, 37, 38, 67),
    "WING": (15, 16, 21, 37, 49, 53),
    "ST": (17, 18, 21, 49, 54, 67),
}
# Do not interpret a simultaneous increase in injury proneness/dirtiness as strength.
FIXED_ABILITY_INDICES = (39, 40, 46, 48, 56, 59, 60, 62, 63, 64, 65)
REQUIRED_PROFILE_FIELDS = (
    "height_cm", "age", "professionalism", "loyalty", "sportsmanship",
    "temperament", "pressure", "ambition", "adaptability", "traits_low",
    "traits_high", "current_ability", "home_reputation", "current_reputation",
    "world_reputation", "condition", "sharpness", "sharpness_secondary",
    "fatigue_raw", "weight_kg", "team_cohesion", "club_cohesion", "morale",
)
PROFILE_RANGES = {
    "height_cm": (140, 220), "age": (14, 60),
    **{k: (1, 20) for k in ("professionalism", "loyalty", "sportsmanship", "temperament",
                             "pressure", "ambition", "adaptability", "morale")},
    "traits_low": (0, 0xffffffff), "traits_high": (0, 0xffffffff),
    "current_ability": (0, 200),
    **{k: (0, 10000) for k in ("home_reputation", "current_reputation", "world_reputation",
                               "condition", "sharpness", "sharpness_secondary")},
    "fatigue_raw": (0, 65535), "weight_kg": (40, 140),
    "team_cohesion": (0, 100), "club_cohesion": (0, 100),
}
CONTEXT_MISSING = ("fixture_to_dump_binding", "reader_build_and_source_hashes",
                   "after_original_preparation_receipt", "original_manager_context",
                   "passive_effectiveness_readbacks")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical_hash(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return sha256(encoded.encode("utf8")).hexdigest()


def validate_attributes(values):
    require(isinstance(values, list) and len(values) == 69, "Exactly 69 attributes required")
    require(all(type(v) is int and (0 <= v <= 20 if i < 15 else 1 <= v <= 100)
                for i, v in enumerate(values)), "Attribute type/range mismatch")
    return values


def profile(kind, ip_position, oop_position, level="medium"):
    """Own explicit 69-vector; active rating families20, unused field families1.

    No native slot mapping is inferred: callers must pass the actual IP/OOP
    positions of the same player after resolving the side-specific OOP mapping.
    """
    require(kind in BOOSTS and level in LEVELS, "Unknown profile kind/level")
    require(ip_position in POSITION_INDEX and oop_position in POSITION_INDEX,
            "Unknown IP/OOP position")
    active = sorted({POSITION_INDEX[ip_position], POSITION_INDEX[oop_position]})
    require((kind == "GK" and active == [0]) or (kind != "GK" and min(active) >= 2),
            "GK/Sweeper needs an explicit separate profile policy")
    values = [0, 0] + [1] * 13 + [LEVELS[level]] * 54
    for index in FIXED_ABILITY_INDICES:
        values[index] = 60
    for index in BOOSTS[kind]:
        values[index] = min(100, LEVELS[level] + 10)
    if kind == "GK":
        values[:15] = [20] + [0] * 14
    else:
        for index in active:
            values[index] = 20
    validate_attributes(values)
    return dict(schema=1, origin="own_declared_synthetic_vector", kind=kind, level=level,
                ip_position=ip_position, oop_position=oop_position,
                active_rating_families=active, attributes=values,
                position_ratings=values[:15], native_validated=False,
                ability_scale="native integer1..100; no universal display-scale calibration claimed",
                strength_claim="declared attribute vector only; no CA/equal-strength calibration")


def profile_catalog():
    positions = {"GK": ("GK", "GK"), "IV": ("DCR", "DCR"),
                 "AV": ("DR", "DR"), "DM": ("DMR", "MC"),
                 "AM": ("AMC", "AMC"), "WING": ("AMR", "MR"),
                 "ST": ("ST", "ST")}
    return {f"{kind}-{level}": profile(kind, *pair, level)
            for kind, pair in positions.items() for level in LEVELS}


def inspect_pkm_file(path):
    """Only fingerprint the opaque source. Do not pretend this is a PKM reader."""
    path = Path(path)
    require(path.is_file() and path.suffix.lower() == ".pkm", "Existing PKM file required")
    return dict(source_sha256=sha256(path.read_bytes()).hexdigest(), size_bytes=path.stat().st_size,
                capacity=None, teams=None, reader_status="opaque_not_decoded",
                missing=["native_reader_context", "original_roster_capacity", "manager_context",
                         "original_player_identity", "fixture_to_dump_binding"],
                native_validated=False, career_replay_released=False)


def context_from_dump(dump, fixture_sha256):
    """Preserve an already available private native dump, with no23-player cap.

    Structural validity does not bind a dump to a PKM, prove its sampling stage,
    or validate its proprietary reader. Those gates remain visibly missing.
    """
    require(isinstance(fixture_sha256, str) and len(fixture_sha256) == 64 and
            all(c in "0123456789abcdef" for c in fixture_sha256), "Fixture SHA256 required")
    teams = dump.get("teams") if isinstance(dump, dict) else None
    require(isinstance(teams, list) and len(teams) == 2, "Two native teams required")
    result = []; all_ids = set()
    for side, team in enumerate(teams):
        require(team.get("side") == side and type(team.get("side")) is int,
                "Native side identity mismatch")
        count, players = team.get("count"), team.get("players")
        require(type(count) is int and 1 <= count <= 256 and isinstance(players, list),
                "Invalid native capacity")
        require(count == len(players), "Native capacity/list mismatch; no trimming or padding")
        identities = []
        for player in players:
            identity = player.get("id")
            require(type(identity) is int and 0 < identity <= 0xffffffff and identity not in all_ids,
                    "Missing/duplicate native player identity")
            all_ids.add(identity); identities.append(identity)
            validate_attributes(player.get("attributes"))
        result.append(dict(side=side, count=count, private_player_ids=identities,
                           private_players=deepcopy(players),
                           roster_sha256=canonical_hash(identities),
                           attributes_sha256=canonical_hash([p["attributes"] for p in players])))
    return dict(schema=1, fixture_sha256=fixture_sha256, private_teams=result,
                missing=["fixture_to_dump_binding", "reader_build_and_source_hashes",
                         "after_original_preparation_receipt", "original_manager_context",
                         "passive_effectiveness_readbacks"],
                native_validated=False, career_replay_released=False)


def public_context(context):
    """Never export native IDs, names, arrays, source paths or private dump bytes."""
    for value in [context["fixture_sha256"], *[t[k] for t in context["private_teams"]
                                            for k in ("roster_sha256", "attributes_sha256")]]:
        require(isinstance(value, str) and len(value) == 64 and
                all(c in "0123456789abcdef" for c in value), "Public context requires hashes, not paths")
    require(len(context["private_teams"]) == 2 and all(
        type(t["side"]) is int and t["side"] == s and type(t["count"]) is int and 1 <= t["count"] <= 256
        for s, t in enumerate(context["private_teams"])), "Invalid public side/count")
    return dict(schema=context["schema"], fixture_sha256=context["fixture_sha256"],
                teams=[{k: t[k] for k in ("side", "count", "roster_sha256", "attributes_sha256")}
                       for t in context["private_teams"]], missing=list(CONTEXT_MISSING),
                native_validated=False, career_replay_released=False)


def bind_profiles(context, by_side):
    """Private planned binding, exactly preserving every observed ID and capacity."""
    require(set(by_side) == {0, 1}, "Both native sides required")
    bound = []
    for team in context["private_teams"]:
        profiles = by_side[team["side"]]
        require(isinstance(profiles, list) and len(profiles) == team["count"],
                "Profile count must match observed capacity exactly")
        for identity, intended in zip(team["private_player_ids"], profiles, strict=True):
            validate_attributes(intended.get("attributes"))
            bound.append(dict(side=team["side"], native_id=identity,
                              attributes=list(intended["attributes"])))
    return bound


def audit_readback(expected, observed):
    """Strict comparison interface; absence is missing, disagreement is mismatch.

    expected needs explicit attributes and all23 native profile fields. This is
    a future adapter contract, not a decoder for state_hex or an invented default.
    """
    missing = []; mismatches = []
    for key in ("native_id", "side", "attributes"):
        if key not in expected or expected[key] is None:
            missing.append("expected." + key)
        elif key not in observed or observed[key] is None:
            missing.append("observed." + key)
        elif expected[key] != observed[key]:
            mismatches.append(key)
    for source, row in (("expected", expected), ("observed", observed)):
        for key, low, high in (("native_id", 1, 0xffffffff), ("side", 0, 1)):
            if row.get(key) is not None and not (type(row[key]) is int and low <= row[key] <= high):
                mismatches.append(source + "." + key + ".type_or_range")
    if expected.get("attributes") is not None:
        validate_attributes(expected["attributes"])
    if observed.get("attributes") is not None:
        validate_attributes(observed["attributes"])
    for field in REQUIRED_PROFILE_FIELDS:
        a, b = expected.get("native_profile", {}).get(field), observed.get("native_profile", {}).get(field)
        if a is None:
            missing.append("expected.native_profile." + field)
        elif b is None:
            missing.append("observed.native_profile." + field)
        elif not (type(a) is int and type(b) is int and
                  PROFILE_RANGES[field][0] <= a <= PROFILE_RANGES[field][1] and
                  PROFILE_RANGES[field][0] <= b <= PROFILE_RANGES[field][1]) or a != b:
            mismatches.append("native_profile." + field)
    for key in ("both_phases_verified", "effective_seed_verified", "identity_verified",
                "after_original_preparation", "passive_effectiveness_verified"):
        if observed.get(key) is not True:
            missing.append("observed." + key)
    return dict(passed=not missing and not mismatches, missing=missing, mismatches=mismatches,
                native_validation_granted=False,
                career_replay_released=False)

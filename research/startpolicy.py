"""Own offline FM27CFG1 codec and opt-in MECH-002 record-level start policy.

This is artifact preparation, NOT a runner or a native approval. It never
imports the upstream server, executes a host or edits a file. Callers must not
feed its opt-in output into historical NativeLab.run: that runner deliberately
requires the historical normalizer's bytes. A new audited runner and passive
native receipts are still missing. No memory hooks or repeated writes exist.
"""
from dataclasses import dataclass
import struct

VERSION = "mech002-startpolicy-offline-v1"
MAGIC = b"FM27CFG1"
SHARPNESS_FIELDS = (16, 17)
BLOCKERS = (
    "no_versioned_startpolicy_runner_binding",
    "host_applies_profiles_before_not_after_original_preparation",
    "no_passive_profile_receipt_at_first_progression",
    "no_passive_original_familiarity_receipts",
    "no_native_opt_in_startpolicy_acceptance",
)
PROFILE_LIMITS = (
    (140, 220), (14, 60), *((1, 20),) * 7, (0, 0xffffffff), (0, 0xffffffff),
    (0, 200), *((0, 10000),) * 6, (0, 65535), (40, 140), (0, 100), (0, 100), (1, 20),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decode_records(payload):
    """Decode only the bounded public record grammar; reject opaque wrappers."""
    require(type(payload) is bytes and payload[:8] == MAGIC, "Expected plain FM27CFG1 bytes")
    require(len(payload) >= 12, "Truncated config header")
    count = struct.unpack_from("<I", payload, 8)[0]
    require(len(payload) == 12 + count * 20, "Record count/length mismatch")
    return tuple(struct.iter_unpack("<5I", payload[12:]))


def encode_records(records):
    """Serialize explicit ordered records, preserving historical order exactly."""
    records = tuple(tuple(row) for row in records)
    require(len(records) <= 0xffffffff, "Too many records")
    require(all(len(r) == 5 and all(type(v) is int and 0 <= v <= 0xffffffff for v in r)
                for r in records), "Expected five uint32 values per record")
    return MAGIC + struct.pack("<I", len(records)) + b"".join(struct.pack("<5I", *r) for r in records)


@dataclass(frozen=True)
class StartPolicy:
    tested_side: int
    level_raw: int

    def __post_init__(self):
        require(type(self.tested_side) is int and self.tested_side in (0, 1), "Invalid tested side")
        require(type(self.level_raw) is int and self.level_raw in (7000, 10000), "Only raw 7000/10000 are declared")


def encode_startpolicy(records, policy=None):
    """Compile own ordered records, with an explicitly selected policy.

    With no policy this is exactly encode_records(records), without a new
    normalization step. Opt-in requires complete absolute roster/lineup and
    controlled profile inputs. GK is the first lineup cell under the D00
    contract; native phase/identity audits must independently prove that binding.
    Only the twenty field16/17 values of ten starting outfield roster slots may
    differ. Other records, ordering and record counts are preserved.
    """
    records = tuple(tuple(r) for r in records)
    baseline = encode_records(records)
    if policy is None:
        return baseline
    require(type(policy) is StartPolicy, "Explicit StartPolicy required")
    require(not any(r[0] == 61 for r in records), "Experimental execution forbidden")
    sizes, lineups, profiles = {}, {}, {}
    for kind, side, a, b, value in records:
        if kind not in (11, 15, 17):
            continue
        require(side in (0, 1), "Invalid team side")
        if kind == 17:
            require(side not in sizes and a == b == 0 and 11 <= value <= 32, "Invalid/duplicate roster size")
            sizes[side] = value
        elif kind == 11:
            require(a in range(11) and b == 0 and (side, a) not in lineups, "Invalid/duplicate lineup record")
            lineups[side, a] = value
        else:
            require(b in range(23) and (side, a, b) not in profiles, "Unknown/duplicate profile field")
            lo, hi = PROFILE_LIMITS[b]
            require(lo <= value <= hi, "Out-of-range profile value")
            profiles[side, a, b] = value
    require(set(sizes) == {0, 1}, "Absolute roster sizes missing")
    require(set(lineups) == {(s, i) for s in (0, 1) for i in range(11)}, "Absolute lineups missing")
    for side in (0, 1):
        lineup = [lineups[side, i] for i in range(11)]
        require(len(set(lineup)) == 11 and all(p < sizes[side] for p in lineup), "Invalid starting roster binding")
        for slot in range(sizes[side]):
            for field, expected in ((15, 10000), (16, 10000), (17, 10000), (18, 0),
                                    (20, 80), (21, 100), (22, 20)):
                require(profiles.get((side, slot, field)) == expected, "Incomplete/nonstandard controlled profile")
    require(all(a < sizes[s] for s, a, _ in profiles), "Profile outside active roster")
    affected = {lineups[policy.tested_side, i] for i in range(1, 11)}
    updated = tuple((k, s, a, b, policy.level_raw)
                    if k == 15 and s == policy.tested_side and a in affected and b in SHARPNESS_FIELDS
                    else (k, s, a, b, v) for k, s, a, b, v in records)
    return encode_records(updated)


def native_status():
    """There is no native receipt decoder/approval path in this offline version."""
    return dict(version=VERSION, status="blocked", native_execution_allowed=False,
                blockers=list(BLOCKERS))

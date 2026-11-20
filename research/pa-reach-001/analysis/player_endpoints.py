"""Stream private landmark outcomes from the verified capture, one player per line."""
import argparse
from datetime import date
from itertools import groupby
import json
from pathlib import Path
import sqlite3


def endpoint(rows):
    first = rows[0]
    dob = date.fromisoformat(first["birth"])
    try:
        horizon = dob.replace(year=dob.year + 28)
    except ValueError:
        horizon = dob.replace(year=dob.year + 28, day=28)
    if first["position"] in (None, "GK") or first["day"] >= horizon.isoformat():
        return None
    observed = [r for r in rows if r["day"] <= horizon.isoformat()]
    peak = max(observed, key=lambda r: r["ca"])
    peak_day = date.fromisoformat(peak["day"])
    age_at_peak = peak_day.year - dob.year - ((peak_day.month, peak_day.day) < (dob.month, dob.day))
    baseline_pa = first["pa"]
    targets = {}
    for name, level in (("full", baseline_pa), ("pa95", (95 * baseline_pa + 99) // 100),
                        ("pa_minus_2", baseline_pa - 2)):
        hit = next((r["day"] for r in observed if r["ca"] >= level), None)
        if hit == first["day"]:
            status = "ALREADY_AT_BASELINE"
        elif hit:
            status = "OBSERVED_HIT"
        elif rows[-1]["day"] < horizon.isoformat():
            status = "RIGHT_CENSORED"
        else:
            status = "NO_OBSERVED_HIT_BY_HORIZON_COVERAGE_UNVERIFIED"
        targets[name] = {"status": status, "first_observed_hit": hit}
    by_day = {r["day"]: r["ca"] for r in observed}
    start = date.fromisoformat(first["day"])
    annual_ca = {}
    for years in (1, 2):
        try:
            anniversary = start.replace(year=start.year + years)
        except ValueError:
            anniversary = start.replace(year=start.year + years, day=28)
        annual_ca[str(12 * years)] = by_day.get(anniversary.isoformat())
    return {
        "schema_version": 1, "baseline_date": first["day"], "baseline_CA": first["ca"],
        "baseline_PA": baseline_pa, "target_date": horizon.isoformat(),
        "last_observed_in_window": observed[-1]["day"], "ca_at_exact_month": annual_ca,
        "observed_peak_CA": peak["ca"], "first_observed_peak_date": peak["day"],
        "age_at_observed_peak": age_at_peak, "observed_peak_fraction": peak["ca"] / baseline_pa,
        "last_minus_baseline_CA": observed[-1]["ca"] - first["ca"],
        "pa_changed_in_window": any(r["pa"] != baseline_pa for r in observed),
        "targets": targets,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("private_database", type=Path)
    parser.add_argument("career")
    parser.add_argument("private_output", type=Path)
    args = parser.parse_args()
    with sqlite3.connect(args.private_database.resolve().as_uri() + "?mode=ro", uri=True) as conn:
        conn.row_factory = sqlite3.Row
        records = conn.execute("SELECT * FROM observation WHERE career=? ORDER BY uid,birth,day",
                               (args.career,))
        with args.private_output.open("x", encoding="utf-8") as out:
            for (uid, birth), group in groupby(records, key=lambda r: (r["uid"], r["birth"])):
                result = endpoint(list(group))
                if result:
                    result.update(career_id=args.career, player_id_within_career=uid, birth=birth)
                    out.write(json.dumps(result, separators=(",", ":")) + "\n")

"""Evaluate two fixed CA point predictions on a subsequent month of the same career."""
import argparse
from collections import defaultdict
from datetime import date
import json
from math import sqrt
from pathlib import Path
import sqlite3


MANIFESTS = Path(__file__).resolve().parents[1] / "manifests"


def measure(history, followup):
    uri = lambda path: path.resolve().as_uri() + "?mode=ro"
    with sqlite3.connect(uri(history), uri=True) as conn:
        conn.execute("ATTACH DATABASE ? AS later", (uri(followup),))
        series = []
        for schema, filename in [("main", "zubieta-native-input.json"),
                                 ("later", "zubieta-control-native-input.json")]:
            manifest = json.loads((MANIFESTS / filename).read_bytes())
            dates = sorted(manifest["snapshots"])
            expected = [(day, manifest["engine_build"], manifest["snapshots"][day]["save_sha256"],
                         manifest["snapshots"][day]["native_sha256"]) for day in dates]
            actual = conn.execute(f"SELECT day,build,save_hash,inventory_hash FROM {schema}.snapshot "
                                  "WHERE career=? ORDER BY day", (manifest["career_id"],)).fetchall()
            if actual != expected or len(actual) != 2:
                raise ValueError("Series differs from dated, hash-checked inputs")
            series.append((manifest["career_id"], actual))
        (past, previous), (future, following) = series
        if previous[-1] != following[0]:
            raise ValueError("Two series must share the exact same baseline")
        t0, t1, t2 = [date.fromisoformat(row[0]) for row in (previous[0], previous[1], following[1])]
        weight = (t2-t1).days / (t1-t0).days
        pairs = conn.execute("""
            SELECT b.age, b.pa-b.ca, a.ca, b.ca, c.ca, b.club FROM main.observation b
            JOIN main.observation a ON a.career=b.career AND a.uid=b.uid AND a.birth=b.birth
            JOIN later.observation c ON c.uid=b.uid AND c.birth=b.birth
            WHERE a.career=? AND a.day=? AND b.day=? AND c.career=? AND c.day=?
                  AND b.age<28 AND b.position<>'GK'
            """, (past, str(t0), str(t1), future, str(t2)))
        groups = defaultdict(lambda: defaultdict(list))
        clubs = defaultdict(lambda: defaultdict(list))
        for age, gap, ca0, ca1, ca2, club in pairs:
            categories = ["all"]
            if gap > 30 and age < 18:
                categories.append("under18_gap_gt30")
            if gap > 30 and age >= 24:
                categories.append("age24_27_gap_gt30")
            initial_error = ca1 - ca2
            trend_error = max(1, min(200, ca1 + weight * (ca1 - ca0))) - ca2
            for name in categories:
                groups[name]["carry_forward"].append(initial_error)
                groups[name]["previous_rate"].append(trend_error)
                if club is not None:
                    clubs[name][club].append(abs(trend_error) - abs(initial_error))
        if not groups:
            raise ValueError("No complete longitudinal observations")
    def metrics(errors):
        n = len(errors)
        return {"n": n, "mae_ca": sum(map(abs,errors))/n, "rmse_ca": sqrt(sum(e*e for e in errors)/n),
                "mean_prediction_minus_observed_ca": sum(errors)/n}
    def club_jackknife(samples):
        n = sum(len(x) for x in samples.values())
        total = sum(map(sum, samples.values()))
        replicates = [(total - sum(values)) / (n - len(values)) for values in samples.values()]
        k = len(replicates)
        mean = sum(replicates) / k
        se = sqrt((k - 1) / k * sum((r - mean) ** 2 for r in replicates))
        delta = total / n
        return {"n": n, "clubs": k, "mae_previous_rate_minus_carry_forward": delta,
                "approximate_club_conditional_95ci": [delta - 1.96 * se, delta + 1.96 * se]}
    return {"schema": "pa-reach-short-horizon-reference/v1", "dates": list(map(str,(t0,t1,t2))),
            "career_origins": 1, "untouched_test_careers": 0, "fitted_parameters": 0,
            "paired_mae_difference_known_club": {g: club_jackknife(s) for g,s in clubs.items()
                                                  if len(s) > 1},
            "groups": {g: {m: metrics(e) for m,e in ms.items()} for g,ms in groups.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path)
    parser.add_argument("followup", type=Path)
    args = parser.parse_args()
    print(json.dumps(measure(args.history, args.followup), indent=2))

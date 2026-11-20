"""Plot observed PA hits and CA changes from public, same-career aggregates."""
import argparse
from datetime import date
from itertools import accumulate
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt


def plot(outcome, windows, output):
    hits = json.loads(outcome.read_bytes())
    base = hits["baseline_day"]
    dates = list(sorted(hits["snapshots"]))
    last = date.fromisoformat(dates[-1])
    groups = hits["groups"]["all"]
    quarters = {}
    for path in windows:
        window = json.loads(path.read_bytes())
        if window["source_root"] != hits["snapshots"][base]:
            raise ValueError("Different March baseline")
        for day, source in window["new_snapshots"].items():
            period = f"{base}:{day}"
            if period not in window["age_gap_intervals"] or day not in dates:
                continue
            if any(source[k] != h for k, h in hits["snapshots"][day].items()):
                raise ValueError("Checkpoint provenance differs")
            d = date.fromisoformat(day)
            if d.day == 30 and d.month in (3, 6, 9, 12):
                quarters[d] = window["age_gap_intervals"][period]["age_gap"]
    if last not in quarters:
        raise ValueError("Expected growth data through the same quarter as the hit counts")
    days = sorted(quarters)
    ticks = [date.fromisoformat(base), *days]
    fig, (left, right) = plt.subplots(1, 2, figsize=(12.5, 5.2))
    fig.subplots_adjust(top=.78, bottom=.27, left=.07, right=.97, wspace=.22)
    colors = ["#1e5671", "#d37527", "#367954", "#80568c"]
    fig.text(.06, .92, "Zubieta Dynasty  |  Gemessene Spielerentwicklung", fontsize=18, weight="bold")
    fig.text(.06, .855, f"Feste Ausgangswerte vom 30.03.2027 bis {last:%d.%m.%Y}  ·  FM27 27.1.0+2505117",
             fontsize=11)
    for index, (key, label) in enumerate((("full", "Volle PA"), ("pa_minus_2", "PA−2"), ("pa95", "95 % der PA"))):
        observed = groups["first_seen_by_date"].get(key, {})
        values = list(accumulate(observed.get(day, 0) for day in dates))
        left.step([date.fromisoformat(d) for d in dates], values, where="post", color=colors[index],
                  marker="o", markersize=3, label=label, linewidth=2)
    left.set_title("Erstmals beobachtete Zieltreffer", loc="left", weight="bold")
    left.set_ylabel("Spieler, kumuliert")
    for index, (code, label) in enumerate((("<18", "U18"), ("18-20", "18–20"), ("21-23", "21–23"), ("24-27", "24–27"))):
        means = [quarters[day][code + "/>30"]["mean_delta"] for day in days]
        right.plot(ticks, [0, *means], "o--", markersize=4, linewidth=1.7, color=colors[index], label=label)
    right.set_title("CA bei mehr als 30 Punkten Ausgangslücke", loc="left", weight="bold")
    right.set_ylabel("Mittlere Änderung seit März 2027")
    shown = ticks if len(ticks) <= 6 else ticks[::2] + ([] if ticks[-1] in ticks[::2] else [ticks[-1]])
    for ax in (left, right):
        ax.set_xticks(shown, [d.strftime("%m/%y") for d in shown])
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.22)
        ax.legend(loc="upper left", frameon=False, fontsize=9)
    n = f"{groups['n']:,}".replace(",", ".")
    fig.text(.06, .13, f"Die Treffer stammen von {n} Feldspielern unter der vollen Ausgangs-PA. Bereits erreichte Schwellen sind ausgenommen.", fontsize=9)
    fig.text(.06, .08, "Die Altersgruppen gelten am Ausgangstag. Jeder CA-Mittelwert verwendet die zu diesem Termin messbaren Spielerpaare.", fontsize=9)
    fig.savefig(output, dpi=145)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outcome", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("windows", type=Path, nargs="+")
    args = parser.parse_args()
    plot(args.outcome, args.windows, args.output)

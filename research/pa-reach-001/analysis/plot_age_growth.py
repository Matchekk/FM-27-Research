"""Plot observed Zubieta growth from public aggregates only."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "research/pa-reach-001/manifests/zubieta-associations.json"
TARGET = ROOT / "docs/pa-reach-001/age-growth-58-days.png"


def plot():
    data = json.loads(SOURCE.read_bytes())
    ages = ["<18", "18-20", "21-23", "24-27"]
    gaps = ["0", "1-10", "11-30", ">30"]
    cells = {(c["age"], c["gap"]): c for c in data["age_gap_cells"]}
    values = np.array([[cells[a,g]["mean_delta"] for g in gaps] for a in ages])
    colors = LinearSegmentedColormap.from_list("growth", ["#f4f2e9", "#92c3b3", "#206563"])
    scale = Normalize(min(0, values.min()), values.max())
    fig, ax = plt.subplots(figsize=(8.9, 5.5))
    fig.subplots_adjust(left=.17, right=.97, top=.79, bottom=.20)
    ax.imshow(values, cmap=colors, norm=scale, aspect="auto")
    for i, age in enumerate(ages):
        for j, gap in enumerate(gaps):
            value = values[i,j]
            fg = "#ffffff" if scale(value) > .71 else "#112c30"
            number = f"{value:+.2f}".replace(".", ",").replace("-", "−")
            count = f"{cells[age,gap]['n']:,}".replace(",", ".")
            ax.text(j, i-.09, number, ha="center", va="center", color=fg, fontsize=14, weight="bold")
            ax.text(j, i+.21, f"n = {count}", ha="center", va="center", color=fg, fontsize=9)
    ax.set_xticks(range(4), ["0", "1–10", "11–30", "über 30"])
    ax.set_yticks(range(4), ["unter 18", "18–20", "21–23", "24–27"])
    ax.set_xlabel("Verbleibende PA-Lücke am 31. Januar (PA minus CA)", labelpad=10)
    ax.set_ylabel("Alter am 31. Januar", labelpad=10)
    ax.tick_params(length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for line in (.5, 1.5, 2.5):
        ax.axvline(line, color="white", linewidth=2)
        ax.axhline(line, color="white", linewidth=2)
    fig.text(.04, .92, "Wie viel CA kam in 58 Tagen hinzu?", fontsize=21, weight="bold", color="#112c30")
    fig.text(.04, .86, "Zubieta Dynasty  ·  31. Januar bis 30. März 2027  ·  Feldspieler unter 28", fontsize=11)
    fig.text(.04, .045, "Zellen zeigen die mittlere CA-Veränderung und die Zahl gepaarter Spieler. Eine Karriere, Build 27.1.0+2505117.", fontsize=9)
    fig.savefig(TARGET, dpi=160, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    plot()

"""Deterministic Markdown summaries and exportable figures from verified observations."""
from pathlib import Path

from .native import require
from .stats import estimate, paired_cells


def experiment_report(receipt, jobs, observations, destination):
    config=receipt["config"]
    require(config["stage"] == "technical", "Scientific report needs its preregistered analysis and complete test families")
    values=[]
    for arm in config["design"]["arms"][1:]:
        cells=paired_cells(observations,jobs,arm["id"],config["metrics"]["primary"])
        values.append(dict(arm=arm["id"],mean=sum(sum(c)/len(c) for c in cells)/len(cells),
                           blocks=sum(map(len,cells))))
    path=Path(destination)
    path.parent.mkdir(parents=True,exist_ok=True)
    lines=[f"# {config['experiment_id']} – technischer Smoke-Test", "",
           f"Build `{config['identity']['build']}` · {len(observations)} akzeptierte Matches.", "",
           "**Technische Funktionskontrolle. Keine wissenschaftliche Effektschätzung, keine Taktikauswahl.**", "",
           "| Arm | Vollständige Seed-Blöcke | Deskriptives Δ der Primärgröße |",
           "|---|---:|---:|", *[f"| {r['arm']} | {r['blocks']} | {r['mean']:.6f} |" for r in values], "",
           "Registrierung → neue Seeds → Scheduler → native Eingabeprüfung → vollständige Blöcke → Bericht.",
           "Die Fallzahl dient ausschließlich dem technischen Durchlauf.", ""]
    path.write_text("\n".join(lines),encoding="utf8")
    return values


def benchmark_figure(summary, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    benchmarks=summary["benchmark"]
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":11,"svg.hashsalt":"VALID-002"})
    fig,ax=plt.subplots(figsize=(6.4,3.6),layout="constrained")
    bars=ax.bar([str(r["workers"]) for r in benchmarks],[r["wall_seconds"] for r in benchmarks],color="#256c74",width=.55)
    ax.bar_label(bars,fmt="%.2f s",padding=4)
    ax.set(xlabel="Native Worker",ylabel="Zeit für 8 Matches (s)",ylim=(0,18),
           title="VALID-002 · kleiner technischer Durchsatzcheck")
    ax.spines[["top","right"]].set_visible(False)
    ax.text(0,-.25,"Ein Durchgang je Stufe · einschließlich Start und Audit",transform=ax.transAxes,fontsize=9)
    fig.savefig(path,metadata={"Date":None})
    plt.close(fig)

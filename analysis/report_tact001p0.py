"""Render the completed pilot's frozen estimates; never chooses a tactic."""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import t

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read,require

DATA=ROOT/"data/tact-001-p0"


def number(value,digits=3):
    return f"{value:+.{digits}f}".replace(".",",")


def report():
    summary=read(DATA/"run-summary.json")
    require(summary["scientific_series_complete"],"Incomplete pilot: technical reporting only")
    result=read(DATA/"effects.json")
    primary=result["primary"]
    lo,hi=primary["ci"]
    decision=("Das Primärintervall enthält null; die Richtung der Interaktion bleibt offen." if lo<=0<=hi else
              "Explorativer Hinweis auf eine positive Interaktion; unabhängig zu bestätigen." if primary["mean"]>0 else
              "Explorativer Hinweis auf eine negative Interaktion; unabhängig zu bestätigen.")
    seconds=summary["charged_native_wall_seconds"]
    lines=["# TACT-001-P0 – Ergebnis des Varianzpilots", "", "**14.11.2026 · explorativ · FM27 27.0.1+2503222 · kein Taktiksieger ausgewählt.**", "",
       f"Alle **128 Hauptmatches** und **23 technische Matches** wurden akzeptiert. Die negative Binärprobe wurde wie erwartet mit Code 108 verworfen. 16 unabhängige Hauptseedblöcke, keine Ausfälle, Ausschlüsse, Ersatzseeds oder Retries. Keine Holdoutmatches.","",
       f"Die vorregistrierte Pressing×Linie-Interaktion auf xGD beträgt **{number(primary['mean'])}**, 95-%-t-Intervall **[{number(lo)}; {number(hi)}]**, zweiseitiges p = {primary['p']:.4f}. {decision}","",
       f"Das stratifizierte Seedblock-Bootstrapintervall reicht von {number(primary['bootstrap_ci'][0])} bis {number(primary['bootstrap_ci'][1])}. Es bleibt ein kleiner Varianzpilot und keine Bestätigung einer optimalen 4-2-3-1.","",
       "## Durchführung und technische Integrität", "",
       "Vorregistrierung, Eingaben, Seeds und Analyse wurden in `650a89af4deada6feb4ea1164e3fc963280d90ed` vor dem ersten Match veröffentlicht. Die technische Freigabe wurde in `c9a4353d9ecd61b78bccdadb4a57d613d4e285e3` vor dem ersten Hauptmatch gepusht.","",
       f"Dauerhaft reserviert: 24 technische Versuche und 128 Hauptjobs. Konservativ verrechnete gesamte Child-Wall-Time **{seconds:.3f} / 900 Sekunden**, einschließlich Vorbereitung, Preflights, Audits und erhaltenem Supervisorfehler vor dem ersten Engineaufruf. Maximal vier Worker, 90 Sekunden ohne Fortschritt; kein Neustart zur Budgeterweiterung.","",
       "Alle 16 Eingabezellen durchliefen `rules=game`, feste IP-4-2-3-1/OOP-4-4-1-1, beide Seiten, vollständige native Attribut-/Rollen-/PI-/Anweisungsreadbacks und je Match 1.058 Profilfeldbelege. Die sieben technischen Wiederholungspaare waren exakt gleich. Jeder Hauptlauf endete natürlich mit verifiziertem Seed und passender Identität.","",
       "Engine-SHA256 `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`, Host `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`, Tactics Lab v1114.6. Rohspielmaterial bleibt privat; öffentliche Messfelder und Hashes wurden vor Export erneut geprüft.","",
       "## Primärer Kontrast und Streuung", "",
       "Pro Seite und Seed: `combined − press − line + baseline`. Danach Seitenmittel im Seed und gleiches Gewicht beider Gegner. Der Kontrast ist eine Differenz-von-Differenzen in xGD-Einheiten; eine einzelne Armsteigerung ist etwas anderes.","",
       "| Kontext | Unabhängige Seeds | Mittlere xGD-DoD | Kontrast-SD | Einseitige 95-%-SD-Obergrenze |", "|---|---:|---:|---:|---:|"]
    for name,cell in primary["context"].items():
        lines.append(f"| {name} | {cell['n']} | {number(cell['mean'])} | {cell['sd']:.3f} | {cell['sd_upper95']:.3f} |")
    lines += ["",f"Gepoolte SD innerhalb der Kontexte: **{primary['pooled_within_context_sd']:.3f}**, einseitige 95-%-Obergrenze **{primary['pooled_sd_upper95']:.3f}**. Die gepoolte Grenze setzt Normalität und gemeinsame Varianz voraus; je Kontext stehen nur acht unabhängige Werte zur Verfügung.","",
       "![Explorative Interaktionsintervalle](../docs/tact001p0-interaction.svg)","",
       "Kontextintervalle in der Grafik sind marginale deskriptive t-Intervalle; daraus wurden keine zusätzlichen konfirmatorischen Tests oder Gewinner abgeleitet.","",
       "## Sekundäre Familie", "",
       "Alle Endpunkte verwenden dieselbe vorregistrierte DoD und Blockstruktur. Holm-Korrektur über genau zehn Tests. Intervalle sind marginal und nicht für gleichzeitige Abdeckung korrigiert.","",
       "| Endpunkt | Mittlere DoD | 95-%-t-Intervall | Roh-p | Holm-p |", "|---|---:|---|---:|---:|"]
    for name,cell in result["secondary"].items():
        lines.append(f"| {name} | {number(cell['mean'])} | [{number(cell['ci'][0])}; {number(cell['ci'][1])}] | {cell['p']:.4f} | {cell['p_holm']:.4f} |")
    significant=[name for name,c in result["secondary"].items() if c["reject_holm"]]
    lines += ["",("Nach Holm auffällig: "+", ".join(significant)+". Auch diese Pilotbefunde bleiben explorativ." if significant else "Keiner der zehn Sekundärtests erreicht die Holm-Schwelle von 0,05."),"",
       "## Neue Bestätigungsfallzahlen", "",
       "Die Planung betrifft eine **neue Bestätigung desselben xGD-Interaktionskontrasts** unter gleichgewichteten Kontexten. Zielpower 90 %, zweiseitiges α=0,05, vier Arme und beide Seiten. Ein Block entspricht acht Matches. Es ist keine Punkte-Powerplanung für die Auswahl einer fertigen Taktik.","",
       "| Angenommene wahre DoD | Blöcke pro Kontext / gesamt mit beobachteter SD | Hauptmatches | Blöcke pro Kontext / gesamt mit SD-Obergrenzen | Hauptmatches |", "|---:|---:|---:|---:|---:|"]
    for row in result["confirmation_planning"]:
        a,b=row["observed_sd"],row["upper95_each_sd"]
        lines.append(f"| {row['effect_xgd_did']:.2f} xGD | {a['n_per_scenario']} / {a['total_seed_blocks']} | {a['matches']} | {b['n_per_scenario']} / {b['total_seed_blocks']} | {b['matches']} |")
    lines += ["", "Nichtzentrale t-Näherung mit Satterthwaite-df; die SD-Schätzungen aus acht Seeds pro Kontext sind unsicher. Die zwei individuellen 95-%-SD-Grenzen sind keine gemeinsame 95-%-Grenze. Diese Zahlen sind Planungsszenarien und kein Auftrag, die angegebenen Matches jetzt auszuführen.","",
       "## Grenzen und nächster Vorschlag", "",
       "Synthetische gleich starke Spielerprofile, natürliche Feldspieler in allen Feldpositionen, ein gebündeltes Fixture, zwei Gegnerstilbündel, fester Supplied-Plan-Pfad. Native Identitäten und übriger Fixturekontext werden beim Seitenwechsel nicht in einen identischen Karriereablauf verwandelt. Keine externe Replikation, keine neue Buildverallgemeinerung und keine validierte Karriere-/Live-Coaching-Aussage.","",
       "Der Pilot endet hier. Als nächster separater Auftrag ist ein abgegrenztes, vorregistriertes Präzisionsdesign für denselben Interaktionskontrast sinnvoll: Zielunterschied und gewünschte Intervallbreite festlegen, die instabilen SD-Annahmen prüfen und ein eigenes Rechenbudget veröffentlichen. Die zwei Holdoutprofile bleiben für spätere unabhängige Bestätigung unangetastet. Keine automatische DoE-Großserie, Optimierung oder finale Taktikauswahl.","",
       "[Vorregistrierung](TACT-001-P0-preregistration.md) · [Technische Freigabe](TACT-001-P0-validation.md) · [Manifest](../data/tact-001-p0/manifest.json) · [Hauptmessungen](../data/tact-001-p0/main.jsonl) · [Effekte und Planung](../data/tact-001-p0/effects.json) · [Jobabrechnung](../data/tact-001-p0/job-accounting.jsonl) · [Budget](../data/tact-001-p0/budget.json).",""]
    (ROOT/"experiments/TACT-001-P0-results.md").write_text("\n".join(lines),encoding="utf8")
    labels=[];means=[];errors=[]
    for name,cell in primary["context"].items():
        width=float(t.ppf(.975,7)*cell["sd"]/(8**.5))
        labels.append(name);means.append(cell["mean"]);errors.append(width)
    labels.append("Gleichgewichtetes Mittel")
    means.append(primary["mean"]);errors.append((hi-lo)/2)
    plt.rcParams.update({"font.family":"DejaVu Sans","svg.hashsalt":"TACT-001-P0"})
    fig,ax=plt.subplots(figsize=(7.4,3.8),layout="constrained")
    ax.errorbar(means,range(3),xerr=errors,fmt="o",color="#256c74",capsize=4)
    ax.axvline(0,color="#777777",linewidth=1)
    ax.set(yticks=range(3),yticklabels=labels,xlabel="Pressing × Linie: Differenz-von-Differenzen (xGD)",
           title="TACT-001-P0 · explorativer Varianzpilot")
    ax.invert_yaxis();ax.spines[["top","right"]].set_visible(False)
    ax.text(0,-.25,"95-%-t-Intervalle · je 8 Seeds/Kontext · Seiten im Seed gemittelt",transform=ax.transAxes,fontsize=9)
    path=ROOT/"docs/tact001p0-interaction.svg"
    fig.savefig(path,metadata={"Date":None})
    fig.savefig(ROOT/"local/tact-001-p0/interaction.png",dpi=140)
    plt.close(fig)
    path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf8").splitlines())+"\n",encoding="utf8")
    print("Wrote fixed-order pilot report and interaction figure")


if __name__=="__main__":
    report()

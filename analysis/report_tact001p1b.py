"""Render completed P1B measurements and resource accounting; no native calls."""
from datetime import datetime,timezone
from pathlib import Path
import json
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read,rows,write,require

PUBLIC=ROOT/"data/tact-001-p1b"
LOCAL=ROOT/"local/tact-001-p1b"
LABELS=dict(A="Pressing häufiger",B="Defensivlinie höher",C="Tempo höher",D="Pässe kürzer",E="Angriffsbreite weiter")


def num(v,d=3):return f"{v:+.{d}f}".replace(".",",")
def interval(v,key="ci"):return f"[{num(v[key][0])}; {num(v[key][1])}]"


def report():
    status=read(PUBLIC/"run-summary.json");require(status["scientific_series_complete"],"Incomplete: technical status only")
    r=read(PUBLIC/"effects.json");budget=read(PUBLIC/"budget.json")
    primary=r["primary"];interactions=r["interactions_exploratory"];candidates=r["candidates_exploratory"]
    inputs=read(PUBLIC/"inputs.json")
    write(PUBLIC/"candidates.json",dict(status="exploratory_proposals_not_confirmed",selection_rule="positive both contexts; worst context then equal context gain then ID",source_experiment="TACT-001-P1B",
        candidates=[dict(c,native_options=[dict(code=f["code"],group=f["group"],option_id=f["high_id"] if c["levels"][f["code"]]==1 else f["low_id"],
            native_bit=f["high_bit"] if c["levels"][f["code"]]==1 else 0) for f in inputs["factors"]],
            setup_sha256={h:{s:by[c["design_id"]] for s,by in sides.items()} for h,sides in inputs["setups"].items()},
            fixed_contexts_source="data/tact-001-p1b/inputs.json",independent_confirmation=False) for c in candidates]))
    figures=[]
    for name,family in (("main",primary),("interactions",interactions)):
        fig,ax=plt.subplots(figsize=(9,4.5 if name=="main" else 6),layout="constrained")
        for i,(key,v) in enumerate(family.items()):
            mean=v["mean"];lo,hi=v["ci"]
            if "ci99_bonferroni5" in v:
                a,b=v["ci99_bonferroni5"];ax.plot([a,b],[i,i],color="#abbfcd",lw=5)
            ax.errorbar(mean,i,xerr=[[mean-lo],[hi-mean]],fmt="o",capsize=3,color="#245a81")
        ax.axvline(0,color="#888888",lw=1)
        ax.set_yticks(range(len(family)),[LABELS.get(k,k) for k in family]);ax.invert_yaxis()
        ax.set_xlabel("xGD pro Match; 95-%-t-Intervall"+(" (hell: simultane 99-%-Intervalle)" if name=="main" else "; physische DoD"))
        ax.set_title("TACT-001-P1B · exploratives Screening · 64 unabhängige Seedblöcke")
        ax.spines[["top","right"]].set_visible(False)
        path=ROOT/f"docs/tact001p1b-{name}.png";fig.savefig(path,dpi=160);plt.close(fig);figures.append(path)
    sessions=[]
    for kind in ("technical","main"):
        entries=[s for file in (LOCAL/kind).glob("part-*/sessions.json") for s in read(file)]
        sessions.append(dict(kind=kind,warm_worker_processes=len(entries),completed_matches=sum(s["completed"] for s in entries),
            all_returncodes_zero=all(s["returncode"]==0 for s in entries),all_cleanup_ok=all(s.get("steam_session_cleanup",{}).get("ok") for s in entries)))
    resources=dict(supervised_operations=len(budget["operations"]),
        image_check_processes=len(budget["operations"]),capability_probe_processes=2,
        non_match_native_probe_processes=len(budget["operations"])+2,
        count_basis="One desktop_engine --check-image per supervised NativeLab initialization; one DesktopWarmRunner capability-cache miss per technical/main child; successful warm worker processes counted from every sessions.json. All probes inside supervised budget.",
        sessions=sessions,negative_processes=1,raw_private_bytes=sum(p.stat().st_size for p in LOCAL.rglob("*") if p.is_file()),
        charged_child_wall_seconds=budget["charged_seconds"],elapsed_native_study_window_seconds=budget["elapsed_study_window_seconds"],
        utc_deadline=budget["wall_deadline_utc"],maximum_simultaneous_workers=4,worker_no_progress_timeout_seconds=90)
    write(PUBLIC/"resource-summary.json",resources)
    main_table=["| Faktor | xGD | 95-%-KI | simultanes KI | Holm-p | ≥0,20 und Holm? |","|---|---:|---|---|---:|---|"]
    for n,v in primary.items():
        main_table.append(f"| {n}: {LABELS[n]} | {num(v['mean'])} | {interval(v)} | {interval(v,'ci99_bonferroni5')} | {v['p_holm']:.5f} | {'ja' if v['mean']>=.2 and v['reject_holm'] else 'nein'} |")
    pair_table=["| Paar | physische xGD-DoD | 95-%-KI | Holm-p (10) |","|---|---:|---|---:|"]
    for n,v in interactions.items():pair_table.append(f"| {n} | {num(v['mean'])} | {interval(v)} | {v['p_holm']:.5f} |")
    context_table=["| Faktor | high_press: Mittel / SD | deep_block: Mittel / SD | 95-%-Breite ≤0,30? |","|---|---:|---:|---|"]
    for n,v in primary.items():
        h,d=v["context"]["high_press"],v["context"]["deep_block"]
        context_table.append(f"| {n} | {num(h['mean'])} / {h['sd']:.3f} | {num(d['mean'])} / {d['sd']:.3f} | {'ja' if v['ci'][1]-v['ci'][0]<=.3 else 'nein'} |")
    sec_table=["| Hauptkontrast | Endpunkt | Effekt | 95-%-KI | Holm-p (25) |","|---|---|---:|---|---:|"]
    for n,family in r["secondary"].items():
        for metric,v in family.items():sec_table.append(f"| {n} | {metric} | {num(v['mean'])} | {interval(v)} | {v['p_holm']:.5f} |")
    arms=["| Zelle | high_press xGD / Punkte / GF / GA | deep_block xGD / Punkte / GF / GA |","|---|---|---|"]
    for arm in r["arm_means"]["high_press"]:
        arms.append("| "+arm+" | "+" | ".join(" / ".join(num(r["arm_means"][h][arm][m]) for m in ("xgd","points","gf","ga")) for h in ("high_press","deep_block"))+" |")
    variance=["| Faktor | Beobachtete / prognostizierte Blockvarianz H | Beobachtete / prognostizierte Blockvarianz D | Größter LOO-Einfluss |","|---|---:|---:|---:|"]
    for n,v in r["variance_transfer"].items():variance.append(f"| {n} | {v['high_press']['ratio']:.2f} | {v['deep_block']['ratio']:.2f} | {primary[n]['leave_one_out']['max_abs_change']:.3f} |")
    candidate_lines=[]
    for c in candidates:
        signs=" ".join(n+("+" if lev==1 else "−") for n,lev in c["levels"].items())
        candidate_lines.append(f"- **{c['design_id']} ({signs})**: xGD-Abstand zu D00 gegen high_press {num(c['context_gains']['high_press'])}, gegen deep_block {num(c['context_gains']['deep_block'])}, gleichgewichtet {num(c['equal_context_gain'])}. Schlechterer Kontext {num(c['worst_context_gain'])}.")
        points={h:r["arm_means"][h][c["design_id"]]["points"]-r["arm_means"][h]["D00"]["points"] for h in ("high_press","deep_block")}
        candidate_lines.append(f"  Tatsächlicher Punkteabstand rein deskriptiv: high_press {num(points['high_press'])}, deep_block {num(points['deep_block'])}, gleichgewichtet {num(sum(points.values())/2)} Punkte pro Match. Kein unabhängiger Nachweis und kein Auswahlkriterium.")
    if not candidate_lines:candidate_lines=["Keine der 15 alternativen geprüften Zellen erfüllt die Positivität in beiden Kontexten; kein Kandidatenvorschlag."]
    content=["# TACT-001-P1B – Ergebnis des Fünffaktor-Screenings","",
        "**14.11.2026 · FM27 27.0.1+2503222 · explorative Discovery · keine Siegerbestätigung.**","",
        f"Alle **2.048 Hauptmatches** und **72 technischen Vollmatches** akzeptiert; eine erwartete Negativabweisung. **64 vollständige unabhängige Seedblöcke**,32 je Gegner. Keine Ausfälle, Ausschlüsse, Retries, Ersatzseeds oder Holdoutmatches. Der Auftrag endet nach diesem Screening.","",
        "**Keiner der fünf Haupteffekte, zehn explorativen Zweifachkontraste oder25 Sekundärtests erreicht die jeweilige Holm-Schwelle.** Die Hauptschätzungen liegen zwischen −0,007 und +0,063 xGD. Alle marginalen95-%-Intervallbreiten liegen zwischen0,150 und0,170 und damit unter dem vorab gewünschten Maximum0,30. Auch sämtliche simultanen Hauptintervalle enthalten null; ihre positiven Obergrenzen liegen unter0,20. Dies begrenzt große positive Faktor-Mittelwerte im getesteten Halbfraction-Kontext, beweist aber keine allgemeine Wirkungslosigkeit oder formale Äquivalenz.","",
        "## Vorregistrierung und Designintegrität","",
        f"Vorregistrierung/Code/Inputs/Seeds vor jedem Prüfmatch gepusht in `{status['preregistration_commit']}`; technische Freigabe vor dem Hauptstart in `9831b2a91bc7e76a1fdf955196589c9014748f43`. Alle64 nativen Zellen und acht exakte Wiederholungen bestanden, neue C/D/E-Bits47/3/51 zurückgelesen. Die negative Binärprobe lieferte Exit108.","",
        "Explizit **E=−ABCD**, D00 all-standard und binäridentisch zur P0-Baseline. `fractional_design(...,fraction=-1)` wird durch Matrix/Vertrag/Binärdifferenzen/native Readbacks/Analyse geprüft; historischer Default+1 blieb unverändert. Keine stillschweigende Umstellung. Hauptkontraste X/8 (high-minus-low), Paar-DoDs XiXj/4. Die negative Hälfte identifiziert Haupt- und Zweifachspalten getrennt voneinander, aber aliasiert sie negativ mit Vierfach-/Dreifachinteraktionen.","",
        "## Fünf Haupteffekte","",
        *main_table,"",
        "Marginale95-%-t-Intervalle; simultane Bonferroni99-%-Intervalle je Hauptkontrast, gemeinsame nominelle Abdeckung mindestens95 % unter den Modellannahmen. Holm über genau5 Tests. Seitenmittel im Seed, beide Gegner je½; Welch-Satterthwaite-df und20.000 stratifizierte vollständige Seedblock-Bootstrapziehungen. Bootstrapintervalle, Roh-p und alle Kontrast-SDs stehen im Effektarchiv. 2.048 Matches sind keine2.048 unabhängigen Replikate.","",
        "![Haupteffekte](../docs/tact001p1b-main.png)","",
        "Die Spalte ≥0,20/Holm ist die eingefrorene Regel für vorläufige Einstellungshinweise; sie bestätigt weder ein zusammengestelltes Paket noch eine universelle Verbesserung. Ein signifikanter Effekt unter0,20 ist kein praktisch ausreichender Einstellungshinweis. Ein unklares Intervall belegt keine Abwesenheit eines Effekts.","",
        "## Gegnerrobustheit und erreichte Präzision","",*context_table,"",
        "Die zwei Gegner sind feste Stilbündel und keine Zufallsstichprobe aller FM-Taktiken. Unterschiede der Kontextmittel sind deskriptiv; daraus werden keine nachträglichen weiteren Haupttests. Gegenläufige Richtungen begrenzen die Übertragbarkeit des Mittelwerts. Seitenmittel/-SD/Kovarianzen und volle16×16-Armkovarianzmatrizen sind im JSON vollständig erhalten.","",
        "## Zehn explorative Zweifachinteraktionen","",*pair_table,"",
        "Separate Holm10-Familie, physische Differenz-von-Differenzen. Höhere Interaktionen können diese Aliaskontraste verursachen. Kein Nachweis ihrer Abwesenheit und keine automatische neue2×2-/Foldover-Serie.","",
        "Der größte positive Paar-Schätzwert ist B×C (Linie×Tempo): +0,177 xGD-DoD, marginales95-%-KI [+0,038; +0,315], aber Holm-p=0,134. Das marginale Intervall allein ist kein korrigierter Nachweis. B, D und E haben deskriptiv unterschiedliche Vorzeichen zwischen Gegnern; auch das begründet keine nachträglichen Kontexttests.","",
        "![Interaktionen](../docs/tact001p1b-interactions.png)","",
        "## Tatsächliche Resultate und sekundäre Familie","",
        "Punkte3/1/0 aus dem tatsächlichen Endstand; GF/GA nicht durch xG ersetzt. Separate vorregistrierte Holm25-Familie, alle25 Kontraste vollständig berichtet. Positive GA bedeutet mehr Gegentore. Diese Werte sind jeweilige Faktor-Hauptkontraste, keine Bestätigung der ausgewählten Zellen.","",*sec_table,"",
        "Alle16 Zellmittel je Gegner, rein deskriptiv, jeweils64 tatsächliche Matches pro Zelle und Gegner:","",*arms,"",
        "Native Schüsse/SOT/Ballbesitz bleiben deskriptive Plausibilitätsendpunkte ohne zusätzliche Leistungs-p-Werte. Alle Endstände und Messwerte stehen in `main.jsonl`; alle technischen Messungen getrennt. xGD ist ein Screeningmaß und erfasst Abschlussqualität sowie den tatsächlichen Punktgewinn nicht vollständig.","",
        "## Varianztransfer, Abhängigkeit und Seed-Einfluss","",*variance,"",
        "Verhältnisse beziehen sich auf die P1A-Annahme τ²/4 für jeden neuen Hauptkontrast; Wert1 entspräche deren Varianzprognose. Die Planungspower94,6 % war bedingt, keine nachträglich gemessene Power. Relevant sind die jetzt tatsächlich erreichten Intervalle. LOO entfernt je einen Seed nur in der Sensitivität, behält die Kontextgewichte½ und ändert keine Hauptergebnisse. Vollständige960 xGD-Blockkontraste erlauben unabhängige Rekonstruktion.","",
        "## Höchstens zwei explorative Vorschläge","",*candidate_lines,"",
        "Angewandt wurde ausschließlich die eingefrorene Auswahlregel: positiver xGD-Abstand in beiden Kontexten; Sortierung nach kleinerem Kontextabstand, dann gleichgewichtetem Abstand, dann Design-ID. Die Auswahl verwendet dieselben Discoverydaten und unterliegt Winner's Curse. Deshalb keine konfirmatorischen Gewinnerintervalle und keine Behauptung einer optimalen Taktik. Faktor+ bedeutet bei D ausdrücklich kürzere Pässe. Alle übrigen Rollen, Phasen, PI, Profile, Standards und das Management bleiben die kontrollierten P0-Eingaben. [Konkrete Kandidaten mit Optionen und allen vier Setup-Hashes](../data/tact-001-p1b/candidates.json).","",
        "## Ressourcen, Vollständigkeit und Grenzen","",
        f"Kumulierte beaufsichtigte Child-Wall-Time **{budget['charged_seconds']:.3f}/2.400 Sekunden**, Zeitfenster vom ersten nativen Vorbereitungsstart bis Hauptabschluss **{budget['elapsed_study_window_seconds']:.3f}/2.400 Sekunden**. Unveränderte Deadline `{budget['wall_deadline_utc']}`, innerhalb eingehalten. Maximal4 Worker,90 s ohne Fortschritt, keine Budgetneustarts. Drei beaufsichtigte Phasen (prepare/technical/main). Alle2.121 Matchversuchsplätze abgerechnet:2.120 akzeptierte Vollmatches plus eine erwartete Abweisung, keine unbegonnenen Jobs.","",
        f"Zusätzliche native Prüfprozesse: {resources['non_match_native_probe_processes']} (drei --check-image, zwei Capabilities-Abfragen), alle innerhalb derselben Zeitreservation. Warmworkerprozesse laut vollständigen Sessionbelegen: Technik {sessions[0]['warm_worker_processes']}, Hauptserie {sessions[1]['warm_worker_processes']}. Dies sind wiederverwendete Hosts, keine zusätzlichen Matches. Private Rohartefakte etwa {resources['raw_private_bytes']/1024**2:.1f} MiB, unter4 GiB. [Ressourcenabrechnung](../data/tact-001-p1b/resource-summary.json).", "",
        "Grenzen: synthetische gleich starke, positionsübergreifend geeignete Profile; ein gebündeltes Fixture, nur zwei Gegner und feste Managementpolitik; Halbfraction-Aliase; explorative Kandidatenselektion. Keine Aussage über echte Kaderstreuung, neue Builds, andere Mannschaftsstärken, Karriereverläufe oder Live-Coaching. Karriere-PKM bleiben gesperrt. Die bestehenden Holdoutprofile und Holdoutseeds bleiben unbenutzt.","",
        "Nächster Vorschlag ausschließlich separat: maximal einen jetzt eingefrorenen Kandidaten gegen D00 an neuen Seeds und unbenutzten Gegner-/Stärkeprofilen bestätigen, tatsächliche Punkte primär und eigene Relevanz-/Powerplanung. Vor realen Karriere-Replays den Adapter separat validieren. Hier keine weitere Simulation, Optimierung oder automatische Bestätigung.","",
        "## Reproduktion und veröffentlichte Belege","",
        "```powershell", ".venv/Scripts/python.exe analysis/analyse_tact001p1b.py", ".venv/Scripts/python.exe analysis/verify_tact001p1b.py", ".venv/Scripts/python.exe -m unittest discover -s tests -v", "```","",
        "Der unabhängige Verifier liest ausschließlich öffentliche Messungen und den Vertrag, ohne Analyse-/Runnerimporte:40 Effekt-/t-/Bootstrapintervalle, fünf simultane Intervalle, Holm5/10/25,960 Blockkontraste, Kandidatenregel und vollständige Jobabrechnung. Die124 geschützten historischen Forschungsdateien werden gegen den Ausgangscommit gehasht. Rohspielmaterial bleibt privat; Export nur über die vorregistrierte Feld-Whitelist.","",
        "[Vorregistrierung](TACT-001-P1B-preregistration.md) · [technischer Gate](TACT-001-P1B-validation.md) · [Daten/Provenienz](../data/tact-001-p1b/README.md) · [Effekte](../data/tact-001-p1b/effects.json) · [Rohmessungen](../data/tact-001-p1b/main.jsonl) · [Budget](../data/tact-001-p1b/budget.json).",""]
    text="\n".join(content)
    text=re.sub(r"\b(Alle|alle|genau|je|Maximal|maximal|mindestens|höchstens|sowie|aus|über|und|pro|jeweils|vor|nach|plus|etwa|keine|Keine|unter|zwischen|oder|Die)(?=\d)",r"\1 ",text)
    for before,after in (("**,32","**, 32"),("Marginale95","Marginale 95"),("marginalen95","marginalen 95"),("marginales95","marginales 95"),("Bonferroni99","Bonferroni 99"),("je½","je ½"),("volle16","volle 16"),("neue2×2","neue 2×2"),("Punkte3/1/0","Punkte 3/1/0"),("Holm25","Holm-25"),("Holm10","Holm-10"),("Holm5/10/25","Holm-5/10/25"),("Wert1","Wert 1"),("Planungspower94","Planungspower 94"),("Kontextgewichte½","Kontextgewichte ½"),("Vollständige960","Vollständige 960"),("Worker,90","Worker, 90"),("abgerechnet:2.120","abgerechnet: 2.120"),("Runnerimporte:40","Runnerimporte: 40"),("25,960","25, 960"),("Maximum0,30","Maximum 0,30"),("Bits47/3/51","Bits 47/3/51"),("Exit108","Exit 108"),("Default+1","Default +1")):
        text=text.replace(before,after)
    (ROOT/"experiments/TACT-001-P1B-results.md").write_text(text,encoding="utf8")
    print("Rendered completed P1B report, figures and resource accounting.")


if __name__=="__main__":report()

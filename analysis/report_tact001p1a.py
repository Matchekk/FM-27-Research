"""Render checked offline P1A numbers; never initializes the native laboratory."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/tact-001-p1a"
LABELS={"press_isolated":"Pressing isoliert","line_isolated":"Linie isoliert",
        "combined":"Beide Änderungen","interaction":"Interaktion (DoD)",
        "press_marginal":"Pressing marginal","line_marginal":"Linie marginal"}


def render():
    a=json.loads((DATA/"exploratory-effects.json").read_text(encoding="utf8"))
    d=json.loads((DATA/"design-comparison.json").read_text(encoding="utf8"))
    effects=a["contrasts"]
    fig,ax=plt.subplots(figsize=(9,4.5),layout="constrained")
    for i,(name,label) in enumerate(LABELS.items()):
        v=effects[name]["xgd"];mu=v["mean"];lo,hi=v["ci95"]
        ax.errorbar(mu,i,xerr=[[mu-lo],[hi-mu]],fmt="o",color="#245a81",capsize=4)
    ax.axvline(0,color="#999999",lw=1);ax.set_yticks(range(6),LABELS.values());ax.invert_yaxis()
    ax.set_xlabel("xGD pro Match; marginales 95-%-t-Intervall")
    ax.set_title("TACT-001-P1A · explorative Wiederverwendung von 16 P0-Seedblöcken")
    ax.spines[["top","right"]].set_visible(False)
    fig.savefig(ROOT/"docs/tact001p1a-effects.png",dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,4.4),layout="constrained")
    for k in ("1.0","2.0","4.0"):
        plans=d["doe_forecasts"]
        ax.plot([p["budget_matches"] for p in plans],
                [p["variance_transfer_sensitivity"][k]["power"] for p in plans],"o-",label=f"Varianz × {float(k):g}")
    ax.axhline(.9,color="#888888",ls="--",label="Ziel: 90 %")
    ax.set_ylim(0,1.03);ax.set_xticks([512,1024,2048]);ax.set_xlabel("Neue Hauptmatches (nur Planung, keine Ausführung)")
    ax.set_ylabel("Bedingte Power für 0,20 xGD, α = 0,01")
    ax.set_title("16-Punkt-Resolution V · unbekannte Varianz neuer Faktoren")
    ax.legend(loc="lower right");ax.spines[["top","right"]].set_visible(False)
    fig.savefig(ROOT/"docs/tact001p1a-power.png",dpi=160);plt.close(fig)
    table=[];context=[];side=[];outcomes=[];dependence=[];influence=[]
    for name,label in LABELS.items():
        v=effects[name]["xgd"];lo,hi=v["ci95"]
        table.append(f"| {label} | {v['mean']:+.3f} | [{lo:+.3f}; {hi:+.3f}] | {v['p']:.4f} |")
        cells=v["context"]
        context.append(f"| {label} | {cells['high_press']['mean']:+.3f} / {cells['high_press']['sd']:.3f} | {cells['deep_block']['mean']:+.3f} / {cells['deep_block']['sd']:.3f} |")
        influence.append(f"| {label} | [{v['leave_one_out']['mean_range'][0]:+.3f}; {v['leave_one_out']['mean_range'][1]:+.3f}] | {v['leave_one_out']['max_abs_change']:.3f} |")
        for h,z in cells.items():
            side.append(f"| {label}, {h} | {z['home_mean']:+.3f} / {z['home_sd']:.3f} | {z['away_mean']:+.3f} / {z['away_sd']:.3f} |")
            q=a["dependence"][name][h]
            dependence.append(f"| {label}, {h} | {q['side_correlation']:+.3f} | {q['paired_to_independent_side_variance']:.3f} | {q['paired_to_independent_arm_variance']:.3f} |")
        outcomes.append(f"| {label} | "+" | ".join(f"{effects[name][m]['mean']:+.3f} [{effects[name][m]['ci95'][0]:+.3f}; {effects[name][m]['ci95'][1]:+.3f}]" for m in ("gf","ga","gd","points"))+" |")
    report="""# TACT-001-P1A – unabhängige Präzisionsanalyse von P0

**14.11.2026 · ausschließlich offline · alle neuen Analysen explorativ.**

Die ursprüngliche Interaktion ist reproduziert. P0 liefert weder einen
Taktiksieger noch einen Nachweis fehlender Interaktion. Für weitere Entdeckung
sind größere, praktisch relevante Haupteffekte und mehrere gemeinsam untersuchte
Faktoren sinnvoller als die präzise Bestätigung einer sehr kleinen DoD.
Die endgültige Designentscheidung und ihre Kosten stehen im
[Designvergleich](../docs/TACT-001-P1A-design.md); der
[Folgeauftrag](TACT-001-P1B-order.md) ist hiermit **nicht gestartet**.

## Daten, Provenienz und Reproduktion

Quelle: unveränderte [P0-Messungen](../data/tact-001-p0/main.jsonl) und sämtliche
öffentlichen P0-Eingaben, Technikbelege, Jobabrechnungen und Ergebnisdateien,
Stand `873799a4eb4f233d2b894a579e53e409f64140fb`. 128 gültige Hauptmatches,
16 unabhängige Seedblöcke (acht je Gegner), vier Arme und zwei Seiten je Block.
Alle 152 damaligen Versuchsplätze sind abgerechnet: 128 Hauptmatches,
23 technische Matches, eine erwartete Negativabweisung; keine Ausschlüsse/Retry.
Diese technischen Matches gehen nicht in die Leistungsanalyse ein.

Historischer Build: FM27 `27.0.1+2503222`, Tactics Lab `v1114.6`, Commit
`91f2eba57fac0b7fbd3dff616056907e3ce461be`. Die Engine-SHA256 ist
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Der lokale DLL-Dateihash und die Dateiversion wurden in P1A lesend abgeglichen;
kein nativer Start und keine neue technische Freigabe. Vollständige historische
Host-/Fixture-/Ressourcenidentität: [P0-Manifest](../data/tact-001-p0/manifest.json).

`analyse_tact001p1a.py` liest die Rohzeilen direkt und baut die Identitäts-, Setup-,
Seed-, Seiten- und Armzuordnung erneut auf. Es importiert weder den alten
Analysepfad noch den nativen Runner. Der Test berechnet alle 30 neuen
Effekt-/Intervallschätzungen zusätzlich mit skalarer Arithmetik nach.
Der ursprüngliche unabhängige P0-Verifier prüft weiterhin alle elf damaligen
Kontraste, Bootstrapintervalle, Holm, SD-Grenzen und sechs Fallzahlminima.

```powershell
.venv/Scripts/python.exe analysis/verify_tact001p0.py
.venv/Scripts/python.exe analysis/analyse_tact001p1a.py
.venv/Scripts/python.exe analysis/report_tact001p1a.py
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

Neue Ausgaben: [Effekte](../data/tact-001-p1a/exploratory-effects.json),
[Designprognosen](../data/tact-001-p1a/design-comparison.json),
[Seed-Einfluss](../data/tact-001-p1a/seed-influence.jsonl),
[Quellprüfsummen](../data/tact-001-p1a/source-manifest.json).
Python 3.12.10, NumPy 2.3.5, SciPy 1.16.3, Matplotlib 3.10.7;
vorhandene `requirements-lock.txt`, keine neue Abhängigkeit.
**Neue native Matches: 0; neue Seedreservierungen: 0; Holdoutzugriffe für Leistung: 0.**

## Schätzgrößen und unabhängige Einheiten

Armreihenfolge B=baseline, P=press, L=line, C=combined:

| Kontrast | Koeffizienten B/P/L/C | Bedeutung |
|---|---|---|
| Pressing isoliert | −1, +1, 0, 0 | Pressing bei Standardlinie |
| Linie isoliert | −1, 0, +1, 0 | Linie bei Standardpressing |
| Beide Änderungen | −1, 0, 0, +1 | konkretes Paket gegen Baseline |
| Interaktion | +1, −1, −1, +1 | Differenz-von-Differenzen |
| Pressing marginal | −½, +½, −½, +½ | Mittel über beide Linien |
| Linie marginal | −½, −½, +½, +½ | Mittel über beide Pressingstufen |

Erst Kontrast pro Seite, dann Seitenmittel im Seed, dann Gegnergewicht je ½.
Standardfehler² = ¼·(s_H²/n_H+s_D²/n_D); Satterthwaite-df,
zweiseitiges t-Intervall. Seedblöcke sind zwischen Kontexten unabhängig.
128 Matches sind **keine 128 unabhängigen Replikate** dieser Kontraste.
Bootstrap: 20.000 Ziehungen kompletter Blöcke, getrennt je Gegner,
deterministischer Analyse-RNG `2026111401`. Das ist kein neuer FM-Matchseed.
P1A-Bootstrapziehungen unterscheiden sich bewusst vom eingefrorenen P0-RNG;
die alten Bootstrapgrenzen werden separat unverändert verifiziert.

Primärreproduktion: +0,0197562342 xGD, SE 0,353394354, df 9,798918,
95-%-KI [−0,769851195; +0,809363664], p=0,956541550.
SD_H=1,818398035 und SD_D=0,830560536. Keine materielle Abweichung von P0.

## Explorative Effekte auf xGD

| Vergleich | Mittel | 95-%-KI | Roh-p |
|---|---:|---|---:|
"""+"\n".join(table)+"""

![Explorative Effekte](../docs/tact001p1a-effects.png)

Alle Intervalle sind marginal; die sechs Vergleiche sind abhängig. Zusätzlich
Holm über die vollständig berichtete explorative Familie von 6 Kontrasten ×
5 Endpunkten (xGD, GF, GA, GD, Punkte) = 30 Tests, ohne positiven Nachweis.
Diese neue Familie ändert die ursprüngliche P0-Familie nicht.
Kein nachträglicher Primärtest und keine Bestätigungsbehauptung.

## Gegner- und Seitenstreuung

| Vergleich | high_press: Mittel / SD | deep_block: Mittel / SD |
|---|---:|---:|
"""+"\n".join(context)+"""

Die Interaktion streut gegen hohes Pressing etwa 4,79-mal so stark in Varianz.
Beim isolierten Pressing ist dagegen deep_block etwas variabler.
Es gibt daher keine für jeden Kontrast optimale Gegnerallokation.
Für die Interaktions-SD lauten die zweiseitigen 95-%-Normalmodellintervalle
[1,202; 3,701] bzw. [0,549; 1,690]. Das zeigt die erhebliche Unsicherheit
aus je acht Seeds; Normalität selbst ist damit nicht belegt.

| Vergleich und Kontext | Heim: Mittel / SD | Auswärts: Mittel / SD |
|---|---:|---:|
"""+"\n".join(side)+"""

Die Seiten sind feste native Fixtureplätze einschließlich Trägeridentität,
kein kausal isolierter Heimvorteil. Die Vorzeichenunterschiede und SDs rechtfertigen
kein leistungsabhängiges Weglassen einer Seite.

## Paarungsabhängigkeit

Die Tabelle vergleicht die gemessene gepaarte Varianz mit der aus den
Randvarianzen berechneten **kontrafaktischen** Varianz bei unabhängigen Seeds.
Ein Wert unter eins begünstigt die Paarung; ein Wert über eins benachteiligt sie.
Die hypothetischen unabhängigen Läufe wurden nicht ausgeführt.

| Vergleich und Kontext | Korr. Heim/Auswärts | Varianzverhältnis Seitenpaarung | Verhältnis Armpaarung |
|---|---:|---:|---:|
"""+"\n".join(dependence)+"""

Für Seiten gilt Var((D_home+D_away)/2)=(V_home+V_away+2Cov)/4.
Für Arme gilt Var(c'Y)=c'Σc; der unabhängige Gegenwert ist Σ c_j²Σ_jj.
Die vollständigen 4×4-Armkovarianz-/Korrelationsmatrizen stehen im JSON.
Gemeinsame Seeds garantieren weder dieselben Ereignisse noch positive Kovarianz
zwischen Ergebnissen verschiedener Taktiken. Eine generelle CRN-Ersparnis wäre
mit diesen Daten unbegründet. Ein späterer unabhängiger Paarungsversuch müsste
selbst vorregistriert werden; P1A ändert keine Seedpolitik eines laufenden Versuchs.

## Einfluss einzelner Seeds und robuste Sensitivität

Leave-one-out entfernt jeweils nur einen Seed im betroffenen Kontext und lässt
beide Zielgewichte bei ½. Keine Zeile wird aus dem eigentlichen Ergebnis entfernt.

| Vergleich | Bereich der 16 Leave-one-out-Mittel | Größte absolute Verschiebung |
|---|---|---:|
"""+"\n".join(influence)+"""

Die Interaktion kann allein durch Weglassen eines Blocks zwischen −0,187 und
+0,194 liegen. Beim isolierten Linieneffekt reicht der Bereich über null.
Diese Empfindlichkeit ist ein Argument für neue Replikation, kein Ausschlussgrund.
Alle 96 xGD-Sensitivitätsläufe einschließlich Seedkennungen und Intervalle
sind öffentlich. Kontextmediane und 20-%-getrimmte Mittel stehen im JSON:
beispielsweise Linie −0,068 bzw. +0,078 gegenüber arithmetisch +0,113.
Sie schätzen andere Lagegrößen; kleinere Streuung wäre kein Beweis für höhere
Präzision des unveränderten mittleren Leistungseffekts.

Ein lineares Modell mit 16 Blockinterzepten und kontextspezifischen
Seiten-/P-/L-/P×L-Termen liefert dieselben Punktschätzungen.
Es erzeugt keine neuen unabhängigen Einheiten. Inferenz bleibt auf vollständigen
Seedkontrasten, statt mit naiven Matchresiduen und n=128.

## Tatsächliche Tore und Punkte

Alle Effekte pro Match, jeweils Mittel [marginales 95-%-KI]. GA positiv bedeutet
mehr Gegentore; GD=GF−GA. Punkte sind 3/1/0 aus dem tatsächlichen Endstand.

| Vergleich | GF | GA | GD | Punkte |
|---|---|---|---|---|
"""+"\n".join(outcomes)+"""

Beispiel Interaktion: xGD +0,020, Tordifferenz −0,031, Punkte −0,188.
Das ist bei diesen Intervallen kein belastbarer Widerspruch. Im deep_block
korrelieren die acht Interaktionskontraste xGD/GD nur mit 0,223 und xGD/Punkten
mit 0,228; gegen high_press mit 0,745 bzw. 0,590. Die vollständigen
3×3-Matrizen (Reihenfolge xGD, GD, Punkte) sind im JSON gespeichert.
Die isolierten Pressingkontraste haben SE_xGD=0,238 versus SE_GD≈0,424;
xGD ist hier ein effizienter Screeningendpunkt. Es misst weder Abschlussqualität
vollständig noch tatsächliche Punkte. Für finale Kandidaten sind neue
Endstand-/Punktevergleiche und deren eigene Powerplanung erforderlich.

## Konsequenz

Eine weniger verrauschte Schätzgröße hilft nur, wenn sie die Forschungsfrage
beantwortet. Ein Zweiarmvergleich für ein konkretes Paket ersetzt keine
Interaktionsschätzung; ein marginaler Haupteffekt ersetzt keinen Vorteil einer
bestimmten vollständigen Taktik. Der folgende Designvergleich behält diese
Unterschiede und die Kosten jedes vollständigen Blocks ausdrücklich bei.
"""
    (ROOT/"experiments/TACT-001-P1A-analysis.md").write_text(report,encoding="utf8")
    print("Rendered offline exploratory report and two scientific figures.")


if __name__=="__main__":render()

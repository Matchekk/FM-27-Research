# ATTR-001 – Attribut-Screening

**Stand 2026-11-06 · Explorativ · FM27 27.0.0+2493426**

Die Ausgangsfrage war, welche Einzelattribute in derselben Aufstellung die xG-Differenz eines ganzen Matches am stärksten verändern. Das Lab-Standardfixture stellt zwei feste Teams und Taktiken bereit. Die behandelte Mannschaft spielte zuhause. Die Baseline setzte die 16 untersuchten Attribute bei denselben zehn Feldspielern auf Rohwert 60 (Anzeige 12). Je Intervention wechselte genau eines dieser Attribute auf Rohwert 80 (Anzeige 16). Torwart, übrige Eingaben und Gegner blieben innerhalb jedes Seed-Paars gleich. Das [Manifest](../data/matches/manifest.json) enthält Attribut-IDs, Setup-Hashes, betroffene Kaderindizes und die vollständigen Seed-Listen.

Mit Ball spielte das behandelte Team 4-3-3 mit einem Sechser. Der Gegner stand im 4-2-3-1. Gegen den Ball standen beide im 4-4-2. Beide Teams verwendeten im Standardfixture Mentalitätswert 4. Die aktiven Kader umfassten 23 und 26 Plätze.

Pro Attribut lagen 40 Seed-Paare vor. 40 Baselines und 640 Interventionsläufe ergeben 680 vollständige Matches. Jeder Seed teilt seine Baseline über die 16 Interventionen. Die 640 Kontraste bilden daher keine 640 unabhängigen Baseline-Stichproben. Der lokale Import prüfte für jeden Lauf den effektiven Seed, den nativen Readback, den natürlichen Abschluss, den Rohlog-Hash und die Teamstatistik. Der [Validierungsbericht](VALID-001-adapter.md) beschreibt die Grenzen des Nachweises. Alle 680 vorgesehenen Matches gingen in die Analyse ein.

Die Zielgröße war die Differenz des teambezogenen xG-Saldos zwischen Intervention und Baseline. Die 95-%-Perzentilintervalle resampeln ganze Seed-Paare. Zweiseitige Vorzeichen-Tests prüfen den Nulleffekt unter Vorzeichenaustauschbarkeit. Die Korrektur nach Benjamini–Hochberg (BH) umfasst die 16 Attribute pro Zielgröße. Benjamini–Yekutieli (BY) ergänzt die Auswertung als Sensitivitätsprüfung bei Abhängigkeit. Das Manifest enthält keine vorab definierte kleinste praktisch relevante Effektgröße.

| Attribut | Δ xGD | 95-%-KI | BH-q |
|---|---:|---:|---:|
| Pace | +0,288 | [0,029; 0,568] | 0,4042 |
| Acceleration | +0,274 | [−0,021; 0,560] | 0,4042 |
| JumpingReach | +0,239 | [−0,017; 0,491] | 0,4042 |
| Dribbling | +0,198 | [−0,083; 0,480] | 0,6073 |
| Agility | +0,161 | [−0,091; 0,413] | 0,6073 |
| Finishing | +0,152 | [−0,122; 0,427] | 0,6073 |
| Passing | +0,144 | [−0,095; 0,393] | 0,6073 |
| Marking | +0,122 | [−0,153; 0,405] | 0,6494 |
| Strength | +0,119 | [−0,152; 0,390] | 0,6494 |
| Positioning | +0,082 | [−0,206; 0,363] | 0,8430 |
| Stamina | +0,047 | [−0,226; 0,317] | 0,8675 |
| Tackling | +0,042 | [−0,205; 0,316] | 0,8675 |
| WorkRate | +0,028 | [−0,250; 0,314] | 0,9012 |
| Anticipation | +0,015 | [−0,275; 0,333] | 0,9252 |
| Decisions | −0,062 | [−0,344; 0,241] | 0,8675 |
| OffTheBall | −0,143 | [−0,405; 0,123] | 0,6073 |

Alle BH-q-Werte lagen über 0,05. Die fünf höchsten Mittelwerte qualifizierten sich nach der im Manifest festgehaltenen Regel für die Hauptreplikation. Die Auswahl ist damit ein Screening-Rang. WorkRate belegte Platz 13 und hat nur die 40 Screening-Paare.

Die beiden älteren Serien umfassen zusätzlich 132 und 96 Matches auf je 12 bzw. 24 Seeds. Ihre publizierten Paarstatistiken stimmen mit den nativen Ergebnissen überein. Sie verwendeten eine Ausgangskonfiguration mit zehn standardisierten Attributen und abweichendem Baseline-Hash. Sie bleiben ein historischer Vergleich außerhalb der 2.504 Matches und der neuen Testfamilien. Einzelmessungen und Rechenabgleich sind separat archiviert. [Historische Daten](../data/historical/) · [Historischer Abgleich](../data/historical/audit.json)

[Matchmessungen](../data/matches/screening.jsonl) · [Effekte aller Zielgrößen](../data/matches/effects.json) · [Auswertungscode](../analysis/verify_matches.py)

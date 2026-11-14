# FM27 Meta-Score v0.1 – explorativer positionsspezifischer Scout-Index

**Stand 14.11.2026 · Status: HYPOTHESEN-/SCOUTINGMODELL, KEINE VALIDIERTE LEISTUNGSPROGNOSE.**
[Maschinenlesbare Gewichte](../research/meta_score_v01_weights.json) · [Direkt ausführbarer Rechner](../analysis/meta_score_v01.py) · [Quellenatlas](FM27_EXTERNAL_STUDY_ATLAS_2026-11-14.md).

## Ziel und Einheit

Die erste Version übersetzt die veröffentlichten **+1-Attributpunkt-Effekte auf die Tordifferenz über 38 Spiele** in einen von 0 bis 100 normierten **innerhalb derselben Positionsgruppe** vergleichbaren Scouting-Index. Das ist weder ein echtes Match-Outcome-Modell noch eine Siegwahrscheinlichkeit. Ein Score von 70 bedeutet einen gewichteten Mittelwert von etwa 14,3 auf der FM-Skala 1–20, **nicht** 70% Siegwahrscheinlichkeit, 70% Leistung oder eine ligaunabhängige Qualitätsstufe. Unterschiedliche Positions-Scores können nicht als gleich große Teambeiträge verglichen werden.

**Quellen:**
- [Fm-Match-Lab Study 13b (immutable Commit e92cf14, 14.11.2026)](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/13b-value-by-position-random.md): 50.000 berichtete Gegenpress-Matches, zwei Stürmer, synthetische gleich starke Kader. GD-Effektfelder für neun ausgewählte Outfield-Attribute und Tore-verhindert-Koeffizienten für GK. Eine angekündigte Catenaccio-Erweiterung war am Snapshot noch nicht abgeschlossen.
- [Purity / FM-Arena (Nov. 2026)](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/): 200.000 berichtete Matches, Brentford, 3-4-2-1 mit **einem** Stürmer. 50.000 Random-Konfigurationen × 4 Seeds, Position×Attribut-Regression auf GD. Torwart nicht getestet.

Diese Studien stammen von **zwei verschiedenen Autoren**, sind aber noch keine extern validierte vollständige Karrierevorhersage; verschiedene Kader, Taktiken und Anzahl Stürmer erklären mögliche Unterschiede. Autoren-Zahlen/Rohdaten sind hier nicht unabhängig nachgerechnet.

## Konstruktion

Für jede Outfield-Position p und jedes der zehn unten genannten Attribute j:
1. Positiven berichteten GD-Koeffizienten je Quelle in derselben Position innerhalb der Quelle auf 100% normieren: `q_mac[p,j] = beta_mac[p,j] / sum_j(beta_mac[p,j])`; analog Purity.
2. Beide **relativen Gewichtsprofile** gleichgewichtet mitteln: `q[p,j] = 0.5*q_mac[p,j] + 0.5*q_purity[p,j]`. **50:50 ist eine bewusst gewählte Ensembleentscheidung**, keine inverse-Varianz-Meta-Analyse oder präregistrierte optimale Mischung.
3. Für die Nutzerformel mit Largest-Remainder auf ganzzahlige Prozentgewichte `w[p,j]` summierend zu exakt 100 runden. Deren leicht gerundete Werte sind der veröffentlichte v0.1 Score. Rohkoeffizienten und ungerundete Quellanteile stehen im JSON.

**Deklarierte Lücken:** Mac 13b druckt keinen separaten GD-Koeffizienten für Dribbling in seiner Kurz-GD-Tabelle (xPts wird berichtet). Daher wird für die Mac-Normalisierung **vorläufig der Purity-GD-Dribblingwert als Proxy geborgt**, nicht als unabhängige Mac-Beobachtung gezählt. Die beiden Tests unterscheiden außerdem Wide-AM und zentrale AM, sowie FB und WB – folglich sind diese Profile **Positionscluster**, keine genauen Einzelrollenmodelle. CM/8 ist ohne direkte Studie als **60%-DM/40%-AM** extrapoliert und damit besonders vorläufig.

Für GK stammen die fünf Gewichte aus **Mac 13b beobachteten verringerten Gegentoren**, nicht aus xG. Dieser spezielle Torwartindex hat daher nur eine experimental-unterstützende Quellenfamilie.

```text
Score(position, player) = SUM_i(weight_percent[position,i] * (attribute_i - 1)) / 19
```

- Alle sichtbaren Attribute müssen als Werte von 1 bis 20 vorliegen; optionales Potenzial/CA/PA, Form, Marktwert, beidfüßige Eignung oder Alter nicht hineinfälschen.
- Der Score bleibt bei einer 1 überall 0 und bei einer 20 überall 100.
- Die Gewichte sind lokale **Ranggewichte**. Der 0–100-Wert ist keine aus Spieleffekten geeichte Punktedifferenz.
- Keinen globalen Effekt einer gesamten 10er-Kader-Aufwertung als kausalen Effekt für einen einzigen Spieler übernehmen.

## Positionsgewichte (Prozentpunkte, jede Spalte summiert 100)

| Attribut | IV/CB | AV/WB | DM/6 | ZM/8 **Proxy** | OM/Flügel | ST |
|---|---:|---:|---:|---:|---:|---:|
| Antritt (Acceleration) | 21 | 18 | 24 | 21 | 17 | 19 |
| Tempo (Pace) | 15 | 22 | 16 | 18 | 21 | 21 |
| Sprunghöhe (Jumping Reach) | 22 | 6 | 9 | 9 | 9 | 16 |
| Ausdauer (Stamina) | 10 | 15 | 13 | 12 | 11 | 7 |
| Antizipation (Anticipation) | 8 | 9 | 5 | 6 | 8 | 7 |
| Balance (Balance) | 8 | 5 | 3 | 4 | 3 | 7 |
| Stärke (Strength) | 7 | 7 | 11 | 11 | 12 | 6 |
| Abschluss (Finishing) | 1 | 2 | 4 | 5 | 6 | 8 |
| Konzentration (Concentration) | 6 | 7 | 7 | 6 | 4 | 5 |
| Dribbling (Dribbling) | 2 | 9 | 8 | 8 | 9 | 4 |
| **SUMME** | **100** | **100** | **100** | **100** | **100** | **100** |

**Zuordnung:** CB = DC/IV; FB = DL/DR/WB; DM = defensives Mittelfeld; CM = zentrales Mittelfeld ohne direkte Bestätigung; AM = AMC/AML/AMR (hohe Rollen-/Kontextunsicherheit); ST = Sturm. Die Gruppen unterscheiden nicht zwischen Stürmerpaar und einzelnem Stürmer oder unterschiedlichen OOP-Rollen.

### Torwart

| Attribut | Gewicht | Ursprünglicher Mac-13b-Effekt (+1 Punkt, pro 38 Matches) |
|---|---:|---:|
| Beweglichkeit (Agility) | **43%** | 0,93 Gegentore weniger |
| Reflexe (Reflexes) | **35%** | 0,76 Gegentore weniger |
| Lufthoheit (Aerial Reach) | 10% | 0,23 Gegentore weniger |
| Antritt (Acceleration) | 7% | 0,15 Gegentore weniger |
| Fangsicherheit (Handling) | 5% | 0,11 Gegentore weniger |
| **SUMME** | **100%** | |

**Lufthoheit (Aerial Reach) ist NICHT Strafraumbeherrschung (Command of Area).** Positioning/One on Ones/Command of Area erhalten in v0.1 keine Gewichte, weil die zitierte randomisierte Torwartstudie für sie keine vergleichbar robuste marginale Tordifferenzwirkung zeigte. Das bedeutet nicht, dass diese Fähigkeiten universell wirkungslos sind. Die beobachtungsbasierte 335-GK-Studie in FM-Player-Analyzer berichtet abweichende GK-Prioritäten; wegen starker potenzieller Kader-/Team-Konfundierung wurde sie nicht als experimenteller Koeffizient vermischt.

## Graubereich / Entscheidungsregel (HEURISTIK, KEIN 95%-KI)

Für einen konkreten Feldspieler werden außerdem zwei getrennte **kontextgebundene Scores** berechnet, einer aus Mac- und einer aus Purity-Gewichtungen, ohne ein Match zu starten:

```text
band_low  = max(0, min(score_mac, score_purity) - 3)
band_high = min(100, max(score_mac, score_purity) + 3)
```

Bei GK mangels eines zweiten randomisierten GK-Modells **±5 Punkte** um den Score als rein pragmatischen Unsicherheitspuffer. Diese `±3/±5` sind **nicht** aus den Studien als korrekt kalibrierte Fehlergrenzen geschätzt. Die Bänder bilden nur Quellen-/Modellunterschiede und einen willkürlichen Vorsichtspuffer ab; sie ersetzen keine posterioren oder frequentistischen Vorhersageintervalle.

**Vergleich zweier Spieler derselben Positionsgruppe:**
- Überlappen sich die beiden Graubereiche: **GRAY_OVERLAP** – kein harter Scoutingentscheid alleine aus dem Score.
- Sind die Bereiche getrennt: das höher bewertete Profil ist **innerhalb dieser Modelle** robuster, nicht schon als realer Matchsieger nachgewiesen.
- Spieler verschiedener Positionen nicht durch direktes 0–100-Ranking priorisieren. Innerhalb einer repräsentativen Liga-/Positionskohorte können später empirische P20/P50/P80-Schwellen bestimmt werden; **globale Grenzwerte für „gut/schlecht“ sind nicht validiert**.
- Ein Score von 73 statt 71 bedeutet noch keinen gesicherten realen Vorteil. Selbst nicht überlappende Heuristik-Bänder sind keine Leistungswahrscheinlichkeiten.

**Beispiele mit fiktiven Werten:**
- ST: Acc 14, Pace 16, JR 15, Stamina 13, Anticipation 12, Balance 13, Strength 13, Finishing 14, Concentration 11, Dribbling 13 → Score **68,68**, Mac/Purity-Modell etwa **68,62/68,54** → Heuristikbereich ca. **65,54–71,62**.
- GK: Agility 16, Reflexes 15, Aerial Reach 13, Acceleration 11, Handling 13 → **72,89** → Heuristikbereich **67,89–77,89**.

## Nicht mit Spielerqualität vermischen

- **Match Condition ≠ Stamina ≠ Match Sharpness.** Mac Study 05 zeigt starke **gesamte Mannschafts-Startzustandseffekte** für 80/90% Condition sowie 50/75% Sharpness. Diese sind keine kalibrierten Einzelspieler-Punktabzüge. Deshalb **separates Readiness-Flag** (Condition, Sharpness, Verletzung/Sperre, Frische); nicht einen fiktiven Multiplikator auf den dauerhaften Attributscore anwenden.
- **Positionseignung / Fuß / OOP / Rolle / Taktik** getrennt als Warnungen anzeigen. Komplexitäts- und Familiarity-Gates nicht aus dem Score ableiten.
- **CA/PA, Trainingsentwicklung, Alter, Gehalt und Vertragslaufzeit** sind andere Entscheidungen als dieser reine Spielleistungsindex.
- Scoutingangaben mit Werteintervallen sollten zuerst über das Attributintervall bewertet werden, nicht unbemerkt als fixer Mittelwert in den Score geraten.
- 200.000 fremde Matches liefern nicht automatisch reale Vorhersagepräzision für eine bestimmte Karriere. Nächste methodisch notwendige Stufe ist ein gehaltenes **Spieler-/Kader- und Fixture-Set**, getrennt nach Position/Rolle; tatsächliche Punkte/GD/Gegentore statt nur xGD.

## Nutzung im Repository

```bash
python analysis/meta_score_v01.py --position ST --attributes-file player.json
python analysis/meta_score_v01.py --position GK --attributes-file keeper.json
python analysis/meta_score_v01.py --position ST --attributes-file player_a.json --compare-file player_b.json
python -m unittest tests/test_meta_score_v01.py
```

Attributschlüssel im JSON sind die englischen `snake_case`-Namen aus der [Gewichtedatei](../research/meta_score_v01_weights.json). Der Rechner greift auf keine FM-Spielinstallation/Save/Engine zu und führt keine Studienläufe aus.

**Nächster wissenschaftlicher Schritt:** Mit unabhängigen Matchdaten validieren, ob der v0.1-Score bessere reale Spielausgänge vorhersagt als (1) simples Attributmittel, (2) vorhandene FM27 Benchmarkprofile und (3) reines CA; danach die Gewichte/Unsicherheitsgrenzen neu kalibrieren. Bis dahin keine automatisierten Transferentscheidungen auf Basis dieses Modells.

# CA-Effizienz – Quellenprüfung

Status15.11.: **tatsächliche marginale CA-Kosten unbekannt**.
Die neu gefundene [öffentliche Tabelle](https://github.com/jamiebolden/fm-scoring/blob/b5928ba2b9aba3c4c40a8f32118401eafb6f4c99/docs/ca_costs_fm27.csv)
ist eine positionsabhängige Modellquelle; eine exakte FM27-Kostenfunktion,
validierte Ableitungen8→9/17→18 und unabhängige Profil-Holdouts fehlen.
Angezeigte CA, RCA, Tabellengewichte und marginaler CA-Verbrauch bleiben getrennt.
PD-ROLE-001 identifiziert keine CA-Kosten.

## Tatsächlich ausgeführte Auswertung A1

Die unveränderlich referenzierte CSV wurde vollständig eingelesen und auf
Duplikate, fehlende Werte und positive ganzzahlige Einträge geprüft.
**221 Tabellenzellen,10Positionsgruppen,20–23 gelistete Attribute/Gruppe.**
Gewichtssummen: GK107, CB91, DL/DR78, DM88, WBL/WBR75, CM90,
ML/MR78, AMC88, AML/AMR88, ST107. Diese Werte sind eine deskriptive
Dokumentenanalyse, **keine Stichprobe von221Spielern oder Interventionen**.
[Messausgabe](../../data/player-development-001-ca/reference-audit.json).

Die quellenseitige Beschriftung „CA cost“ reicht nicht für eine Einheit in
echten CA-Punkten. Ein Tabellenwert10 kann ein Gewicht einer normalisierten
Berechnung sein. Keine Formel mit Intercept, Normierung, Rundung, Rohskalen,
Fuß-/Positionsaggregation oder Levelabhängigkeit ist in der knappen
Tabellendokumentation nachgewiesen. Das Audit allein widerlegt auch keine
lineare Funktion. Alle folgenden Größen bleiben **unbekannt**:

- tatsächlicher CA-Mehrverbrauch8→9 gegenüber17→18;
- Fußkosten und Kosten zusätzlicher Positionsratings;
- Level-/Positionswechselwirkungen, GK-Sonderbehandlung;
- MAE/Bias/Kalibrierung und Unsicherheitsintervalle gegen unabhängige Profile.

Die Tabelle enthält beispielsweise beim ST relative Einträge Acceleration10,
Pace7, Jumping Reach5, Finishing8. Fehlende Zellen sind **nicht** kostenlos.
Es liegen0geeignete unabhängige reale Validierungsprofile und kein separater
Holdout vor. Öffentliche kuratierte Spielerdaten mit ungesichertem Build und
unklarer CA-Provenienz wurden nicht als Goldstandard importiert. Ein
1.000-Spieler-Fit oder eine rekonstruierte Enginefunktion wird nicht behauptet.

## A2: ausführbarer, begrenzter Szenariooptimierer

`analysis/ca_efficiency001.py` löst einen beschränkten ganzzahligen
Optimierungsfall exakt per dynamischer Programmierung:

`max Σ proxy_benefit[j]·increment[j]`

unter `Σ reference_weight[j]·increment[j] ≤ reference_budget` sowie
expliziten Attributobergrenzen. Kosten/Leistungen sind in diesem Szenario
linear und separabel; dies sind Annahmen, keine geschätzten Naturgesetze.
Missing,0Kosten,NaN,Duplikate und ungleiche Variablenmengen werden abgewiesen.
Kleine synthetische Fälle wurden gegen vollständige Enumeration geprüft;
synthetische Implementierungstests sind keine reale Modellvalidierung.

Illustration mit vier ST-Attributen, alle Start12 und Grenze20, Budget20
**Referenzeinheiten**: v0.1-Zählergewichte19/21/16/8 für Antritt/Tempo/JR/
Abschluss ergeben in diesem Modell vier JR-Schritte und sonst0. Das sind
64Zählereinheiten beziehungsweise64/19=3,368v0.1-Scorepunkte. **Nicht20CA,
nicht0,15xGD, kein realer Spieler und kein experimenteller Leistungsgewinn.**
Ohne Kostenschranke wäre Tempo pro Attributschritt im v0.1 höher gewichtet;
mit diesen Tabellengewichten ist JR günstiger. Das zeigt die Bedeutung des
Nenners für ein Optimierungsproblem, nicht dessen wahre FM27-Lösung.

Die Originaltabelle bleibt als externe Quelle referenziert, nicht als
eigener Datensatz umetikettiert. Reproduktion nach lokalem Bezug der
referenzierten CSV mit SHA256
`b42727041a0779bc6bcc76272b0ae67ee323338f5bbdf1a348abd51769f08180`:

```powershell
.venv/Scripts/python.exe analysis/ca_efficiency001.py <lokale-ca_costs_fm27.csv>
.venv/Scripts/python.exe -m unittest tests.test_ca_efficiency001 -v
```

**Antwort auf „welches Attribut pro CA am besten?“: weiterhin unbekannt.**
Ein CA-Effizienzindex mit echter Einheit wird erst nach unabhängiger
Kostenidentifikation veröffentlicht. Dieser Szenariorechner ersetzt ihn nicht.

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

## PD-CA-001: zusätzliche empirische Exportdiagnose

Nach Abschluss des Tabellenaudits wurde ein öffentlicher GK-Export mit109CA-
Profilen gefunden. Vor eigener Anpassung/Auswertung in
[8f26064](https://github.com/Matchekk/FM-27-Research/commit/8f26064aa60a9a5b62756cd4cf76d11f86fad1a6)
[separat protokolliert](../../experiments/PD-CA-001.md), dann tatsächlich
ausgewertet. Das ergänzt die oben dokumentierten **0unabhängig
goldvalidierten** Profile um109extern bereitgestellte Exportzeilen;
die Herkunftsunsicherheit wird dadurch nicht aufgehoben.

Alle109Zeilen zulässig, keine Duplikate/Missing/Ausschlüsse.80Trainingsspieler
und29diagnostische Holdoutspieler nach festem Identitätshash, keine Spieler-
überschneidung. Ein gewichteter linearer SummenproxyW und eine OLS-BaselineU
auf dem einfachen Mittel derselben22Attribute haben jeweils zwei Parameter.
Zusätzlich konstantes Trainings-CA-MittelC.

| Modell | Holdout-MAE | Holdout-RMSE | Bias (Prognose−Export) |
|---|---:|---:|---:|
| W: positionsgewichtete Summe | 1,606 | 2,010 | +0,845 |
| U: gleiches Attributset, ungewichtet | 4,630 | 5,525 | +1,364 |
| C: konstantes Trainingsmittel | 11,368 | 14,354 | −3,156 |

Primärer deskriptiver Vergleich **MAE(W)−MAE(U)=−3,024 exportierte CA-Punkte**,
bedingtes95-%-Spielerbootstrapintervall **[−4,139; −1,908]**. W-MAE-Intervall
[1,183;2,064], W-Biasintervall[+0,178;+1,506].20.000gepaarte Bootstrapzüge,
bedingt auf dieses Trainingssample und diese Aufteilung. Es fehlen Save-/
Vereinscluster und Trainingsunsicherheit; kein populationsweiter Präzisionsnachweis.
Holdout-Kalibrierung `ExportCA = −0,188 + 0,991764·Prognose` ist ein
deskriptiver Diagnosefit auf29Profilen, kein Beleg repräsentativer Kalibrierung.

TrainingsmodellW: `ExportCA_hat = −99,465075 + 0,165178632·Σ(w_j·a_j)`.
Trainings-RMSE2,646. OLS zusätzlich mit getrenntem NumPy-Löser nachgerechnet,
maximaler Koeffizientenabstand unter4×10⁻¹⁴. Tatsächliche Ergebnisse,
Split-/Quellenhashes und alle Baselines:
[profile-diagnostic.json](../../data/player-development-001-ca/profile-diagnostic.json).

**Modellableitung, nicht gemessener Grenzpreis:** Bei GK entspräche ein
zusätzlicher Agility-/Reflexes-Punkt im linearen Proxy jeweils1,321 exportierten
CA-Punkten; Acceleration0,991, Pace0,496, Decisions1,652. Für8→9 und17→18
ist das im Modell derselbe Betrag **per Annahme**. Eine Nichtlinearitäts-
oder reale Interventionsaussage folgt daraus nicht.

**Grenzen:** Der Quellautor hat dieselben109Profile bereits für sein Modell
verwendet; unser nachträglicher Split ist keine neue unabhängige Bestätigungs-
kohorte. Quelle nennt FM27, aber exakter Build, Save, UI-Gold und Clubs sind
nicht unabhängig verifiziert. Kein Multi-Save-Holdout, kein1.000er-Korpus,
keine Füße/zusätzlichen Positionen modelliert, keine Feldspielerextrapolation.
Der Datensatz erklärt exportierte CA-Zahlen, nicht tatsächlichen Verbrauch
oder Matchleistung. Der klare Nutzen gegenüberU gilt für diesen Export;
ein besserer Meta-Score oder echter CA-Effizienzindex ist damit nicht bewiesen.
Export-CA umfasst15–118; der diagnostische Holdout41–109. Ein Beispiel mit
130CA oder einem Elitekeeper läge bereits außerhalb dieser beobachteten Spanne.

Reproduktion: Originaldateien über die unveränderlichen Links im Protokoll
lokal beziehen und ihre veröffentlichten SHA256 prüfen; keine Profile ins
öffentliche Forschungsrepo kopieren:

```powershell
.venv/Scripts/python.exe -m analysis.ca_profile001 <hidden-export.csv> <ca_costs_fm27.csv> --output <diagnose.json>
.venv/Scripts/python.exe -m unittest tests.test_ca_profile001 -v
```

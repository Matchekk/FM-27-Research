# CA-002 – kontrollierte RCA-Modelldifferenzen und externe Exportdiagnose

15.11.2026. Vor Ausführung der nachstehenden Matrix und Exportauswertung festgelegt.
Kein FM-Engineexperiment, keine tatsächlichen CA-Kosten, keine Seedreservierung.

## Neuheit und Wahl nach Machbarkeitsprüfung

Atlas, maschinenlesbarer Index und FINDINGS einschließlich PD-CA-001 geprüft.
Überlappung: MAC-20, PD-CA-001, fm-scoring und neue Quelle
`PD2-SHLK-RCA`. Entscheidung **UNCERTAIN_SOURCE**: Die neue ausführbare
RCA-Funktion besitzt mehr Struktur als die alte Gewichtssumme, ihre ursprüngliche
Herleitung betrifft jedoch den FM26-Pregameeditor. FM27-Goldreadback fehlt.
MAC-20 verändert nominale CA und beantwortet diese Frage nicht.
Kein Wiederholen der alten OLS-Anpassung als neue Studie.

Gewählter Weg: D mit kontrolliertem **Software-Modellaudit**. Ohne verifizierten
FM27-Editorpfad darf A nicht als echte Kostenmessung bezeichnet werden. B braucht
einen verlässlichen Karriereexecutor; C geeignete unabhängige Längsschnittdaten.
Keine Reparatur eines Saveparsers und keine zusätzlichen Native-Matches.

## Eingefrorene Quelle und Hypothese

[Originalfunktion](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/apps/desktop/src/lib/ca.ts),
Funktion `estimateCaExact`, unverändert lokal über Node aufrufen. Der Name
`Exact` ist eine Quellenbezeichnung, keine eigene Genauigkeitsbestätigung.

Primäre Diagnosefrage: Ist die endliche Differenz der **ganzzahligen Modell-RCA**
für einen sichtbaren Attributschritt zwischen 8→9, 12→13 und 17→18 konstant?
Keine Populationshypothese, p-Werte oder aus künstlichen Profilen gebootstrappten
Konfidenzintervalle. Vollständige deterministische Matrix statt Pseudoreplikaten.

## Matrix und Kontrolle

Zehn Positionsfamilien GK, DL, DC, WBL, DM, ML, MC, AML, AMC, STC.
Je eine natürliche Hauptposition 20, übrige 0. Alle 40 von der Funktion
gewichteten Attribute zunächst Rohwert 60 (= konstruierter Anzeigewert 12).
Nur das Zielattribut erhält zunächst 40/60/85 und anschließend +5.
Rohwert=5×Anzeigewert ist hier eine explizite **Szenariodefinition**;
kein unabhängig abgenommenes FM27-UI-Mapping.

Attribute: Acceleration, Pace, Jumping Reach, Stamina, Anticipation, Finishing,
Strength, Agility, Reflexes. Drei Fußkonstellationen Rohwerte links/rechts
5/100, 50/100, 100/100. Zwei Positionsprofile: nur Hauptposition oder
zusätzlich MC20 (bei MC zusätzlich DC20). Zusammen **1.620 eindeutige
Attributinterventionen**. Alters-/Persönlichkeitsfelder sind keine Funktionsinputs;
fehlende Abhängigkeit im Modell beweist keine biologische/Engine-Unabhängigkeit.

Vollständiges Request vor/nach hashen; tiefe Kopie, genau ein Attributfeld
verändern; übrige Attribute, Füße und Positionen identisch. A/A zweimal pro
Ausgangsprofil, Originalhash nach Lauf identisch. Auch Null- und negative
Modelldifferenzen vollständig erhalten. Funktionsergebnis null/ungültig oder
Mutation stoppt die Matrix, keine stillen Ausschlüsse oder Ersatzprofile.

Sekundäre Diagnosen: Level-, Positions-, Fuß- und Zusatzpositionsabhängigkeit;
Rundung/Sättigung und interne Iterationszahl sichtbar. Zusätzliche einmalige
Fuß-/Positions-Gesamtdifferenzen im All-12-Profil dürfen deskriptiv berichtet
werden. Keine Optimierung mit vermeintlich kostenlosen Attributen.

## Reale Exportdiagnose, ausdrücklich bereits gesehene Daten

Unveränderter öffentlicher ScoutReporter-Export aus PD-CA-001, SHA256
`31c1efc4da93fb23ec380b8a6e6c3b5956fb3290e5a51bc39d836bb1fc42f3b9`.
Keine neue unabhängige Kohorte behaupten. Alle 109 GK mit vollständigen
40 Attributen und numerischen Füßen 1..20 verwenden, skalieren ×5, GK20,
andere Positionen unbekannt und für dieses Szenario 0. Nicht als beobachtete
Nullpositionen ausgeben. Identitäten/Zeilen bleiben im ignorierten Cache.
Fehlende/nichtnumerische Werte dokumentieren; kein Nullersatz.

**Kein Fit**: unveränderten neuen RCA-Schätzer gegen exportierte CA prüfen.
MAE, RMSE, Bias, Maximalfehler und Anteil innerhalb ±1/±3/±5 für alle 109
und die alten festen 29 Diagnoseprofile. Alter gewichteter Proxy nur mit
eingefrorenen Trainingskoeffizienten aus PD-CA-001 als Referenz. 20.000 gepaarte
Spieler-Bootstrapzüge, RNG2026111502, für MAE-Differenz auf diesen 29.
Intervalle bedingt auf Export/alten Split, ohne Savecluster oder Modellunsicherheit;
kein neuer konfirmatorischer Holdout und keine RCA-Goldvalidierung.

Reale Export-CA15–118; keine Elite-, Feldspieler-, Entwicklungs- oder
Matchleistungsvalidierung. Der neue Schätzer kann schlechter sein. Alle
Misserfolge bleiben erhalten; keine nachträgliche Fuß-/Positionstuningrunde.

## Ausgaben und technische Reproduktion

`analysis/ca_costs002.py`, `analysis/run_rca002.mjs`,
`data/player-development-002-ca/{manifest,summary,export-diagnostic}.json`,
`model-interventions.jsonl`. Öffentliche Modellprofile sind vollständig
konstruiert und enthalten keine privaten Spieler. Original-Quellcode wird
nicht in das Forschungsarchiv kopiert. Tools/Quellhash im Manifest.
Gezielte Checks für unveränderte Requests, Vollständigkeit, Hashes,
Fehlerbehandlung und unabhängige Nachrechnung der Summaries.

## Struktureller Nachtrag vor Ergebnisansicht

Der erste Lauf erreichte den Vollständigkeitscheck, der die geplante Matrix
wegen identischer Request-Hashes zurückwies. DC20+MC20 und MC20+DC20 sind
unter AUTO identische Eingaben: 81 der 1.620 Zellen sind Beschriftungsaliasse.
Alle 1.620 ursprünglichen Messzeilen bleiben erhalten; die 81 Wiederholungen
werden explizit markiert und ergeben **1.539 einzigartige Interventionen**.
Keine Zahlenanalyse war vor diesem Nachtrag erzeugt oder betrachtet worden.
Primäre Leveldiagnose nutzt nur einzigartige Requests; beide beschrifteten
Basisprofile bleiben für Tabellen erhalten. Der Fehler ist ein gestoppter
Auswertungsschritt, kein fehlgeschlagener FM-Lauf. Kein Ersatzdatensatz.

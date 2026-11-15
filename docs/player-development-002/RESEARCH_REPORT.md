# Spielerentwicklung002 – Ergebnisse vom 15.11.2026

**Neue Originaldaten nachgerechnet, neuer RCA-Rechner kontrolliert vermessen;
tatsächliche FM27-CA-Grenzkosten weiterhin nicht identifiziert.**
Keine weiteren Matchstudien, keine geöffnete oder fortgeschriebene Karriere.
Ausgangscommit20ebc48, nach Fetch sauber und identisch mit origin/main.

## Was wir zusätzlich wissen

1. **CA-Zuwachs und gezielte Attributentwicklung sind verschieden.** Die erstmals
   maschinenlesbar nachgerechnete Harvestgreen-Originalmappe enthält51Pläne×37
   Endpunkte=1.887numerische Zellen,0Missing/Formeln. Im vorab benannten
   Vergleich Plan46−38 stehen **+2,10CA** neben **−0,15Antritt, −0,20Tempo,
   −0,30Ausdauer, +0,65Antizipation**. Das ist eine Quellen-Nachrechnung,
   keine eigene kausale Replikation. Karrierezahl, Streuung und Build fehlen;
   PA130/150 widerspricht sich. [Training mit Zellbelegen](TRAINING_EXPERIMENT.md).
2. **Die neue vollständige RCA-Rekonstruktion liefert keine konstanten Preise.**
   1.539einzigartige kontrollierte Softwareinterventionen, zehn Positionsfamilien,
   neun Attribute, drei Ausgangsniveaus, drei Fuß- und zwei Positionsprofile.
   **339/513Leveltripel** unterscheiden sich; ganzzahlige Differenzen0–4.
   Beispielsweise ST-Antritt8→9/12→13/17→18: **3/2/3Modell-RCA**, GK-Beweglichkeit
   **2/1/2**. Rundung und Verteilungskorrektur sind enthalten. Das sind konstruierte
   Profile, keine1.539FM-Spieler oder echten Editorinterventionen.
   [Alle Kostenantworten und vollständige Tabelle](CA_COSTS.md).
3. **Ein unabhängiger Exportvergleich scheitert an konkreten Messfeldern.**
   Alle109bekannten GK-Profile haben qualitative Fußangaben statt der benötigten
   Rohwerte. Kein belegtes Mapping: **109unzulässige Inputs,0Berechnungen,
   MAE=null**. Keine Fußmittelwerte erfunden und kein erneuter OLS-Fit.
4. **Ein neuer externer Karrierebeleg zeigt Profilrückanpassung nach Edit.**
   Beim selben Ausgangsspieler werden sechs auf100gesetzte Rohattribute nach
   33Tagen mit CA110 als85, mit CA150 als96 berichtet. Differenz+11je Attribut;
   alter Savebuild27.0.0+2486695, ein Spieler/ein Cluster, keine unabhängige
   Bestätigung und kein Trainingseffekt. [Quellenextraktion](../../research/playerdev002-editor-evidence.json).

## Machbarkeit und tatsächliche Entscheidung

| Weg | Ergebnis des begrenzten Zugangschecks | Entscheidung |
|---|---|---|
| A echte CA-/Editor-RCA-Kosten | Kein unabhängig validierter nativer/UI-Rechenpfad; vollständiger externer Rechner gefunden | Nur MODEL_RCA-Audit |
| B kontrollierter Karrierepilot | Wegwerfkopien autorisiert; Executor, Fokusreadback und unabhängige Startcluster fehlen |0gestarteteArme |
| C PA-Prognose | Neue Historienexportwerkzeuge gefunden,0geeignete unabhängige Saisonverläufe | Kein Modellfit |
| D Originaldaten/Quellenanalyse | Original-Trainingsworkbook sowie externe RCA-Funktion und Editorbericht zugänglich | Ausgeführt und abgeschlossen |

Die Quellenentscheidung ist im [vorher gepushten CA-Vertrag](../../experiments/CA-002-model-diagnostic.md)
und [vor numerischer Extraktion geschriebenen Quellenplan](../../experiments/TRAIN-003-source-audit.md)
festgehalten. Wahl nach erstem Zugangscheck; kein stundenlanger Parserreparaturversuch.
Keine Pflicht zur individuellen Teilnahme als pauschales ITT-Hindernis übernommen.
Es fehlen für den eigenen Pilot andere notwendige Durchführungsnachweise.

## Unsicherheit und Reichweite

Quelltabellen enthalten Mittelwerte ohne Streuung/Clusterzahl. Deshalb keine
KIs, p-Werte oder bestätigte Trainingsrangliste. Das deterministische RCA-Gitter
hat keine Stichprobenunsicherheit innerhalb des Gitters; sein FM27-Modellfehler
ist unbekannt. Originalherleitung FM26; Autor berichtet700FM27-Speicherprüfungen
ohne Rohreadbacks/Build. Der öffentliche48k-Test vergleicht gegen gespeichertes
CA, nicht Editor-RCA. `UNCERTAIN_SOURCE` bleibt. [Zugangsaudit](CA_ACCESS_AUDIT.md).

PA-Ausschöpfungsquoten, seriöse Einjahresprognosen, tatsächlicher Nutzen proCA,
der beste Trainingsplan und ein besserer Scouting-Score bleiben **unbekannt**.
Der eingefrorene v0.1-Index steigt im Plan46−38-Vergleich für ST rechnerisch nur
um0,0553Punkte, falls Quelleneinheiten UI-Attributpunkten entsprechen. Kein
Matcherfolgsgewinn daraus abgeleitet. [Modellfolgen](MODEL_IMPLICATIONS.md),
[PA-Auswertung](PA_ANALYSIS.md), [maximal drei nächste Versuche](NEXT_STEPS.md).

## Reproduktion, Fehler und Veröffentlichung

Python3.12.10, NumPy2.3.5, SciPy1.16.3, fmsave0.9.0, Nodev25.9.0.
Installierte DLL erneut gelesen: FileVersion27.0.1,
ProductVersion27.0.1+2503222, SHA2568c6971ce…e340. Keine Engineaufrufe;
dieser lokale Build ist **nicht** der nachgewiesene Build der Trainingsmappe.

Zwei gestoppte Auswertungsschritte vollständig vermerkt: strukturelle
DC/MC-Requestaliasse, anschließend qualitative Füße.81Aliaszeilen bleiben
sichtbar und zählen nicht als neue Beobachtungen. [Ausführungsabrechnung](../../data/player-development-002-ca/execution-ledger.json).
Ein separater Fachagent rekonstruierte sämtliche3.240Requests und spielte
die Originalfunktion unabhängig vom Analysewrapper exakt nach;0Mismatches.
Auch die Trainingstabelle wurde mit getrenntem Parser nachgerechnet.
Das ist Software-/Quellenreview, keine unabhängige FM-Studienreplikation.

```powershell
# Quellen lokal beziehen; vor Ausführung SHA256 prüfen (Skripte prüfen erneut).
.venv/Scripts/python.exe -m analysis.ca_costs002 <ca.ts> --profiles <hidden-export.csv> --output <ausgabeordner>
.venv/Scripts/python.exe -m analysis.audit_training003_source <training.xlsx> --output <audit.json>
.venv/Scripts/python.exe -m analysis.playerdev002_implications
.venv/Scripts/python.exe -m unittest tests.test_ca_costs002 tests.test_training003_source -v
```

Manifest/Quellhashes, kompakte Messungen und Code öffentlich; Originalworkbook,
Spielerprofile, Saves und Spielressourcen nicht veröffentlicht. Tests, exakte
CI und Integration werden in [publication.json](publication.json) gebunden.

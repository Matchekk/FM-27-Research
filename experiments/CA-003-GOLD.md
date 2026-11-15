# CA-003-GOLD – unabhängige Editor-RCA

15.11.2026. Neuer Vertrag; **NOT_STARTED_ACCESS_BLOCKED**. Kein Wiederöffnen
von CA-002 oder einer terminalen Studie. Dies ist eine technische Übergabe,
keine Vorregistrierung einer bereits ausführbaren Hauptserie.

## Frage und Messung

Hypothese: Für identische vollständige Profile entspricht MODEL_RCA dem
unabhängig berechneten EDITOR_RCA. Primär: Anteil exakter Übereinstimmungen
über alle zulässigen Vor-/Nachmessungen. Ein reproduzierbarer Gegenbeleg
widerlegt universelle Exaktheit; Übereinstimmung validiert nur die geprüfte Reichweite.
STORED_CA, EDITOR_RCA, MODEL_RCA, POST_ADVANCE_CA und POST_ADVANCE_ATTRIBUTES
bleiben separate Felder. Gespeichertes CA ersetzt keine RCA-Referenz.

Population: isolierte, vollständig beobachtbare Wegwerfprofile aus sechs
Positionsfamilien. 12 Pilotinterventionen gemäß
[Erfassungsprotokoll](../docs/player-development-003/CAPTURE_PROTOCOL.md).
Je Profilidentität zwei Eingriffe, jeweils nach Rückkehr zum Original; geplant
sechs Basisidentitäten, tatsächlich **null** beobachtet. Die Zahl eindeutiger
vollständiger Baselinehashes wird zusätzlich berichtet. Keine Matchseeds.

Einschluss verlangt 40 rohe Modellattribute, vier zusätzliche Kandidatenattribute,
beide numerischen Füße, alle 15 Positionsratings, getrennte CA-/RCA-Werte,
belegte Rohskalen, Spiel-/Editorbuild und überprüfbare unabhängige RCA-Herkunft.
Keine Kategorie→Fußwert-Imputation, keine ungeprüfte Anzeige×5-Umrechnung.
Ein Eingriff ändert genau ein deklariertes Eingabefeld. Alle anderen Profilfelder
und STORED_CA bleiben konstant; Nebeneffekte werden erhalten und als Mismatch markiert.

Vor Mutation: Originalhash, eindeutige autorisierte Zielkopie, Prozess-/Dateigrenzen,
vollständiger Baselinereadback und wiederholter unveränderter Goldreadback.
Nach Mutation: vollständiger Readback und Beleg mit Zeitstempel/Hash. Original
nicht überschreiben. Buildwechsel, fehlende Messquelle, Inputdrift oder
nicht reproduzierbarer Goldreadback stoppen den Zweig. Fehler bleiben im Ledger.

## Hauptserie und Auswertung

Erst nach bestandenem Pilot: **mindestens 48 zusätzliche Fälle** vor Goldsichtung
als vollständige Profile/Interventionen samt Hashes versionieren. Diese Serie ist
hier **nicht eingefroren oder gestartet**. Abdecken: GK/Feldspieler, mehrere
Positionen, 8→9/12→13/17→18, Fußkonstellationen, Einzel-/Mehrpositionen,
vorab modellierte Rundungsnullen und große Modell-Deltas. Keine Fallauswahl
anhand von Goldfehlern. Pilot und Bestätigung getrennt auswerten.

Deskriptiv: exakte Treffer/Nenner, MAE, RMSE, Bias MODEL−EDITOR, maximaler
Absolutfehler; nach Position, Niveau, Füßen und Mehrpositionen. Paarweise
Deltafehler, exakte Deltaübereinstimmung, Vorzeichenkonflikte und Abweichungen
von einem Punkt separat. Ein Einpunktfehler ist zunächst keine bewiesene
Rundungsursache. Gemeinsame Baselines für Profilemetriken deduplizieren;
Interventionen für Deltametriken erhalten. Stichprobeneinheit sind Basisprofile,
nicht Screenshots oder wiederholte Edits. Für eine gewählte Profilpopulation
allenfalls Bootstrap auf Basisprofilclustern, keine i.i.d.-Zeilenintervalle.
Kein Signifikanztest für universelle Exaktheit und keine Modellanpassung auf
eingefrorenen Bestätigungsfällen; korrigierte Modelle benötigen neue Fälle.

Quellenüberlappung: SHLK20-SCOUT-RCA, PLAYGM-RCA-20261104, MAC-20,
CA-002, PD-CA-001. **REPLICATION_WITH_TRANSFER** für unabhängiges Gold;
Exaktheitsclaim **UNCERTAIN_SOURCE**; weitere identische Modellmatrix
**DUPLICATE_STOP**. Atlas/Index/FINDINGS und Originalquellen heute geprüft;
vor künftigem Start erneut prüfen. [Manifest und Status](../data/player-development-003/status.json).

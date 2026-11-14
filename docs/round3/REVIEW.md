# Runde 3 – unabhängiger Offline-Preflight

14.11.2026. Separater Reviewer nach Abschluss der drei Facharbeiten, eigener
Worktree/Branch `codex/round3-review`, Ausgangscommit `b31e019`. Zentralen
Checkout, Runtime, Upstream und Spielinstallation ausschließlich gelesen.
**0 neue native Prozesse, 0 Seedreservierungen, 0 Kalenderadvances und keine
Holdout-/Karriereöffnung durch diesen Review.** Kein Push durch den Reviewer.

## Entscheidung und Umfang

Die geprüfte ATTR-009-Vorbereitung ist nach den unten verifizierten Korrekturen
für die zentrale Vorbereitung und anschließende technische Prüfung geeignet.
**Keine vorweggenommene Hauptserienfreigabe.** Der Director muss konkrete
Eingaben/Seeds/Vertrag publizieren und CI bestehen; danach alle 32 Technikmatches
und die Negativkontrolle tatsächlich prüfen lassen. MECH und TRAIN bleiben
ausdrücklich nativ gesperrt. Ein Offlinecodec oder vollständige Hashreceipts
ersetzen ihre fehlenden semantischen bzw. nativen Gates nicht.

Direkt gelesen: AGENTS, README, METHODOLOGY, FINDINGS, NEXT_STEPS, PLATFORM,
Runde-2-Übersicht und Ergebnisreview, der verbindliche Round-3-Auftrag, alle drei
neuen Fachberichte/Experimente/Verträge, Autorenmodule, CLI-/Analyse-/Export-/
Verifikationscode und Tests. Branchstatus sauber vor eigenen Änderungen;
Remote-main war `3681fcd271b7fb536aeddef4d6dfcedebd4ea1b6`, zentraler Main vier
Commits voraus. Das ist der Stand dieser Vorprüfung, keine spätere Publikationsquittung.

## Tatsächliche Identität und Quellen

Dateiversion der direkt gelesenen DLL: **27.0.1**, Produktbuild
**27.0.1+2503222**. DLL-, Host- und Fixturedateien selbst erneut gehasht:

| Datei | SHA256 |
|---|---|
| DLL | `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340` |
| Host | `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e` |
| Fixture | `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6` |

Alle elf tatsächlichen Ressourcendateien gegen den Directorbeleg erneut gehasht;
eigener kanonischer Fingerprint
`6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883` stimmt.
Sechs Runtime-/native Quelldateien gegen MECHs Quellenbeleg verglichen;
Servernormalisierung, Encoder, Hostvorbereitung/-readback, native Profile und
Executionpfad direkt gelesen. Katalog geprüft:49=Acceleration,53=Pace,
54=JumpingReach; Kataloghash wie VALID-002. Kein Hoststart, Loaderaudit oder
Beweis einer eigenen bytegenauen Kompilierung dieser Quellen.

Installiertes fmsave **0.9.0** und alle vier inventarisierten Quelldateien selbst
gehasht. Die tatsächlich gelesenen TrainingDay/Week-/TeamTrainingmodelle enthalten
Teamkalender, keine individuelle Durchführung;304 ist unbenannt. Verletzungsquelle
trennt HISTORY-Ereignisdatum von TYPED-erwarteter Rückkehr. Das validiert weder
den heutigen Save-Reader am Spielstand noch tatsächliche Verletzungstage.

## Zwei echte Befunde, vor Freeze zentral korrigiert

1. ATTRs Export ohne Registryreceipt meldete technische Zähler als leeres Objekt.
   Damit fehlten die33 vorab festgelegten Technikplätze. Director korrigierte
   den Fehler im zentralen `analysis/export_attr009.py`: alle417 Blueprintplätze
   werden erhalten, vor Seedreservation mit `seed=null`; vorhandener Seedplan
   wird explizit gebunden. Native Evidenz/Matchreservation ohne Receipt blockiert
   den Export statt fälschlich unbegonnene Jobs zu behaupten. Fix direkt gelesen,
   alle14 ATTR-Tests am zentralen Stand ausgeführt und bestanden.
2. TRAIN akzeptierte gebrochene Sessioncodes sowie `False`/`0.0` als Teilnahme-
   Slot0. Director verlangt nun exakte Ganzzahlen/Codebereich0..65535 und
   Teilnahme-Slots0..2; Fix und Regression direkt gelesen, alle12 TRAIN-Tests
   am zentralen Stand ausgeführt und bestanden. Das war eine strukturelle
   Diagnoselücke; `career_released=false` war zu keinem Zeitpunkt umgehbar.

Der Reviewer änderte keine Autorenmodule. Beide Fixes müssen vor Vorbereitung
integriert, eingefroren und in der folgenden CI enthalten sein.

## ATTR: Scope, Eingriff und Analyse

Der Bindungsauftrag erlaubt ausdrücklich passive Effektivität **oder** eine
sichtbar unidentifizierte Mechanismuszerlegung. Die gewählte totale
Masken×Rohattributwirkung ist damit zulässig. Die native Dosis lautet **60→80**,
keine empirisch gemessene FM-Anzeige12→16. Der gelesene Labformatter `/5` belegt
nur die Laboberfläche. Ohne passiven Recorder bleiben Mediation/abgeleitete
Effektivität unidentifiziert. Execution-/Uniformaktivierung ist kein Ersatz.

Vereinigung aktiver logischer IP/OOP-Familien, gemeinsame DC-/DM-/MC-Familien,
seitenspezifische OOP-Permutation und Lineup→Rosterzuordnung sind korrekt getrennt.
GK/Sweeper, Bank, Gegner und sämtliche Nichtinterventionseingaben bleiben erhalten;
26 serialisierte Auswärtsplätze werden nicht auf23 gekürzt, nur23 aktiv kodiert.
Alle24 Absichtszellen aus den tatsächlichen früheren D00-Konfigurationen direkt
gegen eine unabhängig gebildete erwartete Attributmatrix geprüft.

Die native Freigabe verlangt weiterhin nach Originalvorbereitung alle69Attribute,
46 Identitäten/23erKapazitäten,1058 Profilfelder, tatsächliche22 Spielerbindungen
beider Phasen,44 Rollen-/Positions-/PI-Zellen und748 PI-Gruppen; effektiven Seed
und natürliches Ende. Hostquelle prüft nicht nur Managerpläne, sondern tatsächliche
MATCH_PLAYER-Kopien. Umfangszähler allein sind kein unabhängiger Echtdatenreview.

Design korrekt:24 Eingabezellen plus acht festgelegte OJ/SJ-A/A-Wiederholungen,
32 technische Vollmatches plus eine Exit108-Negativprobe. Hauptserie384Matches
=32 unabhängige Seedblöcke×6Arme×2Seiten,16neueSeeds je bekanntem Kontext.
Keine Baseline-, Holdout- oder neue Taktikfrage; fünf sekundäre Endpunkte des
gleichen Kontrasts/Holm5. Gemeinsame Baselines entfallen algebraisch.

Primär `[J−(A+P)/2]S−[J−(A+P)/2]O` auf xGD: zuerst Seitenmittel je Seed,
Kontexte je½. Welch95 und20000 stratifizierte Seedblockresamples; keine
Matchlevel-Pseudoreplikation. Unbekannte Kontrast-SD, praktische0,30xGD und
gewünschte volle Breite0,50 sind Pilotziele, keine Powergarantie.

DeadlineBudget/NativeLease erben dauerhafte Reservations-/Crash-/Retrygates;
neuer Runner verbietet Worktreeausführung und Phasenwiederholung.600s kumulierte
Childzeit/1200s feste UTC-Frist beginnen mit Vorbereitung und schließen
Publikations-/CI-/Reviewzwischenzeit ein;4Worker/90s,2GiB/20GiB bleiben Grenzen.
Vor Hauptstart muss publizierte technische Zusammenfassung exakt stimmen,
erfolgreiche CI zu deren Commit gehören und unabhängiger Technikreview vorliegen.

## MECH und TRAIN: Ergebnisse und Grenzen

Vier echte archivierte D00/R00-Binaries mit je5557Records unabhängig decodiert
und neu serialisiert. Eigener erwarteter Low-Encoder verwendet tatsächliche
Lineuprecords: Default/full bytegleich; low je Seite exakt20 geänderte Feld16/17-
Records bei zehn Startfeldspielern. Alle publizierten Low-/Baselinehashes stimmen.
Quellen bestätigen harte Blocker: Schreiben vor statt nach Originalvorbereitung,
kein passiver Erstfortschritt-Profilbeleg, keine passive Original-Familiarity,
kein eigener zugelassener Runner. **Keine MECH-Nativfreigabe.**

TRAINs660 historische Originalzeilen ohne Import von Projektanalyser oder
`training002.historical_diagnostic` direkt mit rationaler Arithmetik nachgerechnet:

| Historische Deskription | Rohindexdifferenz | CA-Differenz | kumulative Minuten Intervention/Kontrolle | Verletzungseinträge I/K |
|---|---:|---:|---:|---:|
| Heavy−Conditioning, Woche6 |1/44=+0,022727|1/11=+0,090909|14731/14801|4/9|
| Rest−Conditioning, Woche4 |−3/88=−0,034091|5/22=+0,227273|5850/5940|4/4|

Alle264/176/132/88 Trialzeilen geprüft. Exposition ist kumulativ: Endcheckpoint
statt Wochensumme. Keine Intervalle aus22Spielern; keine unabhängigen
Treatmentreplikate, tatsächlichen individuellen Teilnahmen, Kalibrierung oder
Ausfalltage ableitbar. Hash-/Locatorclaims bleiben semantisch unvalidiert;
abweichende RNGlabels oder Savehashes beweisen keine unabhängigen Streams.
**Keine Karriere-/Advance-/Replayfreigabe.**

## Eigener Rechenkern und Prüfung

`analysis/review_round3.py` importiert für die ATTR-Rechnung keinen Projektanalyser,
Verifier, Runner oder `research.stats`. Direkte sechsarmige Differenzen aus
Scores/xG, eigene Blockbildung, Welch95,20000 vollständige Bootstrapindexmatrizen,
Holm5, Kontext-SDs und zukünftige90-%-Fallzahlminima durch lineare Ganzzahlsuche.
Der MECH-Autorencode ist ausschließlich Objekt des unabhängigen Bytevergleichs.
Eigene technische Prüflogik für alle32 Original-Logs/Dumps ist vorbereitet,
aber vor Existenz der ATTR-Technikdaten noch nicht als echter Gateerfolg ausgeführt.

Fünf eigene Tests mit explizit synthetischen Daten bestehen.123 Repositorytests
und5 historische Analysetests im Review-Worktree bestanden;272 geschützte alte
Dateien unverändert. Zusätzlich zentrale14 ATTR-/12 TRAIN-Fixprüfungen bestanden.
`git diff --check` ohne Befund. Eine anfängliche Syntaxklammer im eigenen neuen
Test und ein fehlender eigener CLI-Suchpfad wurden vor dieser Prüfung korrigiert.
Keine neue ATTR-Effektzahl vor echten Daten erzeugt oder publiziert.

Nächster Review: konkrete Prepareartefakte und Publikations-/CIbelege, danach
tatsächliche Technikdaten in `TECH-REVIEW.md`; nur bei Gateerfolg384Hauptmatches
und unabhängige Rohdatennachrechnung in `RESULTS-REVIEW.md`. Änderungen am
eingefrorenen Eingriff/Analysevertrag benötigen erneute Prüfung.

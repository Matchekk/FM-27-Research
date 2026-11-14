# ATTR-009 – unabhängige Abnahme der tatsächlichen Technikdaten

14.11.2026, nach technischen Vollmatches und vor Hauptmatches.
**Technikgate bestanden. Die384Hauptmatches dürfen nach Veröffentlichung dieses
Reviews/der tatsächlichen Technikdaten und erfolgreicher zugehöriger CI zentral
starten.** Kein Review ersetzt die unveränderten Runtime-/Budgetgates.
Keine Erweiterung, Retries, neuen Seeds, Holdouts oder Karriereausführung.

## Unabhängige Prüfung der Originalbelege

Der Reviewer las alle32 privaten Original-Logs und32 Inputdumps direkt.
Die eigene `technical`-Prüfung in `analysis/review_round3.py` wurde tatsächlich
auf diese Dateien ausgeführt; sie importiert weder Projektverifier/-runner
noch Autorenauditor. Öffentliche Ergebnisflags allein wurden nicht als Beleg
verwendet. Kein nativer Start und keine Registry-/Dateiänderung an den Quellen.

| Tatsächlich direkt geprüft | Umfang / Ergebnis |
|---|---|
| Vollmatches und Eingabezellen |32ok;24verschiedene Zellen, alle erwarteten Jobschlüssel/Seeds |
| Attribute/Identitäten |101568 native Attributwerte=32×46×69; beide23erKader vollständig gegen konkrete eingefrorene Konfigurationen |
| Profile |33856Feldwerte=32×46×23 direkt aus `prefix_hex`/`input_tail_hex` decodiert, einschließlich Float-Höhe, Traits, CA/Reputation, Condition/beiderSchärfen/Fatigue/Cohesion/Moral |
| Vorbereitung |32eindeutige Receipts nach Originalvorbereitung;5557Records je Eingabe, effektiver Seed passend |
| Phase/Rolle/PI |1408Phasezellen und23936PI-Gruppen; Position/Rolle/Duty/Targets/alle17PI-Gruppen je Zelle |
| Tatsächliche Spielerbindung |JeMatch vier Phase-Receipts×11 tatsächliche MATCH_PLAYER-Zellen gegen logische Sollzellen und seitenspezifische OOP-Dumps; kein bloßer Managerplanvergleich |
| Masken/Rohdosis |Jede native Maske unabhängig aus logischer IP/OOP-Familienvereinigung rekonstruiert; Fähigkeit54/49/53 korrekt80/60/60 je Arm |
| Endpunkte |Natürliches Vollmatchende, Score/Endtick und originale Teamstatistiken direkt mit Ledger verglichen;32plausibleResultate |
| Native Provenienz |Vier tatsächliche Workerstarts, Host-/DLL-SHA identisch; alle32Ledgerzeilen an genau diese Startreceipts gebunden; jeWorker8/8erfolgreich |
| Verbotene Eingriffe |Keine Execution-Probe/-Version in irgendeinem der32Logs |

23 Profilfelder wurden aus den in der gelesenen nativen Quelle definierten
Speicherbereichen selbst ausgelesen und gegen **jeden** tatsächlichen Kind15-
Record verglichen. Die1058-Feld-Erfolgsquittung ist zusätzlich vorhanden, aber
nicht der alleinige Beleg. Keine privaten Dumps, Binärbytes oder IDs veröffentlicht.

Alle24 R0-Zellen liefern zusätzlich240 Vor-/Nach-Rohdosispaare mit identischer
nativer Spieleridentität: gleicher Kontext/Seed/Seite/Maske, J gegen A-Sibling,
A/P gegen J-Sibling. Betroffenes Attribut jeweils tatsächlich60 vor und80 nach.
Siblingarme sind technische Eingabebelege, keine zusätzliche Baselineleistungs-
studie oder Kalibrierung einer FM-Karriereanzeige.

## Wiederholungen und negative Kontrolle

Alle acht vorab festgelegten OJ/SJ-A/A-Paare beider Kontexte und Seiten sind
exakt gleich hinsichtlich Score, natürlichem Endtick, sämtlichen Teamstatistiken,
Setup und Seed. Keine nachträgliche Auswahl günstiger Wiederholungen.

Ungültige Binäreingabe endet erwartungsgemäß mit Exit108; privater Loghash
erneut geprüft, kein `natural_match_finished`. Erwartete Abweisung bleibt
eigener technischer Versuch und wird nicht als Nullmatch ausgewertet.

## Vollständige Abrechnung, Budgets und Chronologie

Alle417 vorab geplanten Plätze eindeutig abgerechnet:32technischok,
1erwarteteAbweisung, **384Hauptmatches unbegonnen**. Öffentliche Hauptdatei ist
leer; keine `effects.json`. Keine Ausfälle, Ausschlüsse, Ersatzseeds oder Retries.

Zwei dauerhafte erfolgreiche Operationen: Vorbereitung11,1897836s und
Technik19,7699405s; Summe **30,9597241/600s**. Die tatsächlichen privaten
Operationswerte unabhängig summiert und mit dem öffentlichen Budget verglichen.
Studienfenster bis Technikende200,071489/1200s. Unveränderter Beginn
16:40:36,422962UTC; Ende **17:00:36,422962UTC**. Beide ursprünglichen
Leasebelege passen zu Phase/Supervisor und4Workern und wurden vor Phasenbeginn
erworben. Kein aktiver NativeLease oder unreconciled Child nach Technik.

| Ereignis | Tatsächlicher UTC-Beleg |
|---|---|
| Integrations-CI43616762281@0b354315ccf6babfafcb9d166e204d140f3859e0 erfolgreich |16:40:11, vor Vorbereitung16:40:36,427656 |
| Konkrete Vorregistrierung `fc14746685f0a1f6475b1968912317d9ffabdfb6` publiziert |Remote-main direkt im Inputreview geprüft |
| Vorregistrierungs-CI43616995356@fc1474 erfolgreich |16:43:07 |
| Technischer Childstart |16:43:36,724510 |

Beide CIstände tatsächlich über `gh run view` geprüft; Statuscompleted,
conclusionsuccess und erwarteter vollständiger headSha. Die erfolgreiche
Vorregistrierungs-CI liegt vor sämtlichen technischen Vollmatches. Der frühere
Shallowcheckout-CIfehler wurde vor Vorbereitung durch fetch-depth0 korrigiert;
kein wissenschaftliches Hashgate wurde abgeschwächt.

## Freigabegrenzen

Native Eingabe und deterministische Wiederholung sind in diesem konkreten
kontrollierten Build/Fixture belegt. Roh60→80 ist keine behauptete FM-Anzeige-
änderung12→16. Passive abgeleitete Effektivität/Mediation bleibt unidentifiziert;
die ausdrücklich zugelassene totale Masken×Rohattributwirkung ist der Zielparameter.
Keine Karriere-/Meta-/Optimalitätsaussage. MECH und TRAIN bleiben gesperrt.

Fünf eigene Reviewer-Tests und `git diff --check` bestehen. Die um direkte
Profil-/MATCH_PLAYER-/Startupprüfungen erweiterte eigene Techprüfung wurde erneut
auf alle Originalbelege ausgeführt und bestand. Dies ist unabhängige Nachprüfung
derselben zentralen Ausführung, keine externe Replikation oder weitere Simulation.

Nach Veröffentlichung dieses Gateberichts und erfolgreicher Technik-CI darf der
Director ausschließlich die eingefrorenen384Hauptmatches innerhalb der bestehenden
600s-/1200s-Grenzen ausführen. Danach eigene Rohdatennachrechnung und Ergebnisreview;
vorher keine wissenschaftlichen Effektzahlen aus Technikmatches auswählen.

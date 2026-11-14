# TACT-003-STLESS-R0 – unabhängige native Technikabnahme

15.11.2026 CET · Research Agent, getrennt von Studienrunner/Compiler/Analyse.
**TECH32+1 bestanden. Der registrierte512Match-Hauptlauf ist technisch
akzeptiert, erst nach Veröffentlichung dieses Reviews/Releasegates und
erfolgreicher CI des exakten Freigabecommits.** Keine technische Armauswertung
als wissenschaftlicher Leistungstest, keine Karriere- oder allgemeine
Stürmerlos-Empfehlung.

## Tatsächliche neue Belege

Geprüft wurden [32öffentliche Technikmessungen](../../data/night-002-stless003/technical.jsonl),
[33er-Abrechnung](../../data/night-002-stless003/technical-job-accounting.jsonl),
[Summary](../../data/night-002-stless003/technical-summary.json),
[Budget](../../data/night-002-stless003/technical-budget.json), die neuen
Originaldumps/-logs und sämtliche Cleanup-/Admissionbelege. Der bestehende
Inputreview wird nicht als neue native Validierung ausgegeben.

Der veröffentlichte Read-only-Verifier `review_stless003.py private-technical`
besteht:32Originalmatches,16A/A,1Negativprobe, vollständige öffentliche/private
Übereinstimmung und33reproduzierte Claimzulassungen. Seine Wiederverwendung
des niedrigen Inputaudits ist ausdrücklich offengelegt. Zusätzlich führte
dieser Reviewer eigene direkte Byte-/Eventprüfungen durch.

## Positionen, Rollen und tatsächliche Actorbindungen

Alle16Kontext×Seite×Arm-Zellen sind mit zwei Wiederholungen vertreten.
Insgesamt **1408tatsächliche Phasenzellen** wurden direkt geprüft:32Matches ×
2Mannschaften ×2Phasen ×11Spieler. Die `native_phase_configuration`-Zeilen
stammen im unveränderten gehashten Host aus den tatsächlichen MATCH_PLAYER-
Zellen, nicht allein aus den Managerplänen. Die tatsächlichen Roster-IDs im
Inputdump stimmen mit den erwarteten Originalakteuren überein.

Für jede tatsächliche Actorzelle wurden Positionsmaske und identifizierte
Rollenflags mit ihrer eigenen Armkonfiguration und unabhängig mit den
gehashten Manager-Taktikslotbytes verglichen. Die seitenspezifische OOP-
Permutation wird für Managerpläne verwendet; tatsächliche Actorzeilen werden
an ihren ursprünglichen Spielerslot gejoint. Das vermeidet eine doppelte oder
fehlende Permutation. Explizite native PI-Flags stimmen mit den gebundenen
persönlichen Anweisungen überein.

Die beiden betroffenen ursprünglichen Akteure erscheinen tatsächlich so:

| Arm | Zugewiesene IP-Zellen8/10 | Zugewiesene OOP-Zellen8/10 |
| --- | --- | --- |
| I0-O0 | AMC/AM und ST/CF | AMC/OPAM und ST/OPCF |
| I1-O0 | AMCL/AM und AMCR/SecondStriker | AMC/OPAM und ST/OPCF |
| I0-O1 | AMC/AM und ST/CF | AMCL/OPAM und AMCR/OPAM |
| I1-O1 | AMCL/AM und AMCR/SecondStriker | AMCL/OPAM und AMCR/OPAM |

Damit ist die neue Paketübertragung nativ belegt. Das misst zugewiesene Rollen
und Positionen, **keine Laufwege oder isolierten Rollenmechanismen**.
Intrinsisches Rollenverhalten bleibt Teil des Pakets.

Die beiden ursprünglichen Kind13-Game-Constraints bleiben1. Alle32Matches
werden durch die ursprüngliche Vorbereitung akzeptiert (`gates=[1,1,1]`), ohne
invaliden Rollenkontext, Szenarioabweisung oder Actorbindingmismatch. Normale
Matchabschlüsse sind vorhanden. Diese tatsächliche Annahme ergänzt den zuvor
bestandenen statischen Katalogcheck; kein neuer Host oder Setter war erforderlich.

## Native Eingaben und Startkontrollen konstant

Die eigene direkte Rekonstruktion prüft **101.568Attributwerte** aus den
Originaldumps gegen die jeweiligen Kind1-Records. Zusätzlich wurden alle
**33.856Profilwerte** aus Prefix-/Inputtailbytes unabhängig als ursprüngliche
Integer-/Floatfelder decodiert und gegen die1058Kind15-Records jeMatch geprüft.
Keine veränderte Spielerzahl, Eignung, Fähigkeit, Bank oder Gegnerprofile.
Der vorhandene niedrigstufige Audit prüft darüber hinaus748PI-Gruppen jeMatch.

Nach Vorbereitung und erstem tatsächlichem Fortschritt wurden2944Actorzustände
geprüft:46Akteure ×2Zeitpunkte ×32Matches. Condition/C90/C7A jeweils10000,
Fatigue0, Accumulator1000000 und Penalty0; Cache89/8A der22Starter jeweils100.
Die direkt identitysortiert rekonstruierten Kontrollhashes einschließlich
roher33Byte-Region stimmen mit den vorab eingefrorenen D00-Goldbelegen überein.
Das beweist weder UI-Effectiveness100 noch einen dauerhaften Familiarity-Clamp.

Alle36eingefrorenen Projektquellen und konkreten Setup-/Log-/Dumphashes stimmen.
Kontext bleibt FM27 `27.0.1+2503222`, unveränderter Observerhost, v1114.6 und
das gebündelte D00-Fixture. Keine erlaubte Paketänderung wurde nachträglich
aus einem Kontrollmismatch abgeleitet.

## Wiederholbarkeit, Negativkontrolle und Cleanup

Alle **16A/A-Paare** sind exakt gleich in tatsächlichen Ergebnissen/ursprünglicher
Teamstatistik und den vorab identifizierten Roh-/Cache-/TF33-Zuständen an allen
drei Zeitpunkten. Die eigene Eventprüfung bestätigt dies zusätzlich nach
Identitysortierung. Keine Behauptung über beliebige undecodierte Speicherbytes.
Es wurden keine technischen Resultate proArm zusammengefasst oder als
Effektschätzung verwendet.

Die separate malformed-Binärprobe liefert Exit108, genau ein`scenario_rejected`
und keinen natürlichen Matchabschluss.33geplante/gestartete/aufgelöste Jobs:
32gültige Vollmatches und1erwartete Abweisung. Keine Fehler, unbegonnenen
Technikjobs, Retries oder Ersatzseeds. Alle512Mainjobs bleiben ungestartet.

Alle33Kernelcontainmentreceipts wurden direkt auf bestätigtes Kapselende,
Cleanup und0Kernelrestprozesse geprüft. Joblimit3, Kill-on-close, kein Breakaway
unverändert;0Cleanupfehler/0Pendingmarker, gemeinsame NativeLease frei.
Zusätzliche Windows-Prozessabfrage findet0Observer-/Simulatorreste. Maximal4
gleichzeitig geclaimte Calls sind im Dispatch belegt; dies ist kein gemessener
Engine-PID-Peak.

## Neue Aufrufsummenbegrenzung und erhaltenes Altbudget

Die33Claimproofs wurden zusätzlich unabhängig in der sperrserialisierten
Concurrencyreihenfolge nachgespielt. Jeder Claim reserviert40s für sich sowie
für vorher unaufgelöste Claims; vollständig gemessene Calls gehen mit ihrer
tatsächlichen positiven Dauer ein. Stets stimmen Proof, laufende Claimzahl
und kumulierte Zeit überein. Höchste beobachtete Zulassungsobergrenze:
**1089,143s /3600s**; am Ende0unaufgelöste Claims.

Der unveränderte gefrorene Aufruf verwendet nachweislich den absoluten
`total_timeout=min(allowance,30)` mit Job3. Längster tatsächlicher neuer Call
**3,406s**, alle33unter30s und unter der40sBereinigungshülle. Neue technische
Callsumme **105,142s**. Zusammen mit den erhaltenen257alten Calls/838,064s
ergibt das **943,206s**, ohne die unvollständige MECH-004-Serie umzubenennen.
Die technischen Belege bestätigen die Admissionen und die tatsächlich
gemessenen Zeiten, keine beliebige zukünftige Timeoutgarantie.

Parallel bindende Whole-phase-Abrechnung:

- Eigenes technisches Studienbudget75,6647733s/900s, erfolgreich reconciled.
- Global697,1870802s/3600s; die früheren589,7353507s bleiben vollständig enthalten.
-578globale Reservationen =545alte +33neue Technikplätze. MECH-004 bleibt
  ausdrücklich terminal; eigenes altes Haltledger unverändert.
- Eigene feste Frist15.11.01:19:09,243151UTC; globale Grenze07:00UTC/08:00CET.
  Vor erstem Maincall bleiben die vorregistrierten unmittelbaren600sRestgates
  separat erforderlich.
- Geprüfter Snapshot:20.253.517privateTACT-Bytes und167.266.101Missionsbytes,
  unter2/4GiB. Keine Livekompaktierung oder Dateiumstrukturierung während
  dieser Phase; alle neuen Originalbelege liegen unverändert vor.

Die tatsächliche technische Phase folgte veröffentlichtem Commit
`315eac1c3634ba4000796a4d7aaf40a55f4454db` mit erfolgreicher
[CI43654718507](https://github.com/Matchekk/FM-27-Research/actions/runs/43654718507).
Das Actions-API bestätigt denselbenHead und success am14.11.23:46:54UTC.
Das eigene Technikfenster beginnt23:49:09,243151UTC und endet erfolgreich
23:50:24,929659UTC. Die Reihenfolge und festen Budgets sind nachvollziehbar.

## Releaseumfang

Das [technische Releasegate](../../data/night-002-stless003/technical-release.json)
bindet den LF-SHA256 der tatsächlich geprüften Summary und dieses Reviews.
Akzeptiert wird ausschließlich der registrierte512Match-Pilot nach Publikation
und erfolgreicher Freigabe-CI sowie allen laufenden Admissions-/Restzeitgates.
Neue Rollen-/Positionspakete sind in diesem Fixture technisch ausführbar;
ihre wissenschaftliche Leistung ist durch diese32Technikmatches noch offen.
Keine Wiederaufnahme von MECH-004, keine Karrierefreigabe. Native Aufrufe,
neue Seeds und wissenschaftliche Armauswertungen durch Reviewer: jeweils0.

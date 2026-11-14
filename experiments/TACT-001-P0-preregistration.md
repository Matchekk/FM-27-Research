# TACT-001-P0 – Pressing × Defensivlinie

**Vorregistrierung · 14.11.2026 · Varianzpilot, vor jedem Match veröffentlicht.**
Keine Taktikoptimierung, Kandidatenauswahl oder konfirmatorische Meta-Aussage.
Dieses Dokument und die Analyse bleiben während der Hauptserie eingefroren.
Technische Belege und Ergebnisse erscheinen in separaten Dateien.

## Frage, Kontrolle und Intervention

Interagiert eine höhere Pressingintensität mit einer höheren Defensivlinie im
xG-Saldo unserer selbst aufgebauten IP-4-2-3-1? Zweiseitige Nullhypothese:
mittlere Differenz-von-Differenzen (DoD) = 0. Zielpopulation dieses Pilots sind
die zwei festgelegten synthetischen Laborkontexte, keine beliebige FM-Karriere.

| Arm | TriggerPress (Gruppe 10) | DefensiveLine (Gruppe 9) |
|---|---|---|
| baseline (P0L0) | Standard, ID 1313689463, Bit 0 | Standard, ID 894978671, Bit 0 |
| press (P1L0) | More Often, ID 2000905329, Bit 66 | Standard |
| line (P0L1) | Standard | Higher, ID 1329018200, Bit 57 |
| combined (P1L1) | More Often | Higher |

Alle Optionen kommen aus dem lokal geprüften v1114.6-Katalog. `rules=game` und
IP-4-2-3-1 werden für jede der 16 Eingabezellen streng geprüft. Objekt- und
Binärvergleiche zeigen ausschließlich die deklarierten Änderungen in Gruppe
9/10 auf der Testseite; keine übrige Eingabe ändert sich innerhalb eines Kontexts.
[Binärer Vorabvergleich](../data/tact-001-p0/binary-diff-audit.json).

## Build und eingefrorene Eingaben

FM27 `27.0.1+2503222`, Lab v1114.6, Upstream
`91f2eba57fac0b7fbd3dff616056907e3ce461be`, Adapter
`fm27_desktop_8c6971ce_adapter_v1`.

- Engine: `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
- Host: `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`.
- Fixture: `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6`.
- Ressourcen: `6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883`.

Alle Identitäten stimmen erneut mit [VALID-002](VALID-002-adapter.md) überein.
Live-GitHub-API und Tags zeigen v1114.6 als jüngsten stabilen Release; keine
automatische Aktualisierung. Der Web-Redirect `/releases/latest` lieferte einen
älteren gecachten Stand und wurde nicht als Versionsbeleg verwendet.
Gespeicherte Karriere-PKM werden nicht genutzt.

## Formation, Rollen und Spielermanagement

Beide Teams haben IP-4-2-3-1 und OOP-4-4-1-1. Jede Zeile ist derselbe logische
Spieler in beiden Phasen; nativer OOP-Zellindex wird seitenabhängig aus dem
geprüften Fixturemapping kodiert und zurückgelesen.

| Slot | IP / Rolle | OOP / Rolle |
|---:|---|---|
| 0 | GK / Goalkeeper | GK / OPGoalkeeper |
| 1 | DR / FullBack | DR / OPFullBack |
| 2 | DCR / CentreBack | DCR / OPCentreBack |
| 3 | DCL / CentreBack | DCL / OPCentreBack |
| 4 | DL / FullBack | DL / OPFullBack |
| 5 | DMR / DefensiveMidfielder | MCR / OPCentralMidfielder |
| 6 | DML / DeepLyingPlaymaker | MCL / OPCentralMidfielder |
| 7 | AMR / Winger | MR / OPWideMidfielder |
| 8 | AMC / AttackingMidfielder | AMC / OPAttackingMidfielder |
| 9 | AML / Winger | ML / OPWideMidfielder |
| 10 | ST / CentreForward | ST / OPCentreForward |

Duties explizit `0` (zulässiger Katalogwert), alle 17 PI-Gruppen je Zelle `0`
(keine individuellen Overrides), keine Zielspieler-/Zielpositionsdeckung.
Mentalität 4, feste Startelf Slots 0–10, Kapitänspriorität 2/3, Schützenpriorität
8/7/9. Gegneranweisungen neutral. Alle übrigen benannten Teamanweisungen auf
ihre Standardoption, Angriffspressinglinie des Testteams auf Mid Block
(ID 1196979288 / Bit 62); zusätzliche unbenannte Teamflags 0.
Standards bleiben in allen Armen identisch aus dem gebündelten Laborfixture.

Matchmanagement: absolut kodierte Eingaben, nativer Managerbit 0 = 1 für den
Supplied-Plan-Pfad beider Teams; keine native AI-Neugenerierung, kein
`native_generation`, kein `experimental_execution`, keine injizierten Wechsel,
Zurufe oder Live-Anweisungen. Die originale Benchmark-Matchklasse läuft bis
zum natürlichen Ende. Daraus folgt keine Gleichheit mit vollständigem
Karriere-/Urlaubs-/Instant-Result-Management.

## Kader und Gegnerprofile

23 aktive synthetische Spieler je Seite. Kaderprofile beider Teams sind in
allen geschriebenen 69 Attributwerten und 23 erweiterten Profilfeldern gleich.
Native Fixtureidentitäten bleiben an der Zielseite; übriger Fixturekontext
wird nicht als vollständig identischer Karrierezustand ausgegeben.

- GK-Slots 0 und 11: GK-Eignung 20, andere Positionseignungen 0.
- Feldspieler: GK/UnusedSweeper 0, Positionsindizes 2–14 jeweils 20.
- Alle Fähigkeitsindizes 15–68 auf Rohwert 60. Das ist eine kontrollierte
  synthetische Modellannahme, kein realistisches positionsspezifisches Kaderprofil.
- Alter 25, Größe 180 cm, Gewicht 75 kg, CA 120, Reputationen 5000,
  Persönlichkeitswerte jeweils 12, Traits 0. Fitness/Schärfe 10000,
  Ermüdung 0, Teamkohäsion 80, Clubkohäsion 100, Moral 20.

| Entdeckungsgegner | Pressing | Linie | Engagementlinie | Ballverlust |
|---|---|---|---|---|
| high_press | Much More Often, Bit 65 | Higher, Bit 57 | High Press, Bit 61 | Counter-Press, Bit 70 |
| deep_block | Less Often, Bit 67 | Lower, Bit 58 | Low Block, Bit 63 | Regroup, Bit 71 |

Gleiche Spieler, Rollen, Phasen und übrige Einstellungen zwischen den Gegnerstilen.
Der Gegnerstil ist ein Kontextbündel und kein isolierter Einzelmechanismus.
Zwei vorab markierte Holdouts: `holdout_midblock` und `holdout_direct_counter`;
ihre vollständigen Anweisungs-/Phasenbeschreibungen und Profilhashes sind
eingefroren. **Keine Holdoutsimulation in diesem Auftrag.**
Alle 16 binären Setuphashes, die aktiven Profilhashes, Rollen/PI, Katalogoptionen
und Runtime-/Quellhashes stehen in [inputs.json](../data/tact-001-p0/inputs.json).

## Seeds und Stichprobe

16 neue Hauptseeds, acht je Gegner. Pro Seed vier Arme auf beiden Seiten:
**128 Hauptmatches, 16 unabhängige Seedblöcke**. Testseite wird vollständig
übertragen und alle Ergebnisse werden aus ihrer Sicht gemessen. Seiten sind
abhängige Messungen im selben Block und verdoppeln die unabhängige Fallzahl nicht.

SHA256(`TACT-001-P0/main-v1/{counter}`), erste vier Bytes Little Endian;
null sowie alle archivierten, technischen und lokal reservierten Seeds werden
übersprungen. Drei getrennte technische Seeds werden vor den Hauptseeds
reserviert. Der dritte bleibt für die bereits vor Seedverarbeitung verworfene
negative Konfiguration reserviert und darf später nicht wiederverwendet werden.
Vorab wurden 2.130 verschiedene historische/reservierte Werte ausgeschlossen.
[Exakte Reservation mit Hash der Ausschlussmenge](../data/tact-001-p0/seed-plan.json).
Jobreihenfolge ist vorab durch SHA256 der Jobkennung bestimmt.

## Technische Freigabe und Budget

Vor Hauptstart 16 Eingabezellen je einmal mit technischem Seed prüfen. Sieben
feste identische Wiederholungen: alle vier Arme von high_press auf Testseite 0,
baseline/press/line von deep_block auf Testseite 1. Damit **23 vollständige
Prüfmatches** und eine separate absichtlich ungültige Binäreingabe = **24 technische
Versuche**. Alle sieben A/A-Wiederholungen müssen in Setuphash, Endstand,
Endtick und Teamstatistik exakt gleich sein.

Jedes akzeptierte Match braucht wirksamen Seed, Start 0:0, natürlichen Abschluss,
plausible native Teamstatistik, alle nach Vorbereitung verifizierten Eingaberecords,
beide Phasen, Rollen/Duties, alle aktiven Attribute und 1.058 Profilfeldbelege
(46 Spieler × 23 Felder). Zusätzlich werden die tatsächlichen Creatorbits aller
benannten Teamanweisungen aus dem Dump gegen die Solloptionen geprüft.

Dauerhafte Zähler in `local/tact-001-p0/budget.json`: technische Reservierungen
maximal 24, Hauptreservierungen maximal 128, maximal vier Worker,
90 Sekunden ohne Fortschritt. Kein Retry, keine Ersatzseeds. Matchjobs werden
vor Prozessstart irreversibel reserviert. Hauptläufe in acht Batches zu 16 Jobs;
jeder nutzt dieselbe kumulative Budgetdatei.

Gesamte native Ausführungszeit höchstens **900 Sekunden**. Ein separater
Supervisor misst die gesamte Child-Wall-Time konservativ einschließlich Python-
Vorbereitung/Audit und nativer Preflights. Persistierte aktive Operation und
UTC-Deadline verhindern einen Budgetreset bei Prozessneustart. Der Supervisor
beendet seinen eigenen Prozessbaum spätestens am verbleibenden Limit, mit fünf
Sekunden Rücklage für Abbruch. Unsicherer Prozesszustand oder Fehler verriegeln
weitere Ausführung. 2 GiB Speicherreserve, 512 MiB lokales Artefaktlimit je
Pilotarbeitsverzeichnis, höchstens 16 Jobs pro nativem Batch.

Vor jedem Engine-Aufruf scheiterte zunächst die Supervisor-Authentifizierung
am zusätzlichen Windows-venv-Launcherprozess. Der unmittelbare PPID-Vergleich
wurde durch Token plus Prüfung des lebenden Supervisors ersetzt. Dieser reine
Vorbereitungsfehler startete **keine Engine und kein Match**; seine 0,989 Sekunden
bleiben im Budget, es wurden keine Jobreservierungen oder Zeiten zurückgesetzt.
Die erfolgreiche Vorbereitung verbrauchte einschließlich Preflight insgesamt
4,125 kumulative Sekunden. Alle Reparaturbelege bleiben erhalten.

## Eingefrorene Analyse

Primär `xGD = xGF − xGA`, pro Seite und Seed:
`DoD = combined − press − line + baseline`.
Zuerst Seitenmittel im Seed, dann gleichgewichtetes Mittel beider Gegner
(je 1/2). Positives Vorzeichen bedeutet, dass der gemeinsame Eingriff mehr xGD
liefert als die Summe der beiden marginalen Eingriffe in diesem Kontext.

Gepaarte Kontraste mit 95-%-t-Intervall und Welch-Satterthwaite-Freiheitsgraden
für die zwei Szenariomittel. Ein zweiseitiger Primärtest α=0,05.
20.000 deterministische, innerhalb jedes Gegners stratifizierte Bootstrapresamples
vollständiger Seedkontraste; beide Seiten und alle vier Arme bleiben gebunden.

Sekundäre Familie aus **zehn** gleichartig definierten DoD-Tests: Punkte (3/1/0),
Tore, Gegentore, xGF, xGA, eigene/gegnerische Schüsse, eigene/gegnerische
Schüsse aufs Tor, eigener Ballbesitz. Holm über genau diese zehn Tests.
Marginale Intervalle bleiben als marginal gekennzeichnet. Arm-Mittelwerte sind
rein deskriptiv; kein Ranking oder Gewinnerkriterium.

Berichtet werden Kontrast-SD je Gegner, gepoolte SD innerhalb der Kontexte und
einseitige 95-%-SD-Obergrenzen unter Normalitätsannahme; die gepoolte Grenze
setzt zusätzlich gemeinsame Varianz voraus. Bestätigungsplanung für vorab
festgelegte **0,10 / 0,15 / 0,20 xGD-DoD**, 90 % Power, α=0,05,
balancierte neue Szenarioblöcke und beide Seiten. Nichtzentrale t-Näherung mit
Satterthwaite-df, einmal beobachtete SDs und einmal deren individuelle
95-%-Obergrenzen. Zwei individuelle 95-%-Grenzen sind keine gemeinsame 95-%-Grenze.
Fallzahl als neue Blöcke pro Kontext, Gesamtblöcke und Gesamtmatches berichten.

Dieser Pilot ist **nicht** für den 0,10-xGD-Nachweis gepowert. Kleine n=8 pro
Kontext machen SDs, Bootstrapgrenzen und Powerplanung unsicher. Keine
Bestätigung, universelle Meta-Aussage, Optimierung oder Holdoutauswertung.

## Fehler, Ausschlüsse und Veröffentlichung

Keine ergebnisabhängigen Ausschlüsse und keine stillen Nullen. Native Eingabe-,
Seed-, Identitäts- und Wiederholungsmismatchs stoppen die Serie. Jeder begonnene,
fehlgeschlagene und unbegonnene Job wird aus Plan und Rohbelegen ausgewiesen.
Bei unvollständigen Blöcken wird ausschließlich technischer Status veröffentlicht.
Geschützte Binäreingaben, Dumps, Fixture und sonstiges Spielmaterial bleiben lokal;
öffentliche JSONL enthalten nur erlaubte Messfelder und Hashbelege.

[JSON-Vertrag](../research/specs/TACT-001-P0.json),
[Ausführungscode](../analysis/run_tact001p0.py),
[Analysecode](../analysis/analyse_tact001p0.py),
[Budgetkontrolle](../research/budget.py). Vor dem Hauptlauf wird die konkrete
Registrierung auf den bereits gepushten Vorregistrierungscommit gebunden und
zusammen mit der technischen Freigabe veröffentlicht.

# Forschungsroadmap – FM27 Research 2.0

## Aktualisierung nach abgeschlossener Runde2

[TACT-Rollenpilot512Matches](../experiments/TACT-002-R0-results.md) abgeschlossen,
Präzisionsziel erfüllt,kein Primär-/Holm7-Nachweis. Nicht auf1024aufstocken.
[VALID003- und SET-V0-Module](round2/README.md) sind geprüfte Offlinevorarbeiten,
keine native Profil-/Karriere-/Standardfreigabe. Der neue TACT-Runner integriert
die zentraleLease tatsächlich;alteRunner bleiben unverändert.

Priorität jetzt [ATTR→MECH→TRAIN](../experiments/NEXT-ATTR-MECH-TRAIN-round3.md):
Masken-/Effektivitäts-/Rohskalenaudit,danach gezielter Attributinteraktionspilot;
eigener Startpolicy-Pfad vor Schärfeversuch;Karriere-RNG und Teilnahme vor Training.
Alle weiteren Serien bleiben separate neue Aufträge mit eigenenGates/Budgets.

## Aktualisierte Priorität – Multi-Agent-Programm14.11.2026

[Gesamtauswertung mit sieben getrennten Berichten](program-2026-11-14/README.md)
und [unabhängiger Review](program-2026-11-14/REVIEW.md) ergänzen die ursprüngliche
Planung unten. Das Programm ist Recherche/Design und Offlinevorarbeit, keine
Freigabe zusätzlicher nativer Hauptserien.

1. **TACT-Rollenmanifest und kleiner ST/AMC-Pilot:** erst32 technische Vollmatches
   plus Negativprobe mit vollständigen Rollen-/PI-/Phasenreadbacks; danach eigener
   neuer512-Match-Vertrag. P1C verfehlt die Punkte-Hinweisregel; D15/D09 archivieren.
2. **VALID-003 und Startpolicy-Audits:** positionsabhängige Profile/Stärken,
   kapazitätserhaltende PKM und individuelle Eingriffspfade. Standardnormalisierung
   überschreibt Fitness/Schärfe; normale JSON-Änderung genügt nicht. Keine bestehende
   Freigabe still erweitern. Neue opt-in Exklusivlease ist noch nicht in Runner integriert.
3. **ATTR-Brücke statt globalem Ranking:** JR-vs-Speed×ungenutzte Positionsratings
   gezielt kreuzen. Externe Study17/17b untersucht Positionsratings bereits;
   neuer Mehrwert ist die spezifische Attributinteraktion, nicht ihre Haupteffektreplikation.
  512/1024-Match-Varianzpilot oder nach eigenem Familien-/Technikumbau384/768.
4. **MECH:** isolierbare Startzustände erst nach Schreib-/Readbackgate; Familiarity
   und künstliche Executionrecords nicht mit Karriere-Lernwirkung gleichsetzen.
5. **SET-Messkette:** tatsächliche Ausführung, Schuss-xG, Besitz-/Konterattribution
   zuerst. Bestehender SET-001-Draft hat64/32-Block- und Endpunktwidersprüche;
   archivieren und vor neuer Registrierung konsistent versionieren, keine Leistungsserie.
6. **TRAIN-Karrierefundament:** unabhängige Save-/RNG-Cluster, Kalender-/Teilnahme-
   receipts und Roh-/Anzeigeeinheiten. Kleine/große Karrierepiloten bleiben blockiert;
   kein Ersatz durch isolierte Einzelmatches und keine Power aus22 Spielern.

Alle Budgets, SD-Annahmen, Informationsraten und Blocker stehen in den Fachberichten.
Die folgende Ursprungstabelle bleibt als damalige Modulplanung erhalten; die
aktuelle Reihenfolge und Freigabereife ergeben sich aus dieser Ergänzung.

Stand 14.11.2026. Keine der folgenden Serien wurde in diesem Auftrag ausgeführt.
Erkenntnisziel: eigene belastbare Lösungen innerhalb benannter Kontexte entwickeln.
Ein globales Ranking aller denkbaren Taktiken oder Attribute ist kein identifizierbares
Versuchsziel. [Quellenregister](EXTERNAL_RESEARCH.md) und [technische Freigabe](../experiments/VALID-002-adapter.md)
bestimmen, welche Fragen sinnvoll und technisch tatsächlich erreichbar sind.

## Priorisierung

| Priorität | Programm / neue Frage | Erkenntniswert und bisherige externe Forschung | Aufwand / geplante Stichprobe | Abhängigkeiten und Validierung | Nutzen im echten Save |
|---|---|---|---|---|---|
| P0 | Native Eingabedeckung und Karrierefixture-Kapazität | Verhindert Scheineffekte; Windows/Mac nutzen unterschiedliche Zustandswege | Je neuem Eingabetyp kleine A/A-/Readback-Serie; keine Rankingserie | VALID-002 bestanden nur im gebündelten Fixture; gespeicherte PKM separat reparieren | Aussagen bleiben dem wirklichen Build und Startzustand zugeordnet |
| P1 | TACT-001: eigene 4-2-3-1, Pressing × Linie, danach Rollenpaare | Mehrwert durch gezielte Interaktionen, eigene Kandidaten und gehaltene Gegner; bestehende Downloads sind Referenzen | Erster Pilot 128 Hauptmatches; später getrennt genehmigtes DoE/Bestätigung | Game-Rollenregeln, beide Phasen, PI/Team-Readbacks; Kandidat vor gehaltenen Seeds einfrieren | An Kaderstärke und Gegner anpassbare selbst entwickelte Taktik |
| P2 | MECH-001: Spielschärfe × Pressing | Extern starke Startzustandseffekte; deren Interaktion und Windows-Kontext offen | 32 neue Blöcke × 4 Arme × 2 Seiten = 256 Pilotmatches; Power danach | Startprofil und Eingriff nativ prüfen; Fitness getrennt konstant | Rotation/Matchfitness mit taktischem Belastungsprofil abstimmen |
| P2 | SET-001: Eckroutine mit situationsbezogenem Nettoertrag | Rohes Tore/Match-Ranking oft durch verschiedene Chancenanzahl verzerrt | Zuerst 200 tatsächliche Ecken/Arm für Varianz-/Zählerpilot; bestätigende Fallzahl aus Ereignisrate | Ereignis-/Besitzkettenzähler, Routine- und Taker-Readbacks fehlen noch | Standardtore gegen Konterrisiko abwägen |
| P3 | ATTR-008: Positions-/Rollen-/Niveauabhängigkeit und Verwertung | Viele globale Rankings vorhanden; lokale Nichtlinearität und Taktikinteraktionen offener | Startpilot 32 Blöcke/Szenario; volles 2×2×2-Kontextdesign = 1.024 Matches bei zwei Armen und beiden Seiten | Rolle/Position/Attribute getrennt, Punkte und Tore ergänzen xG | Kaderbezogene marginale Attributgewichte statt universeller Summenscore |
| P3 | TRAIN-002: Leistung und Entwicklung getrennt optimieren | TRAIN-001 und externe Trainingslisten bleiben überwiegend explorativ | 8 gepaarte Ableger/Altersstratum, 2 Arme, 6 Wochen; danach Cluster-Powerplan | Karriere-Executor, tatsächliche Teilnahme, Coach-/Kalenderkontrolle, unabhängige Ableger | Wochenpläne für Profis und Jugend ohne Ermüdung als versteckten Preis |
| P4 | TACT-002: weitere OOP-Strukturen, SET-Freistöße/Einwürfe, versteckte Attribute | Breitere Mechanismen erst nach kleineren identifizierbaren Kontrasten | Neu planen anhand der vorherigen Varianzen; kein kartesisches Vollraster | Erfolgreiche Eingabeaudits und unabhängige Bestätigung | Robustheit und Gegenanpassung |
| Später | SCOUT: Entscheidungen aus bestätigten Kontextmodellen | Anwendung, kein weiteres ungesichertes Attributranking | Retrospektiver Prognosetest auf gehaltenen Kadern/Saves | ATTR/TACT/MECH-Endpunkte, Unsicherheit, Transferkosten getrennt modellieren | Position-/taktikspezifische Shortlists mit nachvollziehbaren Grenzen |

Die Benchmarkzeit von etwa fünf Sekunden für acht Jobs bei vier Workern ist nur
ein grober lokaler Größenordnungsanker. Große Serien brauchen ein neues Zeit-/Speicherbudget,
gemessene Eingabevorbereitung und Fehlerquote. 128 einfache Pilotmatches könnten
rechnerisch wenige Minuten benötigen; Karrierefortschreibung und große Saveimporte
sind darin überhaupt nicht enthalten. Keine unkontrollierte mehrstündige Serie.

## Fallzahlgrundlage statt willkürlicher Spielanzahl

Planungsbeispiele aus `research.stats.required_n`, zweiseitiger gepaarter t-Test,
90 % Power, unabhängige neue Seedblöcke. **Angenommene**, nicht neu gemessene SD:

| Endpunkt / angenommene SD | Zielunterschied | α=0,05 | α=0,05/4 als konservative Familie |
|---|---:|---:|---:|
| xGD / 1,0 | 0,10 | 1.053 | 1.432 |
| xGD / 1,0 | 0,15 | 469 | 638 |
| xGD / 1,0 | 0,20 | 265 | 361 |
| Punkte / 1,5 | 0,10 | 2.367 | 3.217 |
| Punkte / 1,5 | 0,15 | 1.053 | 1.432 |
| Punkte / 1,5 | 0,20 | 593 | 807 |

Das sind **Blöcke**, nicht automatisch einzelne Matches. Jeder Block kann mehrere
Arme, Seiten und Kontexte enthalten. Werden beide Seiten mit demselben Seed gespielt,
werden sie im Seed gemittelt; sie verdoppeln nicht die unabhängige Fallzahl.
Bei mehreren Szenarien feste Gewichte und stratifizierte Resamples verwenden.
Eine SD aus dem alten ATTR-Build oder einem anderen Eingriff ist nur ein
Planungsszenario. Pilot-SD einschließlich einseitiger 95-%-Obergrenze vor dem
Bestätigungsplan verwenden; nicht den höchsten optimierten Effekt als Wahrheit einsetzen.

Bei Karriere, Ecken und Verletzungen sind diese t-Fallzahlen nicht übertragbar:
hier braucht es Cluster-/Zählmodelle bzw. simulationsbasierte Planung mit
Expositionsraten und Überdispersion. Eine große Zahl Spieler oder Ecken ersetzt
keine unabhängigen Save-/Matchcluster.

## Modulprogramme und nächste freigabefähige Designs

- **TACT:** [TACT-001](../experiments/TACT-001-discovery.md): Baselineaudit → zulässiger
  Suchraum → effizientes DoE → vier benannte Interaktionsfamilien → begrenzte
  Modellvorschläge → gehaltene Bestätigung. Stürmerlose Systeme erhalten eine
  eigene spätere Suchklasse; die erste Klasse behält IP-4-2-3-1.
- **ATTR:** [ATTR-008](../experiments/ATTR-008-design.md): Unterschied der Grenzwerte
  zwischen zwei Ausgangsniveaus, Positionen und Taktiken; Verwertung und
  Torwartverhalten mit echten Toren/Punkten prüfen. Historische ATTR-001–007
  bleiben unverändert und liefern keine aktuelle Buildfreigabe.
- **TRAIN:** [TRAIN-002](../experiments/TRAIN-002-design.md): kontrollierte gepaarte
  Karriereableger und tatsächliche Teilnahme statt theoretischer Sessionlisten.
  Langfristige Entwicklung und kurzfristige Spielleistung getrennt berichten.
- **SET:** [SET-001](../experiments/SET-001-design.md): tatsächlich entstandene
  Situationen als Exposition und Konterketten als mögliche Nebenwirkung.
- **MECH:** [MECH-001 und Mechanikregister](../experiments/MECH-001-design.md):
  Spielschärfe zuerst; danach kausal isolierbare Fitness-, Positions-, Moral-,
  Standort- und Spielmanagementeffekte.

## Evidenz und Übergang zur Praxis

Jede Ergebniszeile erhält eine der Klassen **Hypothese**, **explorativ**,
**vorläufig repliziert**, **bestätigt im Testkontext**, **extern repliziert**.
Ein neuer Seedpool auf derselben Maschine bestätigt nicht automatisch einen
neuen Gegner-, Club- oder Karrierekontext. Externe Replikation verlangt eine
unabhängige Ausführung mit ausreichender Eingabe-/Buildprovenienz.

Übergang in einen realen Save erst nach: (1) gehaltenen Gegnern und Stärken,
(2) geprüftem Startzustand und Ausführungs-/Komplexitätseinfluss,
(3) kontrollierten Karriereablegern einschließlich Kalender und Matchmanagement.
Fehlt eine dieser Stufen, wird die Empfehlung ausdrücklich auf das Labor begrenzt.

## Aktualisierung nach Runde3

[ATTR-009](../experiments/ATTR-009-results.md):384Matches/32Blöcke,Moderator
−0,162xGD[−0,488;+0,164],unklar,keineGloballiste. Weiterer Erkenntnisgewinn
zuerst durch passive Zustandsmessung und realistischere positionsabhängige
Profile,statt automatischeFallzahlvergrößerung derselben Interaktion.
MECH-002 und TRAIN-002 bleiben wegen tatsächlicher Mess-/Semantikgates blockiert;
SET braucht echteAusführungsexposition,TACT neueOOP-/Rollenfragen nachProfilabnahme.
Die [aktuelle priorisierteListe](round3/PRIORITIES.md) nennt technischeAbhängigkeiten,
getrennteBudgetvorschläge und Freigabekriterien. Keine neue Studie wird daraus
automatisch gestartet;Holdouts/Karriere-Replays bleiben unangetastet.

# NIGHT-001 – externe Evidenz, erster geprüfter Abschnitt

14.11.2026. Zehn gezielt ausgewählte Primärseiten wurden gelesen, nicht zehn
unabhängige Studien repliziert. [Register](../../data/night-001-evidence/sources.json)
enthält Zugriff in UTC, Quellfamilie, Versionsbezug, Autor-Fallzahlen, Endpunkte,
Missingwerte und Kritik. [Transportbelege](../../data/night-001-evidence/access-checks.json)
halten zehn erfolgreiche anonyme HTTP-Abrufe und zwei alte404-Endpunkte fest.
Keine vollständigen Artikel, Bilder oder FMF-Anhänge werden übernommen.

## Was die zehn Quellen tragen

| Register-ID / Primärseite | Geprüfter Inhalt und Entscheidung |
|---|---|
| NIGHT-SI-TRAIN · [Hersteller: Training](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness) | Vier Effektivitätskomponenten und Trennung von Mannschaftsvorbereitung/individueller Entwicklung. Keine gemessenen Gewichte oder Lernraten. |
| NIGHT-SI-ENGINE · [Hersteller: Engine](https://www.footballmanager.com/fm27/features/fm27-tactical-tweaks-and-match-engine-upgrades) | Stamina soll wiederholte Sprints und Konditionsabfall stärker beeinflussen. Neue testbare Hypothese, kein numerischer Attributrang. |
| NIGHT-ARENA-STATUS · [Patchtabelle](https://fm-arena.com/tactic-testing/aggregators/1/) | Nur eine sichtbare Dummy-Zeile/PLD600, Label27.0.0. Nicht als echte600-Spiele-Studie oder breites Ranking zählen. |
| NIGHT-ARENA-ATTR · [ZaZ: Attribute](https://fm-arena.com/threads/player-attributes.59/) | Harvestgreen-/squirrel-Aufbereitung; lineare Zwischenwerte sind Annahmen. Keine neue unabhängige Replikation. |
| NIGHT-ARENA-TRAIN · [ZaZ: Trainingsplan](https://fm-arena.com/threads/training-schedules.60/) | Konzentrierte Trainingstage und Resttage werden empfohlen. Prozent-, Verletzungs- und Schwellenbehauptungen bleiben unbestätigt. |
| NIGHT-ARENA-SET · [ZaZ: Standards](https://fm-arena.com/threads/set-pieces.61/) | Routineanhang und Screenshots, keine Ausführungsexposition oder Wirksamkeitsserie. |
| NIGHT-ARENA-POS · [Purity: Positionen](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/) | Berichtet200000Matches/50000Konfigurationen;250Koeffizienten. Ein Club/eineTaktik, keine verlinkten Rohjobs. Explorative Fremdevidenz. |
| NIGHT-MAC-POS · [Mac17/17b](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/17-positions-in-and-out-of-possession.md) | Positionsrating-Eingriffe bei fixierter Familiarity. Beantwortet keinen JR-versus-Speed×Masken-Kontrast und beweist keinen Zonenmediator. |
| NIGHT-MAC-TWEAK · [Mac8](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/08-tactical-tweaks.md) | Ganzmatch-Tweaks ab Anpfiff. Keine Aussage über optimalen späten Einsatz oder Ertrag je ausgeführtem Standard. |
| NIGHT-ARENA-EDITOR · [Editor-Testmodus](https://fm-arena.com/threads/how-to-get-fm27-pre-game-editor-for-free-and-use-it-to-run-tests-without-fm27.113/) | Beschriebener Test-Competitions-Pfad. Simulationsumfang und Karriereäquivalenz nicht validiert; nichts installiert/ausgeführt. |

Die macOS-Schnittstellenbeschreibung und ausgewählte CLI-Zeilen von
`scripts/study.py` wurden am selben unveränderlichen Commit zusätzlich gelesen.
Das ist ein Quellvergleich, keine Windows-Kompatibilität oder Ausführung.
ZaZs Seiten sind Primärbelege seiner Aussagen; für zugeschriebene Experimente
sind sie Sekundärzusammenfassungen. Registereinträge derselben Quellfamilie
werden nicht als unabhängige Bestätigung gezählt.

### Wichtige Versions- und Interpretationsgrenzen

Die früher verwendeten Endpunkte
[`/table/26-player-attributes-testing/`](https://fm-arena.com/table/26-player-attributes-testing/)
und [`/thread/20917-fm27/`](https://fm-arena.com/thread/20917-fm27/) lieferten am
Abrufzeitpunkt404. Das beweist weder die Nichtexistenz historischer Forschung
noch eine heutige FM27-Rangfolge. Suchtreffer alter Tabellen bleiben kein
Nachweis eines aktuell erreichbaren Datensatzes.

Puritys Koeffizienten sind bedingt auf seine Konfigurationen und3-4-2-1.
Vier Seeds je Konfiguration sind beschrieben; eine globale Seedliste fehlt.
Clamping kann Eingriffsverteilungen ändern. Konfigurationscluster und ein
Split-Hälften-Filter belegen keine universelle Präzision oder vorregistrierte
Fehlerkontrolle für250Entscheidungen. Der behauptete Präzisionsfaktor ist hier
nicht nachgerechnet. Seine Werte werden nicht als lokale Powerbasis verwendet.

Herstellerbeschreibung und Forumshypothese können dieselbe sinnvolle Frage
motivieren, ohne einander als kontrollierte Replikationen zu bestätigen.
Für Shouts beschreibt SI eine Änderung der mentalen Zustände statt kleiner
Attributboosts. Alte Zurufregeln und ein bloßer Moralfeldsetter belegen diese
Semantik nicht; Kontext/Spielerreaktionen benötigen eigene passive Messbelege.
Ein Transporthash identifiziert die abgerufenen Bytes; bei dynamischem HTML ist
er keine unveränderliche Remoteversion und erst recht kein Matchdatenbeleg.
Unbekannte Build-/Hosthashes bleiben `null`.

## Drei neue, isolierbare Fragen – Vorschläge, keine registrierten Läufe

### Q1: Stamina × Pressing im kontrollierten D00-Kontext

Hat eine definierte native Stamina-Dosis40→80 einen durchschnittlichen
xGD-Effekt, und ändert Pressing dessen Größe? Die rohe Dosis wird ausdrücklich
nicht ungeprüft in FM-Anzeigepunkte übersetzt. Katalogposition52 ist der
Stamina-Feldname im vorhandenen Tactics-Lab-Quellkatalog; dies allein ist noch
kein neuer nativer Readbacknachweis.

Enger voller2×2-Entwurf: Stamina40/80 × Standard/MoreOften, alle anderen
Fähigkeiten60 und D00-Rollen/Phasen/Profile/Management unverändert. Beide bekannten
Discoverygegner und beide Seiten, keine Holdouts. Primär marginaler Staminaeffekt
auf xGD, sekundär genauHolm7: dessen Punkte/GF/GA/xGF/xGA sowie Pressing- und
Stamina×Pressing-xGD. Interaktion wird nicht als kleiner, bereits gepowerter
Primäreffekt verkauft. Ohne passiven Verlaufsbeleg ist nur der totale
Matcheffekt identifiziert, nicht der Ermüdungsmechanismus.

Vorschlag32neueSeeds je Gegner=64Blöcke/512Mainmatches, separat32technische
Vollmatches+1Negative;600Child-/1200UTC-Sekunden, maximal4Worker/90s,
2GiBprivateArtefakte. Neue Dosis zuerst in allen69Attributen/23Profilfeldern,
beidenPhasen/PI und Seeds nach Originalvorbereitung prüfen; A/A/Negativkontrollen,
publizierter Vertrag/Code/Seeds und unabhängige Abnahme vor Main. Neue Kontrast-SD
unbekannt:0,30xGD ist eine praktische Planungsschwelle, keine90-%-Powergarantie.
Kein Ersatzseed, kein automatischer Ausbau.

### Q2: Gleiches Wochenpensum konzentriert oder verteilt

Die Hypothese ist eine Änderung der tatsächlichen Expositionstage bei gleicher
vorab festgelegter Sessionmenge. Erst müssen Rest/Reha/Absage, individuelle
Teilnahme, beide Schärfefelder, Verletzungsbeginn/-ende und unabhängige Karriere-
RNG/Cluster lesbar sein. Ohne sie sind weder eine Verletzungsrate noch
Entwicklung je absolvierter Einheit kausal interpretierbar.

Jetzt0Kalenderadvances. Nach eigenem technischen Vertrag höchstens8Armwochen/
30Minuten in einem seriellen Executor; danach erst Varianz-/Expositionsplanung.
Ein identischer Saveklon ist ein gepaarter Start, kein neuer unabhängiger
Karriereprozess. Individuelle Trainings- und Mannschaftsvorbereitungsziele
getrennt behandeln; keine nachträgliche Anpassung für behandlungsbedingte
Verletzungen oder Minuten. Keine wissenschaftliche Fallzahl aus Einzelspielzeiten
oder aus22Spielern eines Kaders ableiten.

### Q3: Eigene Eckzielzone bei gleicher Restabsicherung

Nach technischer Ereignisfreigabe eine Zielzonenänderung bei gleicher Swing-
politik, Schützen-/Zielspielerprofilen und Restabsicherung vergleichen.
Messung braucht tatsächliche Ausführung, Schuss-xG/Tor-/VAR-Zuordnung und
Konterketten; Selektionslogs allein bleiben kein Nenner.

Zuerst Offline-Goldfälle und echte positive/negative Mappingbelege, jetzt
0Wirksamkeitsmatches. Ein späterer256Match-Varianzpilot hätte im2Arm-/2Seiten-
Design64unabhängigeKontextseeds; die Expositionsrate und nötige Fallzahl bleiben
unbekannt. Nettoertrag pro100ausgeführtenEcken und unbedingte Matchleistung
getrennt berichten. Nullnenner nicht alsNullrate ausgeben; sparse Bootstrapfälle
vor Registrierung methodisch behandeln. Keine Routine aus Downloadzahlen wählen.

## Tatsächlich geliefert und geprüft

Dieser Agent startete **0native Prozesse/Matches,0Seeds und0Karriereadvances**.
Keine Spielstände, FMF-Anhänge, privaten Matchdumps oder Holdouts geöffnet.
Nur neue eigene Dateien; historische Register und Studien unverändert.

`analysis/audit_night_evidence.py` prüft Struktur, Zugriffshashbindung,
Unbekanntwerte und die Trennung von Seitenlektüre/Replikation. Der Auditor
prüft **nicht** die Wahrheit der Fremdergebnisse. Sechs Regressionstests
verhindern unter anderem, dass eine Dummy-PLD oder einHTTP200 als eigene
Studienstichprobe bzw. Replikation geführt wird. Alle sechs gezielten Tests,
130Repositorytests und fünf historische Analysetests bestanden im Fachworktree;
`git diff --check` ohne Befund. Veröffentlichung/Integrations-CI und weitere
Aufträge bleiben zentral beim Director.

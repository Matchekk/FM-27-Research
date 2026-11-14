# Externe Forschung und Evidenzregister

Geprüft am 14.11.2026. [Maschinenlesbares Register](../research/external-studies.json).
Quellenbehauptung, technische Toolvalidierung und unabhängige wissenschaftliche
Replikation werden getrennt. Kein hier gelisteter externer Befund wurde in diesem
Auftrag lokal repliziert. Forenpost und Repository desselben Autors zählen als
eine Quellenfamilie. Die Liste ist eine gezielte Ausgangsbasis, keine vollständige
systematische Literaturübersicht.

| ID | Quelle / Version | Datengrundlage und Zugang | Einordnung und Konsequenz |
|---|---|---|---|
| EXT-WIN-001 | [Tactics Lab v1114.6](https://github.com/lqf0624/fm-tactics-lab/releases/tag/v1114.6), `91f2eba` | Offizieller Windows-Host, Steam-Hotfix 27.0.1+2503222; lokaler VALID-002 ergänzt tatsächliche Messungen | Technische Quelle, kein Beweis taktischer Überlegenheit oder des vollständigen Karriereablaufs |
| EXT-MAC-001 | [Attributstudie 1](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/01-attribute-values.md) | Autor nennt 32.700 Matches, zehn gespeicherte Begegnungen, 54 Attribute und je 300 gepaarte Kontraste; 27.0.1, genauer Studien-DLL-Hash hier nicht festgestellt | Externe explorative Evidenz; Zielmetriken und Eingriffszeitpunkt wichtig. Verwertung zusätzlich über Tore/Punkte prüfen |
| EXT-MAC-002 | [Fixture-/Profilvergleich](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/02-real-vs-levelled.md) | Autor nennt 65.400 Matches; reale Profile, nivellierte Profile und generisches Fixture | Nicht nur Attribute unterscheiden die Fixturearme. Anlass zur Kontextreplikation, kein isolierter Beweis eines einzigen Fixturemechanismus |
| EXT-MAC-013 | [Positionswerte](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/13-value-by-position.md) | Autor nennt 15.680 Matches, synthetische mittlere Kader, mehrere Gegner/Seiten; 27.0.1 | Nichtsignifikante Positionsunterschiede sind keine Gleichheit. ATTR-008 soll konkrete lokale Kontraste und deren Präzision prüfen |
| EXT-MAC-015 | [Heimvorteil / Moral](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/15-home-advantage-morale.md) | Autor nennt 2.480 Matches, darunter gleiche Teams über zwölf Grounds | Standort und feste native Seiten sorgfältig trennen; keine universelle Heimkorrektur aus einem Labfixture |
| EXT-MAC-OPT | [Optimierer](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/scripts/optimise.py) | Quellcode für Screening, Ridge und gehaltene Gegner; keine eigene Ausführung auf Windows | Methodische Referenz. Dessen Hinweis auf nicht neu berechnete Komplexität begrenzt Praxistransfer; konventionelle t-Schwellen ersetzen keine registrierte Testfamilie |
| EXT-FORUM-001 | [caiogracos FM-Arena-Beitrag](https://fm-arena.com/threads/fm27-match-engine-what-we-know-so-far.122/) | Autorenzusammenfassung derselben Mac-Studien, veränderliche Webseite | Gleiche Quellenfamilie wie EXT-MAC; keine zweite Replikation. Gleichsetzung mit Instant Result wird hier nicht übernommen |
| EXT-HG-001 | [harvestgreen22](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test), Seite seit 04.11.2026 | Beschrieben: standardisierte Spieler/Coaches, fixierte Zustände, fünf Gegnerformationen; verlinkte Tabellen hier nicht heruntergeladen/rohdatengeprüft; exakter Buildhash fehlt | Explorative externe Quelle, stark kontrollierter Kontext. Für Trainingskausalität sind tatsächliche Einheiten und unabhängige Saveableger weiterhin nötig |
| EXT-DELICIOUS-001 | [FMDelicious-Methodik](https://fmdelicious.com/methodology), `vac-3clubs-fm27 v1` | FM27-Beta: bis zu drei Clubsaisons bzw. 114 Ligaspiele pro Taktik; genaue Matchengine-Provenienz dort nicht vollständig belegt | Praxisreferenz mit Stärkestrata; eine Clubsaison ist keine große unabhängige Matchstichprobe. Nicht mit 6.000er-FM26-Protokoll verwechseln |
| EXT-SI-001 | [Offizielle Updateinformation](https://community.sports-interactive.com/forums/topic/612665-fm27-minor-update-1-rolling-out-now-plus-more-info-on-updates/) | Produkt-/Updatebeschreibung, keine gepaarte Messserie | Anlass für Buildüberwachung; ersetzt weder tatsächliche lokale Buildermittlung noch Hash-/Regressionsprüfung |

Bei jedem Eintrag zusätzlich festhalten: Zugriffstag, immutable Commit oder
Webseitenstand, vom Autor genannter Build und Host, Stichprobeneinheit, tatsächliche
Messzahl, Eingriffs-/Ausschlussregeln, Seeds, Korrektur der Testfamilie, verfügbare
Rohdaten und unabhängige Reproduktion. Fehlende Angaben bleiben **unbekannt**.
Die hier genannten externen Matchzahlen sind ausschließlich Autorenangaben.

Neue Forschung wird bevorzugt, wenn sie einen klaren Mehrwert bietet: kausal
getrennte Interaktionen, kontrollierte Eckexposition, Trainingsableger, gehaltene
Gegner und Tore/Punkte dort, wo xG den Mechanismus nicht abbildet. Ein weiteres
ungeprüftes globales Attributranking ist nachrangig.

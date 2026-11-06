# Arbeitsanweisungen für Codex – FM27 Meta Research

## Mission
Forsche systematisch zur FM27-Meta und dokumentiere nachvollziehbare, wiederholbare Ergebnisse. Dieses Repository ist **das versionierte Forschungsarchiv**; lokale Simulationsprogramme, Spielinstallationen und fremde Repositories werden nicht ungefragt kopiert oder umstrukturiert.

## Vor jedem Auftrag
1. Lies `README.md`, `METHODOLOGY.md`, `FINDINGS.md`, `NEXT_STEPS.md` und das relevante Experimentdokument.
2. Prüfe `git status`, aktuelles Branch-Tracking und den aktuellen Remote-Stand, bevor du Dateien änderst.
3. Ermittle tatsächliche Versionsnummern von FM27 und verwendeten Tools. Keine angenommenen Buildnummern als Testfakt ausgeben.
4. Prüfe die konkrete Quelle lokaler Vorarbeiten; Gesprächszusammenfassungen gelten ohne importierte Belege als **nicht unabhängig verifiziert**.

## Bei Experimenten
- Definiere vor der Ausführung Hypothese, primäre Zielgröße, Ein-/Ausschlüsse, Variablen, Seed-Strategie, Stichprobengröße und Auswertung.
- Lege ein Experimentdokument unter `experiments/` an, mit eindeutiger ID, Manifest-/Run-Dateiverweisen und Buildangabe.
- Nutze kontrollierte, gepaarte Vergleiche; ändere nur die für den Versuch deklarierte Intervention.
- Verifiziere, dass Attribute/Anweisungen tatsächlich in der Engine ankommen. Vorher Baseline- und deterministische Wiederholungstests.
- Bewahre Fehlversuche, Abbrüche, Mismatchs, Missing Values und Ausschlussgründe auf. **Niemals stillschweigend als Null behandeln.**
- Speichere pro Lauf Setup-Hash, Build, Adapterversion, Teams/Taktiken, Seed, Intervention, Teamseite und Resultate.
- Bei abweichenden Builds oder nicht validiertem nativen Adapter die Testserie stoppen und den Blocker dokumentieren.
- Keine unbewiesene Gleichsetzung von externem Engine-Adapter, normaler Karrierepartie, Urlaub und Instant Result.

## Forschungsstandard
- Berichte immer Effektgröße, Unsicherheit, Stichprobenumfang, Ausfälle und Grenzen.
- Trenne exploratives Screening von vorab festgelegter Bestätigung an **neuen** Seeds/Szenarien.
- Multiple Tests berücksichtigen und sowohl statistische als auch praktische Relevanz berichten.
- Keine „OP“-Behauptung ohne Replikation über zusätzliche Aufstellungen/Gegner.
- Negative und uneindeutige Ergebnisse genauso dokumentieren wie positive.
- Alte Ergebnisse nie still überschreiben; mit Build, Datum und Versionsbezug archivieren.
- `FINDINGS.md` nur mit nachvollziehbaren Quellen/Experimentlinks ergänzen.

## Dateiformate
- **Markdown:** Forschungsberichte, Annahmen, Design, Interpretationen, Änderungslog, Roadmap.
- **JSON/JSONL:** Konfigurationen, Metadaten und kompakte Rohmessungen.
- **CSV:** nur als Export, wenn tatsächlich für externe Auswertung oder Veröffentlichung benötigt.
- Keine Gigabyte-Rohlogs in Git. Stattdessen verifizierbare Zusammenfassungen und ggf. gehashte externe Artefakte.

## Git-Workflow – verbindlich
1. Nach **jedem abgeschlossenen, validierten Arbeitsabschnitt/Experiment** relevante `.md`-Dateien aktualisieren.
2. `git diff`, `git status`, Dateigrößen und potentielle Secrets prüfen.
3. Verständlichen Commit erstellen (z. B. `research(attributes): add paired-seed screening results`).
4. **Commit auf den dafür vorgesehenen Remote-Branch pushen** (standardmäßig `origin/main`, soweit ausdrücklich so eingerichtet). Kein Force-Push; fremde Commits nicht überschreiben.
5. Bei Konflikten sicher synchronisieren oder einen separaten Branch/PR nutzen. Ist Push technisch nicht möglich, klar als **nicht gepusht** melden und SHA/Blocker angeben.
6. Nach Push SHA, Branch, veröffentlichte Dateien, gemessene Erkenntnisse und verbleibende Fragen zusammenfassen.
7. Auch bei längerem Versuch den abgeschlossenen Zwischenschritt nachvollziehbar committen/pushen, nicht unvalidierte Zahlen als Befunde darstellen.

## Sicherheit und Veröffentlichungsgrenzen
**Dieses Repository ist derzeit öffentlich.** Nie `*.fm`-Spielstände, FM-DLLs/-Archive/-Assets, lizenzierte Inhalte, `*.exe`, Zugangsdaten, Tokens, private Pfade mit personenbezogenen Daten, personenbezogene Spieler-IDs aus privaten Quellen oder vertrauliche Daten pushen. Vor Veröffentlichung prüfen, ob der Inhalt geteilt werden darf. Referenziere fremde Projekte über Links und Versionen, nicht über kopierte geschützte Dateien.

## Aufgabe abgeschlossen?
Erst wenn Dokumentation, Plausibilitäts-Checks, Teststatus und Push-Status eindeutig feststehen. Bei unvollständiger Testserie nur einen Zwischenstand als solchen dokumentieren.

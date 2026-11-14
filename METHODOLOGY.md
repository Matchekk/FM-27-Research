# Methodik – FM27 Meta Research

Version: 0.1 · Stand: 2026-11-06

## 1. Evidenzstufen
- **Hypothese:** plausibler, noch nicht getesteter Mechanismus.
- **Explorativ:** beobachteter Effekt aus Screening, unzureichender oder selektierter Stichprobe.
- **Vorläufig repliziert:** unabhängige neue Seeds liefern einen vergleichbaren Effekt, aber Generalisierbarkeit offen.
- **Bestätigt im getesteten Kontext:** vorab definierte Auswertung, Qualitätsgates, Unsicherheit und unabhängige Wiederholung erfüllt. Nicht automatisch allgemeingültig für jede Liga, Taktik und Buildnummer.
- **Unklar/widerlegt:** Daten erlauben keine Richtungsaussage bzw. widersprechen Hypothese; Unterschiede innerhalb einer praktisch relevanten Äquivalenzspanne erfordern gesondertes Design.

## 2. Pre-Registration vor dem Lauf
Jedes Experiment legt vor Ausführung fest:
- eindeutige Kennung, Zeit/Version, Start-Setup und SHA256
- präzise Hypothese und **eine primäre Zielgröße**
- Kontroll- und Interventionsgruppe (nur deklarierte Änderungen)
- Einheit der Analyse, Seeds, Anzahl, Wiederholungen, Heim-/Auswärts-Design
- Gegner, Taktiken, Attribute, Positionen und Startbedingungen
- Ausschlussregeln, Fehlerbehandlung, Plausibilitätsgrenzen
- Analyseverfahren, Konfidenzniveau, Multiple-Testing-Regel und kleinste praktisch relevante Effektgröße
- bekannte Grenzen und gegebenenfalls eine separate Validierung im Karriere-Save

## 3. Gepaarte Matchengine-Versuche
Standard-Primärmetrik für Attribut-/Taktiktests:

`delta_xgd = (xG_for - xG_against)_intervention - (xG_for - xG_against)_baseline`

Für jede Paarung denselben Seed, dieselben Kader, dieselbe Teamseite, Gegner, Taktiken und vorbereiteten Startzustand verwenden. Resultate je Seed als Paar speichern. **Gleicher Seed ist eine Varianzreduktion, kein Garant für identische Ereignisfolgen oder statistische Unabhängigkeit.**

Sekundär: Tor-/Punktedifferenz, xG für/gegen, Schüsse, Schüsse aufs Tor. Bei Testläufen mehrfach pro Seed oder gleichem Szenario Clusterung/Abhängigkeiten beachten. Matches mit Fehlern nicht in Aggregaten kaschieren.

**Bekannte externe Modellgrenze:** FM Tactics Lab nutzt nach Projektdokumentation die detaillierte FM27-Matchberechnung, aber nicht zwangsläufig alle Karriere-, Live-Coaching- und Spielzustandsabläufe. Standardisierte Fitness/Spielschärfe/Moral sind kein Ersatz für Karrieredaten. Quelle: https://github.com/lqf0624/fm-tactics-lab/blob/main/docs/SIMULATION_FIDELITY.md

## 4. Statistische Auswertung
- Zunächst Datenqualität, Stichprobe, Fehlerquoten, Effektverteilungen und Baseline-Differenzen prüfen.
- Für `delta_xgd`: Mittelwert, Standardabweichung, 95-%-Intervall mit auf Paar-/Cluster-Ebene geeignetem Bootstrap; robuste Sensitivitätschecks.
- Explorative Mehrfachvergleiche kennzeichnen; gewählte Fehlerkorrektur (z. B. Benjamini-Hochberg/FDR) mit Zahl der getesteten Hypothesen dokumentieren.
- Konfirmatorische Serie mit **neuen Seeds** und vorher eingefrorenen Kandidaten/Entscheidungsregeln durchführen.
- „Nicht signifikant“ bedeutet **nicht** automatisch „kein Effekt“. Praktische Effektgröße und Präzision gemeinsam beurteilen.
- Taktik-Rankings sollten mindestens verschiedene Gegnerprofile, Heim/Auswärts sowie unterschiedliche Spielstärken abdecken.
- Buildwechsel können Ergebnisse entwerten: bei Änderungen der Match Engine Hauptbefunde erneut testen.

## 5. Trainingsversuche
- Nach Möglichkeit dieselben Spieler aus einem identischen Anfangssave, gleiche Spielbelastung, Kader/Trainer, Termine, Spielminuten und absolvierte Trainingseinheiten.
- Eine gezielte Variable ändern, etwa `Conditioning` vs. `Heavy Conditioning`.
- Primär: Veränderung der vorher definierten Rohattribute pro Spieler. Zusätzlich CA, PA, Kondition, Ermüdung, Verletzungstage, Einsatzminuten und tatsächlich absolvierte Einheiten getrennt ausweisen.
- Wiederholung aus bytegleichen Startdateien erforderlich, um Zufallsvariabilität zu schätzen.
- Nicht aus hinterlegten Trainingsziel-Listen allein auf beobachtetes Attributwachstum schließen.

## 6. Reproduzierbarkeit und Provenienz
Jedes Experiment besitzt ein Markdown-Protokoll, ein maschinenlesbares Manifest und Rohmessungen (`.jsonl` oder extern referenzierte, gehashte Daten). Dazu gehören Spiel-Build, Adapter-/Toolversion, Setup-Hash, Seedrange, Zeitstempel, Kontrollfaktoren, Ergebnispfade und Auswertungscode/Commit-SHA. CSV ist abgeleiteter Export, keine maßgebliche Datenquelle.

**Keine im Repo belegten Daten = kein im Repo bestätigter Befund.**

## 7. Plattformstandard 2.0 (Ergänzung vom 14.11.2026)

Historische Methoden und Ergebnisse oben bleiben unverändert ihrem damaligen
Build zugeordnet. Neue Studien erfüllen vor Start alle folgenden Punkte:

1. Veröffentlichte Hypothese mit eindeutiger ID und eingefrorenem Analysecommit.
2. Kontrollarm und vollständig deklarierte Intervention.
3. Genau eine primäre Zielgröße bzw. explizit korrigierte primäre Testfamilie.
4. Vollständig vorab benannte sekundäre Zielgrößen.
5. Feste Start-, Team-, Gegner-, Seiten- und Managementbedingungen.
6. Native Eingabeprüfung nach Originalvorbereitung; JSON allein genügt nicht.
7. Neue reservierte Seeds, disjunkt zu Archiv, Fehlversuchen und anderen Phasen.
8. Power-/Präzisionsplan mit Analyse-/Clustereinheit, SD-Annahmen und Sensitivität.
9. Geeignetes gepaartes oder longitudinales Modell; Abhängigkeiten erhalten.
10. Effekt in praktischen Einheiten und Konfidenzintervall, nicht nur p-Werte.
11. Vorab festgelegte Multiple-Testing-Korrektur einschließlich vollständiger Familie.
12. Strikte Trennung von Entdeckung, Auswahl und gehaltenen Bestätigungsdaten.
13. A/A, Negativkontrollen, Zähler- und Plausibilitätsprüfungen.
14. Vollständige Ausfälle, ausstehende Jobs, Ausschlüsse und Retries mit Gründen.
15. Neue technische Freigabe nach relevantem Engine-, Host-, Ressourcen- oder Eingabewechsel.

Gleiche Seeds verbinden Arme zu Blöcken; sie garantieren keine identischen
Spielereignisse. Gemeinsame Baselines, Seiten und Spielerkohorten zählen nicht
mehrfach als unabhängige Beobachtungen. Ein Suchgewinner wird ausschließlich
mit eingefrorenen Eingaben, unbenutzten Seeds und gehaltenen Gegnern bestätigt.
Wird auf Bestätigungsdaten weiter optimiert, sind diese danach Entdeckungsdaten.

Evidenzklassen für neue Berichte: **Hypothese**, **explorativ**, **vorläufig
repliziert**, **bestätigt im Testkontext**, **extern repliziert**. Die letzte
Klasse verlangt eine unabhängige Ausführung mit überprüfbarer Provenienz;
ein zweiter Post desselben Experiments genügt nicht. Unklare/negative Befunde
behalten dieselben Dokumentationspflichten. Fehlende Signifikanz beweist keine
Äquivalenz; diese braucht eine vorab definierte Spanne und geeignete Prüfung.

In der Taktiksuche sind xGD und modelliertes xPts Screeninghilfen. Bestätigung
verwendet tatsächliche Punkte sowie Tore/Gegentore. Finishing, Torwartleistung,
Verletzungen und Training verlangen mechanismengerechte Endpunkte und Exposition.
Die [Plattform](docs/PLATFORM.md) automatisiert gemeinsame Gates; sie ersetzt
keine experimentbezogene Analyse oder Karrierevalidierung.

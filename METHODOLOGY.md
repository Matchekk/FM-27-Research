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

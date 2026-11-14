# MECH-002-SHARPNESS-P0: Ergebnisgrafik

Vorbereitung vom 14.11.2026 auf Basis `0adf47b`. Der neue eigenständige
[Renderer](../../analysis/render_sharpness002.py) liest ausschließlich öffentliche
JSON-Dateien. Keine Imports des Projektanalysers, Runners oder nativen Adapters;
keine Änderung des eingefrorenen Analysecodes. Keine Hypothese, Seeds,
Simulationen, UI-/Computersteuerung oder neue statistische Testfamilie.

## Darstellung und Grenzen

Zwei Panels: marginaler Effekt des ursprünglichen Startpakets Raw10000 minus
Raw7000 auf xGD (primär) und tatsächliche Punkte (sekundär, Holm7-Vermerk).
Je Panel stehen Gesamtmittel mit veröffentlichtem marginalem Welch95- und
stratifiziertem Seedblock-Bootstrap95-Intervall sowie beide Kontextmittel.
Die Kontextintervalle werden aus Kontext-SD und 32 vollständigen Seedblöcken
als `Mittel ± t(.975,31) × SD/sqrt(32)` berechnet. Sie sind ausdrücklich
deskriptiv/explorativ und nicht simultan; keine neuen Moderatorentests.
Keine Sterne, signifikanzabhängige Auswahl oder Farbgebung. Zwei Einheiten
erhalten getrennte beschriftete Achsen; alle vier Zeilen werden dargestellt.

Die Figur nennt registrierten Build, 512 Matches / 64 Blöcke, D00, synthetisches
Fixture, beide bekannten Discoverygegner und beide Seiten. Quellen werden durch
gekürzte SHA256 von effects/summary/manifest identifiziert; der CLI-Beleg enthält
volle Inputhashes beim `--validate-only`-Aufruf. Kein UI-Prozent-, Consumer-,
Mediations-, Karriere- oder allgemeiner Meta-Nachweis wird dargestellt.

## Striktes Ausgabegate

`effects.json` muss das tatsächliche Schema und 512 Matches / 64 unabhängige
Seedblöcke, die genaue Holm7-Familie und den registrierten Rohpaketkontrast tragen.
`main-summary.json` muss `phase=main`, `full_matches=512`, keine Mainabweisung
und jeweils exakt `true` für `passed`, `complete`, `budget_reconciled` und
`scientific_analysis_allowed` enthalten. Gewichte, Kontextanzahl und SD/SE werden
auf Konsistenz geprüft; der veröffentlichte Vertrag muss 32 Blöcke pro Kontext,
beide Seiten und ausschließlich Discoverykontexte festlegen. Nichtfinite Werte,
duplizierte JSON-Felder, fehlende Freigaben oder falsche Interpretation blockieren.

Diese Format-/Freigabeprüfung ersetzt **keine unabhängige Nachrechnung aus den
Rohmessungen**. Der Director darf die tatsächliche Grafik erst nach vollständigem
Main und Analyse-/Rohbelegreview veröffentlichen. Es liegen bei Erstellung dieses
Renderers noch keine von ihm verwendeten tatsächlichen Hauptresultate vor.
Es wurde daher weder eine echte noch eine fingierte FM-Ergebnisgrafik erzeugt.

## Späterer Aufruf durch den Director

Zuerst ohne Ausgabe prüfen:

```powershell
python analysis/render_sharpness002.py --effects data/mech-002-sharpness-p0/effects.json --summary data/mech-002-sharpness-p0/main-summary.json --manifest data/mech-002-sharpness-p0/manifest.json --validate-only
```

Nach unabhängiger Abnahme dieselben Pfade mit
`--output data/mech-002-sharpness-p0/contrast-intervals.svg` verwenden.
Bestehende Ausgaben werden nicht überschrieben. Die selbständige SVG enthält
Glyphenpfade, festes `svg.hashsalt`, keine Datumsmetadaten und keine abschließenden
Leerzeichen. Für dieselben Eingaben und dieselbe Matplotlib-/Fontversion ist sie
deterministisch. Eine private PNG-Vorschau und Sichtkontrolle dürfen erst aus
tatsächlichen freigegebenen Daten erfolgen; jetzt keine Plotvorlage mit Testzahlen.

## Tatsächlich geprüfter Stand

- Syntax/Import/CLI-Hilfe und gültiges rein speicherinternes Formschema geprüft;
  kein Aufruf der Renderfunktion, kein Bildartefakt.
- 14 negative Form-/Freigabevarianten zurückgewiesen; Kontext-df31-Arithmetik
  geprüft. Der erste Formfixture enthielt einen NumPy-Skalar statt JSON-Float;
  nach Korrektur des Fixtures besteht die Prüfung, ohne Produktionsgate zu lockern.
- Zwölf bestehende Sharpness-Designchecks: elf bestanden, ein optionaler privater
  Binär-Goldtest mangels konfiguriertem Pfad übersprungen.
- Matplotlib 3.10.7 vorhanden. Keine neuen Abhängigkeiten oder alten Dateien.
- Diff-/Dateigrößenprüfung vor Commit; kein Push durch den Fachagenten.
  Director integriert den lokalen Commit auf `main` und prüft die Integrations-CI.

Noch offen: wirkliche Datenpfade/Release, unabhängige Rohbelegprüfung und
visuelle Abnahme des tatsächlichen SVG. Dieser Vorbereitungscommit behauptet
keine bereits bestandene visuelle Prüfung oder byteweise Rendering-Replikation.

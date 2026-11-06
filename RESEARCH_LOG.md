# Research Log

## 2026-11-06 – ATTR-004 abgeschlossen

- Alle 3.360 Hauptmatches der vorregistrierten acht Szenarien wurden angenommen. Das ergibt 1.120 vollständige Seed-Tripel auf Build `27.0.0+2493426` ohne fehlgeschlagene Hauptversuche oder Ausschlüsse. Die 96 technischen Läufe sind separat archiviert. [Manifest](data/attr-004/manifest.json)
- Der direkte Kontrast Sprunghöhe minus Antritt beträgt +0,021 xGD (95-%-KI −0,038 bis +0,080, p = 0,479). Das Intervall liegt innerhalb der praktischen Schwellen. Beide Attribute verbesserten xGD gegenüber Baseline im Szenariomittel. Keiner der 21 Kontexttests war nach Holm signifikant. [Ergebnisse](experiments/ATTR-004-ergebnisse.md)
- Primärtest, alle 33 Sekundärtests und die Holm-Entscheidungen aus den publizierbaren Matchzeilen unabhängig nachgerechnet. Die ATTR-004-Analysetests und die Rechenprüfung des bisherigen Archivs bestanden.

## 2026-11-06 – ATTR-004 vorregistriert und technisch freigegeben

- Die [Vorregistrierung](experiments/ATTR-004-cross-tactic.md) und der Analysecode wurden in `ccfd630` vor dem ersten Match auf `main` gepusht. Acht Szenarien mit je 140 disjunkten Seeds und drei Armen sind festgelegt.
- FM27 meldete beim Start `27.0.0+2493426`. Engine, Host, Matchressourcen und Fixture stimmten mit VALID-001 überein.
- 96 technische Prüfläufe wurden akzeptiert. Alle 48 Wiederholungspaare stimmten bei Endstand, Teamstatistik und Endtick exakt überein. Die Übertragung der aktiven Profile auf beide Spielseiten und die nativen Attribut- und Taktik-Readbacks sind geprüft. Die getrennte ungültige Konfiguration wurde mit Exitcode 108 abgewiesen. [Validierungsbericht](data/attr-004/validation-summary.json)

## 2026-11-06 – Lokale Messdaten archiviert und nachgerechnet

- Build `27.0.0+2493426`, Adapter `fm27_desktop_2493426_adapter_v1`, Tactics Lab v1106. Der Ausgangsstand auf `main` war `fa436a2171fb2c3ed97b34e25d0f759d57d222e6`. Der Git-Verlauf führt den Commit dieser Archivierung.
- Für 2.504 akzeptierte Matches wurden native Logs und Startup-Belege abgeglichen. Zwei absichtliche Negativproben stehen getrennt im Archiv. Weitere 228 historische Matches sind separat erfasst.
- Die Archivprüfung reproduziert 2.080 Baseline-Kontraste, zehn direkte Attributkontraste und zwei Venue-Kontraste einschließlich Bootstrap-Intervallen, BH und BY. [Prüfskript](analysis/verify_matches.py)
- Die vorläufige Rangfolge des Screenings änderte sich in der Replikation. Sprunghöhe, Antritt und Tempo blieben als Einzeleffekte im Hauptszenario bestehen. Der ursprüngliche Heim-/Auswärts-Seitentausch scheiterte vor dem Start an ungleichen Kaderkapazitäten. Die korrigierte Variante verwendet zwei gleich große aktive Kader und gepaarte Seeds. [Hauptreplikation](experiments/ATTR-002-hauptreplikation.md) · [Zusatzszenarien](experiments/ATTR-003-zusatzszenarien.md)
- Die Karrierebeobachtungen verwenden zufällig vergebene Teilnehmerkürzel und Attributdifferenzen. Datenqualität und fehlende Wiederholungen begrenzen die Interpretation. [Karrierebericht](experiments/TRAIN-001-karriere.md)
- Dieser Archivschritt bestand aus Prüfung, Analyse und Veröffentlichung bereits vorhandener Messungen. Es wurde keine neue Simulation gestartet.

## 2026-11-06 – Repository-Grundlage
- Projektstruktur mit Markdown-first-Regeln und maschinenlesbarem Rohdatenformat vorbereitet.
- Repository ist zum Zeitpunkt der Anlage öffentlich.
- Es wurden **keine neuen Simulationen** in diesem GitHub-Schritt ausgeführt.
- Frühere lokale Arbeiten wurden in der Konversation beschrieben (FM26/FM27-Trainingsarchive, Conditioning-vs-Heavy, Jugendvergleich, erste Attributsensitivitäten), jedoch **noch nicht als überprüfbare Rohdaten in dieses Repository übernommen**.
- Nächste Aufgabe: vorhandene Artefakte sichten, Versionen verifizieren, Reproduzierbarkeit prüfen, dann erste neue Testserie ausführen.

## Neue Einträge
Für jeden Lauf Datum, Bearbeiter/Tool, Branch+SHA, Build, Experiment-ID, Ergebnis, Einschränkungen und Folgeschritt ergänzen.

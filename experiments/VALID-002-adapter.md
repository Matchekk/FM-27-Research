# VALID-002 – isolierte Adaptermigration

Technischer Prüfplan, angelegt am 14.11.2026 vor neuen Matchläufen.
Keine Hypothesenprüfung zur taktischen Leistung und keine ATTR-Replikation.

## Identität und Fragestellung

Kann v1114.6 auf der vorhandenen Windows-/Steam-Installation mit
`27.0.1+2503222` kontrollierte Eingaben verifizieren, natürlich beenden und
identische Seedläufe reproduzieren? Engine-SHA256:
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Upstreamcommit `91f2eba57fac0b7fbd3dff616056907e3ce461be`.
Adapter `fm27_desktop_8c6971ce_adapter_v1`, Host-SHA256
`2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`.
Die statische native Prüfung ist bestanden: verified, null Warnungen.

## Vorab festgelegter Umfang

- Höchstens 48 vollständige Matches, höchstens vier Worker, 90 Sekunden ohne
  Fortschritt je Worker; keine automatische Wiederholung gescheiterter Jobs.
- Zwei neue, gegen sämtliche archivierten JSONL-Seeds geprüfte technische Seeds.
  Zwei Wiederholungen von 4-2-3-1-Baseline und höherem Pressing, jeweils auf
  beiden Teamseiten: 16 Matches. Spielerprofile werden auf feste native IDs
  der Zielseite übertragen; aktive Kader werden auf 23 angeglichen.
- Ein Benchmark mit denselben acht Jobs bei 1/2/4 Workern: 24 Matches.
  Dies ist ein kleiner Durchsatzcheck einschließlich Startkosten, kein
  universelles Leistungsbenchmark und keine Powergrundlage.
- Bis zu zwei Läufe mit vollständiger Ereigniserfassung; bis zu zwei gespeicherte
  Karriere-PKM-Läufe, sofern der native Reader sie akzeptiert.
- FMF-Import einer vorhandenen lokalen 4-2-3-1 und Export/Reimport; semantischer
  Vergleich beider Phasen, Rollen, Team-/Spieleranweisungen und Mentalität.
- Negativproben: ungültiges JSON-Szenario, ungültige Rolle, ungültige FMF-Datei,
  ungültiges Binärsetup (erwartet Code 108); keine erfundenen Nullresultate.

## Annahmekriterien

Exakte Build-/DLL-/Host-/Ressourcen-/Fixturebelege; wirksamer Seed-Override;
Start 0:0; natürlicher Abschluss vor Watchdog; plausible native Teamstatistik;
vollständige Readbacks von Attributen, Positionen und Rollen in beiden Phasen,
Anweisungen und kontrollierten Startprofilen. Ergebnis, Endtick und Statistik
müssen bei gleicher Eingabe und Seed exakt wiederholbar sein und zwischen
Workerzahlen übereinstimmen. Jeder Versuch und Ausfall wird separat archiviert.
Bei Integritätsfehlern stoppen die abhängigen Prüfungen. Keine wissenschaftliche
Leistungsserie bei fehlender Freigabe.

## Reversibilität und Grenzen

Neue Runtime ausschließlich unter ignoriertem `local/`, aus dem per GitHub-
Assetdigest geprüften offiziellen Release extrahiert. Desktop-EXE nicht gestartet.
Bestehender v1106-Host, alte Forschung, Spielinstallation und Saves unverändert.
Die alte Engineversion wird nicht wiederhergestellt oder mit der neuen vermischt.
Ein gespeichertes Karriere-Match ist kein Karriere-Längsschnitt und seine erneute
Simulation beweist noch keine Gleichheit mit dem historischen Spielablauf.

Ergebnisabschnitt und publizierbare Messbelege folgen nach Ausführung.

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

## Reale Ergebnisse

**Teilfreigabe:** Der kontrollierte Betrieb auf dem mitgelieferten Fixture ist
bestanden. Gespeicherte Karrierefixtures und Karriere-Längsschnittversuche sind
weiterhin nicht freigegeben. Eine Freigabe neuer Rollen-/Anweisungskandidaten
erfordert deren eigenen nativen Eingabeaudit.

| Prüfung | Beobachtung |
|---|---|
| Aktueller Release | GitHub Releases/Tags am 14.11.2026 abgefragt; v1114.6 weiterhin neuester stabiler Tag |
| Lokaler Build | Spielstartlog vom 13.11.: 27.0.1+2503222; Dateiversion 27.0.1; Steam-Build-ID 26577676 |
| Native Kompatibilität | verified, null Warnungen, exakter Referenz-DLL-Hash |
| Kernserie | 16/16 Matches akzeptiert; vier Eingaben × zwei Seeds × zwei Wiederholungen |
| Wiederholbarkeit | 8/8 Vergleiche exakt in Score, Endtick und vollständiger publizierter Teamstatistik |
| Phasen / Rollen / Seiten | Beide Phasen und alle 22 Startspieler nativ geprüft; alle 69 Attributwerte pro aktivem Spieler, Rollen/Duties und Positionsmasken; 23 aktive Spieler je Seite |
| Seed-Override | Für jeden akzeptierten Lauf nativ geprüft; technische Seeds 2362620850 und 4019023467, vorab gegen altes Archiv geprüft |
| Worker / Wiederverwendung | 24/24 Benchmarkmatches akzeptiert; sämtliche Resultate stimmen mit Kernserie überein; Protokoll 2, natürliche Freigabe pro Match |
| Quick / vollständige Events | 2/2 vollständige Läufe akzeptiert, native Ereignisaudits bestanden; Endstand, Teamstatistik und Endtick identisch zum Quick-Lauf |
| FMF | Lokale 4-2-3-1 importiert; native Serialisierung + erneuter nativer Import mit identischen Phasen, Rollen, Team-/Spieleranweisungen, Mentalität und zusätzlichen Teambits |
| Negativproben | Ungültiges Schema, Rolle und FMF abgelehnt; ungültiges Binärsetup Code 108, kein akzeptiertes Matchresultat |
| Gespeicherte PKM | Originalreader akzeptiert Datei; Szenarioübertragung verwirft Datensatzart 17 (Kadergröße 23), Code 108; 1 Fehlversuch, zweite geplante Wiederholung nicht gestartet |
| Upstreamtests | 173 ausgeführt, 172 bestanden, 1 Windows-Symlink-Test übersprungen; keine Suitefehlfunktion |

**42 akzeptierte technische Matches**, ein zurückgewiesener Karriereversuch und
eine nicht gestartete Karrierewiederholung. Negative Eingaben sind separate Probes,
keine Matches. Es wurden keine taktischen Effekte geschätzt oder Kandidaten gewählt.

### Laufzeitmessung

Identische acht Jobs; ein Durchgang je Workerzahl, einschließlich Prozessstart,
nativer Ausführung und Nachverarbeitung. Keine statistische Präzisionsbehauptung.

| Worker | Sessions | Sekunden | Matches/s |
|---:|---:|---:|---:|
| 1 | 1 | 14,608 | 0,548 |
| 2 | 2 | 8,285 | 0,966 |
| 4 | 4 | 4,999 | 1,600 |

Die Kernserie dauerte mit zwei Workern 15,157 Sekunden. Vier Worker bleiben das
Forschungslimit; Upstreams mögliche 256 Worker werden nicht übernommen.

### Weitere Provenienz

| Artefakt | SHA256 |
|---|---|
| Offizielles Release-EXE | `12be6612326b8264fbb2a9901555bfa1ebc964346b78f05af5854e1b473a8278` |
| Eingebettetes Payload | `9b4d93d8c3a22beaeaca059a7af49df0a5381b95cc439809a421d5c5dda3c36b` |
| Fixture | `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6` |
| Ressourcenfingerabdruck | `6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883` |
| Importierte FMF | `48a0228760bd1ad79bc94e9e9caf9dd08d5661d6a1aec8e67eebe0c5b2426498` |

Die 49 Python-Module des Releasepayloads stimmen nach Normalisierung von CRLF/LF
textlich mit dem Tag überein. Der native Host stammt aus dem gehashten offiziellen
Release; er wurde hier nicht aus C++ neu kompiliert. MSVC war nicht als nutzbare
Toolchain im Suchpfad verfügbar. Die GitHub-Asset-Prüfsumme identifiziert das
verwendete Binärartefakt; sie ist kein unabhängiger Reproducible-Build-Nachweis.

### Fehler und dokumentierte Änderung am Prüfablauf

Der erste Workerstart scheiterte **vor jedem Match** an Upstreams pauschaler
20-GiB-Speicherreserve (18,5 GiB frei). Dafür bleiben der ursprüngliche Versuch
und die leere Sessionliste lokal erhalten. Die neue Forschungsanbindung setzt
ausschließlich für begrenzte technische Batches eine 2-GiB-Reserve, höchstens
512 MiB Artefakte und 16 Jobs pro Batch. Die Funktion wird nach dem Aufruf
wiederhergestellt; keine Upstreamdatei wurde geändert. Der neue Lauf verwendet
ein eigenes Verzeichnis. Das ist eine explizite technische Anpassung nach
Vorregistrierung, keine Änderung einer wissenschaftlichen Auswertungsregel.

Der PKM-Readerfehler ist **kein Engine-Deserialisierungsfehler**: Die aufgezeichnete
Mannschaft hat nicht die Kapazität des mitgelieferten Laborfixtures. Für gespeicherte
Matches muss ein eigener Reader-/Roster-/Phasenadapter entwickelt und auditiert
werden. Der Fehlversuch wird nicht durch ein anderes Match oder einen Seed ersetzt.
Es ist weder historisch exaktes Replay noch Gleichheit von Handspiel, Urlaub,
Instant Result oder Live-Coaching nachgewiesen. Karriereimport von Kadern und
gespeicherte Match-TAC-Objekte ersetzen keine Karrierefortschreibung.

### Wiederholung und Rollback

`analysis/prepare_lab.py` prüft das Release-EXE gegen den Assetdigest und extrahiert
nur in ein neues ignoriertes Verzeichnis. `analysis/validate002.py core` und
`extras` erhalten explizite Runtime-, Spiel- und Artefaktpfade. Bereits vorhandene
Versuchsverzeichnisse werden nicht überschrieben. Der öffentliche
`analysis/export_valid002.py` exportiert nur erlaubte Felder und prüft dabei
Rohlog-, Dump- und Startup-Receipt-Hashes erneut. Ein erneuter Validierungslauf
benötigt neue Versuchspfade und einen aktualisierten technischen Plan; diese
Ausführung setzt keine Serie automatisch fort.

Rollback: neuen Runtimepfad abwählen, alten Host erhalten. Eine Rückkehr zu alten
wissenschaftlichen Experimenten setzt auch deren exakte alte Engine und Ressourcen
voraus; der alte Host allein reicht nicht. Die Spielinstallation wurde nicht geändert.

[Messungen](../data/valid-002/matches.jsonl) ·
[Fehlversuch](../data/valid-002/failures.jsonl) ·
[Maschinenlesbare Teilfreigabe](../data/valid-002/validation-summary.json) ·
[Hashes lokaler Belege](../data/valid-002/evidence-index.json).

Der abschließende Plattform-Smoke-Test wird separat berichtet und bleibt innerhalb
des Gesamtlimits von 48 vollständigen technischen Matches dieses Auftrags.

## Abschließender Plattform-Smoke (MECH-000)

Nach Veröffentlichung der vollständigen Grundlage und SVG-Korrektur wurde der
native Vier-Match-Smoke auf Codecommit `73e5e83a2c5937b24bf41552f3be86811faded33`
ausgeführt. Zwei frische Seeds, bytegleiche A/A-Eingaben, zwei Worker;
**4/4 akzeptiert**, beide Seedpaare exakt in Endstand, Endtick und Teamstatistik.
Laufzeit einschließlich Sessions und Audit **4,659 Sekunden**. Registrierung,
Scheduler, native Readbacks, vollständige Blöcke und automatischer Bericht wurden
gemeinsam durchlaufen. Das deskriptive A/A-Delta beträgt null, ohne
wissenschaftlichen Wirksamkeitsanspruch.

Gesamtabrechnung: **48 geplante technische Matchjobs = 46 akzeptiert + ein
zurückgewiesener Karriereversuch + ein nicht gestarteter Karrierejob**.
Der anfängliche Speicherabbruch startete kein Match. Negative Eingabeprobes und
FMF-Serialisierung/-Parsing sind keine vollständigen Matches.
[Smoke-Receipt](../data/platform-smoke/manifest.json) ·
[Smoke-Messungen](../data/platform-smoke/matches.jsonl) ·
[Automatischer Bericht](../data/platform-smoke/report.md).

# FM27 Research 2.0 – Abnahme am 14.11.2026

Die erste Ausführung liefert eine geprüfte native Teilmigration und eine kleine,
wiederverwendbare Forschungsgrundlage. Die wissenschaftliche Taktiksuche wurde
noch nicht gestartet. Karrierefixtures, Längsschnittfortschreibung und spezielle
Ereigniszähler bleiben explizite technische Folgearbeiten.

## 1. Technischer Ist-Zustand

Ausgang `0b6a609dc3429d4b5141da2c4c000d36d9cb7a7c`; sauberer neuer Checkout,
`origin/main`, keine anfänglichen Benutzeränderungen. Bestehende Forschung und
der erhaltene alte native Host wurden nicht überschrieben.
Lokaler Spielbuild **27.0.1+2503222**, Dateiversion 27.0.1, Steam-Build-ID 26577676.
Enginehash `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
[Bestandsaufnahme](INVENTORY-2026-11-14.md).

## 2. Tatsächlich aktualisiert

Isolierte Runtime aus dem offiziellen **v1114.6**-Release, erneut als neuester
stabiler Upstreamtag geprüft. Das Release-EXE wurde gegen den GitHub-Assetdigest
geprüft und nur extrahiert; seine Desktopoberfläche wurde nicht gestartet.
Offizieller Hosthash `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`.
Bestehende Schnittstelle für absolute Szenarien, native Readbacks und warme
Worker wiederverwendet; keine Änderung an fremden Quelldateien oder Spielinstallation.

Eigene Ergänzungen: Registry/Schemavertrag, Seedplanung, Scheduler, nativer Audit,
Statistik, begrenzte Modellvorschläge, Karriere-Checkpointimport, Berichte,
Build-/Toolprüfung und CI. Ein lokaler Python-Lock hält die geprüften Abhängigkeiten fest.

## 3. VALID-002

**Native Teilfreigabe für das gebündelte kontrollierte Fixture.**
42 akzeptierte Prüfmatches vor dem Plattform-Smoke. Acht deterministische
Vergleiche exakt; 24 Benchmarkmatches bei 1/2/4 Workern stimmen exakt überein;
zwei vollständige Ereignisläufe stimmen mit Quick-Ergebnissen überein.
Beide Phasen, tatsächlich verwendete Rollen, Attribute und Eingaben geprüft.
FMF-Import und semantischer Export/Reimport bestanden. Vier Negativprobes
abgelehnt, einschließlich nativer Rückweisung mit Code 108.

Gespeicherte Karriere-PKM: Reader akzeptiert, unpassender 23er-Kadertransfer
scheitert mit Code 108. Keine Freigabe gespeicherter Fixtures. Ein erster
20-GiB-Speicherpreflight scheiterte vor Simulation; der begrenzte technische
Adapter verwendet dokumentiert 2 GiB Reserve und 512 MiB Ausgabelimit.
Die standardmäßige Upstream-Speicherregel wird nicht dauerhaft verändert.
[Vollständiger Bericht und Hashes](../experiments/VALID-002-adapter.md).

## 4. Neue Forschungsarchitektur

TACT, ATTR, TRAIN, SET und MECH teilen maschinenlesbare Verträge und eine
unveränderliche lokale Registry. SCOUT ist reserviert. Seedreservierungen
berücksichtigen Archive, Fehler und offene Registrierungen. Fehlende Arme,
Identitätsdrift und nachträglich veränderte Konfigurationen sperren die Auswertung.
Seiten werden innerhalb eines Seeds gemittelt. Konfirmatorische TACT-Verträge
verlangen tatsächliche Punkte, eingefrorene Kandidaten und gehaltene Gegner.

Implementiert sind eine 16-Punkt-Resolution-V-DoE-Funktion und ein begrenzter
Ridge-Vorschlagskern. Sie simulieren nicht selbständig. Karriereadapter nimmt
geprüfte Checkpoints entgegen; ein automatischer Karriere-Executor existiert
noch nicht. [Dateien, Befehle und Grenzen](PLATFORM.md).

## 5. Echte Tests und Smoke

| Prüfung | Reales Ergebnis |
|---|---|
| Plattformtests | 14 bestanden |
| Bestehende Analysetests | 5 bestanden |
| Upstreamsuite | 173 ausgeführt, 172 bestanden, ein Windows-Symlink-Skip |
| Ursprüngliches Archiv | 2.504 Matches, 2.080 Baseline-, zehn Rang- und zwei Venue-Kontraste reproduziert; weitere 228 historische Matches und Trainingsdaten geprüft |
| ATTR-004–007 | Sämtliche gespeicherten Effektarchive exakt nachgerechnet |
| A/A-Plattform-Smoke | 4/4 akzeptiert, zwei neue Seedblöcke, beide Paare exakt gleich, 4,659 Sekunden |
| Archivschutz | ATTR-001–007, zugehörige Daten/Runner/Analysen und FINDINGS unverändert gegenüber Ausgangscommit |
| Veröffentlichung | Nur erlaubte numerische Messfelder, Hashes, eigene Programme, Texte und Grafik; keine geschützten Spieldateien |

Der Smoke wurde erst nach Veröffentlichung des Codes auf
`73e5e83a2c5937b24bf41552f3be86811faded33` ausgeführt.
**Gesamtabrechnung: 48 geplante Jobs, 46 akzeptiert, einer zurückgewiesen,
einer nicht gestartet.** FMF- und negative Parserprobes sind keine Matches.
[Smoke-Receipt](../data/platform-smoke/manifest.json),
[Messungen](../data/platform-smoke/matches.jsonl),
[automatischer Bericht](../data/platform-smoke/report.md).

## 6. Wissenschaftliche Gesamtroadmap

Priorität: TACT-001-P0 → MECH-Spielschärfe/Pressing und SET-Zähler →
positions-/niveauabhängige ATTR-Kontraste → kontrollierte TRAIN-Längsschnitte.
Kader-/Gegnerrobustheit und Karrierevalidierung begleiten den Transfer in echte
Saves. Globale Attributranglisten ohne neue Mechanismen werden nicht einfach
wiederholt. Fallzahlen bleiben von Effekt, Streuung, Clustern und Testfamilie
abhängig. [Prioritäten, Rechenlast, Powerbeispiele und Abhängigkeiten](ROADMAP.md).

## 7. Erste Designs

- [TACT-001](../experiments/TACT-001-discovery.md): eigene IP-4-2-3-1, 128-Match-
  Varianzpilot Pressing×Linie, später effizientes DoE und gehaltene Bestätigung.
- [ATTR-008](../experiments/ATTR-008-design.md): marginaler Nutzen nach Position,
  Ausgangsniveau und Taktik; Tore/Punkte ergänzen xG.
- [TRAIN-002](../experiments/TRAIN-002-design.md): gepaarte Karriereableger,
  Coaches/Kader/Kalender konstant, individuelle Exposition und Altersstrata.
- [SET-001](../experiments/SET-001-design.md): tatsächliche Ecken, Nettoertrag
  je Situation und Konterrisiko statt ausschließlich Tore/Spiel.
- [MECH-001](../experiments/MECH-001-design.md): Spielschärfe×Pressing und
  Register weiterer kausal isolierbarer Mechanikfragen.

Alle sind Entwürfe. Unbekannte Setuphashes und fehlende Vorregistrierungsprovenienz
verhindern Ausführung. [Externe Evidenz mit Versions-/Datengrundlage](EXTERNAL_RESEARCH.md)
unterscheidet Autorenbehauptungen von unabhängiger Replikation.

## 8. Verbleibende Einschränkungen

Keine Gleichsetzung von nativem Einzelmatch, Karriere, Urlaub, Instant Result
und Live-Coaching. Gespeicherte PKM-Kapazität, Originalmanagement,
Taktikausführung/Komplexität und neue Rollen-/PI-Typen brauchen zusätzliche Audits.
SET-Ereignis-/Konterzähler und TRAIN-Kalender-/Teilnahme-Executor fehlen.
Der offizielle Host wurde hier nicht selbst kompiliert; kein unabhängiger
Reproducible-Build-Nachweis. Benchmark nur ein kleiner Durchgang je Workerzahl.

## 9. Veröffentlichte Abschnitte

| Commit | Abschnitt |
|---|---|
| `a898b77` | Bestandsaufnahme |
| `894c51f` | Vorab veröffentlichter VALID-002-Plan und reversible Runtimevorbereitung |
| `2a32759` | Reale native Validierung, Messungen, Fehler und Teilfreigabe |
| `6b3e74e` | Modulare Grundlage, fünf Moduldesigns, Roadmaps, Evidenzregister und CI |
| `73e5e83` | SVG-Exportkorrektur; tatsächlich im Plattform-Smoke verwendeter Code |

Smoke-Belege und dieser Abnahmebericht werden in einem anschließenden eigenen
Deliverycommit veröffentlicht. Den endgültigen SHA nennt die Auftragsantwort.
Es gibt keinen Force-Push. Der Git-Verlauf bleibt die Zuordnung von Bericht,
Vorregistrierung und Ausführung.

## 10. Exakter nächster Auftrag

[docs/NEXT_CODEX_TASK.md](NEXT_CODEX_TASK.md) enthält den vollständigen,
kopierbaren Auftrag für **TACT-001-P0**: maximal 128 Hauptmatches plus
24 technische Prüfmatches, vier Worker und 15 Minuten native Gesamtausführungszeit,
vorheriger Push des konkreten Plans und keine finale Taktikauswahl aus Pilotdaten.

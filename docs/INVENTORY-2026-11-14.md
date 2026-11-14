# Bestandsaufnahme – FM27 Research 2.0

Stand: 14.11.2026. Ausgangscommit: `0b6a609dc3429d4b5141da2c4c000d36d9cb7a7c`.

## Checkout und Erhaltung

Das vorgegebene Arbeitsverzeichnis war leer. Das öffentliche Repository wurde frisch
geklont; `main` trackt `origin/main`, Remote ist
`https://github.com/Matchekk/FM-27-Research.git`. Keine uncommitteten Änderungen
im neuen Checkout. Ein früherer Forschungscheckout und dessen lokale Messungen
wurden gefunden und bleiben unangetastet. Der dortige temporäre Lab-Checkout
steht auf v1106, hat aber weitgehend gelöschte Quelldateien. Der erhaltene Host
hat weiterhin SHA256 `50c8eef1e3c560974070163ec2c1633508be314bdd31d69de5388470efc0f81a`.
Eine vollständige Wiederherstellung dieses alten Laufzeitsystems ist damit nicht belegt.

README, AGENTS, Methodik, Findings, Next Steps, Research Log, VALID-001,
ATTR-001–007, TRAIN-001, Datenbeschreibungen, Manifeste sowie alle Python-Runner,
Exporter und Analysen wurden für die Architekturaufnahme geprüft.

## Bestehende Architektur

| Schicht | Bestand | Wiederverwendung / Grenze |
|---|---|---|
| Wissenschaftliches Archiv | `experiments/`, `data/`, Findings und Journal | Unverändert erhalten; historische Aussagen bleiben Build 27.0.0+2493426 zugeordnet |
| Native Ausführung | `analysis/run_attr004.py`, darauf aufbauend 005–007 | Strikte Hash-, Build-, Readback-, Seed- und Abschlussgates; absichtlich an alten Host gebunden |
| Eingaben | Externer Windows-Lab-Server, FM27CFG1-Binärdatensätze, lokale PKM | Keine Spielressourcen im Forschungsrepository; keine stabile öffentliche Engine-API |
| Audit / Export | `run_attr004`, `export_attr004`, native Dumps und Startup-Receipts | Allowlist-Export und Hashprüfung wiederverwenden als Muster, eingefrorene Programme nicht umbauen |
| Statistik | `verify_matches`, `analyse_attr004`–007 | Gepaarte Kontraste, vollständige Seed-Blöcke, t-/Bootstrapintervalle, Holm bzw. BH/BY; geeignet als Referenz |
| Karriere | TRAIN-001, pseudonymisierte Differenzen und Exposition | Kein allgemeiner Karriere-Runner im Repo; unabhängige Save-Ableger und Teilnahmehistorie fehlen |

Datenfluss bisher: lokale Lab-Eingaben → binäre Konfiguration → externer nativer
Host → Rohlog + Eingabedump + Startup-Receipt → Audit → publizierbare JSONL →
eingefrorene Analyse → Markdownbericht. Verteilte Seedfunktionen kennen jeweils
die vorherigen Serien; es fehlen zentrale Registry, allgemeines Schema,
versionsgebundene Freigaben und eine gemeinsame modulübergreifende Planung.

## Verifikation des Bestands

- Python 3.12, isolierte Umgebung; NumPy 2.3.5 und SciPy 1.16.3 wie dokumentiert.
- `python -m unittest discover -s analysis -p 'test*.py' -v`: **5/5 bestanden**.
- `python analysis/verify_matches.py`: **2.504 Matches, 2.080 Baseline-Kontraste,
  zehn Rangkontraste, zwei Venue-Kontraste und 228 historische Matches reproduziert**;
  Trainingsarchiv ebenfalls nachgerechnet. Keine neue Simulation in diesem Schritt.
- ATTR-004–007 bleiben einschließlich ihrer Auswertungsprogramme unverändert.
- Der TRAIN-Readback und die Nachrechnung bleiben maßgeblich; keine Korrektur
  alter Befunde oder Aufwertung explorativer Evidenz in diesem Auftrag.

## Aktuelle Umgebung und Migration

Lokales FM27: Laufzeitlog `27.0.1+2503222`, DLL-Dateiversion `27.0.1`,
Steam-Build-ID `26577676`, DLL-Größe 408.383.448 Bytes,
SHA256 `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Der Hash entspricht dem neuen offiziellen Steam-Adapterprofil.

Release-/Tag-Abfrage am 14.11.2026: neuestes stabiles Tactics Lab **v1114.6**, Commit
`91f2eba57fac0b7fbd3dff616056907e3ce461be`; kein neuerer Tag gefunden.
v1106→v1114.6: 184 geänderte Dateien, Karriereimport, native AI-Pläne,
Taktikausführung, Worker-Protokoll 2 mit Ressourcenfreigabe pro Match,
FMF-/Phasen-/Identitätskorrekturen sowie Hotfix-Anpassung. Keine ungeprüfte
Übernahme früherer Adapteroffsets.

Mac-Referenz: `849b16f9c4057598da33b255649c86d8cecb525b`.
Methodisch relevant: gehaltene Gegner/Matches, frische Bestätigungsseeds,
Ridge-Modelle mit Interaktionen, native Replaykontrolle und ausdrückliche Grenzen
der Taktikkomplexität. Mac-Host und Installationsskripte werden nicht ausgeführt.
Externe Forschungsbehauptungen sind zunächst Quellenbehauptungen.

## Implementierungsabschnitte

1. Bestandsaufnahme und Erhaltungsnachweis (dieses Dokument).
2. Isoliertes v1114.6-Laufzeitsystem und begrenzte VALID-002; reale Fehler bleiben erhalten.
3. Kleine Python-Bibliothek für Registry/Schema, Seedplanung, Scheduler, Audits,
   Statistik und Berichte; native Einzelmatches getrennt von Karrierezeitreihen.
4. Modulroadmaps, externe Evidenzübersicht und TACT-001-Vorregistrierungsentwurf.
5. End-to-End-Smoke, Regression, Veröffentlichungsprüfung, Commit und Push.

Quellen: [Tactics Lab v1114.6](https://github.com/lqf0624/fm-tactics-lab/releases/tag/v1114.6),
[Änderungsvergleich](https://github.com/lqf0624/fm-tactics-lab/compare/v1106...v1114.6),
[Mac-Referenz](https://github.com/caiograco289/Fm-Match-Lab/tree/849b16f9c4057598da33b255649c86d8cecb525b).

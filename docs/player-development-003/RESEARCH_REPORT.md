# Spielerentwicklung003 – Zugang entschieden, keine neuen FM27-Messungen

15.11.2026. **CA-003: INDEPENDENT_EDITOR_RCA_UNAVAILABLE.** CA-004 und
TRAIN-004 wurden ebenfalls vor jeder Intervention gestoppt. Die offene
wissenschaftliche Frage konnte in dieser Umgebung nicht neu beantwortet werden.
Dieser Abschluss dokumentiert einen begrenzten technischen Zugangscheck und
eine sofort befüllbare Übergabe, kein empirisches Forschungsergebnis.

| Bereich | Tatsächliche Entscheidung | Neue Daten |
|---|---|---|
| CA-003-GOLD | Kein verifizierter unabhängiger RCA-Readback | 0 Goldprofile / 0 Interventionen |
| CA-004-EXEMPT A/B | Weder Goldzugang noch kontrollierter Rückanpassungsexecutor | 0 statische Fälle / 0 Karrierearme |
| TRAIN-004-QUICKNESS | Fokussetzung/Readback, Executor und unabhängige Starts fehlen | 0 Arme / 0 Armwochen |

## Konkrete Zugangsevidenz

Start 18:45:52 UTC / 19:45:52 CET. Arbeitsbaum sauber, HEAD und nach Fetch
origin/main gleich `8035085622ec3cd93fa93e13e33751e1ce2bccea`; anschließend
`pull --ff-only`, neuer Branch `codex/player-development-003`.
FM27-Prozess und Fenster tatsächlich vorhanden. Computer Use lieferte nur
`0 pane Football Manager 27`; Bildschirmaufnahme scheiterte mit
`FrameArrived timed out`, nach erneuter Fensterauswahl nochmals
`window capture timed out`. Keine blinden Tastatureingaben oder Klicks.
Die laufende Karriere wurde weder als Wegwerfkopie identifiziert noch verändert.

Kein separater FM27-Editor im geprüften Steam-Common-Verzeichnis, den geprüften
Steam-Appmanifesten oder laufenden Fenstern gefunden. Das ist eine begrenzte
Inventur, kein Beweis, dass auf keinem Datenträger ein Editor existiert.
Der Ingame-Editor und seine Freischaltung bleiben wegen fehlender Bild-/UI-
Erfassung **UNKNOWN**, nicht als nicht vorhanden behauptet.

Die bestehenden lokalen Cheat-Deck-/Living-Potential-/Scout-/View-Exporter-
Quellen liefern keinen nachgewiesenen unabhängigen RCA-Readback und keinen
Quickness-/Kalenderexecutor. Kein neuer Hook, keine Injektion und kein
Readerreparaturversuch. Vorhandene alte private Readerkopien sind keine
freigegebenen neuen Karrierearme. `research/career.py` importiert JSON;
`research/training002.py` diagnostiziert Checkpoints. Beide steuern FM nicht.
Die aktuelle fmsave-Quelle v0.12.5 bietet keinen entsprechenden Fokussetter
oder Advanceweg. Fehlende Anwesenheitsdaten allein wurden nicht als ITT-Sperre verwendet.

## Versionen, Quellen und Ressourcen

Installierte `game_plugin.dll` erneut per Dateimetadaten/Hash gemessen:
**27.0.1+2503222**, SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Steam-Build-ID 26577676 ist eine eigene Versionsgröße, keine Enginebuildnummer.
Runtimebuild und gespeicherter Karrierebuild wurden nicht unabhängig gemessen.
Python 3.12.10, NumPy 2.3.5, SciPy 1.16.3, Node v25.9.0, installierter
fmsave 0.9.0; geprüftes Upstream v0.12.5 ist nicht lokal neu installiert.

Scout-Quelle heute weiterhin `084d7f0a18ac790d7c4087c5b6bdff008186d4fa`.
Atlas, Index, FINDINGS und Originalquellen erneut geprüft. Der Quellenrefresh
ist im [Abrufnachweis](source-refresh.json) gebunden; Einzelheiten zur
[RCA-Herkunft](EDITOR_GOLD_VALIDATION.md). Ein separater Agent prüfte nur
Quellen, nicht dieselbe lokale technische Blockade.

Bestehenden Comparator direkt auf **einen schon archivierten CA-002-Input**
angewandt: MODEL_RCA 107, exakte Reproduktion, zwei reine Funktionsaufrufe
einschließlich A/A. Das ist ausschließlich Betriebsbereitschaft, kein neuer
Spieler, kein Goldvergleich und keine wiederholte wissenschaftliche Modellmatrix.
[Technikbeleg](../../data/player-development-003/comparator-smoke.json).

Ressourcen: null native Simulationsaufrufe, Saveöffnungen, Saveänderungen,
Kalenderadvances, neue Seeds oder gestartete wissenschaftliche Arme;
zwei fehlgeschlagene GUI-Bilderfassungen, ein Offline-Comparatorrequest.
Keine selbst gestarteten FM-/Editor-/Controllerprozesse zu bereinigen.
Quellcache bleibt ignoriert; keine privaten Profile oder Binärdateien publiziert.
CPU-/RAM-Spitzen dieses reinen Zugangschecks wurden nicht gemessen.

Die drei Zugangsentscheidungen waren um 18:54:22 UTC / 19:54:22 CET
festgehalten, rund 8,5 Minuten nach Beginn und innerhalb der ersten 15 Minuten.
Keine fortgesetzte technische Retryschleife bis zur 45-Minuten-Grenze.

## Übergabe und Prüfung

[Drei getrennte Verträge](../../experiments/CA-003-GOLD.md),
[CA-004](../../experiments/CA-004-EXEMPT.md),
[TRAIN-004](../../experiments/TRAIN-004-QUICKNESS.md),
[Erfassungsprotokoll](CAPTURE_PROTOCOL.md) und
[leere Vor-/Nachher-Vorlage](../../data/player-development-003/editor-capture.template.jsonl)
liegen vor. Kein vorgetäuschter 48-Fälle-Freeze ohne Pilotzugang.
Alle wissenschaftlichen Fehler-/Effektschätzer sind null/NOT_MEASURED.
Vorhandenen Analysecode wiederverwenden; kein neues VALID-System und keine
erneute Berechnung der Trainingsmappe. [Prüf-/Publikationsbeleg](publication.json)
führt den tatsächlichen Test-, Commit-, CI- und Pushstatus.

Archivcommit `3f51379bd3f9a9ca5eec2798f874cbe35bcb3c8f` ist auf dem Forschungsbranch veröffentlicht und hat
[exakte CI 43749649506](https://github.com/Matchekk/FM-27-Research/actions/runs/43749649506)
bestanden. Lokal: 477 Testfälle (474 bestanden, drei bestehende Skips), fünf
Analysetests und alle 19 vorhandenen Archivprüfungen erfolgreich. Die folgende
Publikationsnotiz ändert keine Messwerte; sie benötigt vor Mainintegration
ebenfalls erfolgreiche CI auf ihrem exakten Commit.

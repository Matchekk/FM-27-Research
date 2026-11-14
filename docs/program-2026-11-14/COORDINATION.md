# Forschungsprogramm – zentrale Koordination

Stand14.11.2026. Dieses Programm ist Recherche, Design und sichere Offlinevorarbeit.
Es ist **kein** Sammelauftrag zur Ausführung der vorgeschlagenen Studien.
Der zuvor autorisierte P1C-Lauf wurde zentral abgeschlossen; das neue Programm
startet keine zusätzliche native Simulation und verwendet keine Holdoutdaten.

## Tatsächliche Agenten und Dateiverantwortung

| Rolle | Tatsächlicher Codex-Subagent | Exklusive Schreibbereiche |
|---|---|---|
| Agent1 TACT | `tactics_researcher` | `TACT.md` |
| Agent2 ATTR | `attribute_researcher` | `ATTR.md` |
| Agent3 TRAIN | `training_researcher` | `TRAIN.md` |
| Agent4 SET | `set_piece_researcher` | `SET.md`, gegebenenfalls explizit zugewiesene eigene Offlinevorarbeit |
| Agent5 MECH | `match_engine_researcher` | `MECH.md` |
| Agent6 VALID | `validation_engineer` | `VALID.md`, neue `research/coordination.py`, neue `tests/test_coordination.py` |
| Agent7 unabhängiger Review | `independent_reviewer` | `REVIEW.md`, `P1C-review.md` |
| Research Director | Root-Agent | Integration, bestehende Übersichtsdokumente, explizites Staging/Commits/Push und alleinige native Freigabekoordination |

Berichtspfade beziehen sich auf dieses Verzeichnis. Getrennte Dateien im gemeinsamen
Checkout, keine konkurrierenden Branchwechsel. Subagents committen nicht und
schreiben nicht in fremde Bereiche. Quell-/Archivdateien bleiben lesbar, außer
gehaltenen Daten. Änderungen außerhalb der Zuständigkeit benötigen neue Zuweisung.

Es stehen in dieser Sitzung vier Agenten-Slots **einschließlich Director** zur
Verfügung. Deshalb maximal drei gleichzeitig arbeitende Subagents und eine
Warteschlange; das Nutzermaximum von vier gleichzeitigen Subagents wird eingehalten.
Erste parallele Welle: TACT/ATTR/VALID. Weitere Fachaufgaben und unabhängige
Reviews werden nach frei werdenden Slots zugewiesen. `QUEUE.json` dokumentiert
Aufträge und tatsächlichen Abschluss; es ist kein Automationsdienst.

## Native Ausführung, Seeds und Budgets

- Nur der Director darf einen nativen Auftrag starten. In diesem Programm keine
  weiteren Starts, keine Registry-/Seedreservierung durch Fachagenten.
- Ein nativer Supervisor global, maximal vier tatsächliche Engine-Worker insgesamt,
  90 Sekunden ohne Fortschritt. Gemeinsame private Koordinationsstelle vor
  zukünftigen Starts; bestehende Runner besitzen weiterhin ihre eigenen Budgets.
- Die neue `NativeLease` ist eine **optionale Offlinevorarbeit** für kooperierende
  Supervisoren. Sie ist noch nicht in historische Runner integriert und erzwingt
  dort kein globales Prozess-/Zeit-/Seedlimit. Das globale Limit dieses Auftrags
  wird durch zentrale Serialisierung eingehalten. Keine falsche Integrationsfreigabe.
- Neue Studien benötigen zuvor veröffentlichte Konfiguration, Code, konkrete
  neue Seedreservation, feste Versuchszähler und Gesamtdeadline. Keine Neustarts,
  Ersatzseeds oder ergebnisabhängigen Ausschlüsse. Abgebrochene Seeds bleiben belegt.
- Keine Datei aus `local/` veröffentlichen. Nur eigene Deskriptoren, erlaubte
  numerische Messungen, Hash-/Versionsprovenienz. Save/PKM/FMF/DLL/EXE und
  personenbezogene IDs bleiben privat.

## Wissenschaftliche Freigabekette

1. Quellen-/Versionsregister und klarer zusätzlicher Erkenntniswert; bekannte
   Rankings nicht ohne neue kausale Frage wiederholen.
2. Protokoll mit einem Primärkontrast oder korrigierter Familie, praktischer
   Schwelle, unabhängiger Einheit und bedingter SD-/Power-/Kostenplanung.
3. Prüffähige native Schreib- und Nach-Vorbereitungsreadbacks aller geänderten
   Felder. JSON-/Katalogmitgliedschaft ist keine technische Wirksamkeitsfreigabe.
4. A/A, deterministische neue technische Seeds, negative Eingaben, Zähler und
   Fehler-/Abbruchbelege. Drift stoppt; VALID-002 bleibt unverändert buildgebunden.
5. Unabhängiger Reviewer rekonstruiert Statistik und prüft Aliase, Multiplikität,
   Selektion, fehlende Daten, Unsicherheiten und Übertragungsgrenzen.
6. Director integriert nur geprüfte Ergebnisse, führt CI/Diff-/Archiv-/Geheimnis-
   prüfungen aus und committet/pusht. Ein geprüfter **Entwurf** ist dadurch kein
   gestartetes oder technisch freigegebenes Experiment.

Karriere-PKM, Karrierefortschreibung und Trainingskalender benötigen getrennte
Gates. Bytegleiche Save-Klone mit identischem RNG sind keine unabhängigen
Replikate; diese Unabhängigkeit muss zwischen Replikaten nachgewiesen werden.
Gleiche Seeds verbinden Arme und Seiten, garantieren keine gleichen Spielereignisse.
Discoverydaten dürfen keine nachträgliche Gewinnerbestätigung liefern. Gehaltene
Gegner/Seeds bleiben ungeöffnet und werden nicht als Entwicklungsdaten verwendet.

## Abschluss dieser Ausführung

Sieben getrennte Fach-/Reviewberichte, konsolidierte Prioritäten und bedingte
Budgets, klare technische Blocker, geprüfte Offlinevorarbeit, Tests/CI und
veröffentlichte Commit-SHAs. Danach stoppen; keine automatische Optimierungsrunde,
Holdoutstudie oder Karrierefortschreibung.

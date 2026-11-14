# VALID-004 – realistische Karrierequelle „Test FM Research“

**14.11.2026 · technischer Entwurf, nicht registriert, nicht nativ ausgeführt.**

## Ausgangslage

Runde 3 ist abgeschlossen: ATTR-009 lieferte einen unklaren Maskenmoderator (−0,162 xGD; 95%-KI [−0,488;+0,164]), MECH-002 benötigt passive Erstschritt-/Familiarity-Messungen, TRAIN-002 benötigt unabhängige Karriere-RNG-/Teilnahmedaten. VALID-002 gibt ausschließlich das kontrollierte Bundled-Fixture frei. Der gespeicherte Karriere-PKM-Pfad scheiterte bisher am Unterschied zwischen gespeicherter Kaderkapazität und erzwungenem 23-Spieler-Transfer (Recordtyp 17 / Exit 108).

Eine neu erzeugte realistische Wegwerfkarriere namens `Test FM Research` ist eine wertvolle technische Quelle, aber kein Beleg für unabhängige Karrierereplikate und kein Grund, bestehende Holdouts anzutasten.

## Phase 0 – sicheres Datei-Inventar (im PR vorbereitet)

`analysis/capture_test_fm_research.py` ist bewusst **nur** ein privater Hash-/Stabilitätsprüfer. Er erhält explizite `PRE.fm`, optionale `POST.fm` sowie ausgewählte `PKM`/`REC`, verweigert doppelte oder instabile Dateien und schreibt einen neuen JSON-Beleg unter `local/`. Weder Dateinamen/Pfade noch Originalbytes erscheinen im Receipt. **Keine** Engine, kein Decoder, keine Karrieresimulation, keine Seedreservation. Technische Abnahme: mindestens vier Offline-Unit-Tests plus Repository-CI; keine wissenschaftliche Freigabe. Das Capture-Protokoll steht unter [docs/test-fm-research](../docs/test-fm-research/README.md).

## Phase 1 – realer Reader und semantische Zugehörigkeit (noch gesperrt)

- Tatsächlichen FM-Build, DLL-/Host-/Reader-/Toolhash und Matchdatum aus **privaten Originalbelegen** bestimmen; keine Versionsnummer übernehmen, nur weil sie in einem früheren Laborbericht stand.
- Save/PKM/REC-Kapazität, Teams, Startscore, Kaderplätze, Originalträgeridentitäten, IP-/OOP-Taktik, Rollen/Duties/PI und Managementzustand soweit **lesbar** erfassen.
- Jedes Feld mit Decoder-Version, Quelloffset/-Record und Prüfsumme belegen; nicht lesbare Daten mit `unknown` kennzeichnen.
- Die Zusammengehörigkeit von PRE, PKM, REC und POST mittels zweitem unabhängigen Beleg (Matchdatum, Teams, Ergebnis, Zeit) nachweisen; der bloße Dateiname/Hash reicht nicht.
- Beim PKM-Kader niemals auf 23 abschneiden/auffüllen. Bei unbekannter Kapazität stoppen. Originalmanager-/Wechsel-/Live-Entscheidungen nicht durch generische Fixture-Defaults ersetzen.
- Das bestehende `research/training002.py` ist ein strikter Receipt-Validator, **kein** Save-Decoder oder Kalenderexecutor. Neue Decoderimplementierung getrennt versionieren und reviewen, keine vorhandene Freigabe mutieren.

## Phase 2 – interventionsfähige technische Adapter-Gates (separater Auftrag)

Nach bestandenem Phase-1-Gate zunächst reine Readbacks/Negativproben und A/A-Identitäten auf dem **echten** Kontext vorregistrieren. Höchstens eine gesondert budgetierte technische Pilotserie, nur wenn die externen nativen Eingaben tatsächlich nach Vorverarbeitung überprüfbar sind. Ein reparierter PKM-Reader allein beweist keine originalgetreue Re-Simulation. Engine-/Hostpatches getrennt versionieren und auf dem unberührten Bundled-Fixture erneut mit neuen technischen Seeds validieren.

**Verbindlich:** ein globaler NativeLease-Supervisor, höchstens vier Worker, 90 s ohne Fortschritt, gesondertes dauerhaftes Zeit-/Startbudget und neu reservierte Seeds; TECH-Preregistration und Code vor dem ersten Vollmatch pushen. Negative Eingaben und A/A-Wiederholung müssen funktionieren. Bei Drift oder unbekannten Originalzuständen keine Ersatzseeds/Standardwerte; den Blocker dokumentieren.

## Phase 3 – getrennte Forschungsvorhaben, noch nicht freigegeben

- **MECH:** passive Originalzustände nach Vorbereitung und nach dem ersten Matchschritt prüfen, bevor ein opt-in Startpolicy-Eingriff als wirksam gilt. `experimental_execution`-Aggregate sind kein validierter isolierter Understanding-Effekt.
- **ATTR/TACT:** positionsspezifische realistische Profilvektoren, Rollen/Phasen und passende Kaderstärken zuerst nativ freigeben. Neue Suchkontexte dürfen bisher versiegelte Holdouts nicht verbrauchen.
- **SET:** native *tatsächlich ausgeführte* Standards, legale Kontakte, Zeitachsen, Schuss-xG, Tor/VAR und Besitz-/Konterkette gegen unabhängige Goldfälle validieren. Synthetischer Parser ist kein echter Ausführungszähler.
- **TRAIN:** reale, tatsächlich absolvierte Einheiten, Coach/Fokus/Intensität, Kalender, Minuten/Verletzungen und nachweislich unabhängige Karriere-RNG-Streams bzw. echte getrennte Club-/Savecluster; identische Klone zählen nicht als unabhängige n.

## Agenten-Koordination für eine lokale Folgerunde

Director liest [docs/round3/README.md](../docs/round3/README.md), [Prioritäten](../docs/round3/PRIORITIES.md), AGENTS.md, METHODOLOGY.md sowie diesen Plan. Maximal drei Fach-Subagents gleichzeitig auf getrennten Worktrees:

1. **VALID/PKM:** Phase 1, Versions- und Kapazitätsbelege; keine native Replayausführung.
2. **MECH:** statisches Mapping passiver Erstschritt-/Familiarityquellen, eigener technischer Gateentwurf; keine simulierten oder erfundenen Erstschrittbelege.
3. **TRAIN:** Reader- und tatsächliche Session-/Teilnahmeprovenienz, unabhängige Karriere-RNG-Prüfbarkeit; kein Kalenderadvance.
4. **SET** nach einem freien Agentenslot: reale Ereignisquellen analysieren, noch kein Standard-Ranking.
5. **Reviewer** unabhängig nach Facharbeit: alle Feldprovenienzen, Sicherheitsgrenzen, Replikate und Inputdifferenzen prüfen. Director integriert erst nach CI und Review.

Sind die privaten Dateien nicht vorhanden oder unzugänglich, kann Phase 0 anhand synthetischer Dateien getestet und Phase 1 **nur als Offline-Quellplan** weitergeführt werden. Keine angebliche Arbeit auf dem PC oder aktuelle Matching-Zahlen erfinden.

## Abnahmekriterien und Stopregel

- Originalspielstände unverändert; keine privaten Bytes/Spieleridentitäten auf GitHub.
- Hash-Receipts beweisen nur Identität, nicht Semantik; originäre Join-Belege je Partie.
- Alle neuen Messgrößen mit Quelle, Einheit, unbekannten Feldern und Versionshashen.
- Unbekannte Kaderkapazität, RNG oder Startzustände blockieren darauf aufbauende Aussagen.
- Kein neues Performance-Experiment, keine Karrierefortschreibung, keine Holdouts/Seedreservation im Capture-/Planungsauftrag.
- Abschluss mit technischen Ergebnissen **oder** dokumentierten Blockern; CI, Review und historischer Archivschutz.

**Erste Freigabestufe:** Phase 0 als rein lesender lokaler Dateicapture. **Phase 1–3 bleiben bis nach realer lokaler Prüfung gesperrt.**

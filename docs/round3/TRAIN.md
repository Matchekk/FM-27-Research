# Agent TRAIN – Forschungsrunde3

**Reader-/Diagnosevorarbeit implementiert und offline geprüft; native Karrieregates
blockiert.** Eigener Branch/Worktree, keine gemeinsamen Registerschreibzugriffe.
[Vollständiger technischer Bericht](../../experiments/TRAIN-002-technical-round3.md).

Forschungsfrage bleibt, ob Heavy Conditioning gegenüber Conditioning die
kalibrierte Entwicklung pro unabhängiger Karriere-/Clubreplikation verändert,
getrennt von Matchvorbereitung, Belastung und Verletzungskosten. Die heutige
Arbeit misst keine solche Wirkung. Sie schließt den Fehler aus, Plankalender,
boolesche Teilnahmebehauptung oder22Spieler mit echter Exposition/Unabhängigkeit
gleichzusetzen.

## Geprüfte Evidenz und Forschungslücke

- [TRAIN-001-Originalarchiv](../../experiments/TRAIN-001-karriere.md):660reale
  historische Delta-Zeilen/Build27.0.0+2493426; keine unabhängigen
  Treatmentreplikate, individuelle Teilnahme oder Ausfalltage daraus ableitbar.
- [Früherer externer Evidenzvergleich](../program-2026-11-14/TRAIN.md): historische
  Hersteller-/Fremdstudienbelege werden hier nicht neu unabhängig geprüft oder
  aufgewertet. Kein neuer externer Wirksamkeitsbefund in dieser technischen Runde.
- Installiertes fmsave0.9.0 tatsächlich statisch geprüft: TrainingDay/Week und
  TeamTraining enthalten Teamkalender, keine per-Spieler-Ausführungsbelege.
  Session304 ist in dieser Version **unbenannt**, selbst wenn ältere lokale
  Forschung sie als Heavy Conditioning interpretierte. Nicht still neu labeln.
  InjuryRecord trennt HISTORY-Ereignisdatum von TYPED-erwartetem Rückkehrdatum;
  daraus folgt noch kein tatsächlich beobachtetes Verletzungsintervall.
  Modellsignaturen/Quellhashes im [Inventar](../../data/train-002-technical/reader-inventory.json).

Neuheitswert: überprüfbare Entwicklung je **tatsächlich ausgeführter** Einheit,
Persistenz und Belastungskosten. Eine erneute Planrangliste ohne diese Gates
würde vor allem unbekannte Durchführung und Saveabhängigkeit vergleichen.

## Implementierungs- und Teststatus

Neu `research/training002.py`: eigener strikter JSON-Exportvertrag,
Quellbyte-Prüfung, explizite Missingwerte, Kalender-/Teilnahme-/Verletzungslogik,
Kontroll-/Klonprüfung und konservative Roh-/Anzeigediagnose. Kein `.fm`-Decoder,
kein fmsaveimport, kein Executor und **kein Pfad zur Karrierefreigabe**.
Zwei Offline-CLIs rekonstruieren Archiv und statische Paketsignaturen.
Alle11neuen gezielten Tests bestanden; zusätzlich97Repositorytests und5historische
Analysetests im eigenen Worktree bestanden. `git diff --check` ohne Befund.
Director führt integrierten Archivschutz/CI und separate unabhängige Abnahme durch.

Die Checkpointprüfungen testen Format und Widersprüche. Vollständige Hashreceipts
belegen nicht automatisch Feldbedeutung, Auslesevollständigkeit oder unabhängige
RNG-Ströme. Die synthetischen Tempfixtures tragen ausschließlich origin=synthetic.

## Fallzahl, Kosten, offene Gates und nächste Schritte

Aktuelles Budget/Verbrauch:0Matches/0Advance/0Seeds/0Armwochen.
Keine inferenzstatistischen Intervalle aus individuellen Spielerzeilen und keine
Karrierelaufzeitprognose aus nativen Einzelmatchzeiten.

Priorität1: echte Quelle für individuelle Durchführung und RNG-/Clusterherkunft,
anschließend read-only Feld-/Skalenabnahme. Priorität2: separat veröffentlichter
technischer A/A-Benchmark mit maximal8Armwochen/30Minuten und serieller
Lease-/Deadlinekoordination, **nur nach neuer Abnahme**. Erst danach wissenschaftlicher
Varianzpilot:8unabhängigePaare je Alterstratum,32Arme/192Armwochen,
Primärkalibrierung/Holm2 und vorab lesbare sekundäre Endpunkte.

Spieler bleiben im Baseline-ITT-Nenner. Tatsächliche Verletzungen/Minuten können
Mediatoren der Trainingswirkung sein und werden nicht nachträglich wegangepasst.
Alle Zukunftsbudgets bleiben Entwürfe; keine automatische Fortschreibung oder
Ersatzreplikation bei fehlenden Gates. Karriere-Replay unverändert gesperrt.

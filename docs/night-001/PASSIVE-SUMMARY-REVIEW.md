# VALID-005 – unabhängiger Review der deskriptiven Zustandsübersicht

14.11.2026, ergänzend zur [technischen Ergebnisabnahme](OBSERVER-RESULTS-REVIEW.md).
Geprüft wurden der neue Auswerter `analysis/summarize_passive005.py`,
`data/valid-005-observer-v1/passive-state.json`, die zugehörige SVG und die bereits
erhaltenen privaten JSON-/JSONL-Belege. Keine Saveöffnung, kein nativer Start,
keine zusätzlichen Matches oder Prozess-/Kerneltests durch diesen Zusatzreview.

Der Reviewer berechnete die Aggregate mit einem eigenen temporären Skript aus
den vier Rohlogs neu. Weder `build()` noch die bereits veröffentlichten
Aggregatfunktionen wurden dafür aufgerufen. Der Konfigurationshash wurde mit der
festgelegten JSON-Kanonisierung rekonstruiert; alle vier Rohloghashes entsprechen
den tatsächlich vorhandenen Bytes und den Messungsreceipts. Vier unterschiedliche
Seeds decken genau beide Gegnerkontexte und beide Setupseiten ab. Verwendet
wurden ausschließlich die vier `observer_on`-Läufe, keine A/A-Wiederholungen.

Die ursprünglichen Feldstarter wurden je Match über `(side, roster_index)` aus
**beiden** Team-Lineups, jeweils `lineup[1:]`, gebunden: zehn pro Seite, zwanzig
insgesamt. Alle Identitäten sind je Snapshot eindeutig; kein fehlender Cache wurde
mit Null ersetzt. Drei Zustände je Match ergeben zwölf Snapshots,
240 Feldstarter-Zustandsbeobachtungen und552 Actor-Zustandsbeobachtungen insgesamt.
Diese Mengen sind keine240 beziehungsweise552 unabhängigen Replikate.

Sämtliche JSON-Zellen stimmen einschließlich Minimum, Mittelwert, Maximum,
Nenner und Missingzahl mit der unabhängigen Rechnung überein:

| Technische Zelle | Cache0x89 am Ende: Mittel der20 Feldstarter | Minimum–Maximum |
|---|---:|---:|
| high_press, Seite0 | 78,60 | 72–84 |
| high_press, Seite1 | 76,85 | 63–82 |
| deep_block, Seite0 | 80,10 | 72–87 |
| deep_block, Seite1 | 79,30 | 72–84 |

Vorbereitung und erster Fortschritt liefern bei diesen zwanzig Spielern
jeweils Profilstorage10000, Accumulator1000000 sowie Cache0x89 und0x8a jeweils100.
Am Ende bleibt die betrachtete Profilstorage10000 und Cache0x8a100, während
Accumulator und Cache0x89 abweichen. Die33Byte-Rohregion ist je Match zunächst
bei0von46 Actors nichtnull, am Ende bei22von46. Sechs Cachepointer je46er-Snapshot
bleiben explizit fehlend; die ausgewählten zwanzig Feldstarter haben vollständige
Caches. Es wird kein unbekannter Pointer- oder Regionsinhalt semantisch ergänzt.

Die Bildvorschau wurde angesehen. Drei getrennte Achsen zeigen die verschiedenen
Rohquellen und die zwölf tatsächlichen Snapshotpunkte korrekt; überlagerte
identische Linien sind keine zusätzlichen unabhängigen Daten. Die Verbindung
der Kategorien beschreibt keine gemessene Entwicklung zwischen den drei
Aufnahmezeitpunkten. Die Grafik bezeichnet weder Profil- noch Cachewerte als
kalibrierte FM-UI-Prozente und enthält keine inferentiellen Fehlerbalken.

Dieser Befund trennt statische Profilstorage von beobachteten anderen
Runtimequellen. Er beweist weder einen bestimmten Consumeraufruf noch die Wirkung
eines Schärfe-, Konditions- oder Familiarityeingriffs. Die Zuordnung von
Nichtnull-Rohbytes zu UI-Familiarity bleibt offen. Es gibt keinen Kausaleffekt,
keine neue Leistungsstudie und keine Startpolicy-/Karrierefreigabe.

LF-normalisierte Hashes der tatsächlich geprüften Artefakte:

| Artefakt | SHA256 |
|---|---|
| Auswerter | `323ad1ab31c7f38c4cf6710c0483bf36ab09860caaf4d7f1c615d9d331c8e1fb` |
| passive-state.json | `26da5f3cdfcfa2c5be1eb5ff51fe70968c1cd1278991917dafd4c2f16de70a0c` |
| passive-state.svg | `25ba59680eaebf75bb2ca0edf20ce33fdb585669108750ed6df670b52cf3a322` |
| measurements.jsonl | `bef72df02120594398f6f8f9dfab94ef0304842ab83cf77ab7f74a2a7be5967f` |

Der SVG-Hash bindet das gelieferte Bild einschließlich Render-Metadaten;
numerische Reproduzierbarkeit wurde über die JSON-Aggregate geprüft.

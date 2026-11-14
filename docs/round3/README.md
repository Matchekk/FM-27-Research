# Forschungsrunde 3 – ATTR, MECH und TRAIN

Arbeitsstand 14.11.2026, Europe/Berlin. Drei tatsächliche Codex-Fachagenten
arbeiteten parallel in getrennten Git-Worktrees und Branches. Der Director allein
integriert und publiziert; native Prozesse werden ausschließlich zentral und
nacheinander unter NativeLease und persistentem Studienbudget ausgeführt.
Die drei Facharbeiten und der anschließende separate unabhängige Preflight sind
integriert. 124 integrierte Repositorytests und fünf historische Analysetests
bestehen. Zwei Reviewbefunde wurden vor Freeze korrigiert: fehlende unbegonnene
Technikplätze beim Vorbereitungsexport und unstrenge TRAIN-Session-/Slottypen.
[Unabhängige Abnahme](REVIEW.md) erlaubt zentrale ATTR-Vorbereitung/Technik,
noch keine Hauptserie. Noch kein neuer nativer Prozess oder Seed in dieser Runde.

## Verantwortlichkeiten

| Bereich | Branch | Exklusive neue Dateien | Freigabegrenze |
|---|---|---|---|
| ATTR | `codex/round3-attr` | `research/attr009.py`, eigene ATTR-009-Analyse/Tests/Vertrag, `ATTR.md` | Masken-/Rohdosis-Audit vor 384 Hauptmatches |
| MECH | `codex/round3-mech` | `research/startpolicy.py`, eigene MECH-002-Dateien, `MECH.md` | Passive erste Fortschreibung und Familiarity zwingend |
| TRAIN | `codex/round3-train` | `research/training002.py`, eigene TRAIN-002-Dateien, `TRAIN.md` | Keine Kalenderfortschreibung oder Hauptserie |
| Director | `main` | Integration, gemeinsame Übersicht/Queue/Baseline, native Ausführung | Ein Supervisor, maximal vier Worker |

Verbindlich ist [der Round-3-Auftrag](../../experiments/NEXT-ATTR-MECH-TRAIN-round3.md).
Keine Holdoutausführung, alten Seeds, Ersatzsimulationen oder automatische
Folgerunde. Historische Quellen und Messungen werden durch
`baseline.json` gegen Commit `7767d859e3a66a9aedcf9c1574f3e48dc8dc841f`
mit LF-normalisierten SHA256 geschützt.

## Zu Beginn erneut geprüft

Main war sauber und auf `origin/main`; dessen CI 43612939765 war erfolgreich.
DLL-Dateiversion 27.0.1, Produktbuild 27.0.1+2503222. DLL, Host, gebündeltes
Fixture und Katalog stimmen im direkten Dateihash mit VALID-002 überein:

| Artefakt | SHA256 |
|---|---|
| DLL | `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340` |
| Host | `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e` |
| Fixture | `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6` |
| Katalog | `c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c` |

Auch der erneut aus elf tatsächlichen Dateien berechnete Ressourcenfingerprint
`6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883`
stimmt überein. Upstreamquelle sauber auf v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be.
Dies ist ein statischer Identitätscheck, keine vorweggenommene Freigabe neuer
Eingriffe. Native Loader-/Laufzeitreceipts müssen vor einer Serie folgen.
Private Engine-/Spielmaterialien bleiben lokal.

## Vorläufige technische Abgrenzung

MECH findet derzeit keine passive Profilaufnahme nach dem ersten Simulationsschritt
und keine unveränderten Familiarity-Receipts. TRAIN findet keinen validierten
Karriere-Executor und keine unabhängigen RNG-/individuellen Teilnahmebelege.
Diese Lücken werden durch sichere Offline-Module diagnostiziert; daraus folgt
keine Freigabe der jeweiligen Hauptserie.

ATTR definiert rohe Abilitywerte 60→80 ausdrücklich als native Dosis. Die
Lab-Anzeige `raw/5` ist kein Beweis einer FM-Karriereanzeige. Der verbindliche
Auftrag erlaubt einen totalen Masken×Attributkontrast bei ausdrücklich
unidentifizierter Mechanismuszerlegung; fehlende passive Effektivitätsgrößen
werden weder synthetisch ergänzt noch experimentell neutralisiert.

Abschlusszahlen, Teststatus, unabhängiger Review und Prioritäten werden nach
den tatsächlichen Prüfungen ergänzt.

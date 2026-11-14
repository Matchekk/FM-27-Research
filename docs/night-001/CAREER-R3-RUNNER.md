# R3-DIAG: separater Supervisor vorbereitet

Eigener Branch `codex/night-career-r3-run`, Basis `99ef6b148e4a2411b1a1d1f60bbacb16b626631a`.
Neue Quellen ausschließlich unter `analysis/` und `tests/`; bestehende
Forschungsmodule, R3-Draft/Prereg und historische Studien unverändert.
Keine echte R3-Ausführung, kein Savehash/-read, kein Host/UI/Advance/Seedzugriff.

[Ausführungsvertrag](../../experiments/VALID-004-career-readonly-R3-RUN.md),
[finaler Quellenvertrag](../../data/night-001-career-r3/final-contract.json),
[neuer Runner](../../analysis/run_career004r3.py).

`prepare` liest nur Code, Wheel und Metadaten; `run` prüft Veröffentlichung,
exakte CI, finales Review und ausdrückliches Director-Proceed vor `Popen`;
`child` benötigt vorherige Job-/GO-/Parentzulassung; `export` liest nur vorhandene
Artefakte. Dieser Implementierungsauftrag führt ausschließlich `prepare` und
synthetische beziehungsweise harmlose Kerneltests aus. Kein echter `run`/`child`.

Alle späteren Savezugriffe liegen im einen Decoder mit180s Gesamt-/175s
Decoderfenster,3GiB Prozess-/Joblimit und engerem512KiB-Writer-Gesamtmaximum
innerhalb des1MiB-Verzeichnislimits. Fünf feste Stufen, kein Retry. Exklusiver
ReaderLease bleibt bis geprüftem Kernel-0/Decoderexit/finalem Capreadback erhalten.
Native Helper werden weder geändert noch deren3..10-Prozess-Gates umgangen.

Die finale Freigabedatei muss folgende geprüfte Angaben enthalten:

```json
{
  "experiment_id": "VALID-004-CAREER-R3-DIAG",
  "passed": true,
  "director_proceed": "published proceed",
  "published_commit": "vollstaendiger-veroeffentlichter-40-hex-SHA",
  "ci_run": 0,
  "review_document": "docs/night-001/CAREER-R3-RUNNER-REVIEW.md",
  "review_sha256": "normalisierter-64-hex-Reviewhash",
  "reviewed_contract_sha256": "normalisierter-64-hex-final-contract-Hash"
}
```

Platzhalter und CI0 sind absichtlich ungültig. Neues Runnerreview muss den echten
finalen Vertragshash im Text benennen und im selben freigegebenen Commit liegen.
Freigabedatei bleibt privat und wird nur vom Director nach Review/CI erstellt.
Ein Review des Offlineentwurfs oder alte R2-Freigabe reicht nicht.

Erreichbarer Befund bleibt ausschließlich eine dokumentierte originale
Parserexception mit begrenztem Fehlerort. Keine Taktik-/Replay-/Karrierefreigabe.
Ein tatsächlicher Diagnosepass benötigt einen separaten Auftrag; Fachagent
erstellt in dieser Stufe nur einen lokalen Commit, keinen Push.

Geprüfter Implementierungsstand nach Review:27 eigene Tests bestanden, davon vier echte
harmlose Windows-Kerneltests und23synthetische Fault-/Export-/Gateprüfungen.
Gesamtsuite271Tests:270bestanden, eine vorhandene Auslassung; fünf historische
Analysetests bestanden. NIGHT-001-Archivschutz bestätigt340unveränderte Dateien.
Kerneltests belegen GO vor Projektcode, Speicherabweisung unter64MiB-Testcap,
verweigerte Nachkommen bei Prozesslimit1 und Kill-on-close; letzteres wird
ausdrücklich nicht als Kernel-0-Nachweis akzeptiert. Keine `.fm`-Testdatei wurde
angelegt/geöffnet/gehasht. Finale CI und unabhängiger Runnerreview stehen noch aus.

Unabhängige rote Regressionen fanden vor jeder echten R3-Ausführung eine zu
späte GO-Fristprüfung und die Möglichkeit gültiger Cacheimporte trotz `-B`.
Version2 prüft Monoton-/UTC-Restzeit vor GO, isoliert Parent-/Childimports über
nicht existente private UUID-Cacheprefixe und pinnt `research/__init__.py`.
Außerdem wird `--release` vor Inhaltslesen auf den festen privaten JSON-Bereich
`local/night-001-career/releases/` und64KiB begrenzt. Sechs unveränderte externe
Reviewregressionen bestanden gegen den Fixstand; finaler unabhängiger Review folgt
nach erneutem Quellenfreeze. Es gab keinen Befund manipulierter Projektcaches.

Ein weiterer enger Exportreview fand `null` als verschachtelten Markereintrag:
Ein expliziter Dict-Typschutz klassifiziert ihn jetzt als `invalid_retained`.
Der öffentliche Export erhält alle fünf Stufen und den ursprünglichen Fehlschlag;
kein pauschales Schlucken zusätzlicher Exceptionklassen und keine Parseränderung.
Die vollständige synthetische Capture-Regression prüft den beschädigten Beleg
ohne erneuten Reader-/Snapshotzugriff. Auch nach zusätzlich fehlendem Nachhash
bleiben beide Messlücken ausdrücklich erhalten.

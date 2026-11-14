# Karriereforscher: R1/R2-Vorbereitung

Zwei neue, getrennte Readerverträge bereiten die Fortsetzung des unveränderten
[R0](CAREER.md) vor. Kein R1-/R2-Save wurde geöffnet. Die isolierte offizielle
Version0.12.4 ist privat vorhanden; Basisvenv und Fremdquellen wurden nicht geändert.

| Pfad | Prüfzweck | Besonderes Risiko | Aktueller Stand |
|---|---|---|---|
| [R1 Runtime V10](../../experiments/VALID-004-career-readonly-R1.md) | vorhandene Kompatibilitätsquellen eingefroren prüfen | Summary-Draftfallback, geänderte Layoutzuordnungen | nur vorbereitet |
| [R2 offizieller Reader](../../experiments/VALID-004-career-readonly-R2.md) | isoliertes Wheel0.12.4 prüfen | unbekannter Build/Schemaübernahme, advisory Coverage | nur vorbereitet |

Beide erhalten je180 s, harte3 GiB Prozess-/Job-Speichergrenze, einen echten
Decoderprozess, separate dauerhafte Attemptmarker und exklusiven Reader-Lease.
Keine Seeds, native Hosts, Kalenderaktionen oder Karriere-Replayfreigaben.
Windows-Kerneltests an harmlosen Prozessen beweisen Speicherabweisung und
Kill-on-close. Der tatsächliche Basisinterpreter wird direkt gestartet;
die Windows-Venv-Weiterleitung wäre ein zusätzliches Prozesskind.

Die neue CLI trennt `prepare` (nur Code-/Paketmetadaten), `run` (gesperrt bis
veröffentlichter exakter Commit/CI/Review), `child` (elterlicher Job-Handshake),
`export-status` (nur gespeicherte Ledgers) und `compare` (nur vorhandene Berichte).
Der Director muss zusätzlich ausdrücklich `published proceed` erteilen.
Worktreeausführung eines echten Passes wird früh abgelehnt.

Öffentliche Feldverträge benennen Quelle, Einheit und fehlende native Semantik.
Warnungen, fehlende Nenner, blockierte/unbegonnene Probeplätze und abgestürzte
Supervisorversuche bleiben sichtbar. Zwei Reader auf einer Datei ersetzen
keine unabhängigen Karriere-Replikate und keine echte UI-/native Feldkalibrierung.

Fachagent erstellt lokalen Commit, keinen Push. Nach Integration: unabhängiges
Review und CI, veröffentlichte Freigaben, anschließend allenfalls separat
zugewiesene serielle einmalige Lesepässe. Diese Vorbereitung autorisiert keinen Lauf.

Geprüfter Vorbereitungsstand: 157 Repositorytests und fünf historische
Analysetests bestanden, darunter elf neue Reader-/Budgettests. Acht bestehende
Archiv-/Reproduktionsprüfprogramme bestanden; NIGHT-001 meldet 340 unveränderte
Archivdateien. R0-Code, R0-Daten und vorhandene öffentliche Studien bleiben
bytegleich. GitHub-CI und unabhängiges Review dieser neuen Quellen stehen noch
aus; daraus wird keine Freigabe abgeleitet.

# VALID-004-CAREER-R1/R2: Vorbereitung und einmalige Lesepässe

`R1-contract.json` und `R2-contract.json` enthalten eingefrorene Verträge,
Feldquellen, Budgets und Quellenhashes. `isolated-package-preparation.json`
belegt lediglich die offizielle Wheelidentität und private Installation ohne
Basisupgrade. Die ursprünglichen Verträge bleiben unverändert.

Nach erfolgreicher Veröffentlichung/CI wurden R1/R2 jeweils einmal rein lesend
ausgeführt. R1 stoppte bei Training, R2 bei Taktiken. Alle24 Probeplätze einschließlich
13unbegonnener sind in `R1/coverage.json` und `R2/coverage.json` erhalten.
[Ergebnisbericht](../../docs/night-001/CAREER-R1-RESULTS.md), kein Retry und keine
native/Kalender-/Replayfreigabe.

Nach eigener veröffentlichter Freigabe dürfen `R1/coverage.json` beziehungsweise
`R2/coverage.json` vollständige anonyme Probeledgers erhalten; `cross-reader.json`
vergleicht ausschließlich stabile gleiche Snapshotbytes. Save, IDs, Namen,
private Pfade und Rohwarnungen bleiben privat. Releaseflags bleiben gesperrt.

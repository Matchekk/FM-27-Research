# ATTR-009-Bridge

Vorbereiteter Bereich für den vorregistrierten384-Match-Masken×Rohattributpilot.
Der initiale Offlinecommit enthält **keine neuen nativen Messungen/Seeds**.
[Vorregistrierung](../../experiments/ATTR-009-preregistration.md),
[technischer Arbeitsstand](../../docs/round3/ATTR.md).

Zentrale Vorbereitung erzeugt gehashte `contract.json`, `inputs.json`,
`mask-manifest.json`, `design-matrix.json`, Binärdifferenzaudit und die disjunkte
Seedreservierung vor Veröffentlichung/Registrierung. Private Konfigurationen,
Native-IDs, Original-PKM und Logs bleiben außerhalb dieses öffentlichen Bereichs.

Nach tatsächlicher Ausführung: erlaubte `technical.jsonl`/`main.jsonl`,
`manifest.json`, `technical-summary.json`, negativeKontrolle, `budget.json`,
vollständige `job-accounting.jsonl` und technischer `run-summary.json`.
`effects.json` und `block-contrasts.jsonl` entstehen nur bei vollständigen32
Blöcken und bestandenem Gate, sonst keine wissenschaftliche Analyse.

`analysis/verify_attr009.py` prüft Vertrag/Seeds/Archiv/öffentliche Messungen
portabel ohne native Starts. Eine zweite unabhängige Reviewrechnung ist davon
getrennt notwendig. Keine FM-Anzeigekalibrierung oder Mediation identifiziert;
Eingriff ist nativeRoh60→80, ausschließlich im kontrollierten D00-Fixture.

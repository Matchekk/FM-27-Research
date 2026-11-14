# TACT-001-P1C – unabhängiger Seed-/Punkte-Präzisionspilot

D15 gegen D00, beide bisherigen synthetischen Gegner/Seiten,512 Hauptmatches,
128 unabhängige Blöcke. D09 bleibt archiviert; keine Holdout-/Karriereausführung.
[Vorregistrierung](../../experiments/TACT-001-P1C-preregistration.md) ·
[Vertrag](../../research/specs/TACT-001-P1C.json) ·
[VALID-003 nur geplant](../../experiments/VALID-003-plan.md).

`seed-plan.json` und `excluded-seeds.json`:131 disjunkte neue Reservierungen und
gehashte Ausschlussmenge. `inputs.json`, `design-matrix.json` und
`binary-diff-audit.json`:acht unveränderte P1B-Eingaben, D15 einziges Paket.
`historical-archive.json`:sämtliche bisherigen versionierten Analyse-/Daten-/
Experiment-/Vertragsdateien gegen317dec75. `planning-before-run.json`:bedingte
Planung aus P1B, kein neues Wirksamkeitsergebnis.

Später getrennt `technical.jsonl`, `technical-summary.json`, `manifest.json`,
`main.jsonl`, `effects.json`, `block-contrasts.jsonl`, `budget.json` und
`job-accounting.jsonl`. Nur eingefrorene Whitelistfelder; Rohlogs/Spielmaterial/
PKM/Binärinputs/personenbezogene IDs bleiben privat. Keine fehlenden Werte als Null.

Offline nach Abschluss:
```
python analysis/verify_tact001p1c.py
python analysis/analyse_tact001p1c.py
python -m unittest discover -s tests -v
```
Keine dieser drei Prüfungen startet neue native Matches.

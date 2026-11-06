# ATTR-004 – Daten und Provenienz

- [Vorregistrierung](../../experiments/ATTR-004-cross-tactic.md) und [Auswertung](../../analysis/analyse_attr004.py).
- [Manifest](manifest.json) mit Build, Engine-/Host-/Fixture-Hashes, Setup-Hashes, Szenarien und Seedplan.
- [Technische Prüfläufe](validation.jsonl) und [Validierungsbericht](validation-summary.json). Die Prüfläufe gehören zu einer eigenen Seedmenge und bleiben außerhalb der Effektschätzung.

JSONL-Zeilen enthalten den nativen Endstand und die unveränderten Teamstatistikwerte in Heim-/Auswärtsreihenfolge. `tested_side` bezeichnet die Seite des behandelten Teams. `pair_id` gruppiert Szenario, Seed und Wiederholungsindex. `setup_sha256` identifiziert das vollständige binäre Setup des Arms. `baseline_setup_sha256` referenziert das entsprechende Baseline-Setup. Die Beleg-Hashes identifizieren lokal geprüfte Dateien. Native Logs, Readback-Dumps, Fixture-Dateien, Spielstände und ausführbare Dateien bleiben lokal.

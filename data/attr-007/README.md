# ATTR-007 – Daten und Provenienz

[Vorregistrierung](../../experiments/ATTR-007-vorregistrierung.md) · [Analysecode](../../analysis/analyse_attr007.py)

Das [Manifest](manifest.json) enthält Versions- und Setup-Identität, die nativ gelesenen Positionen, die Eingriffe je Arm und die Seed-Listen. Die [technischen Matchzeilen](validation.jsonl) und der [Validierungsbericht](validation-summary.json) dokumentieren die Freigabe mit separaten Prüfseeds.

Die JSONL-Zeilen enthalten den Endstand und die native Teamstatistik in Heim-/Auswärtsreihenfolge. `pair_id` gruppiert alle Arme desselben Seeds und Wiederholungsindex. Die SHA-256-Werte belegen die lokal geprüften Setups, Laufprotokolle, Readbacks und Startbelege. Vollständige Dumps, Spielstände und Originalspielmaterial verbleiben lokal.

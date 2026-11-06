# ATTR-007 – Daten und Provenienz

[Vorregistrierung](../../experiments/ATTR-007-vorregistrierung.md) · [Ergebnisbericht](../../experiments/ATTR-007-ergebnisse.md) · [Analysecode](../../analysis/analyse_attr007.py)

- [Manifest](manifest.json) mit Build, Adapter-, Fixture- und Setup-Hashes, den nativ gelesenen Positionen, den Eingriffen je Arm und den Seed-Listen.
- [Technische Matchzeilen](validation.jsonl) und [Validierungsbericht](validation-summary.json) mit 32 Prüfmatches und der getrennten Negativprobe.
- [Hauptmessungen](matches.jsonl) mit 1.600 Matches in 200 vollständigen Achtarmblöcken.
- [Effektarchiv](effects.json) mit 84 explorativen Tests, dem deskriptiven Gesamteffekt, der exakten Shapley-Prüfung und der Fallzahlplanung.

Die JSONL-Zeilen enthalten den Endstand und die native Teamstatistik in Heim-/Auswärtsreihenfolge. `pair_id` gruppiert alle Arme desselben Seeds und Wiederholungsindex. Die SHA-256-Werte belegen die lokal geprüften Setups, Laufprotokolle, Readbacks und Startbelege. Vollständige Dumps, Spielstände und Originalspielmaterial verbleiben lokal.

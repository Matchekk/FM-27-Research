# ATTR-006 – Daten und Provenienz

[Vorregistrierung](../../experiments/ATTR-006-vorregistrierung.md) · [Ergebnisbericht](../../experiments/ATTR-006-ergebnisse.md) · [Analysecode](../../analysis/analyse_attr006.py)

- [Manifest](manifest.json) mit Versions- und Setup-Identität, den nativ gelesenen Positionen, den Seed-Listen und den Fallzahlen.
- [Technische Matchzeilen](validation.jsonl) und [Validierungsbericht](validation-summary.json) mit acht Prüfmatches und der getrennten Negativprobe.
- [Hauptmessungen](matches.jsonl) mit 600 Matches in 300 vollständigen Paaren.
- [Effektarchiv](effects.json) mit Primärtest, explorativen Sekundärtests und Sensitivitätsprüfungen.

Die JSONL-Zeilen enthalten den Endstand und die native Teamstatistik in Heim-/Auswärtsreihenfolge. `pair_id` gruppiert beide Arme desselben Seeds und Wiederholungsindex. Die SHA-256-Werte belegen die lokal geprüften Setups, Laufprotokolle, Readbacks und Startbelege. Der native Laufstand ist Commit `3bca400`. Commit `a9a9113` behebt die Typkonvertierung der Entscheidung beim JSON-Export. Vollständige Dumps und Originalspielmaterial verbleiben lokal.

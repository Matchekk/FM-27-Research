# ATTR-005 – Daten und Provenienz

[Vorregistrierung](../../experiments/ATTR-005-position-screening.md) · [Ergebnisbericht](../../experiments/ATTR-005-ergebnisse.md) · [Analysecode](../../analysis/analyse_attr005.py)

- Das [Manifest](manifest.json) enthält die Build-, Engine-, Host- und Fixture-Identität, beide Seed-Listen, die binären Setup-Hashes und die nativ bestätigte Positionszuordnung. Die angegebenen Startelf- und Kaderplätze zählen ab null.
- [Technische Messungen](validation.jsonl) und [Validierungsbericht](validation-summary.json) dokumentieren die separate Freigabeserie mit 36 Matches.
- Die [Hauptmessungen](matches.jsonl) enthalten 900 Matches in 100 vollständigen Neunerblöcken. Das Manifest weist keine Fehlversuche oder Ausschlüsse aus.
- Das [Effektarchiv](effects.json) enthält 12 primäre und 66 sekundäre Tests mit Effektgrößen, Varianzen, Intervallen, rohen und korrigierten p-Werten sowie die Fallzahlplanung für 18 xGD-Kontraste.

Die Matchzeilen speichern die native Teamstatistik und den Endstand in Heim-/Auswärtsreihenfolge. `tested_side` bezeichnet die behandelte Seite. `pair_id` gruppiert alle Arme desselben Seeds und Wiederholungsindex. Die Hashes belegen lokal geprüfte Eingaben, Laufprotokolle und Readbacks. Die Dateien mit Originalspielmaterial und vollständigen nativen Dumps verbleiben lokal.

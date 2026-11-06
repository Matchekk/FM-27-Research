# Daten und Metadaten

## Archiv vom 6. November 2026

| Pfad | Umfang |
|---|---|
| [matches/](matches/) | 2.504 vollständige Matchmessungen, zwei getrennte Negativproben, Manifest, Validierung und vollständige Effektschätzungen |
| [historical/](historical/) | 228 ältere Matchmessungen in zwei getrennten Serien und Vergleich mit den früheren Zusammenfassungen |
| [training/](training/) | Spielerdifferenzen mit versuchslokalen Kürzeln, Kalender, Belastungsaggregate und A/A-Kontrolle |

Die Matchdaten enthalten den Endstand und die native Teamstatistik in Reihenfolge Heim/Auswärts. `tested_side` legt die Auswertungsrichtung fest. `setup_sha256` identifiziert das Arm-Setup, `baseline_setup_sha256` das geteilte Ausgangssetup. `pair_id` gruppiert Phase, Szenario, Seed und Wiederholung. Innerhalb einer solchen Gruppe bildet jede Intervention ihren Kontrast zur gleichen Baseline. SHA-256-Felder für Rohlogs, Startup-Belege und Eingabedumps dienen als Herkunftsnachweise für lokal geprüfte Dateien. Sie sind keine öffentlichen Downloadverweise.

Die Analyse lässt sich ohne FM27 oder Adapter mit Python und NumPy 2.3.5 ausführen.

```sh
python analysis/verify_matches.py
```

Das Skript rekonstruiert je Phase sämtliche Effektschätzungen und vergleicht sie mit `effects.json`. Es verwendet 20.000 Bootstrap-Stichproben, 49.999 zufällige Vorzeichenpermutationen mit Plus-eins-Korrektur und einen deterministischen RNG-Seed je Kontrast. Die historischen Zusammenfassungen behalten ihre ursprünglichen gepaarten t-Intervalle. Das Skript prüft außerdem die importierten Trainingsstichproben, ausgewählte Endpunktdifferenzen und die Kalenderexposition.

Markdown fasst die Forschung zusammen; **JSON/JSONL** dient der verlustarmen, maschinenlesbaren Aufbewahrung. CSV ist optionaler Export, kein Pflichtformat.

## Mindestformat einer JSONL-Zeile (Beispielschema, keine echten Daten)

```json
{"experiment_id":"ATTR-001","build":"27.0.0+2493426","adapter_version":"v1106","setup_sha256":"SHA256_HIER","seed":1001,"pair_id":"scenario1-1001","arm":"baseline","status":"completed","xg_for":1.4,"xg_against":0.8}
```

Zusätzlich nach Design: Team/Gegner, taktische Konfiguration, Spieler-IDs in nicht-personenbeziehbarer Form, Rolle/Position, Intervention, Tore, Schüsse, Log-/Setup-Verweis, Zeitstempel, Fehlergründe. Eine zweite Zeile mit identischer `pair_id` bildet die Interventionsgruppe. `setup_sha256` muss die **vollständige Ausgangskonfiguration** abbilden; die Intervention wird separat dokumentiert. Für unterschiedliche Builds dürfen Daten nicht ohne Kennzeichnung aggregiert werden.

## Datenqualität
- Jede Paarung muss eindeutig und vollständig sein.
- Fehlerhafte Läufe mit `status` und Grund protokollieren, nicht als gültige Nullen ausgeben.
- Große oder geschützte Rohartefakte **nicht** in Git ablegen; nur kontrollierte Auszüge, Zusammenfassungen und Hashes/Verweise.
- Datensätze erst als wissenschaftlich geprüft markieren, wenn Herkunft, Version und Analyse nachvollziehbar sind.

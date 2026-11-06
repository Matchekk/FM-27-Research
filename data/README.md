# Daten und Metadaten

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

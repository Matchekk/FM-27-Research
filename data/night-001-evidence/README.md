# NIGHT-001-EVIDENCE

Gezielte Quellenprüfung vom14.11.2026, zehn Primärseiten bzw. Originalberichte.
[Bericht und drei Folgefragen](../../docs/night-001/EVIDENCE.md).

- `sources.json`: eigene kurze Paraphrasen, Versionen, Autor-Fallzahlen und
  explizite Unknowns; keine eigene Replikation oder neue FM-Leistungsdaten.
- `access-checks.json`: zwölf anonyme HTTP-Abrufe, zehn200 und zwei404;
  nur Bytehashes/Metadaten, keine ganzen Seiten oder Anlagen gespeichert.

Die Zahlen der externen Versuche sind Autorenangaben. Segmentzahlen werden
nicht unbesehen zu unabhängigen Samples addiert. Guideseiten und Dummy-PLD
sind keine wissenschaftlichen Fallzahlen. Dynamische Transporthashes ersetzen
keine unveränderliche Studienversion; macOS-Berichte sind perCommit gepinnt.

Offlineprüfung ohne Netzwerk-/Native-/Savezugriff:

```powershell
python analysis/audit_night_evidence.py
python -m unittest tests.test_night_evidence -v
```

Der Schemaerfolg bestätigt Metadatenkonsistenz, keine externe Ergebniswahrheit.
Keine Quellen werden durch diese Sammlung automatisch hochgestuft.

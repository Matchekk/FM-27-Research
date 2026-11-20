# Vorab festgelegte CA-Referenz zum 30.03.2028

Beim Einfrieren war der genaue Jahresendpunkt noch offen. Die Arbeitsgruppe kannte bereits den Juni-Verlauf derselben Welt. Dieser Vergleich prüft ein späteres Datum innerhalb der untersuchten Karriere. Eine unabhängige Testkarriere fehlt.

Für den Retentionszweig wurden zwei CA-Punktreferenzen für exakt den 30.03.2028 eingefroren. Die bisherigen Kurzzeittests legten bereits Referenzen für 31 beziehungsweise 61 Tage fest. Der Jahrestermin erhält eine eigene Auswertung. Eingaben sind ausschließlich die abgeglichenen Spielerwerte vom 31.01. und 30.03.2027. Der März-Save stimmt zwischen Ausgangsuniversum und Retentionszweig überein. [Frühere 61-Tage-Referenz](../../research/pa-reach-001/analysis/prospective_ca61.py) · [Jahresbeleg mit Hashes und Gruppengrößen](../../research/pa-reach-001/manifests/prospective-ca-20280330.json)

- **Konservative Referenz.** Die gespeicherte CA vom 30.03.2027 bleibt als Punktprognose unverändert.
- **Vorherige Rate als Vergleich.** Die beobachtete CA-Differenz aus 58 Tagen wird mit `366/58` multipliziert und zur März-CA addiert. Der exakte 12-Monats-Abstand enthält den Schalttag. Begrenzung auf 1–200 wie im früheren Kurzfristvergleich, keine Rundung bei der Auswertung. Die räumlich und zeitlich unveränderte Rate dient als bewusst einfache Vergleichsregel über einen längeren Horizont. Es werden keine Modellparameter geschätzt.

Die feste Population umfasst **59.784** Feldspieler unter 28 Jahren mit bekannter Märzposition und eindeutiger Zuordnung per Datenbank-ID und Geburtsdatum an beiden Eingabetagen. Alter und `PA−CA` stammen vom 30.03.2027. Altersgruppen sind unter 18, 18–20, 21–23 und 24–27. Lückengruppen sind 0–10, 11–30 und über 30. Eine negative Lücke wäre eine eigene Gruppe. Alle Regeln und numerischen Einzelprognosen wurden vor dem Zielwertzugriff eingefroren. Die Einzeldatei bleibt privat.

Bei der späteren Prüfung zählen ausschließlich der exakte Spieltag im Retentionszweig und doppelt abgeglichene CA-Werte auf `27.1.0+2505117`. Ausfälle bleiben pro Gruppe im eingefrorenen Nenner. Beide Regeln verwenden dieselben beobachtbaren Paare. Gesamt und je Alters-/Lückenzelle sind gepaarter MAE, RMSE, mittlerer Fehler `Prognose−Messung` und die MAE-Differenz `Rate−unveränderte CA` zu berichten. Fehlende Zielwerte bleiben ohne Ersatz. Abweichende Datums-/Buildstände erfordern einen getrennten Befund. Der Test misst Punktprognosegüte innerhalb eines Karriereursprungs. Die individuelle Erreichungswahrscheinlichkeit und Übertragbarkeit auf andere Karrieren bleiben offen. [Eingefrorener Rechenweg](../../research/pa-reach-001/analysis/prospective_ca_year.py) · [Freigabekriterien](MODEL_DESIGN.md)

Nach Übernahme des exakten und bestätigten Ziel-Snapshots erzeugt der CLI-Aufruf das aggregierte JSON. Die beiden Hashes müssen aus der bestätigten Zielreceipt stammen. Die bereits eingefrorene Liste wird unverändert eingesetzt.

```text
python research/pa-reach-001/analysis/prospective_ca_year.py score RETENTION_PANEL FORECAST_LIST --save-sha256 SAVE_SHA256 --native-sha256 NATIVE_SHA256
```

## Gemessen am 30.03.2028

Bei **55.079 von 59.784** Spielern war die exakte Jahres-CA messbar. **4.705** Zielwerte fehlten. Unveränderte März-CA ergab einen MAE von **2,932 CA**, die Fortschreibung der 58-Tage-Rate **4,108 CA**. Die individuelle Rate erhöhte den MAE um 1,176 Punkte. Auch der RMSE stieg von 5,432 auf 7,588. Der mittlere Fehler wechselte von −1,798 auf +2,019 CA. [Zielauswertung mit Quellhashes und Zellnennern](../../research/pa-reach-001/manifests/prospective-ca-20280330-score.json)

| Ausgangsalter | PA−CA 0–10 | PA−CA 11–30 | PA−CA >30 |
|---|---:|---:|---:|
| U18 | 0,854 → 4,979 | 5,452 → 8,491 | 10,553 → 8,049 |
| 18–20 | 0,593 → 2,503 | 2,886 → 5,154 | 6,015 → 6,617 |
| 21–23 | 0,798 → 2,616 | 1,876 → 3,032 | 3,554 → 4,126 |
| 24–27 | 1,388 → 2,109 | 2,395 → 3,129 | 4,006 → 4,828 |

Die Zellen zeigen den MAE der unveränderten CA gefolgt von der individuellen Rate. Bei U18-Spielern mit mehr als 30 CA-Punkten zur PA verbesserte die Rate den Fehler um 2,503 Punkte. In den elf übrigen Gruppen erhöhte sie ihn. Die Zeitprüfung betrifft eine Karrierewurzel.

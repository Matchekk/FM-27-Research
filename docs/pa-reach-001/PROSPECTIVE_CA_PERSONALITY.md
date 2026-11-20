# Verändert Persönlichkeit den Fehler der Jahres-CA-Prognose?

## Zeitlich nachfolgender Test bis 30. März 2029

Der Vergleich auf **63.054 von 65.695** eingefrorenen Profilen ergab einen Zusatznutzen der fünf Attribute und der Altersinteraktion von **0,050 CA-Punkten** beim mittleren absoluten Fehler. Bei 2.641 Profilen fehlte ein eindeutiger Folgewert. Bei keinem vollständigen Paar änderte sich die PA. Der mittlere gerichtete Fehler stieg durch die Erweiterung von +0,465 auf +0,530 CA. Beide Modelle überschätzten die End-CA im Mittel.

| Auswahl am Ausgangstag | Paare | MAE konstante CA | MAE Grundmodell | MAE mit Persönlichkeit und Attributen |
|---|---:|---:|---:|---:|
| Alle | 63.054 | 3,728 | 3,196 | 3,146 |
| Spieler bereits im Modellfit des Vorjahres | 46.778 | 2,364 | 2,492 | 2,504 |
| Spieler im Modellfit des Vorjahres ungesehen | 16.276 | 7,647 | 5,220 | 4,989 |
| U18, mehr als 30 Punkte PA-Lücke | 13.894 | 9,641 | 6,248 | 5,869 |
| U18, höchstens 10 Punkte PA-Lücke | 2.375 | 0,692 | 1,086 | 1,635 |

Über alle Spieler fiel der RMSE von 6,794 bei konstanter CA über 4,719 im Grundmodell auf 4,567 im erweiterten Modell. Innerhalb dieser Karriere profitierten insbesondere junge Spieler mit großer Ausgangslücke. Bei U18 und kleiner Lücke sowie bei den bereits im Vorjahr zum Fit verwendeten Spielern war konstante CA genauer. Der Vergleich misst den gemeinsamen Vorhersagebeitrag aller ergänzten Merkmale. Mit einer unabhängigen Karriere lässt sich erst prüfen, ob dieselben Vorteile übertragbar sind. [Alle zwölf Gruppen, Ausfälle und Fehlermaße](../../research/pa-reach-001/manifests/annual-personality-outcome-20290330.json)

## Vor dem Test festgelegtes Verfahren

Für 65.695 Feldspieler liegen vorab eingefrorene Prognosen vor. Bei weiteren 56 fehlte der eindeutige Scout-Abgleich. 49.338 der prognostizierten Spieler hatten bereits zum Schätzen der Koeffizienten im Vorjahr beigetragen, 16.357 kommen neu in diesen Vergleich. Die Regressionen lernten aus denselben 53.423 Jahresverläufen. Bei 4.182 weiteren geprüften Ausgangsprofilen fehlte der bestätigte Jahresendwert. [Prognosehash, Eingangsprüfungen und Modellkoeffizienten](../../research/pa-reach-001/manifests/annual-personality-forecast-20290330.json) · [Reproduktion](../../research/pa-reach-001/analysis/annual_personality_ca.py)

Vor der Messung am 30.03.2029 vergleichen wir drei Punktprognosen auf demselben Spielerbestand. Das Ziel ist die CA am exakten Endtag. Die Lernperiode reicht vom 30.03.2027 bis 30.03.2028, die zeitlich nachfolgende Prüfung vom 30.03.2028 bis 30.03.2029. Beide Perioden liegen im selben Zubieta-Universum. Ein bereits im Lernjahr beobachteter Spieler darf auch im Folgejahr eine Vorhersage erhalten. Seine Identität geht nicht in die Modellformel ein.

* **Konstante CA** übernimmt den gemessenen Ausgangswert.
* **Grundmodell** schätzt die jährliche CA-Änderung linear mit einer eigenen Konstante je Alters- und PA-Lückenzelle (vier Altersgruppen, drei Lückengruppen), dem genauen Ausgangsalter in abgeschlossenen Jahren, der Ausgangslücke, CA und der Feldposition.
* **Erweitertes Modell** ergänzt Professionalität, Ehrgeiz, Zielstrebigkeit, Natural Fitness und Verletzungsanfälligkeit auf der 1–20-Skala sowie Alter × Professionalität. Die Auswahl entspricht dem bestehenden 58-Tage-Vergleich. [Frühere Zusammenhänge](CORRELATION_REPORT.md)

Beide Regressionen verwenden gewöhnliche kleinste Quadrate auf identischen Trainingsfällen. Beide Punktprognosen werden auf die CA-Skala 1–200 begrenzt. Die Position wird im strukturellen und nativen Panel abgeglichen. Alle fünf zusätzlichen Eingaben müssen am jeweiligen Starttag in Save und geklammertem Scout übereinstimmen. Einschluss verlangt einen Feldspieler, gültige heutige CA und PA, ein konsistentes Geburtsdatum, einen identitätsbestätigten Ausgangsstand und einen Endtag spätestens am 28. Geburtstag. Echte PA-Änderungen werden am Endtag gesondert gezählt. Fehlende Folgewerte führen zum Ausschluss aus dem gepaarten Fehlervergleich.

Primär vergleichen wir den mittleren absoluten Fehler des erweiterten Modells mit dem Grundmodell. Zusätzlich berichten wir RMSE, mittleren gerichteten Fehler (Prognose minus Messung), Fehler je Alters-/Lückenzelle und bei im Lernjahr erstmals ungesehenen Testpersonen. Private Einzelprognosen werden vor dem Zieltermin gehasht. Interpretierbar ist der Zusatznutzen dieser gemeinsam geprüften Ausgangsvariablen für die beobachtete Jahres-CA innerhalb dieser Karriere. Für individuelle PA-Erreichung und kausale Auswirkungen wäre weitere Evidenz erforderlich.

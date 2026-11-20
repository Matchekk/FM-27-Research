# Alters- und CA-Lücken-Wachstumstabelle für den 30.03.2028

Zwei CA-Punktreferenzen für den Retentionszweig sind vor dem Zielwertzugriff eingefroren. Die erste übernimmt die CA vom 30.09.2027. Die zweite addiert den erwarteten Zuwachs aus einer in zwölf Alters-/Lückenzellen unterteilten Wachstumstabelle. Der Vergleich prüft, ob die beobachtete Gruppenrate einen neuen Zeitraum derselben Karriere besser beschreibt als unveränderte CA. Der separate Januar–März-Jahresvergleich bleibt eigenständig. [Versiegelte Abrechnung](../../research/pa-reach-001/manifests/prospective-ca-groups-0930.json) · [Jahresreferenz](PROSPECTIVE_CA_YEAR.md)

Die Wachstumsrate jeder Zelle stammt aus den beobachteten CA-Differenzen vom 30.03. bis 30.09.2027 über **184 Tage**. Alter und `PA−CA` stammen beim Lernen aus dem März. Die Gruppen sind U18, 18–20, 21–23, 24–27 und je Altersgruppe 0–10, 11–30, über 30 CA-Punkte Abstand. Die Zuordnung der September-Spieler verwendet ihren dann bekannten September-Zustand. Hat ein Spieler in genau dieser Zelle zur Rate beigetragen, werden sein eigener Zuwachs und sein Beitrag zum Nenner vor seiner Prognose entfernt. Die erwartete CA ist die September-CA plus der so berechnete mittlere Zuwachs mal `182/184`, auf 1–200 begrenzt. Die Auswertung verwendet den Wert vor Rundung.

Für die Schätzung waren 62.047 März-Feldspieler unter 28 mit gültigem CA-/PA-Paar und Positionsangabe zugelassen. Bei 5.514 fehlte eine bestätigte September-CA derselben Datenbank-ID und desselben Geburtsdatums. Die Prognosepopulation umfasst 68.485 gültige September-Feldspieler unter 28. Davon lieferten 13.706 keinen eigenen historischen Beitrag. Bei 44.918 Prognosen wurde der Beitrag des Spielers aus seiner September-Zelle entfernt. In den übrigen Fällen lag sein historischer Beitrag in einer anderen Zelle. Die Einzelprognosen bleiben privat. Dezember-Werte fließen in keinen der Schritte ein.

Für genau den 30.03.2028 auf demselben Build und Retentionszweig werden je Zelle und insgesamt MAE, RMSE, mittlerer Fehler und die gepaarte MAE-Differenz beider Regeln berechnet. Beide Regeln verwenden dieselben gültigen Zielpaare. Fehlende Zielwerte bleiben im eingefrorenen Nenner. Das Ergebnis ist eine zeitlich getrennte Prüfung innerhalb einer Karriere und keine unabhängige Kalibrierung.

```text
python research/pa-reach-001/analysis/prospective_ca_groups.py score RETENTION_PANEL FORECAST_LIST --save-sha256 SAVE_SHA256 --native-sha256 NATIVE_SHA256
```

## Gemessen am 30.03.2028

Bei **67.050 von 68.485** Spielern war die exakte Ziel-CA messbar. **1.435** Zielwerte fehlten. Der MAE sank von **1,995 CA** für unveränderte September-CA auf **1,814 CA** mit der Wachstumstabelle. Die gepaarte Differenz beträgt **−0,181 CA**. Der RMSE sank von 3,961 auf 2,844, der mittlere Fehler änderte sich von −1,926 auf +0,097 CA. [Zielauswertung mit Quellhashes und Zellnennern](../../research/pa-reach-001/manifests/prospective-ca-groups-20280330-score.json)

| Septemberalter | PA−CA 0–10 | PA−CA 11–30 | PA−CA >30 |
|---|---:|---:|---:|
| U18 | 0,647 → 0,833 | 2,616 → 2,493 | 5,611 → 4,131 |
| 18–20 | 0,412 → 0,595 | 1,626 → 1,848 | 2,934 → 2,487 |
| 21–23 | 0,294 → 0,518 | 0,862 → 1,202 | 1,604 → 1,964 |
| 24–27 | 0,262 → 0,283 | 0,486 → 0,604 | 1,122 → 1,313 |

Die Zellen zeigen den MAE der unveränderten CA gefolgt von der Wachstumstabelle. Drei der zwölf Zellen verbesserten sich. Den größten Rückgang hatte U18 mit `PA−CA > 30`, um 1,479 CA. Der gemeinsame Fehler sank, obwohl er in neun Zellen stieg. Das Ergebnis beschreibt ausschließlich den späteren Zeitraum derselben Karriere.

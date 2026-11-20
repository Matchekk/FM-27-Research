# Versiegelte Referenz für das CA-Maximum an fünf Stichtagen

Die Referenz ist auf die CA-Skala bis 200 begrenzt. Bei 1.567 der 65.751 vorab gespeicherten Profile übersteigt die obere Gruppengrenze die persönliche März-PA. Untergrenze und Median liegen bei allen innerhalb der persönlichen März-PA. Das ist eine Einschränkung der groben Lückengruppen, insbesondere für den einzelnen Spieler. Die spätere Bewertung verwendet die unverändert versiegelten Werte.

Für **65.751** Feldspieler sind drei CA-Punktwerte für den Retentionszweig eingefroren. Das Ziel ist die höchste gespeicherte CA unter den fünf exakten Messungen **30.03., 30.06., 30.09. und 30.12.2028 sowie 30.03.2029**. Die Start-CA ist Teil des Maximums. Der Geburtstagshorizont verlangt, dass der Endtag spätestens auf den 28. Geburtstag fällt. Das Verfahren beschreibt ein über fünf Stichtage messbares CA-Maximum innerhalb eines Jahres. [Manifest mit Quellhashes und Gruppengrößen](../../research/pa-reach-001/manifests/prospective-peak-ca-20290330.json)

Die Lernperiode verwendet die gleichen fünf Kalendertage ein Jahr früher. Von 57.620 geeigneten Feldspielern hatten **51.336** alle fünf CA-Messwerte. Bei 6.284 fehlte wenigstens ein Wert. Fehlende Messungen werden im Manifest nach Datum und Fehlermuster gezählt. Die Längsschnittbindung verwendet die bestätigten Saves und unabhängigen Inventare, Datenbank-ID und Geburtsdatum. Alter und `PA−CA` werden jeweils am Start gemessen. Die vier Altersgruppen U18, 18–20, 21–23 und 24–27 werden mit den drei Lücken 0–10, 11–30 und über 30 kombiniert.

Je Zelle wird die empirische Verteilung des jeweils größten beobachteten CA-Zuwachses gebildet. P10, Median und P90 sind die kleinsten Werte, deren empirische kumulierte Häufigkeit die jeweilige Schwelle erreicht. Bei **29.734** Zielprofilen wurde der eigene historische Zuwachs aus der Zielzelle entfernt. Die drei Zuwächse werden zur März-2028-CA addiert und bei 200 begrenzt. Da die Start-CA im beobachteten Maximum enthalten ist, kann keine Prognose darunter fallen. Der Vergleich ohne Wachstum setzt alle drei Prognosewerte auf die Start-CA. Die privaten Einzelprognosen ergeben bei Wiederholung denselben Hash. [Versiegelungs- und Auswertungscode](../../research/pa-reach-001/analysis/prospective_peak_ca.py)

Erst mit fünf gehashten und identitätsgeprüften Zielmessungen auf `27.1.0+2505117` wird je Zelle und insgesamt ausgewertet. Die Auswertung zählt fehlende Zielmessungen separat und verwendet für beide Regeln dieselben vollständigen Paare. Berichtswerte sind der Anteil der Zielmaxima im geschlossenen P10–P90-Intervall, mittlere Intervallbreite und der Fehler der Medianprognose. Die Bewertung erfolgt zeitlich getrennt innerhalb einer Karriere. Spitzen zwischen den Stichtagen und PA-Erreichungswahrscheinlichkeiten werden hier nicht gemessen.

```text
python research/pa-reach-001/analysis/prospective_peak_ca.py score RETENTION_PANEL FORECAST_LIST TARGET_SOURCE_HASHES_JSON
```

## Gemessen bis zum 30.03.2029

Bei **61.365 von 65.751** Spielern lagen alle fünf Messungen vor. **4.386** hatten mindestens eine Lücke. Das geschlossene P10–P90-Intervall enthielt **89,50 %** der beobachteten Maxima und war im Mittel **8,948 CA-Punkte** breit. Die Medianprognose senkte den MAE von **3,486** bei konstanter Start-CA auf **2,701 CA**. Der mittlere Fehler änderte sich von −3,486 auf −0,322 CA, der Median des absoluten Fehlers blieb bei 1 CA. Die konstante Start-CA traf das beobachtete Maximum bei 47,69 % der vollständigen Verläufe exakt. [Zielabrechnung mit Quellhashes und Ausfallmustern](../../research/pa-reach-001/manifests/prospective-peak-ca-20290330-score.json)

| Alter | PA−CA | Vollständige Verläufe | Abdeckung | Breite in CA | MAE konstant | MAE Medianprognose |
|---|---:|---:|---:|---:|---:|---:|
| U18 | 0–10 | 2.375 | 94,11 % | 3 | 0,661 | 0,661 |
| U18 | 11–30 | 3.128 | 94,05 % | 12 | 4,216 | 3,700 |
| U18 | >30 | 13.931 | 78,52 % | 20 | 9,613 | 6,423 |
| 18–20 | 0–10 | 1.991 | 89,70 % | 2 | 0,663 | 0,663 |
| 18–20 | 11–30 | 10.478 | 94,52 % | 8 | 2,224 | 2,161 |
| 18–20 | >30 | 2.591 | 93,44 % | 13 | 4,537 | 3,995 |
| 21–23 | 0–10 | 3.136 | 93,78 % | 2 | 0,482 | 0,482 |
| 21–23 | 11–30 | 11.391 | 90,83 % | 5 | 1,410 | 1,410 |
| 21–23 | >30 | 1.383 | 93,56 % | 10 | 2,827 | 2,800 |
| 24–27 | 0–10 | 3.743 | 91,13 % | 1 | 0,388 | 0,388 |
| 24–27 | 11–30 | 6.593 | 92,78 % | 3 | 0,736 | 0,736 |
| 24–27 | >30 | 625 | 94,24 % | 6 | 1,690 | 1,690 |

Die fehlenden Messwerte verteilen sich auf 326 am 30.06., 3.317 am 30.09., 3.486 am 30.12. und 2.642 am 30.03.2029. Einzelne Spieler fehlen an mehreren Tagen. Die größte jüngste Lückengruppe hatte trotz der breitesten Intervalle die niedrigste Abdeckung. Die diskreten, geschlossenen Quantilintervalle und der Ausschluss unvollständiger Pfade prägen die Abdeckung. Sie ist für diesen Zeitabschnitt binnen einer Karriere gemessen.

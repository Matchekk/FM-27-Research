# Kalibrierungsbericht · noch kein freigegebenes Modell

Im bestätigten historischen TRAIN-005-Kontrollarm gibt es 59.730 Feldspieler unter 28 an der Baseline. Der feste Zielwert ist ihre jeweilige Start-PA. Das folgende Ergebnis beruht auf maximal vier tatsächlichen Spieltagen über 19 Tage auf 27.0.1+2503222. [Maschinenlesbare Zählung](../../data/pa-reach-001/summary.json)

| Ziel | Bereits an Baseline | Erstmals später beobachtet | Letzter Tag vor Horizont, Ziel offen | Geburtstag erreicht/überschritten, kein Treffer beobachtet, Verlauf lückenhaft |
|---|---:|---:|---:|---:|
| Exakt volle PA | 432 | 9 | 59.035 | 254 |
| Mindestens 95 Prozent | 3.764 | 35 | 55.739 | 192 |
| Mindestens PA−2 | 1.626 | 19 | 57.848 | 237 |

Die neun späteren Treffer sind echte positive Zukunftsbeobachtungen. Der Nenner einer individuellen Wahrscheinlichkeit bis 28 lässt sich aus diesen 19 Tagen nicht bestimmen. Weder alle offenen Fälle noch die 254 nur punktuell beobachteten Grenzfälle bilden gesicherte negative Beispiele. Die Zeit zwischen erstem und letztem positiven Readback begrenzt die Genauigkeit der Ereigniszeit. [Private Endpunktableitung](../../research/pa-reach-001/analysis/player_endpoints.py)

| Prüfgröße | Ergebnis |
|---|---|
| Versiegelte unabhängige Testkarrieren, gefittete Prognosemodelle | 0, 0 |
| Brier Score, Log Loss, Intercept, Slope | null |
| Kalibrierdiagramm und Gruppenfehler nach Alter, PA, Position und Stufe | Keine Vorhersage-/Outcome-Paare im unabhängigen Test |
| Erwartete Peak-CA, Peak-Intervall, erwarteter Peak-Meta | null |
| Status | `INSUFFICIENT_LONGITUDINAL_EVIDENCE`, `NOT_OUTCOME_VALIDATED` |

Der Zubieta-Bestand wird nach Build und Messqualität separat geführt. Die Herkunftsverwandtschaft mit TRAIN-005 wird im Längsschnittaudit geprüft. Seine bereits explorativ eingesehenen Spieler ergeben keinen rückwirkend unberührten Holdout. [Zubieta-Längsschnitt](LONGITUDINAL_ANALYSIS.md) · [Modell- und Freigabeplan](MODEL_DESIGN.md)

Im bestätigten Zubieta-Fenster auf 27.1.0+2505117 (58 Tage) umfassen die 60.635 Baseline-Feldspieler unter 28 für den exakten Endpunkt 434 bereits erreichte Ziele, 37 neu beobachtete Treffer, 59.432 rechtszensierte Personen und 732 Fälle ohne belegten Treffer bis zum im Fenster liegenden Geburtstag bei lückenhafter Abdeckung. Bei der 95-Prozent-Schwelle wurden 154 neue Treffer beobachtet, bei PA−2 waren es 86. Die zusätzliche Namensprüfung, der geforderte Endpunkt-Readback und das Positionskriterium der Regressionsstichprobe führen dort zu einer anderen Grundgesamtheit (60.550 Paare). [Endpunktzählung](../../research/pa-reach-001/manifests/zubieta-58-days.json) · [Regressionspopulation](CORRELATION_REPORT.md)

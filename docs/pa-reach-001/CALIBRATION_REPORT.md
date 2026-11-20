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

Der Nachweis des gespeicherten Progression Factor auf 27.1.0+2505117 qualifiziert einen möglichen Prädiktor. Der Vergleich von Modellen mit und ohne Faktor benötigt dieselben vorab eingefrorenen Testkarrieren und ausreichend bis zum Zielhorizont verfolgte Spieler. [Direkte Messung](NAMED_PROGRESSION_READBACK.md)

### Wie gut lässt sich die CA einen Monat im Voraus fortschreiben?

Für 59.665 Feldspieler unter 28 am 30. März waren alle drei Messungen im selben Karrierestamm verfügbar. Zwei feste Rechenregeln verwenden ausschließlich die bis März beobachteten Werte. Die erste nimmt für April dieselbe CA wie im März an. Die zweite schreibt die Änderung vom 31. Januar bis 30. März um weitere 31 Tage linear fort (31/58 der bereits beobachteten Änderung, begrenzt auf CA 1–200). Für beide Regeln ist die tatsächlich gemessene CA am 30. April die Referenz. Die schon explorativ untersuchte Kontrollfortschreibung liefert einen Vergleich dieser Regeln innerhalb einer Karriere.

| Märzgruppe | Dreifach beobachtet | Mittlerer absoluter Fehler bei konstanter CA | Mittlerer absoluter Fehler bei fortgeschriebenem Trend |
|---|---:|---:|---:|
| Alle | 59.665 | 0,292 CA | 0,295 CA |
| Unter 18, Lücke über 30 | 2.713 | 1,216 CA | 0,819 CA |
| 24–27, Lücke über 30 | 426 | 0,146 CA | 0,204 CA |

Über alle 59.665 Spieler sank der quadratisch gewichtete Fehler (RMSE) von 0,748 auf 0,646 CA. Bei jungen Spielern mit großer Lücke erfasste der Trend einen Teil der weiteren Entwicklung. In dieser Gruppe beträgt der mittlere Unterschied der absoluten Fehler unter den 1.530 Spielern mit bestätigtem Ausgangsklub −0,409 CA (klubweise Jackknife, approximatives 95-%-Intervall −0,464 bis −0,354). Das Intervall beschreibt die Streuung über die 357 vertretenen Klubs dieser Teilgruppe. Die drei Beobachtungen schließen Spieler ohne Januarhistorie aus. Aussagen zu einem Jahr, anderen Karrieren und zur Kalibrierung der vollen PA bleiben offen. [Fehler je Regel und Gruppe](../../research/pa-reach-001/manifests/short-horizon-reference.json) · [Auswertung](../../research/pa-reach-001/analysis/short_horizon_reference.py)

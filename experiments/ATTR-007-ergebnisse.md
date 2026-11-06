# ATTR-007 – Ergebnisse zur Sprunghöhe einzelner Angriffspositionen

**7. November 2026 · Explorativ · FM27 27.0.0+2493426 · 200 vollständige Achtarmblöcke**

Der Shapley-Beitrag von **ST beträgt +0,103 xGD pro Match** (marginales 95-%-KI +0,042 bis +0,163, Holm-p = 0,0065). Für AMR und AML lagen die Beiträge bei +0,030 und −0,0004. Der direkte Abstand ST minus Flügelmittel beträgt +0,088 xGD (marginales 95-%-KI +0,016 bis +0,160, Holm-p = 0,104). Die Daten machen ST zum Kandidaten für eine unabhängige Prüfung des Positionsunterschieds. Die isolierte ST-Aufwertung schätzt +0,020 xGD mit einem Intervall von −0,105 bis +0,146.

## Lauf und native Validierung

Die [Vorregistrierung](ATTR-007-vorregistrierung.md) und der Analysecode wurden vor dem ersten Match in `9ceaf95` gepusht. Spielstartprotokoll, Engine, Adapter-Host, Fixture und Ressourcenfingerabdruck stimmten mit ATTR-006 überein. Die binären Hashes von Baseline und ALL waren jeweils mit ATTR-006 identisch. Der native Readback ordnete AMR, AML und ST den nullbasierten Kaderplätzen 8, 9 und 10 zu.

Alle 32 Prüfmatches wurden akzeptiert. Der binäre Vergleich und die 28 gepaarten nativen Readbacks zeigten genau die pro Arm deklarierten JumpingReach-Änderungen. Die Phasenkonfigurationen beider Teams stimmten über die Arme exakt überein. Kader, Rollen, Mannschaftsanweisungen, kontrollierte Startprofile und die übrigen Attribute erfüllten den nativen Eingabeaudit. Alle 16 Wiederholungspaare waren bei Endstand, Teamstatistik und Endtick identisch. Die getrennte Negativprobe endete mit Code 108. [Validierung](../data/attr-007/validation-summary.json)

Alle 1.600 Hauptmatches wurden im ersten Versuch akzeptiert. Jeder der 200 neuen, zu früheren Archiven disjunkten Seeds lief in allen acht Armen. Der Export prüfte die Beleg-Hashes erneut. [Manifest](../data/attr-007/manifest.json) · [Hauptmessungen](../data/attr-007/matches.jsonl)

## Isolierte Effekte und Shapley-Beiträge

Die isolierten Effekte vergleichen die jeweilige Einzelaufwertung mit Baseline. Die Shapley-Beiträge verteilen den gemeinsamen Eingriff über die gewichteten marginalen Beiträge in allen möglichen Aufwertungskombinationen. Die Schätzungen und Intervalle beruhen auf gepaarten Seed-Kontrasten. Beide Intervalle sind marginal. Die Holm-Entscheidung verwendet die Familie aus sieben primären Tests.

| Kontrast | Δ xGD | 95-%-t-KI | 95-%-Bootstrap-KI | SD | Holm-p |
|---|---:|---:|---:|---:|---:|
| AMR allein − Baseline | +0,006 | −0,136 bis +0,148 | −0,135 bis +0,148 | 1,019 | 1,000 |
| Shapley AMR | +0,030 | −0,040 bis +0,100 | −0,040 bis +0,100 | 0,505 | 1,000 |
| AML allein − Baseline | −0,017 | −0,148 bis +0,113 | −0,148 bis +0,114 | 0,935 | 1,000 |
| Shapley AML | −0,0004 | −0,075 bis +0,074 | −0,076 bis +0,075 | 0,537 | 1,000 |
| ST allein − Baseline | +0,020 | −0,105 bis +0,146 | −0,104 bis +0,145 | 0,901 | 1,000 |
| Shapley ST | +0,103 | +0,042 bis +0,163 | +0,044 bis +0,162 | 0,432 | 0,006 |
| Shapley ST − Mittel der Flügel | +0,088 | +0,016 bis +0,160 | +0,016 bis +0,160 | 0,517 | 0,104 |

Der Gesamteffekt ALL minus Baseline beträgt deskriptiv +0,132 xGD (95-%-t-KI −0,0006 bis +0,265). In ATTR-006 betrug die Schätzung für denselben gemeinsamen Eingriff +0,171. Die Shapley-Beiträge summieren sich in **jedem der 200 Seed-Blöcke exakt** zu ALL minus Baseline. Die rationale Prüfung bestätigte die Identität für alle Blöcke, der größte numerische Gleitkommarest betrug 4,44 × 10⁻¹⁶ xGD. Die Summe ist eine Eigenschaft der Zerlegung. Der Kontrast zum Flügelmittel testet gesondert, wie gut die Daten einen Positionsunterschied stützen.

## Faktorielle Haupt- und Interaktionseffekte

Die Haupteffekte mitteln den marginalen Positionsunterschied gleichgewichtet über die vier Kombinationen der beiden anderen Positionen. Bei Zweifachinteraktionen wird die Differenz der marginalen Effekte über beide Stufen des dritten Faktors gemittelt. Die Dreifachinteraktion misst die Veränderung dieser Differenz beim Einschalten des dritten Faktors.

| Kontrast | Δ xGD | 95-%-t-KI | 95-%-Bootstrap-KI | SD | Holm-p |
|---|---:|---:|---:|---:|---:|
| Haupteffekt AMR | +0,042 | −0,024 bis +0,109 | −0,025 bis +0,108 | 0,477 | 1,000 |
| Haupteffekt AML | +0,012 | −0,059 bis +0,082 | −0,059 bis +0,082 | 0,505 | 1,000 |
| Haupteffekt ST | +0,115 | +0,057 bis +0,172 | +0,057 bis +0,172 | 0,414 | <0,001 |
| AMR × AML | −0,065 | −0,195 bis +0,065 | −0,195 bis +0,064 | 0,933 | 1,000 |
| AMR × ST | +0,066 | −0,065 bis +0,197 | −0,063 bis +0,196 | 0,939 | 1,000 |
| AML × ST | +0,051 | −0,075 bis +0,177 | −0,073 bis +0,175 | 0,906 | 1,000 |
| AMR × AML × ST | −0,144 | −0,390 bis +0,102 | −0,386 bis +0,102 | 1,766 | 1,000 |

Der gemittelte ST-Haupteffekt erreichte die Holm-Schwelle in seiner Familie. Alle vier Interaktionsintervalle enthalten null und lassen relevante Abweichungen von Additivität zu. Die Kombination aus einem positiven gemittelten ST-Effekt und einer unsicheren isolierten ST-Schätzung erlaubt keine eindeutige Aussage darüber, wie sich ST in einem bestimmten Aufwertungskontext verhält.

Unter den 70 sekundären Tests erreichte der gemittelte ST-Haupteffekt auf xGA die Holm-Schwelle (−0,091 xGA pro Match, Holm-p = 0,043). Das ist ein explorativer Hinweis auf weniger gegnerisches xG über die vier ST-Vergleichskontexte. Alle Schätzungen für xGF, xGA, Tore, Gegentore und Punkte sind im [Effektarchiv](../data/attr-007/effects.json) dokumentiert.

## Fallzahlen und vorgeschlagene Folgestudie

Die Tabelle gibt vollständige neue Seed-Blöcke bei einem einzelnen zweiseitigen Test mit α = 0,05 an. Die erste Zahl nutzt die beobachtete gepaarte SD. Die zweite nutzt deren einseitige 95-%-Obergrenze unter Normalitätsannahme. Zielunterschiede und Power sind Szenarien für einen neuen Versuch. Die Ergebnisse für α = 0,05/7 stehen zusätzlich im Effektarchiv.

| Kontrast | 0,10 xGD bei 80 % | 0,10 xGD bei 90 % | 0,15 xGD bei 80 % | 0,15 xGD bei 90 % |
|---|---:|---:|---:|---:|
| AMR allein − Baseline | 817 / 971 | 1092 / 1299 | 364 / 433 | 487 / 578 |
| Shapley AMR | 202 / 240 | 270 / 320 | 91 / 108 | 121 / 144 |
| AML allein − Baseline | 689 / 819 | 922 / 1095 | 308 / 365 | 411 / 488 |
| Shapley AML | 229 / 272 | 305 / 363 | 103 / 122 | 137 / 163 |
| ST allein − Baseline | 640 / 761 | 856 / 1017 | 286 / 339 | 382 / 454 |
| Shapley ST | 149 / 176 | 198 / 235 | 67 / 80 | 89 / 106 |
| Shapley ST − Mittel der Flügel | 212 / 252 | 283 / 337 | 96 / 113 | 127 / 151 |
| Haupteffekt AMR | 181 / 214 | 241 / 286 | 82 / 97 | 109 / 129 |
| Haupteffekt AML | 203 / 240 | 270 / 321 | 91 / 108 | 122 / 144 |
| Haupteffekt ST | 137 / 163 | 183 / 217 | 62 / 74 | 83 / 98 |
| AMR × AML | 686 / 815 | 917 / 1090 | 306 / 364 | 409 / 486 |
| AMR × ST | 695 / 825 | 929 / 1104 | 310 / 368 | 414 / 492 |
| AML × ST | 646 / 768 | 864 / 1027 | 288 / 343 | 385 / 458 |
| AMR × AML × ST | 2450 / 2913 | 3279 / 3898 | 1090 / 1296 | 1459 / 1734 |

Als nächste Studie bietet sich ein unabhängiger Achtarmversuch mit dem **einzigen Primärkontrast Shapley(ST) minus Flügelmittel** an. Er prüft direkt den in ATTR-007 offenen Positionsunterschied. Bei einem Zielunterschied von 0,10 xGD und 90 % Power ergeben sich 283 Seeds, mit oberer SD-Grenze 337. Die Fallzahl und Entscheidungsregel werden im eigenen Analyseplan festgelegt. Ein Test der isolierten ST-Aufwertung beantwortet eine andere Frage und benötigt bei denselben Annahmen 856 bis 1.017 Paare. Aussagen über andere Spieler, Rollen oder Fixtures benötigen eigene Daten.

## Reproduktion

```sh
python -m pip install numpy==2.3.5 scipy==1.16.3
python analysis/analyse_attr007.py
```

Die eingefrorene Analyse reproduziert das Effektarchiv exakt. Die unabhängige Rechnung über alle sechs Positionsreihenfolgen und direkte faktorielle Differenzen bestätigte alle 84 Tests, Bootstrap-Intervalle und 224 Fallzahlminima. [Analysecode](../analysis/analyse_attr007.py) · [Datenbeschreibung](../data/attr-007/README.md)

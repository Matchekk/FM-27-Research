# Beobachtete Treffer der festen März-PA bis 30.06.2027

**45 von 61.613** Feldspielern unter 28 mit einem CA-Rückstand am 30.03.2027 wurden im Retentionszweig bis einschließlich 30.06. erstmals mit voller Ausgangs-PA beobachtet. Die ersten beobachteten Treffer verteilen sich auf 6 am 07.04., 19 am 30.04. und 20 am 30.06. Weitere 434 U28-Feldspieler lagen schon am Ausgangstag auf oder über der vollen Ausgangs-PA und gehören deshalb außerhalb dieser Risikokohorte. Alle Beobachtungen stammen aus einer Karrierewurzel auf FM27 27.1.0+2505117. [Aggregierte Daten und Quellhashes](../../research/pa-reach-001/manifests/retention-pa-hits-0630.json)

In jeder Zielspalte stehen nacheinander **schon an Baseline / erstmals später beobachtet / Folgebeobachtung fehlt / vor 28 zensiert / Geburtstagsabdeckung offen**. Die letzten drei Kategorien betreffen Spieler ohne beobachteten Treffer für die jeweilige Schwelle.

| Ausgangsgruppe | Spieler | Volle PA | PA−2 | Mindestens 95 % PA |
|---|---:|---:|---:|---:|
| Gesamt | 61.613 | 0 / 45 / 91 / 60.538 / 939 | 1.201 / 76 / 82 / 59.392 / 862 | 3.280 / 152 / 74 / 57.396 / 711 |
| U18 | 7.055 | 0 / 0 / 1 / 7.054 / 0 | 50 / 6 / 1 / 6.998 / 0 | 31 / 5 / 1 / 7.018 / 0 |
| 18–20 | 18.979 | 0 / 6 / 3 / 18.970 / 0 | 251 / 18 / 3 / 18.707 / 0 | 354 / 27 / 3 / 18.595 / 0 |
| 21–23 | 17.071 | 0 / 11 / 9 / 17.051 / 0 | 203 / 21 / 9 / 16.838 / 0 | 429 / 56 / 9 / 16.577 / 0 |
| 24–27 | 18.508 | 0 / 28 / 78 / 17.463 / 939 | 697 / 31 / 69 / 16.849 / 862 | 2.466 / 64 / 61 / 15.206 / 711 |
| Lücke 1–2 | 1.201 | 0 / 34 / 9 / 1.081 / 77 | 1.201 / 0 / 0 / 0 / 0 | 1.102 / 1 / 0 / 97 / 1 |
| Lücke 3–5 | 3.347 | 0 / 9 / 10 / 3.145 / 183 | 0 / 64 / 10 / 3.090 / 183 | 1.852 / 23 / 3 / 1.422 / 47 |
| Lücke 6–10 | 9.537 | 0 / 2 / 24 / 9.217 / 294 | 0 / 12 / 24 / 9.207 / 294 | 326 / 115 / 23 / 8.795 / 278 |
| Lücke 11–20 | 22.645 | 0 / 0 / 35 / 22.307 / 303 | 0 / 0 / 35 / 22.307 / 303 | 0 / 13 / 35 / 22.294 / 303 |
| Lücke 21–30 | 14.155 | 0 / 0 / 7 / 14.084 / 64 | 0 / 0 / 7 / 14.084 / 64 | 0 / 0 / 7 / 14.084 / 64 |
| Lücke >30 | 10.728 | 0 / 0 / 6 / 10.704 / 18 | 0 / 0 / 6 / 10.704 / 18 | 0 / 0 / 6 / 10.704 / 18 |

Die Identität folgt Datenbank-ID und Geburtsdatum. PA bleibt auf dem individuellen März-Wert fixiert. Die 95-%-Schwelle wird auf den nächsten ganzzahligen CA-Wert aufgerundet. Die ersten Treffer zählen bis einschließlich des 28. Geburtstags und nur an belegten Stichtagen. Ein Spieler ohne Folgebeobachtung bis zum Geburtstag bleibt fehlend. Wenn weitere Messungen vor dem Horizont vorliegen und die letzte Spielerbeobachtung davor endet, gilt der Verlauf als rechtszensiert. Für insgesamt 972 Spieler liegt eine spätere Messung ohne Messung am Geburtstag selbst vor, für 41 liegt eine Messung genau am Geburtstag vor. Auch dann bleibt die Abdeckung zwischen Stichtagen offen. Wann eine Schwelle zuerst überschritten wurde und ob zwischen Stichtagen ein kurzzeitiger Treffer vorkam, ist unbekannt. Das JSON enthält zusätzlich die gekreuzten Alters-/Lückenzellen und Datumshäufigkeiten. [Auswertung für beliebige bestätigte Folgestichtage](../../research/pa-reach-001/analysis/retention_pa_hits.py)

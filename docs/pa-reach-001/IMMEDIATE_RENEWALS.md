# Verändert sich der gespeicherte ProgressionFactor unmittelbar nach einer Verlängerung?

**Bei allen 28 Spielern mit einer unmittelbar gespeicherten Verlängerung blieb der Faktor gleich.** Beide Spielstände zeigen denselben 31. März 2027. Im ersten waren die 16 individuellen Jugendangebote bereits abgegeben. Danach folgten die einzeln delegierten Vertragsverhandlungen und die zweite Speicherung, ohne zwischenzeitliche Kalenderfortschreibung. Bei den 28 Spielern rückte das Vertragsende nach hinten und das gespeicherte Anfangsdatum wechselte auf den 31.03.2027. Ein weiterer fälliger Spieler lehnte laut Postfach ab. Die Zahl der wirksamen neuen Abschlüsse ist damit von der Zahl der angesprochenen Spieler unterscheidbar. [Inventar vor der Delegation](../../research/pa-reach-001/manifests/zubieta-contracts-retention-0331.json) · [Inventar danach](../../research/pa-reach-001/manifests/zubieta-contracts-retention-0331-renewals.json)

## Spieler und Messwerte

Die zwei Saves des Builds `27.1.0+2505117` enthielten jeweils 107.365 strukturell vollständige Spieler. Für alle passten eindeutige ID, Geburtstag und ein nichtleerer Hash des vollen Namens. Die 99 Mitglieder der drei vorab festgelegten Gruppen ließen sich zusätzlich an beiden Speicherzeitpunkten an die private Klub- und Vertragsliste anbinden. Bei fünf Personen unterschied sich der Anzeigename vom vollen Namen. Beide Namensfelder wurden an beiden Checkpoints aus demselben Spielerprofil bestätigt. Die übrigen 94 Namen stimmten direkt überein. Der zusätzliche Klubangehörige außerhalb dieser Gruppen bleibt separat.

Die Messung liest die gespeicherten CA-, PA- und Faktorwerte. Eine namentliche Engine-Abfrage bestätigte den Faktor auf diesem Build an zwölf Identitäten. Für dieses unmittelbare Paar liegen keine zwei separaten nativen Vollinventare vor. fmsave 0.14.1 meldet für den Build den dokumentierten Layout-Vorbehalt. [Benannte Gegenprobe](NAMED_PROGRESSION_READBACK.md) · [Quellprogramm und Ein-/Ausschlüsse](../../research/pa-reach-001/analysis/immediate_renewals.py)

| Vorabgruppe | Spieler | Späteres Vertragsende und neuer Beginn am 31.03. | Faktor 0→0 | 1→1 | 2→2 | 3→3 | 4→4 | 5→5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bis Juni fällig | 29 | 28 | 0 | 0 | 3 | 14 | 10 | 2 |
| Darin tatsächlich verlängert | 28 | 28 | 0 | 0 | 3 | 13 | 10 | 2 |
| Später fällige Ausgangsverträge | 54 | 0 | 0 | 2 | 3 | 19 | 18 | 12 |
| Neue Jugendkandidaten | 16 | 0 | 16 | 0 | 0 | 0 | 0 | 0 |
| Übriges Klubinventar | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 |
| Außerhalb des nachgewiesenen Klubinventars | 107.265 | – | 1.390 | 7.745 | 23.750 | 53.223 | 16.095 | 5.062 |

Jede der vollständigen **5×5-Matrizen** enthält auf sämtlichen Nebendiagonalfeldern null Beobachtungen. Auch die Übergänge aus oder nach dem numerischen Wert 0 außerhalb von 0→0 sowie fehlende Faktorwerte kamen nicht vor. Die CA-Differenz und die PA-Differenz betrugen in allen 107.365 Paaren null. Die Teilgruppe der 28 Verlängerten ist in der Zeile mit 29 Fälligen enthalten. Der Populationsvergleich außerhalb des Klubinventars erfasst die Ruhe im selben Speicherintervall. Er liefert keine unabhängige Karriere. [Alle Matrizen und Messwertdifferenzen](../../research/pa-reach-001/manifests/immediate-renewals.json)

Die 28 Veränderungen der Vertragseinträge zeigen, dass der gespeicherte Faktor dieser Spieler während der Folge von Handlungen keinen **sichtbaren Nettoübergang** machte. Eine interne Auslosung könnte denselben Wert liefern. Mehrere Übergänge zwischen den Speicherpunkten bleiben unbeobachtet.

## Sieben Kalendertage später im selben Retentionsarm

**Unmittelbar nach der Vertragsaktion hatten 0 von 28 verlängerten Spielern einen anderen gespeicherten Faktor. Am 7. April waren es 19 von 28.** Vierzehn hatten einen höheren, fünf einen niedrigeren Faktor. Unter den 52 länger gebundenen Spielern ohne zwischenzeitlich beobachtete Verlängerung behielten alle ihren Faktor.

| Gruppe vom 31.03. | Spieler | Netto-Wechsel bis 07.04. | Höhere Stufe 1–5 | Niedrigere Stufe 1–5 | Gleiche Stufe | Von 0 auf 1–5 |
|---|---:|---:|---:|---:|---:|---:|
| Bis Juni fällig | 29 | 19 | 14 | 5 | 10 | 0 |
| Davon mit verlängertem Vertragsende bereits am 31.03. | 28 | 19 | 14 | 5 | 9 | 0 |
| Davon am 31.03. ohne Verlängerung | 1 | 0 | 0 | 0 | 1 | 0 |
| Später fällige Ausgangsverträge | 54 | 1 | 1 | 0 | 53 | 0 |
| Davon im Wochenverlauf zusätzlich verlängert | 2 | 1 | 1 | 0 | 1 | 0 |
| Davon ohne beobachtete Verlängerung | 52 | 0 | 0 | 0 | 52 | 0 |
| Neue Jugendkandidaten | 16 | 16 | 0 | 0 | 0 | 16 |

**Die Spielstände datieren unterschiedliche Phasen der Verlängerung.** Bei allen 28 fälligen Spielern zeigte der erste Stand nach der Delegation als Beginn den 31.03. Im aktiven Vertrag vom 07.04. war das verlängerte Ende weiterhin identisch. Als Beginn stand dort der 03.04. bei einem, der 04.04. bei 14 und der 05.04. bei 13 Spielern. Bei den zwei zusätzlich verlängerten Spielern der länger gebundenen Gruppe waren die aktiven Beginndaten der 04. und der 05.04. Einer wechselte von Stufe 3 auf 4, der andere blieb auf 5. Alle 16 Jugendkandidaten hatten bis zum 07.04. einen eigenen Vertrag desselben Vereins mit ausgelesenem Beginn am 02.04. (2) oder 03.04. (14). Ihre Endfaktoren verteilten sich auf 3 (2), 4 (8) und 5 (6).

Alle 99 Spieler wurden im Ausgangs- und Folgestand über ID, Geburtstag und Namenshash verknüpft. Die Klublisten bestätigen Identität und Anzeigenamen. Der 07.04. ist unabhängig abgesichert: Das native Inventar stimmte bei allen 99 hinsichtlich CA und PA mit der Datei überein, ein getrennter Scout-Scan bei allen 99 hinsichtlich des Vertragsendes. Für den 31.03. gibt es kein natives CA/PA-Vollinventar. Für alle 83 Altspieler stimmt das am **30.03.** nativ gemessene Wertepaar mit dem gespeicherten Wertepaar vom 31.03. überein. Bei den 16 Jugendkandidaten bestätigten benannte Engine-Abfragen an beiden Stichtagen die Faktoren. Die CA- und PA-Werte des ersten Jugendmesspunkts stammen aus der Datei. Für die Altspieler weist die Tabelle gespeicherte Faktoren aus. [Messprogramm](../../research/pa-reach-001/analysis/renewals_week.py) · [Sämtliche Übergänge, CA-/PA-Differenzen und Vertragsdaten als Aggregate](../../research/pa-reach-001/manifests/week-after-renewals.json) · [Benannter Faktorverlauf des Jugendjahrgangs](../../research/pa-reach-001/manifests/zubieta-named-youth16-7-days.json)

Der Wochenvergleich erfasst mehrere verarbeitete Tage, Vertragsannahmen und weitere Spielereignisse einer Karriere. Für die erwachsenen Spieler konzentrierten sich die sichtbaren Übergänge auf die Gruppe mit verlängertem Vertrag. Der Zeitpunkt jedes Faktorwechsels innerhalb der sieben Tage, mögliche gleichwertige Neuauslosungen und andere zeitgleiche Einflüsse bleiben offen. Die Häufigkeiten sind beobachtete Gruppenverläufe. Eine individuelle Neuwurf- oder PA-Erreichungswahrscheinlichkeit lässt sich daraus nicht ableiten.

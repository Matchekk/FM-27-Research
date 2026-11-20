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

Die 28 Veränderungen der Vertragseinträge zeigen, dass der gespeicherte Faktor dieser Spieler während der Folge von Handlungen keinen **sichtbaren Nettoübergang** machte. Eine interne Auslosung könnte denselben Wert liefern, mehrere Übergänge zwischen den Speicherpunkten sind unbeobachtet, und die Engine kann Ereignisse bei einer späteren Tagesverarbeitung auswerten. Die Studie identifiziert weder den internen Ausführungszeitpunkt noch eine Neuwurfwahrscheinlichkeit. Es gibt eine Karriere, einen Spieltag und ein gemeinsam durchlaufenes Aktionsintervall. Für Aussagen über einen späteren Kalendertag muss derselbe Spieler erneut anhand seiner Identität gemessen werden.

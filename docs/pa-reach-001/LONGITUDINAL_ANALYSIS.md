# Zubieta Dynasty · 58 Tage gemessene Karriereentwicklung

**94.585 Spieler lassen sich auf FM27 27.1.0+2505117 am 31. Januar und 30. März 2027 eindeutig verbinden.** An beiden Tagen stimmen gespeicherte und separat im Spiel gelesene CA und PA bei derselben Datenbank-ID und demselben Geburtsdatum überein. Das Zeitfenster stammt aus zwei tatsächlich vorhandenen Karriereständen. Das Öffnen einer Kopie und ein erneutes Auslesen zählen nicht als simulierte Kalenderzeit. Die Bilanz der neuen Fortschreibung steht im [Bridge-Bericht](NATIVE_BRIDGE_VALIDATION.md).

## Quellen und Abgleich

| Quelle | Spieltag | Schreibbuild bzw. Scanversion | Als Save-Zeilen lesbar | CA/PA mit nativem Spielreferenzwert abgeglichen |
|---|---|---|---:|---:|
| Historische Zubieta-Kopie 03 | 22.10.2026 | 27.0.1+2494687 | 114.172 | Kein zeitgleicher nativer Abgleich dieser historischen Version |
| Historische Zubieta-Kopie 02 | 31.01.2027 | 27.1.0+2505117 | 113.581 | 94.708 |
| Scout-Vollscan | 17.03.2027 laut Exportkopf | FM27 27.1, Scanner 1.7.3 | 111.652 Scanprofile | Kein separater Save am gleichen Tag |
| Eingefrorene Zubieta-Baseline | 30.03.2027 | 27.1.0+2505117 | 107.231 | 97.258 |

Alle drei Save-Kopien enthalten dieselbe auslesbare menschliche Manager-Staff-ID und Klub-ID. Alle Zweige haben einen gemeinsamen Forschungsursprung. Auch TRAIN-005 teilt diese beiden Kennungen. Sämtliche 6.424 unter 18-jährigen TRAIN-005-Ausgangsspieler im hohen ID-Bereich ab zwei Milliarden fanden sich in der Zubieta-Januarkopie mit gleichem Geburtsdatum und identischer numerischer PA. Hohe IDs belegen für sich keine Neugenerierung. TRAIN-005 eignet sich damit nicht als unabhängiger Zubieta-Holdout. Der ältere Oktober-Schreibbuild bleibt separat. [Save- und Wiederholungsbeleg](../../research/pa-reach-001/manifests/zubieta-readback.json) · [TRAIN-005](../../experiments/TRAIN-005-INGAME.md)

Für die Januar- und Märzmessung wurde fmsave 0.14.1 auf den byteidentischen Kopien verwendet. Das Paket warnt auf beiden Builds vor Layoutübernahme. Ein Anker aus dem schließenden Personenheader, eindeutige Datenbank-ID, vollständiges Geburtsdatum und gültige CA/PA sind Pflichtwerte. Nur Lesepaare, deren beide Ability-Werte dem eigenen nativen Referenzinventar entsprechen, gehen in die Hauptauswertung ein. Am 31.01. enthält das Inventar 94.776 Zeilen. Davon liegen 3 IDs außerhalb des Save-Abgleichs und 65 Geburtsdaten fehlen oder weichen ab. Am 30.03. sind es 97.555 Zeilen, davon 8 und 289. Nach dem Identitätsabgleich stimmen alle geprüften CA-/PA-Paare. Der Datensatz ist eine selektierte Lesekohorte. 123 Januar-Identitäten fehlen am Endtag, 2.673 bestätigte Endidentitäten erscheinen erstmals. Zwei vollständige Lesedurchläufe auf getrennten privaten Datenbanken ergaben keine Differenz. [Quellhashes](../../research/pa-reach-001/manifests/zubieta-native-input.json) · [Zählung und Ausschlüsse](../../research/pa-reach-001/manifests/zubieta-58-days.json)

### Welche Attribute an beiden Spieltagen unabhängig lesbar waren

Ein neuer Vollscan bei unverändertem FM-Prozess und kontrolliertem Spielstand meldete intern **20.03.2027**. Unmittelbar davor und danach las die Game-Thread-Bridge **30.03.2027**, denselben Pfad und ruhenden Spielzustand. Die Datierung dieses Scans stützt sich auf die beiden unabhängigen Spieluhrmessungen. Von 108.233 Scanprofilen passen 97.241 über eindeutige UID, komplettes Geburtsdatum, CA und PA zur bereits bestätigten Märzreferenz. Unter den 52 Attributen auf der 1–20-Skala und acht Persönlichkeitswerten stimmen 5.783.678 gültige Feldpaare überein. 50.782 Vergleiche enthalten einen fehlenden oder außerhalb der Anzeigeskala liegenden Wert. Kein gültiges numerisches Paar weicht ab. Professionalität, Ehrgeiz und Zielstrebigkeit stimmen jeweils für alle 97.241 überein. Am ebenfalls von der Bridge datierten 31.01. bestätigt derselbe Weg 94.706 Profile. Professionalität, Ehrgeiz und Zielstrebigkeit stimmen dort bei allen 94.706 Profilen überein. Über alle 60 Felder sind 5.632.313 Werte gleich, 50.047 fehlen oder liegen außerhalb der Skala, und kein gültiger Wert weicht ab. Der Scannerkopf meldet für diesen Stand den 30.01. Der Nachweis betrifft auslesbare gerundete Attribute und Persönlichkeit auf diesen Spieltagen. Es gibt keine direkte inhaltliche Abnahme des Stufenbytes. [Januarabgleich](../../research/pa-reach-001/manifests/zubieta-january-scout-fields.json) · [Märzabgleich](../../research/pa-reach-001/manifests/zubieta-scout-fields.json)

### Was der zusätzliche Vollscan belegt

Der historische Vollscan mit Exportdatum 17.03. enthält den Spieldatum-Ursprung „memory“. Sein Managername und Klub stimmen mit der Wurzelkopie überein. Bei **94.583** beidseitig abgeglichenen Spielern passen auch im zusätzlichen Scan die UID und das vollständige Geburtsdatum. Alle drei PA-Werte stimmen in dieser Teilmenge überein. Die im historischen Export gespeicherte CA unterscheidet sich bei 29.575 Spielern vom Januarwert und bei 9.423 vom späteren Märzwert. Diese Anzahlen beschreiben Unterschiede zwischen Messpunkten und schließen Rückgänge ein. Die Buildangabe des Scans endet bei 27.1. Der oben nachgewiesene Kalenderfehler desselben Scannertyps lässt auch für das historische Exportdatum eine Abweichung zu. Sein genauer Spieltag bleibt offen. Die gepaarte Hauptauswertung verwendet die beiden exakt versionsgebundenen Save-/Inventarpaare. [Scan-Provenienz](../../research/pa-reach-001/manifests/zubieta-readback.json)

Die private Managerhistorie enthält 115.975 UID-Schlüssel und sechs Daten vom 02.01. bis 17.03.2027. Für den 17.03. stimmen alle 5.927 expliziten CA-/PA-Deltapunkte mit dem Vollscan überein. Für frühere historische Punkte fehlen individuell gespeichertes Geburtsdatum, exakter Schreibbuild und eindeutige Zweigzuordnung. Ein aus alter CA fortgeschriebener fehlender Deltapunkt kann bei einem fehlenden Spieler ein nicht beobachtetes Plateau vortäuschen. Diese Historie erhöht die Stichprobe der Hauptauswertung nicht. [Maschinenbeleg](../../research/pa-reach-001/manifests/zubieta-readback.json)

## Beobachtete Stufen- und CA-Verläufe

| Byte an CA+7 | 31.01. | 30.03. |
|---:|---:|---:|
| 0 | 529 | 1.273 |
| 1 | 6.687 | 6.868 |
| 2 | 20.362 | 20.851 |
| 3 | 47.297 | 48.029 |
| 4 | 15.086 | 15.406 |
| 5 | 4.747 | 4.831 |

Bei **2.382** gepaarten Spielern änderte sich der Bytewert. Darunter sind 527 Übergänge von 0 zu 1–5. Bei 653 Spielern war der Endwert niedriger als zu Beginn, während die End-CA über der zum neuen Wert postulierten Grenze lag. Von **2.224** erstmals am Endtag beobachteten Unter-18-Jährigen hatten 1.272 das Byte 0. Der Entstehungstag eines einzelnen Newgens ist damit nicht belegt. Null bleibt `NOT_ROLLED_OR_UNVERIFIED`. Das Feld ist auf dem Zielbuild lokalisierbar, eine explizite native Stufenreferenz fehlt. [Übergangsmatrix](../../research/pa-reach-001/manifests/zubieta-58-days.json)

Für Unter-28-Feldspieler mit an beiden Messpunkten unveränderten PA- und Bytewerten zeigt sich folgendes Muster. Mehr als zehn CA-Punkte unter der postulierten Grenze beträgt die mittlere Änderung **+1,382 CA** (n=15.844), innerhalb von ±2 Punkten **+0,041** (n=12.560) und mehr als zwei Punkte darüber **−0,012** (n=17.990). Auch nahe der Grenze gibt es 658 positive Deltas. Die Analyse kann Alters- und Auswahlunterschiede sowie unbemerkte Monatsausnahmen zwischen den Messungen enthalten. [Vollständige Gruppen](../../research/pa-reach-001/manifests/zubieta-58-days.json) · [Adjustierte Auswertung](CORRELATION_REPORT.md)

Für Spieler mit Byte 1–5 an beiden Enden und beidseitig unabhängig abgeglichener Klubkennung änderte sich das Byte bei 17 von 32 Klubwechseln sowie 782 von 36.896 Spielern mit gleichbleibendem Klub. In 57.130 Intervallen fehlte mindestens eine bestätigte Klubkennung, davon 1.056 mit Bytewechsel. Beobachtet wurden Kennungsänderungen zwischen zwei Stichtagen. Vertragsbeginn, Leihstatus, Managerwechsel, der Tag eines Ereignisses und Neuwürfe ohne sichtbare Wertänderung sind darüber nicht identifizierbar. [Ereignistabelle](../../research/pa-reach-001/manifests/zubieta-58-days.json)

## PA-Erreichung bis zum 28. Geburtstag

Unter 60.635 zu Beginn geeigneten Feldspielern waren 434 bereits am Ausgangsziel. Weitere 37 überschritten oder erreichten im bestätigten Fenster die ursprüngliche PA vor oder am 28. Geburtstag. 59.432 enden vor dem Horizont ohne beobachteten Treffer und sind rechtszensiert. Bei 732 liegt der Geburtstag im Beobachtungsfenster ohne bestätigten Treffer bis zu diesem Tag. Vereinzelte Messungen lassen einen zwischenzeitlichen Treffer offen. Für die 95-Prozent-Schwelle wurden 154 neue Treffer und 3.780 bereits zu Beginn erreichte Ziele beobachtet. Für PA−2 sind es 86 und 1.642. Für alle Endpunkte gelten feste Ausgangs-PA und dieselbe Kalendergrenze. Eine individuelle Zukunftswahrscheinlichkeit und ein kalibrierter Erwartungswert der Peak-CA lassen sich daraus noch nicht ableiten. [Endpunktbilanz](../../research/pa-reach-001/manifests/zubieta-58-days.json) · [Kalibrierungsstand](CALIBRATION_REPORT.md)

## Reproduzieren

Die private Erfassung konserviert je identifiziertem Spieler 52 Rohattributfelder, 15 Positionseignungen und acht Persönlichkeitswerte gemäß dem Feldvertrag des Readers. Für beide historischen Spieltage gibt es zusätzlich den unabhängigen Profilvergleich und für einen Teil der Spieler die Klubzuordnung. Einzelprofildaten bleiben privat. Der vom Märzstand abgezweigte Urlaubsmonat hat eine getrennte [prospektive Auswertung](PROSPECTIVE_CONTROL.md). Die SQLite-Tabelle `field_order` enthält die Reihenfolge der gespeicherten Felder. Die drei strukturellen Captures sind separat zugänglich, die doppelt abgeglichenen Beobachtungen liegen in der eigenen privaten Kerntabelle. [Feldkatalog](VARIABLE_ATLAS.md) · [Snapshot-Programm](../../research/pa-reach-001/analysis/zubieta_snapshot.py) · [Provenienzprüfung](../../research/pa-reach-001/analysis/zubieta_readback.py)

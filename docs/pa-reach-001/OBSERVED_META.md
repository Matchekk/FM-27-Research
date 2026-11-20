# Beobachtete Änderung des Feldspieler-Meta

**In Zubieta hatten 14.793 Feldspieler unter 28 Jahren am 30. März mehr CA als am 31. Januar. Bei 3.164 blieb der Meta-v2.1-Index gleich, bei 1.381 sank er.** Für diese Spieler sind an beiden Stichtagen die zehn benötigten Anzeigeattribute und dieselbe Einsatzposition abgeglichen. Gemessen wird die Änderung des aktuellen Feldspielerindex auf seiner Skala von 1 bis 20. Erwarteter Peak-Meta und zukünftige Attribute bleiben offene Prognoseziele. [FMSuperScout-Implementierung bei 977ecef](https://github.com/Matchekk/FMSuperScout/blob/977ecefe623a3d4081871a0f558ab12d9bce850d/app/outfield-meta27.js)

| Zeitraum und Auswahl | Spieler | Meta gestiegen | Gleich | Gesunken | Mittlere Änderung |
|---|---:|---:|---:|---:|---:|
| 31.01.–30.03.2027, alle gültigen Paare | 61.483 | 18.684 | 33.478 | 9.321 | +0,0232 |
| Davon mit CA-Gewinn | 14.793 | 10.248 | 3.164 | 1.381 | +0,1346 |
| 30.03.–30.04.2027, fortgeschriebener Kontrollmonat | 60.011 | 13.476 | 41.183 | 5.352 | +0,0169 |
| Davon mit CA-Gewinn | 11.619 | 6.865 | 3.831 | 923 | +0,0902 |

Gleichstand bedeutet identische Indexwerte bis auf eine numerische Rechentoleranz von 10⁻¹². Die Werte gehen vor einer etwaigen Darstellungskürzung im UI ein. Änderungen der sichtbaren Attribute sind selbst diskret. Kleine Änderungen der Rohattribute können deshalb beim angezeigten Index unauffällig bleiben. Der Index gewichtet ausgewählte Attribute je Einsatzposition. Die Gruppenmittel fassen ausschließlich Änderungen innerhalb desselben Spielers auf derselben Position zusammen. Die beiden Zeitfenster gehören zum selben Karriereuniversum. Eine zwischen Karrieren gültige Unsicherheit ist nicht schätzbar. [Zählungen nach Einsatzposition](../../research/pa-reach-001/manifests/observed-meta.json)

### Messweg

Das Auswertungsprogramm gleicht je Tag die Datenbank-ID, das Geburtsdatum, CA und PA eines nativen Vollscans mit der gehashten geladenen Save-Kopie ab. Alle zehn benötigten angezeigten Attribute müssen im Bereich 1–20 liegen und mit den auf die Anzeigeskala überführten Save-Werten übereinstimmen. Hinzu kommt die Prüfung der Einsatzpositionen anhand der Positionsratings des Saves und der Positionslisten des Scanners. Beide Tage eines Paares müssen denselben nichtleeren Namensprüfwert liefern. Das Originalmodul wählt die Position über `defaultPosition` und berechnet den aktuellen Index mit `score`. Der Modulinhalt wird vor dem Aufruf gegen das im Fork archivierte Git-Objekt geprüft. Der Algorithmus verwendet ausschließlich aktuelle Attribute. [Abgleich](../../research/pa-reach-001/analysis/observed_meta.py) · [Scoring-Aufruf](../../research/pa-reach-001/analysis/observed_meta.cjs)

### Qualifikation der Endpunkte

An allen drei Tagen bestätigen die vor und nach dem Scan abgefragten Spiel-Bridge-Daten dieselbe geladene Kopie, denselben Spieltag und einen ruhenden Zustand. Der eingebettete Save-Kalender stützt diese Zuordnung. Die Scout-Header melden abweichend 30.01., 20.03. und 28.04.2027. Keine Datumskorrektur wurde auf andere Scannerdateien übertragen.

| Kontrollierter Spieltag | Vollständig abgeglichene Eingaben, alle Alter/Positionen | Mindestens ein ungültiges Anzeigeattribut | Fehlender eindeutiger Identitäts-/CA-/PA-Abgleich |
|---|---:|---:|---:|
| 31.01.2027 | 106.397 | 7.181 | 3 |
| 30.03.2027 | 100.544 | 6.669 | 18 |
| 30.04.2027 | 106.135 | 7.704 | 20 |

Im ersten Intervall erfüllen 67.210 Feldspieler die Eingangskriterien. 5.691 davon fehlen beim qualifizierten Folgeabgleich, bei 36 wechselt die vom Fork gewählte Einsatzposition. Im Kontrollmonat sind es 63.001 Ausgangsspieler, davon fehlen 2.971 beim Folgeabgleich und bei 19 wechselt die Einsatzposition. Für alle verbleibenden Paare war der Originalscore berechenbar. Die CA-Wachstumsanalyse verwendet ein anderes Referenzinventar. Ihre Fallzahlen können deshalb abweichen. Das März–April-Aggregat wurde eigenständig und im Drei-Stichtage-Lauf reproduziert. [Vollständige Abrechnung und Hashes](../../research/pa-reach-001/manifests/observed-meta.json)

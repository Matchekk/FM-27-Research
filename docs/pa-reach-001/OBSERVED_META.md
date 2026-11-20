# Beobachtete Änderung des Feldspieler-Meta

**In Zubieta hatten 14.793 Feldspieler unter 28 Jahren am 30. März mehr CA als am 31. Januar. Bei 3.164 blieb der Meta-v2.1-Index gleich, bei 1.381 sank er.** Für diese Spieler sind an beiden Stichtagen die zehn benötigten Anzeigeattribute und dieselbe Einsatzposition abgeglichen. Gemessen wird die Änderung des aktuellen Feldspielerindex auf seiner Skala von 1 bis 20. Erwarteter Peak-Meta und zukünftige Attribute bleiben offene Prognoseziele. [FMSuperScout-Implementierung bei 977ecef](https://github.com/Matchekk/FMSuperScout/blob/977ecefe623a3d4081871a0f558ab12d9bce850d/app/outfield-meta27.js)

| Zeitraum und Auswahl | Spieler | Meta gestiegen | Gleich | Gesunken | Mittlere Änderung |
|---|---:|---:|---:|---:|---:|
| 31.01.–30.03.2027, alle gültigen Paare | 61.483 | 18.684 | 33.478 | 9.321 | +0,0232 |
| Davon mit CA-Gewinn | 14.793 | 10.248 | 3.164 | 1.381 | +0,1346 |
| 30.03.–30.04.2027, fortgeschriebener Kontrollmonat | 60.011 | 13.476 | 41.183 | 5.352 | +0,0169 |
| Davon mit CA-Gewinn | 11.619 | 6.865 | 3.831 | 923 | +0,0902 |
| 30.04.–30.06.2027, Retentionszweig | 69.268 | 20.727 | 41.656 | 6.885 | +0,0280 |
| Davon mit CA-Gewinn | 13.708 | 9.244 | 3.260 | 1.204 | +0,1241 |

Im 61-Tage-Fenster des Retentionszweigs stieg die CA der 15 auswertbaren Jugendfeldspieler im Mittel um 0,80. Der mittlere Meta-Index änderte sich um −0,0109. Alle Zweige stammen aus derselben Karriere. [Saisonstichtag, Jugendjahrgang und Reproduktion](RETENTION_META_SEASON1.md)

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

### Längere Verläufe im Retentionszweig

| Ausgangsgruppe bis 30.12.2027 | Tage | Gültige Paare | Mittlere ΔCA | Mittlere ΔMeta | Meta gestiegen / gleich / gesunken |
|---|---:|---:|---:|---:|---:|
| Feldspieler unter 28 am 30.03.2027 | 275 | 58.538 | +1,0149 | +0,0869 | 31.512 / 12.675 / 14.351 |
| Fester Jugendjahrgang ab 30.04.2027 | 244 | 15 | +7,4667 | +0,6090 | 14 / 1 / 0 |

Von 63.001 geeigneten März-Ausgangsprofilen fehlten im Dezember 4.049 bei der strukturellen Identitätsprüfung, und 323 hatten mindestens ein ungültiges Anzeigeattribut. Bei 91 weiteren Paaren wechselte die vom App-Modell gewählte Bewertungsposition. Bei den 22.983 auswertbaren Feldspielern mit CA-Gewinn stieg der Index im Mittel um 0,3376 Punkte und sank bei 1.918. Von den 16 gebundenen Jugendspielern fiel der Torwart außerhalb des Feldspielerindex. Die 15 Feldspieler haben keine fehlenden oder gewechselten Bewertungspositionen. Die identische Scoringfunktion reproduzierte auch die frühere Juni-Auswertung. [Dezember-Abrechnung](../../research/pa-reach-001/manifests/retention-meta-1230.json) · [Juni-Abrechnung](RETENTION_META_SEASON1.md)

Der gehashte Retentionssave und ruhende Kontextabfragen vor und nach dem Scan bestätigen den 30.12.2027. Der Scout-Header nennt den 18.12. Der CLI-Lauf verwendet dieselben März-/April-Baselines für die exakten Folgetage 30.03.2028 und 30.03.2029. Er benötigt je Stichtag Panel, bestätigten Snapshot-Tag, Scan und beide Kontextbelege sowie für den Zieltag den bestätigten Save-Hash. Die Ergebnisse zeigen beobachtete Indexdifferenzen zwischen festen Stichtagen. Das höchste tatsächlich erreichte Meta zwischen diesen Tagen und künftiger Peak-Meta bleiben unbekannt. [Wiederverwendbarer CLI-Lauf](../../research/pa-reach-001/analysis/retention_meta_long.py)

### Erster Jahresstichtag im Retentionszweig

| Ausgangsgruppe bis 30.03.2028 | Tage | Gültige Paare | Mittlere ΔCA | Mittlere ΔMeta | Meta gestiegen / gleich / gesunken |
|---|---:|---:|---:|---:|---:|
| Feldspieler unter 28 am 30.03.2027 | 366 | 56.346 | +1,5532 | +0,1250 | 33.153 / 9.187 / 14.006 |
| Fester Jugendjahrgang ab 30.04.2027 | 335 | 14 | +9,4286 | +0,6996 | 13 / 0 / 1 |

Von 63.001 geeigneten März-Ausgangsprofilen fehlten zum Jahresstichtag 6.157 im strukturellen Folgeabgleich, 377 hatten ungültige Anzeigeattribute und 121 eine andere App-Bewertungsposition. Bei 24.573 Spielern mit CA-Zuwachs stieg der Index im Mittel um 0,3899 Punkte. Unter ihnen sank er bei 2.106. Im festen Jugendjahrgang entfallen ein Torwart und ein Spieler mit geänderter Bewertungsposition. Der Scout-Header meldete den 22.03.2028. Die Save-Prüfsumme und die beidseitige Kontextklammer bestätigen den 30.03.2028. [Jahresabrechnung](../../research/pa-reach-001/manifests/retention-meta-20280330.json)

### Theoretisches PA-Meta bei exakt erreichter Ausgangs-PA

Unter **145** gepaarten Feldspielern, deren CA am 30.03.2028 exakt ihrer PA vom 30.03.2027 entsprach, lag das PA-Meta der Original-App im MAE um **0,0845 Meta-Punkte** näher am beobachteten Jahreswert als unverändertes Ausgangs-Meta. Unter den **129** auswertbaren Spielern, deren Jahrestag spätestens auf den 28. Geburtstag fiel, betrug die Verbesserung **0,0950 Punkte**. Die Werte sind bedingt auf das tatsächliche Erreichen der Ausgangs-PA genau am Folgestichtag. [Messabrechnung](../../research/pa-reach-001/manifests/potential-meta-at-pa-20280330.json)

| Auswahl | Vergleichsregel | Gültige Paare | MAE | Mittlerer Fehler Regel minus Messung |
|---|---|---:|---:|---:|
| Jahres-CA exakt auf Ausgangs-PA | Unverändertes Ausgangs-Meta | 145 | 0,30284 | −0,29666 |
| Jahres-CA exakt auf Ausgangs-PA | PA-Meta nach Original-App | 145 | 0,21830 | −0,19048 |
| Jahres-CA exakt auf Ausgangs-PA | PA-Meta mit bestätigtem Stichtag im App-Datumskontext | 145 | 0,21979 | −0,19197 |
| Zusätzlich bis einschließlich 28. Geburtstag | Unverändertes Ausgangs-Meta | 129 | 0,32371 | −0,31676 |
| Zusätzlich bis einschließlich 28. Geburtstag | PA-Meta nach Original-App | 129 | 0,22869 | −0,19742 |
| Zusätzlich bis einschließlich 28. Geburtstag | PA-Meta mit bestätigtem Stichtag im App-Datumskontext | 129 | 0,23036 | −0,19909 |

Ausgangspunkt waren 61.613 U28-Feldspieler mit CA unter PA. Bei 4.689 fehlte der verifizierte strukturelle und native Folgeabgleich. **158** lagen exakt am Jahresstichtag auf ihrer festen Ausgangs-PA, darunter 141 bis einschließlich des 28. Geburtstags. Zehn der 158 scheiterten an der Ausgangsprüfung, einer an der Folgeprüfung und zwei an der gleichermaßen erforderlichen App-Bewertungsposition. Die separat berichteten **153** vollen PA-Treffer beschreiben ein anderes Ereignis. Dort zählt jeder belegte Stichtag bis einschließlich 28. Geburtstag, an dem die Ausgangs-PA erreicht oder überschritten wurde. [Altersbegrenzte Verlaufszählung](../../research/pa-reach-001/manifests/retention-pa-hits-20280330.json)

Der Offline-Aufruf verwendet die unveränderten Funktionen `metaPaScore`, `projectAttrs` und `weightedMeta` des geprüften App-Blobs zusammen mit dem Originalscorer. Alle 47 sichtbaren Ausgangsattribute und die erforderlichen Folgeattribute wurden gegen die Save-Struktur geprüft. Die App verwendet bei der Attributprojektion das Alter aus der im Scan gelieferten Metadatenzeit. Im März-Ausgangsscan stammt das Headerdatum aus dem Speicher und lautet 20.03.2027. Der Save und die beidseitigen Kontextbelege datieren den tatsächlichen Scan auf 30.03.2027. Die Tabelle zeigt zusätzlich dieselbe App-Berechnung mit diesem belegten Datum als Referenz. Die Ursache der unterschiedlichen Datumswerte bleibt offen. [Gepinnter Original-App-Code](https://github.com/Matchekk/FMSuperScout/blob/977ecefe623a3d4081871a0f558ab12d9bce850d/app/app.js) · [Abgleich und Ausführung](../../research/pa-reach-001/analysis/potential_meta_compare.py)

Für den 30.03.2029 sind dieselben App-Regeln auf **51.381** verifizierten Ausgangsprofilen vom 30.03.2028 vorab eingefroren. Die Auswertung verwendet die identischen Kriterien für exakt erreichte Ausgangs-PA und gleiche App-Bewertungsposition. Die DOB-Teilgruppe mit Enddatum bis einschließlich 28. Geburtstag ist ebenfalls vorab festgelegt. Der Vergleich bleibt bedingt auf später beobachtete Treffer innerhalb derselben Karriere. [Versiegelte Basis](../../research/pa-reach-001/manifests/potential-meta-baseline-20280330.json)

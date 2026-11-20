# Das Byte bei CA+7 im Karriereverlauf

Auf **27.0.1+2503222** lässt sich das Feld in vier separat abgeglichenen Save-Zeitpunkten reproduzierbar lesen. Seine Veränderungen und die kurzfristigen CA-Verläufe stimmen in mehreren Punkten mit Caiogracos Beschreibung überein. Die anschließende Untersuchung des Zielbuilds **27.1.0+2505117** steht im [Zubieta-Readback](LONGITUDINAL_ANALYSIS.md). Der Produktstatus lautet `PROGRESSION_TIER_UNVERIFIED`.

### Identität vor Interpretation

fmsave 0.14.1 findet strukturgeprüfte Spielerrecords in `game_db` (Schema 4000). Relativ zum CA-Anfang liegen CA bei +0 als 16-Bit-Wert, PA bei +2 als vorzeichenbehafteter 16-Bit-Wert und der Kandidat bei +7 als einzelnes Byte. Punkt der Identitätsprüfung ist die Datenbank-ID aus dem schließenden Personenheader (`Player.unique_id`). Der öffnende Schlüssel (`Player.uid`) führte zum verworfenen Erstversuch mit 3/3/3/4 scheinbaren Treffern. Dessen Fehlzählungen sind erhalten. Erst eindeutige ID, Geburtsdatum und dieselben CA/PA-Werte im zeitgleichen, separat erhobenen Spielinventar qualifizieren eine Zeile. Den Kandidatenwert zieht der Reader erst danach. Die Referenz liefert keinen separat beschrifteten Progression Factor. [Readerquelle](https://github.com/rhiever/fmsave/blob/9dd60521042e9c5a33a14725da59023eb3ad8dfa/src/fmsave/readers/players.py) · [Fehlversuch, Wiederholung und Einzelabgleich](../../data/pa-reach-001/readback-audit.json)

| Spieltag | Byte 0 | 1 | 2 | 3 | 4 | 5 | Abgeglichen |
|---|---:|---:|---:|---:|---:|---:|---:|
| 16.01.2027 | 26 | 6.602 | 20.038 | 46.825 | 14.960 | 4.710 | 93.161 |
| 19.01.2027 | 211 | 6.621 | 20.120 | 46.926 | 14.993 | 4.712 | 93.583 |
| 23.01.2027 | 547 | 6.638 | 20.190 | 47.040 | 15.007 | 4.730 | 94.152 |
| 04.02.2027 | 476 | 6.743 | 20.508 | 47.557 | 15.097 | 4.768 | 95.149 |

Am ersten Tag beträgt der Median CA/PA bei den Bytes 1 bis 5 der Reihe nach 0,8240 / 0,8265 / 0,8400 / 0,8592 / 0,8595. Das sind Querschnittswerte aller akzeptierten Spieler, einschließlich bereits entwickelter Spieler. Auf allen vier Spieltagen liegt das Byte zwischen 0 und 5. Bei 773 erstmals nach Baseline erfassten Unter-18-Jährigen hatten 681 zunächst eine Null. Davon wurden 218 später mit 1–5 gesehen. Der erste Nachweis datiert weder die Erzeugung eines Newgens noch die Auslosung. Null erhält den Status `NOT_ROLLED_OR_UNVERIFIED`. [Verteilungen und Übergangsmatrix](../../data/pa-reach-001/summary.json)

### Zeitlicher Abgleich und mögliche Auslöser

Bei 964 von 93.113 identitätsgleichen Spielern differiert das Byte zwischen Tag 0 und Tag 19. In 322 Fällen mit einem niedrigeren Endwert lag die End-CA über der dazu postulierten neuen Grenze. Beim früher per UI identifizierten P001 blieb das Byte an allen vier Daten auf 4, während CA von 134 auf 135 stieg und PA bei 160 blieb. Ein zweiter vollständiger Lesevorgang lieferte identische Mess- und Abrechnungszeilen. [Verlauf P001 und Wiederholung](../../data/pa-reach-001/readback-audit.json)

| Klubkennung an benachbarten Spieltagen | Intervalle mit Byte 1–5 an beiden Enden | Byte verschieden |
|---|---:|---:|
| Beide Quellen bestätigen verschiedene Klubs | 48 | 29 |
| Beide Quellen bestätigen denselben Klub | 110.514 | 395 |
| Mindestens eine Klubkennung ungeklärt | 169.502 | 531 |

Die drei Intervalle dauern 3, 4 und 12 Tage. Personen können mehrfach beitragen. Unklare Vereinszuordnungen bleiben in einer eigenen Zeile. Endpunktunterschiede belegen Veränderungen innerhalb eines Intervalls. Transferart, Leihbeginn/-ende, Zeitpunkt, neuer Vertrag, Manager und mögliche gleichzeitige Ereignisse sind hier offen. Ein Neuwurf mit gleichem Ergebnis ist unsichtbar. Eine kausale Auslösewahrscheinlichkeit, der Anteil besserer Neuwürfe und die monatliche Ausnahme lassen sich so nicht bestimmen. [Zeitlich aufgeschlüsselte Zählung](../../data/pa-reach-001/summary.json)

Die Hypothese einer Entwicklungsgrenze erhält zusätzliche deskriptive Unterstützung durch den Zusammenhang zwischen Abstand und ΔCA. Eine vom Spiel benannte Stufenreferenz und kontrollierte Eingriffe fehlen für diese Auswertung. [Wachstumsanalyse](AGE_GROWTH_ANALYSIS.md)

### Replikation im gewünschten Build 27.1.0+2505117

Der Zubieta-Verlauf liefert denselben Feldanker an zwei nativ bestätigten Enden des 58-Tage-Fensters. Von 529 Ausgangswerten null sind 527 bei derselben verfolgbaren Person am zweiten Tag als 1–5 beobachtbar (41/139/231/92/24). Insgesamt wechseln 2.382 von 94.585 gepaarten Spielern das Byte. In 653 Fällen liegt die End-CA nach einem niedrigeren Endbyte oberhalb der dazu postulierten Grenze. Bei stabil beobachtetem Byte und stabiler PA gewannen Feldspieler unter 28 mit mehr als zehn Punkten Spielraum im Mittel 1,382 CA (n=15.844), innerhalb von zwei Punkten 0,041 (n=12.560). Mechanismus und harte Schwellen lassen sich aus diesem Befund allein nicht identifizieren. [Übergänge, Verteilungen und Abstandsgruppen](../../research/pa-reach-001/manifests/zubieta-58-days.json)

In der anschließend ausgeführten Monatsfortschreibung auf der privaten Kontrollkopie änderte sich das Byte bei 2.904 Spielern. Verwaltete Matches und die parallele Jugendaufnahme sind Bestandteile dieser Urlaubsphase. Der Nachweis betrifft einen identitätsgebundenen gespeicherten Zustand. Ein eigener nativ benannter Tier-Readback, isolierte Verletzungs-/Vertragsexperimente und direkt beobachtete monatliche Ausnahmefreigaben bleiben separate Evidenzstufen. [Kontrollmonat](../../research/pa-reach-001/manifests/zubieta-control-31-days.json)

# VALID-004 R1/R2 – reale einmalige Lesepässe

14.11.2026, nach veröffentlichtem Commit
`2172b76faaeb7db7f38e1dbf693b69e2757cc1fd`, erfolgreicher
[CI43626055825](https://github.com/Matchekk/FM-27-Research/actions/runs/43626055825),
[unabhängigem Quellenreview](CAREER-R1-REVIEW.md) und ausdrücklichem Director-Proceed.
Die beiden Verträge, Reader und Grenzen wurden zwischen Veröffentlichung und
Ausführung nicht geändert. Ergebnisse stammen ausschließlich aus der bereits
autorisierten, unveränderten privaten R0-Snapshotkopie.

| Ergebnis | R1 Runtime V10 | R2 offizielles fmsave0.12.4 |
|---|---:|---:|
| Beobachtete Probeplätze einschließlich Openwarnung | 4 | 5 |
| Fehlgeschlagene Probeplätze | 1: Training | 1: Taktiken |
| Danach unbegonnen | 7 | 6 |
| Gesamtlaufzeit in Sekunden | 13,985 | 14,453 |
| Peak Job Private Bytes | 1.177.456.640 | 1.181.728.768 |
| Harte Prozess-/Jobgrenze | 3GiB | 3GiB |
| Tatsächliche Decoderprozesse / Retries | 1 / 0 | 1 / 0 |

Beide Läufe blieben unter180s; Vor-/Nachhash des147.130.636-Byte-Snapshots
stimmen mit R0 überein. Jeweils `UnknownBuildWarning` beim Öffnen. Die
beendete Supervisoroperation mit Returncode0 bedeutet ausschließlich korrekte
Fehlerabrechnung: die jeweiligen fachlichen Probeprüfungen sind **gescheitert**.
Kein stilles Überspringen und keine Wiederholung. Insgesamt24 feste Probeplätze:
9beobachtet,2fehlgeschlagen,13unbegonnen. Null native Starts, Seeds oder
Kalenderfortschreibungen.

## Tatsächlich erschlossene Strukturen und Grenzen

Beide Reader liefern konsistent einen verwalteten Club,42.001 Clubrecords,
113.815 Spielerrecords und77 per Parser dem verwalteten Kader zugeordnete
Spielerrecords. Der abgeglichene Parserdatumclaim lautet16.01.2027; eine
Bindung an die aktive UI fehlt.13 vorab benannte vergleichbare Feldergruppen
stimmen überein,11 weitere sind nicht vergleichbar. Das sind dieselben
Snapshotbytes und verwandte Readerquellen, keine unabhängigen Replikate.
Native Feldsemantik und Roh-/FM-Anzeigekalibrierung bleiben ungeprüft.

R1 öffnete die Summary ohne Draftfallback:1Summaryaufruf,0Fallbackaufrufe.
Sein Trainingsreader verweigerte den nichtleeren Trainingsheader.
R2 las vier Team-Trainingsrecords mit61/30/30/34 datierten Wochen und
427/210/210/238 Tagen. Das ist zunächst ein technischer Parserfortschritt.
Die Wochen reichen teilweise über das gelesene Savedatum hinaus, etwa beim
ersten Team bis16.08.2027. Daher weder absolvierte Trainingseinheiten noch
individuelle Teilnahme aus den Rohcodes ableiten. Trainerzuordnung, Fokus,
Intensität und tatsächliche Teilnahme bleiben explizit fehlend.

R2 stoppte danach an einer unerwarteten Setpiece-Markerposition im
`tactics_man`-Parser. Selektionen, Standards, Staff, Verletzungen und Fixtures
wurden deshalb nicht mehr gelesen. Keine Aussage, dass diese Bereiche im Save
leer wären. Kein manuelles Entfernen des Parsergates.

## Nachprüfbare Veröffentlichung

[Anonyme R1-Abrechnung](../../data/night-001-career-r1/R1/coverage.json),
[R2-Abrechnung](../../data/night-001-career-r1/R2/coverage.json) und
[gleichbleibender Snapshotvergleich](../../data/night-001-career-r1/cross-reader.json)
enthalten alle24 Probeplätze, Warnungen, Checks, Ressourcen und Herkunft.
Savebytes, Namen, personenbezogene IDs, private Pfade und Rohwarntexte bleiben
privat. R0 und sämtliche historische Studien bleiben unverändert.

Der nächste Karrierearbeitsschritt ist ein begrenzter, separat registrierter
Parser-/UI-Abgleich für Training und Taktikstruktur. Zuerst die genaue Ursache
des Markerfehlers aus Quellcode und bereits erhaltenem Fehlerbeleg eingrenzen.
Keine Karriere-Replays, RNG-Replikate oder Trainingswirkungsstudie freigegeben.
[Unabhängiger Ergebnisreview](CAREER-RESULTS-REVIEW.md) rekonstruiert sämtliche
öffentlichen Probezeilen aus den privaten Ereignisledgers und bindet diese per
Hash. Keine Savebytes wurden für diesen Review erneut geöffnet.

## Zusätzlicher explorativer Offlineaudit der Trainingscodes

Die R2-Aggregate ergeben155 gespeicherte Wochen,1.085 Tage und3.255 Slots,
exakt drei je gespeichertem Tag. Der eingefrorene
[Readerenum](https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/models/training.py)
benennt elf nichtnegative FM27-Codes. Davon lassen sich2.011 Slots zuordnen
(61,78%);1.244 Slots (38,22%) besitzen in diesem Enum noch kein Label.
Auch vorhandene Labels sind hier nicht gegen unsere FM-UI kalibriert.

[Deterministischer Offlineaudit](../../analysis/audit_saved_training004.py) und
[vollständige Codeabdeckung](../../data/night-001-career-r1/training-code-coverage.json)
erhalten sämtliche unbenannten Codes. Drei eigene Softwaretests prüfen Missing,
falsche Nenner sowie die Trennung zukünftiger Slots und tatsächlich absolvierter
Exposition. Der Audit liest ausschließlich die bereits veröffentlichten
anonymen R2-Aggregate, keinen Save. Das ist eine zusätzliche technische
Abdeckungsanalyse und keine vorregistrierte Trainingswirkungsanalyse.

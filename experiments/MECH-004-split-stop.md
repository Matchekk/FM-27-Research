# MECH-004-SPLIT-R0: dauerhaft gestoppter Hauptlauf

15.11.2026 · **Technische Splitabnahme bestanden, wissenschaftliche Hauptserie
unvollständig und terminal geschlossen. Keine Haupt- oder Sekundäreffektschätzung.**
Dies ist ein dokumentierter Fehlschlag innerhalb der weiterlaufenden Mission
NIGHT-002, kein abgeschlossenes wissenschaftliches Ergebnis.

Die verbindlichen Endzustände stehen in
[`termination.json`](../data/night-002-split004/termination.json),
der fehlgeschlagenen [`main-summary.json`](../data/night-002-split004/main-summary.json),
der vollständigen [512er-Hauptjobabrechnung](../data/night-002-split004/main-job-accounting.jsonl)
und der [separaten Aufrufzeitrechnung](../data/night-002-split004/native-call-time.json).
Der unabhängige Review des terminalen Abschlusses steht bei Erstellung dieses
Berichts noch aus; erfolgreiche Abschluss-CI wird hier nicht vorweggenommen.

## Tatsächlich ausgeführt und offen geblieben

| Teil | Geplant | Tatsächlicher Endstand |
| --- | ---: | --- |
| Native Technik |32Vollmatches+1Negativprobe |32gültige Vollmatches,16exakte A/A-Paare,1erwartete Exit108-Abweisung; abgeschlossen und unabhängig geprüft |
| Wissenschaftlicher Hauptlauf |512Matches/64Seedblöcke |224akzeptierte Vollmatches,1fehlgeschlagener Job **vor** Native-Aufruf,287unbegonnene Jobs |
| Vollständige Hauptblöcke |32je bekanntem Gegner, je4Arme×2Seiten |28vollständige Achtjobblöcke ausschließlich `deep_block`;0vollständige `high_press`-Blöcke |
| Gesamte reservierte Versuchsplätze |545 |Alle33technischen und512Hauptplätze erhalten und abgerechnet; keine Ersatzplätze |

Die Blockangabe wurde direkt aus dem unveränderten Main-Dispatchledger nach
Kontext/Seed und vorhandenen Seiten-/Armkombinationen geprüft. Die224akzeptierten
Matches bilden28Blöcke mit je acht verschiedenen Kombinationen aus beiden
Seiten und vier Armen. Sie erfüllen **nicht** das vorregistrierte vollständige
Zwei-Kontext-Design. Es werden weder deren Fußballmittel noch vorläufige
Primär-/Sekundärtests, Konfidenzintervalle oder nachträgliche Ein-Kontext-Effekte
berechnet. Fehlende Jobs werden nicht als Null, Niederlage oder zufällige
wissenschaftliche Missing Values behandelt.

## Fehlerursache und Verantwortung

Die terminale Zulassungsabwehr meldete **`Mission artifact path escaped`**.
Zu diesem Zeitpunkt hatte der Director während der laufenden Hauptphase
bereits abgeschlossene private Jobbelege verlustfrei in ein ZIP-Archiv
kompaktieren und die verifizierten Originaldateien entfernen lassen.
Diese zusätzliche Speicherintervention war ein Fehler der Versuchsleitung:
Der aktive Artefaktscan löste Pfade erneut mit `Path.resolve()` auf, während
dieselben Pfade durch die Kompaktierung verschwinden konnten. Die gleichzeitigen
Operationen waren nicht gemeinsam gegen diesen Zustandswechsel abgesichert.

Die Guardmeldung beweist **keinen tatsächlich außerhalb des Missionsbaums
liegenden Dateiinhalt oder Pfadzugriff**. Dokumentiert ist eine durch die
Direktor-Speicherintervention ausgelöste Zulassungsabwehr; eine echte
Pfadflucht wurde nicht nachgewiesen. Der Fehler war kein zufälliger
Matchausfall, kein Schärfe-Readbackmismatch und kein negativer Fußballbefund.

Der einmal als fehlgeschlagen verbuchte Hauptjob besitzt
`native_invocation_started=false`; auch die auslösende weitere Admission
erreichte keinen Native-Aufruf. Der Scheduler stoppte, statt weitere Seeds
oder Ersatzjobs zuzulassen. Der bestehende Vertrag wird nach diesem Fehler
nicht gelockert, auf einen anderen Namen übertragen oder fortgesetzt.

## Rohbelege, Bereinigung und unveränderte Abrechnung

Der einzige kompaktierte Batch enthielt128abgeschlossene Jobs mit je sechs
Belegdateien und zwei Dispatchmarkern, insgesamt **1024Archiveinträge**.
Nach Ende der nativen Phase wurden alle ursprünglichen Pfade bytehashgeprüft
wiederhergestellt; Archivhash/CRC und Journal bleiben privat erhalten.
Es sind keine Rohbelege verloren. Budgets, Eingaben, Quellfreeze, Ledger und
Konkurrenzprotokoll wurden durch die Kompaktierung nicht umgeschrieben.

Die terminale Abrechnung dokumentiert **257tatsächliche Native-Aufrufe**:
33technische Calls einschließlich Negativprobe und224Maincalls. Für alle257
liegen bestätigte Kernelbereinigungen mit0aktiven Prozessen vor. Keine
Pendingmarker, keine aktive globale NativeLease und keine ungelösten
gestarteten Calls verbleiben. Der fehlgeschlagene prä-native Job zählt
keinen zusätzlichen Engine-Aufruf.

| Zeitgröße | Unverändert belasteter Endstand |
| --- | ---: |
| Eigene beaufsichtigte Studien-Childzeit |528,8133745s/900s; ursprüngliches Budget bleibt `halted=true` |
| Globale beaufsichtigte NIGHT-002-Phasenzeit |589,7353507s/3600s im originalen Haltsnapshot |
| Summe der einzelnen technischen Native-Aufrufzeiten |110,736s/33Calls |
| Summe der einzelnen Main-Aufrufzeiten |727,328s/224Calls |
| Summe aller tatsächlichen Native-Aufrufzeiten |838,064s/257Calls |

Parallele Callzeiten und inklusive ganze beaufsichtigte Phasen sind verschiedene
Messgrößen und werden getrennt erhalten. Keine Zeit wird zurückerstattet;
alle545reservierten Plätze sowie64Main- und4Technikseeds bleiben reserviert.
`main-summary.json` bleibt ausdrücklich `passed=false`, `complete=false`,
`budget_reconciled=false`, `scientific_analysis_allowed=false`. Der
terminale Abschlussbericht ergänzt die vollständige Fehler-/Prozessabrechnung,
ohne diese fehlgeschlagene Hauptphase als erfolgreich umzudeklarieren.

## Was technisch bestehen bleibt und wissenschaftlich offen ist

Die vor dem Hauptlauf veröffentlichte
[TECH32+1-Abnahme](../docs/night-002/SPLIT004-TECHNICAL-REVIEW.md) bleibt gültige
Evidenz für ihren eigenen geprüften Kontext: Beide C90/C7A-Offdiagonalen
überstehen Originalvorbereitung und ersten tatsächlichen Fortschritt getrennt.
Das beobachtete Startcachebyte8A unterscheidet die C90-Stufen70/100 und änderte
sich bei isolierter C7A-Änderung dort nicht. Keeper/Bank/Gegner und die
festgelegten Anfangskontrollen blieben erhalten.

Dieser technische Zusammenhang beweist weder Wirkungslosigkeit von C7A noch
einen Fußballwirkungsvorteil von C90, keinen einzelnen Engine-Consumer und
keine FM-UI-Prozentskala. Der vorregistrierte Attributionskontrast, seine
praktische Größe und sämtliche Leistungs-/Punkte-/Torfragen bleiben nach dem
Hauptstopp **unbeantwortet**. Keine Änderung des Meta-Scores v0.1 oder einer
Karriere-/Trainingsentscheidung wird daraus abgeleitet.

## Historische Freigaben und weitere Mission

Die tatsächlich ausgeführte erste Studienepoche bleibt über folgende
unveränderte Gitstände rekonstruierbar:

- Vorregistrierung und Codefreeze:
  [`0e535dc`](https://github.com/Matchekk/FM-27-Research/commit/0e535dcd39fd00b1221334a675ec25c7fc2afd14).
- Registrierungs-/Verifierbindung:
  [`b53c56e`](https://github.com/Matchekk/FM-27-Research/commit/b53c56e07f58b6756fbd15f110ec2a71e4475a4e).
- Unabhängige technische Freigabe:
  [`5ea00c8`](https://github.com/Matchekk/FM-27-Research/commit/5ea00c8b9fcc234a39258839ad9313fd399e9504).

Analyse, Eingriffe und Budgets dieser Epoche werden nicht nachträglich
umgeschrieben. Der terminale MECH-004-Vertrag erlaubt keine Fortsetzung,
keine Wiederholung, keine Ersatzseeds und kein Umbenennen zur Umgehung des Stopps.

NIGHT-002 darf an einer **anderen unabhängigen Frage**, insbesondere dem
separat geplanten TACT-003-Paketvergleich, weiterarbeiten. Dafür sind ein neuer
unabhängiger Review, Veröffentlichung und erfolgreiche CI der administrativen
Fortführungsregeln sowie alle eigenen wissenschaftlichen/native Gates nötig.
Ein neuer Controller für diese unabhängige Arbeit muss die bisherigen
589,7353507beaufsichtigten Phasensekunden,838,064gemessenen Callsekunden,
Reservationen, Seeds und Fehlerhistorie übernehmen. Die alten Haltsnapshots
bleiben erhalten; das ist weder Budgetreset noch Reaktivierung von MECH-004.

Dieser Abschnitt dokumentiert einen überprüfbaren terminalen Zwischenstand.
Der konsolidierte Missionsbericht bleibt
[`docs/night-002/OVERNIGHT_REPORT.md`](../docs/night-002/OVERNIGHT_REPORT.md).

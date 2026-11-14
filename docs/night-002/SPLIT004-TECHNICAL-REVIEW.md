# MECH-004-SPLIT-R0 – unabhängige native Technikabnahme

14.11.2026 · Research Agent, nicht Autor des Studienrunners, Compilers oder
der Analyse. **TECH32+1 bestanden; der vorregistrierte512Match-Hauptlauf ist
technisch akzeptiert, nach Veröffentlichung dieses Reviews/Releasegates und
erfolgreicher CI des exakten Freigabecommits.** Noch keine wissenschaftliche
Wirkungsschätzung oder Karriere-/UI-/Consumerfreigabe.

## Tatsächlich geprüfte neue Evidenz

Geprüft wurden die [32 öffentlichen Technikmessungen](../../data/night-002-split004/technical.jsonl),
[33er-Abrechnung](../../data/night-002-split004/technical-job-accounting.jsonl),
[Summary](../../data/night-002-split004/technical-summary.json),
[Budget](../../data/night-002-split004/technical-budget.json), der registrierte
Vertrag und **alle privaten Originalbelege** dieser neuen Phase. Der vorherige
[Inputreview](SPLIT004-INPUT-REVIEW.md) wird nicht als nativer Nachweis behandelt.

Der veröffentlichte Read-only-Verifier wurde im Modus `private-technical`
ausgeführt: öffentliche Zeilen und private Originale stimmen überein,
32Matches/16A/A/1Negativprobe vollständig. Seine Wiederverwendung des
niedrigstufigen Inputaudits ist ausdrücklich keine unabhängige Neuimplementierung
dieses Audits. Zusätzlich hat der Reviewer deshalb eigene direkte Schleifen
über die Originalsnapshots und Binär-/Inputdumpbytes ausgeführt.

In32Originaldumps stimmen **101.568 native Attributwerte** direkt mit den
Kind1-Werten der jeweiligen gehashten Eingabebinärdatei überein. Der bestehende
niedrigstufige Audit prüft zusätzlich proMatch1058Profilfelder,44Phasenzellen
und748PI-Gruppen. Originale natürliche Abschlüsse, tatsächliche Seed-, Actor-,
Setup- und Enginebindungen sind vollständig vorhanden. Kein unbekannter
Build/Host, kein Mismatch, keine Ergebnisexklusion oder Nullimputation.

## Die beiden Rohfelder bleiben getrennt erhalten

Die eigenen Prüfungen bestimmen die zehn Startfeldspieler aus den absoluten
Lineuprecords, anstatt eine angenommene Zielreihenfolge zu verwenden.
Alle32Matches liefern `prepared`, `first_advance`, `finished` in dieser Folge.
Für die ersten beiden Zeitpunkte wurden insgesamt **64Snapshots mit2944
Actorbindungen und5888 einzelnen C90/C7A-Rohwertvergleichen** kontrolliert.
Kein Akteur oder Slot fehlt; jeSnapshot23Spieler proSeite.

Zusätzlich wurden C90/C7A im vorbereiteten Originalinputdump direkt als
Little-Endian-U16 bei den Offsets0xC90/0xC7A aus `input_tail_hex` decodiert und
mit den identitygebundenen Observerfeldern abgeglichen. Dies nutzt keine
Studienfunktion zur Interpretation des Offdiagonalarms.

In allen vier Kontext×Seiten-Zellen und beiden Wiederholungen gilt für die
zehn Zielakteure nach Vorbereitung **und** erstem tatsächlichem Fortschritt:

| Arm | C90 roh | C7A roh | Empirisches Cachebyte8A an beiden Zeitpunkten |
| --- | ---: | ---: | ---: |
| C90L-C7AL | 7000 | 7000 | 70 |
| C90H-C7AL | 10000 | 7000 | 100 |
| C90L-C7AH | 7000 | 10000 | 70 |
| C90H-C7AH | 10000 | 10000 | 100 |

Damit sind insbesondere **beide Offdiagonalen unabhängig erhalten**; die
Engine hat sie in dieser Phase weder gleichgesetzt noch auf dieselbe Diagonale
normalisiert. Keeper, Bank und Gegner bleiben10000/10000. Condition10000,
Fatigue0, Accumulator1000000 und Penalty0 stimmen bei allen46Akteuren.
Die eigenen rekonstruierten Kontrollhashes einschließlich roher33Byte-Region
entsprechen jeweils dem vorab eingefrorenen D00-Goldbeleg. Cache89 ist100.

**Technische neue Beobachtung:** Cache8A unterscheidet in diesem Fixture beim
Start die C90-Stufen, während eine isolierte C7A-Änderung es hier nicht ändert.
Das ist eine empirische Zuordnung der beobachteten Startbytes. Es beweist
weder, dass C7A wirkungslos ist, noch dass alle Engineverbraucher nur C90 lesen,
noch eine FM-UI-Prozentskala. Spätere Änderungen, Wirkungsgrößen und natürliche
Karriereerreichbarkeit sind dadurch nicht geklärt. Es wurde kein Cachewert
geschrieben, kein Clamp eingeführt und keine Consumerannahme als Gate benutzt.

## Wiederholung, Negativkontrolle und Prozessbereinigung

Alle **16A/A-Paare** stimmen exakt in tatsächlichem Ergebnis/Teamstatistik
sowie den vorab identifizierten, identitysortierten Zustandsfeldern an allen
drei Zeitpunkten überein. Die eigene direkte A/A-Prüfung umfasst Rohfelder,
Controls, roheTF33, Cache89/8A und Fortschrittsmetadaten. Sie behauptet keine
semantische Gleichheit beliebiger undecodierter Speicherbereiche.

Die separate malformed-Binärprobe endet mit **Exit108**, genau einem
`scenario_rejected` und ohne natürlichen Matchabschluss.33geplante,
33gestartete und33aufgelöste Jobs;32gültige Vollmatches plus eine erwartete
Abweisung. Keine offenen oder unbegonnenen Technikjobs, Retries oder Ersatzseeds.
Alle512Hauptjobs sind noch ungestartet und nicht als technische Replikate gezählt.

Alle **33Kernelcontainmentreceipts** wurden auch direkt geprüft:
Kapselende und Bereinigung bestätigt, Kernelprozesszahl nach Bereinigung0,
erfolgreiches Jobterminieren, keine Cleanupfehler. Joblimit3, Kill-on-close,
kein Breakaway unverändert. Alle Rohlog-/Dump-/Containmenthashes stimmen mit
dem Ledger überein.0Pendingmarker, gemeinsame NativeLease frei; zusätzliche
Windows-Prozessabfrage findet0Observer-/Simulatorreste.

Der Dispatchbeleg misst maximal4gleichzeitig zugelassene Calls. Dies ist ein
Claim-Peak, **kein gemessener Engine-PID-Peak**. Die Prozessobergrenze folgt
zusätzlich dem unveränderten Host-/Containmentvertrag.

## Budget und Publikationschronologie

Die Technik startete erst nach veröffentlichtem Commit
`b53c56e07f58b6756fbd15f110ec2a71e4475a4e` und erfolgreicher
[CI43649328317](https://github.com/Matchekk/FM-27-Research/actions/runs/43649328317).
Der Reviewer hat das tatsächliche Actions-API-Ergebnis geprüft: derselbe
Head-SHA, `completed/success`, Abschluss22:42:56UTC. Die äußere technische
Phase beginnt22:44:40,740805UTC, das innere Studienbudget22:45:10,134292UTC;
reconciled Abschluss22:46:28,689642UTC. Die Reihenfolge stimmt.

- Eigene beaufsichtigte technische Childzeit: **78,533186s /900s**.
- Äußere globale NIGHT-002-Childzeit: **107,9617252s /3600s**.
- Separat summierte tatsächliche33Callzeiten: **110,736s**, längsterCall3,656s.
  Die Summe paralleler Calls ist eine andere Größe als die ganzen
  beaufsichtigten Phasen; alle drei Werte werden getrennt berichtet.
- Eigene unverrückbare5400s-Frist:15.11.00:15:10,134292UTC.
  Globale Deadline unverändert15.11.07:00UTC/08:00CET. Keine Fristverlängerung,
  Zeitrückerstattung oder Öffnung eines alten NIGHT-001-Vertrags.
- Geprüfter Snapshot nach Technik:19.467.245privateStudienbytes,
  19.480.110Bytes im gesamten neuen Missionsbaum; unter2/4GiB.

Innere und äußere Budgets sind erfolgreich reconciled, ohne aktive Operation
und ohne Halt. Reservationen enthalten exakt die33technischen Jobkeys und
keine Hauptphase. Unmittelbare erste Mainadmission muss die vorregistrierten
mindestens600s eigener/globaler Child-/UTC-Restzeit später nochmals prüfen;
dieser Review ersetzt dieses Laufzeitgate nicht.

## Releasebindung und Grenzen

SHA256 der geprüften technischen Summary, LF-normalisiert:
`afac46d26380677b766affc2130fab5cbc3093c5eb77377abc215673e159faf9`.
Das [technische Releasegate](../../data/night-002-split004/technical-release.json)
bindet diesen Hash und den Hash dieses unabhängigen Reviews.
Alle32eingefrorenen Projektquellen stimmen weiterhin mit dem Inputmanifest
überein. Der tatsächliche Host/Enginekontext bleibt FM27 `27.0.1+2503222`,
v1114.6, unveränderter Observerhost und dasselbe gebündelte D00-Fixture.

**Abnahme:** getrennte Rohfeldübertragung, vorhandene Kontrollgleichheit,
Wiederholbarkeit, Negativprobe, Prozessbereinigung und Technikbudget bestanden.
Der registrierte Hauptlauf darf erst nach Publikation und erfolgreicher
Freigabe-CI zentral beginnen. Noch kein Leistungs-, UI-, Consumer-, Trainings-
oder Karrierebefund; Cacheassoziation ist kein Mediationsnachweis.
Durch diesen Reviewer ausgeführt: **0 native Aufrufe, 0 neue Matches,
0 Seedreservierungen, 0 Karriereaktionen**.

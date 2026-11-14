# MECH-004-SPLIT-R0 – unabhängiger Review des terminalen Stopps

15.11.2026 CET · neuer Prüfgegenstand nach dem Hauptlaufabbruch.
**Saubere technische Schließung bestätigt; die wissenschaftliche Serie ist
unvollständig und dauerhaft beendet. Keine Wiederaufnahme oder Ersatzserie.**
Dieser Review ist weder eine Hauptmatchfreigabe noch eine Freigabe zur
Auswertung der Teilserie. Der vorherige technische Release bleibt historischer
TECH32+1-Beleg und wird durch den späteren terminalen Stopp nicht zu einem
erfolgreichen Hauptlauf umgedeutet.

## Tatsächliche Abrechnung statt Teilserienbefund

Geprüft wurden die privaten Dispatch-/Jobbelege, Archive und wiederhergestellten
Originale sowie [öffentliche Mainabrechnung](../../data/night-002-split004/main-job-accounting.jsonl),
[Mainstatus](../../data/night-002-split004/main-summary.json),
[Budgetstatus](../../data/night-002-split004/main-budget.json),
[Termination](../../data/night-002-split004/termination.json) und
[einzeln gemessene Callzeiten](../../data/night-002-split004/native-call-time.json).

| Gegenstand | Tatsächlicher Zustand |
| --- | ---: |
| Geplante Hauptjobs | 512 |
| Erfolgreich abgeschlossene Hauptmatches, Rohbelege erhalten | 224 |
| Geclaimter Job mit Guardfehler **vor** nativer Invocation | 1 |
| Nicht gestartete Hauptjobs | 287 |
| Technik aus separater abgeschlossener Phase | 32Vollmatches +1erwartete Negativabweisung |
| Tatsächliche native Calls beider Phasen zusammen | 257 |
| Bestätigte Kernelbereinigungen | 257 |

Die512öffentlichen Mainzeilen stimmen in Identität, Status und Seed mit dem
geplanten Manifest und den privaten Markern überein. Der Dispatch enthält
225Claims/225aufgelöste Einträge,224`ok` und1`failed`,0aktive Claims und
0`started_unresolved`. Die287unbegonnenen Jobs enthalten auch einen zusätzlich
vor Claim abgewiesenen Admissionversuch; dieser zählt nicht als weiterer
gestarteter oder nativer Job.

Alle224erfolgreichen Mainbelege wurden **einzeln technisch** nachgeprüft:
Originallog-/Dump-/Containmenthashes, Setup-/Seed-/Actor-/Buildbindungen,
deklarierte getrennte Rohfelder, native Profile/Attribute/Phasen/PI und
Kontrollgleichheit. Dabei wird der bereits geprüfte niedrigstufige Inputaudit
wiederverwendet. Es wurden keine Fußballendpunkte über Matches aggregiert,
keine Kontraste, Effekte, Intervalle, p-Werte oder Sekundäranalysen berechnet.
Die224Messungen ersetzen weder die fehlenden288Mainplätze noch den kompletten
vorregistrierten512Match-Lauf. Kein Missing wurde als Null behandelt.

`scientific_analysis_allowed=false`, `complete=false`, `passed=false` sind im
öffentlichen Mainstatus korrekt. `main.jsonl`, `effects.json` und
`seed-contrasts.jsonl` sind nicht als erfolgreich publizierte Mainausgaben
vorhanden. **Kein Schärfe-Wirkungsbefund aus dieser Teilserie.** Der technische
Abbruch ist weder ein wissenschaftlicher Nullbefund noch ein Gegenbeweis der
ursprünglichen Hypothese.

## Beobachteter Fehler und Grenze der Ursachenbehauptung

Der geclaimte Fehlerjob besitzt `native_invocation_started=false`, keinen
Admittedmarker, keine nativen Jobdateien und den Fehlertext
`Mission artifact path escaped`. Ein anderer Job besitzt denselben Fehler im
separaten Admissionfailuremarker und keinen Startedmarker. Damit ist für beide
Fälle **kein Engineaufruf** belegt oder zu verrechnen.

Der Director hatte während der noch laufenden Phase eine verlustfreie
Komprimierung bereits abgeschlossener Belege ausgeführt. Die Archivquelle
prüft Cleanup und Bytehashes, entfernt danach aber Originalpfade inklusive
abgeschlossener Dispatchmarker; gleichzeitig traversiert der globale
Pfadschutz den Missionsbaum. Die vorhandenen Zeitmetadaten zeigen die
Archivierung im Fehler-/Abschlusszeitfenster. Der protokollierte Guardfehler
ist mit dieser konkurrierenden Pfadänderung vereinbar. Ein tatsächlicher
Pfadausbruch oder eine Veränderung laufender Engineinputs wurde **nicht**
nachgewiesen; die Race wurde vom Reviewer nicht erneut erzeugt.

Der präzise belegte Stopgrund ist die Admissionabweisung während dieser
konkurrierenden Belegkomprimierung. Vollständige Wiederherstellung hebt den
terminalen Fehlervertrag nicht auf. Die Sicherheitsprüfung darf nicht gelockert
und der geclaimte Job nicht erneut gestartet werden. Künftige unabhängige
Studien benötigen eine andere, vorher geprüfte Arbeitsregel: keine solche
Dateistrukturänderung während einer aktiven nativen Phase.

## Rohdaten erhalten und Bereinigung vollständig

Der Reviewer hat das private ZIP, seinen Journalhash, CRC/Memberabdeckung und
**alle1024Archivinhalte** erneut gelesen. Ihre SHA256 stimmen jeweils mit
dem Journal **und** dem wiederhergestellten Original am ursprünglichen Pfad
überein. Es handelt sich um128abgeschlossene Jobs mit je acht Dateien/Markern.
Alle ursprünglich geclaimten225Mainmarker sind wieder vorhanden; die
224erfolgreichen Jobsets besitzen sämtliche im Ledger gehashten Originalbelege.
Für diese überprüften Daten wurde kein Verlust festgestellt. Das private
Archiv bleibt als Fehler-/Wiederherstellungsnachweis erhalten.

Alle257tatsächlichen Calls aus Technik/Main besitzen gehashte, direkt geprüfte
Kernelcontainmentreceipts: Kapselende/Bereinigung bestätigt,0aktive
Kernelprozesse nach Bereinigung, keine Cleanupfehler und unverändertes Joblimit3.
0Pendingmarker, keine gemeinsame aktive NativeLease und zusätzliche
Windows-Prozessabfrage mit0Observer-/Simulatorresten. Der vor Invocation
abgewiesene Job besitzt bewusst keinen erfundenen Cleanupreceipt eines Calls.

DLL, Observerhost, dessen Buildmanifest und Fixture stimmen weiterhin mit den
ursprünglichen Inputhashes überein. Die32ausgeführten eingefrorenen Projektquellen
wurden gegen ihre Original-Gitblobs im Vorregistrierungscommit geprüft.30davon
sind auch aktuell bytegleich. Zwei Controllerdateien werden inzwischen für
den **neuen**, separat zu prüfenden TACT-003-Pfad geändert; ihre beobachteten
Dateizeiten23:12:42/23:14:07UTC liegen nach dem alten Budgetabschluss23:05:28UTC.
Das ist keine Behauptung, der aktuelle Controller entspreche weiterhin dem alten
Ausführungsepoch. Die originalen Quellen bleiben über Git und ihre Hashes erhalten;
der alte Runner, seine Inputs, das alte Budget und die native Spielbinärdatei
wurden für eine Wiederaufnahme nicht verändert. Die tatsächlich ausgeführte
Archivquelle liegt zur Vermeidung einer erneuten aktiven Nutzung unverändert
unter [archive_completed_native_v0.py](../../archive/night-002/archive_completed_native_v0.py)
und stimmt mit dem in `termination.json` festgehaltenen Hash überein.

Im geprüften Studienrunner existiert kein Karriereadvance-/Savepfad; alle
Invocationen verwenden das gebündelte Fixture. Im neuen privaten Missionsbaum
liegen0`*.fm`-Dateien. Dieser Review führte keine Karriereoperation aus und
erteilt keine Karrierefreigabe.

## Alle Zeiten und Reservationen bleiben verbraucht

- Inneres Studienbudget: `halted=true`, `active=null`, belastet
  **528,8133745s** =78,533186sTechnik +450,2801885sfehlgeschlagene Mainphase.
- Globales altes NIGHT-002-Ausführungsepoch: `halted=true`, `active=null`,
  **589,7353507s** =107,9617252sTechnik +481,7736255sMain.
- Separat summierte257tatsächliche Callzeiten: **838,064s**,
  davon110,736sTechnik und727,328sMain. Keine parallele Zeitdefinition wird
  still mit der anderen gleichgesetzt oder rückerstattet.
- Exakt **545Jobreservationen** bleiben im inneren und äußeren Ledger:
  33Technikplätze und512Mainplätze, auch die fehlgeschlagenen/unbenutzten.
  Alle **68Seeds** (64Main/4Technik) bleiben unverändert in Registry und
  öffentlichem gehashtem Seedplan reserviert. Kein Ersatzseed oder Rename.

Beide belasteten Zeitsummen entsprechen exakt den unveränderten Operationen.
Der öffentliche Fehlerbudgetexport kennzeichnet seinen erfolgreichen
Reconciliationwert korrekt als fehlend und bewahrt die tatsächlichen
aufgezeichneten Belastungen gesondert. Eine spätere administrative
Reconciliation darf keine alten Fehler, Charges oder Reservationen überschreiben.

Geprüfte SHA256 der terminal geschlossenen Budgetdateien:

| Artefakt | SHA256 |
| --- | --- |
| Globales altes Budget | `dad11f1be95f9bbccff8e9b62079d943af63cbd3828790e96f07809986bad114` |
| Eigenes Studienbudget | `492bbb53cf803aaa59d1d2a16ebd6cdfd42cfb989ce77592e72d897e6b964971` |

## Zulässige Erkenntnis und Abschlussumfang

Die unabhängig abgenommenen **32initialen Technikmatches** behalten ihren
engen Aussagewert: beide Offdiagonalen überstehen Vorbereitung/Erstfortschritt;
das beobachtete Startcache8A beträgt70bei C90low und100bei C90high unabhängig
von C7A. Kein zusätzlicher Leistungs-, UI-, Consumer- oder Karrierebefund wird
aus den224Teilserienmessungen abgeleitet.

Das [Termination-Reviewgate](../../data/night-002-split004/termination-review.json)
bestätigt allein die überprüfte saubere Schließung und dauerhafte Sperre von
MECH-004. Eine vollständig unabhängige Frage `TACT-003-STLESS-R0` benötigt
eigene Quellen-/Input-/Runner-/Technikabnahmen und eine separat veröffentlichte,
geprüfte administrative Reconciliation mit erfolgreicher CI. **Dieses Review
erlaubt keine Mainfortsetzung, Wiederaufnahme oder Budgetrücksetzung irgendeiner
Studie.** Native Aufrufe, neue Seeds und partielle wissenschaftliche
Effektberechnungen durch diesen Reviewer: jeweils0.

# VALID-004-R3-DIAG – unabhängige Prüfung des endgültigen Supervisors

14.11.2026. Geprüft: ursprünglicher Runner `2054bd3`, danach die separaten
Korrekturen `ba82daf96c76a1b49b06fc71314c4535b07d70c5` und
`a5868d119484040490d56d2d0eae9bbaf48de92f`. Eigener Reviewbranch
`codex/night-career-r3-runner-review`; keine Änderungen fremder Quellen.

**Der programmierte einmalige Read-only-Diagnosepfad ist für den folgenden
endgültigen Vertrag technisch geprüft. Ein echter R3-Pass wurde nicht ausgeführt.**

LF-normalisierter SHA256 von `data/night-001-career-r3/final-contract.json`:

`116caf7e203c6a6735218b4f712f4fcf732bba0525cd0e8b6b9ac2087307f5ee`

Diese Freigabe gilt ausschließlich nach Veröffentlichung genau dieses Vertrags,
Codes und Reviews, erfolgreicher GitHub-CI auf genau deren vollständigem Commit
und separatem Director-`published proceed`. Sie ersetzt kein Laufgate und erteilt
keine native, Taktik-, Trainings-, Replay- oder Karriereadvancefreigabe.

## Unabhängig nachgeprüfte Quellen und Eingaben

Eigene Hashrechnung gegen tatsächliche Dateien: sämtliche eigenen Quellen,
Dokumente und Inputverträge stimmen mit den LF-normalisierten Manifestwerten
überein. `research/__init__.py` ist ausdrücklich mitgebunden. Alle86 offiziellen
Pythonquellen stimmen sowohl mit dem eingefrorenen Inventar als auch mit den
unabhängig gelesenen Bytes des offiziellen0.12.4-Wheels überein. Isolierte
Distributionsmetadaten, Basis-fmsave0.9.0, Basisinterpreter und19 deklarierte
Decompressor-Python-/Pyd-Dateien einschließlich Metadaten stimmen ebenfalls.
Kein fmsave wurde für diese Quellenprüfung importiert.

Der einzige zulässige Snapshot ist die bestehende private R0-Kopie mit
147.130.636Bytes und SHA256
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
Dies ist hier ein Abgleich der unveränderten Vertrags-/R0-Belegbindung;
der Reviewer hat den Save ausdrücklich weder geöffnet noch erneut gehasht.
Die tatsächliche Identität muss erst der zulässige Decoder vor dem Readeraufruf
und danach erneut prüfen.

## Startgrenze und Ressourcen

Vor `Popen` werden zentraler Checkout, exakte Quellen, vollständiger
veröffentlichter Commit, vorgesehener Remote, erfolgreiche exakte CI,
veröffentlichter Reviewhash mit obigem Vertragshash und Directorfreigabe geprüft.
Ein vorhandenes privates R3-Verzeichnis sperrt jeden neuen Versuch. Die
Release-Datei wird vor ihrem Inhaltszugriff auf aufgelösten Pfad, festen privaten
JSON-Bereich und maximal64KiB begrenzt. Der Parent öffnet keinen Save.

Der direkte Basisinterpreter startet als **ein** tatsächlicher Prozess mit
`-I -S -B`. Vor GO liest sein Bootstrap nur das begrenzte private stdin-Paket;
kein Projekt-/Readerimport und kein Savezugriff. Der Parent weist zuvor den
konkreten eigenen Windows-Job zu und prüft Mitgliedschaft und Policy. Erst nach
GO und Runnerhashprüfung werden Projekt- und Readerquellen geladen.

Der eigene Readeradapter verlangt Flags0x2308, Prozesslimit1,3GiB harte
Prozess- und Job-Private-Memory, Kill-on-close ohne Breakaway, Decoderexit,
Kernel-Active-Process-Count0 und finalen Policyreadback vor Handleabschluss.
Die unveränderten nativen3..10-Prozess-Prüfregeln werden dafür nicht gelockert.
Unbestätigte Bereinigung erhält die exklusive ReaderLease und den dauerhaften
Versuch; keine automatische Übernahme oder Wiederholung.

Das feste175s-Fenster wird vor GO erneut gegen monotone Zeit und verbleibende
UTC-Zeit abzüglich5s Cleanup geprüft. Auch die Schleife prüft die absolute
23:00UTC-Deadline mit Cleanupreserve. Ein rechtzeitig gestarteter Parent gibt
nach verspäteter Jobzuweisung damit keine verspätete Decoderzulassung mehr.
Ein tatsächlicher Overshoot bleibt ein Budgetfehler, kein gültiger Befund.

Die bekannten Writer sind auf128KiB Parentmetadaten,256KiB Childmetadaten,
64KiB Stufenledger und64KiB stdout/stderr begrenzt; insgesamt512KiB innerhalb
des1MiB-Verzeichnislimits. Der letzte Bytezähler schließt sein eigenes
Completionreceipt ein. Outputüberschreitung wird gekennzeichnet und stoppt den
Job. Keine großen Dumps oder Savekopien sind vorgesehen.

## Vor einer echten Ausführung korrigierte Reviewbefunde

Vier eigene Regressionen scheiterten auf der ursprünglichen Fassung:

- Nach bereits verbrauchtem175s-Fenster beziehungsweise überschrittener
  UTC-Deadline wurde noch GO gesendet. Jetzt stoppen beide Grenzen davor.
- `-B` allein verhinderte zwar Cache-Schreiben, aber nicht das Laden vorhandener
  `.pyc`. Ein harmloser temporärer Test zeigte abweichenden Cachecode trotz
  unverändertem Sourcehash. Das ist kein beobachteter Tamperbefund an unseren
  Projektdateien. Jetzt wählen Parent und Bootstrap vor Projektimporten einen
  frischen nachgewiesen nicht vorhandenen privaten UUID-Cacheprefix und
  deaktivieren Bytecode-Schreiben; keine bestehenden Caches werden gelöscht.
- Ein falscher Releasepfad konnte zuvor vom Parent als JSON gelesen werden.
  Pfad-, Suffix- und Größenprüfung erfolgen jetzt vor Inhaltszugriff.

Zusätzlich wurde ein verschachtelter ungültiger Markerbeleg geprüft:
`marker_checks=[null]` brach den Export zuvor mit `AttributeError` ab. Ein enger
Dictguard macht daraus jetzt `invalid_retained`; alle fünf Stufen und der
ursprüngliche Fehler bleiben sichtbar, der Diagnosestatus bleibt ungültig.
Kein breites Exceptionverschlucken oder Ersatzwert wurde eingeführt.

## Unveränderte Grammatik und vollständige Abrechnung

Der bereits separat geprüfte äußere Exception-Observer bleibt unverändert.
Genau ein striktes `open` und ein `tactics()`-Aufruf, keine Fremdfunktionsersetzung,
V10-Patches, zusätzlichen Probes oder alternative Marker-/Offsetsuche.
Originalargumente, Rückgabeobjekt oder identische Exception bleiben erhalten;
interne verworfene Kandidatenfehler werden nicht als finaler Fehler ausgegeben.
Close und Nachhash werden auch nach Taktik- oder Ledgerfehlern versucht.
Nach nicht bestandener initialer Identität gibt es keinen weiteren Snapshotread.
Bei hartem Kill fehlende Finally-Belege bleiben Missing, ohne Ersatzread.

Alle fünf Stufen behalten beobachtet, fehlgeschlagen, unbegonnen oder
gestartet-unaufgelöst sowie ungültige Ledgerzeilen. `export` liest ausschließlich
erhaltene JSON-Artefakte, startet keinen Prozess und räumt keine Lease auf.
Ein gültiger Fehlerortstatus erfordert vollständige Identitäts-, Warnungs-,
Marker-, Ressourcen- und Abschlussbelege. Genau eine `UnknownBuildWarning`
wird erwartet und bleibt ausdrücklich kein Beweis eines bekannten Layouts.
Zusätzliche oder abgeschnittene Warnungen verhindern gültigen Diagnosestatus.

Öffentliche Felder sind feste Codes, geprüfte Counts/Boolwerte und Hashes sowie
die im neuen RUN-Vertrag explizit erlaubten abgeleiteten Bereichszählwerte.
Keine absoluten Cursor-/Blockoffsets, Savebytes, Namen, Spieler-IDs, privaten
Pfade, Warnungstexte oder fremden Objektrepräsentationen werden exportiert.
Ein erfasster ursprünglicher Taktikfehler ist kein erfolgreich gelesener
Taktikdatensatz und keine native IP-/OOP-/SET-Prüfung.

## Tatsächliche Prüfung und verbleibende Gates

33gezielte Tests bestanden:27Autortests und sechs eigene Regressionen.
Darunter fünf echte harmlose Windows-Kerneltests für GO, Speicherabweisung,
Prozessgrenze, Kill-on-close und Sourceausführung trotz abweichendem Temp-PYC.
Die vollständige Suite dieses Reviewcheckouts bestand mit301Tests, davon zwei
wegen nicht vorhandener privater historischer Goldbelege ausgelassen; zusätzlich
fünf historische Analysetests. Archivprüfungen bestätigen340 NIGHT-Basisdateien
und272 Round3-Basisdateien unverändert. Der enge Quellen-/Paketabgleich bestand.

Reviewer:0echte Saveöffnungen/-hashes,0Decoderstarts,0native Hosts,0Seeds,
0Kalenderadvances. Harmloser temporärer Pythoncode ist kein Save- oder Enginetest.
Ein echter R3-Pass bleibt bis Veröffentlichung, exakter erfolgreicher CI und
separatem Director-Proceed ausstehend. Danach sind seine realen Rohbelege erneut
unabhängig zu prüfen. Alle wissenschaftlichen und Karrierefreigaben bleibenfalse.

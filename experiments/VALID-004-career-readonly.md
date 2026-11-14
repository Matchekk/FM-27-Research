# VALID-004-CAREER-R0 – unveränderter Testsave, rein lesender Readeraudit

Vor dem ersten Readerlauf festgelegt,14.11.2026. Technischer Coverageaudit,
keine Trainings-,Match- oder Karrierewirkungsstudie. Ein ausdrücklich vom Nutzer
benannter Wegwerfspielstand wird ausschließlich als stabile private Kopie gelesen.
Keine anderen Saves suchen/öffnen; keine Kalenderfortschreibung,kein Replay,
keine Seeds,kein NativeHost und kein Zugriff auf den laufenden Spielprozess.

## Fragestellung und Kontrolle

Kann installiertes fmsave0.9.0 den freigegebenen aktuellen Testsave strukturell
lesen und welche benötigten Endpunkte bleiben unbekannt? Primär vollständiger
Status aller zwölf vorab benannten Readerprobes; keine Effektgröße/Power aus
einem Checkpoint. Kontrollinvariante: Source-SHA256 vor Kopie,nach Kopie und
nach dem Reader unverändert; private Kopie identisch. Drift stoppt Freigabe.

Probes in fester Reihenfolge: open,managed_clubs,clubs,players,training,tactics,
selections,set_pieces,staff,staff_lists,injuries,fixtures. fmsave-FM27-Strictchecks
werden nicht abgeschaltet oder durch Boundsüberschreibung umgangen. Fehler
einer Methode werden erhalten; weitere unterschiedliche Methoden dürfen nur
innerhalb desselben einmaligen Passes die Coverage erfassen. Der Quellcache
merkt bereits gescheiterte gemeinsame Decodes; kein teurer Wiederholungsversuch.

## Ressourcen und Datenschutz

Ein Pythonreader,ein Versuch,180s ab Start einschließlich Snapshot,keine Retries.
Privater Prozessspeicherwächter beendet oberhalb1536MiB; Beobachtungsintervall
0,2s,kein behaupteter kernelharter Speicherlimit. Paket-FM27-Sektionen sind
zusätzlich auf512MiB gesamt/256MiB pro Frame begrenzt. Maximal512MiB Quelldatei,
maximal1GiB neue private Artefakte. Jeder gestartete,fehlgeschlagene und
unbegonnene Probeplatz bleibt im privaten Ledger und öffentlichen Status.

Öffentlich nur eigenes Schema,Versions-/Quell-/Savehashes,anonyme Teamcodes,
Zählwerte,Rawcodehäufigkeiten und Missinggründe. Save,Personen- und Team-IDs,
Namen,Quellpfade,rohe Fehlermeldungen und Originaldaten bleiben privat.

## Harte Grenzen

Readerchecks belegen strukturelle Konsistenz,keine native Feldsemantik oder
unabhängige Karriere-RNG. Gespeicherter Teamkalender ist keine individuelle
Durchführung; erwartete Rückkehr ist kein beobachtetes Verletzungsende. Keine
Roh-/Anzeigekalibrierung aus bloßen Zahlenpaaren und keine taktische Wirksamkeit
aus gespeicherten Rollen-/Instructionswerten. Da Windows-Bildaufnahme am
FM-Fenster aktuell zweimal timeoutete,ist die geöffnete Karriere unabhängig
von der Dateiquelle noch nicht visuell gebunden. Freigaben für nativeSimulation,
Karriereadvance,Trainingseffekt und Replay bleiben in jedem Ergebnis false.

Ergebnisse und tatsächliche Einschränkungen werden nach dem einmaligen Pass
ergänzt. Originalforschung und bestehende Module bleiben unverändert.

## Tatsächliches Ergebnis R0 – blockiert

Ein Pass am14.11.2026 um17:27:50UTC,0,703/180s,ein eigener Pythonreader.
Snapshot147.130.636Bytes; SHA256
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`
war vor Kopie,nach Kopie und nach Reader identisch; Kopie ebenso.

`open` scheitert mit `UnsupportedGameError`: Die installierte Version0.9.0
registriert für `SaveSummaryLayout`/`save_game_summary` kein Layout zur
Kombination Build27.0.1+2503222/Schema31. Alle elf übrigen Probeplätze bleiben
**not_started**,nicht Nullbeobachtungen. Keine Wiederholung,kein Schema-/Buildpatch,
keine größere Memorygrenze und kein stiller Rückfall auf FM26.

**Wichtig:** Schema31 ist bereits für27.0.0+2486695 registriert. Der Fehler
beweist zunächst fehlende exakte Buildzulassung,nicht dass sich die Bytegrammatik
tatsächlich verändert hat. `_layouts.find_layout` lässt in0.9.0 für FM27 nur
exakte Build-/Schemaeinträge zu. Die daraus abgeleiteten Endpunkte und die
aktiveKarrierezugehörigkeit bleiben unbekannt. Der Lauf bindet nur die explizite
Dateiquelle,nicht das visuell nicht erfassbare geöffnete Spiel.

Erfasster privater Prozessspeicher maximal901.120Bytes in0,2s-Abtastung. Das
ist **keine** Aussage über den wirklichen kurzzeitigen Peak; der sehr kurze
Fehlerpfad kann zwischen Abtastungen mehr Speicher benutzt haben. Der Watcher
wurde vorher an einem eigenen harmlosen Pythonprozess funktionsgeprüft.
Die abgebrochene Summarymetadatenlesung ist auf1MiB begrenzt;FM27s engerer
Indexcap wird erst nach erfolgreicher Versionsmetadatenprüfung angewendet und
wurde in diesem frühen Fehlerpfad noch nicht erreicht.
PrivateArtefakte147.132.191Bytes,unter1GiB. NativeStarts/Matches/Advances/Seeds je0.
Sämtliche Freigabeflags bleibenfalse.

## Einordnung und nächster separater Meilenstein

Dieses R0 ist eine rein lesende Teilstufe von
[VALID-004Phase1](VALID-004-test-fm-research.md),keine Erfüllung der dortigen
Feld-/Matchzugehörigkeitsgates. [Coverage](../data/night-001-career/coverage.json),
[strukturierterBlocker](../data/night-001-career/blocker.json),
[Quellbelege](../data/night-001-career/run-provenance.json).

Die offizielle [PyPI-Version0.12.4](https://pypi.org/project/fmsave/),veröffentlicht
13.11.2026,ist ein möglicher **separat zu prüfender** Reader. Aktuelle Dokumentation
bezeichnet nicht registrierte FM27-Builds alsunverified und meldet geliehene
Layouts; das ist keine native Feldbestätigung. WheelSHA256
`2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa`;
PublishingCommit`e0704bc5d7e6bf687fecf85cd48b28c497bdef68`.

[PrimäreReleasenotes](https://rhiever.github.io/fmsave/changelog.html):Seit0.9.1
können unregistrierteFM27-Builds passendeLayouts leihen,seit0.12.3 auch bei
abweichendem Schema mitWarnung.0.12.1 korrigiert bestimmteTrainingtrailer.
Seit0.10.1 bleibenPopulation-/Coveragechecks selbstimStrictmodus Warnungen.
Ein R1 muss deshalb **jede Warnung und Feldabdeckung** prüfen; kein Exception
allein bedeutet keinen Gateerfolg. Stand14.11.2026,keine Installation oder
erneuteSaveöffnung innerhalbR0. Basispaket/Pins bleiben unverändert.

Auch der vorhandene Lab-Quelladapter `desktop_save_compat.py` nennt den aktuellen
Build,ändert aber zusätzlich Layoutvarianten und Decompressionsgrenzen.
Er wurde nicht ausgeführt und ist kein Ersatz für eine eigene R1-Abnahme.
Weder Readerupgrade noch Labadapter dürfen den erhaltenen R0-Fehler ersetzen.

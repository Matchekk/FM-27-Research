# NIGHT-001 – unabhängiger Quellen-, Provenienz- und Gate-Review

14.11.2026. Reviewbasis `79c5663`, eigener isolierter Reviewbranch.
**Vorarbeiten nachvollzogen; keine native Start- oder Hauptstudienfreigabe.**
Der separate neue Observer-Supervisor war bei diesem Review noch in Arbeit und
gehört ausdrücklich nicht zum geprüften Ausführungsumfang. R1/R2-Karrierearbeit
ist ebenfalls kein ausgeführtes Ergebnis dieses Berichts.

## Unabhängig geprüfte Originalbelege

Original-DLL tatsächlich als Dateiversion27.0.1 und Produktversion
27.0.1+2503222 gelesen; SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Originalhost SHA256
`2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`.
Upstream sauber, Tagv1114.6/Commit
`91f2eba57fac0b7fbd3dff616056907e3ce461be` tatsächlich abgefragt.
Privater Observer-Build3 SHA256
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`
stimmt mit privatem Manifest und öffentlichem Buildbeleg überein.

Alle19 originalen Quell-/Manifestdateien, MIT-Lizenz, kompilierten eigenen Header,
modifizierte Hostquelle, private Kompatibilitätsquelle, Compilerstdout und
Observerbinary anhand tatsächlicher Dateien gehasht. Die Hostquelle entspricht
bytegenau der deklarierten Transformation. Der ausgecheckte öffentliche Header
stimmt nach expliziter CRLF→LF-Normalisierung mit dem kompilierten LF-Header
überein. Keine Behauptung einer reproduzierbar identischen Neuübersetzung;
deren Nachweis fehlt weiterhin.

Die vier privaten statischen Disassemblate stimmen mit ihren veröffentlichten
Hashes überein. Stichproben der tatsächlichen Befehle bestätigen getrennte
Actor-/Cachequellen um0x36a20 und den Versionsvergleich bei0x47a01. Dies
belegt Datenflusskandidaten, keine Laufhäufigkeit oder UIeinheit. Originales
Kind62 schreibt vor Vorbereitung MATCH+0xa3a=0x1b000000; der Originalverifier
prüft dies. Die historische Carrierangabe26.8 beweist daher keine abgeschaltete
Tactical-Effectiveness-Verarbeitung. Auch das erfüllte Versionsprädikat beweist
noch keinen vollständigen Consumerpfad.

## Quellen und Missing Values

Karriere-R0: private Ereignis-/Attemptdateien stimmen mit ihren öffentlichen
Hashes überein. Ein tatsächlich gestartetes `open` scheitert nach0,703s;
elf weitere Probes bleiben `not_started`. Die gespeicherten Snapshot-Receipts
sind konsistent, die Snapshotgröße stimmt. Der Reviewer hat weder `.fm` geöffnet,
gehasht oder decodiert noch die ursprüngliche Quelldatei erneut gelesen; deren
damalige Bytegleichheit wird durch die erhaltenen Runreceipts belegt und nicht
als zweite unabhängige Inhaltslesung ausgegeben.

Installiertes fmsave0.9.0 und die konkreten Layoutquellen geprüft: exakte
FM27-Build-/Schemazulassung fehlt für27.0.1+2503222/31; Schema31 existiert für
27.0.0+2486695. **Zulassungsfehler, kein Beweis veränderter Bytegrammatik.**
Keine semantische Readerabdeckung, UIbindung, unabhängige Karriere-RNG oder
individuelle Trainingsteilnahme nachgewiesen. Gespeicherte Kalender bleiben
von tatsächlicher individueller Durchführung zu unterscheiden.

Das externe Register zählt zehn Seiten und sieben Provenienzlabels, keine zehn
Replikationen oder sieben Studien. Unabhängige Stichproben am14.11.2026:
[Patchtabelle](https://fm-arena.com/tactic-testing/aggregators/1/) zeigt eine
Dummyzeile/PLD600; [SI](https://www.footballmanager.com/fm27/features/fm27-tactical-tweaks-and-match-engine-upgrades)
motiviert Stamina-/Pressingfragen ohne Effektgröße;
[Purity](https://fm-arena.com/threads/attribute-importance-by-position-in-fm27-a-test-on-my-own-tactic.125/)
berichtet200000Matches/50000Konfigurationen für einen Club/eineTaktik.
Keine eigenen Rohjobs nachgerechnet. Der Browsingdienst konnte die Purityseite
nicht öffnen; ein eigener anonymer Standardbibliothek-GET erhielt200 und
bestätigte die genannten Textmerkmale. Die beiden alten Endpunkte erneut404.
Transportverfügbarkeit bleibt vom empirischen Wahrheitsnachweis getrennt.
Stamina40/80×Pressing bleibt bis eigener Registrierung/Abnahme ein Vorschlag.

## Technische Gates und offene Ausführungsprüfung

Header und fünf Einfügestellen gelesen: neue Operationen schreiben Hostlogs und
eigene Variablen; keine neuen Enginesetter, Hooks, Versionsschreibzugriffe oder
Clamps. Lesbarkeits-/Rostergrenze26, nullable Pointer+0x1880 und drei Stagequellen
sind vorhanden. Originale Profil- und Cachewerte sowie33Rohbytes bleiben
uninterpretierte Speicherbeobachtungen. Der private112Byte-Bereich wird erhalten,
aber sinnvollerweise vom deterministischen A/A-Endpunkt ausgeschlossen.

Der festgelegte Technikplan hat vier neue Seedzellen, vier Modi pro Zelle,
16Vollmatches+2Negativprobes+2Imagechecks=20Probeplätze. Die16Matches sind keine
16unabhängigen Leistungsreplikate. Noch ausstehend: publizierte konkrete Seeds,
CI, unabhängiger Review des fertigen Runners, tatsächliche Loader-/Input-/Seed-/
Provenienzgates, alle nativen Ergebnisgleichheiten und vollständige Stagebelege.
Keine automatische Freigabe der MECH-002-512erStudie oder anderer Hauptmatches.

Masterquellen `night_control.py`/`night_supervise.py` gelesen: feste Deadline
23:00UTC/5sBeendigungsreserve,1800Childsekunden,192Technik-/2048Mainplätze,
persistente phasen-/keygebundene Zulassung mit Tokenhash und lebendem Supervisor.
Die innere NativeLease und studieneigene Grenzen bleiben zusätzlich erforderlich;
der Master ist kein globaler OS-Lock. Fehlgeschlagene Operationen behalten
Zeit/Reservierung und sperren weitere Studien, kein Reset/Refund/Ersatzseed.

Review fand einen falsch eingerückten Testrest, der das Failed-Child-Gate nicht
ausführte. Director korrigierte die zentrale Testdatei; der Reviewer las den Fix
erneut und führte dort alle sieben Mastertests erfolgreich aus. Zusätzlich eigene
Regressionen für Fehlchild-Halt und studienübergreifende Gesamtkontingente.
Dieser Testbefund war kein nachgewiesener Fehler der geprüften Budgetlogik.

## Reproduktion und Status

Eigener Auditor [review_night001.py](../../analysis/review_night001.py) prüft
öffentliche Konsistenz und optional explizit benannte private Build-/Ledgerbelege.
Kein Save-Decoder-/Serverimport, kein nativer Start, keine Registry-/Seedmutation.
34gezielte Tests bestanden im Reviewworktree; die korrigierten sieben
Mastertests zusätzlich im zentralen Checkout. Historischer Archivvalidator:
340Dateien unverändert (335ausadb708e plus5aus parallelemfd954ba).
Zusätzlich alle162Repositorytests bestanden; `git diff --check` ohne Befund.

Reviewer:0native Host-/Spielstarts,0Matches,0Karriereadvances,0Seeds.
Alle Consumer-/UI-/Startpolicy-/Karriere-/Mainfreigaben bleibenfalse.
Lokaler Reviewcommit ohne eigenen Push; Integration/öffentliche CI liegen beim
Director. Ein späterer nativer Technikbefund benötigt einen separaten Review.

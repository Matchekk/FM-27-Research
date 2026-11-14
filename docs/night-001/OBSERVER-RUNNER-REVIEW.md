# VALID-005 – unabhängiger Review des seriellen Supervisors

14.11.2026. Erstprüfung `f94609d`, abschließender Fixreview
`4d2261fa661f1645cda30503e83683394aa37a12` einschließlich Containment
`a1caba3`. **Code und statische Vorbereitung freigegeben; keine native
Start-/Messfreigabe.** Observervorbereitung und technische Serie noch nicht
ausgeführt. Dieser Bericht prüft den Supervisor, nicht spätere Matchdaten.

## Befunde vor Freeze

Der erste Review fand zwei Ausführungslücken:

1. Nach erfolgreichem `Popen` konnten Fehler beim privaten Prozessreceipt oder
   Logmonitoring ohne bestätigte Childbeendigung propagieren. Der äußere Budget-
   supervisor behandelt Nichtnull-Rückkehr als Fehler, beendet dabei aber nicht
   automatisch einen bereits verwaisten Nachfahren. Die NativeLease könnte so
   trotz weiterlaufendem Host freigegeben werden. Synthetisch reproduziert:
   Receipt-I/O-Fehler, keine Kill-/Waitoperation; kein echter Prozess gestartet.
2. Nach Vorbereitung fehlte vor den Vollmatches die erneute Fixturehashprüfung.
   Ein erst später erworbener Leseguard bindet keine davor veränderte Datei an
   den alten Hash. Ebenso sind Host-/Inputhashes nach Erwerb aller Handles erneut
   gegen den Freeze zu prüfen. Ressourcenfingerprint wurde bereits wiederholt.

Beide Befunde wurden vor dem Freeze korrigiert und unabhängig erneut geprüft.
Der spätere separate Ergebnisreview darf dieses eingefrorene Dokument nach
`prepare` nicht verändern; tatsächliche Technikresultate benötigen ein neues Dokument.

## Korrekturen und abschließende Bewertung

`research/native_process005.py` ist ausdrücklich Teil des Codefreeze. Vor jedem
nativen CLI-Aufruf startet nur eine harmlose Basis-Pythonkapsel. Erst nach
Kerneljob-Zuordnung, spezifischem Mitgliedschafts- und Policyreadback und
privatem stdin-Token darf diese den eigentlichen Command starten. Kill-on-close,
kein Breakaway und maximal drei OS-Prozesse begrenzen Kapsel, CLI-Launcher und
seinen Enginechild. **Drei Prozesse sind ein serieller Engineworker**, keine
zusätzlichen drei Engineworker. Kein Speicherlimit wird für diesen Job behauptet.

Alle normalen und fehlerhaften Pfade verlangen bestätigten Kapselexit plus
Kernel-ActiveProcessCount0. Elternexit bei verbleibenden Nachfahren ist ein
Fehler; der ganze Job wird beendet. Schließen eines Jobs ohne erfolgreichen
Nullreadback genügt nicht als Cleanupbeweis. Der Wrapper verlangt zusätzlich
ein dauerhaftes Bestätigungsreceipt mit exaktem Prozesslimit3, bevor sein
Cleanupmarker entfernt werden darf. Fehlender/defekter Receipt bleibt sperrend.

Der Studienparent gibt die globale NativeLease nur bei reconciliertem inneren
Budget ohne Cleanupmarker frei. Sonst bleiben Lease, Haltflag und ausdrücklich
unvollständige Zeitabrechnung erhalten; keine automatische Übernahme oder
Rückerstattung. Offline-Crashexport erhält trotzdem alle20Probeplätze und
redigiert PID-/Tokenfelder im aktiven Zustand. Bestätigt bereinigte Fehler
bleiben Fehlversuche und schalten keinen Retry frei.

Nach Erwerb aller Leseguards werden Ressourcen, beide Hosts, das Originalfixture,
alle vier Binärinputs, Katalog und private Konfigurationen erneut gegen den
Freeze gehasht. Damit ist die zuvor gefundene Fixture-/Handlelücke geschlossen.
Opt-in-Negative benötigt nun den exakten `invalid_opt_in`-Grund; Binärnegative
ein `scenario_rejected`-Ereignis. Unerwarteter natürlicher Finish bleibt verboten.

13Kerneltests des neuen Helfers sowie zwei zusätzliche eigene Fehlerregressionen
eigenständig ausgeführt. Eigene Tests provozieren Receipt-I/O-Fehler vor GO und
`Popen.poll`-Fehler nach GO mit ausschließlich harmlosen Pythoncommands: jeweils
bestätigter Kernelnullstand und erst danach gelöschter Wrappermarker. Weitere
Fachtests decken Zuweisungsfehler, Callback-/Statfehler, Timeouts, lebende
Nachfahren, verschachtelte Jobs, verweigerte vierte Prozesse und fehlenden
Null-/Finalreceipt ab. Kein echter Host oder Spielprozess durch diese Tests.

## Bereits nachvollzogene Grenzen

Ein serieller CLI-Aufruf nach dem anderen; Originalhost und separater Observer,
keine Warmworker oder In-place-Modifikation. Vier Kontexte/Seitenzellen erhalten
je einen neuen Seed und vier gleiche D00-Eingaben in Referenz/aus/an/Wiederholung.
16Vollmatches+2Imagechecks+2Negativprobes=20Probeplätze. Ungültiger Opt-in erwartet
252 mit wiederverwendetem ersten Technikseed; defekte Binärdatei erwartet108 ohne
Seed. Kein Retry, Ersatzseed, Mainmodus oder Holdoutstart.

Vorbereitung liest nur Daten-/Quellbelege, kopiert vier bereits identische eigene
D00-Binärdateien und reserviert vier neue Seeds unter globalem Registrylock.
Kein Runtime-/Serverimport oder Hostaufruf in `prepare`. Die Vorbereitung selbst
läuft unter Masterzulassung, innerer NativeLease und dauerhaftem180Child-/900UTC-
Budget; die Frist beginnt damit bereits vor Publikation/CI und wird nicht erneuert.
Ein gewählter Worker,90sFortschrittsgrenze,512MiBArtefakt-/20GiBFreiraumkontrolle.

Der Master bindet Phase, alle20Keys und Token an einen lebenden Supervisor;
innere Zulassung bindet eigenen Token, Ownerpid und1Workerlease. `register`
verlangt vollen veröffentlichten Commit, erfolgreichenCI-Head genau diesesSHA,
Ancestorbindung an lokalesHEAD/Remote-main und bytegleiche öffentliche Gitblobs.
Technikphase prüft Freeze undCI erneut. Der Reviewbericht gehört selbst zum
eingefrorenen Codevertrag. Konkrete Seeds/Inputs sind noch nicht erzeugt und
werden dadurch noch nicht freigegeben.

Alle FM27-Diagnosevariablen werden entfernt; nur Engine-/Spielwurzel, erwarteter
DLL-Hash und deklarierter Observeropt-in werden gesetzt. Die dynamisch gelesene
Runtimequelldatei definiert Leseguards; `initialize`/Server werden nicht aufgerufen.
Erhaltene private Attempt-/Ledgerbelege und öffentliche20Slot-Abrechnung trennen
`not_started`, `started_unresolved`, fehlgeschlagen und erwarteteAbweisung.
Öffentlicher Export enthält numerische Resultate und Hashes, keine privaten
Rohdumps, Trägeridentitäten, Prozess-/Quellpfade oder Zulassungstokens.

Originalinputaudit am echten historischen privaten D00Gold unabhängig ausgeführt:
3174Attributwerte,1058Profilfelder, beidePhasen/PI; manipuliertes Attribut abgewiesen.
Kein Save/PKM geöffnet und kein nativer Prozess gestartet. Die16erErgebnis-/
Stagegleichheiten sind weiterhin ungemessen; Consumer-/UI-/Setter-/MECH-/Karriere-
undMainfreigaben bleibenfalse.

## Konkreter Freigabeumfang und Validierung

Alle222Repositorytests und fünf historische Analysetests im Reviewworktree
bestanden; ein privater-Goldtest ist dort mangels lokaler Artefakte übersprungen
und wurde gesondert auf den tatsächlichen zentralen Lesebelegen erfolgreich
ausgeführt.38gezielte Review-/Kernel-/Runner-/Mastertests bestanden. NIGHT340
und Round3-272 historische Dateien unverändert; `git diff --check` ohne Befund.

Statisches `prepare` darf unter authentifizierter Master-/innerer Zulassung,
persistenten Budgets und NativeLease die vier unveränderten Inputs prüfen und
vier neue Seeds reservieren, ohne Hostaufruf. Danach konkrete Inputs, Seeds,
Codefreeze und dieses unveränderte Dokument veröffentlichen und erfolgreiche CI
am exakten Registrierungscommit nachweisen. Diese noch nicht vorhandenen
konkreten Artefakte müssen vor der nativen20Probephase separat geprüft werden.
`register` und der tatsächliche Technikstart bleiben bis dahin gesperrt.
Keine automatische MECH-, Leistungs-, Setter-, UI- oder Karrierefreigabe.

# MECH-002-STARTPOLICY-TECH-V1 – unabhängiger Codereview

14.11.2026. Quellbasis `8e9a0e0`, Korrekturen `5f3d3ad` und
`54cdcbcbe556397cd6c71e38765e40590c44fcd7`. **Code und rein statische
Vorbereitung freigegeben; keine native17Probe-Freigabe vor konkretem
Input-/Seed-/Reviewgate, Veröffentlichung und exakter CI.** Dieses Dokument
gehört zum nächsten CODE-Freeze und wird danach nicht für Ergebnisse verändert.

## Enger Zweck und unveränderte Quellen

Neue technische Frage: Überträgt der vorhandene Originalprofilpfad gemeinsam
rawC90/C7A7000 statt10000 bei zehn aufgestellten Feldspielern in die tatsächlichen
Actorwerte und den Runtimecache nach Originalvorbereitung und erstem Tick?
7000→Cache70 bleibt ausdrücklich **ungetestete Transferhypothese**, kein bereits
bestätigter Befund, keine FM-UI-Prozentkalibrierung und kein Leistungseffekt.

Keine Änderung an Forschungsmodulen, Originalcodec, DLL, Originalhost, C++-Header
oder Observerbinary. Verwendet wird der separat technisch geprüfte Readonlyhost
SHA58e05…d32 mit Engine27.0.1+2503222/SHA8c697…e340. Historische Observer-/Codec-
Quellen werden gegen die exakten Gitblobs aus `39b6af5` gebunden; die neue
Masterroute wird separat eingefroren. Alte MECH-002-Blockerberichte und deren
fehlende Mainfreigabe bleiben erhalten.

Alle acht geplanten Eingaben entstehen über den unveränderten geordneten
FM27CFG1-Codec: vier D00-Zellen ×10000/7000. Default/explicit10000 müssen
byteidentisch zum bekannten D00 bleiben.7000 ändert exakt20Kind15-Werte,
Felder16/17 für die zehn Slots aus absoluten `lineup[1:]`-Records. Alle5557Record-
Positionen sowie Attribute, restliche Profile, GK/Bank/Gegner, IP/OOP, Rollen/PI,
Management und Kind62-Version bleiben gleich. Kein Kind61/Execution, neuer
Setter, Post-preparation-Schreibzugriff oder dauerhafter Clamp.

Die vollständige vorhandene Offline-Quell-/Archivprüfung unabhängig gegen
tatsächliche Original-DLL, MIT-Hostquelle und private D00/R00-/Observerbelege
rekonstruiert: Reportinhalt exakt gleich. Vier historische Highzellen und ihre
A/A-/Startcachebelege bestehen die neuen Gates. Niedrige Profile wurden dabei
ausschließlich codiert; kein neuer7000-Lauf, keine neue Seedreservierung.
Kurze gehashte private RVAfenster bestätigen eine statische Datenflussquelle,
keine tatsächlich ausgeführte Consumerkette oder Kalibrierung.

## Start-/Kontroll- und Wiederholungsgates

Genau vier extern vom Director neu reservierte Seeds, Namespace
`MECH-002-STARTPOLICY-TECH-V1/technical-v1`; der Runner reserviert keine Seeds
und verweigert historische sowie anderweitig reservierte Überschneidungen.
Jede Kontext-/Seitenzelle hat10000r0/r1 und7000r0/r1:16Vollmatches,
acht A/A-Paare, dann eine seedlose defekte Binärdatei.17Windows-sichere Keys,
ein Worker, kein zusätzlicher Loader-/Capabilityaufruf. Der unveränderte Host
hat bereits eigene Loaderbelege; diese bleiben gehashte Voraussetzung.

Alle3174Attribute und1058Profilfelder, tatsächlichen Spielerphasen,44Rollen-/
Positionszellen und748PI-Gruppen je Match müssen nach Originalvorbereitung
verifiziert sein. Prepared/erster Tick verlangen bei allen46Actors die
deklarierten Rawprofile sowie unveränderte Condition/Fatigue/Akkumulator/Abzug.
Für22Starter ist der tatsächliche Cache nötig:89=100,8a=70 oder100 entsprechend
dem deklarierten Target. Null bleibt fehlend. Identitäten und RawTF33 werden
zwischen High/Low in beiden Anfangsstages gebunden; TFnull bedeutet keine
validierte Nullfamiliarity der UI.

Jedes A/A-Paar bindet exakte Scores, Endtick/Clock, Originalteamstatistiken und
identifizierte Rohzustände aller drei Stages. Das112Byte-Fenster bleibt bewusst
vom A/A-Endpunkt ausgeschlossen. High/Low-Ergebnisse dürfen verschieden sein;
es gibt daraus keinen Effektp-Wert. Finished-Rohzustände werden erhalten, ohne
7000-Erhaltung zu fordern. Wiederholungs- und Kontrollfehler stoppen sofort beim
jeweiligen Job; keine automatische alternative Schreibmethode.

## Zwei vor Freeze korrigierte Befunde

Die erste Fassung erwartete für defekten Header den erfundenen Emissionsstage
`header`. Tatsächliche Originalsource und bereits erhaltenes privates108-Gold
belegen `scenario_rejected.stage=initial`. Der Fix verlangt genau dieses eine
Ereignis, Exit108 und kein natürliches Ende; falsche/duplizierte/missing Stages
werden abgewiesen. Der Reviewer führte das vorhandene private Gold erneut rein
lesend durch den korrigierten Auditor; kein neuer Host.

Die erste Exportfassung hätte nach einem Child-/Budgetfehler eine vorher
geschriebene `passed=true`-Summary beibehalten können. Jetzt bindet der eigene
Budgethelfer Erfolg an genau eine erfolgreiche, reconciliierte technische
Operation, alle17Reservierungen, vollständige gleiche Zeitbelastung≤180s,
unverändertes900s-Fenster und tatsächlichen Abschluss darin, nicht halted und
bekannte Bereinigung. Der Supervisor erzeugt sein exklusives Finalreceipt mit
Budgethash erst nach erfolgreicher Childabrechnung und Leasefreigabe.
Fehlende/defekte Receipts, Zeitüberschreitungen, Retry/Refund und unaufgelöste
Zustände erzwingen öffentlich `passed=false`. Unbekannte Zeiten bleiben null;
active/operations werden ohne Tokens, private Pfade oder argv ausgegeben.
Der neue Helfer ist ausdrücklich Teil von CODE.

## Ressourcen, Publikation und Freigabegrenze

Statisches Prepare importiert keinen Server und startet keinen Host. Es benötigt
die externe unveränderliche Vierseedreservierung und beide Reviewdokumente,
prüft reale Build-/Quell-/Ressourcenhashes und friert acht Inputs ein. Das ist
eine andere technische Frage als die administrativ geschlossene Staminastudie;
deren Frist/Budget bleiben unverändert geschlossen und werden nicht umetikettiert.

Erst anschließend konkrete Inputs und Seedplan unabhängig prüfen und ein
`review-gate.json` mit exaktem Inputhash, diesem Reviewhash und Observer-Ergebnis-
reviewhash erstellen. Der Runner erstellt keine eigene Freigabe. Voller
veröffentlichter Commit, erfolgreiche CI genau diesesSHA und Gitblobgleichheit
aller CODE-/Publicartefakte sind für Register und technischen Start zwingend.
Die Masterroute und CLI haben keine Mainzulassung.

Native Technik: persistentes17/0-Versuchsbudget,180s kumulierte überwachte
Technikchildzeit und900s unverlängertes UTCfenster ab technischer Operation,
zusätzlich Nachtmaster1800s/23:00UTC. Die frühere rein statische Vorbereitung
wird vom Master belastet, erzeugt aber keine innere native Operation. Ein serieller
Worker; bekannte3OS-Prozess-Kapsel,90s ohne Fortschritt,512MiB Artefaktgrenze und
20GiB Freiraum. Leseguards und erneute Hashprüfung binden Host, DLL/Ressourcen,
Fixture, Buildsource, Katalog, Konfigurationen und alle Binärdateien vor Aufrufen.

Fehlende Kernelnull-/Kapselexitbestätigung erhält Cleanupmarker und globale
Lease; bestätigte Fehlversuche erhalten Budget/Slots ohne Retry. Alle begonnenen,
fehlgeschlagenen und unbegonnenen17Plätze bleiben im Export sichtbar. Rohbytes,
Trägeridentitäten und private Warn-/Fehlertexte bleiben lokal.

Alle17gezielten Tests unabhängig bestanden, einschließlich tatsächlichem
privatem Initialstage-Gold, positivem Budgetfall und elf negativen Budget-/
Exportvarianten. Eigener zusätzlicher synthetischer17Zeilen-Export bei halted/
181s/Timeout blieb korrektfalse. Keine Saveöffnung, kein neuer FM-Host oder Seed.
Alte eingefrorene Observerquellen/-Reviews unverändert.

Freigegeben ist ausschließlich Code und statisches Prepare. Konkrete technische
Ausführung wartet auf externen Inputreview, Gate, Veröffentlichung, exakte CI
und zentrale Zulassung ohne parallelen nativen Supervisor. Nach tatsächlichem
Lauf neuer Ergebnisreview; keine automatische wissenschaftliche Main-, Consumer-,
UI-, Setter-, Karriere-, Holdout- oder Wirkungsfreigabe.

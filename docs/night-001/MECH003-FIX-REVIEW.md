# MECH-003 – unabhängige Abnahme der Ausführungsfixes

14.11.2026. Fixbasis `061576c` und
`83ce6ee71653993a5d06f433fae94487b6d7cf8c`, neue Masterquellenepoche `d3ad665`.
**Code-/Vertragsvorbereitung akzeptiert.** Echte Vorbereitung mit einem nativen
Loader erst nach veröffentlichtem exaktem Preparegate, erfolgreicher CI und
zentraler Masterzulassung. Konkrete Inputs/Seeds, Technik und Main noch nicht
ausgeführt oder dadurch freigegeben.

Die wissenschaftliche Bewertung aus [MECH003-REVIEW](MECH003-REVIEW.md) bleibt
bestehen. Die dort benannten Ausführungslücken sowie zwei zusätzliche reale
Schnittstellenfehler wurden vor jedem MECH-Start behoben.

## Konkrete Korrekturen

Die gesamte Phase läuft vor `NativeLab`-/Serverimport in der geprüften
Kernelkapsel. Damit sind der implizite Loader, Capabilities und sämtliche
Warmhostnachfahren im gleichen No-breakaway-/Kill-on-close-Job. Der Parent
verlangt bestätigten Kernelnullstand und Kapselexit mit Prozesslimit10 vor
Leasefreigabe. Unbekannte/fehlende/partielle Bereinigungsreceipts erhalten einen
dauerhaften Cleanupmarker und die globale Lease. Der Negativlauf hat zusätzlich
eine eigene3Prozess-Kapsel; Timeout kann keinen ungeschützten Enginechild hinterlassen.
Der Helfer ist Teil des Codefreeze; Budget600Child-/1200UTC und das Nachtbudget
bleiben kumulativ, ohne Retry, Seedersatz, Reset oder Zeitverlängerung.

Die tatsächlichen zusätzlichen Probes sind nun reserviert und erhalten:

| Phase | Vollmatches | weitere logische Probes | Reservierte Keys |
| --- | ---: | --- | ---: |
|prepare|0|ein Loader|1|
|technical|32|Loader, Capabilities, defekte Binärdatei|35|
|main|512|Loader, Capabilities|514|
|gesamt|544|sechs weitere Probes|550|

Inneres Reservierungsbudget36technical/514main; die fachliche32+1-Technikfallzahl
bleibt von den drei zusätzlichen technischen Metadatenslots getrennt.
Zwei technische und64Mainseeds bleiben66neue Seeds. Der Mainzeitpunkt besitzt
dadurch keine neue Mainfreigabe. Startabsicht im Hostledger ist ausdrücklich
kein erfolgreicher Loader-/Capabilityreadback; eigene Erfolgsreceipts und ihre
Hashbindung sind zusätzlich erforderlich.

## Windows-Audit tatsächlich nachvollzogen

Der Reviewer reproduzierte zunächst mit einem harmlosen echten Pythonchild,
dass CPythonWindows `subprocess.Popen` als `executable=None` und eine einzige
Windows-Commandlinezeichenfolge auditiert. Die erste Hookfassung hätte deshalb
vor dem ersten Loader mit `Path(None)` abgebrochen; ihre synthetischen Tests
hatten die falsche Argumentform angenommen. Kein echter Host wurde dafür gestartet.

Die neue Fassung benutzt `CommandLineToArgvW` mit korrektem `LocalFree` und
leitet bei fehlendem expliziten Executable den Pfad aus argv0 ab. Ein echter
harmloser Windows-Subprocesstest mit Leerzeichen, eingebetteten Anführungszeichen
und Backslashes besteht. Zusätzliche Fälle prüfen die tatsächlich erzeugte
Windowsform gegen den Hosthook. Loader-DLL, Warmmanifest/Output unter eigener
Runwurzel, Tickstep1, Cancel-ID und eigene Kapselgrammar sind eng begrenzt;
unbekannte/zusätzliche CLI-Optionen werden vor `Popen` abgewiesen.

Der vor Serverimport installierte Hook prüft Masterzulassung und schreibt
Startabsicht dauerhaft vor jedem tatsächlichen Python-Hoststart. Genau ein
Loader pro Phase, eine Capabilityprobe je Matchphase und höchstens vier
Technikwarmhosts bzw.64Mainwarmhosts. Die Limits verhindern versteckte
Wiederholungen. Die einmalige negative Kapsel und ihre Startfreigabe sind separat
gezählt, ohne als zusätzlicher Mainmatch oder neuer Seed zu gelten.

## Capabilitygate und Lebensdauer der Warmhosts

Der Fremdrunner erlaubte ursprünglich einen leeren/malformed Capabilitycache als
Legacyfallback. Die erste MECH-Fixfassung hätte dies erst nach32/512Matches
bemerkt. Jetzt erzwingt ein expliziter Vorcheck vor Jobaufbau genau eine reale
Constructorprobe aus leerem Cache; vor jedem `lab.run` folgt ein Cachevergleich.
Verlangt werden exakt
Protocol2, max_jobs1000000, Executionreset und Per-match-release=true sowie
tatsächlich aktiver counted-session-Modus. Alle späteren Constructoren verwenden
denselben geprüften Cache; Mutation oder Leerwert stoppt vor dem nächsten Block.
Erfolg wird vor dem ersten Match in einem eigenen Receipt gespeichert.

Das vorhandene `adapter_version.json` und die unveränderte Originalhostquelle
wurden rein lesend geprüft: sie deklarieren genau diese Werte. Die tatsächliche
Capabilityausgabe ist dennoch erst im zukünftigen Lauf zu belegen. Der
Negativcheck verlangt Exit108, genau ein `scenario_rejected` und kein natürliches
Ende; eine beliebige108-Abweisung reicht nicht mehr.

Quellenprüfung von `NativeLab.run` und `DesktopWarmRunner.run`: Native Futures
laufen in einem synchron verlassenen ThreadPoolExecutor-Kontext; jede Session
wartet auf Prozessende und `communicate`, bevor der Aufruf zurückkehrt. Daher
sind alle vier Warmhosts geschlossen, bevor die Negativkapsel startet. Max10
deckt zwei Steuerprozesse plus vier Paare Launcher/Enginechild; es bezeichnet
vier Engineworker. Sollte trotzdem ein Nachfahre bleiben, stoppt die äußere
Kernelkapsel die Phase und bestätigt ihre Bereinigung, statt neue Probes zu starten.

## Veröffentlichung und neuer Masterpfad

Prepare hat einen echten Hostaufruf und benötigt deshalb bereits vor Budget- und
NativeLab-Anlage ein `prepare-gate.json`: erfolgreicherCI-Head exakt des vollen
veröffentlichten Commits, identische Code-/Vertrags-/Dokumentblobs und unabhängiger
Reviewhash. Die technische Phase braucht danach konkrete veröffentlichte
Inputs/66Seeds/Registrierung; Main zusätzlich die erfolgreichen echten
Technikbelege und ihren separaten veröffentlichten Review-/CI-Commit.

Die neue Masterroute `MECH-002-STARTPOLICY-TECH-V1` ist davon unabhängig geprüft:
Prepare verlangt[], Technik die exakten17Keys in definierter Reihenfolge,
`main` wird ausdrücklich abgewiesen. Neun Mastertests und eigene Missing-/
Reihenfolge-/Main-/Prepare-Abweisungschecks bestanden, ohne Dispatcheraufruf.
Dies ist eine Routerprüfung und keine Freigabe des noch separat zu prüfenden
Startpolicy-Runners oder eines7000-Setters.

Diese neue Quellenepoche folgt der abgeschlossenen Observer-Technikserie.
Observerrekonstruktion bleibt an deren alten Gitcommit `39b6af5` gebunden;
ein neuer MECH-Freeze verwendet den jetzigen Router. Keine alten Budgets oder
Läufe werden umetikettiert. Zusätzlich prüft `published_registration` sämtliche
`research/*.py`; auch weitere gemeinsame Researchquellen müssen deshalb vor
dem neuen Freeze fertig sein und danach unverändert bleiben.

## Validierung und Restgates

Alle27MECH-Fachtests und neun Mastertests im zentralen Checkout eigenständig
bestanden, einschließlich echter Windows-Argumentform, frühem Capabilityfehler,
fehlender Bereinigung,550Slot-Abrechnung und exakter CI-/Reviewbindung.
Eigene Rohstatistikprüfung des unveränderten synthetischen Entwurfs bleibt
gültig. Reviewer:0FM-Hoststarts,0Matches,0Seedreservierungen,0Savezugriffe.

Freigegeben ist die veröffentlichbare Code-/Vertragsvorbereitung. Der Director
darf nach erfolgreicher exakter Veröffentlichung/CI/Preparegate allein den
registrierten einzelnen Prepareloader unter Master/Lease/Restbudget ausführen.
Danach konkrete Inputs/Seeds erneut unabhängig prüfen und veröffentlichen.
Technik, Main, UI-/Consumer-/Ermüdungsmediation und Karriereübertragung bleiben
bis ihren jeweiligen echten Gates gesperrt; keine automatische Folgeserie.

## Letzter Masterguard vor Preparefreeze

Den nach `d3ad665` ergänzten `selected_runner.is_file()`-Guard separat gelesen
und unabhängig geprüft. Er liegt nach Routen-/Phasen-/Key-/Argumentprüfung,
aber **vor** `NightBudget`-Anlage, Budgetreservierung und Childstart; auch der
interne `admitted`-Pfad wird vor Token-/Zulassungsweitergabe abgewiesen, wenn
der ausgewählte Runner noch fehlt. Damit verbraucht eine lediglich vorgemerkte
Zukunftsroute kein globales Versuchsbudget. Keine Frist oder bestehende
Reservierung wird dadurch zurückgesetzt oder verändert.

Alle zehn aktuellen Mastertests bestanden. Zusätzliche eigene Prüfungen mit
harmloser temporärer Checkoutstruktur bestätigen für `run` **und** `admitted`:
fehlender Runner führt zur erwarteten Abweisung, `NightBudget`, Admission und
`subprocess.run` werden jeweils nicht aufgerufen.0Hosts,0Seeds,0Savezugriffe.
Geprüfter endgültiger Routerhash, CRLF→LF normalisiert:
`63bbf08ce8d19474bba956140deca44ab43cef70f7c719cec229090d10148791`.

Die obige enge Preparefreigabe gilt auch mit diesem Guard. Vor tatsächlicher
Vorbereitung sind genau diese Routerquelle und die endgültige Fassung dieses
Reviewdokuments gemeinsam zu veröffentlichen und an erfolgreiche exakte CI
sowie das Preparegate zu binden. Diese Ergänzung erfolgte vor jedem MECH-Prepare;
keine eingefrorene Observerquelle oder dessen alter Reviewtext wurde verändert.

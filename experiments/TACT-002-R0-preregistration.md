# TACT-002-R0 – Vorregistrierung des kleinen ST/AMC-Rollenpiloten

Entwurf vor nativer Vorbereitung/Vollmatches,14.11.2026. Autorisierung gilt nur
für die kleine512-Hauptmatch-Variante nach allen technischen Gates. Keine
D15-Optimierung,keine Holdouts,keine automatische1024-Erweiterung. Der Director
führt alle nativen Prozesse zentral aus; dieser Implementierungsabschnitt startet0.

## Frage, Hypothese und feste Eingaben

Ändert IP-DeepLyingForward statt CentreForward die mittlere xGD unserer eigenen
IP-4-2-3-1,gemittelt über die zwei vorab eingefrorenen AMC-Rollen?
Ein zweiseitiger Primärtestα0,05,praktische Screeninggröße0,30xGD,
gewünschte volle95-%-KI-Breite≤0,50. Ein Rollenvarianzpilot,keine garantierte
90-%-Bestätigung und keine Auswahl einer optimalen Taktik.

Vollständiges2×2,unverrückbare Armreihenfolge:

| Arm | IP-ST | IP-AMC | ST/AMC-Stufen |
|---|---|---|---|
|R00|CentreForward|AttackingMidfielder|−1/−1|
|R10|DeepLyingForward|AttackingMidfielder|+1/−1|
|R01|CentreForward|SecondStriker|−1/+1|
|R11|DeepLyingForward|SecondStriker|+1/+1|

Funktionale Roleflags:CF2048,DLF1024,AttackingMidfielder512,
SecondStriker2199023255552. Alle `Duty=0`; `rules=game`.
IP-Grundordnung und OOP4-4-1-1 bleiben unverändert. Sämtliche anderen Rollen,
17expliziten PI-Gruppen je Spieler/Phase,Targets,Teaminstruktionen,Mentalität,
Standards,Taker,Lineup,69Attribute,Profile und Management werden von D00übernommen.
PI0 heißt keine zusätzliche explizite Auswahl; rolleninterne Vorgaben sind
Bestandteil der Rollenintervention und werden nicht als abwesend behauptet.

Zwei bisherige Discoverygegner `high_press`/`deep_block`,gleiche synthetische
23-Spieler-Kaderstärke. Zwei feste native Fixtureseiten0/1,nicht als isolierter
Heimvorteil interpretiert. Seitenmittel im Seed und Gegnergewicht je½.
Keine Änderung an `holdout_midblock`/`holdout_direct_counter`,keine Öffnung
gehaltener Messdaten oder ihrer Nutzung. Keine Karriere-PKM.

R00muss **binäridentisch** zu D00aus P1B sein,für alle vier Gegner/Seitenzellen.
Zulässiger Binärdiff der anderen Arme ausschließlich native kind4-Rollenrecords
für getestetes Team,IP-ST/AMC. Keine Duty-/PI-/Profil-/Phasen-/Managementänderung.
Normalisierung darf außer den zwei deklarierten Role-IDs keine JSON-Änderung
verursachen. Vollständiges Rollenmanifest beider Teams/Phasen und gehashte
Binärdiffs werden im öffentlichen Datenarchiv veröffentlicht,keine privaten IDs.

## Stichprobe, neue Seeds und Randomisierung

**32neue unabhängige Seeds je Gegner**,64vollständige Seedblöcke.
Jeder Seed bindet vier Arme×zwei Seiten=achtHauptmatches;gesamt**512**.
Neue Namespaces `TACT-002-R0/main-v1`/`technical-v1`,keine bisherigen,
fehlgeschlagenen oder anderweitig reservierten Seeds. Zentrale gemeinsame
Registry und exklusive `.allocation.lock`; keine parallelen Reservierungen.

Separat3neue technische Seeds: einer pro Gegner und ein reservierter unbenutzter
Negativseed.16vollständige Eingabezellen jeweils zweimal=**32Vollmatches**,
16exakteA/A-Paare. Eine absichtlich ungültige eigene Binäreingabe ohne wirksamen
Seed muss Exit108liefern. Insgesamt**33technische Versuchsplätze**,67reservierte
Seeds. Der Negativseed bleibt verbraucht/reserviert,auch wenn er nicht wirksam wurde.
Offline zusätzlich unbekannteRolle,falschePhase,ungültigePI für jede feste
Gegner-/Seitenbaseline ablehnen. Diese12Schema-Probes sind keine nativen Matches.

Kanonische SHA256-Jobreihenfolge aus `schedule()`,danach Python
`random.Random(2026111406).shuffle`; Technik2026111407. Dies sind Scheduler-
RNGs,keine zusätzlichen Spielseeds. Batches≤64,kein Retry,kein Effekt-Zwischenstopp.
Fehler stoppen. Alle begonnenen,fehlgeschlagenen und unbegonnenen Jobs erhalten;
keine Ersatzseeds,Nullersetzung oder Ergebnisexklusion. Bei unvollständigem
Block nur technischer Status,keine partielle Leistungsanalyse/Rangliste.

## Native Gates, Versionsbindung und persistente Budgets

Nur der VALID-002/P1B-freigegebene aktuelle Build27.0.1+2503222 mit TacticsLab
v1114.6,Commit91f2eba57fac0b7fbd3dff616056907e3ce461be und Adapter
fm27_desktop_8c6971ce_adapter_v1. Engine-/Host-/Fixture-/Ressourcenhashes,
Katalog und sämtliche Runtime-Pythonquellen werden tatsächlich abgeglichen und
im Manifest/Inputs festgeschrieben. Drift stoppt; keine automatische Migration.

Vorregistrierung,Code,konkreter JSON-Vertrag,Eingabe-/Analysehashes und Seedplan
vor Vollmatches auf origin/main veröffentlichen. Der technische Gatebericht
muss vor dem ersten Hauptmatch ebenfalls gepusht und unverändert sein.
Director prüft zugehörige CI. Keine wissenschaftliche Ausführung bei Gatefehler.

Jedes Vollmatch benötigt Nach-Vorbereitungsreadbacks sämtlicher kodierter
Records,effektiven Seed und natürliche Beendigung. `NativeLab`prüft alle69
Attribute und Slot-/Position-/Rollen-/Duty-/Profilbindung; ergänzender Audit
prüft beide Teams,alle44Phasenzellen,alle748expliziten PI-Gruppen und Targets,
Teaminstruktionen und getestete ST/AMC64bit-Flags. Rolleninterne Verhaltensvorgaben
werden nicht mit expliziten PI verwechselt. Negative natürliche Resultate sind
keine Eingabefehler. Stats: endliche nichtnegative xG,SOT≤shots,
completed_passes≤passes,Besitz0..1/Summe1,ganzzahlige Tore≥0,natürlich0<tick<47996.
A/Averlangt gleiche Seeds/Setups,Scores,Endticks und vollständige Teamstatistik.

Ein zentraler Supervisor hält `NativeLease` am gemeinsamen
`local/global-native` für den **gesamten** `DeadlineBudget.run`-Childlauf,
auch Vorbereitung und negative Probes. Child prüft Leasebesitzer/Experiment/
Workerdeklaration gegen seinen authentifizierten lebenden Supervisor.
Nur zentraler Checkout darf nativ starten,keine Worktrees. Leasecrashdatei
bleibt blockierend und wird nie automatisch übernommen/gelöscht.

Dauerhafte Gesamtgrenzen vor erster nativer Vorbereitung:
512Hauptversuche,33technische Versuche,**900s kumulierte beaufsichtigte
Child-Wall-Time**,**1800s unverrückbares UTC-Zeitfenster** einschließlich
Publikationspausen,maximal4Engine-Worker,90s ohne Fortschritt.
2GiBprivate Rohartefakte/20GiBfreie Diskreserve. Phasen teilen dasselbe Budget;
kein Reset durch Neustart oder Retry. Supervisor beendet Prozessbaum bei Frist.
Keine konkurrierende native VALID-/SET-Ausführung.

## Eingefrorene Auswertung

ArmreihenfolgeR00/R10/R01/R11:

- Primär ST auf xGD: **(−½,+½,−½,+½)**,DLFminusCF,marginal über AMC.
- AMC auf xGD: (−½,−½,+½,+½).
- Physische ST×AMC-DoD: **(+1,−1,−1,+1)**,kein Faktor2-/4-Fehler.

Seitenmittel innerhalb eines vollständigen Seeds,dann Kontexte je½.
SE²=¼(s_H²/32+s_D²/32),Welch-Satterthwaite-df,zweiseitige95-%-t-KI/p.
Zusätzlich20000stratifizierte vollständige Seedblock-Bootstrapziehungen;
RNGerste8Byteslittle-endianSHA256(`TACT-002-R0/bootstrap-v1`).
Rohscores bleiben erhalten,Punkte3/1/0aus tatsächlichem Endstand.

Genau sieben sekundäre Kontrast×Endpunkt-Paare,eine **Holm7-Familie**:
AMC×xGD,ST×AMC-DoD×xGD,ST×Punkte,ST×GF,ST×GA,ST×xGF,ST×xGA.
Kein zusätzlicher Punkte-DoD. Marginale95-%-KI bleiben marginal; sekundäre
Ergebnisse ersetzen keinen Primärnachweis. Native Schüsse/SOT/Besitz deskriptiv.
Alle vier Armmittel je Gegner mit Punkten/Toren/Chancen,Kontext-SDs,Seiten-
Kovarianzen,Kontrastkovarianzen und Leave-one-seed-out ohne Ausschlüsse berichten.

Die Rollen-Kontrast-SD ist unbekannt. Bei rein angenommener gleicher SD0,8/1,2/1,8
liefert diese kleine Variante volle95-%-Breiten0,400/0,600/0,900 und Power für
0,30etwa84/50/26%. Keine tatsächliche Rollenvarianz aus P1B ableiten.
Nach Pilot neue Bestätigungsfallzahlen für feste0,20/0,30xGD,90%Power gegen Null,
beobachtete SDs und gemeinsame95-%-Normalmodell-SD-Obergrenzen (jede97,5-%-
χ²-Grenze,df31) angeben. Nichtzentrale Welch-t-Näherung; neue n je Kontext,
64hier beobachtete Blöcke nicht wiederverwenden,Kosten16nMatches im selben2×2.
Keine garantierte Power für andere Kontexte oder die Sekundär-/Interaktionsfamilie.

## Interpretation, Archiv und Abschluss

Keine optimale Rolle/Taktik oder universelle Positionsgewichtung behaupten.
Es wird **kein Kandidat ausgewählt**. Positive Rolle im marginalen Kontext
bestätigt keine ganze Taktik und keine Karriereübertragbarkeit. Signifikanz
gegen0belegt keine Mindestverbesserung0,30; Nichtsignifikanz keine Äquivalenz.
Vorbereitung/Technik/Hauptserie getrennt abbrechen und vollständig abrechnen.

Historisches Analyse-/Daten-/Experiment-/Vertrags-/Programmarchiv wird gegen
Ausgangscommit790727f3ef830209baf55f2dde36b6dca1299685gehasht und unverändert
behalten. Nur eingefrorene Whitelist-JSONL,Provenienz,negative Kontrollen,
Job-/Budget-/Leaseabrechnung,Analyse/Unsicherheit veröffentlichen. DLL/EXE/PKM/
FMF/private Spieleridentitäten/Dumps/Binärinputs bleiben privat.
Tests,unabhängiger Reviewer und Verifier,Diff/Secrets und CI zentral prüfen;
Director committet/pusht. **Nach512Hauptmatches stoppen**,keine1024Erweiterung,
Holdoutstudie,Karrierefortschreibung oder weitere Optimierungsrunde.

[Runner](../analysis/run_tact002r0.py) · [Analyse](../analysis/analyse_tact002r0.py) ·
[Exporter](../analysis/export_tact002r0.py) · [unabhängiger Verifier](../analysis/verify_tact002r0.py).
Der konkrete [JSON-Vertrag](../research/specs/TACT-002-R0.json) und die Daten unter
`data/tact-002-r0/` werden erst durch zentrale budgetierte Vorbereitung erzeugt.

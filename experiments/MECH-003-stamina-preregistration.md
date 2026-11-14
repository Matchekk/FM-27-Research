# MECH-003-STAMINA-R0: Stamina × Pressing

Status 2026-11-14: **Vorbereitungsentwurf, keine native Freigabe, keine neuen
Matches oder Seedreservierungen durch den Fachagenten.** Ausführung allein durch
den Research Director nach separatem Review, Veröffentlichung, erfolgreicher CI
und bestandener technischer Prüfreihe. Dieser Auftrag erweitert keine alte Studie.

## Frage, Kontext und Eingriffe

Verbessert Stamina52 raw80 gegenüber raw40 das mittlere xGD, gemittelt über zwei
Pressingstufen, innerhalb des unveränderten synthetischen D00-Kontexts?
Die offizielle Enginebeschreibung motiviert die Frage; sie belegt weder die
Wirksamkeit unseres Eingriffs noch einen quantitativen Effekt
([Quellenaudit](../docs/night-001/EVIDENCE.md)).

Alle vier Zellen verwenden D00 mit identischer IP-4-2-3-1 und OOP-4-4-1-1,
Rollen, PI, Positionsratings, Profilfeldern, Start-/Matchmanagementpolitik und
Gegnern. Nur zehn getestete Startfeldspieler (`lineup[1:]`, nicht die ersten zehn
Kaderslots) erhalten Stamina-Index52 raw40 beziehungsweise raw80. Ihre übrigen
53 Fähigkeitswerte bleiben raw60; originale Positions-/Metawerte bleiben erhalten.
Torwart, Bank, Gegner und inaktive serialisierte Auswärtsslots bleiben unverändert.
Es gibt keinen Vergleich mit der ursprünglichen raw60-Stamina und keine
kalibrierte FM-Anzeigeskala. Regeln: `game`, ausschließlich gebündeltes Fixture.

| Arm | Stamina52 raw | TriggerPress Gruppe10 | Native Bit |
| --- | ---: | --- | ---: |
| R00 | 40 | Standard, ID1313689463 | 0 |
| R10 | 80 | Standard, ID1313689463 | 0 |
| R01 | 40 | MoreOften, ID2000905329 | 66 |
| R11 | 80 | MoreOften, ID2000905329 | 66 |

Katalogsemantik und beide Bits müssen erneut nativ geprüft werden. Gegenüber den
ursprünglichen D00-Binäreingaben sind exakt zehn Attributrecords und bei MoreOften
zusätzlich ein Instruktionsrecord erlaubt. Kein Observer, permanenter Clamp,
experimenteller Execution-Pfad, Gegnerpool oder zusätzlicher Eingriff.

## Stichprobe und neue Seeds

Zwei bereits bekannte Discoverykontexte `high_press` und `deep_block`, jeweils
Gewicht1/2; beide Teamseiten jeweils Gewicht1/2 innerhalb desselben Seeds. Je32 neue
Seeds pro Kontext:64 unabhängige Seedblöcke, acht Matches je Block, **512 Hauptmatches**.
Dieselben Seeds innerhalb aller vier Arme und beider Seiten kontrollieren
Startzufall, garantieren jedoch keine gleichen Ereignisverläufe.

Separat32 technische Vollmatches: alle16 Kontext×Seite×Arm-Zellen zweimal,
16 exakte A/A-Paare. Zwei zusätzliche neue technische Seeds, einer pro Kontext;
ein ungültiger Binärinput als zusätzlicher Prozessversuch, erwarteter Exit108 ohne
natürlich beendetes Match. Insgesamt66 neue Seeds und545 Versuchsplätze.
Namespace `MECH-003-STAMINA-R0`. Nur der zentrale Preparepfad darf atomar unter
Registrylock reservieren. Alle früheren, technischen, reservierten und lokalen
Programmseeds werden ausgeschlossen und als gehashte Ausschlussmenge eingefroren.
Keine Holdouts, Seedersatz, Wiederholung, nachträgliche Exklusion oder Erweiterung.

## Vorregistrierte Auswertung

Ein zweiseitiger Primärtest: marginaler Staminaeffekt auf xGD (xGF−xGA), raw80−40.
Armanordnung `[R00,R10,R01,R11]`, Koeffizienten `[-.5,+.5,-.5,+.5]`.
Die vier Armmessungen werden zuerst innerhalb Seite/Seed kontrastiert, dann beide
Seiten gemittelt. Kontextmittel werden gleich gewichtet.64 Blöcke sind die
Analyseeinheiten;512 Einzelmatches werden nicht als unabhängige Replikate behandelt.

Gepaarter Welch-Kontextschätzer mit Satterthwaite-Freiheitsgraden, zweiseitigem
95-%-KI und p-Wert; zusätzlich20.000 stratifizierte Bootstrapziehungen vollständiger
Seedblöcke. Bootstrapseed ist deterministisch aus dem Studiennamespace abgeleitet.
Kontext-SD, Seitendurchschnitte/-SD/-Kovarianz und Leave-one-seed-out-Spannweite
werden berichtet. Bootstrapintervalle sind deskriptive Unsicherheitsbelege,
keine zusätzlichen unabhängigen Tests.

Genau eine eingefrorene **Holm7-Sekundärfamilie**:

1. Stamina: tatsächliche Punkte pro Match.
2. Stamina: erzielte Tore.
3. Stamina: Gegentore.
4. Stamina: xGF.
5. Stamina: xGA.
6. Pressing: xGD, Koeffizienten `[-.5,-.5,+.5,+.5]`.
7. Stamina×Pressing: xGD, physische Differenz-von-Differenzen `[+1,-1,-1,+1]`.

Die Primärhypothese gehört nicht zu dieser siebenfachen Sekundärfamilie. Kontext-
und Seitenzerlegungen sind explorativ, ohne zusätzliche unbereinigte Signifikanz-
oder Gewinnerbehauptungen. Alle Effekte sind totale Matcheffekte. Weder Ermüdungs-
mediation noch Tactical-Effectiveness-Wirkmechanismus sind identifiziert.

Kleinste praktische Größenordnung:0,30xGD; gewünschte volle Primär-KI-Breite≤0,50.
Die neue Kontrast-SD ist unbekannt; dies ist ein Präzisionspilot ohne90-%-Powergarantie.
Nach vollständiger Serie werden neue Bestätigungsfallzahlen für0,20/0,30xGD bei
90% Power mit nichtzentralem Welch-Modell berechnet: einmal beobachtete Kontext-SD,
einmal simultane95-%-SD-Obergrenzen unter Normalmodell (je97,5%,df31).
Diese bedingte Planung löst keine weitere Serie aus. Gleichallokation mit n Seeds
je Kontext kostet2n unabhängige Blöcke und16n native Matches.

## Identität, Audits und Stopregeln

Keine angenommene aktuelle Buildidentität: der zentrale Preparepfad muss die
tatsächliche DLL/Host/Fixture/Ressourcen-/Tool-/Runtimeidentität gegen VALID-002 und
P1B prüfen und im konkreten `contract.json`/`inputs.json` einfrieren. Originalhost
SHA256 `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e`;
NativeLab bleibt unverändert. Der neue passive Observer ist ausdrücklich kein
freigegebener Warmworker für diese Studie.

Vor Hauptbeginn: veröffentlichte Vorregistrierung, Vertrag, Code,66er-Seedplan und
vollständige technische Belege; erfolgreiche CI am exakten Freigabecommit und
separater Review mit versioniertem Dokument/Hash. Codefreeze umfasst ausdrücklich
`research/night_control.py` und den zentralen `analysis/night_supervise.py`.
NativeLab prüft46 aktive Spieleridentitäten und alle69 Attributfelder
(3174 Werte),23 Profilfelder je Spieler (1058), tatsächliche22 IP/OOP-Spielerbindungen;
der eigene Audit zusätzlich44 Rollen-/Positions-/PI-Zellen und748 PI-Gruppen,
beide Team-Instruktionssätze sowie exakt zehn Staminadosen und Pressingbit.
Seed, Setup, Startreceipt und natürliches Matchende müssen stimmen.
Technik:16 A/A-Paare exakt in Ergebnis, Endtick, Statistik, Setup und Seed;
acht low/high-Paare mit je zehn tatsächlichen raw40/80-Readbacks; ungültige
Stamina0/101/bool und unbekannte Pressing-ID müssen offline abgewiesen werden.

Bei erstem Identitäts-, Input-, Seed-, Audit-, Prozess- oder Budgetfehler stoppen.
Alle begonnenen, fehlgeschlagenen und unbegonnenen Jobs erhalten. Kein stilles
Nullsetzen. Bei unvollständigen Hauptblöcken ausschließlich technischen Status
veröffentlichen, keine wissenschaftlichen Effekte. Rohlogs/Inputdumps/Spielmaterial
bleiben privat; öffentliche JSONL enthalten nur erlaubte Messungen und Hashprovenienz.

## Ressourcen und exklusive Ausführung

Ein zentraler Supervisor mit globaler NativeLease, maximal vier Engineworker,
90 Sekunden ohne Workerfortschritt. Inneres unveränderliches Budget:600 Sekunden
gesamte überwachte Child-Walltime einschließlich Vorbereitung/Audits und höchstens
1200 Sekunden ab erstem Studienstart auf UTC-Uhr (Publikationspausen zählen mit).
Maximal33 technische Prozessslots und512 Hauptmatchslots; maximal2GiB private
Artefakte, mindestens20GiB freier Datenträger. Zusätzlich gilt der NIGHT-001-Master:
1800 Childsekunden und harte Deadline2026-11-14T23:00:00Z sowie dessen globale Caps.
Neustart, Retry oder innerer Supervisorwechsel verlängert keines dieser Budgets.

Nur der Director startet über `analysis/night_supervise.py`. Der innere CLI-Parent
prüft Mastertoken, lebenden Parent, Phase und vollständige echte Jobkeys vor
Budgetanlage; der Child prüft erneut vor NativeLab. Phasekeys: Prepare[], Technik33,
Hauptserie512; globale Keys tragen das Studiennamespace. Worktrees dürfen keinen
Prepare-/Register-/Nativepfad betreten. Retained Lease-/Crashbelege sperren erneute
Ausführung. Ausführung bleibt blockiert, solange irgendeines dieser Gates offen ist.

## Artefakte und Interpretation

[Vertragsentwurf](../data/mech-003-stamina/contract-draft.json),
[Offline-Intentionsprobe](../data/mech-003-stamina/offline-preparation.json),
[Implementierungsstatus](../docs/night-001/STAMINA.md).
Später ausschließlich zentral erzeugte `contract.json`, `manifest.json`,
`main.jsonl`, `technical.jsonl`, `job-accounting.jsonl`, `effects.json` und
`block-contrasts.jsonl`; der öffentliche Verifier rekonstruiert alle Effekte.
Aktueller Entwurf ist keine technische Abnahme und enthält keine Messergebnisse.
Kein globales Attributranking, keine optimale Taktik, keine Karriereübertragbarkeit,
keine Holdoutbestätigung und keine automatische Folgestudie.

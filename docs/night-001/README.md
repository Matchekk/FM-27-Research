# NIGHT-001 – Forschung bis 00:00CET

Fortsetzung nach abgeschlossenem Runde3-Auftrag aufgrund neuer ausdrücklicher
Nutzerautorisierung. [Programmvertrag](../../experiments/NIGHT-001-program.md).
Deadline14.11.2026 23:00UTC/15.11.2026 00:00CET;keine alten Studienbudgets,
Seeds oder Holdouts wiederverwenden.

Drei parallele Spezialisten prüfen externe Evidenz,die rein lesende Testkarriere
und einen getrennten passiven Engine-Observer. Die aktuelle Arbeit erteilt keine
MECH-/Karrierehauptserienfreigabe. Native Versuche werden ausschließlich zentral
mit konkreter Vorregistrierung,neuen Seeds,persistenten Budgets und unabhängiger
Abnahme ausgeführt. Gemeinsamer Mitternachts-/1800s-Childbudgetbaustein vorhanden;
noch keine neue native Operation in diesem Programm gestartet.

Computer Use erkannte das FM27-Fenster,jedoch scheiterten beide Bildaufnahmen.
Deshalb bisher keine UI-Eingaben oder Kalenderadvances. Die ausdrücklich benannte
Testdatei existiert;die aktive ungespeicherte Karriere ist damit nicht verifiziert.
Spieldateien und private Identitäten werden nicht veröffentlicht.

Getrennte Spezialberichte und reale Messergebnisse folgen erst nach Prüfung.

## Geprüfter Zwischenstand 19:21CET

Die [Quellenrecherche](EVIDENCE.md) trennt öffentliche Empfehlungen von
reproduzierbaren Experimenten. Die aktuellen FM-Arena-Einträge ersetzen weder
eine native Eingabeprüfung noch unabhängige Replikate unseres Versuchs.
[Karriere-R0](CAREER.md) scheiterte an der exakten Buildzulassung. Für zwei neue
isolierte Readerpfade liegen [Verträge](CAREER-R1.md) und ein
[unabhängiger Quellenreview](CAREER-R1-REVIEW.md) vor. Noch kein R1/R2-Lesepass.
Der zusätzliche zentrale Pfadschutz ist implementiert, die Sourceverträge wurden
danach ohne Savezugriff neu erzeugt. Veröffentlichung und exakte erfolgreiche CI
sind vor jedem der zwei getrennten Lesepässe weiterhin zwingend.

200 Repositorytests, fünf historische Analysetests und beide Archivprüfungen
bestanden:340 NIGHT-Basisdateien sowie272 Round3-Basisdateien unverändert.
Eine neue Accessibility-Abfrage konnte nur das FM-Fenster als Pane lesen;
Karriere, Spieltag und Bildinhalt bleiben unverifiziert. Keine UI-Eingaben.

Observer- und Staminaausführung bleiben wegen noch zu prüfender
Prozessbaumbegrenzung gesperrt. Der unabhängige Review entdeckte außerdem
zusätzliche Loader-/Capabilitiesaufrufe der Warmruntime; diese müssen vor einer
Staminafreigabe ausdrücklich in den Zählern stehen. Weiterhin null neue native
NIGHT-Starts und keine reservierten neuen Simulationsseeds.

## Karrierezwischenstand nach erfolgreicher CI2172b76

Die zwei getrennten, vorab freigegebenen Lesepässe wurden einmalig ausgeführt:
R1 in13,985s, R2 in14,453s, jeweils ein Decoder unter3GiB/180s.
9der24Probeplätze beobachtet,2gescheitert,13unbegonnen. Beide erkennen
konsistent77 Kaderrecords; R2 erschließt außerdem vier gespeicherte
Trainingskalender. Ein Trainingsheader- beziehungsweise Taktikmarkerfehler
stoppt die jeweilige Folge. Keine Retries oder Karrierefortschreibung.
[Reale Ergebnisse und Grenzen](CAREER-R1-RESULTS.md),
[unabhängige Rekonstruktion aus privaten Ledgers](CAREER-RESULTS-REVIEW.md).

Der zusätzliche Offlineaudit zeigt:2.011von3.255 gespeicherten Kalender-Slots
haben ein Label im eingefrorenen Readerenum;1.244noch keines. Kalender enthalten
auch Zukunftswochen. Damit fehlt weiterhin der Nenner tatsächlich absolvierter
Einheiten und individueller Teilnahme; keine Trainingswirkung ableitbar.
204Repositorytests plus fünf historische Analysetests bestehen lokal.

## VALID-005 abgeschlossen

Die separat vorregistrierte passive Prüfung ist mit16Vollmatches,2Loaderchecks
und2erwartetenNegativabweisungen erfolgreich. Vier exakte Viermodusgruppen,
vollständige Eingabe-/Stagebelege und20bestätigteProzessbereinigungen;
0Ausfälle/Retry/Holdouts. [Ergebnisse](OBSERVER-RESULTS.md) und
[unabhängige Rekonstruktion](OBSERVER-RESULTS-REVIEW.md).
Das globale Nachtbudget steht bei60,5217007/1800Childsekunden.

Neue Erkenntnis ist die Trennung statischer Profilfelder von veränderlichen
Runtimequellen. Der aktuelle Recorder erlaubt keine UI-/Consumer-/Setter- oder
Karrierefreigabe. Eine neue Startpolicyroute ist ausschließlich technisch;
Main ist dort strukturell gesperrt. Der Staminaentwurf hat Windows-/Capability-
und Prozessgates im [Fixreview](MECH003-FIX-REVIEW.md) bestanden; seine native
Vorbereitung und Studienphasen sind noch nicht ausgeführt.

## MECH-003: Technik bestanden, Main aus Ressourcengründen unbegonnen

32technische Vollmatches/16exakteA/A-Paare, insgesamt2Loaderchecks,
1Capabilitycheck und1erwarteteNegativabweisung vollständig geprüft.
Der512erHauptlauf samt2CLI-Probes blieb vor seiner Zulassung stehen:
Review-/Publikations-CI war bis zum laufzeitbasierten Cutoff nicht vollständig.
Die feste Frist wurde eingehalten und das eigene Budget terminal geschlossen.
[Ergebnisbericht](STAMINA-TECH-RESULTS.md),
[unabhängiger Stopreview](MECH003-STOP-REVIEW.md).
Keine Stamina-Leistungsaussage;550Plätze vollständig abgerechnet.
Der globale Nachtstand beträgt101,2047395/1800Childsekunden.

## Vorbereitete nächste enge Prüfungen

MECH-002-STARTPOLICY-TECH-V1 ist rein statisch vorbereitet:8Eingaben,
4neueSeeds,17geplanteProbes (16Full+1Negativ),1Worker,180/900s.
[Konkreter Inputreview](STARTPOLICY-002-INPUTS-REVIEW.md) und finale
[Codeprüfung](STARTPOLICY-002-REVIEW.md) bestanden. Der7000→Cache70-Transfer ist
noch ungetestet. Keine Mainroute oder automatische weitere Serie.
Globale Zeitladung nach dieser inerten Vorbereitung112,1350788/1800s.

Die separate [R3-Parserdiagnose](CAREER-R3-RUNNER.md) hat ihren
[finalen Codereview](CAREER-R3-RUNNER-REVIEW.md) bestanden. Einmaliger tatsächlicher
Lesepass bleibt bis exakter öffentlicher CI und Director-Proceed gesperrt.
Keine Kalender-/Replay-/Trainingsfreigabe. Alle bisherigen Savebytes und
Forschungsarchive bleiben unverändert.

## Geprüfter Stand 21:36 CET

Die ursprüngliche Startpolicy hat ihre separate technische Prüfung bestanden:
16 vollständige Matches, acht exakte A/A-Paare und eine erwartete
Negativabweisung. Das gemeinsame Rohpaket C90/C7A7000 erreicht die beiden
Actorfelder und Cache8A70 nach Originalvorbereitung und erstem Fortschritt.
Keine UI-Prozentkalibrierung oder Leistungswirkung wird daraus abgeleitet.
[Ergebnisse](STARTPOLICY-002-RESULTS.md),
[unabhängiger Rohreview](STARTPOLICY-002-RESULTS-REVIEW.md) und
[öffentliche reproduzierbare Prüfung](STARTPOLICY-002-PUBLIC-REVIEW.md).
Global stehen 170,4746041 von 1800 Childsekunden zu Buche; bisher 64 technische
Vollmatches und keine wissenschaftlichen Hauptmatches im Nachtprogramm.

Die einmalige [R3-Karrierediagnose](CAREER-R3-RESULTS.md) grenzt den erhaltenen
Taktikmarkerfehler ein, repariert den Parser aber nicht. Ein Decoder, 13,922s,
vier beobachtete und eine gescheiterte Stufe; der Save bleibt unverändert.
[Unabhängiger Review](CAREER-R3-RESULTS-REVIEW.md).
Karrierefortschreibung, Replay und Trainingswirkung bleiben gesperrt.

Ein eigener [Schärfe×Pressing-Entwurf](SHARPNESS-PLAN.md) wird parallel geprüft.
Er ist eine neue Studie mit eigener Vorregistrierung, neuen Seeds und
eigenständigen Technik-, Publikations- und Budgetgates. Keine Übernahme der
geschlossenen Stamina-Studie und keine Freigabe durch diesen Zwischenstand.

## Schärfe-Pilot: eigene Technik bestanden

Vorregistrierung und545 Jobplätze sind nach konkretem Inputreview unter
`f17f0b4` veröffentlicht; CI43641170744 bestand vor dem ersten Aufruf.
Die [eigene Technikreihe](SHARPNESS-TECH-RESULTS.md) ist mit32 Vollmatches,
16 exakten A/A-Paaren und einer erwarteten Negativabweisung vollständig.
Alle Eingabe-, Seed-, Start-/Erstschritt- und Bereinigungsgates bestanden;
61,9805068/900 eigene Childsekunden,268,9756700/1800 global.
Damit96 technische Vollmatches und weiterhin0 wissenschaftliche Hauptmatches
in NIGHT-001. Die strengere eigene Frist endet23:11:09CET; die globale Nachtfrist
bleibt00:00CET. Hauptlauf bis unabhängigem Technikreview und dessen erfolgreicher
Veröffentlichungs-CI gesperrt. Keine UI-, Consumer- oder Karrierefreigabe.

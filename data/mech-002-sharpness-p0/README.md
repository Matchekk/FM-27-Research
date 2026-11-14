# MECH-002-SHARPNESS-P0: abgeschlossener Seedpilot

512/512 gültige Hauptmatches,64 unabhängige Blöcke. Der marginale Effekt des
gemeinsamen originalen Rohpakets10000 minus7000 beträgt+0,477xGD,
95-%-KI[+0,322;+0,632]; tatsächliche Punkte+0,441,
95-%-KI[+0,242;+0,641],Holm7-p=0,000236. Alle Rohbelege und acht Kontraste
sind unabhängig nachgerechnet. Nur der eingefrorene synthetische Testkontext;
keine kalibrierte UI-Skala oder Karriere-/Trainingsbestätigung.

[Ergebnisbericht](../../experiments/MECH-002-sharpness-results.md) ·
[unabhängiger Review](../../docs/night-001/SHARPNESS-RESULTS-REVIEW.md) ·
[512 Messzeilen](main.jsonl) · [Effekte](effects.json) ·
[545er-Abrechnung](complete-job-accounting.jsonl) · [Grafik](contrast-intervals.svg).
545 geplante Jobs vollständig erledigt:544 Vollmatches und eine erwartete
Negativabweisung;0 unerwartete Ausfälle/Retry/Ersatz/Unbegonnene.
560,5738462/900 eigene Childsekunden, keine NativeLease/Pendingmarker.
Der Pilot ist beendet; keine weitere Serie oder Computerbedienung.

## Erhaltener Verlauf der Vorbereitung

Stand 14.11.2026,22:01CET: Das separate TECH17-Transfergate ist tatsächlich
bestanden und [unabhängig freigegeben](../mech-002-startpolicy-tech/release-gate.json).
Die geprüfte neue Codegeneration `95d94a4e674a13eea543b64677f7c621c52e871a`
hat [CI43640107860](https://github.com/Matchekk/FM-27-Research/actions/runs/43640107860)
bestanden. Inerte Vorbereitung erstellt16 gehashte Eingabebinaries privat und
den konkreten [Vertrag](contract.json), [Inputbeleg](inputs.json) und
[Seedplan](seed-plan.json) öffentlich.64 neue Main- und vier neue Technikseeds
sind zentral reserviert;2528 frühere/reservierte Werte ausgeschlossen.
Keine Engine wurde dabei gestartet; das eigene3600s-Fenster ist noch ungeöffnet.
Konkreter Inputreview, Registrierung und eigene Technikfreigabe stehen noch aus.

## Registrierung vor dem ersten neuen Engineaufruf

Der [konkrete Inputreview](../../docs/night-001/SHARPNESS-REVIEW.md) ist bestanden.
Veröffentlichung `e1de6d0a666987a72dcdd2113eedb5f45fb51e77` samt
[CI43640761105](https://github.com/Matchekk/FM-27-Research/actions/runs/43640761105)
ging der Registrierung voraus. Das [Manifest](manifest.json) friert den
registrierten Vertrag, Analyse, Inputs, Code und Seeds ein;
[33 Technikplätze](technical-job-plan.json) und
[512 Hauptplätze](main-job-plan.json) sind vollständig vorab festgelegt.
Diese Registrierung startet keine Simulation. Vor TECH ist noch die erfolgreiche
CI genau dieser Manifestveröffentlichung erforderlich; vor Main zusätzlich
die eigene tatsächliche Technikabnahme und deren Veröffentlichungs-CI.

## Tatsächlicher Techniklauf

32 Vollmatches,16 exakte A/A-Paare und eine erwartete initiale108-Abweisung
sind vollständig abgeschlossen; keine unerwarteten Ausfälle oder Ersatzseeds.
[Technikbericht](../../docs/night-001/SHARPNESS-TECH-RESULTS.md),
[Messungen](technical.jsonl), [Jobstatus](technical-job-accounting.jsonl),
[Budget](technical-budget.json) und [Summary](technical-summary.json).
61,9805068/900 eigene Childsekunden abgerechnet. Keine Hauptmatches gestartet;
Main benötigt weiterhin den veröffentlichten unabhängigen Technikreview,
Freigabe und erfolgreiche CI dieser Veröffentlichung.

## Erhaltener ursprünglicher Entwurfsstatus

`contract-draft.json` beschreibt den separaten Raw-Startpaket×Pressing-Pilot:
vier Arme,64 neue unabhängige Seedblöcke/512 Hauptmatches,32 neue technische
Vollmatches plus eine Negativkontrolle. Noch keine Identitäts-/Setup-/Seed-/Code-
oder Commitfreigabe. Die vier technischen und64 Hauptseeds sind hier nicht reserviert.

Der Entwurf bleibt bis tatsächlich bestandenem TECH17 und unabhängig publizierter
Freigabe blockiert. Vor jeder wissenschaftlichen Ausführung sind zusätzlich die
eigenen Technik-, Ressourcen-, Review- und Publikationsgates erforderlich.
Die Staminastudie bleibt terminal geschlossen; ihre unbenutzten Seeds bleiben
ausgeschlossen. Keine neuen nativen Aufrufe, Holdouts oder Karriereversuche durch
diesen Designauftrag. Keine Ergebnisdateien oder Effekte werden erfunden.

Später ausschließlich getrennt eingefrorene Eingabebelege, Elternabrechnungen,
erlaubte öffentliche Mess-JSONL und545 vollständig erhaltene Jobstatus ergänzen.
Private Dumps, Rohlogs, Rawregionen, IDs und geschützte Spieldateien bleiben privat.

[Vorregistrierung](../../experiments/MECH-002-sharpness-pilot.md) ·
[Technischer Plan](../../docs/night-001/SHARPNESS-PLAN.md).

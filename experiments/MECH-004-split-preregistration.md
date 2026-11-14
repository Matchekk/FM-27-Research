# MECH-004-SPLIT-R0 – getrennte ursprüngliche Schärferohfelder

NIGHT-002 · vor dem ersten nativen Aufruf eingefrorener Varianzpilot.
Status: vorbereitet; **keine technische oder wissenschaftliche Freigabe durch dieses Dokument**.

## Erkenntnisfrage und Neuheit

Bleiben C90 (ursprüngliches Profilfeld16) und C7A (Profilfeld17) als getrennte
Startinterventionen erhalten, und unterscheiden sich ihre marginalen xGD-Effekte?
Gerichtete Arbeitshypothese: C90 und C7A tragen unterschiedlich zur beobachteten
Startpaketwirkung bei; getestet wird zweiseitig gegen einen Unterschied von null.
Positive Attribution bedeutet größeren C90-Beitrag.

`NOVEL_HYPOTHESIS` innerhalb der tatsächlich geprüften Literatur. Überlappung:
MAC-05 und MECH-002-SHARPNESS-P0 setzen beide Felder gemeinsam. Der Originalcode
[MAC-05, unveränderlicher Commit](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_everything.py)
setzt `sharpness` und `sharpness_secondary` auf denselben Wert. Hier liefern
erstmals in diesem Archiv die beiden gekreuzten Offdiagonalen neue Information.
Kein Anspruch weltweiter Erstmaligkeit. [Quellenprüfung](../docs/night-002/LITERATURE_AUDIT.md)
und [Kandidatenentscheidung](../docs/night-002/NOVELTY_MATRIX.md) sind Pflichtgates.

## Kontrollierter Eingriff

Vier Arme in dieser Reihenfolge:

| Arm | C90 roh | C7A roh |
| --- | ---: | ---: |
| C90L-C7AL, Kontrolle | 7000 | 7000 |
| C90H-C7AL | 10000 | 7000 |
| C90L-C7AH | 7000 | 10000 |
| C90H-C7AH | 10000 | 10000 |

Nur die zehn identitygebundenen Startfeldspieler der getesteten Seite werden
verändert. Originale Recordart15, bestehende Felder16/17, kein neuer Setter,
keine Kind61-Records, kein Eingriff nach Vorbereitung und kein dauerhafter Clamp.
Torwart, Bank und Gegner bleiben raw10000/10000. Alle46 aktiven Spieler behalten
Stamina60. D00-IP4-2-3-1/OOP4-4-1-1, Standardpressing, Phasen, Rollen, PI,
Positionsratings, Kaderstärke und originale Managementpolitik bleiben konstant.

Der unveränderte passive Observer und der ursprüngliche Recordcodec werden
wiederverwendet. Neue enge Compiler-/Auditfunktionen ändern keine historischen
Studien. Ein Rohfeldname ist keine validierte UI- oder Consumersemantik.
Gekreuzte Startzustände können künstlich sein; ihre Existenz in Karrieren ist
nicht nachgewiesen. Deshalb keine unmittelbare Rotations-/Trainingsempfehlung.

## Identität und Freigaben

Erwarteter, tatsächlich erneut zu hashender Kontext: FM27 `27.0.1+2503222`, DLL
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`,
Observerhost `58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`,
Fixture `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6`,
Tactics Lab v1114.6 / `91f2eba57fac0b7fbd3dff616056907e3ce461be`.
Die Eingabedatei enthält die vollständigen Ressourcen-/Katalog-/Quellhashes und
tatsächlich verwendeten Python-/NumPy-/SciPy-Versionen. Bei Drift Stopp.

Vor Technik: Quellenprüfung, öffentliche Vorregistrierung, konkrete unabhängige
Code-/Inputprüfung und erfolgreiche CI des exakten veröffentlichten Commits.
Vor Main zusätzlich: vollständige technische Abnahme, unabhängige Rohprüfung,
öffentliche Freigabe und erfolgreiche CI ihres exakten Commits. Dieselben
unveränderten Artefakte werden nicht ohne neuen Grund mehrfach begutachtet.

## Stichprobe und Reihenfolge

TECH32+1: vier neue technische Seeds, einer je Gegner×Seite; alle vier Arme
jeweils zweimal exakt wiederholt.32 Vollmatches und eine erwartete
Header-Negativabweisung mit Exit108. Technische Daten bleiben aus Mainanalysen.

Main:32 neue Seeds je festem Gegnerkontext (`high_press`, `deep_block`), jeweils
vier Arme und beide Teamseiten.512 Matches bilden **64 unabhängige Seedblöcke**,
nicht512 Replikate. Seitenmittel innerhalb des Seeds, Kontextgewichte je1/2.
Alle68 Seeds sind unter neuem Namespace gegen öffentliche und private frühere
Messungen, Fehler, Reservierungen und Holdouts zu prüfen und vor Start festzulegen.
Keine Seedwiederverwendung, Ersatzseeds, Retries, Holdouts oder automatische
Erweiterung. Seedplan, Manifest und vollständiger Jobplan sind öffentlich.

## Primär-/Sekundäranalyse

Primär genau ein Test auf xGD:

`ATTRIBUTION = mean(C90H-C7AL) − mean(C90L-C7AH)`.

Das entspricht `marginaler C90-Effekt − marginaler C7A-Effekt`, nicht deren
Summe. Einzelne marginale Effekte erhalten die Koeffizienten
`C90=(-.5,+.5,-.5,+.5)` und `C7A=(-.5,-.5,+.5,+.5)`;
physische Interaktion `(+1,-1,-1,+1)`.

Zweiseitiges α0,05; feste Kontextgewichte, Welch-t-Intervall und stratifizierter
20.000-Seedblock-Bootstrap mit festem RNG-Seed. Alle Seiten/Arme desselben Seeds
bleiben beim Resampling zusammen. Explorative Kontext-/Seitenmittel,
Leave-one-seed-out sowie beobachtete SD und einseitige95-%-SD-Obergrenzen werden
berichtet. Keine Auswahl eines Rollensiegers oder Optimierung anhand der Daten.

Eine einzige sekundäre Holm8-Familie umfasst C90:xGD, C7A:xGD,
Interaktion:xGD und ATTRIBUTION für tatsächliche Punkte, erzielte Tore,
Gegentore, xGF und xGA. Alle acht Tests werden unabhängig von ihrer Richtung
berichtet. Ein Sekundärbefund ersetzt keinen Primärnachweis.

Praktische Referenz: absolut0,20xGD Attribution/Match; gewünschte volle
95-%-Intervallbreite≤0,50. Dies ist ein Präzisions-/Varianzpilot ohne garantierte
90-%-Power. Bei angenommener SD der seiten-gemittelten Seedkontraste von0,5/1,0/1,5
ergibt n64 ungefähr volle Normalintervallbreiten0,245/0,490/0,735 und
Power für0,20 von ca.89/36/19%. Die unbekannte Splitkontrastvarianz lässt sich
nicht aus dem gemeinsamen alten Paketeffekt als gesichert übernehmen.
Erreichte Unsicherheit entscheidet über Informationswert; kein Nachfüllen bei
knapper Signifikanz. Bedingte Zukunftsplanung ist keine neue Ausführung.

## Technisches Gate und Ausschlüsse

In **jedem** Technikmatch müssen beide Rohfelder getrennt nach originaler
Vorbereitung und nach dem ersten Fortschritt für alle46 Spieler exakt stimmen.
Cache8A wird empirisch separat dokumentiert: kein angenommener C90-/C7A-Consumer.
Cache89=100, Condition10000, Fatigue0, Accumulator1000000, Penalty0 und die
initiale rohe33Byte-Region müssen mit dem eingefrorenen D00 übereinstimmen.
Alle69 Attribute,23 Profilfelder, Phasen/PI/Lineups und Seed sind nativ zu prüfen.
Alle16 A/A-Paare müssen identische Resultate und identitygebundene Zustände
aufweisen. Originaler TECH17-Transferbeleg bleibt eng und unverändert gültig.

Normalisiert die Engine die Offdiagonalen oder fällt ein anderes Gate aus,
**kein Mainlauf**; dokumentierter technischer Stopp dieses Vertrags. Fehlende
Werte/Fehler sind keine Nullen. Unerwarteter Exit, Timeout, Mismatch,
unbestätigte Bereinigung oder unvollständige Blöcke stoppen weitere Admissionen.
Bereits zugelassene Aufrufe werden begrenzt beendet und vollständig abgerechnet.
Keine ergebnisbasierten Ausschlüsse; unvollständige Mainserie ist ein technischer
Zwischenstand und liefert keine vorregistrierte Hauptschätzung.

## Engere Ressourcen und Abschluss

Eigene Grenze:512 Main,32 technische Vollmatches+1Negativprobe, maximal vier
kalte Worker,900 kumulierte beaufsichtigte Childsekunden und unveränderliche
5400s Studienfrist ab erster technischer Phase. Vor der unmittelbar ersten
Maininvokation mindestens600s aus eigenem/globalem Child-/UTC-Rest;90s ohne
Fortschritt, Jobobjektlimit3 je Aufruf. Maximal2GiB private Studienartefakte,
20GiB freie Platte. Keine weiteren nativen Vorbereitungsaufrufe.

NIGHT-002 zusätzlich insgesamt≤2048 Main,≤192 technische Vollmatches,
≤3600 Childsekunden,≤4GiB neue private native Artefakte und feste Deadline
15.11.2026 08:00Europe/Berlin =07:00UTC. Genau eine gemeinsame Exklusivlease.
Negative Probe konservativ als technischer Budgetplatz mitgerechnet. Alte
NIGHT-001-Budgets, Seeds und terminale Stopps werden nicht verändert.

Veröffentlichung nur zulässiger Rohmessungen/Hashes und sanitisierten Budgets;
keine Dumps, Spielmaterialien, Spieleridentitäten, Zugangsdaten oder privaten
Pfade. Nach Main unabhängige Rekonstruktion aus öffentlichen Rohdaten,
technische Provenienzprüfung, lokale Tests, CI, Commit/Push und Ergebnisbericht.

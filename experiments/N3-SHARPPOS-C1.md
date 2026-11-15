# N3-SHARPPOS-C1 – zwei Angreifer gegenüber zwei Innenverteidigern

Vorregistrierung15.11.2026; eigenständige zweite Frage von NIGHT-003.
[Neuheit/Quellen](../docs/night-003/LITERATURE_POS.md): NOVEL_HYPOTHESIS,
MAC-05/13/13B, FM27-PURITY-POS; eigener MECH-002-Ganzfeldspielereffekt unverändert.
Noch keine Ausführungsfreigabe durch diesen Text allein.

## Kausale Frage und Intervention

Unterscheidet sich der marginale Team-xGD-Nutzen derselben gemeinsamen
C90/C7A-Startänderung7000→10000 zwischen zwei festen Positionsgruppen?

| Arm | Feldstarter mit beiden Rohfeldern7000 | Alle anderen Akteure |
|---|---|---|
| ATTACK_LOW | originale Slots8AMC/AttackingMidfielder und10ST/CentreForward | beide Rohfelder10000 |
| DEFENCE_LOW | originale Slots2DCR/CentreBack und3DCL/CentreBack | beide Rohfelder10000 |

Je Arm genau vier Profilrecords der **zwei identitygebundenen ursprünglichen
Akteure**. Wiederverwendeter ursprünglicher MECH-002-Compiler erzeugt zuerst
die legalen Vorbereitungsrecords; ausschließlich die vier deklarierten Records
werden aus seinem Output ausgewählt. Kein neuer nativer Setter oder Eingriff
nach Vorbereitung, kein Clamp, keine Kind61-Ausführung. Beide originalen
IP4231/OOP4411, alle Positionen/Rollen/Attribute/Positionsratings, übrigen
Startzustände, Gegner, Keeper, Bank, Team Instructions und Management konstant.
Der unveränderte vollständige55xx-Recordvertrag und native Legalität gelten weiter.

## Primärer Kontrast und Aussagegrenze

`xGD(DEFENCE_LOW) − xGD(ATTACK_LOW)`.

Dies entspricht exakt `(HIGH_ALL−ATTACK_LOW)−(HIGH_ALL−DEFENCE_LOW)`:
ein gemeinsamer vollständiger Hochschärfe-Kontrollwert kürzt sich heraus.
Positive Werte bedeuten einen größeren marginalen Nutzen bei AMC/ST.
**Separate absolute Gruppeneffekte sind ohne zusätzlichen Kontrollarm nicht
identifiziert.** Es werden keine solchen absoluten Effekte nachträglich berichtet.
Feste Akteure und Rollen: kein universeller reiner Positionseffekt bei beliebigen
Spielern und kein kausaler Karrierenachweis von Einwechsel-/Trainingsstrategien.

## Stichprobe, Power und festgelegte Auswertung

4096neueHauptmatches = zwei feste bekannte Gegner×512neueSeeds×zweiSeiten×zweiArme.
**1024 unabhängige Kontext-Seedblöcke**; Seitenmittel je Seed, Kontextgewichte½.
Planreihenfolge wird mit festem RNG2026111504 blockweise gemischt und in dieser
Reihenfolge dispatcht. Keine Interim-Leistungsanalyse, keine adaptive Erweiterung,
kein statistischer Pilot. Technikseeds und historische/terminale Reservierungen
vollständig disjunkt; keine Retries/Ersatzseeds oder Nullimputation.

Primär xGD, zweiseitigα0,05, Welch/Satterthwaite95%-KI; stratifizierter
20000-Seedblock-Bootstrap als Sensitivität, RNG2026111504. Praktische Referenz
±0,15xGD/Match, gewünschte volle KI-Breite≤0,15. Keine universelle
Äquivalenzbehauptung; ein präzises KI innerhalb der Referenz schränkt diesen
Kontext ein. Punktwerte, Unsicherheit, Ausfälle und alle Arme vollständig berichten.

Vorabplanung aus dem ursprünglichen MECH-002-S100-P0−S70-P0-Kontrast,32Seeds je
Kontext: Block-SD0,943/0,854, erwartete volle KI-Breite0,110; Power für0,10/0,15
94,4%/99,96%. Simultane95%-SD-Obergrenzen1,253/1,136 liefern0,147 und76,2%/98,0%.
Das ist ein **anderer Zehnspieler-Kontrast als Varianzanker**, keine garantierte
neue Zweispieler-Varianz. Zahlen werden vor Main in `planning.json` eingefroren.

Eine **Holm6-Sekundärfamilie**: derselbe Gruppenkontrast auf tatsächliche
Punkte3/1/0, Tore, Gegentore, xGF, xGA; außerdem high_press−deep_block des
primären xGD-Kontrasts. Alle Tests unabhängig vom Vorzeichen berichten.
Armmittel/kontextweise Schätzer deskriptiv; keine Auswahl einer besten Teilgruppe.
Separate skalare Nachrechnung aus ursprünglichem Team-xG, ohne Array-/Schätzcode
der Hauptanalyse; gleicher Analyst, kein behaupteter separater Gutachter.

## Technik, Ressourcen und Abbruch

Unveränderter FM27-Build27.0.1+2503222, Engine/Observer/Ressourcen wie
N3-SHARPSTRUCT; exakte Hashes in eigenem `inputs.json`, erneut pro Phase/Call.
NativeActor-/Profilbindung,3174Attribute,1058Profilfelder,44Phasenzellen und
748PI-Gruppen müssen vollständig passen. Nach Vorbereitung und erstem Fortschritt
genau zwei deklarierte Akteure raw7000/cache70, alle anderen raw10000/cache100;
Kondition/Fatigue/Accumulator/Penalty und Raw-TF33 bleiben ursprünglichem D00 gleich.

Technik16+1: vier eigene neue Kontext×Seite-Seeds, beide Arme je zweimal,
acht exakte A/A-Paare und eine erwartete Exit108-Abweisung. Eigene Technik-
Leistung zählt nicht zur Wissenschaft. Vor Main neue technische Freigabe,
zweiter Rohbelegpass nach Bereinigung, veröffentlichte unveränderte Inputs/
Vorregistrierung und erfolgreiche exakte CI.

Erste Studie muss vollständig simuliert, analysiert und separat nachgerechnet
sein, bevor diese Studie irgendeinen nativen Call startet. Eigene Budgets,
keine Wiederverwendung/Änderung alter Reservierungen. Max4kalteWorker, eine
globale exklusive NativeLease, unverändertes Job3-Containment je Call, absolut30s
und begrenzte Bereinigung. Eigene7200s beaufsichtigte Phasenzeit/10800s ab erster
Technikphase; **zusätzlich bindet die bereits feste Missionsfrist der ersten
Studie11:11:21UTC** (keine Verlängerung). Vor Main mindestens4200s Missionsrest.
16GiB private Belege,20GiB freie Reserve; keine Archivierung während der Phase.

Jeder Input-/Build-/Ressourcen-/Seed-/Readback-/Wiederholungs-/Cleanupfehler
stoppt neue Zulassungen. Fehlende Jobs bleiben fehlend, keine Leistungsauswertung
einer unvollständigen Hauptserie. Keine privaten Spielstände oder Originalhosts ändern.

Artefakte `data/night-003-sharppos/`: `inputs.json`, `seed-plan.json`,
`technical-plan.json`, `main-plan.json`, `technical.jsonl`, `main.jsonl`,
`effects.json`, `independent-recalculation.json`, `seed-contrasts.jsonl`.
Runner `analysis/night003_pos.py`, Analyse `analysis/analyse_night003_pos.py`.
Native Dumps/geschütztes Spielmaterial bleiben lokal und werden nicht gepusht.

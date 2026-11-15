# N3-AMCSHIFT-C1 – isolierter seitlicher AMC-Positionsrecord

Vorregistrierung 15.11.2026. Dritte, eigenständige Restfensterfrage von NIGHT-003;
kein nativer Start durch dieses Dokument allein. [Neuheitsprüfung](../docs/night-003/LITERATURE_AMC.md):
NOVEL_HYPOTHESIS, Überschneidung MAC-07/07B/08/17/19 und eigene Paketstudien.

## Neue Frage und einziger veränderter Input

Welchen mittleren xGD-Effekt hat allein die im STLESS-Paket enthaltene seitliche
Verschiebung des ursprünglichen AMC nach AMCL, wenn Rolle und Mittelstürmer
unverändert bleiben? Zweiseitige Hypothese; keine vorgegebene Gewinnerichtung.

| Arm | Ursprünglicher Actor8, IP | Actor10, IP | OOP / Schärfe |
|---|---|---|---|
| BASE | AMC / AttackingMidfielder | ST / CentreForward | Original4411 / raw10000 |
| AMC_LEFT | AMCL / AttackingMidfielder | ST / CentreForward | identisch |

BASE bytegleich ursprünglichem D00. AMC_LEFT ändert genau einen Kind5-Record,
getestete Seite, nativer IP-Slot8. Der bestehende archivierte STLESS-Compiler
liefert den erlaubten Positionsrecord; alle anderen Records werden aus dem
Original übernommen. Keine Rolle, PI, Attribute, Positionsratings, Startprofile,
Team Instructions, Mentalität, Kaderidentitäten, Gegner oder Managementpolitik
ändern. Beide gemeinsamen Schärfefelder bleiben bei allen46Akteuren10000;
kein neuer Setter, kein Clamp und kein Eingriff nach Vorbereitung.

Dies isoliert eine **zugewiesene Inputposition**, keinen einzelnen Laufweg,
Abstandsmechanismus oder universellen AMCL-Effekt. Der übrige STLESS-Schritt
ST→AMCR/SecondStriker wird in dieser Studie nicht ausgeführt. Frühere gemeinsame
Pakete werden nicht unter neuer Kennung wiederholt.

## Fallzahl und eingefrorene Analyse

**2.048 neue Hauptmatches = zwei feste Gegner ×256neueSeeds ×zweiSeiten ×zweiArme.**
512 unabhängige Kontext-Seedblöcke, Seitenmittel im Seed, gleiche Kontextgewichte.
Primär `xGD(AMC_LEFT)−xGD(BASE)`, zweiseitigα0,05, Welch/Satterthwaite95%-KI;
20.000 stratifizierte Seedblock-Bootstraps, RNG2026111505. Praktische Referenz
±0,20xGD; Ziel volle KI-Breite≤0,20. Keine Interim-Leistungsanalyse, kein Pilot,
keine adaptive Vergrößerung, keine Ergebnisausschlüsse oder Nullimputation.

Eine vorregistrierte Holm6-Sekundärfamilie: derselbe Kontrast auf tatsächliche
Punkte3/1/0, Tore, Gegentore, xGF, xGA; außerdem high_press−deep_block auf xGD.
Kontext-/Armmittel deskriptiv; keine Auswahl einer besten Teilgruppe.
Separate skalare Nachrechnung aller formalen Welch-Schätzer und Holm6.
Keine separaten absoluten Rollenmechanismen aus Paketdifferenzen ableiten.

Planungsanker ist der abgeschlossene N3-SHARPSTRUCT-IP_HIGH-Paketkontrast:
Block-SD0,8763/0,8265 bei256Seeds je Kontext. Für die neue2.048er-Serie ergeben
sich volle erwartete KI-Breite0,1479 und Power99,96% für0,20. Simultane95%-
Normalmodell-SD-Obergrenzen0,9595/0,9050 ergeben0,1620 und99,80%.
Für0,15:97,8% beziehungsweise95,3%. **Andere Intervention, nur Varianzproxy**;
die neue Komponentenvarianz ist unbekannt. Keine AMC-only-Ergebnisse wurden
zur Auswahl benutzt. `planning.json` wird vor Main veröffentlicht.

## Gezielte Technik und feste Grenzen

Vier eigene Technikseeds, alle acht Kontext×Seite×Arm-Zellen je zweimal:
16Vollmatches,achtA/A-Paare plus eine erwartete Exit108-Abweisung. Originale
Game-Constraints aktiv. Alle3.174Attribute,1.058Profilfelder,44Phasenzellen,
748PI-Gruppen und Actor-/Phasenbindungen müssen dem Plan entsprechen.
Raw-/Cache-Startzustände10000/100 und Nichtschärfe-/Raw-TF33-Kontrollen nach
Vorbereitung/erstem Fortschritt unverändert. Natürlicher Matchabschluss nötig.

Gepinnter FM27-Build27.0.1+2503222 und unveränderter passiver Observer wie in
den ersten Studien; exakte Engine-/Host-/Fixture-/Ressourcenhashes im eigenen
Inputmanifest und pro Call erneut geprüft. Nur ursprüngliche bestehende
Eingabefelder, kein neuer Host oder neue Eingriffsart.

Native Technik **erst nach vollständiger zweiter Hauptserie und ihrer separaten
Nachrechnung**, zusätzlich mindestens2.700s Rest bis zur bereits festen
Missionsfrist11:11:21UTC. Main erst nach eigenem Technikpass, zweitem Rohbelegpass,
veröffentlichter Freigabe/erfolgreicher CI und mindestens2.400s Missionsrest.
2.048Matches kosten nach bisher gemessener Phasenrate ungefähr1.666s;
2.400s Zulassung lässt rund44% zeitliche Reserve. Bei fehlendem Rest keine
wissenschaftlichen Calls; alle Reservierungen bleiben erhalten.

Eigene2.700s kumulierte beaufsichtigte Phasenzeit,3.600s eigener UTC-Zeitraum
ab erstem Technikcall; die frühere globale Missionsfrist bindet zusätzlich.
Max4kalteWorker, eine exklusive NativeLease, unverändertes Job3-Containment
je Call, absolut30s plus begrenzte Bereinigung,8GiB private Belege,20GiB freie
Reserve. Jeder Input-/Build-/Ressourcen-/Readback-/Legalitäts-/A/A-/Cleanupfehler
stoppt weitere Zulassungen. Keine Retries oder Ersatzseeds. Nur vollständige
2.048Matches erlauben die Wirkungsanalyse. Keine laufende Archivierung.

Artefakte `data/night-003-amcshift/`: `inputs.json`, `seed-plan.json`,
`technical-plan.json`, `main-plan.json`, `technical.jsonl`, `main.jsonl`,
`effects.json` und separate Nachrechnungen. Runner `analysis/night003_amc.py`,
Analyse `analysis/analyse_night003_amc.py`. Geschützte Originalbelege bleiben privat.

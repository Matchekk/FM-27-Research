# N3-SHARPSTRUCT-C1 – präzise begrenzte Schärfe×IP-Interaktion

15.11.2026. **4.096 gültige neue Hauptmatches, 512 unabhängige Seedblöcke.**
Primäre Interaktion **−0,013320 xGD/Match**, 95-%-Welch-KI
**[−0,118593; +0,091953]**, p=0,803779. Separat skalar nachgerechnet.

Das gesamte Intervall liegt innerhalb der vorab festgelegten praktischen
Referenz ±0,20. Die Daten stützen im geprüften Kontext keine Wechselwirkung
dieser Größenordnung. Kleinere Wirkungen bleiben möglich; keine universelle
Wirkungsfreiheit oder Gleichwertigkeit beliebiger Taktiken behauptet.

## Frage, Eingriff und wissenschaftliche Neuheit

[Vorregistrierung](N3-SHARPSTRUCT-C1.md):
`[STLESS10000−BASE10000]−[STLESS7000−BASE7000]`, OOP4411 unverändert.
Originales gemeinsames C90/C7A-Startpaket bei zehn Feldstartern, archiviertes
IP4240-Paket aus TACT-003, alle anderen Inputs und Managementpolitik konstant.
Die neue Erkenntnis ist die präzise Eingrenzung ihrer **Interaktion**.
Die separaten MECH-002- und TACT-003-Haupteffekte bleiben eigene Vorbefunde.

256 neue Seeds je festem Gegnerkontext, zwei Seiten, vier Arme. Seitenmittel
innerhalb des Seeds, gleiche Kontextgewichte; 4.096 Matches sind nicht 4.096
unabhängige Beobachtungen. Kein Pilot, keine Interim-Leistungsanalyse,
keine Stichprobenänderung, kein Holdout oder Karrierefortschritt.

## Alle vorregistrierten Ergebnisse

| Kontrast | Effekt/Match | Marginales 95-%-KI | p / Holm6-p |
|---|---:|---|---:|
| Interaktion xGD, primär | −0,013320 | [−0,118593; +0,091953] | 0,803779, einzelner Primärtest |
| Interaktion tatsächliche Punkte | −0,080078 | [−0,232091; +0,071935] | 1,000000 |
| Interaktion erzielte Tore | −0,090820 | [−0,210563; +0,028922] | 0,820898 |
| Interaktion Gegentore | −0,005859 | [−0,150010; +0,138292] | 1,000000 |
| Interaktion xGF | −0,008046 | [−0,074430; +0,058338] | 1,000000 |
| Interaktion xGA | +0,005274 | [−0,072483; +0,083031] | 1,000000 |
| Interaktion high_press minus deep_block, xGD | −0,073101 | [−0,283647; +0,137444] | 1,000000 |

Kein Sekundärtest besteht die vorab festgelegte Holm6-Korrektur. Positive
Gegentore/xGA bedeuten größere Chancen-/Torabgabe. Tatsächliche Punkte sind
3/1/0, keine modellierten xPts. Ihre Unsicherheit erlaubt weiterhin andere
Abstände als die praktisch eingegrenzte primäre xGD-Interaktion.

Primär stratifizierter 20.000-Seedblock-Bootstrap:
[−0,118783; +0,090835]. Welch-SE 0,053582, df 502,476.
Volle KI-Breite **0,210546**, Präzisionsziel ≤0,25 erreicht. Kein nachträgliches
Powerargument aus dem beobachteten p-Wert; die vorab archivierten Varianzanker
ergaben erwartete Breiten etwa 0,184–0,252 bei beobachteten alten Interaktions-SD.

## Deskriptive Einordnung, keine weitere Testfamilie

| Kontext | Interaktion xGD | Block-SD |
|---|---:|---:|
| high_press | −0,049871 | 1,284468 |
| deep_block | +0,023231 | 1,135827 |

Einfache IP-Paketabstände: bei raw10000 −0,244552 xGD
[−0,318504; −0,170599], bei raw7000 −0,231232
[−0,308778; −0,153685]. Diese Intervalle sind **deskriptiv und unadjustiert**.
Keine zusätzliche Siegerentscheidung. Im konkreten Fixture verschafft volle
Schärfe diesem STLESS-Paket keinen durch die Daten gestützten relativen Gewinn
von 0,20 xGD gegenüber dem klassischen System. Andere stürmerlose Pakete,
Gegner, natürliche Positionsratings und reale Karrieren sind damit nicht bewertet.
Neue Scouting-Attributgewichte folgen aus dieser Studie nicht.

## Technik, Ressourcen und Provenienz

FM27 **27.0.1+2503222**, Tactics Lab v1114.6,
Observer-SHA `58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`.
DLL-/Fixture-/Ressourcenhashes und alle Code-/Inputhashes im
[Inputmanifest](../data/night-003-sharpstruct/inputs.json).

32 technische Vollmatches, 16 exakte A/A-Paare und eine erwartete Exit108-Probe
gingen Main voraus. Alle 4.129 geplanten Calls vollständig abgerechnet:
4.128 Vollmatches plus eine Negativabweisung. **0 unerwartete Ausfälle,
0 unbegonnene/unaufgelöste Jobs, 0 Ausschlüsse, Retries oder Ersatzseeds;
0 fehlende Ergebnis- oder deskriptive Messwerte.** Jede native Eingabe,
Actorbindung, Startcacheübertragung und Nichtschärfe-/Raw-TF33-Kontrolle bestand.

Maximal vier kalte Calls; vorhandenes Windows-Job3-Containment und exklusive
NativeLease. Tatsächlicher Engine-PID-Peak nicht gemessen; Vierergrenze durch
Dispatch/Containment belegt. Native Prozesse vollständig bereinigt. Ein zweiter
Pass nach Bereinigung las und prüfte jeden unveränderten Rohlog/Inputdump
erneut gegen den Export. Keine laufende Archivierung, Verschiebung oder Löschung.

Beaufsichtigte Phasenzeit insgesamt 3.360,474/7.200 Sekunden, davon Main
3.332,793 Sekunden. Summe der parallelen nativen Main-Aufrufzeiten
12.737,829 Sekunden; diese Summe ist nicht die Phasen-Wanduhrzeit.
Private Artefakte bei Nachinventur 2.242.155.322 Bytes, unter 16 GiB.
Feste UTC-Frist 11:11:21 eingehalten; volle Messserie endete 09:11:27 UTC.

[Reihenfolgeänderung vor Main](../docs/night-003/TECHNICAL_RELEASE.md): der
wiederverwendete Dispatcher sortiert Kontext-Seedblöcke erneut. Dies wurde vor
dem ersten wissenschaftlichen Match veröffentlicht; keine Behauptung einer
randomisierten Dispatchreihenfolge. Arme, Fallzahl, Seeds und Analyse unverändert.

[Hauptmessungen](../data/night-003-sharpstruct/main.jsonl) ·
[512 Blockkontraste](../data/night-003-sharpstruct/seed-contrasts.jsonl) ·
[vollständige Effekte/Armmittel](../data/night-003-sharpstruct/effects.json) ·
[separate Nachrechnung](../data/night-003-sharpstruct/independent-recalculation.json) ·
[Abrechnung/Software/Fehlstellen](../data/night-003-sharpstruct/execution-provenance.json).
Die unabhängige Arithmetik verwendet ursprüngliches Team-xG, Wörterbücher und
skalare Momente ohne den Array-/Schätzpfad der Hauptanalyse. Gleicher Analyst,
kein behaupteter separater Gutachter. Historische terminale Studien unverändert.

Vorregistrierung ac5b993, Freigabe/Korrektur f57c193 und erfolgreiche
[CI43693487274](https://github.com/Matchekk/FM-27-Research/actions/runs/43693487274)
lagen vor Main vor. Portable Ergebnistests rekonstruieren alle 4.096 Messungen
und den Primäreffekt in beiden Rechenwegen. Ergebniscommit
`a58e11d59cf8b75f366197e56282c471247f2bc8` besteht
[CI43699039037](https://github.com/Matchekk/FM-27-Research/actions/runs/43699039037).
Eine zusätzliche [unabhängige skalare Statistikprüfung](../data/night-003-sharpstruct/independent-statistics-review.json)
rekonstruiert alle sieben formalen Schätzer, deren Welch-Intervalle und Holm6
ohne die ursprünglichen Analyse-/Statistikmodule. Gleicher Analyst.

# MECH-004-SPLIT-R0 – unabhängiger konkreter Inputreview

14.11.2026 · Research Agent, getrennt von Studiencompiler, Runner, Controller
und Analyseautor. **Konkrete Offlineinputs für TECH32+1 akzeptiert.**
Veröffentlichung und erfolgreiche CI des exakten Commits bleiben vor Technik
verpflichtend. **Keine native Splitübertragung oder Mainfreigabe festgestellt.**

## Gebundene Artefakte

Geprüft wurden [Vorregistrierung](../../experiments/MECH-004-split-preregistration.md),
[Neuheitsmatrix](NOVELTY_MATRIX.md), [Runnerreview](SPLIT004-RUNNER-REVIEW.md),
[konkretes Inputmanifest](../../data/night-002-split004/inputs.json),
[Vertrag](../../data/night-002-split004/contract.json) und
[Seedplan](../../data/night-002-split004/seed-plan.json).
Der bereits erstellte Literaturreview beantwortet eine andere Prüfaufgabe und
ersetzt keine Input- oder spätere Ergebnisprüfung.

SHA256 des Inputmanifests, LF-normalisiert:
`b322aa51b2e478f6c86e3405ef273bf78831f473bb0ece9d55c054b30a65d0a5`.
Alle **32** darin eingefrorenen Projektquellen/-dokumente wurden erneut gegen
ihre tatsächlichen LF-normalisierten Bytes geprüft. Die acht expliziten
Dateihashes des Runnerreviews stimmen ebenfalls; keine Quellenänderung durch
diesen Reviewer. Der Inputreview liegt außerhalb dieses eingefrorenen
Quellmanifests und wird über sein separates Reviewgate gebunden.

## Tatsächliche Binärprüfung ohne Studiencompiler

Die 16 erzeugten Dateien wurden mit einem eigenen kleinen Pythondecoder gelesen:
Header `FM27CFG1`, 32-Bit-Little-Endian-Recordzahl, anschließend fünf getrennt
decodierte UInt32 je Record. Kein Aufruf des Studiencompilers, Runners, nativen
Hosts oder fremden Servers. Alle Dateien besitzen **5.557 Records** und genau
die gebundenen Setup-SHA256. Jede wurde direkt mit ihrem tatsächlichen früheren
D00-Binäroriginal verglichen.

| Kontext | Teamseite | LL / HL / LH / HH geänderte Records |
| --- | ---: | --- |
| high_press | 0 | 20 / 10 / 10 / 0 |
| high_press | 1 | 20 / 10 / 10 / 0 |
| deep_block | 0 | 20 / 10 / 10 / 0 |
| deep_block | 1 | 20 / 10 / 10 / 0 |

Jeder Unterschied betrifft ausschließlich Recordart15, getestete Seite und
Feld16 beziehungsweise17 eines der **zehn aus den absoluten Lineuprecords
bestimmten Startfeldspieler**. Vorher10000, nachher7000; HH ist vollständig
byteidentisch zum ursprünglichen D00. Torwart, Bank und Gegner behalten beide
Felder10000. Recordreihenfolge, andere Profilfelder, Rollen, PI, Phasen,
Positionsratings und Mannschaftsanweisungen sind identisch. Keine Kind61-Records.
Alle46Stamina-Records bleiben60. Standardpressing auf der getesteten Seite ist
auch in den gebundenen Konfigurationen vorhanden.

Die privaten Konfigurationen ergeben exakt den publizierten kanonischen Hash
`ca63168da0bb3c7c6fb79cfd1b9604a75620a9550309720a2616fe9b9c0dcdd7`.
Vier frühere D00-Goldlogs stimmen mit ihren Hashes überein. Die darin für
`prepared` und `first_advance` gespeicherten, identitysortierten Kontrollen
(Condition, Fatigue, Accumulator, Penalty und rohe33Byte-Region) wurden mit
eigener JSON-/Hashberechnung rekonstruiert und stimmen exakt mit dem neuen
Inputmanifest überein. Das bindet die Sollkontrollen; es beweist noch nicht,
dass neue Splitläufe diese Kontrollen tatsächlich erfüllen.

## Identität und Seeddisjunktheit

Die installierte DLL wurde erneut gehasht und ihre Windows-Dateimetadaten
gelesen: ProductVersion **27.0.1+2503222**, FileVersion **27.0.1**.
Alle elf Ressourcen, ursprünglicher Host, unveränderter Observerhost,
Buildmanifest, Hostquelle, Observerheader, Fixture, Katalog und49Runtimequellen
stimmen mit den gebundenen Belegen überein. Ressourcenfingerprint:
`6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883`.
DLL-/Host-/Fixturehashes und Upstreamidentität entsprechen der Vorregistrierung.
Ein Hashvergleich ist kein neuer nativer Kompatibilitätslauf.

Der TECH17-Release ist über Review-/Summary-/Releasehashes unverändert gebunden;
er ersetzt keine neue Splitabnahme. Die Abwesenheit der vier verbotenen
Namespace-/Shadowdateien wurde kontrolliert.

Unabhängiger eigener Archivscan mit Dateibaum-/JSONrekursion, ohne Aufruf der
studieneigenen Seedfunktion: **13.288 JSON/JSONL-Dateien, 2.065.456.106 gelesene
Bytes**, öffentliche Archive, frühere private Versuche und Registry. Nur der
eigene öffentliche/private Studienunterbaum und die eigene neue Reservierung
wurden ausgeschlossen. Zusätzliche ausdrücklich benannte Main-/Technikarrays
wurden konservativ mitgeprüft.

Das ergibt dieselben **2.597** ausgeschlossenen früheren Seedwerte und denselben
kanonischen Seedsethash wie die Reservierung:
`68d34e0e9ca0ad3aa9a1d2e3c294b161c96145cd897754563156edc40a4f2400`.
Alle **68 neuen Seeds** sind eindeutige positive UInt32, davon64Main und4Technik;
keine Überschneidung untereinander oder mit dem Altbestand. Öffentlicher Plan
und Registryeintrag sind identisch. Keine Seedreservation durch diesen Reviewer.

## Wissenschaftliche und technische Eintrittsbedingungen

Der Primärkontrast `HL−LH` entspricht algebraisch der Differenz der zwei
marginalen Effekte. C90/C7A-Haupteffekte sind korrekt halbiert, die physische
Interaktion nicht. Eine Primärhypothese und genau acht vorab benannte
Holm-Sekundärtests; tatsächliche Punkte, Tore und Gegentore sind berücksichtigt.
64 unabhängige Seedblöcke mit Seitenmittel und festen Kontextgewichten, keine
512 unabhängigen Replikate. Unbekannte neue Varianz wird als Pilotgrenze geführt.

Der geprüfte technische Audit verlangt getrennte richtige Rohfelder nach
Originalvorbereitung und erstem Fortschritt für alle46Actorbindungen; andere
Startkontrollen und RawTF33 müssen unverändert bleiben. Cache8A wird beobachtet,
keine C90-/C7A-Consumerzuordnung erzwungen. A/A prüft Zustände und Ergebnisse;
Kollaps, Mismatch, Fehler oder unbestätigte Bereinigung stoppen die Studie.
Keine Clamps, Ersatzseeds, Retries, UI-Prozentskala oder Karrierevalidierung.

Das [Reviewgate](../../data/night-002-split004/review-gate.json) erteilt allein
die vorbereitete Inputabnahme für **32 technische Vollmatches plus eine
Negativprobe**, nach Publikation/CI und unter den engeren900Childsekunden/
5400UTCsekunden sowie den globalen NIGHT-002-Limits. Für Main sind neue native
Belege, unabhängiger technischer Rohreview, veröffentlichter Release und
erfolgreiche CI erforderlich. Durch den Reviewer ausgeführt: **0 native
Aufrufe, 0 Matches, 0 Karriereaktionen**.

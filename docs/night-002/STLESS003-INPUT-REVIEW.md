# TACT-003-STLESS-R0 – unabhängiger konkreter Inputreview

15.11.2026 CET · Research Agent, getrennt von Compiler-/Analyse-/Runnerautoren.
**Konkrete Offlineinputs für TECH32+1 akzeptiert.** Öffentliche Vorregistrierung,
erfolgreiche exakte CI und Registrierung/Jobplanpublikation bleiben vor Technik
erforderlich. Keine native Legalität, erfolgreiche neue Technik oder Mainfreigabe
wird durch diesen Review behauptet.

## Gebundener neuer Stand

Geprüft wurden [konkrete Inputs](../../data/night-002-stless003/inputs.json),
[Vertrag](../../data/night-002-stless003/contract.json),
[Seedplan](../../data/night-002-stless003/seed-plan.json),
[Runnerreview](STLESS003-RUNNER-REVIEW.md), die privaten16Binärdateien und
ihre16erwarteten Armkonfigurationen. Die vorhandenen Neuheits-/Wissenschaftsreviews
werden nicht ohne neuen Grund wiederholt. Der
[zusätzliche Quellenpreflight](STLESS003-SOURCE-PREFLIGHT.md) wurde vor neuen Seeds
abgeschlossen und erteilt keine technische Freigabe.

SHA256 des Inputmanifests über LF-normalisierte Bytes:
`5f1886c044ff890c81828cdf89141a27f2135f9ef4238ae354660a0fbeed7de7`.
Alle36gebundenen Projektquellen/-dokumente stimmen mit ihren tatsächlichen
Hashes überein, ebenso die zehn expliziten Quellhashes des Runnerreviews.
Die wissenschaftliche Analyse behält
`58da6f79cb1e262f113158455e9767f2bc88b6e9d8999b8b3d5d4a4fc14166b6`.
Keine Quellenänderung durch diesen Reviewer.

## Eigenständiger Binär-/Konfigurationsvergleich

Die Dateien wurden mit eigenem Pythondecoder gelesen: Header `FM27CFG1`,
UInt32-Recordzahl und anschließend Little-Endian-Fünferrecords. Der Studiencompiler
wurde für diese Prüfung nicht aufgerufen. Alle16Dateien haben5557Records;
ihre SHA256 stimmen mit dem Manifest überein. Direkter Vergleich mit den
vier tatsächlich vorhandenen D00-Originalen:

| Kontext | Teamseite | I0O0 / I1O0 / I0O1 / I1O1 geänderte Records | Native OOP-Ziele für ursprüngliche Akteure8/10 |
| --- | ---: | --- | --- |
| high_press | 0 | 0 / 3 / 3 / 6 | 23 / 26 |
| high_press | 1 | 0 / 3 / 3 / 6 | 25 / 26 |
| deep_block | 0 | 0 / 3 / 3 / 6 | 23 / 26 |
| deep_block | 1 | 0 / 3 / 3 / 6 | 25 / 26 |

Die erwarteten Änderungen wurden unabhängig aus Originalkatalog und
Konfiguration konstruiert. Nur Kind4/Rollenflags und Kind5/Positionsmasken der
deklarierten getesteten Seite und Akteure8/10 ändern sich. IP: AMC→AMCL und
ST/CF→AMCR/SecondStriker. OOP: AMC→AMCL und ST/OPCF→AMCR/OPAM.
Die ursprüngliche seitenspezifische OOP-Permutation wird wirklich verwendet;
ein gleicher ungeprüfter Slotindex für beide Seiten wäre hier falsch.
I0-O0 ist in jedem Kontext vollständig bytegleich D00.

Alle übrigen Records stimmen in Wert und Reihenfolge exakt überein:
3174Attributwerte,1058Profilfelder, originale Startelf/Identitäten,
Rostergrößen, PI/Duties/Targets, Anweisungen und sonstige Steuerwerte.
Die beiden ursprünglichen nativen Game-Constraints bleiben1;
keine Kind61-Records.46aktive Spieler,23je Seite; alle46kodierten Staminawerte60.
Der vorhandene Konfigurationscontainer enthält auf einer Seite weitere ungenutzte
Zeilen, aber `roster_size=23` und der tatsächlich kodierte aktive Vektorsatz
bleiben unverändert. Es wurden keine zusätzlichen Spieler in die Engine aufgenommen.

Jede Armkonfiguration entspricht exakt einer eigenen Kopie ihrer Baseline mit
nur diesen deklarierten vier Positions-/Rollenänderungsstellen. Auch Gegner,
Spieler-/Eignungsvektoren und vollständige Spielerlisten sind identisch.
Das neue kanonische Konfigurationshash ist
`7f716c293cb5206450c041a04669809e02a000e081eff1b82dba3e0b8e847964`;
das unveränderte Original bleibt
`ca63168da0bb3c7c6fb79cfd1b9604a75620a9550309720a2616fe9b9c0dcdd7`.

Alle11besetzten Positionen jeder Phase sind eindeutig. Die konkrete statische
Rollen-/Phaseneignung wurde für **beide Mannschaften und alle Arme** im
originalen Katalogkontext `0:0` geprüft. Dies ist Kataloglegalität, noch keine
neue native Game-Abnahme. Vier tatsächliche D00-Goldlogs und ihre
identitysortierten Kontrollhashes für Vorbereitung/Erstfortschritt wurden mit
eigener JSONberechnung erneut an die neuen Sollinputs gebunden.

## Identität und Seeddisjunktheit

Installierte DLL tatsächlich erneut gehasht und Dateimetadaten gelesen:
ProductVersion27.0.1+2503222, FileVersion27.0.1. Alle elf Ressourcen ergeben den
identischen gebundenen Fingerprint
`6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883`.
Observerhost, Buildmanifest, Hostquelle/-header, Fixture, Katalog und49
Runtimequellen stimmen mit den konkreten Belegen überein. Python3.12.10,
NumPy2.3.5, SciPy1.16.3 und Basis-Pythonhash entsprechen den tatsächlich
verwendeten Projektbibliotheken. Keine neue native Kompatibilitätsprüfung.

Unabhängiger eigener Dateibaum-/JSONseedscan ohne studieneigene Seedfunktion:
**15.132Dateien /2.205.568.302gelesene Bytes**. Öffentliche Archive, frühere
private Versuche, terminale Restreservationen und Registry wurden berücksichtigt;
nur die eigene neue Studie und ihre eigene Reservation ausgeschlossen.
Ergebnis exakt2665frühere Seedwerte, Hash
`0beb129664600688b689b2bf4991859219a640123ea4e845e824329c0a66a3bf`.
Die68neuen positiven UInt32-Seeds (64Main/4Technik) sind eindeutig und vollständig
disjunkt. Öffentlicher Plan und Registryeintrag stimmen überein. Keine Seeds
des terminalen MECH-004 werden ersetzt oder wiederverwendet.

## Administrative Kontinuität ohne Wiederaufnahme

Die tatsächliche administrative Übergangsreceipt ist über ihren Hash und ihre
Bindung im Inputmanifest geprüft. Der aktuelle globale Budgethash stimmt exakt
mit dem erlaubten Nachzustand überein:
`3dd7e09b93fee8d4a13f47646d7aa7f027db033acc662b7aa9ba84d9f8f792e0`.
Die Receipt bindet veröffentlichtes
`d143d3ed22b58ecda484ae12803bf89f70fcc8e4` und
[CI43653104526](https://github.com/Matchekk/FM-27-Research/actions/runs/43653104526).
Das Actions-API-Ergebnis wurde geprüft: derselbeHead, completed/success,
23:27:11UTC, vor ausgeführter Übergangsreceipt.

Der globale Zustand ist inaktiv, behält alle545früheren Jobreservationen,
beide Operationen einschließlich Mainfehler und589,7353507sBelastung exakt bei.
MECH-004 steht ausdrücklich in `terminal_studies`. Sein eigenes Ledger bleibt
bytegleich dem terminalen Snapshot, `halted=true`, `active=null`,528,8133745s.
Die bloße administrative Erlaubnis für eine andere Frage ist keine Fortsetzung
der ersten Studie. Deren257tatsächliche Calls mit838,064s bleiben gebunden;
`scientific_series_complete=false` wird nicht umetikettiert.

Der neue Ressourcenvertrag enthält zusätzlich30sabsoluteCallgrenze,
40sReservehülle und3600smissionsweite Summe einzelner Calls; die bisherigen
900sStudien-/5400sUTC-/600sMainrestgrenzen bleiben bindend. Dieser Inputreview
prüft deren konkrete Vertragsbindung und unveränderten geprüften Runnerstand,
ersetzt aber keine Laufzeitkontrolle.

## Abnahmeumfang

Das [Inputreviewgate](../../data/night-002-stless003/review-gate.json) akzeptiert
ausschließlich die konkrete Vorbereitung für32technische Vollmatches plus
Negativprobe nach Publikation/CI. Neue native Rollen-/Positionslegalität,
Actor-/Phasenreadbacks,16exakte A/A-Paare und eigener unabhängiger technischer
Release fehlen vor Main weiterhin. Pakete und synthetische Profile bleiben
Interpretationsgrenzen; keine isolierte Rollen-/Laufweg- oder Karriereaussage.
Durch diesen Reviewer:0nativeAufrufe,0neueMatches,0Seedreservierungen.

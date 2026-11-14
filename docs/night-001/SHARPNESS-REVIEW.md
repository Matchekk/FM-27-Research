# MECH-002-SHARPNESS-P0: unabhängige konkrete Inputfreigabe

Stand2026-11-14. **Konkrete Offline-Inputs, Seedreservierung und Quellenbindung
bestanden.** Diese Freigabe betrifft ausschließlich die Vorbereitung der
vorregistrierten32 technischen Vollmatches plus einer Negativkontrolle. Deren
vollständige Veröffentlichung, Registrierung und exakte erfolgreiche CI bleiben
vor Ausführung zwingend. Keine Mainfreigabe und keine bereits behauptete
TECH32+1-Abnahme.

Geprüfter Quellenstand: `95d94a4e674a13eea543b64677f7c621c52e871a`.
Der GitHub-Lauf[43640107860](https://github.com/Matchekk/FM-27-Research/actions/runs/43640107860)
wurde unabhängig per API geprüft: derselbe `head_sha`, `completed`, `success`.
Alle27 im vorbereiteten Manifest genannten Quellen stimmen sowohl mit dem
aktuellen Archiv als auch mit den Gitblobs dieses Commits überein. Die erst
danach inert erstellten konkreten Inputs sind bei diesem Quellencommit noch
nicht enthalten; sie werden zusammen mit diesem Review gesondert publiziert.

## Exakte Artefaktbindung

SHA256 mit ausschließlich CRLF→LF für öffentliche Textartefakte:

| Artefakt | SHA256 |
| --- | --- |
| `data/mech-002-sharpness-p0/inputs.json` | `0f1f4e048a1f3f893f47acf21b99b2730341424eb83a70c7ede066402b92f34f` |
| `data/mech-002-sharpness-p0/seed-plan.json` | `ae757f43be92774cd53ac7632f47527db39ff1613d931c2aeb0d8f9fabb19692` |
| `data/mech-002-sharpness-p0/contract.json` | `4956470ec0a03822aa9e0c4dd99781ce99060a81152aa3f64b34878f7b4cab9a` |

Die binären Input-SHA256 werden über unveränderte Originalbytes geprüft.
Design und Statistik sind zusätzlich im[Wissenschaftsreview](SHARPNESS-SCIENCE-REVIEW.md)
und der endgültige Cold-Runner im[Runnerreview](SHARPNESS-RUNNER-REVIEW.md)
getrennt geprüft. Die eingefrorenen Design-/Analysequellen sind seit diesem
wissenschaftlichen Review unverändert.

## Selbst rekonstruierte Eingaben

Der neue rein lesende Prüfer `analysis/review_sharpness002_results.py` ruft weder
Factory noch Runneraudit als Beweis auf. Er liest die vier tatsächlichen
historischen D00/R01-Konfigurationspaarungen, bindet deren SHA256 an die
veröffentlichten Vorgängermanifeste und konstruiert jede der16 erwarteten
Recordsequenzen selbst. Danach folgt ein vollständiger Bytevergleich mit den
tatsächlich vorbereiteten Dateien und ihren veröffentlichten Setuphashes.

Alle16 Zellen bestanden:5557 Records,3174 Attributwerte für46 aktive Akteure
(23 je Seite),1058 Profilwerte, unveränderte46 Stamina52-Werte60. Die49
Spielerobjekte einschließlich drei unkodierter Auswärtsträger werden nicht als49
native Attributakteure behandelt. Absolute Aufstellungsrecords bestimmen die
zehn getesteten Startfeldspieler; Torwart, Bank, Gegner und übrige Slots bleiben
unverändert. D00 hat das originale Rohpaket10000 in beiden Feldern16/17.

Der originale R01-Carrier enthält genau zehn deklarierte Staminawerte40.
Nach ausschließlich deren Wiederherstellung auf60 bleibt exakt ein Unterschied
zu D00: Pressinggruppe10, ID1313689463→2000905329 (Bit0→66). Für die Arme
`[S70-P0,S100-P0,S70-P1,S100-P1]` ergeben sich je Kontext/Seite exakt
`[20,0,21,1]` veränderte Records. Low verändert ausschließlich beide
Rohprofilfelder16/17 der zehn getesteten Startfeldspieler auf7000; High/Standard
bleibt bytegleich D00. Keine zusätzlichen Attribute, Rollen, PI, Taktikphasen,
Kaderprofile, Positionen, Matchmanagement- oder Kind61-Eingriffe.

Zusätzlich sind die historischen vier Observer-Goldlogs an ihre Originalhashes
gebunden. Deren vorbereitete und erste echte Fortschreibung werden erneut
gelesen und die eingefrorenen Kontrollhashes aller46 identifizierten Akteure
einschließlich Raw33 unabhängig berechnet. Sie stimmen mit den neuen
Kontrollbindungen überein. Keine Rohregionen oder Spieleridentitäten werden
veröffentlicht; deren Hashvergleich ist keine Familiarity-/UI-Kalibrierung.

## Neue und ausgeschlossene Seeds

Öffentlicher Seedplan, private Kopie und bereits vorhandene zentrale Reservierung
sind identisch:64 Mainseeds, vier separate Technikseeds,68 eindeutige uint32.
Die Rekonstruktion liest9426 vorhandene öffentliche/private JSON/JSONL-Belegdateien
und fremde Reservierungen; sie schreibt weder Registry noch neue Seeds.

Ergebnis:2528 historische/reservierte Ausschlüsse einschließlich Null,
TECH17-Metadaten und aller terminal reservierten Staminaseeds. SHA256 über die
kanonisch sortierte Ausschlussliste:
`a59f0a9c5f58a6ba5e6bb938675e63336655bf0871c3e4373e961b2e32cbefa4`.
Kein neuer Seed überschneidet sich damit. Eine eigene SHA256-Namespaceableitung
rekonstruiert die vollständige geordnete64+4-Liste exakt. Holdoutgegner und ihre
Matchdaten werden nicht verwendet; reservierte Seedmetadaten bleiben Ausschlüsse.

## Tatsächliche frühere TECH17-Freigabe

Die konkrete Vorbereitung bindet die frühere unabhängig abgenommene TECH17-Serie
an `4011e17b5e5e6aa75fbbabb63329fd63aca2a514`. Der GitHub-Lauf
[43638521137](https://github.com/Matchekk/FM-27-Research/actions/runs/43638521137)
wurde erneut unabhängig auf exakten Commit, `completed` und `success` geprüft.
Die veröffentlichten Summary-/Reviewgitblobs stimmen mit den eingefrorenen
Releasehashes überein:

- Summary: `77a62b42ec4c6f00dc0254962db869262036751d9a05ed53195f4f1c3d8e0487`.
- Unabhängiger Review: `996240c9fc924a7784b6dbb29e076f99abab34960165bcc35bc1966d55e4876c`.

Releasefile, konkretes Inputmanifest und neuer Vertrag tragen identische
Freigabebindungen. Freigegeben bleibt allein das originale Zwei-Feld-Startpaket
im gebündelten Fixture: Observerhost
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`,
Engineidentität `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Dieser Inputreview startet keinen Host und behauptet keine eigene neue
Live-DLL-/Engineprüfung. Aktuelle geladene Identität und unveränderte
Ressourcen müssen die bevorstehende technische Serie nochmals belegen.

## Offene Ausführungsgates

Zum Reviewzeitpunkt existiert kein eigenes natives `budget.json` dieser Studie.
Der Auditor startet0 native Aufrufe und reserviert0 Seeds. Der zentrale inerte
Prepareaufruf ist getrennt im NIGHT-Programm abgerechnet; er ist kein technischer
Matchnachweis.

Vor der technischen Serie: dieses Review mit exaktem Inputhash verknüpfen;
Vorregistrierung, Quellen, Inputs, Vertrag, Seeds und Review publizieren;
exakte erfolgreiche CI abwarten; registrierte33/512-Jobpläne ebenfalls
publizieren und erfolgreiche CI prüfen. Ein Supervisor, NativeLease, höchstens
vier kalte Worker,90s ohne Fortschritt. Eigene Grenzen900 Childsekunden und
3600UTC-Sekunden erst ab erstem Technikstart, zusätzlich NIGHT1800 Childsekunden
und23UTC. Keine Neustarts, Alternativ-/Ersatzseeds oder verdeckten Zusatzproben.

TECH32+1 muss vier gleichzeitige Claims, alle16 A/A-Paare, tatsächliche vollständige
Eingabe-/Seed-/Identitätsreadbacks,46 Staminawerte60, Raw-/Cacheübertragung in
Vorbereitung/Erstschritt, eingefrorene Kontrollen, natürliche Ergebnisse,
Negativ108/initial/kein NaturalFinish und bestätigtes Kernelzero für jeden Job
nachweisen. Alle begonnenen, fehlgeschlagenen und unbegonnenen Jobs bleiben
erhalten. Die öffentliche32er-Erfolgstabelle ersetzt die Negativkontrolle nicht;
eine getrennte erlaubte33-Job-Evidenzprojektion ist nach tatsächlichem Lauf
aus den privaten Rohbelegen zu rekonstruieren.

Main512 bleibt bis separatem tatsächlichem Technikreview, publizierter
Releasefreigabe und deren erfolgreicher CI gesperrt. Unmittelbar vor dem ersten
Mainaufruf müssen mindestens600s eigener/globaler Child- und UTC-Allowance
nachweisbar bleiben. Keine Holdouts, Karriere-Replays, Warmworker, Setter,
fortlaufenden Clamps oder automatische Erweiterung. Keine UI-, Consumer-,
Mediations- oder allgemeine Karriereübertragbarkeitsaussage.

## Reproduktion und Teststatus

`python analysis/review_sharpness002_results.py inputs --central <zentrales Archiv>`
prüft Quellen, konkrete16 Inputs, vier historische Kontrolllogs und die komplette
Seedherkunft rein lesend. `seeds` prüft nur den Seedplan; spätere `technical`
und `main` verlangen tatsächliche vollständige private Belege. `public-technical`
und `public-main` sind ausdrücklich nur öffentliche Subset-QA, keine private
Readback- oder Ressourcenfreigabe. `verify_publication()` prüft exakte Gitblobs
und den tatsächlichen GitHub-CI-Run mittels reiner Git-/API-Lesezugriffe.

Neun eigene reine Softwaretests bestanden, darunter absichtlich falsche native
Attribute/Profile/Rollen/PI/Seeds/Caches/Raw33/Identitäten, fehlendes Kernelzero,
Claims nach Stop, Retry-/Budget-/UTC-Fehler, falsche CI-Identität sowie fehlende
Hauptdaten. Gesamtsuite334 Tests erfolgreich (drei optionale Privatgoldskips),
zusätzlich fünf historische Analysetests;340 NIGHT- und272 Round3-Archivdateien
unverändert. Nach den letzten eng begrenzten Auditorergänzungen nochmals alle
neun eigenen Tests bestanden. Tatsächliche Sharpness-Technik-/Mainresultate
liegen diesem Review noch nicht zugrunde. Keine Fremdquellen oder eingefrorenen
Dateien verändert.

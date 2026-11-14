# Agent 3 – Training Researcher

**14.11.2026 · Recherche, unabhängige Offline-Nachrechnung und Karriereentwurf.**
Nur dieser Bericht wurde geschrieben. Keine native Simulation, Karrierefortschreibung,
Seedreservierung, Registryänderung, Holdoutnutzung oder Veröffentlichung durch diesen
Agenten. Git-Tracking geprüft: `main` und Remote auf44d6a97 zum Beginn dieses
Teilauftrags; vorhandene P1C-/Agentenänderungen erhalten.

## Forschungsfrage und überprüfter Ausgangspunkt

Welche Trainingspolitik verbessert Entwicklung **und** kurzfristige Einsatzfähigkeit,
und welchen Preis verursacht sie durch Belastung und Verletzungen? Entwicklung,
Matchvorbereitung und Verletzungsrisiko bleiben getrennte Zielgrößen. Ein einzelner
gewichteter „optimaler Trainingsscore“ würde diese Zielkonflikte verdecken.

Lokale DLL rein lesend tatsächlich geprüft: Dateiversion27.0.1,
Produkt27.0.1+2503222. Keine native Kompatibilitätsprüfung dieses Agenten.
[TRAIN-001](../../experiments/TRAIN-001-karriere.md) gehört unverändert zum
historischen Build27.0.0+2493426, Decoderfmsave0.10.0 und Savehash
`b8c8a6c52bbd0d0a8a46abe8e9a44db74445fe550a2c0dfb0ac672c5ca3aad8f`.
Das ist keine aktuelle Karrierefreigabe.

Alle660 veröffentlichten Spielerzeilen in
[`player-deltas.jsonl`](../../data/training/player-deltas.jsonl), Manifest,
Expositions- und A/A-Datei gelesen. Die660 sind wiederholte Spielermessungen,
nicht660 unabhängige Behandlungen. Eine vollständige individuelle Teilnahmehistorie,
Verletzungsdauer und unabhängige Save-Replikate fehlen.

| Teilversuch | Überprüfte Beobachtung | Kausale Grenze |
|---|---|---|
| Zweiwochenpilot | Je22 Spieler/Arm; nur2/5,4/5,1/5,1/5 Zielslots erhalten. | Vorgabe war keine vollständige tatsächliche Intervention; technischer Pilot. |
| Conditioning/Heavy,6Wochen |12/12 Zielslots erhalten;14.801/14.731 Matchminuten und9/4 Verletzungseinträge. | Kalenderbeleg ist keine Teilnahme; ein Karrierearm je Plan, Verletzungseinträge keine Ausfalltage. |
| Conditioning/Rest,U19,4Wochen |8/8 Zielslots;5.940/5.850 Matchminuten,je4 Verletzungseinträge. | Andere Alterskohorte und andere Intervention als Profivergleich; kein isolierter Altersvergleich. |
| Wochenpläne,5Wochen | Profis14/14 undU1915/15 Zielslots erhalten; zwei zusätzliche Profislotabweichungen. U19-I:1 statt8 Verletzungseinträge bei P/R. | Keine belastbare Verletzungsraten- oder Wochenplanrangfolge aus einem Arm. |
| A/A,bytegleiche Eingabe,2Wochen | Attributeprofile16/22 identisch;CA/PA22/22;Kondition8/22;Schärfe13/22. | Kein perfekter Determinismus über sämtliche Felder; Unterschiede sind noch kein Nachweis unabhängiger RNG-Replikate. |

Unabhängig ohne historischen Analyseimport aus den Endcheckpoint-Zeilen gerechnet:
physischer Index=ungewichtetes Mittel der Rohänderungen von Antritt,Tempo,
Beweglichkeit,Ausdauer, anschließend Mittel der22 Spieler.

| Vergleich | Indexänderung Kontrolle / Intervention | Abstand | ΔCA-Abstand |
|---|---|---:|---:|
| Heavy−Conditioning,6Wochen |−0,397727 /−0,375000 |+0,022727 Rohpunkte |+0,090909 |
| Rest−Conditioning,U19,4Wochen |+0,193182 /+0,159091 |−0,034091 Rohpunkte |+0,227273 |

Das sind **neue explorative Deskriptionen historischer Daten**, keine
nachträglichen Primärtests. Rohpunkte nicht ohne Kalibrierung mit gerundeten
1–20-Anzeigepunkten gleichsetzen. Aus Spielervarianz entsteht keine gültige
Treatment-Standardabweichung: die Intervention wurde auf Karrierearme zugewiesen.
Keine inferenzstatistischen Gewinnerintervalle oder Power ausn22 abgeleitet.

Reproduktion der neuen Deskription, ohne Engineimport:

```python
import json, statistics
from pathlib import Path
r = [json.loads(s) for s in Path('data/training/player-deltas.jsonl')
     .read_text(encoding='utf8').splitlines()]
keys = ('acceleration','pace','agility','stamina')
for trial, end, control, intervention in [
    ('conditioning-heavy',6,'A','B'),('conditioning-rest',4,'A','C')]:
    def means(arm):
        v = [x for x in r if (x['trial'],x['checkpoint'],x['arm'])
             == (trial,end,arm)]
        assert len(v) == 22 and len({x['subject'] for x in v}) == 22
        return (statistics.mean(statistics.mean(x['delta']['raw'][k]
                for k in keys) for x in v),
                statistics.mean(x['delta']['ca'] for x in v))
    a,b = means(control),means(intervention)
    print(trial, a, b, tuple(y-x for x,y in zip(a,b)))
```

## Geprüfte externe Evidenz und tatsächliche Forschungslücke

Zugriff14.11.2026; Produkt-/Mechanismusbeschreibung, Fremdbericht und unabhängige
Rohdatenreplikation getrennt. Keine Tabellen-/Save-Downloads oder externe Programme
ausgeführt. Die Quellen liefern keinen belastbaren universell besten Wochenplan.

| Primärquelle / Version | Geprüfte Datengrundlage | Aussage und Grenze |
|---|---|---|
| [SI: FM27 Training & Tactical Effectiveness](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness),FM27-Feature/FAQ | Herstellerbeschreibung, keine kontrollierte Stichprobe/Enginehash. | Beschreibt stärkeren Fokus auf Matchvorbereitung und taktisches Verständnis; individuelle Entwicklung bleibt separat. Belegt Produktabsicht, keine quantifizierte Planüberlegenheit. |
| [harvestgreen22,Originalbericht](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test),seit04.11.2026,verlinkte Trainingstabelle20261103ver2 | Autor beschreibt standardisierte Spieler/Trainer und nennt zwei Gruppen à1000Matches für taktisches Training; keine hier nachgerechneten Karriere-Rohzweige/Seeds/Buildhashes. | Berichtet etwa30% mehr Verständnis und+3,5% Winrate nach acht Wochen-Sessions. Das ist kein kalibrierter kausaler Trainingswochen-Effekt; zeitliche Persistenz bleibt laut Autor offen. |
| [Mac Study3](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/03-tactical-familiarity.md),10.11.,FM27.0.1,Commit849b16f9 |6.900berichtete Einzelmatchsimulationen; zehn gespeicherte Fixtures×30Seeds je Bedingung, künstlich festgesetzte Recordkomponenten. | Liefert Hinweise auf Relevanz der Trainings-/Match-Exposure-Komponenten. Manipulation eines fertigen Recordwertes misst weder Lernen pro Session noch Jugendwachstum oder Verletzungskosten. Mac-Adapter ist keine Windowsfreigabe. |
| [SI: Youth Development FM26](https://www.footballmanager.com/the-dugout/top-tips-youth-development-fm26),ältere Produktversion | Offiziell veröffentlichter Autorenleitfaden, keine randomisierte Trainingsstudie. | Regt altersabhängige Trainings-/Einsatzfragen an; weder feste Altersgrenzen noch quantitative FM27-Wachstumsraten daraus übernehmen. |
| [Geprüfter Windows-Fidelitystand](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/docs/SIMULATION_FIDELITY.md),v1114.6 | Technische Beschreibung, normierte Einzelmatchprofile. | Keine Karrierefortschreibung, Teilnahme- oder Entwicklungsvalidierung. |

Hoher zusätzlicher Erkenntniswert: tatsächlicher Kompetenzzuwachs je ausgeführter
Einheit, Persistenz nach Trainingspause, Alters-/PA-Kontext und Entwicklung gegen
Verletzungs-/Matchvorbereitungskosten. Ein weiterer Downloadplanvergleich ohne
Teilnahme-/RNG-Kontrolle reproduziert hauptsächlich unbekannte Kontexte.

## Technische Voraussetzungen mit Agent VALID

Der [VALID-Bericht](VALID.md) und [VALID-003-Plan](../../experiments/VALID-003-plan.md)
liefern die Abhängigkeiten. `research/career.py` validiert importierte Checkpoints,
führt aber keinen Kalender aus. Seine booleschen Kalender-/Teilnahmeflags müssen
später durch echte Readerreceipts belegt werden. Ein eingetragenes `true` genügt nicht.

1. **Reader-/Einheitengate:** Start-/Enddatum, Cohort-/Spieleridentität intern,
   Attribute inklusive Roh-/Anzeigeabbildung,CA/PA,Alter,Professionalität,
   Verletzungsdisposition und Naturfitness mit Quell-/Buildhash erfassen.
   Namen/Quell-IDs bleiben privat; öffentlicher Teilnehmercode nur innerhalb
   Replikat/Kohorte. Jede nicht lesbare Variable als unbekannt kennzeichnen.
2. **Kalender-/Executor-Gate:** Teamplan,Coachzuteilung,Anlagen,individueller
   Fokus/Intensität,Session/Tag/Slot,tatsächliche Teilnahme,Rest/Reha/Absage,
   Terminverdrängung und tatsächliche Matchminuten protokollieren. Vor und nach
   jedem Wochenadvance kontrollierte Inputs nativ lesen, nicht nur Endkalender.
3. **RNG-/Replikat-Gate:** Innerhalb jedes Paares bytegleiche Ausgangsdatei;
   zwischen Replikaten validierte unabhängige Karriere-Zufallsstreams oder
   echte unabhängige Club-/Save-Starts. Neue isolierte Matchseeds ersetzen diese
   Karriere-RNG-Kontrolle nicht. Gleiche Datei+RNG mehrfach kopieren zählt nicht.
   Ein A/A-Abstand beweist weder Unabhängigkeit noch einen brauchbaren Seedsetter.
4. **Zustands-/Wirksamkeitsgate:** Fitness/Schärfe/Ermüdung und rohe lesbare
   taktische Trainings-/Exposure-Komponenten samt Komponentenherkunft prüfen.
   Der normale Labornormalisierer überschreibt kontrollierte Startzustände;
   Karrierewerte nicht durch diese Defaults als vermeintlich identisch ersetzen.
5. **Sicherheits-/Ausfallgate:** Saveexport/Reload,A/A und falscher Build,
   ungültiger Sessioncode,beschädigter Checkpoint,fehlende Teilnahme negativ
   prüfen. Kalender-/Inputfehler stoppen die abhängige Serie; sämtliche begonnenen,
   fehlgeschlagenen und unbegonnenen Zweige erhalten. Keine Ersatzreplikate.

## TRAIN-002-P0 – konkretisierter Varianz-/Durchführungspilot

Ergänzung des [bestehenden Entwurfs](../../experiments/TRAIN-002-design.md),
**keine neue Registrierung oder Ausführungsfreigabe**. Zunächst nur diesen
kleinen vorregistrierbaren Vergleich planen, keinen Wochenplanoptimierer.

Kontrolle: zwei Conditioning-Slots/Woche. Intervention: genau diese zwölf Slots
in sechs Wochen durch Heavy Conditioning ersetzen. Übrige Wochenstruktur,
Coach/Anlagen/Kader/Gegner/Taktik und individuelle Schwerpunkte/Intensität innerhalb
jedes Replikatpaares identisch. Zwei separat behandelte Altersstrata U19/Profis;
keine Randomisierung des Alters, daher kein isolierter kausaler Alterseffekt.
Paarzuordnung/Branchreihenfolge randomisieren, alle Zweige archivieren.

Primär je Altersstratum: Kohortenmittel des festen vierteiligen Attributindex
nach sechs Kalenderwochen, abzüglich Ausgangswert, dann Intervention−Kontrolle
im unabhängigen Savepaar. Rohpräzision erhalten und vorab auf vergleichbare
1–20-Einheiten kalibrieren. Kleinste praktische Verbesserung als **Planungswahl**
+0,10 kalibrierte Indexpunkte nach sechs Wochen; keine universelle Nützlichkeitsgrenze.
Falls die Skalierung nicht belastbar kalibrierbar ist, keine Registrierung mit
vorgegebener Power oder dieser Schwelle. Zwei primäre Alterskontraste,Holm2;
95-%-marginale und97,5-%-Bonferroni-Intervalle plus vollständiger Paarbootstrap.

Die Baselinekohorte bleibt der primäre Intention-to-treat-Nenner, einschließlich
verletzter/nicht trainierender Spieler. Feste **Rotations-/Minutenpolitik** und
exogene Fixturetermine einfrieren. Tatsächliche Minuten können wegen durch Training
verursachter Verletzung/Fitness differieren und sind dann Wirkung/Mediator.
Nachträgliches Zwangsmatchen, Neustarten oder Ausschließen solcher Spieler würde
Teile des Gesamteffekts wegkonditionieren. Input-/Durchführungsfehler davon vorab
trennen. Keine Datenimputation zu Null; bei nicht lesbaren Endpunkten nur technischen
Status, keine complete-case-„Gewinner“ unter weiter trainierenden Spielern.

Sekundär eine vorab vollständig benannte Holm20-Familie: je Altersstratum
(1)ΔCA,(2)zeitliches Konditionsmittel,(3)Schärfemittel,(4)Ermüdungsmittel,
(5)Mittel der acht lesbaren taktischen Trainingsbeiträge,(6)tatsächliche
Punkte/Match,(7)xGD/Match,(8)verletzungsbedingte Ausfalltage je1000Kohorten-
Kalendertage,(9)Trainingsverletzungsereignisse/1000Trainingsstunden,
(10)Matchverletzungsereignisse/1000Matchstunden. Die gewählten Komponenten und
Einheiten müssen vor Ausführung einzeln kalibriert/lesbar sein; keine nachträgliche
Ersetzung eines nicht vorhandenen Feldes. Verletzungsraten benötigen Cluster-/
Zählmodell und können bei wenigen Replikaten nur deskriptiv auswertbar sein;
fehlende Testdefinition blockiert Registrierung dieser inferenziellen Familie.
Gesamtscores/Tore/Expositionsminuten/Verletzungstypen zusätzlich deskriptiv.

Trainingseffizienz ergänzend je Arm als Kohortenindexzuwachs pro Kalenderwoche
und je100tatsächlich absolvierter Spieler-Trainingsstunden berichten. Kein
Individuenmittel bloßer Quotienten und keine Gleichsetzung von Kalenderslot mit
Teilnahme. Der Stundennenner kann selbst Treatmentfolge sein; die Kennzahl ist
keine separat identifizierte direkte Trainingswirkung. Bei unbekannter/Null-
Exposition keinen Quotienten bilden. Entwicklung, Vorbereitung und Risiko nicht
zu einem nachträglichen kombinierten Siegerwert zusammenziehen.

## Stichproben, Präzision und Rechenkosten

Unabhängige Einheit: gepaartes Save-/RNG-Replikat, **nicht Spieler, Woche oder
Einzelmatch**. Für jedes Altersstratum eigene unabhängige Replikate. Werden
stattdessen beide Alterskohorten aus denselben Saves gemessen, ihre Abhängigkeit
explizit clustern und keine zusätzliche Replikatzahl behaupten.

| Budgetentwurf | Neue unabhängige Paare/Stratum | Karrierearme insgesamt | Armwochen | Wöchentliche Checkpoints einschließlich Start |
|---|---:|---:|---:|---:|
| Kleiner Varianzpilot |8|32|192|224|
| Größerer Pilot,später separat entscheiden |16|64|384|448|

SD der **gepaarten Kohortenindexdifferenz** unbekannt;0,10/0,20/0,30 sind nur
Planungsszenarien. Individuelle TRAIN-001-SDs sind dafür nicht einsetzbar.
Zweiseitige nichtzentrale t-Planung,konservativα0,025 pro Alterskontrast,
keine90-%-Garantie beide Kontraste gleichzeitig zu entdecken:

| SD-Annahme | Volle95-%-Breite bei8 Paaren | Power für+0,10 bei8 | Breite bei16 | Power bei16 |
|---:|---:|---:|---:|---:|
|0,10|0,167|53,2%|0,107|92,1%|
|0,20|0,334|14,3%|0,213|34,2%|
|0,30|0,502|7,4%|0,320|15,5%|

90-%-Power erfordert unter diesen Annahmen16/53/115 **neue Paare je
Stratum**, also64/212/460 Karrierearme und384/1272/2760 Armwochen.
Kein Vorschlag, diese hohen Zahlen automatisch auszuführen. Pilot-SD samt
Obergrenzen und pragmatische Fragestellung zuerst prüfen; bei sehr kleinen
Effekten oder großer Streuung Design vereinfachen statt unbegrenzt klonen.

Reproduktion der Tabellen: für nPaare,SDs,Effektδ0,10,
`SE=SD/sqrt(n)`, `c=t.isf(.025/2,n-1)` und
`Power=nct.cdf(-c,n-1,δ/SE)+nct.sf(c,n-1,δ/SE)`;
95-%-volle Breite=`2*t.isf(.05/2,n-1)*SE`.
Ganzzahlige n aufsteigend ab2 bisPower≥0,90 geprüft, nicht gerundet geschätzt.

Native Einzelmatch-Benchmarks sind **keine Karriere-Laufzeitmessung**.
Bei bloß angenommenen10/30/60s pro Karrierearmwoche benötigt die kleine Variante
32/96/192Minuten, die große64/192/384Minuten, jeweils plus Reader-/Startkosten.
Zuerst technischer Benchmark mit höchstens2 unabhängigen A/A-Paaren×2Wochen
=8Armwochen, festem30-Minuten-Gesamtcap und einem seriellen Karriereexecutor.
Technischer RNG-/Kalenderfehler stoppt; keine wissenschaftliche Power aus diesem
Benchmark. Native Prüffunktionen global nur über Director,≤4Engine-Worker.

Bedingte spätere Hardcaps nach Benchmark: kleine Variante120Minuten,große240Minuten
kumulierte beaufsichtigte Ausführung sowie180/360Minuten feste UTC-Fenster,
keine Budgetneustarts. Bei höherer gemessener Laufzeit vor Registrierung neu
planen oder kleiner technisch bleiben; **in diesem Auftrag keine Ausführung**.
Private Save-/Checkpointartefakte vorab vermessen; maximal64/128GiB als
Budgetvorschlag,freie Reserve zusätzlich20GiB. Ohne passende Plattenplanung
kein Lauf. Keine Spieldatei oder personenbezogene ID in Git.

Pro1000simulierte Einzelmatches lässt sich kein seriöser Entwicklungsgewinn
angeben: das Ergebnis hängt von tatsächlichen Karrierewochen, Teilnahme und
unabhängigen Savepaaren ab. Rechenressource in Armwochen und gemessener Wallzeit
planen, Erkenntnisgewinn in präziserem gepaarten Politik-/Entwicklungskontrast.

## Langfristige Forschungsroadmap ohne Ausführung

1. **Jetzt:** Reader-/RNG-/A/A-/Kalender-/Teilnahme-/Einheitengate zusammen mit VALID;
   gesonderte technische Vorregistrierung. Isolierte Matchsimulationen ersetzen es nicht.
2. **Danach:** kleiner TRAIN-002-P0 als Durchführung/Varianzfrage, keine endgültige
   optimale Wochenplanwahl. Kurzfristige Leistung und Sechswochenentwicklung getrennt.
3. **Neue Frage:** gleiche Zahl gezielter taktischer Sessions konzentriert versus
   verteilt,vier bis sechs Wochen plus vorab fixierte Auswaschphase. Primär
   Persistenz eines nativ lesbaren Trainingsbeitrags; echte Stunden/Matchlast
   kontrollieren. Ein Record-Hold aus Mac-Studien beantwortet diese Lernfrage nicht.
4. **Jugend:**24-Wochen-Verlauf mit festen individuellen Fokusarmen,PA-/Alter-
   Strata und getrennten Club-/RNG-Clustern; Wachstumskurven,Plateaus/Ermüdung,
   Verletzungen und späterer Matchbeitrag. Fallzahl nach unabhängiger Pilot-SD;
   keine lineare Extrapolation von sechs Wochen auf eine Saison.
5. **Später:** Coachqualität,Fokus,Intensität und Spieldauer einzeln auditieren;
   nicht alle gleichzeitig ändern. Behandlung von durch Verletzungen entstehender
   Nichtteilnahme vorab festlegen, Originalausfälle erhalten.

## Implementierungs-/Teststatus und nächste konkrete Schritte

**Implementiert:** ausschließlich dieser Bericht. Öffentliche TRAIN-001-Daten
unabhängig arithmetisch geprüft, A/A-/Kalendergrenzen aus Originalarchiv gelesen,
oben angegebene SciPy-Power-/Präzisionswerte tatsächlich offline gerechnet.
Die erste Dateninspektion traf auf historische Feldnamenunterschiede
`raw_condition` versus `condition`; die anschließende Indexnachrechnung nutzt
nur die in beiden betroffenen Versuchen vorhandenen `raw`-/CA-Felder.
Kein nativer Fehler oder Datenersatz. Keine neuen Unit-Tests, weil weder Code
noch Daten geändert wurden; zentrale CI und Independent Review erfolgen beim Director.

**Blockiert:** Karriereexecutor, nachgewiesene unabhängige RNG-Replikate,
individuelle Teilnahme und Verletzungsdauer, aktuelle Roh-/Anzeige-Kalibrierung,
lesbare dynamische Taktikkomponenten. `automatic_game_execution_validated=False`
bleibt maßgeblich. Kein Trainingsplan ist durch diesen Auftrag als überlegen bestätigt.

**Nächste Schritte:** Independent Reviewer prüft n/Clustereinheit/Mehrfachtests
und die Mediatorbehandlung; VALID spezifiziert unverwechselbare Readerreceipts;
Director priorisiert den kleinen technischen Karrierebenchmark gegenüber einer
noch nicht durchführbaren Hauptstudie. Erst nach technischen Gates neue konkrete
Vorregistrierung/Code/Budget/Seeds publizieren, niemals automatische Fortschreibung.

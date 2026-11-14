# Agent 2 – Attribute Researcher

Stand 14.11.2026. **Recherche und Design, keine neue native Ausführung, keine
Seedreservierung und keine Änderung historischer Studien.** Verantwortungsdatei
nur dieser Bericht. AGENTS, Methodik, Plattform, Roadmap und ATTR-001–007 wurden
geprüft; fremde Änderungen bleiben erhalten. Historische ATTR-Daten betreffen
FM27 **27.0.0+2493426**. Die aktuelle lokale DLL meldet27.0.1+2503222
([zentraler Versionsbeleg](../../data/tact-001-p1c/environment.json)); daraus folgt
keine automatische Replikation der alten Attributbefunde.

## Forschungsfrage und überprüfter Ausgangspunkt

Warum liegt Jumping Reach in unserem Standardfixture teilweise vor Pace,
während internationale Tabellen häufig Pace/Acceleration priorisieren?
Das ist zunächst ein Unterschied **konkreter Eingriffe und Kontexte**, kein
Widerspruch universeller Attributgesetze. Zu klären ist insbesondere, ob die
positionsübergreifende Vertrautheit des synthetischen Kaders den relativen Nutzen
von Sprunghöhe gegenüber Geschwindigkeit verändert.

| Eigene Studie | Eingriff und Datengrundlage | Tatsächlicher Befund und Grenze |
|---|---|---|
| [ATTR-001](../../experiments/ATTR-001-screening.md) |16 Attribute, je40 gepaarte Seeds; zehn Feldspieler12→16,680 Matches | Pace+0,288, Acc+0,274, JR+0,239 xGD; alle BH-q≥0,404. Die Screeningreihenfolge war selbst Pace/Acc/JR, ohne korrigierten Nachweis. |
| [ATTR-002](../../experiments/ATTR-002-hauptreplikation.md) |240 neue Seeds, gemeinsame Baseline plus fünf Attribute,1.440 Matches | JR+0,316, Acc+0,229, Pace+0,144 xGD. Sekundär JR−Pace+0,172 [0,052;0,291]; JR−Acc+0,087 [−0,042;0,218], Reihenfolge JR/Acc offen. Kein universeller Rang. |
| [ATTR-003](../../experiments/ATTR-003-zusatzszenarien.md) |360 Matches; Pace/Acc, gegnerische Mentalität und Seitenübertrag | Kontextintervalle breit; JR dort gar nicht geprüft. Kein Beleg, dass JR gegen jede Gegner-/Seitenbedingung führt. |
| [ATTR-004](../../experiments/ATTR-004-ergebnisse.md) |1.120 disjunkte Tripel/3.360 Matches, acht Formation×Mentalität×Seiten-Szenarien | JR−Acc **+0,021 xGD [−0,038;+0,080]**. Beide Baselineeffekte positiv; ihr mittlerer Abstand ist klein. Punkte: JR+0,184, Acc+0,215 gegenüber Baseline; Rangrichtung hängt auch am Endpunkt. |
| [ATTR-005](../../experiments/ATTR-005-ergebnisse.md) |100 neue Neunarmblöcke/900 Matches, vier Positionsgruppen | Keine der zwölf Primärtests nach Holm signifikant. Gruppen umfassen zwei oder drei behandelte Spieler; daraus keine fein aufgelösten Einzelspielergewichte ableiten. |
| [ATTR-006](../../experiments/ATTR-006-ergebnisse.md) |300 neue Paare/600 Matches, JR12→16 an AMR/AML/ST |+0,171 xGD [0,052;0,290], p0,00498; Punkte+0,107 [−0,064;0,278], Holm0,4018. Positiver xGD-Effekt im damaligen Kontext, keine gesicherte Punktesteigerung. |
| [ATTR-007](../../experiments/ATTR-007-ergebnisse.md) |200 neue Achtarmblöcke/1.600 Matches, JR an drei Angreifern faktoriell | Shapley(ST)+0,103 xGD, Holm0,0065; ST−Flügelmittel+0,088, Holm0,104. Isolierte ST-Aufwertung+0,020 [−0,105;0,146]. Shapleybeitrag ist kein isolierter Einzelspielereffekt. |

Die ursprüngliche ATTR-Baseline standardisierte **16 untersuchte Attribute**, nicht
notwendigerweise alle69. Zehn Feldspieler12→16 unterscheiden sich von einer
±5-Änderung am ganzen Kader einschließlich Bank und Torwart. Effekte weder durch
Spielerzahl noch Attributpunkte teilen und als allgemein lineare Gewichte ausgeben.

Unabhängig aus allen3.360 öffentlichen ATTR-004-Messungen neu gerechnet, ohne
Import des Analyseprogramms: JR−Acc=0,02118996256758929,
SE=0,029955219891332444, df1080,018251948208,
95-%-t-KI[−0,03758705906299281;0,07996698419817139].
Acht vollständige140-Tripel-Strata, kein fehlender Arm. Das bestätigt die
veröffentlichte Zahl, nicht ihre Übertragbarkeit auf den aktuellen Build.

## Quellenregister und externe Evidenz

Abgerufen14.11.2026. Bei dynamischen Foren ist der Abrufstand angegeben;
GitHub-Studien sind an Commit **849b16f9c4057598da33b255649c86d8cecb525b**
gebunden. Fremde Rohjobs/PKM wurden weder heruntergeladen noch simuliert.
Extern berichtete Zahlen sind **keine von uns unabhängig reproduzierten Resultate**.

| Quelle / Version | Datengrundlage und Endpunkt | Bewertung |
|---|---|---|
| [FM-Arena: aktueller Player-Attributes-Thread](https://www.fm-arena.com/threads/player-attributes.59/), ZaZ/squirrel_plays,10.–14.11.2026 | Aufbereitung von Harvestgreen, Attributstufen1/6/12/18, Winrate; berichtet Pace/Acc/Stamina vorn und stärkeres JR oberhalb12. Kein eigener offener gepaarter Seed-Datensatz im Thread. | Sekundäre Zusammenfassung; Rang und lineare Interpolation sind keine neue unabhängige Replikation. |
| [Harvestgreen22: Originalbericht](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test),04.11.2026, FM27, exakter Enginehash nicht angegeben | Autor nennt18-Jährige, PA150,180cm/70kg, Ausgangsattribute12, Gegenpress4-2-4/4-4-2, fünf Gegnerformationen×100 Matches je Niveau, mindestens51.000 Fälle. Über1→18: Winrateänderungen Pace59,4, Acc48,1, JR33,4 Prozentpunkte laut Bericht. | Eigenbericht; Build-/Seed-/Clusterbelege fehlen. Jahreskalender, Trainings-/Coachzustand und gesperrte Werte unterscheiden sich vom isolierten Labormatch. Nicht als51.000 unabhängige Replikate behandeln. |
| [FM-Arena: FM24-Attributtabelle](https://fm-arena.com/table/26-player-attributes-testing/) und [Methodenpost](https://fm-arena.com/thread/14009-attribute-testing-football-manager-24/page-4/), FM24 | Historische8→20-Vergleiche, tatsächliche Saisonpunkte/Tore. Alte Haupt-URLs waren beim Direktabruf teils404/Timeout; indizierter Methodenpost lesbar. | Kein aktueller FM27-Nachweis; vollständige Rohdaten/Versionierung hier nicht reproduziert. Keine Zahlen aus Screenshots erfinden. |
| [Mac Study1](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/01-attribute-values.md),27.0.1,10.11.2026 |32.700 Matches,54 Attribute, zehn gespeicherte Fixtures×30 Seeds; ganze Mannschaft±5, gekappt1..20. Bericht: xGD pro Attributpunkt Pace0,102, Acc0,094, JR0,068; ppg0,071/0,066/0,033. | Reproduktionscode vorhanden, Rohjobs privat; ein Club, feste Fixtures, viele Tests. Exakter für diese Studie geladener Binärhash nicht aus dem Bericht belegt. |
| [Mac Study2](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/02-real-vs-levelled.md),11.11.,65.400 zusätzliche Matches | A echte Profile/Fixtures, B nivellierte Profile/echte Fixtures, C nivelliertes generisches Sample. Pro+5 xGD: Pace A0,51/B0,69/C0,15; Acc0,47/0,44/0,26; JR0,34/0,28/0,32. | C zeigt die qualitative JR/Acc/Pace-Verschiebung unseres Fixtures. B→C ändert mehrere Kontextbestandteile gleichzeitig, isoliert weder Taktik noch Positionsrating kausal. |
| [Mac Study12](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/12-thresholds.md),13.11.,21.000 Matches |13 Attribute, acht Niveaus1..20,200 Paare/Niveau, synthetische Premier-League-Profile, Gegenpress, vier Gegner, beide Seiten. xPts-Dosisverläufe: Speed flacher oberhalb≈12, JR steiler oberhalb≈9. | Knieposition datengetrieben gesucht; keine vorregistrierten universellen Schwellen. Ausgangsniveau ist eine konkrete Alternativerklärung. xPts bildet tatsächliche Verwertung nicht vollständig ab. |
| [Mac Study13](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/13-value-by-position.md),13.11.,15.680 Matches | Acht Attribute, fünf Gruppen àzwei Spieler+5,320 Paare/Bedingung; zusätzlich1/3/6/11 behandelte Spieler. Keine hinreichend klaren feinen Positionsunterschiede. | Anders als ATTR-005 gleiche Gruppengröße. Nichtsignifikanz ist keine Gleichheit; Spieleranzahl und Auswahlreihenfolge sind bei Mengenkurven gebündelt. |
| [Mac Study14](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/14-team-strength.md),13.11.,8.800 Matches | Zehn Attribute, fünf moderate Stärkepaarungen,160 Paare/Bedingung; berichtet Heterogenität p0,81 auf xPts. | Begrenzter Stärkebereich/ein Stil; p0,81 beweist keine Stärkeinvarianz. Keine Übertragung auf extreme Leistungsabstände. |
| [Mac Study17/17b](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/17-positions-in-and-out-of-possession.md),13.11.,3.200+1.600 Matches | Aktive IP/OOP-Ratings auf10 bei drei/vier Spielern: unklare kleine Effekte;17b kontrastiert aktive/alle Feldspielerratings und GK. Alle Feldratings zu kappen schadet stärker; GK-Kappung betrifft vor allem Saves/Gegentore. | Bereits vorhandene Evidenz für Positionsrating-Haupteffekte, keine neue globale Frage. Ein Stil/Profil; Management als mögliche Mitursache, unbekannte externe Rohprovenienz. |
| [PierreSmague/FM23_attribute_analysis, Notebook](https://github.com/PierreSmague/FM23_attribute_analysis/blob/df8ee6bd492f8f810443b83249b77e32387863db/Ds_project.ipynb), Commitdf8ee6bd492f8f810443b83249b77e32387863db | Öffentliches Notebook mit saisonalen Spielerbeobachtungen, Positionsmodellen und selbst gewichteter Leistungszielgröße aus Ratings/Statistiken/Reputation. Externe HTML-Daten; Matchanzahl und exakter Build hier nicht belegt. | Code überprüfbar, in diesem Auftrag nicht ausgeführt. Beobachtungsregression beantwortet Prognose, keinen isolierten Attributkausaleffekt. FM23 ist kein FM27-Replikat. |

Das [Mac-Projekt](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/README.md)
ist ausdrücklich macOS-spezifisch; dessen Saved-Match-/Managementadapter ist keine
Windowsfreigabe. Mehrere Studien desselben Tools und Clubs zählen nicht als
mehrere unabhängige Labore. Weitere veröffentlichte globale Ranglisten ohne
prüfbare Eingaben/Rohdaten werden hier nicht als belastbare Zusatzbestätigung geführt.

## Welche Erklärungen sind plausibel, welche belegt?

| Erklärung | Was die Quellen tatsächlich ermöglichen | Konsequenz |
|---|---|---|
| Ausgangsniveau/Nichtlinearität |12→16 liegt bei JR im extern vermuteten steilen Bereich; Speed-Vorteile über1→18 oder±5 schätzen andere Strecken. | Später gleich große lokale2-Punkt-Inkremente z.B.8→10 und14→16 testen, keine nachträgliche optimale Kniesuche. |
| Profile/Fixture | Mac A/B/C zeigt Bündelunterschiede; eigene Baseline standardisiert andere Attribute und andere Spieleranzahl. | Eine einzige Kontextkomponente gezielt ändern. |
| Formation/Rollen | ATTR-004 änderte Formation samt zugeordneten Rollen; seine Kontexttests schließen relevante Interaktionen nicht aus. | Keine reine Formationswirkung aus dem vorhandenen Bündel behaupten; Rollen einzeln nativ prüfen. |
| Mannschaftsstärke | Moderate externe Stärkevariationen erlauben keine universelle Invarianz. | Eigene realistische Stärkeprofile erst nach VALID-003; nicht mit CA allein gleichsetzen. |
| Positionsvertrautheit | Study17/17b untersucht Positionsrating-Haupteffekte bereits; eine gekreuzte relative JR/Speed-Wirkung ist dort nicht getestet. | Höchster zusätzlicher Erkenntniswert: gezielter Positionsrating×Attribut-Kontrast. |
| xGD/Punkte | Eigene ATTR-004-Punktrichtung JR/Acc unterscheidet sich deskriptiv von xGD; ATTR-006-Punkte unsicher. | Tatsächliche Scores erhalten; ein xG-Effekt ist kein bestätigter Punktgewinn. |

## Neuheitsabgleich mit Study17/17b

Bericht und [Definitionscode `s17`/`s17b`](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/port/validation/roadmap_studies.py)
wurden gezielt nachgelesen: Sie variieren Positionsratings, **keine gekreuzten
JR-/Acceleration-/Pace-Aufwertungen**. Unser Zusatznutzen ist ausschließlich die
vorab definierte **relative Attributwirkung×Ratingmaske-Interaktion**. Ein bloßer
neuer Positionsrating-Haupteffekttest wäre weitgehend Doppelarbeit. Das belegt
Neuheit gegenüber diesen geprüften Spezifikationen, keine weltweite Neuheitsgarantie.
Unsere aktive Maske bleibt20, nur ungenutzte Feldfamilien ändern sich; GK konstant.
Die Stufe1 ist ein bewusst extremer Sensitivitätstest, keine realistische Kaderverteilung.

## Vorgeschlagenes Experiment: ATTR-009-bridge-P0

**Designentwurf, kein reservierter Registereintrag und keine Ausführungsfreigabe.**
Ergänzt den bestehenden [ATTR-008-Entwurf](../../experiments/ATTR-008-design.md),
überschreibt ihn nicht. ATTR-008 fragt nach lokalen Grenzwerten/Position/Taktik;
dieser kleinere kausale Brückenversuch fragt nach einer spezifischen Fixtureeigenschaft.

Hypothese: Die Positionsratings des Testteams verändern den relativen
xGD-Nutzen von Jumping Reach gegenüber Acceleration/Pace.
Eigene feste IP-4-2-3-1 und dieselbe OOP-Struktur in allen Zellen; zwei bestehende
Discoverygegner `high_press`/`deep_block`, keine gehaltenen Gegner oder Daten.

Zwei kontrollierte Ratingmasken des **Testteams**: O=vorhandene
positionsübergreifende Feldspielervertrautheit. Der veröffentlichte
[P1B-Profilvertrag](../../data/tact-001-p1b/inputs.json) benennt Feldspieler-GK/Sweeper
als0 und Familienindizes2..14 als20; GK-Slots0/11 haben GK20, übrige Ratings0.
Dies wurde im lokalen Discovery-D00-Konfigurationssatz lesend gegengeprüft,
ohne personenbezogene IDs zu übernehmen. S=bei Feldspielern natürlich20 in
allen tatsächlich benötigten IP-/OOP-Positionsfamilien, übrige Feldfamilien1;
GK/Sweeper-Werte und die beiden Torwartvektoren bleiben **unverändert**. Das ist eine kontrollierte Spezialisierungs-
maske, noch kein realistischer kompletter Kader. Gegnerprofil unverändert.
Kein gleichzeitiger Wechsel von Körper, Alter, Fähigkeiten, Taktik oder Management.
Die Fähigkeit, genau diese Vektoren ohne versteckte Normalisierung zu schreiben
und nach Originalvorbereitung zu lesen, ist ein zwingendes neues technisches Gate.

Je Maske vier Arme: B=JR/Acc/Pace bei denselben zehn Feldspielern auf12;
J=nur JR16; A=nur Acc16; P=nur Pace16. Torwart/Bank und alle anderen Attribute
konstant. Ein zentral neu reservierter Seed bindet alle2×4Arme auf beiden Seiten:
**16 Matches je unabhängigen Block**. Unterschiedliche Seeds für beide Gegner.
Keine Aussage über einen „Attributpunkt pro Einzelspieler“.

Primär pro Seite `R=Y(J)−½Y(A)−½Y(P)` auf xGD, dann
`D=R(S)−R(O)`, Seitenmittel im Seed und Gegnergewichte je½.
Armkosten/Baseline dienen auch der Plausibilität; B fällt aus diesem Primärkontrast
algebraisch weg. Ein zweiseitiger Testα0,05, praktisch relevantes
Interaktionsziel0,30 xGD, gewünschte volle95-%-Breite≤0,50 als Pilotziel.
Die Schwelle ist eine **Planungsentscheidung**, kein aus den Daten geschätztes MDE.
Welch-Satterthwaite-t-KI,20.000 vollständige stratifizierte Seedblock-Resamples,
SD je Gegner und einseitige SD-Obergrenzen mit Modellannahmen.

Genau elf sekundäre Tests als eine Holm-Familie: derselbe D-Kontrast auf
Punkte/GF/GA/xGF/xGA (5), plus J−B/A−B/P−B auf xGD für jede Maske,
gleichgewichtet über Gegner (6). Keine zusätzlichen Rangtests.
Punkte3/1/0 und Tore vollständig berichten. Ein späterer Anwendungsnachweis
würde Punkte primär benutzen und neue realistische Kontexte separat registrieren.

## Stichproben, Kosten und erwarteter Erkenntnisgewinn

Die SD des **neuen zusammengesetzten Interaktionskontrasts** ist unbekannt.
SD1,0/1,5/2,0 sind reine Szenarien, keine Übernahme der ATTR-004-Einzelkontrast-SD.
Balancierte unabhängige Gegnerstrata; folgende Zahlen direkt mit SciPy-t/nct
berechnet, df=Gesamtblöcke−2 bei den angenommenen gleichen Stratumvarianzen.

| Variante | Seeds/Gegner | Unabhängige Blöcke | Hauptmatches | Volle95-%-Breite bei SD1/1,5/2 | Power für0,30 bei SD1/1,5/2 |
|---|---:|---:|---:|---|---|
| Kleiner Varianzpilot |16 |32 |512 |0,722 /1,083 /1,444 |37,6% /19,5% /13,0% |
| Größerer Pilot |32 |64 |1.024 |0,500 /0,750 /0,999 |65,6% /35,0% /21,9% |

Damit ist auch die große Variante kein garantierter Interaktionsnachweis.
Für eine neue90-%-Bestätigung von0,30 wären unter SD1/1,5/2 genau
60/133/235 neue Seeds **je Gegner**, also1.920/4.256/7.520 Matches nötig;
für0,20 bereits4.256/9.504/16.864. Eine unbegrenzte Skalierung wird nicht empfohlen.
Wenn der Pilot nur kleine Unterschiede zulässt oder breit bleibt, zuerst die
technische/profilebezogene Frage anders vereinfachen; keine automatischen Zusatzseeds.

Effizientere aktive Kontrolle bei ausschließlichem Primärziel: Da B algebraisch
nicht in D eingeht, könnten seine Hauptmatches **vor Registrierung** entfallen.
Dann kosten32/64 vollständige Blöcke384/768 Matches,25% weniger bei unverändertem
Kontrast und angenommener gleicher SD; die sechs Baselineeffekte entfallen dann
und die sekundäre Familie umfasst nur fünf Tests. Das ist eine theoretische
Kosteneinsparung, kein gemessener Varianzgewinn. Die hier vollständig beschriebene
512/1.024-Variante kauft zusätzlich diese sechs absoluten Effektschätzungen.
Der Director muss **eine** Variante vorab wählen, keine adaptive Umschaltung.

Technikentwurf separat:32 Eingabezellen einmal plus acht vorab bestimmte
A/A-Wiederholungen und eine ungültige Eingabe=40 Vollmatches+1Negativversuch.
Alle1058 bisherigen Profilfelder, sämtliche Positionsratings/abgeleitete
Ausführungswerte und69 Attribute nach Originalvorbereitung auditieren.
Große/spezifische Positionseignungsänderung muss wirksam sein; unveränderte
Scores werden nicht als Nachweis ignorierter Eingaben interpretiert.
Bei fehlender Readbackdeckung blockieren, statt eine Wirkung durch Resultate zu erraten.

Kostenannahme **0,7 beaufsichtigte Child-Sekunden je Vollmatch**, konservativer
Planungsanker aus dem vier-Worker-P1B-Durchsatz, keine neue Messung:
552/1.064 Gesamtvollmatches ≈386/745s plus Vorbereitungs-/Publikationspausen.
Vorgeschlagene harte Caps600/1.200s Child-Zeit,1.200/2.400s unverrückbares
UTC-Fenster; maximal4Worker,90s ohne Fortschritt, keine Retries/Ersatzseeds.
Die zentrale Koordination muss den Anker vor endgültiger Registrierung aktualisieren.
Alle Seeds ausschließlich zentral reservieren, keine parallelen Registrywrites.

Erkenntnisgewinn pro1.000Matches: im großen Design62,5 unabhängige komplette
Interaktionsblöcke; im kleinen dieselbe Rate, jedoch breitere Intervalle.
Das ist ein rechnerisches Informationsmaß, **kein gemessener Varianzgewinn**.
Bei angenommener SD1 beträgt die asymptotische volle95-%-Breite für1.000Matches
≈0,496 xGD (mit endlichen df etwas größer). Das erklärt die Grenzen kleiner
Interaktionsforschung und begünstigt die kleine Variante als technische/Varianzfrage,
bevor eine größere wissenschaftliche Serie entschieden wird.

## Technischer und wissenschaftlicher Status

**Implementierung:** nur dieser Recherche-/Designbericht; kein neuer Runner,
keine Profiländerung, kein nativer Start. Vor Ausführung sind VALID-003A,
vollständiger JSON-Vertrag und eigener deterministischer Kontrastcode erforderlich.
Konkrete Sourceprüfung, mit VALID abgeglichen: Der normale
`validate_scenario`-Pfad übernimmt die ersten15 Attributfelder als Positionsratings
0..20, standardisiert aber `native_profile` mit `CONTROLLED_START`.
`away_tactic_pool.uniform` kann aktive IP-/OOP-Ratings20 sowie Fähigkeitsfelder15..68
pauschal überschreiben; dieser Pfad muss im Brückenversuch nachweislich fehlen.
`experimental_execution` darf nicht still die abgeleitete Effektivität ersetzen.
DM-L/R und DC-L/R teilen Ratingfamilien; keine unabhängigen L/R-Vertrautheits-
parameter erfinden. Sollvektoren aus der tatsächlichen Positionsindexabbildung
ableiten. Diese Sourcebefunde sind noch kein bestandener nativer Audit.
Die Masken/OOP-/GK-Ausführungswerte sind heute nicht interventionsspezifisch freigegeben.
Gespeicherte Karriere-PKM bleiben gesperrt.

**Prüfung in diesem Teilauftrag:** vorhandene Dokumente/Manifeste/Messungen
lesend geprüft; ATTR-004-Primärzahl unabhängig aus Rohzeilen reproduziert;
Szenario-Power und ganzzahlige Fallzahlminima berechnet. Diese Offline-Rechnungen
starten keine Engine. Externe Mac-Analysen und das FM23-Notebook wurden gelesen,
nicht ausgeführt; keine externe Rohdatenreplikation. Keine Repositorytests als
neu bestanden behauptet, zentrale CI und Independent Review folgen beim Director.

**Offene Unsicherheiten:** neue Kontrast-SD, genaue Rolle der übrigen
Positionsratings/GK-Spezialisierung, Attributnormalisierung/abgeleitete Effektivität,
Kompatibilität des Windows-PKM-Kontexts, externe Rohprovenienz und Generalisierung.

**Nächste konkrete Schritte:** Independent Reviewer prüft Kontrast-/Kostenarithmetik
und Quellenreichweite; VALID identifiziert einzeln schreib-/lesbare Ratingfelder;
Director entscheidet zwischen technischem Maskenaudit und bestehendem ATTR-008-
Dosisentwurf. Erst danach neue Vorregistrierung samt Seeds/Code veröffentlichen.
Neue bestätigende Daten bleiben von Entdeckung getrennt, alte Archive unverändert.

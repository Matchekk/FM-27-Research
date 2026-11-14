# Agent 4 – Set Piece Researcher

**14.11.2026 · Quellenprüfung, vorhandene technische Belege und Design.**
Keine neuen nativen Starts, Seedreservierungen, Registry-/Runneränderungen,
Karriere- oder Holdoutzugriffe. Ausschließlich diese Datei geschrieben.
Historische SET-001-Entwürfe bleiben unverändert. Veröffentlichung/CI zentral.

## Forschungsfrage, Forschungslücke und Erkenntnisgewinn

Welche eigene Standardroutine erhöht den Ertrag **je tatsächlich ausgeführtem
Standard**, ohne durch Konter den Vorteil zu verlieren? Zunächst muss die
Messkette zwischen zugesprochener Situation, ausgewählter Routine, wirklicher
Ausführung, Ballbesitzkette, Schuss-xG und endgültigem Tor technisch nachweisbar
werden. Ein Zähler für Routineauswahl ist keine Exposition.

Der höchste unmittelbare Informationsgewinn liegt im Messbarkeitsgate, nicht
im Downloadturnier. Danach eine einzelne eigene Routinekomponente testen;
kurz/lang, ein-/auslaufende Bälle, Zielzonen/Laufwege und Profile nicht zugleich
ändern. Eine pauschale Rangliste ohne Exposition beantwortet diese Frage nicht.

AGENTS, Methodik, Plattform, Roadmap, Findings, SET-001 und der
[VALID-Bericht](VALID.md) wurden gelesen. DLL-Dateiversion rein lesend:
27.0.1, Produkt27.0.1+2503222. Freigegebener Kontext v1114.6,
Commit91f2eba57fac0b7fbd3dff616056907e3ce461be; keine erneute native
Kompatibilitätsprobe durch diesen Agenten.

## Geprüfte externe Evidenz

Abruf14.11.2026. Diese Quellen ersetzen keine neue FM27-Eingabe-/Zählerfreigabe.

| Primärquelle / Version | Datengrundlage und geprüfte Aussage | Evidenzgrenze |
|---|---|---|
| [Tactics Lab Setpiece-Codec](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_setpieces.py), v1114.6 | Typisierte Routinen, Strategien, Swing, Aufgaben-/Backupgruppen, Rollenzuordnung und Wurfstile werden normalisiert/kodiert. | Implementierungsbeleg, kein Eingabe-/Leistungsnachweis unserer neuen Routinen. |
| [Nativer Host](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp#L847) und [Episodenpfad](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_setpiece_episode.h), gleicher Commit | Selektionszustände und erste qualifizierende Episode sind technisch vorhanden. | Kein geprüfter Zähler aller legal ausgeführten Standards; Episode ist kein Vollmatch. |
| [Mac Study8](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/08-tactical-tweaks.md),11.–12.11.2026 | Teil2: fünf gespeicherte Fixtures×12Seeds×zehn Gegner,600 Paarungen je Tweak; Torwart-bei-Standards über das ganze Match berichtet−0,17Punkte/+0,28GA. | Ganzmatch-Tweak statt Routinevergleich; keine Zahl tatsächlicher Standards/Konterketten. Mac-Adapter und private Rohjobs hier nicht repliziert. Kein isolierter Konterkausalnachweis. |
| [Sports Interactive, Match Days FM26](https://www.footballmanager.com/the-dugout/maximising-your-match-days-fm26), Herstellertext, Abrufstand | Beschreibt neue visuelle Perspektiven für Ecken/Freistöße. | Produkt-/Darstellungsbeleg, keine FM27-Effektgröße oder wissenschaftliche Routineempfehlung. |
| [Lucey et al., Quality vs Quantity, Sloan2015](https://global-uploads.webflow.com/5f1af76ed86d6771ad48324b/5fee09c092fcdb0989d51ecf_1034_rppaper_SoccerPaper5.pdf) | Originalstudie:9.732Schüsse aus353Spielen einer anonymisierten Profiliga; trennt Schusskontexte und berücksichtigt räumliche/strategische Merkmale. | Beobachtungsdaten echter Spiele, keine randomisierte Routinewirkung und keine Übertragung ihrer Raten auf FM27. Schussverwertung ist nicht Ertrag je zugesprochener Ecke. |
| [StatsBomb/Hudl Open Data](https://github.com/hudl/open-data), dynamischer Abrufstand14.11.2026 | Dokumentiert offene JSON-Ereignis-/Matchdaten und separate Schemadokumentation als methodisches Vorbild. | Hier kein Datensatz ausgewertet; dessen Ereignisdefinitionen sind keine native FM-Semantik. |

Der gesuchte2018er Sloan-Originalbericht zu Set-Piece-Mythen ließ sich über den
Originalendpunkt nicht zuverlässig abrufen. Deshalb werden verbreitete Aussagen
über angeblich bessere Inswinger/Outswinger daraus **nicht** als geprüft geführt.
Auch einzelne Downloads/Forenempfehlungen sind keine reproduzierte Zusatzstudie.

## Tatsächlicher lokaler Messstand

Nur erlaubte technische Full-event-Belege aus VALID-002 gelesen, keine neuen
Simulationen. Beide Dateien gehören zum **gleichen** Seed2362620850 und
wiederholen denselben0:0-Endstand/Endtick22651; sie sind keine unabhängigen
Matchstichproben und keine Schätzung von Standardhäufigkeiten.

| Beleg unter ignoriertem `local/valid002-run1/full-events/` | SHA256 | Zeilen |
|---|---|---:|
| home_baseline-2362620850-r0.jsonl | `bd16b50548b28afc71c61d2a32472995b1fc2204ef46f304a8f9bd630d759cd7` |112|
| home_baseline-2362620850-r1.jsonl | `5f4860ee770addac04333a4fa2c5eec42c48468aa7300f01c9e28b131ea066e6` |122|

Je Datei52 `native_setpiece_selected`-Zeilen an26verschiedenen Ticks: jeweils
Angriff und passende Abwehr werden protokolliert. Selektions-Typzahlen:
Ecke15/15, direkte Freistoßtypen1/1, seitliche4/4, entfernte2/2,
Einwurf4/4. **Das sind keine nachgewiesenen15 ausgeführten Ecken usw.**
Die zwei Logs haben unterschiedliche Bootstrapbelege, dieselben52Selektions-
Tupel. Keine personenbezogenen Spielerfelder oder vollständigen Rohlogs publiziert.

Der Host hält je Team einen Key aus Deadballtyp, Routineart und Variante;
gleichbleibende Keys werden nicht erneut protokolliert, erst der Austritt aus dem
relevanten Zustand setzt sie zurück. Es fehlt eine eindeutige Ausführungs-ID mit
belegtem Ballkontakt. Eine Zustandsänderung kann Auswahl/Abbruch bedeuten;
nicht jede protokollierte Seite ist das angreifende Team.

Der Eventcollector `fm27_match_events.py` reconciliert Tore/Karten gegen native
Endregister und Spielertotale. Die gelesenen Full-event-Logs enthalten keine
Schuss-xG-/Besitzwechselkette, sondern aggregierte `native_match_statistics`.
`native_xg_models_parsed` ist ein Ladebeleg, kein Schussereignis. Daher fehlen
hier die Daten für xG je Ecke und kontrollierte Gegenkonterattribution.
Der0:0-Beleg enthält zudem keinen positiven Standardtor-/VAR-Testfall.

Episodenmodus: erster passender Typ5..9/Seite, Start beim Deadballzustand;
„Delivery“ wird aus dessen Verlassen abgeleitet. Fenster5..120Sekunden,
Vorgabe30; interne Rechnung verwendet4Clockeinheiten/Sekunde und weitere
60Sekunden Settlement. Er beendet mit `full_match_completed=false` und
liefert Teamstatistikdifferenzen des Fensters. Das ist weder Nachweis eines
wirklichen Ballkontakts noch ein Vollmatchzähler oder reine Standard-xG-Summe.
Clock-/Tickabbildung und Attribution müssen gesondert validiert werden.

Read-only Quellhashes: Runtime `fm27_setpieces.py`
`c1ef500a0591174624db5ad47d17e624284f3cdeb1bde407568bf64aa67f6f65`;
Upstream `native_setpiece_episode.h`
`311e04ee09de7a08a140908a3918e1344c3259db68dc7cde4be41657c204e49b`;
`native_match_events.h`
`197cb8c5c8dce17a543eb5886eb15bca9e497a8cec485e9bb1588f56f345f462`.

### Vorhandenen SET-001-Entwurf vor Registrierung bereinigen

`research/specs/SET-001-draft.json` plant64Blöcke in **einem** Kontext und
256Matches; seine `power_basis` nennt abweichend32Blöcke und eine t-Planung
für0,10xGD. Der gemeinsame generische Matchanalysator implementiert keinen
Expositionsquotienten. Zudem ist die sekundäre Familie im Markdown breiter als
im JSON. Diese Widersprüche blockieren Registrierung. Originalentwurf erhalten;
eine neue konkrete Version muss Fallzahl, Endpunkt-Einheit, komplette Familie
und eigenen Ratencode konsistent einfrieren, statt die alten Angaben still zu übernehmen.

## Messbarkeitsgate SET-V0 / VALID-003D – nur Entwurf

Zuerst minimaler, versionierter Ereignisvertrag, kein Ranking:

- `match_id`, Build/Host/Inputhash, Seed, Seite, monotone Ereignis-ID,
  Periode, nativer Tick und validierte Matchzeit.
- `awarded_id`, Typ und angreifende Seite; eigene Felder für zugesprochen,
  Routine ausgewählt, tatsächlich freigegeben/ausgeführt, abgebrochen,
  regelwidrig/wiederholt. Alle Versuche erhalten; legale abgeschlossene
  Ausführung als vorab definierter primärer Nenner, Wiederholungsversuche extra.
- Tatsächlicher Schütze/Empfänger nur privat, öffentliche pseudonyme Zuordnung;
  Routinehash, tatsächlicher Fuß/Ziel-/Laufweg, Taker-/Rollenzuordnung nach
  Originalvorbereitung. Endstand und endgültige Torereignisse reconciliieren.
- Besitzwechsel mit Quelle, Schuss-ID und ursprünglichem nativem Schuss-xG,
  endgültiger Torstatus/VAR-Storno. Keine xG-Verteilung aus Matchsummen schätzen.
- Originalkette endet bei nächster Unterbrechung oder kontrolliertem gegnerischen
  Besitz; daraus entstehende Konterkette endet bei Unterbrechung, erneutem eigenen
  kontrollierten Besitz oder10Sekunden validierter Matchzeit. Nächster Standard
  startet eigene Kette; keine Doppelattribution. Alternative10/20Sekunden nur
  vorab als Sensitivität, nicht nach Ergebnis auswählen.

Minimaler Goldtrace-Satz, unabhängig annotiert: kein Standard; Auswahl ohne
Ausführung; eine echte Ausführung mit vielen Zustandssamples; gleiche Routine
zweimal; Angriff/Abwehr desselben Standards; kurz gespielt mit zweiter Flanke;
Wiederholung; Halbzeit/Grenzuhr; Ecke→Schuss→Tor; VAR-Storno; Besitzwechsel→
Konterschuss/Gegentor; neuer Standard statt fortlaufender alter Kette.
Parser muss unbekannte/mangelhafte Eingaben ablehnen und Missing markieren.
Ein eigener synthetischer Trace prüft Parserlogik, **nicht** die native Semantik.

Künftige native technische Serie nach veröffentlichtem neuen Code/Hashes/Seeds:
8Eingabezellen(2Routinearme×2Discoverygegner×2Seiten) zweimal =16Vollmatches,
8exakte A/A-Vergleiche; dazu≤4negative Probes für unerlaubte Routine/Taker/
korrupten Trace/Identitätsdrift. Budget≤600s Child-Zeit,1200s feste UTC-Frist,
4Worker global,90s ohne Fortschritt,4GiB private Artefakte/20GiB Diskreserve.
Beide Teams/phasen, Aufgaben/Backups/Prioritäten, tatsächliche Taker/Foot,
Seed und Naturabschluss vollständig auditieren. Fehlende seltene Ereignistypen
in diesen16Matches sind **keine** bestandenen Zählertests; Gate bleibt für
unabgedeckte Typen blockiert, keine stillen Zusatzseeds. Positiv-/Negativ-Goldfälle
und zweite unabhängige native Quelle müssen alle behaupteten Typen abdecken.
Hoständerungen benötigen neue technische Freigabe; VALID-002 nicht überschreiben.

## Wissenschaftlicher Folgepilot nach bestandenen Gates

**Vorschlag SET-002-R0**, nicht registriert. Erster klar lesbarer Faktor:
eine eigene feste direkte Eckroutine mit Swing0(Inswinger) gegen1(Outswinger),
Zielzone NearPost0, alle Aufgaben/Restabsicherung/Profile/Teaminstruktionen und
geordneten Schützenlisten konstant. Katalogmitgliedschaft wurde nur gelesen;
keine neue native Eingabefreigabe. Wenn Swingpolitik die tatsächliche Schützenwahl
ändert, misst der Vergleich die **Politik einschließlich dieser Auswahl**, nicht
isoliert Ballkrümmung. Nicht nachträglich solche Situationen ausschließen.

Zwei bekannte Discoverygegner, gleiche synthetische Stärke, beide Seiten;
32neue Seeds/Gegner =64 unabhängige Viermatchblöcke =**256Hauptmatches**.
Größere separate Variante64/Gegner =128Blöcke/**512Matches**. Keine Holdouts.
Keine Mindestexposition durch nachträgliche Verlängerung erzwingen.

Primär Differenz des Netto-xG-Ertrags pro100 **ausgeführte legale Ecken**:
Summe eigener Eckketten-xG minus Summe gegnerischer unmittelbarer Konterketten-xG,
geteilt durch tatsächliche Eckexposition. Zuerst Quotient je Arm×Gegner×Seite,
dann Seite/Gegner jeweils½. Kein Mittel über einzelne Matchquotienten mit
Nullnennern. Vollständige Seedblöcke innerhalb Gegner resamplen, mit beiden
Armen/Seiten/Nennern und Zählern gemeinsam;20.000Clusterbootstrapziehungen,
95-%-Intervall. Nullgesamtexposition eines benötigten Stratum ist undefiniert,
keine Nullersetzung oder Weglassen des Stratum. Auch jede Bootstrapziehung muss positive Nenner in allen benötigten Strata haben.
Vorgeschlagene konservative Stopregel für den neuen Vertrag: Sobald eine Ziehung
Nullnenner erzeugt, Primär-KI als nicht berechenbar markieren und Zahl/Strata der
undefinierten Ziehungen vollständig berichten. Keine Ziehungen verwerfen oder
ersetzen, kein KI aus der verbleibenden Teilmenge. Dann nur Mess-/Expositionsstatus,
kein inferenzieller Leistungsnachweis. Ein anderes für sparse Nenner geeignetes
Verfahren darf ausschließlich vor neuer Registrierung methodisch validiert und
festgelegt werden, nicht nach Sichtung der Leistungsrichtung. Das genaue
Intervallverfahren und seine Randfalltests bleiben Vorregistrierungsvoraussetzung.

Prospektive praktische Schwelle **+2,0Netto-xG/100Ecken**, gewünschte volle
95-%-Breite≤4,0 als Pilotziel. Das ist eine Planungsentscheidung, keine gemessene
MDE oder garantierte Power. Neun sekundäre Tests(Holm9): Tore/100Ecken,
eigenes xG/100Ecken, Konter-xG/100Ecken, Kontertore/100Ecken, Ecken/Match,
Netto-xG/Match, Punkte/Match, GF/Match, GA/Match. Defensive Gegentore je
gegnerischem ausgeführten Standard separat deskriptiv; eine echte defensive
Routinenintervention bekommt eigenen Vertrag. Endstände vollständig erhalten.

Routine kann Exposition verändern: bedingter Ertrag je Ecke ist kein kausaler
Gesamteffekt des Spiels. Unbedingte Netto-xG-/Punkte-/Torwerte gehören zwingend
daneben. Höchstens ein eingefrorener Vergleich, keine Gewinnerwahl aus Varianten.

### Exposition, Stichprobenplanung und Kosten

Aktuelle Eckrate/Clusterstreuung sind **unbekannt**, die52Selektionszeilen
liefern keinen kalibrierten Nenner. Bei rein angenommenen2/5/8ausgeführten
Ecken pro Testteam-Match ergäben256Matches128Matches/Arm und256/640/1024
Ecken/Arm. Bei512Matches verdoppelt sich das. Weder Paarungsgewinn noch
Ereignisunabhängigkeit behaupten; Karten/Spielstand erzeugen Clusterabhängigkeit.

Zur Größenordnung nur unabhängige Bernoulli-Normalnäherung, zweiseitigα0,05,
90%Power:2%→3% Tore/Ecke bräuchte≈5121Ecken/Arm,3%→5%≈2016/Arm.
Das ist **keine** Powerplanung des Netto-xG-Primärtests, keine gemessene FM-Rate
und wegen Clusterung/Paarung/Multiplikität nicht als echte Fallzahl freigegeben.
Schon200Ecken/Arm hätten bei angenommener3%-Torquote eine naive95-%-
Halbbreite≈2,36Prozentpunkte. Seltene Tore brauchen wesentlich mehr Exposition;
xG hilft nur, wenn es ereignisbezogen valide messbar ist.

Nach Pilot: gemeinsame Verteilung von Nenner und Nettoertrag je Seed/Gegner/
Seite sowie Überdispersion pilotieren. Bestätigungsplanung mittels eingefrorener
Cluster-/Expositionssimulation unter vorab gewählten Verbesserungen, nicht naiver
Match-t-Fallzahl. Ohne diese Varianz keine belastbare90-%-Primärpower angeben.

Bedingter Rechenanker0,7Child-Sekunden/Vollmatch, keine neue Messung:
256+16≈190s,512+16≈370s ohne zusätzliche Event-/Auditkosten. Vorschlags-Caps
900/1200s Child-Zeit und1800/2400s feste UTC-Frist; technische17..20Versuchsplätze
separat exakt bestimmen, nie ungeprüft wiederverwendete technische Seeds.
Full-event-Aufzeichnung kann deutlich teurer sein als P1B-Quickruns; dieser
Kostenanker ist keine Benchmarkgarantie. Globale Maximalgrenzen bleiben4Worker,
90s ohne Fortschritt, kein Retry/Seedersatz.

Pro1000Matches liefert ein Zweiarm-/Zweiseitendesign≈250unabhängige Seedblöcke,
bei angenommener Eckrate5 etwa2500Ecken/Arm. Das ist eine Rechenrate, kein
bewiesener Informationsgewinn. Der zusätzliche Erkenntniswert ist die Trennung
von Routineeffizienz, erzeugter Exposition und defensivem Preis, nicht die größte
simulierte Spielzahl.

## Weitere Suchräume, Status und nächste Schritte

Nach erster Messfreigabe sequenziell statt kombinatorischer Vollsuche:
kurze Kombination vs direkte lange Lieferung (zunächst genaue native Semantik
festlegen); NearPost/Central/FarPost bei konstanter Swingpolitik;
Zielspieler-/Laufwegpaket mit gleicher Restabsicherung; danach Profilinteraktionen
wie Zielspielersprungkraft oder Schützenfähigkeit. Jeder Profilwechsel braucht
VALID-003 und keine gleichzeitige versteckte Positions-/Fitnessänderung.
Freistöße getrennt nach direkter/seitlicher/ferner Situation; Einwürfe nach
Feldzone. Der gelesene UI-/Codecpfad besitzt für vordere Einwürfe Stil0/1
(kurz/lang), für andere Zonen Besitzhalten/entlang Linie; tatsächliche Ausführung
kann von Fähigkeit, Raum und Spielzustand abhängen. Auswahlflag ist kein Flugnachweis.

**Implementierungsstatus:** nur dieser Bericht und Ereignis-/Goldtraceentwurf.
Kein neuer Zähler/Parser/Runner und keine neue native Messfreigabe implementiert.
Scheinzähler aus dem vorhandenen Selektionslog wären unsicher; deshalb kein
solcher Code ergänzt. **Prüfstatus:** zwei bestehende Logs rein lesend gehasht/
gezählt, Selektions-Tupel verglichen, Typ-/Quellpfade gelesen, bedingte
Binomial-/Kostenarithmetik offline ausgeführt. Externe Studien nicht repliziert.
Eine Konsolenausgabe mit Unicode-Labels musste auf ASCII-JSON umgestellt werden;
keine native Aktion oder Quelldatei betroffen. Keine Tests für einen nicht
implementierten Parser als bestanden ausgegeben; zentrale CI folgt beim Director.

**Nächste Schritte:** Independent Review prüft Nenner/Attribution und Familien;
VALID legt passive Ausführungs-/Schuss-/Besitzreceipts fest; eigenen strikt
validierenden Parser und synthetische Goldtraces im nächsten technischen Auftrag
implementieren; anschließend veröffentlichte native Zählerabnahme. Erst dann
SET-002-R0 registrieren. Bis dahin kein Routine-Leistungsvergleich, keine
Karriereausführung und keine neue Hauptserie.

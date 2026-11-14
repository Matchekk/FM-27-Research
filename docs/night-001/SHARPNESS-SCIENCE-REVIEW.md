# Unabhängiger Wissenschaftsreview: MECH-002-SHARPNESS-P0

Stand: 2026-11-14. Prüfer im separaten Branch `codex/night-sharpness-science-review`.
Dies ist ein Offline-Review von Design, Eingabefactory und Statistik; keine
native Freigabe und kein wissenschaftliches Matchergebnis.

## Gegenstand und Status

Geprüfter Ausgangsstand: `6a97ca0342312ada5713781dc68337d835506723`
(Designautor `011c4ec`), mit finalem Designerfix
`e63e40fef56e2d30bab57fb034014a5300c04635` (lokaler Reviewcherry `6db59b4`,
quellgleich mit Directorintegration `b135754`). Der Review umfasst
`analysis/sharpness002_design.py`, `analysis/analyse_sharpness002.py`, den
JSON-Vertragsentwurf, Vorregistrierung, Planungsdokument und Designer-Tests.
Die ausführbare Reviewreproduktion liegt in
`analysis/review_sharpness002_science.py`; eigene Regressionen in
`tests/test_sharpness002_science_review.py`.

**Design, Statistik und korrigierte Offline-Factory bestanden.** Im Ausgangsstand
erwartete die Factory49 statt46 aktive Attributträger. Der unabhängige reale
Binär-Goldnachlauf reproduzierte den Fehler. Der finale Fix verlangt strikt46,
23 je Seite; fehlende, doppelte und49er-Inventare werden abgewiesen. Alle16 realen
Outputzellen sind danach unabhängig bytegenau geprüft. Diese Softwareprüfungen
ersetzen weder TECH17-Abnahme noch Studientechnik, tatsächliche CI, Runnerreview
oder Ressourcenfreigabe; der Review erteilt keine native Startgenehmigung.

Finale Quellenbindung, SHA256 über Bytes mit ausschließlich CRLF→LF:

| Datei | SHA256 |
| --- | --- |
| `analysis/sharpness002_design.py` | `2baa7bec34f1bb013a710861a6e3bab617f6e844b2b6402c259190b4eb084ba0` |
| `analysis/analyse_sharpness002.py` | `e9131272561892067abdd1ceb18c02e7267ccb0da2b8680e4db179e8b0f6dec8` |
| `data/mech-002-sharpness-p0/contract-draft.json` | `8822b45ca76131ef90823e695431ca33c4ddfc302cb2fa4cf9276c2905f52a63` |
| `experiments/MECH-002-sharpness-pilot.md` | `9b0751337f5f6e4c17ddc4299ee001d86d1ffd61576cab8c2aadfa69703c11d8` |
| `docs/night-001/SHARPNESS-PLAN.md` | `b10a1fc9da8631429ceb9a86c81415320f542363baf0bf75681be2e029778411` |

## Unabhängige mathematische Rekonstruktion

Der Prüfer erzeugt512 ausdrücklich synthetische Rohscore-/Team-xG-Zeilen. Nur
Schema und Identitätshülle stammen aus der Designer-Testfixture; sämtliche
Scores und xG-Werte werden unabhängig überschrieben. Die Konstruktion enthält
ungleiche Kontextstreuungen, Seiteneffekte, positive und negative
Seitenkovarianzen sowie unterschiedliche Punkte-/Tor- und xG-Effekte. Sie ist
keine FM-Beobachtung und liefert keine empirische Power- oder Wirkungsaussage.

Aus Rohscores werden tatsächliche Punkte3/1/0 sowie getestetseitig GF/GA und
xGF/xGA neu abgeleitet. Für Armanordnung `[S70-P0,S100-P0,S70-P1,S100-P1]`
rekonstruiert der Review unmittelbar:

- Schärfepaket: `((b-a)+(d-c))/2`.
- Pressing: `((c-a)+(d-b))/2`.
- Physische Interaktion: `(d-c)-(b-a)`, nicht der um Faktor4 kleinere
  Regressionskoeffizient einer ±1-kodierten Interaktion.

Zuerst werden die beiden Seiten innerhalb jedes vollständigen Seeds gemittelt;
danach erhalten die zwei Kontextmittel jeweils Gewicht1/2. Damit sind64
Seedblöcke die Replikate, nicht512 unabhängige Matches. Die unabhängige Rechnung
verwendet `statistics` und explizite Formeln statt der Projektkontrastmatrix,
`einsum`, Projektmetriken oder Projekt-Statistikfunktionen. Die Projektanalyse
wird erst anschließend zum Vergleich aufgerufen.

Für alle acht vorab festgelegten Kontrast-/Endpunktkombinationen stimmen
Mittelwerte, Standardfehler, Welch-Satterthwaite-Freiheitsgrade, zweiseitige
95-%-Intervalle und p-Werte,20.000 deterministische stratifizierte
Seedblock-Bootstrapziehungen, Kontext-SD einschließlich normalmodellabhängiger
einseitiger95-%-Obergrenzen, Seitenkovarianzen und vollständiges
Leave-one-seed-out überein. Alle512 abgeleiteten Kontrastzeilen werden einzeln
geprüft. Lineare Kontraste vor dem Blockbootstrap zu kollabieren bewahrt hier
dieselbe Blockresampling-Verteilung. Seiten als unabhängig zu behandeln liefert
in der Testkonstruktion nachweislich eine andere und falsche Varianz.

Synthetischer Kontrollwert: marginaler Schärfepaketkontrast0,220;
physische Interaktion0,090. Diese Zahlen sind ausschließlich Software-Goldwerte.
Holm wird unabhängig über exakt sieben Sekundärtests nachgerechnet. Der separate
Primärtest ist keine achte Holm-Komponente; daraus folgt keine gemeinsame
5-%-Familienfehlerkontrolle über sämtliche acht Tests. Kontext-, Seiten-,
LOO- und15 Cache-/Rawbeschreibungen bleiben explorativ/deskriptiv.

## Präzision und Interpretation

Eine unabhängige lineare ganzzahlige Suche reproduziert die projektseitige
binäre Suche für neue unabhängige Bestätigungsseeds: gleiche feste
Kontextgewichte, nichtzentrale Welchapproximation, zweiseitig alpha0,05,
90% bedingte Power für0,20/0,30xGD,2n Blöcke und16n Matches. Die simultane
95-%-SD-Obergrenze verwendet je Kontext97,5% mit31 Freiheitsgraden und ist
normalmodellabhängig; sie ist keine robuste verteilungsfreie Garantie.

Als reiner Softwaretest mit angenommenen Kontext-SD0,8/1,2 ergeben sich für
0,20/0,30xGD138/62 neue Seeds je Kontext beziehungsweise2208/992 Matches.
Mit den simultanen SD-Obergrenzen sind es243/109 beziehungsweise3888/1744.
Dies sind keine Schätzungen der tatsächlichen FM-Kontraststreuung und keine
zusätzlichen genehmigten Simulationen. Die512er-Studie ist ein Präzisionspilot;
praktische Referenz0,30xGD und gewünschte volle KI-Breite0,50 begründen keine
vorab bewiesene90-%-Power.

Identifizierbar ist nur der totale Matcheffekt des gemeinsam veränderten
Zwanzig-Record-Startpakets im eingefrorenen synthetischen Kontext. S70/S100 sind
Rohpaketnamen. Keine validierte UI-Skala, kein isolierter Consumer-,
Ermüdungs-, Familiarity- oder Mediationsmechanismus, keine Karriereübertragung,
kein Taktiksieger und keine nachträgliche Kandidatenauswahl.

## Reale Offline-Eingabekontrolle

Vier vorhandene private D00/R01-Paarungen, beide bekannten Gegnerkontexte und
beide Teamseiten, wurden ausschließlich als eingefrorene Konfigurationsbytes
gelesen. Keine Spielstände, Engine oder Holdouts wurden geöffnet; keine privaten
Spieleridentitäten werden publiziert. Jede D00-Datei enthält5557 Records,3174 Attributwerte und1058
Profilwerte für46 aktive Akteure,23 je Seite. Die49 Spielerobjekte der
Konfiguration einschließlich drei zusätzlicher Auswärtsträger sind keine49
aktiven Attributrecord-Akteure.

In R01 sind genau zehn getestete Startfeldspieler in Stamina52 auf40 und genau
ein Pressingrecord geändert. Nach Wiederherstellung dieser zehn Werte auf60
bleibt ausschließlich der Pressingunterschied Standard→MoreOften. Die
getesteten zehn Akteure werden unabhängig über absolute `lineup[1:]`-Records
bestimmt. Für jede der vier Kontext×Seite-Zellen werden alle vier Factoryoutputs
mit einer unabhängig aus D00 aufgebauten vollständigen Recordliste verglichen.
Ergebnis in Armanordnung:20,0,21,1 geänderte Records, ausschließlich20 deklarierte
Profilwerte und/oder ein Pressingrecord. S100-P0 ist bytegleich D00. Alle46
kodierten Staminawerte bleiben60, kein Kind61-Record. D00 und R01 sind vorher
gegen die öffentlich registrierten Setup-SHA256 geprüft. Der Reproduktionscode
kann die16 Output-SHA256 ausgeben; kein Binärmaterial wird veröffentlicht.

## Verbindliche Ausführungsgrenzen und Tests

Entwurf und vollständige synthetische Messdaten überstimmen keine fehlende
TECH17-Releasefreigabe; eine eigene Regression weist diesen Fall ab. Ein
wohlgeformtes Receipt ist kein Beweis erfolgreicher publizierter CI oder
tatsächlicher Ressourcenabrechnung. Diese Tatsachen müssen der separate
Supervisor und der unabhängige technische Reviewer vor Export prüfen.

Vor Technik bleiben veröffentlichte Code-/Input-/Seed-/Preregistrierung,
exakte erfolgreiche CI, tatsächliche unabhängige TECH17-Freigabe und
unveränderte Identitäten zwingend. Vor Main zusätzlich32 valide Technikmatches,
16 A/A-Paare, eine eindeutige Negativabweisung, eigener technischer Review und
publizierte Freigabe. Vier Worker, ein Supervisor und NativeLease;900 eigene
Childsekunden und3600UTC-Sekunden ab erstem Technikstart, NIGHT1800Childsekunden
und23UTC. Vor Main müssen mindestens600s eigener und globaler Child- sowie
UTC-Allowance verbleiben. Kein Main bei Gatefehlern, keine Retries oder
Ersatzseeds, Holdouts oder automatische Erweiterung.

Fehlende/fehlgeschlagene Eingaben blockieren sämtliche Effektauswertung;
Begonnenes, Fehlgeschlagenes und Unbegonnenes bleibt in der technischen
Abrechnung. Nur zwei fertige Cachemittel dürfen mit explizitem Fehlgrund fehlen.
Öffentlich nur freigegebene Messungen und Provenienz, keine privaten Rawregionen,
Identitäten oder geschützten Dateien.

Eigene Tests: vier reine Softwaretests bestanden. Gemeinsam mit den zwölf
Designer-Tests16 Tests bestanden, einschließlich des ausdrücklich konfigurierten
privaten Designer-Goldtests; der unabhängige private Goldnachlauf lief zusätzlich
erfolgreich für alle16 Zellen. Vollständiger Testnachlauf:325 Tests erfolgreich,
davon drei optionale Privatgoldtests im Standardlauf übersprungen, plus fünf
historische Analysetests bestanden. Historische Archive:
340 NIGHT-Dateien und272 Round3-Dateien unverändert. Dieser Reviewer
startete0 native Engineprozesse/Matches, reservierte0 Seeds und änderte keine Registry.
Lokaler Reviewcommit wird dem Director zur Integration übergeben; kein eigener Push.

Reproduktion ohne Engine: `python -m unittest tests.test_sharpness002_science_review`
und `python analysis/review_sharpness002_science.py`. Optionaler privater
Konfigurationsnachlauf: letzteres mit `--private-root <zentrales Archiv>`;
dies liest nur bereits vorhandene Konfigurationsbytes/JSON und schreibt nichts.

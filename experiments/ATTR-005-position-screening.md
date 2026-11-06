# ATTR-005 – Position-Specific Attribute Research

**Vorregistrierung · 2026-11-06 · Exploratives Screening**

[ATTR-002](ATTR-002-hauptreplikation.md) und [ATTR-004](ATTR-004-ergebnisse.md) fanden xGD-Gewinne bei gleichzeitiger Aufwertung aller zehn Feldspieler. ATTR-005 untersucht die acht Eingriffe auf jeweils eine Positionsgruppe und prüft innerhalb jeder Gruppe den direkten Attributkontrast. Die Arbeitshypothese ist, dass sich die Effekte mit den eingesetzten Positionsgruppen ändern. Alle Tests sind zweiseitig.

## Fixture und Arme

Das validierte Standardfixture entspricht ATTR-002. Das Testteam spielt zu Hause im 4-3-3 mit Ball gegen ein 4-2-3-1, beide gegen den Ball im 4-4-2 und mit Mentalität 4. Die nativen Standardkader umfassen 23 und 26 Spieler. Startelf, Rollen, Gegner, Taktik und kontrollierte Startprofile bleiben über die Arme gleich. Die unveränderte Kontrollvariante ist die standardisierte ATTR-002-Baseline mit denselben 16 Attributen auf Rohwert 60 (Anzeige 12) bei den zehn Heimfeldspielern.

| Gruppe | Positionen mit Ball | Größe |
|---|---|---:|
| Innenverteidiger (CB) | DCR, DCL | 2 |
| Außenverteidiger (FB) | DR, DL | 2 |
| Zentrales Mittelfeld (CM) | DMC, MCR, MCL | 3 |
| Angriff (FW) | AMR, AML, ST | 3 |

Die Zuordnung zu Kaderplätzen folgt ausschließlich aus dem nativen Baseline-Readback. Der Adapter muss für jeden Startplatz die tatsächliche Ballbesitzposition und Rollenbindung nach der Spielvorbereitung melden. Das Readback der Startelf wird über lokale Spielerkennungen mit den Setup-Kaderplätzen abgeglichen. Die vier Gruppen müssen sich zu genau zehn verschiedenen Feldspielern ergänzen. Pro Gruppe entstehen zwei Arme. Genau ein Attribut wird bei den zugeordneten Spielern von Rohwert 60 auf 80 (Anzeige 12→16) gesetzt, JumpingReach (Index 54) oder Acceleration (Index 49). Der Vergleich der vollständigen binären Eingaben muss ausschließlich diese Änderungen zeigen. Torwart, Ersatzspieler und Gegner verbleiben auf ihren Baseline-Werten. Die Gruppen unterscheiden sich auch in Spielerzahl, Rollen und Spielermischung. Gruppenunterschiede sind Effekte des jeweiligen gesamten Eingriffs.

## Seeds und Freigabe

100 neue Seed-Blöcke mit jeweils neun Armen ergeben 900 vollständige Hauptmatches. Für die Validierung zwei separate Seeds, jeweils alle neun Arme zweimal (36 vollständige Prüfmatches). Der Seedgenerator entnimmt die ersten vier SHA-256-Bytes von `ATTR-005/{validation|main}/{Zähler}` als Little-Endian-uint32. Der Zähler startet je Phase bei null. Null, bereits vergebene Seeds und alle archivierten Matchseeds aus VALID-001, ATTR-001 bis ATTR-004 und den historischen Matchserien werden übersprungen. Alle Arme eines Blocks teilen genau einen Seed und die zugehörige Baseline. Gehashte Job-Schlüssel legen die Reihenfolge innerhalb der technischen Teilserie bzw. Hauptserie fest.

- Freigabe erst nach Push dieser Vorregistrierung und des Analysecodes. Engine `27.0.0+2493426`, Adapter, Host, Fixture, Quellhashes und Ressourcenfingerabdruck müssen mit [VALID-001](VALID-001-adapter.md) und dem [ATTR-004-Manifest](../data/attr-004/manifest.json) übereinstimmen. Bei inkompatiblem Build oder Identitätsabweichung bleibt der native Matchlauf gesperrt.
- Zuerst vier Baseline-Prüfläufe. Die tatsächliche Startelf und Positionskarte müssen in allen vier Läufen übereinstimmen. Anschließend die 32 Interventionsprüfläufe mit vollständigem Readback aller aktiven Attributvektoren, Positionen, Rollen, Mentalitäten und Startprofile. Je Seed und Arm müssen Endstand, native Teamstatistik und Endtick exakt wiederholbar sein. Eine getrennte ungültige Binärkonfiguration muss mit Exitcode 108 scheitern.
- Im Hauptlauf dieselben Identitäts-, Readback- und Ergebnisprüfungen für jeden Job. Wirksamer Seed-Override, Start 0:0, natürlicher Abschluss vor dem Watchdog, vollständige plausible Teamstatistik und ganzzahliger Endstand sind Pflicht. Lab-Quick-Modus, maximal vier Worker und 90 Sekunden ohne Fortschritt als Timeout.
- Höchstens ein Wiederholungsversuch mit identischem Seed und Setup bei transienten Workerfehlern. Abweichungen bei Provenienz, Eingabe oder Ergebnisaudit sperren die Serie. Alle fehlgeschlagenen Versuche mit Grund und verfügbaren Belegen protokollieren. Keine Ersatzseeds, Nullersetzung oder aus Ergebnisgründen entfernten Spiele. Für das geplante Screening müssen alle 100 Neunerblöcke vollständig sein. Bei dauerhafter Unvollständigkeit nur technischen Status veröffentlichen. Kein vorzeitiger Effekttest.

## Analyse und Folgeplanung

Zielgröße ist der xG-Saldo `xGD = xGF − xGA` pro Match aus Heimsicht. Primäre explorative Familie mit 12 Tests. Je Gruppe zwei gepaarte xGD-Kontraste gegen Baseline und ein direkter JumpingReach-minus-Acceleration-Kontrast aus demselben Block. Der höchste Mittelwert pro Attribut benennt deskriptiv einen Kandidaten. Eine vorläufige praktische Orientierung ist 0,10 xGD pro Match, wie in ATTR-004.

Die sekundäre Familie enthält 66 Tests. Für xGF, xGA, Tore, Gegentore und Punkte (3/1/0) werden dieselben 12 Kontraste ausgewertet. Hinzu kommen sechs xGD-Interaktionen als paarweise Differenzen der vier direkten Attributkontraste zwischen Gruppen. Alle Differenzen und Differenzen von Differenzen werden zuerst innerhalb desselben Seeds gebildet. Die gemeinsame Baseline und Korrelationen über Arme bleiben so erhalten.

Pro Kontrast werden Mittelwert, Stichprobenvarianz, SD, gepaarter t-Test und marginales 95-%-t-Intervall berechnet. Ein gemeinsames Resampling ganzer Seed-Blöcke mit 20.000 deterministisch gezogenen Bootstrap-Replikaten liefert marginale 95-%-Perzentilintervalle für die 12 primären Kontraste. Holm-Korrektur bei 0,05 getrennt über die 12 primären und 66 sekundären Tests. Die Intervalle sind marginal. Alle Ergebnisse einschließlich ausgewählter Kandidaten bleiben explorativ.

Für alle 12 primären Kontraste und sechs xGD-Interaktionen schätzen wir die benötigte Zahl vollständiger neuer Seed-Blöcke für gepaarte t-Tests per nichtzentraler t-Verteilung. Planungsszenarien sind wahre Unterschiede von 0,10, 0,15 und 0,20 xGD, Zielpower 80 % oder 90 % sowie zweiseitiges α = 0,05 oder konservativ 0,05/4 für bis zu vier Kontraste. Als Streuung verwenden wir die Screening-SD und als Sensitivität deren einseitige 95-%-Obergrenze unter Normalitätsannahme. Die Planung hängt vom festgelegten Kontrast und der übertragbaren Varianz ab. Die beobachteten Höchstwerte dienen nicht als angenommene wahre Effekte. Die unabhängige Bestätigung erhält einen eigenen eingefrorenen Analyseplan.

## Artefakte

[Analysecode](../analysis/analyse_attr005.py). Unter `data/attr-005/` erscheinen Manifest, technische Validierung, zulässige JSONL-Matchmessungen, Effekte und Planungsrechnungen. Native Dumps, Spielstände, ausführbare Dateien und Fixture-Dateien bleiben lokal.

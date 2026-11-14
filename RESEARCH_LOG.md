# Research Log

## 2026-11-14 – TACT-001-P1B vollständig abgeschlossen

- Nach gepushter Vorregistrierung `e0b63bd` und technischer Freigabe `9831b2a`
  alle2.048 Hauptmatches akzeptiert, 64 vollständige unabhängige Seedblöcke.
  Alle2.121 Versuchsplätze abgerechnet: 2.120 Vollmatches plus erwartete Exit108-
  Abweisung. Keine Ausfälle, Ausschlüsse, Retries, Ersatzseeds oder Holdouts.
- Hauptschätzungen A/B/C/D/E: +0,063/−0,007/+0,034/+0,018/+0,026 xGD.
  Kein Haupttest nach Holm-5, keine Paarinteraktion nach Holm-10 und kein
  Sekundärtest nach Holm-25 signifikant. B×C +0,177, Holm-p0,134 bleibt explorativ.
  Alle fünf Hauptintervalle erfüllen die volle Zielbreite≤0,30.
- Eingefrorene Auswahlregel ergibt D15 und D09 als explorative Vorschläge,
  xGD-Abstände zu D00 +0,229/+0,180 im Kontextmittel. Keine unabhängige
  Gewinnerbestätigung; konkrete Optionen und vier Setup-Hashes veröffentlicht.
- Child-Wall-Time 1.119,500/2.400 s, gesamtes natives Studienzeitfenster
  1.474,665/2.400 s innerhalb der unveränderten UTC-Deadline. Vier Worker,
  alle128+8 Warmworkerprozesse erfolgreich und sauber beendet; fünf zusätzliche
  native Vorbereitungs-/Capabilitiesprozesse innerhalb derselben Zeitreservation.
- 42 Plattform-/Studientests und fünf historische Analysetests bestanden.
  Unabhängiger Verifier reproduziert alle40 Effekt-/t-/Bootstrapintervalle,
  fünf simultane Intervalle, Holm-Familien,960 Seedkontraste und Kandidatenregel.
  Alle124 historischen Forschungsdateien unverändert; native Leistungsanalyse
  und Ausführungscode seit Vorregistrierung unverändert. Nach P1B gestoppt.
  [Ergebnisse](experiments/TACT-001-P1B-results.md).

## 2026-11-14 – TACT-001-P1B technisch freigegeben

- Vorregistrierung in `e0b63bd` vor dem ersten Prüfmatch veröffentlicht, CI
  erfolgreich. Alle72 Vollmatches,64 Eingabezellen und acht exakte Wiederholungen
  bestanden; negative Binärprobe erwartungsgemäß Exit108. Neue C/D/E-Bits nativ
  in beiden Phasen-/Seitenkontexten und Matrixzuordnung verifiziert.
- Alle73 technischen Versuchsplätze verbraucht,2.048 Hauptjobs noch unbegonnen,
  keine Holdouts. 47,616/2.400 s Child-Wall-Time kumuliert; feste UTC-Deadline
  14:09:26,985 am14.11.2026 bleibt unverändert.
  [Technische Freigabe](experiments/TACT-001-P1B-validation.md).

## 2026-11-14 – TACT-001-P1B vorbereitet und vorregistriert

- Große Variante beauftragt: 2.048 Hauptmatches, 64 unabhängige Seedblöcke.
  Gemeinsame Designfunktion um explizites `fraction=-1` ergänzt; historischer
  Standard +1 bleibt unverändert. D00 all-standard, Resolution V und physische
  Kontrastskalierung automatisiert geprüft. Explizite D00-Kontrollkennung im Schema.
- DLL27.0.1+2503222, Host, Fixture, Tooltag und Katalog stimmen mit Freigabekontext
  überein. Native Vorbereitung prüft Ressourcen-/Adapteridentität erneut.
  64 regelkonforme Eingabezellen erstellt; D00 jeweils binäridentisch zur P0-
  Baseline. Alle übrigen Binärdifferenzen betreffen nur fünf benannte Instructions.
- 67 neue Seeds gegen 2.150 historische/reservierte Werte geprüft und dauerhaft
  reserviert. Noch keine technischen oder wissenschaftlichen Matches gestartet.
  Vorbereitung 4,769 s, unverrückbare Gesamtdeadline und 2.400-s-Childbudget aktiv.
- 40 Plattform-/P1A-/P1B-Tests und fünf historische Analysetests bestanden,
  P0 unabhängig reproduziert. Die feste Testanzahl vorhandener Entwurfsspezifikationen
  wurde um den achten Vertrag ergänzt. 124 historische Forschungsdateien unverändert.
  [Vorregistrierung](experiments/TACT-001-P1B-preregistration.md) und Code werden
  vor dem ersten Prüfmatch gepusht; technische Ergebnisse in separater Freigabe.

## 2026-11-14 – TACT-001-P1A: Offline-Präzisionsanalyse und Suchdesign

- Sauberer Ausgangsstand `873799a4eb4f233d2b894a579e53e409f64140fb`, origin/main.
  P0-Haupt-/Technikmessungen, Eingaben, Budget und Abrechnung erneut gelesen.
  128 Hauptmatches/16 Blöcke, 23 Technikmatches, sieben exakte Wiederholungen,
  eine erwartete Negativabweisung und alle 152 Plätze nachvollzogen.
- P0-Primärergebnis unabhängig exakt reproduziert. Sechs Kontraste × fünf
  Endpunkte zusätzlich explorativ analysiert; Kontext-/Seiten-/Armpaarung,
  Seed-Einfluss und Endpunktunterschiede vollständig veröffentlicht.
  Kein Sieger oder nachträglicher Bestätigungsbefund.
- Varianzreduktionsalternativen einschließlich Kalibrierungskosten verglichen.
  Fünffaktor-Resolution-V-Screening E=−ABCD empfohlen; 1.024/2.048 Hauptmatches
  ergeben unter explizitem Varianztransfer 61,1/94,6 % konservative Power pro
  0,20-xGD-Haupteffekt. Unbekannte neue Faktorvarianzen begrenzen diese Prognose.
  Kader-/Stärke-/Gegner-/Karrieretransferplan und ausführlicher separater P1B-Auftrag.
- Neue native Matches **0**, neue reservierte Seeds **0**, Holdoutmatches **0**.
  Historische Archive und eingefrorener P0-Code unverändert; Quelltextprüfsummen
  auf LF normalisiert, um Git-CRLF-Checkouts vergleichbar zu halten.
  Alle elf P0-Kontraste/Intervalle, Holm, SD-Grenzen/Fallzahlen und das historische
  Archiv erfolgreich nachgerechnet. 30 Plattform-/Pilot-/P1A-Tests und fünf
  historische Analysetests bestanden; Analyse-/Bericht-/Grafikausgaben bei
  erneuter Erzeugung byteidentisch. Alle 113 historischen Dateien unter
  `analysis/`, `data/`, `experiments/`, `research/specs/` gegen den Ausgangscommit
  unverändert. Analyse, Tests, Design und Folgeauftrag in `ab14975` auf origin/main
  veröffentlicht; dieser Folgecommit ergänzt nur Einstieg und Plattformdokumentation.
- [Analyse](experiments/TACT-001-P1A-analysis.md) ·
  [Designvergleich](docs/TACT-001-P1A-design.md) ·
  [Datenausgaben](data/tact-001-p1a/README.md) ·
  [Folgeauftrag, nicht gestartet](experiments/TACT-001-P1B-order.md).

## 2026-11-14 – TACT-001-P0 vorbereitet und vorregistriert

- Ausgangscommit `d0e8aae`, sauberer Arbeitsbaum; DLL, Host, Fixture, Ressourcen
  und aktueller Upstreamtag stimmen mit VALID-002 überein.
- Eigene regelkonforme IP-4-2-3-1/OOP-4-4-1-1, zwei binäre Faktoren,
  zwei Gegnerstile mit identischen geschriebenen Spielerprofilen. 16 Eingabezellen
  und zwei ungespielte Holdoutprofile eingefroren. Keine Downloads als Kandidaten.
- 19 neue Seeds gegen 2.130 historische/reservierte Werte geprüft. Hauptplan:
  128 Matches, 16 unabhängige Seedblöcke; Technikplan 23 Matches plus Negativprobe.
- Dauerhafte Budgetkontrolle und externe Deadline implementiert und getestet;
  reiner Supervisorfehler vor Engineaufruf repariert, Zeitverbrauch erhalten.
  Vorbereitungszeit kumulativ 4,125 Sekunden, noch kein Match gestartet.
- 21 Plattform-/Pilot-/Budgettests und fünf bisherige Analysetests bestanden.
  [Eingefrorener Plan](experiments/TACT-001-P0-preregistration.md).

## 2026-11-14 – TACT-001-P0 technisch freigegeben

- Vorregistrierung, Code und Seeds wurden in `650a89a` vor dem ersten Match
  gepusht. Der tatsächliche Registry-Receipt ist auf diesen Commit gebunden.
- 23/23 technische Matches, alle 16 Eingabezellen, sieben exakte Wiederholungen
  und die negative Binärprobe mit Code 108 bestanden. Pro Match 1.058 native
  Profilfelder und sämtliche deklarierten Eingaben verifiziert.
- Alle 24 technischen Plätze verbraucht; 128 Hauptjobs noch unbegonnen.
  Kumulatives Budget 22,553/900 Sekunden, keine Retries oder Ersatzseeds.
  [Technische Freigabe](experiments/TACT-001-P0-validation.md).

## 2026-11-14 – TACT-001-P0 Hauptserie abgeschlossen

- Nach Push der technischen Freigabe `c9a4353` alle 128 vorregistrierten
  Hauptmatches akzeptiert. 16 vollständige Seedblöcke, keine Ausfälle,
  Ergebnisexklusionen, Ersatzseeds oder Retries. Keine Holdouts simuliert.
- Primärer xGD-DoD-Kontrast +0,019756, 95-%-t-KI [−0,769851; +0,809364],
  p=0,956542. Bootstrap-KI [−0,616687; +0,679748]. Richtung offen.
  Keiner der zehn Sekundärtests erreicht Holm bei 0,05.
- SD 1,8184 (high_press) und 0,8306 (deep_block); gepoolt 1,4136, gepoolte
  einseitige 95-%-Obergrenze 2,0634. Neue Fallzahlplanung für 0,10/0,15/0,20
  xGD-DoD bei 90 % Power publiziert; keine dieser Serien gestartet.
- Alle 152 Versuchsplätze abgerechnet: 151 vollständige akzeptierte Matches
  (128 Haupt-/23 Technikmatches) und eine erwartete negative Eingabe.
  Dauerhaft verrechnete Wall-Time 108,478/900 Sekunden, keine Budgetrücksetzung.
- Alle elf Kontraste, t-/Bootstrapintervalle, Holm-Familie, SD-Obergrenzen und
  sechs Fallzahlminima unabhängig aus öffentlichen Matchzeilen nachgerechnet.
  [Pilotbericht](experiments/TACT-001-P0-results.md). Stopp nach dem Pilot;
  kein Gewinner gewählt und keine Optimierung oder Karrierefortschreibung.

## 2026-11-14 – Bestandsaufnahme und VALID-002

- Leeres Arbeitsverzeichnis mit dem Forschungsrepository verbunden; sauberer Ausgang
  `0b6a609`. [Bestandsaufnahme](docs/INVENTORY-2026-11-14.md), veröffentlicht in `a898b77`.
- VALID-002-Prüfplan vor neuen Matchläufen in `894c51f` gepusht. Lokaler Build
  `27.0.1+2503222`, Tactics Lab v1114.6, offizielle Referenz-DLL und Hosthash geprüft.
- 42 technische Matches akzeptiert, acht Wiederholungsvergleiche exakt, Ergebnisse
  bei 1/2/4 Workern identisch. FMF-Roundtrip und vollständige Events bestanden.
  Karriere-PKM-Reader akzeptiert, Kaderübertragung scheitert mit Code 108;
  keine Karrierefreigabe. [Reale Ergebnisse und Einschränkungen](experiments/VALID-002-adapter.md).
- Ein Speicher-Preflightabbruch vor Simulation und die begrenzte lokale Speicherregel
  sind dokumentiert. Keine wissenschaftlichen Leistungsvergleiche ausgeführt.
- 173 Upstreamtests (172 bestanden, ein Skip), fünf bestehende Analysetests sowie
  Nachrechnung des ursprünglichen Archivs bestanden. Alte ATTR-Dateien unverändert.

## 2026-11-14 – modulare Grundlage und Forschungsplanung

- Gemeinsame Bibliothek für Schema/Registry, disjunkte Seedreservierungen,
  Scheduler, native Audits, Statistik, Karriere-Checkpointimport und Berichte.
  [Architektur und tatsächliche Grenzen](docs/PLATFORM.md).
- TACT/ATTR/TRAIN/SET/MECH besitzen Roadmaps und vorregistrierbare erste Designs;
  SCOUT ist als spätere Anwendung reserviert. [Roadmap](docs/ROADMAP.md).
- Eigene 4-2-3-1-Suche mit effizientem DoE, benannten Interaktionen, begrenzten
  Modellvorschlägen und strikter gehaltener Bestätigung entworfen. Keine Suchserie
  ausgeführt. [TACT-001](experiments/TACT-001-discovery.md).
- Externe Studien mit Quellenfamilie, Version, Autorenfallzahlen und ungeklärter
  Reproduktionslage erfasst. Die Mac-Implementierung wird nicht als Windowsadapter
  behandelt. [Quellenregister](docs/EXTERNAL_RESEARCH.md).
- Vier-Match-A/A-Smoke ist vorab beschrieben; Ausführung erst nach Veröffentlichung
  der vollständigen Grundlage. [Exakter Folgeauftrag](docs/NEXT_CODEX_TASK.md).

## 2026-11-14 – End-to-End-Abnahme

- Grundlage in `6b3e74e` veröffentlicht; generierte SVG-Leerzeichen anschließend
  in `73e5e83` normalisiert. Vollständiger Diff-Check gegenüber Ausgangsstand besteht.
- Vier-Match-A/A-Smoke auf dem veröffentlichten Code `73e5e83` ausgeführt:
  4/4 akzeptiert, zwei neue Seedblöcke, alle A/A-Resultate exakt gleich,
  4,659 Sekunden mit zwei Workern. [Automatischer Bericht](data/platform-smoke/report.md).
- Gesamtbudget: 48 geplante Jobs, 46 akzeptierte technische Matches, ein
  zurückgewiesener Karrierejob und ein unbegonnener Job. Keine große Suchserie.
- 14 Plattformtests, fünf bestehende Tests und alle ATTR-004–007-Effektarchive
  aus unveränderten Rohmessungen erfolgreich nachgerechnet. Ursprüngliche
  Match-/Trainingsarchive ebenfalls reproduziert. [Abnahmebericht](docs/UPGRADE_REPORT.md).

## 2026-11-07 – ATTR-007 abgeschlossen

- Alle 1.600 Hauptmatches wurden auf Build `27.0.0+2493426` im ersten Versuch akzeptiert. Die 200 neuen Seed-Blöcke enthalten alle acht Arme. [Manifest](data/attr-007/manifest.json)
- Shapley ST +0,103 xGD, Holm-p = 0,0065. Der direkte Kontrast ST minus Flügelmittel liegt bei +0,088 xGD, Holm-p = 0,104. Alle vier Interaktionen bleiben unsicher. Die Shapley-Summe stimmt in jedem Block exakt mit ALL minus Baseline überein. [Ergebnisse](experiments/ATTR-007-ergebnisse.md)
- Die eingefrorene Analyse und die unabhängige Nachrechnung stimmen für alle 84 Tests, Bootstrap-Intervalle und 224 Fallzahlminima überein. [Effektarchiv](data/attr-007/effects.json)

## 2026-11-07 – ATTR-007 vorregistriert und technisch freigegeben

- Die [Vorregistrierung](experiments/ATTR-007-vorregistrierung.md) und der Analysecode wurden vor dem ersten Match in `9ceaf95` gepusht.
- Build `27.0.0+2493426`, Adapter, Fixture und die binären Baseline- und ALL-Setups stimmen mit ATTR-006 überein. Die 32 Prüfmatches bestätigen Positionszuordnung, Attributänderungen und identische Phasenkonfigurationen beider Teams. Alle 16 Wiederholungspaare stimmten exakt überein, die Negativprobe endete mit Code 108. [Validierung](data/attr-007/validation-summary.json)

## 2026-11-07 – ATTR-006 abgeschlossen

- Alle 600 Hauptmatches auf Build `27.0.0+2493426` wurden akzeptiert. Die 300 neuen Paare sind vollständig und von den früheren Matcharchiven getrennt. Es gab keine Hauptfehlversuche oder Ausschlüsse. [Manifest](data/attr-006/manifest.json)
- Die Sprunghöhenanhebung bei AMR, AML und ST verbessert xGD um +0,171 pro Match (95-%-KI +0,052 bis +0,290, p = 0,00498). Der vorregistrierte positive Effekt ist bestätigt. Das Intervall lässt Effekte unter und über der praktischen Schwelle von +0,10 zu. [Ergebnisbericht](experiments/ATTR-006-ergebnisse.md)
- Alle sechs Tests und 300 Sensitivitätsläufe unabhängig nachgerechnet. Commit `a9a9113` korrigiert die JSON-Typkonvertierung. Der Vergleich mit dem vorregistrierten Code ergab identische Zahlen und Entscheidungen.

## 2026-11-07 – ATTR-006 vorregistriert und technisch freigegeben

- [Vorregistrierung](experiments/ATTR-006-vorregistrierung.md) und Analysecode in `b9cb3e6` vor dem ersten Match auf `main` gepusht.
- Build `27.0.0+2493426`, Engine, Host, Adapter, Fixture und Matchressourcen geprüft. Beide Setup-Hashes stimmen mit ATTR-005 überein. Acht Prüfmatches wurden akzeptiert. Jeder gepaarte native Vergleich zeigte genau drei JumpingReach-Änderungen. Vier Wiederholungspaare stimmten exakt überein. Die Negativprobe wurde mit Code 108 abgewiesen. [Validierung](data/attr-006/validation-summary.json)

## 2026-11-06 – ATTR-005-Positionsscreening abgeschlossen

- Alle 900 Hauptmatches auf Build `27.0.0+2493426` sind akzeptiert. 100 disjunkte Seeds lieferten je neun vollständige Arme. Es gab keine Hauptfehlversuche oder Ausschlüsse. [Laufmanifest](data/attr-005/manifest.json)
- Der Angriff hatte für beide Attribute die höchsten xGD-Schätzwerte gegenüber Baseline. Sprunghöhe erreichte +0,232 xGD (95-%-KI +0,073 bis +0,392, Holm-p = 0,058). Kein primärer oder sekundärer Test erreichte die Holm-Schwelle. [Ergebnisbericht](experiments/ATTR-005-ergebnisse.md)
- Alle 78 Tests und 432 Mindestfallzahlen nachgerechnet. Die Planung verwendet gepaarte Varianzen und mehrere Zielunterschiede. Die unabhängige Bestätigung erhält einen eigenen Analyseplan. [Effektarchiv](data/attr-005/effects.json)

## 2026-11-06 – ATTR-005 vorregistriert und technisch freigegeben

- [Vorregistrierung](experiments/ATTR-005-position-screening.md) und Analysecode in `41460cc` vor dem ersten Match auf `main` gepusht.
- Engine `27.0.0+2493426`, Adapter-Host, Standardfixture und Matchressourcen stimmten mit dem validierten Stand überein. Vier Baselines ergaben dieselbe native Startelf und Positionszuordnung. 36 Prüfmatches wurden akzeptiert, alle 18 Wiederholungspaare stimmten exakt überein und die getrennte Negativprobe endete mit Code 108. [Validierung](data/attr-005/validation-summary.json)

## 2026-11-06 – ATTR-004 abgeschlossen

- Alle 3.360 Hauptmatches der vorregistrierten acht Szenarien wurden angenommen. Das ergibt 1.120 vollständige Seed-Tripel auf Build `27.0.0+2493426` ohne fehlgeschlagene Hauptversuche oder Ausschlüsse. Die 96 technischen Läufe sind separat archiviert. [Manifest](data/attr-004/manifest.json)
- Der direkte Kontrast Sprunghöhe minus Antritt beträgt +0,021 xGD (95-%-KI −0,038 bis +0,080, p = 0,479). Das Intervall liegt innerhalb der praktischen Schwellen. Beide Attribute verbesserten xGD gegenüber Baseline im Szenariomittel. Keiner der 21 Kontexttests war nach Holm signifikant. [Ergebnisse](experiments/ATTR-004-ergebnisse.md)
- Primärtest, alle 33 Sekundärtests und die Holm-Entscheidungen aus den publizierbaren Matchzeilen unabhängig nachgerechnet. Die ATTR-004-Analysetests und die Rechenprüfung des bisherigen Archivs bestanden.

## 2026-11-06 – ATTR-004 vorregistriert und technisch freigegeben

- Die [Vorregistrierung](experiments/ATTR-004-cross-tactic.md) und der Analysecode wurden in `ccfd630` vor dem ersten Match auf `main` gepusht. Acht Szenarien mit je 140 disjunkten Seeds und drei Armen sind festgelegt.
- FM27 meldete beim Start `27.0.0+2493426`. Engine, Host, Matchressourcen und Fixture stimmten mit VALID-001 überein.
- 96 technische Prüfläufe wurden akzeptiert. Alle 48 Wiederholungspaare stimmten bei Endstand, Teamstatistik und Endtick exakt überein. Die Übertragung der aktiven Profile auf beide Spielseiten und die nativen Attribut- und Taktik-Readbacks sind geprüft. Die getrennte ungültige Konfiguration wurde mit Exitcode 108 abgewiesen. [Validierungsbericht](data/attr-004/validation-summary.json)

## 2026-11-06 – Lokale Messdaten archiviert und nachgerechnet

- Build `27.0.0+2493426`, Adapter `fm27_desktop_2493426_adapter_v1`, Tactics Lab v1106. Der Ausgangsstand auf `main` war `fa436a2171fb2c3ed97b34e25d0f759d57d222e6`. Der Git-Verlauf führt den Commit dieser Archivierung.
- Für 2.504 akzeptierte Matches wurden native Logs und Startup-Belege abgeglichen. Zwei absichtliche Negativproben stehen getrennt im Archiv. Weitere 228 historische Matches sind separat erfasst.
- Die Archivprüfung reproduziert 2.080 Baseline-Kontraste, zehn direkte Attributkontraste und zwei Venue-Kontraste einschließlich Bootstrap-Intervallen, BH und BY. [Prüfskript](analysis/verify_matches.py)
- Die vorläufige Rangfolge des Screenings änderte sich in der Replikation. Sprunghöhe, Antritt und Tempo blieben als Einzeleffekte im Hauptszenario bestehen. Der ursprüngliche Heim-/Auswärts-Seitentausch scheiterte vor dem Start an ungleichen Kaderkapazitäten. Die korrigierte Variante verwendet zwei gleich große aktive Kader und gepaarte Seeds. [Hauptreplikation](experiments/ATTR-002-hauptreplikation.md) · [Zusatzszenarien](experiments/ATTR-003-zusatzszenarien.md)
- Die Karrierebeobachtungen verwenden zufällig vergebene Teilnehmerkürzel und Attributdifferenzen. Datenqualität und fehlende Wiederholungen begrenzen die Interpretation. [Karrierebericht](experiments/TRAIN-001-karriere.md)
- Dieser Archivschritt bestand aus Prüfung, Analyse und Veröffentlichung bereits vorhandener Messungen. Es wurde keine neue Simulation gestartet.

## 2026-11-06 – Repository-Grundlage
- Projektstruktur mit Markdown-first-Regeln und maschinenlesbarem Rohdatenformat vorbereitet.
- Repository ist zum Zeitpunkt der Anlage öffentlich.
- Es wurden **keine neuen Simulationen** in diesem GitHub-Schritt ausgeführt.
- Frühere lokale Arbeiten wurden in der Konversation beschrieben (FM26/FM27-Trainingsarchive, Conditioning-vs-Heavy, Jugendvergleich, erste Attributsensitivitäten), jedoch **noch nicht als überprüfbare Rohdaten in dieses Repository übernommen**.
- Nächste Aufgabe: vorhandene Artefakte sichten, Versionen verifizieren, Reproduzierbarkeit prüfen, dann erste neue Testserie ausführen.

## Neue Einträge
Für jeden Lauf Datum, Bearbeiter/Tool, Branch+SHA, Build, Experiment-ID, Ergebnis, Einschränkungen und Folgeschritt ergänzen.

## 2026-11-14 – TACT-001-P1C vorregistriert

P1B vollständig unabhängig verifiziert; D15 einziger eingefrorener Kandidat, D09 archiviert.
Eigener Punkte-Präzisionspilot:512 Hauptmatches/128 neue Seedblöcke,16 technische
Vollmatches plus Negativprobe,131 neue reservierte Seeds. Acht native Setups
bytegleich zu P1B; Identität/Runtimesourcen geprüft. 48+5 Offline-Tests bestanden.
900s kumulierte Child-Zeit,1800s feste UTC-Frist; keine Retries/Seedersetzung.
Vorregistrierung/Code/Seeds werden vor Vollmatches publiziert. VALID-003 nur geplant.

## 2026-11-14 – P1C technische Gates bestanden

16/16 Vollmatches,8 exakte A/A-Paare und Exit108-Negativkontrolle bestanden.
Keine Hauptmatches gestartet. Child-Zeit 24.623/900s; Frist unverändert.
Erste CI scheiterte an privater Seedpfadabhängigkeit im neuen Test; behoben
durch Prüfung des öffentlichen Seedplans, keine Änderung eingefrorenen Codes.
Lokal erneut48 Tests bestanden; Hauptlauf erst nach erfolgreicher Freigabe-CI.

## 2026-11-14 – P1C vollständig abgeschlossen

512/512 Hauptmatches,128 neue unabhängige Seedblöcke,16 technische Vollmatches
und eine Exit108-Abweisung. Keine Ausfälle, Ausschlüsse, Retries, Ersatzseeds
oder Holdouts. Punkte+0,09765625,95-%-KI[−0,137;+0,333],p0,41246.
Hinweisregel nicht erfüllt; expliziter Wechsel zu Rollen/OOP empfohlen.
900s Child-Budget mit320,441s genutzt;1800s Fenster mit661,419s genutzt.
Öffentlicher unabhängiger Verifier reproduziert sechs Kontraste, Holm5,
SD-/Powerplanung,128 Blöcke,529 Versuchsplätze und151 historische Dateihashes.
Nachfolgender Multi-Agent-Auftrag startet ausschließlich Recherche/Planung
und klar getrennte Offlinevorarbeiten, keine weitere native Hauptserie.

## 2026-11-14 – tatsächliches Multi-Agent Scientific Program abgeschlossen

Sieben eigenständige Codex-Subagents TACT/ATTR/TRAIN/SET/MECH/VALID/Independent
Review in parallelen Wellen; maximal drei gleichzeitig neben dem Director,
weitere Aufgaben in Warteschlange. Getrennte Verantwortungsdateien, zentrale
Registry-/Nativekoordination, keine konkurrierenden Runner-/Seedwrites.
[Gesamtauswertung](docs/program-2026-11-14/README.md),
[Agenten-/Hashabschluss](docs/program-2026-11-14/QUEUE.json),
[unabhängige Schlussprüfung](docs/program-2026-11-14/REVIEW.md).

Neu: kleine optionale Exklusivlease mit vier echten Konkurrenz-/Crash-/Eigentums-
/Workercap-Tests; bestehende Runner nicht integriert.52 Repositorytests und5
historische Analysetests bestanden. P0/P1B/P1C-Verifier und Archivschutz bestehen;
151 historische Forschungsdateien bleiben unverändert. Alle zehn früheren
Quellenregistereinträge erhalten, vier neue quellenkritisch ergänzt.

Review präzisierte sieben TACT-Sekundärpaare, neutrale xPts-Verwertungsgrenze,
SET-Bootstrap-Nullnennerregel und getrennte Mac-Study3-Teilzahlen. Kontraste,
Power-/Kosten-/Replikatarithmetik und ausgewählte Primärquellen unabhängig
geprüft. Sechs Berichtshashes binden den freigegebenen Stand. Bestehende
SET-/MECH-Draftwidersprüche dokumentiert; kein historischer Vertrag umgeschrieben.

Keine neue native Simulation, Seedreservierung, Holdoutnutzung oder
Karrierefortschreibung innerhalb dieses Programms. Der zuvor separat autorisierte
P1C-Abschluss ist in a1c85979ecf57ec160954eafb31e1d910728e744 veröffentlicht,
CI43606391029 erfolgreich. Neue Rollen-, Profil-, Startpolicy-, PKM-, Standard-
und Karrieregates bleiben offen. Nach finalem Diff-/CI-/Pushabschluss stoppen;
keine automatische Hauptserie oder weitere Optimierung.

## 2026-11-14 – Runde2: drei parallele Implementierungsagenten und Preflight

TACT/VALID/SET in eigenen Branches/Worktrees implementiert, Director integrierte
lokale Commits und beide unabhängig gefundenen Korrekturen. Separater Reviewer
prüfte alle Module,86Tests und vier echte frühere D00-Dumps(44/44/748) ohne
Serverimport. Native Vorbereitung/Seedreservation noch nicht begonnen.

Neue Module: VALID003-Profil-/Kapazitätsabsichten mit explizitem Missing und
hart blockierter PKM-/Replayfreigabe, separater NativeLease+DeadlineBudget-
Python-Testpfad; SET-V0 synthetic-only Parser/elfGoldfälle ohne Native-Mapping;
TACT002R0 eigener kleiner512-Match-Runner/Vertrag/Analyse/Auditor/Exporter.
SET-Repeatnachweis und TACT-Retry-Leaseprovenienz vor Registrierung korrigiert.
VALID-Attribute trennen15Positionsratings0..20 und54Abilityrohwerte1..100.

86Repositorytests+5historischeTests und alteVerifier bestanden. Zentraler
VALID-Offline-Smoke erzeugte21eigene Vektoren/zweiPythonchildren,0native/0Seeds.
193altewissenschaftlicheDateien gegen790727f geschützt. Codeveröffentlichung/CI
vor budgetierter nativer Vorbereitung; keine Holdouts,Karriere oder D15-Optimierung.

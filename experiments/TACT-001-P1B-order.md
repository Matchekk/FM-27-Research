# Nächster Codex-Auftrag: TACT-001-P1B – eingefrorenes Fünffaktor-Screening

**Vorschlag vom 14.11.2026, nicht gestartet oder vorregistriert.**
Dieser Text ist ein separat vom Nutzer zu erteilender Folgeauftrag. P1A führt
ihn nicht aus. Der [Planungsvertrag](../data/tact-001-p1a/next-study-plan.json)
ist ausdrücklich kein registrierbarer nativer Laufvertrag; tatsächliche
Hashwerte, Seedwerte und Vorregistrierungscommit fehlen noch.

---

Du bist Lead Research Engineer und Statistiker im Repository
`https://github.com/Matchekk/FM-27-Research`.

Führe ausschließlich **TACT-001-P1B** aus: kontrolliertes Discovery-Screening
einer eigenen IP-4-2-3-1 mit fünf binären Team-Instruction-Faktoren. Keine
Downloadkonkurrenz, Modelloptimierung, neue OOP-/Rollen-/PI-/Standardvariation,
Holdoutbestätigung oder Karrierefortschreibung. Keine Behauptung einer optimalen
Taktik. Bestehende ATTR-001–007, P0, ursprüngliche Vorregistrierungen und fremde
Änderungen vollständig erhalten.

## 1. Einstieg und wissenschaftliche Frage

Lies AGENTS.md, README, METHODOLOGY.md, docs/PLATFORM.md, VALID-002,
TACT-001-discovery.md, P0-Preregistrierung/Validierung/Ergebnis und vollständig
TACT-001-P1A-analysis.md sowie docs/TACT-001-P1A-design.md.
Prüfe Arbeitsbaum, Remotes, origin/main und existierende reservierte Seeds.

Frage: Welche der fünf kontrollierten Änderungen verbessern den über die
anderen Designstufen gemittelten xGD-Wert unserer eigenen 4-2-3-1 gegen die
zwei eingefrorenen Entdeckungsgegner im freigegebenen synthetischen Kontext?
Gibt es ausreichend große kontextspezifische oder Zweifachsignale, um eine
gezielte neue Interaktionsprüfung zu rechtfertigen?

Primäre Zielgröße xGD pro Match. Fünf vorab eingefrorene Hauptkontraste
`mean(xGD|F+)−mean(xGD|F−)`, nicht fünf isolierte Eingriffe am Standardanker.
Kleinste praktisch relevante Änderung +0,20 xGD. Primärfamilie Holm-5 bei
α=0,05; Planung konservativ zweiseitig α=0,01 je Kontrast. Ziel 90 % Power
je solchem Effekt, marginale volle 95-%-Intervallbreite ≤0,30 xGD.
Keine Garantie gleichzeitiger Entdeckung aller fünf Effekte.

## 2. Budget vor jedem nativen Prozess festlegen

**Standard dieses Folgeauftrags: große Variante**, 32 neue unabhängige Seeds je
Gegner, 64 Blöcke insgesamt, 16 Bedingungen×2 Seiten je Block = **2.048 Hauptmatches**.
Vor jedem nativen Aufruf persistenten Versuchszähler und unverrückbare Deadline
einbauen und testen. Maximal vier Worker, 90 s ohne Fortschritt je Worker,
2.400 s kumulierte Child-Wall-Time, 40 Minuten gesamte native Ausführungszeit
ab erstem nativen Aufruf. Vorbereitung/Audits/Negativprozesse zählen mit.
Keine Retry-/Neustart-/Workerwechsel-Schleife darf Grenzen zurücksetzen.

Technikplan maximal 73 Startversuche: 64 Readbackmatches, acht exakte A/A-
Wiederholungen, eine erwartete negative Abweisung. Bei Erfolg 72 technische
Vollmatches, insgesamt 2.120 Vollmatches bzw. 2.121 Matchstartversuche.
Weitere native Vorbereitungsprozesse benötigen ebenfalls eine Zeitreservierung;
ihre Zahl zusätzlich ausweisen, nicht als weitere Matches verstecken.

Die günstigere Variante darf **nur bei ausdrücklicher Auswahl vor Registrierung**
verwendet werden: 16 Seeds je Gegner, 32 Blöcke, 1.024 Hauptmatches,
unverändert 73 technische Versuche, 1.200 s Child-Wall-Time und 20 Minuten
Gesamtdeadline. Bedingte Power dafür nur 61 %, keine 90-%-Behauptung.
Kein automatischer Wechsel nach Ergebnissen oder automatische Erweiterung.

## 3. Identität, Design und eigene Taktik

Prüfe tatsächliche FM27-DLL/Dateiversion, Host, Fixture, Ressourcen, Tooltag,
Adapter und letzten Freigabekontext gegen VALID-002/P0. Bei Drift zuerst
separat technisch revalidieren; falls dies im festgelegten Budget nicht sicher
möglich ist, nur technischen Status liefern. Kein stilles Upgrade oder Übertragen
alter Leistungsbefunde auf neue Builds. Karriere-PKM bleiben gesperrt.

Nutze ausschließlich das validierte gebündelte Fixture und die unveränderten
geschriebenen P0-Kaderprofile, beide Gegner high_press/deep_block gleich stark,
gleiche Rollen-/PI-/Managementpolitik und IP-4-2-3-1/OOP-4-4-1-1.
Jede konkrete eigene und gegnerische Phase, Formation, Rolle, Duty, PI,
Team Instruction, Profilfeld, Seitenzuordnung und Matchmanagementregel muss
im neuen Vertrag und Setup-Hash stehen. Alles außer den fünf Faktoren bleibt
innerhalb des jeweiligen Kontext-/Seitenplatzes unverändert.

Design: 16 Zeilen in lexikographischer Reihenfolge A/B/C/D, jeweils −1 vor +1,
IDs `D00` bis `D15`, **E=−A×B×C×D**, `I=−ABCDE`, Resolution V.
Verwende die getestete P1A-Matrix; all-standard `-----` ist D00.
Keine falsche Annahme, dass all-plus in dieser Halbfraction enthalten sei.

Vorläufige konkrete Stufen aus dem **nur statisch gelesenen** v1114.6-Katalog
SHA256 `c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c`:

| Faktor | Gruppe / Phase | −1 | +1 |
|---|---|---|---|
| A Pressing | TriggerPress / OOP | Standard, bit0, option1313689463 | More Often, bit66, option2000905329 |
| B Linie | DefensiveLine / OOP | Standard, bit0, option894978671 | Higher, bit57, option1329018200 |
| C Tempo | Tempo / IP | Standard, bit0, option1496610426 | Higher, bit47, option1345339954 |
| D Direktheit | PassingDirectness / IP | Standard, bit0, option1483944022 | Shorter, bit3, option1146434657 |
| E Breite | AttackingWidth / IP | Standard, bit0, option1951095402 | Wider, bit51, option1244744824 |

`+1` bezeichnet die gewählte Intervention, bei D also **kürzere**, nicht längere
Pässe. Native Bits sind keine ordinalen Skalen. Standard bit0 bedeutet die
vollständige Neutralisierung sämtlicher Alternativen der betreffenden Gruppe,
kein gemeinsames globales Standardbit. Prüfe Phase-/Konfliktregeln in `rules=game`
und alle 64 Gegner-/Seiten-/Designzellen. Falls der aktuelle Katalog abweicht,
keine automatische Ersetzung: Diagnose und aktualisierte Vorregistrierung vor
Leistungsdaten; bislang nicht validierte C/D/E sind ein technisches Gate.

## 4. Vollständig offline vorbereiten und vor dem ersten Match pushen

Erstelle neuen experimentbezogenen Runner und deterministische Analyse ohne
Mutation von P0-Code. Wiederverwende Registry, NativeLab und Budgetbausteine,
wo die Verträge passen; keine unnötigen Änderungen an fremdem Upstream.

Erstelle und publiziere `experiments/TACT-001-P1B-preregistration.md`, konkreten
`research/specs/TACT-001-P1B.json`, Analyse-/Runnercode, exakte 16-Zell-Matrix,
64 Setup-Hashes sowie dauerhafte Seedreservierung. Hauptseeds je Gegner disjunkt,
gemeinsam über alle 16 Bedingungen und beide Seiten innerhalb des Blocks.
Zusätzlich drei disjunkte neue technische Seeds (je einer pro Gegner, einer
für Negativprobe); nie als Hauptseeds verwenden. Historische, technische,
reservierte und sämtliche Holdoutseeds vollständig ausschließen. Auch abgebrochene
Reservierungen bleiben verbraucht. Matchreihenfolge deterministisch randomisiert
mit separat benanntem Scheduler-RNG; dieser darf die FM-Seeds nicht verändern.

Die unveränderten Holdoutprofile `holdout_midblock` und `holdout_direct_counter`
werden nicht simuliert, ausgewertet oder zur Suche genutzt. Keine Reservierung
neuer Holdoutmatches in diesem Auftrag. Neue Discoverybedingungen erhalten
zukünftig separate IDs; jetzt keine neue Stärke-/Kaderdimension einführen.

Offline Tests vor Ausführung: Resolution-V-Orthogonalität/Aliassignaturen,
physische Kontrastskalierung, synthetische bekannte Haupt-/Interaktionseffekte,
gepaarte Block-/Seitenaggregation, Holm-Familien, Seeddisjunktheit, Budget-/Crash-
Wiederaufnahme, Kill-Deadline, Eingabeverletzung stoppt Serie, Export-Whitelist
und Archivschutz. Prüfe tatsächlich erfolgreichen Push des Vorregistrierungs-
commits auf origin/main; binde dessen SHA und Datei-Hashes im Registry-Receipt.

## 5. Technischer Gate vor Hauptmatches

Jede der 64 Zellen einmal mit dem zugehörigen technischen Kontextseed starten.
Lies beide Phasen, native Positions-/Rollen-/Duty-/PI-/Instructionfelder,
Spielerattribute/Profile, Identitäten, tatsächlichen Seed und natural finish
zurück. Vergleiche mit eingefrorenen Sollwerten, nicht nur Eingabe-JSONs.

Wiederhole exakt die acht Kombinationen
`(high_press/deep_block) × (Seite 0/1) × (D00/D01)` mit denselben technischen
Seeds und bytegleichen Eingaben, unter eigenem A/A-Label. Endstand, Endtick
und native Teamstatistiken müssen exakt übereinstimmen. Die eigenständige
negative Probe verletzt denselben bekannten nativen Binärvertrag wie P0 und
muss vor Leistungsannahme mit dem vorher festgelegten Exitcode108 scheitern.
Keine absichtliche Korruption geschützter Spieldateien.

Eingabe-/Seed-/Identitäts-/Readback-/Repeatfehler stoppen. Keine Ersatzseeds,
Ergebnisexklusion oder Nullersetzung. Alle begonnenen, fehlgeschlagenen und
unbegonnenen Jobs samt Verbrauch erhalten. Nur nach bestandenem Gate Bericht,
Tests und technischen Freigabecommit pushen; erst danach Hauptmatches starten.

## 6. Hauptanalyse und vollständige Berichterstattung

Pro Seed/Seite für jeden Faktor acht Pluszellen minus acht Minuszellen mitteln;
dann beide Seiten mitteln, dann Gegner je ½. Varianz und df kontextspezifisch.
Gepaarte marginale t-95-%-Intervalle, simultane Bonferroni-99-%-Intervalle
für fünf Hauptkontraste, Holm-5-p, stratifizierter Bootstrap kompletter Blöcke
(20.000 Ziehungen, separater eingefrorener Analyse-RNG). Kein n=2.048-Pseudoreplikat.

Zehn physische Zweifach-DoDs (jede Viererzellgruppe über die anderen Faktoren
gemittelt), jeweils eigene Seedkontraste, separate explorative Holm-10-Familie.
Insbesondere A×B und C×D. Vierfach-/Dreifachaliasierung ausdrücklich nennen;
keine behauptete Aliasauflösung durch Modellregularisierung.

Sekundär je Hauptkontrast die fünf Endpunkte tatsächliche Punkte, GF, GA,
xGF, xGA: komplette Holm-25-Familie. Native Plausibilitätsendpunkte fest:
shots_for/against, shots_on_target_for/against, possession_for. Diese dienen
deskriptiver Diagnose und technischen Gültigkeitsregeln; keine zusätzlichen
Leistungs-p-Werte außerhalb der eingefrorenen Familien. Feldnamen/Skalen vorher
an den exportierten nativen Messungen binden. Alle Endstände/Gegentore erhalten.

Zusätzlich: Kontextmittel/SD, Seitenkovarianz, vollständige Armkovarianz,
Leave-one-seed-out ohne Entfernen im Hauptergebnis, Varianztransfer gegenüber P1A,
Ressourcen-/Jobabrechnung, alle Ausfälle und alle vollständigen Blockzahlen.
Bei irgendeinem unvollständigen Block ausschließlich technischen Status
publizieren, keine partiellen Leistungsergebnisse oder Kandidatenrangfolge.

## 7. Auswahl- und Stopregel

Kein Effekt-/p-Wert-Stopping; nur feste Fallzahl oder technische/Budgetstopps.
Keine Fallzahlerweiterung aus beobachteter Richtung. Primäre Interpretation
umfasst alle fünf Faktoren. Ein vorläufiger Einstellungshinweis benötigt
Holm-p≤0,05 und Schätzwert≥+0,20; keine Garantie der Paketwirkung.

Höchstens zwei **explorative Vorschläge** aus den 16 tatsächlich geprüften
Zellen: nur positiver xGD-Abstand zum Standardanker in beiden Kontexten;
ordne nach dem kleineren der beiden Kontextabstände, dann dem gleichgewichteten
Abstand, dann lexikographischer Design-ID. Falls keine Zelle qualifiziert,
keinen Kandidaten ernennen. Diese Selektion hat Winner's Curse, deshalb keine
konfirmatorischen Gewinner-CIs aus denselben Daten. Größere gegenläufige
Kontext- oder Zweifachsignale nur als Anlass einer neuen gezielten Studie melden.

Unabhängige Bestätigung nur als **nächsten separaten Auftrag planen**:
gefrorener Kandidat gegen Anker, neue Seeds, unbenutzte Gegner/Stärken,
tatsächliche Punkte primär, eigene Power-/Multiple-Test-Planung.
Keine Holdoutmatches, kein Foldover, keine adaptive Optimierungsrunde starten.

## 8. Abnahme und Abschluss

Nur erlaubte JSONL-Messungen, eigene Profile/Verträge, Provenienz, Tests,
Analysen, Figuren und Grenzen publizieren. Keine DLL/PKM/FMF/Saves/private
Pfad- oder Spieleridentitäten. Historische SHA256 gegen P1A-Quellmanifest
und Git-Baseline prüfen. Tests und Archivverifier, Git-Diff/Dateigrößen/Secrets
prüfen, gemäß AGENTS committen und pushen. Tatsächliche Commit-SHAs,
gültige/fehlgeschlagene/unbegonnene Matches, unabhängige Blockzahlen,
verbrauchte Zeit und Freigabegrenzen im Abschluss nennen.

**Stoppe nach P1B. Keine automatische weitere Forschungsserie.**

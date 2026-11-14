# Externe Reproduzierbarkeit: JR/Speed und Spielschärfe

Offline-/Webaudit vom 14.11.2026, Zugriff 20:58:59–21:06:48 UTC.
Basis `95d94a4`; neun neue Originalbelege beziehungsweise Codeprüfungen.
[Register und Rechenwerte](../../data/night-001-external-replication/sources.json),
[Lesepfad](../../data/night-001-external-replication/README.md).
Die [frühere Quellenübersicht](EVIDENCE.md) bleibt unverändert.

**Zugänglicher Originalcode und bedingte Baseline-/Varianzinformation sind
vorhanden. Eine unabhängige externe Rohdatenreplikation unseres
Positionsmaskenkontrasts oder unseres Schärfe-Startpakets ist nicht verifiziert.**
Dieses Audit startete keine FM-Host-/Engineprozesse, Matches, Karrierefortschreibungen
oder Seedreservierungen. Es ändert keine eingefrorene Studie.

## Neue Belege statt weiterer Ranglisten

| Originalbeleg | Was neu geprüft wurde | Grenze zur lokalen Frage |
|---|---|---|
| [HarvestGreen, Originalbericht](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test) · REP-HG-ORIGINAL | Alter18/PA150, Attribute12; Dosen1/6/18, fünf Gegnerformationen, je100 Saisonmatches, Siegquote. FMRTE sperrt benannte Zustände. | Zwölf Monate statt isolierter Replays; vollständiger Build, Seeds, Masken und Rohvarianz fehlen. Verlinktes Workbook nicht heruntergeladen, Lizenz/Granularität ungeprüft. |
| [Mac01](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/01-attribute-values.md) · REP-MAC-01 | Baseline1,79 Punkte, xGF2,11/xGA1,45; zehn echte Fixtures, gesamter Kader einschließlich Bank, geklemmte ±25-Rohdosis. | Ein Club, reale Startzustände, In-Match-Management. Wiederholung auf zwei Builds mit denselben Fixtures/Seeds ist interne Reanalyse. |
| [Mac02](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/02-real-vs-levelled.md) · REP-MAC-02 | Reale Fixtures, nivellierte reale Fixtures und synthetisches Sample liefern unterschiedliche Effekte. A übernimmt frühere Messungen. | Der Samplewechsel ändert gleichzeitig Taktik, Masken, Körper, Zustand und Fixture; kein isolierter Maskeneffekt. |
| [Mac12](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/12-thresholds.md) · REP-MAC-12 | Mehrere Dosen, gemeinsame Baseline und GLS; JR-/Speed-Kurven unterscheiden sich im berichteten Kontext. | Gesuchte Knickpunkte sind explorativ. Keine universelle Schwelle oder unabhängige Bestätigung; xPts erfasst Verwertung unvollständig. |
| [Mac13b](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/13b-value-by-position-random.md) · REP-MAC-13B | Neue Positionsregression, Gegenpress424, synthetische Kader und Familiarity80; anderer Autor als Purity. | Vergleich und Split-Hälften-Filter sind keine extern geprüfte Replikation. Rohmessungen und vollständige Runprovenienz fehlen. |
| [Mac14](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/14-team-strength.md) · REP-MAC-14 | Fünf EPL-Stärkepaarungen,160 Paare pro Bedingung. | Enge Stärkespanne; nicht erkannte Heterogenität ist kein Äquivalenznachweis. |
| [Mac05](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/05-everything-else.md) · REP-MAC-05 | Natürlicher Ausgangszustand; ausgewählte100%-Bedingung auf neuen Seeds untersucht. | Ganze aktive Mannschaft einschließlich GK/Bank statt zehn Startfeldspieler. Niederwertige50/75%-Arme stammen aus dem Screening. |
| [Mac-Runner](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/overnight.py) · REP-MAC-PROTOCOL | Fehlerpfad überspringt fehlgeschlagenen Job und läuft weiter; Analyse nimmt verfügbare Paar-Schnittmengen. | Originaljobs, Logs und Ausfallzählung sind nötig. Das ist kein Beweis tatsächlich aufgetretener oder selektiver Ausfälle. |
| [Unabhängige Editor-Notizen](https://github.com/barak14/fm-editor/blob/c597c89fc4f41b9bf9fd5e12fc6a71045f97c6b6/docs/fm27/memory-layout.md) · REP-EDITOR-SHARP | Live-Spielerfelder für Condition/Sharpness/Fatigue ausdrücklich ungeprüft beziehungsweise defekt. | Andere Datenstruktur; weder unsere Match-Caches noch eine UI-Prozentkalibrierung oder Leistungswirkung belegt. |

Die Versionszahlen sind Autorangaben. Wo kein kompletter Runbuild beziehungsweise
Engine-/Hosthash vorliegt, steht im Register ausdrücklich `null`. Ein
Repositorycommit identifiziert Code und Text, nicht die damals ausgeführte DLL.

HarvestGreens Seitenbeschreibung belegt nicht, ob alle Attributwerte über die
zwölf Monate konstant blieben. Saisonentwicklung wird deshalb weder als sicher
ausgeschlossen noch als tatsächlich eingetretener Störfaktor behauptet.

## Was aus Zusammenfassungen nachrechenbar ist

Für Mac02 gilt laut [Originalanalysecode](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study2_levelled.py)
der Kontrast `(plus−minus)/2`. Mit300 Paaren lassen gerundete Mittel und
t-Werte die Näherung `SD=abs(Mittel/t)×sqrt(300)` zu:

| Arm | Pace | Acceleration | JR |
|---|---:|---:|---:|
| A: reale Fixtures/Kader |0,796|0,754|0,718|
| B: reale Fixtures/nivelliert |0,781|0,726|0,703|
| C: synthetisches Sample |0,351|0,341|0,385|

Einheiten: xGD des beschriebenen Halbdifferenzkontrasts. Das Register enthält
Rechenweg und reine Rundungsbereiche, keine neuen Konfidenzintervalle.
**Das sind keine Rohdaten-SDs unserer Studie.** Ohne Kreuzkovarianzen ist
weder die JR-minus-Speed- noch die Maskeninteraktionsvarianz rekonstruierbar.
Diese Zahlen liefern keine lokale Powergarantie.

## Seed- und Analyseebene präzise trennen

Der [Originalgenerator von Mac13b](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/random_study.py)
verteilt50.000 Konfigurationen über16 Settings; der Seedzähler wächst nach
je16 Jobs. Daraus folgen3.125 numerische Seedwerte, während das Paar
Setting/Seed eindeutig bleibt. Gleiche Zahlen über verschiedene Konfigurationen
beweisen weder gleiche Ereignisse noch Korrelation. Unabhängigkeit muss anhand
Randomisierung und Generierungs-/Samplingebene begründet werden.
Die dortige Kovarianz ist homoskedastische OLS; eine alternative Cluster- oder
robuste Auswertung bleibt ohne Rohzeilen offen. Hier wird weder die effektive
Fallzahl noch die Gültigkeit publizierter Intervalle nachträglich festgelegt.

## Schärfe: Zielintervention bleibt das verifizierte Rohpaket

[Mac05s Encoder](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_everything.py)
setzt beide Profilfelder gemeinsam für den ganzen aktiven Kader.
[Der Bestätigungscode](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_confirm.py)
enthält nur den100%-Arm dieser Schärfeauswahl, mit Seeds31–120.
Eine gemeinsame Feldänderung identifiziert keine einzelnen Consumer oder
Mediation. Natural-Baseline, Kaderumfang, Dosis und Plattform verhindern eine
Wirkungsgleichsetzung mit unserem vorregistrierten7000→10000-Startpaket.
Die externe Evidenz ändert weder dessen eingefrorenen Vertrag noch technische
Gates oder Interpretation. Eine UI-Kalibrierung wird nicht behauptet.

## Reproduktionsstufe und rechtliche Reichweite

Der vollständige Gitbaum von Maccommit
`e92cf1416ca5c8c4b13009f8cf7d695f290b0368` hat176 Einträge,
`truncated=false`, keine getrackten JSONL-Messreihen oder erkannten
Jobresultattabellen/Design-NPZ.
[`.gitignore`](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/.gitignore)
ignoriert JSONL und private Daten. Das ist eine begrenzte Bestandsaufnahme
dieses Baums, keine Behauptung über sämtliche Releases oder externen Speicher.

[MIT-Lizenz](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/LICENSE)
und [Drittanbieterhinweise](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/THIRD_PARTY_NOTICES.md)
erlauben keine pauschale Weitergabe spielbezogener Eingaben/Daten.
Dieses Audit übernimmt nur eigene knappe Beschreibungen, Metadaten und
nachgerechnete Zusammenfassungswerte. Keine Spieleridentitäten, Assets,
Workbooks oder Originalartikel werden gespiegelt. Quellcode wurde gelesen,
nicht ausgeführt oder importiert.

Damit sind drei Stufen auseinanderzuhalten: zugänglicher Code,
nachvollziehbare Summary-Arithmetik und vollständige Rohdatenreproduktion.
Hier wurden nur die ersten beiden erreicht. Mehrere Seiten desselben
Mac-Forschungsprogramms oder HarvestGreen-Ableitungen sind keine entsprechend
vielen unabhängigen Replikationen. Die Round-3-Nachrechnung unserer Daten ist
ebenfalls ein unabhängiges Review derselben Ausführung, keine externe Replikation.

## Konsequenz für die nächste Priorisierung

[ATTR-009](../../experiments/ATTR-009-results.md) untersuchte einen anderen,
engen Maskenmoderator: Raw60→80 bei zehn Startfeldspielern; aktive IP/OOP-Familien
fest. Der lokale Kontrast−0,162xGD mit95%-KI[−0,488;+0,164] bleibt unklar.
Die neuen Quellen erklären diese Unsicherheit nicht kausal und widerlegen
weder die lokale Studie noch fremde Ranglisten.

1. **Zuerst Reproduktionsvertrag statt weiterer globaler Rangliste.**
   Offline prüfen, ob öffentlich erlaubte Originaljobs, Runbuild-/Hosthashes,
   Inputmanifeste, vollständige Ausfälle und RNG-/Kontextzuordnung auffindbar
   werden. Aufwand: höchstens ein weiterer begrenzter Quellen-/Schemaabschnitt,
   null native Matches. Keine Kontaktaufnahme oder Datenerhebung hier.
2. **ATTR-Folgefrage: ein festgelegter CB-Slot versus ein ST-Slot.**
   Je genau ein Startspieler erhält JR, Acceleration oder Pace Raw60→80;
   die übrigen Eingaben bleiben D00. Primär der Unterschied der beiden
   JR-minus-Speed-Kontraste. Sechs Arme, beide Seiten,32 neue Seedblöcke
   über zwei feste Gegner ergeben384 Hauptmatches. Das isoliert Slotkontext,
   nicht reine Rollenmechanik; beide Slots müssen nach IP/OOP nativ feststehen.
   Vorher komplette Readbacks, unveränderte Startzustände, getrennte technische
   Seeds, ein primärer Kontrast und ein vorab begrenztes Gesamtbudget.
   Die Varianz dieser Einzelspielerfrage ist unbekannt: Pilot, keine
   Powergarantie. Baseline-/Dosisvariation wäre eine **separate** Folgestudie,
   kein automatischer Ausbau; zwei statt eines Baselinekontexts würden bei
   gleicher Replikatzahl mindestens768 statt384 Matches benötigen.
3. **Schärfe: zuerst den bereits eingefrorenen engen Pilot abschließen.**
   Nur dessen vollständig bestandene Gates und vollständige Hauptblöcke
   erlauben Effektbericht. Danach allenfalls separat den Kaderumfang des
   Pakets untersuchen, ohne UI- oder Consumerbehauptung. Ein hypothetisches
   2×2 aus Startfeldspieler-/GK-Bank-Paket benötigt bei64 vollständigen
   achtmatchigen Blöcken512 Hauptmatches, eigene Readback-Abnahme und neue
   Vorregistrierung. Dieser Vorschlag ist keine Ausführungsfreigabe.

Keine Holdout-, Karriere- oder Optimierungsfreigabe entsteht aus diesem Audit.
Der Informationsgewinn liegt in klareren Vergleichszielen und überprüfbaren
Replikationslücken, nicht in neuen simulierten Ergebnissen.

## Prüfnachweis

Dateien: nur dieser Bericht und das neue Quellenregister mit README.
JSON-Struktur, IDs, SHA-Formate, Rechenwerte und Quellwortbudgets werden
vor Commit lokal geprüft. Test- und Archivstatus stehen im README; kein Push
durch den Fachagenten, Integration und Veröffentlichung durch den Director.

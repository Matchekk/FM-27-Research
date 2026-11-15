# TRAIN-003 – neue Originaltabellenauswertung, Karrierepilot ungestartet

15.11.2026. **Neu nachgerechnet:** 51 Trainingsplanzeilen mit 1.887 numerischen
Endpunkten aus Harvestgreen22s Originalworkbook; keine neue Karriere ausgeführt.
[Vorregistriertes Quellenaudit](../../experiments/TRAIN-003-source-audit.md),
[kompakte Messausgabe](../../data/player-development-002-training/source-table-audit.json),
[ausführbare Extraktion](../../analysis/audit_training003_source.py).
Keine künstlichen Spieler oder zusätzlichen Matchsimulationen.

## Originalquelle und tatsächliche Datenstruktur

Der [Originalbericht](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test)
verlinkt das [Trainingworkbook](https://pixeldrain.com/u/92NJyBDb), Upload
01.11.2026. 26.333 Bytes, SHA256
`005a704ed0f9205b8003c150ab182f0944d7cea2f8c8745078344eac612c3552`.
Eine Tabelle `Sheet1`, Plan-IDs 0–50 in Zeilen14–64, 37 Endpunkte:
CA plus36 Attribute. Alle1.887 numerischen Zellen vorhanden, keine Formeln,
keine imputierten Nullen. Originaldatei bleibt unverändert außerhalb von Git.

Quelle berichtet: 18Jahre, Ausgangsattribute8, Professionalität/Ehrgeiz12,
Trainerattribute16, Anlagen20, 4-2-4, zwölf Monate/100Spiele und doppelte
Intensität für gute/sehr gute Kondition. Verletzungen und Moral sind laut Autor
per FMRTE fixiert. **A1 nennt PA130, A2 dagegen PA150**; der chinesische
Einleitungstext nennt zusätzlich beide Füße20. A10 berichtet20–30Spieler
je Stichprobe, ohne exakte Zuordnung pro Plan und ohne unabhängige
Karrierereplikate. Weder Buildhash noch Einzelspielerwerte, Varianz,
Start-/Endsavebelege, RNG-Strategie, Wochenkalender oder Readbacks enthalten.
Die abgedruckten Attributänderungen sind Quelleneinheiten; eine unabhängige
Roh-/Anzeigeskalenkalibrierung fehlt.

## Vorab benannter Vergleich der Empfehlungen38 und46

38: Conditioning + Attacking Ball Work. 46: Light Conditioning + Conditioning
+ Attacking Ball Work + Defensive Ball Work. Beide mit Quickness-Fokus.
Es handelt sich um verschiedene Wochenplanpakete; keine isolierte Zusatzfokusstudie.
Locators: Plan38 in Zeile52, Plan46 in Zeile60; CA in SpalteJ, englische
Attributbeschriftungen in Zeile12.

| Saisonänderung laut Originaltabelle | Plan38 | Plan46 | 46−38 |
|---|---:|---:|---:|
| CA |31,15|33,25|+2,10|
| Acceleration (AM) |2,90|2,75|−0,15|
| Pace (AS) |3,05|2,85|−0,20|
| Quickness-Mittel aus beiden |2,975|2,800|−0,175|
| Jumping Reach (AN) |1,30|1,40|+0,10|
| Stamina (AP) |2,15|1,85|−0,30|
| Anticipation (AK) |2,10|2,75|+0,65|
| Finishing (U) |1,20|1,35|+0,15|
| Strength (AR) |2,25|2,30|+0,05|

**Der größere berichtete CA-Zuwachs geht hier mit weniger Tempo-/Antrittszuwachs
einher.** Welcher Plan praktisch besser ist, hängt bereits in dieser Tabelle
vom Ziel ab. Wegen unbekannter Clusterzahl/Varianz keine KIs, p-Werte oder
kausale Trainingsrangfolge. Das ist eine neue Nachrechnung derselben Quelle,
keine unabhängige Bestätigung ihres Experiments oder allgemeine Trainingsempfehlung.

Nach Sichtung zusätzlich explorativ: Beide Restpläne0/1 unterscheiden sich
in der Fokusbeschriftung (`no` gegen `Quickness`, Zeilen14/15). Berichteter
Fokusarm: Antritt+1,1267, Tempo+1,0600, Quickness-Mittel+1,0933 gegenüber
ohne Fokus; CA-Abstand nur+0,5667. Gleichzeitig JR−0,48 und Ausdauer−0,68.
Fehlende Paarungs-/Zufallsbelege, variable20–30Spieler und fixierte Zustände
verhindern eine kausale Zuschreibung. Der Kontrast wurde **nach** Tabellensichtung
gewählt und ist ausdrücklich kein vorab bestätigter Primärbefund.

## Warum der neue Karrierepilot dennoch nicht startet

Nutzerautorisierung für isolierte Wegwerfkarrieren liegt vor. Fehlende
individuelle Anwesenheit ist **allein kein Ausschlussgrund für Intention-to-Treat**:
eine zuverlässig zugewiesene Intervention mit vollständigen Endpunkten erlaubt
eine Aussage zur Planzuweisung. Anwesenheit wäre für Dosis/Wirkung erforderlich.
Die ältere TRAIN-002-Anforderung wird deshalb nicht als universelles ITT-Gate übernommen.

Das tatsächliche Hindernis bleibt: kein lokal validierter Kalenderexecutor,
kein verlässlicher Setz-/Readbackweg für individuellen Fokus und kein belegter
Korpus unabhängiger Karriere-Ausgangszustände. `research/career.py` importiert
JSON-Checkpoints; es steuert FM nicht. Die übrigen Karriereprogramme sind
lesende Save-/Parserdiagnosen. Der vorhandene R3-Fehler betraf Taktikmarker;
er beweist keine Unlesbarkeit sämtlicher Attribute, liefert aber keinen Executor.
Heute installierter Reader fmsave0.9.0, Python3.12.10. Der aktuell erneut
abgefragte Upstream bleibt f4f70f62; das ist keine lokale Decoderabnahme.
Keine zeitaufwendige Parserreparatur begonnen.

Abrechnung: **0neueKarrierearme,0angefangeneArme,0Armwochen,0Advances,
0Saveänderungen,0neueMatchergebnisse.** Kein gestarteter Arm ausgeschlossen.
Verletzungstage/Minuten/Kondition/Schärfe der externen Pläne sind unbekannt;
fixierte Verletzungen erlauben gerade keine reale Sicherheitsbewertung.

Reproduktion:

```powershell
.venv/Scripts/python.exe -m analysis.audit_training003_source <lokales-training.xlsx> --output <audit.json>
.venv/Scripts/python.exe -m unittest tests.test_training003_source -v
```

Das Skript prüft den Quellhash vor dem XML-Lesen, inventarisiert alle51Pläne
und veröffentlicht nur ausgewählte Werte und Differenzen. Keine Excel-Formeln,
Makros, Fremdprogramme oder Spielressourcen werden ausgeführt.
Der erste reine XML-Konsolenausdruck brach wegen chinesischer Zeichen in der
Windows-cp1252-Ausgabe ab; UTF-8 korrigierte ausschließlich die Ausgabe.
Die Quelldatei wurde nicht geändert, keine Messzeile ausgeschlossen oder ersetzt.

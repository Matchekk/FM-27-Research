# Findings – geprüfte Forschungsergebnisse

**Stand 2026-11-07 · Match- und Karrieredaten für FM27 27.0.0+2493426**

Hier stehen ausschließlich Befunde mit eindeutiger Experiment-ID, verlinktem Protokoll, Buildnummer, Messwerten und Unsicherheit. Ergebnisse aus vorherigen Chat-Zusammenfassungen werden erst nach Einsicht in originale Messdaten und Reproduzierbarkeitsprüfung eingetragen.

## Übersicht

| ID | Thema | Effekt | Build | Evidenzstufe | Beleg |
|---|---|---|---|---|---|
| VALID-001 | Lab-Adapter | 24 vollständige Matches. Acht Wiederholungsgruppen stimmen in Endstand, Teamstatistik und Endtick exakt überein. | 27.0.0+2493426 | Eingabe und Wiederholbarkeit lokal geprüft | [Validierung](experiments/VALID-001-adapter.md) |
| ATTR-001 | Screening | 16 Attribute mit je 40 Paaren. Kleinster BH-q 0,4042. | 27.0.0+2493426 | Explorativ | [Screening](experiments/ATTR-001-screening.md) |
| ATTR-002 | Sprunghöhe | +0,316 ΔxGD pro Spiel, 95-%-KI [0,203; 0,432], BH-q 0,00010. | 27.0.0+2493426 | Bestätigt im Hauptszenario, 240 neue Paare | [Hauptreplikation](experiments/ATTR-002-hauptreplikation.md) |
| ATTR-002 | Antritt | +0,229 ΔxGD, 95-%-KI [0,107; 0,348], BH-q 0,00050. | 27.0.0+2493426 | Bestätigt im Hauptszenario, 240 neue Paare | [Hauptreplikation](experiments/ATTR-002-hauptreplikation.md) |
| ATTR-002 | Tempo | +0,144 ΔxGD, 95-%-KI [0,033; 0,254], BH-q 0,01847. | 27.0.0+2493426 | Bestätigt im Hauptszenario, 240 neue Paare | [Hauptreplikation](experiments/ATTR-002-hauptreplikation.md) |
| ATTR-002 | Direkter Vergleich | Sprunghöhe minus Tempo +0,172 ΔxGD, 95-%-KI [0,052; 0,291], BH-q 0,0094. Der Abstand zwischen Sprunghöhe und Antritt bleibt offen. | 27.0.0+2493426 | Sekundärer Rangvergleich, 240 Paare | [Alle zehn Kontraste](experiments/ATTR-002-hauptreplikation.md#direkte-attributvergleiche) |
| ATTR-003 | Kontext | Gegnerwechsel und direkter Heim-/Auswärtsvergleich für Antritt und Tempo liefern breite Intervalle. | 27.0.0+2493426 | Kontexttests, je 40 Paare pro Attribut | [Zusatzszenarien](experiments/ATTR-003-zusatzszenarien.md) |
| ATTR-004 | Sprunghöhe und Antritt über acht Szenarien | Gegen Baseline +0,325 xGD, 95-%-KI [0,266; 0,383], bzw. +0,303 xGD, 95-%-KI [0,246; 0,361]. Beide Holm-p < 0,001. | 27.0.0+2493426 | Beide Einzeleffekte im Szenariomittel bestätigt, 1.120 neue Tripel | [Ergebnisse](experiments/ATTR-004-ergebnisse.md#sekundärtests-gegen-baseline) |
| ATTR-004 | Direkter Vergleich | Sprunghöhe minus Antritt +0,021 xGD, 95-%-KI [−0,038; +0,080], p = 0,479. Das Intervall liegt innerhalb von ±0,10 xGD. | 27.0.0+2493426 | Vorregistrierter Primärtest, mittlerer Unterschied praktisch klein | [Ergebnisse](experiments/ATTR-004-ergebnisse.md#primärer-endpunkt) |
| ATTR-005 | Sprunghöhe und Antritt nach Positionsgruppe | Höchste Baseline-Kontraste im Angriff. Sprunghöhe +0,232 xGD, 95-%-KI +0,073 bis +0,392, Holm-p = 0,058. Antritt +0,166 xGD, 95-%-KI −0,007 bis +0,338, Holm-p = 0,652. Alle direkten Kontraste bleiben unsicher. | 27.0.0+2493426 | Explorativ, 100 gepaarte Seeds | [Positionsscreening](experiments/ATTR-005-ergebnisse.md) |
| ATTR-006 | Sprunghöhe für AMR, AML und ST | +0,171 xGD pro Match, 95-%-KI +0,052 bis +0,290, p = 0,00498. Die Intervalluntergrenze liegt unter +0,10 xGD. | 27.0.0+2493426 | Positiver Effekt im getesteten Standardfixture bestätigt, 300 neue Paare | [Bestätigung](experiments/ATTR-006-ergebnisse.md) |
| ATTR-007 | Sprunghöhe nach Angriffsposition | Shapley ST +0,103 xGD, 95-%-KI +0,042 bis +0,163, Holm-p = 0,0065. ST minus Flügelmittel +0,088 xGD, 95-%-KI +0,016 bis +0,160, Holm-p = 0,104. Der isolierte ST-Effekt und die Interaktionen bleiben unsicher. | 27.0.0+2493426 | Explorativ, 200 neue Achtarmblöcke | [Faktorielle Studie](experiments/ATTR-007-ergebnisse.md) |
| TRAIN-001 | Wochenpläne | Profis P mit höherer Kondition und Spielschärfe. U19 I mit einem statt acht Verletzungseinträgen bei ähnlichen Rohwertzuwächsen. | 27.0.0+2493426 | Explorativ, ein Save-Ableger je Arm | [Karriereversuche](experiments/TRAIN-001-karriere.md) |

ATTR-001 bis ATTR-004 werteten jeweils ein Attribut um vier Anzeigepunkte bei zehn Feldspielern auf. ATTR-005 änderte jeweils zwei oder drei Spieler einer Positionsgruppe. ATTR-006 bestätigte den positiven xGD-Effekt der Sprunghöhenanhebung bei drei Angreifern im Standardfixture. Dribbling und Beweglichkeit bleiben nach der Hauptreplikation unklar. Einsatzfreude belegte Screening-Platz 13 und hat keine neue Hauptreplikation. Der Aufbau erlaubt einzelne Rangvergleiche im Standardfixture. Eine übergreifende FM27-Meta-Rangliste bleibt offen.

## Bei jedem neuen Befund dokumentieren
1. Hypothese und präzise Intervention.
2. Primäre Zielgröße, Effektgröße, Konfidenzintervall, Stichprobe.
3. Wiederholbarkeit/Signifikanzkorrektur und Fehlerquote.
4. Gültigkeitsbereich (Build, Teams, Gegner, Taktiken).
5. Welche alternative Erklärung weiterhin möglich ist.
6. Link zu Experimentdokument, Manifest und Rohdaten.

## Ergänzung 14.11.2026 – TACT-001-P0 auf neuem Build

Die obigen ATTR- und TRAIN-Einträge bleiben unverändert Build
`27.0.0+2493426` zugeordnet. Der folgende Befund verwendet **27.0.1+2503222**.

| ID | Vorregistrierter Kontrast | Ergebnis | Evidenz und Grenze |
|---|---|---|---|
| TACT-001-P0 | Pressing×Defensivlinie: combined − press − line + baseline auf xGD; Seitenmittel im Seed, zwei Gegner je 1/2 | +0,020 xGD-DoD, 95-%-t-KI [−0,770; +0,809], p=0,9565; 128 Hauptmatches, 16 unabhängige Seedblöcke | Explorativ, Richtung offen. Kein Nachweis von Äquivalenz, kein Taktiksieger und keine universelle Meta-Aussage. |

Keiner der zehn sekundären DoD-Tests erreicht die vorregistrierte Holm-Schwelle.
Die Kontrast-SD beträgt 1,818 gegen high_press und 0,831 gegen deep_block.
23 technische Matches, sieben exakte Wiederholungen und die negative Binärprobe
bestanden; keine Hauptausfälle, Ausschlüsse oder Retries. Die Vorregistrierung
wurde in `650a89a`, die technische Freigabe in `c9a4353` vor der Hauptserie gepusht.
[Ergebnisbericht](experiments/TACT-001-P0-results.md) ·
[Vorregistrierung](experiments/TACT-001-P0-preregistration.md) ·
[Matchmessungen](data/tact-001-p0/main.jsonl) ·
[Effekte und Powerplanung](data/tact-001-p0/effects.json).

## 2026-11-14 – TACT-001-P1B, FM27 27.0.1+2503222

**Exploratives Fünffaktor-Screening**, 2.048 gültige Hauptmatches und 64
vollständige unabhängige Seedblöcke. Explizite negative Resolution-V-Halbfraction
E=−ABCD, unveränderte eigene IP-4-2-3-1/OOP-4-4-1-1 und zwei synthetische Gegner.

| Hauptkontrast | xGD | Marginales 95-%-KI | Holm-p (5) |
|---|---:|---|---:|
| Häufigeres Pressing | +0,063 | [−0,022; +0,148] | 0,721 |
| Höhere Defensivlinie | −0,007 | [−0,090; +0,076] | 1,000 |
| Höheres Tempo | +0,034 | [−0,042; +0,111] | 1,000 |
| Kürzere Pässe | +0,018 | [−0,056; +0,093] | 1,000 |
| Größere Angriffsbreite | +0,026 | [−0,056; +0,108] | 1,000 |

Kein Haupttest, keine der zehn explorativen Paar-DoDs und keiner der 25
Sekundärtests erreicht seine vorregistrierte Holm-Schwelle. Linie×Tempo ist
mit +0,177 der größte positive Paar-Schätzer, Holm-p=0,134; kein korrigierter
Nachweis. Alle fünf Hauptintervalle erfüllen die gewünschte volle Breite≤0,30.
Die Halbfraction aliasiert Haupt-/Paarwirkungen mit Vierfach-/Dreifachinteraktionen.

Die eingefrorene Auswahlregel liefert ausschließlich explorative Vorschläge:
D15 (häufigeres Pressing, höhere Linie, höheres Tempo, kürzere Pässe,
Standardbreite) und D09 (häufigeres Pressing, Standardlinie/-tempo, kürzere
Pässe, Standardbreite). Ihre Kontextmittel-Abstände zu D00 sind +0,229/+0,180
xGD aus denselben Selektionsdaten. **Keine Siegerbestätigung**, keine Aussage
zu optimalen realen Karrieretaktiken. Punkte/Tore/Gegentore vollständig berichtet.

72 technische Vollmatches, alle 64 Eingabezellen, acht exakte Wiederholungen
und erwartete Exit108-Negativprobe bestanden. Keine Hauptausfälle, Ausschlüsse,
Retries, Ersatzseeds oder Holdoutmatches. Historische ATTR- und P0-Befunde
bleiben unverändert. [Ergebnisbericht](experiments/TACT-001-P1B-results.md) ·
[Vorregistrierung](experiments/TACT-001-P1B-preregistration.md) ·
[Rohmessungen](data/tact-001-p1b/main.jsonl) · [Effekte](data/tact-001-p1b/effects.json).

## 2026-11-14 – TACT-001-P1C, unabhängiger Seed-/Präzisionspilot

FM27 27.0.1+2503222; D15 als einziges eingefrorenes Paket gegen D00, bekannte
synthetische Discoverygegner.512 Hauptmatches/128 vollständige neue Seedblöcke.
Primär tatsächliche Punkte **+0.098/Match**,95-%-KI
[-0.137; +0.333],p=0.41246.
Volle Breite0,470 statt Ziel≤0,30, Schätzer unter praktischer Schwelle+0,15.
**Vorregistrierte Hinweisschwelle nicht erfüllt: Rollen/OOP-Strukturen priorisieren,
dieses Instruktionspaket nicht unbegrenzt wiederholen.** Keine Äquivalenzbehauptung.

Sekundär xGD+0,196 (Holm5p=0,093); xGA−0,161 (Holm5p=0,027) als
korrigierter sekundärer Hinweis auf geringere Chancenabgabe. Das bestätigt weder
Punkteverbesserung noch Karriereübertragbarkeit. D09 bleibt archiviert; keine
nachträgliche Kandidatenauswahl.16 technische Vollmatches/8 exakte A/A-Paare
und Exit108-Negativkontrolle bestanden; keine Ausfälle/Retry/Ersatzseeds/Holdouts.
[Ergebnis](experiments/TACT-001-P1C-results.md) ·
[Messungen](data/tact-001-p1c/main.jsonl) · [Planung](data/tact-001-p1c/effects.json).

## 2026-11-14 – TACT-002-R0,FM27 27.0.1+2503222

Vorregistrierter Rollenvarianzpilot,512Hauptmatches/64neueSeedblöcke:
DLF−CF marginal über zweiAMC-Rollen **-0.018xGD**,95-%-KI
[-0.160;+0.124],p0.80072. VolleBreite0,283 erreicht
Pilotziel≤0,50. Kein Primärnachweis,keine der siebenSekundärhypothesen nachHolm
signifikant. AMC+0,049xGD,Interaktion−0,211[−0,544;+0,122]; Richtung unklar.
ST-Punkteffekt−0,098[−0,283;+0,088]. KeinKandidat/Rollensieger ausgewählt.

32technischeVollmatches/16exakteA/A und Exit108bestanden;alleInputs/Seeds/Rollen/
PI/Profile nativ geprüft. Keine nativen Ausfälle,Retries,Ersatzseeds oderHoldouts.
Synthetische omnipotente Profile und feste zweiGegner schränken Übertragung ein;
kein Beweis universeller Wirkungsfreiheit oder formalerÄquivalenz.
[Ergebnis](experiments/TACT-002-R0-results.md) ·
[Rohmessungen](data/tact-002-r0/main.jsonl) · [Runde2](docs/round2/README.md).

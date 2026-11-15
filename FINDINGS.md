# Findings – geprüfte Forschungsergebnisse

## 2026-11-15 – N3-SHARPPOS-C1, marginaler Zweispieler-Schärfenutzen

**4.096 gültige Hauptmatches,1.024 unabhängige neue Blöcke**, FM27 27.0.1+2503222.
AMC/ST-Nutzen minus CB-Nutzen **0,053613xGD/Match**,
95%-KI **[-0,003894; 0,111120]**,p=0.0676289; innerhalb vorab±0,15.
Volle Breite0,115014 erreicht Ziel≤0,15. Kleinere Vorteile
bei AMC/ST bleiben möglich; kein Primärnachweis und keine universelle Positionsregel.
Sekundär Tore+0,133789 undxGF+0,085995 bestehenHolm6, Punkte+0,075684 nicht.
Separate absolute Gruppennutzen nicht identifiziert; feste Akteure/Rollen,
omnipotente Positionsratings und zwei feste Gegner begrenzen Übertragung.
16Technik/achtA/A+Exit108 und alle4.113Jobs vollständig,0unerwarteteAusfälle,
keine Ausschlüsse/Retry/Ersatz. Rohbelege zweimal geprüft, alle sieben formalen
Statistiken separat skalar reproduziert. [Ergebnisse](experiments/N3-SHARPPOS-C1-results.md) ·
[Messungen](data/night-003-sharppos/main.jsonl) ·
[Nachrechnung](data/night-003-sharppos/independent-statistics-review.json).

## 2026-11-15 – N3-SHARPSTRUCT-C1, Schärfe×IP bei fester OOP

**4.096 gültige Hauptmatches, 512 unabhängige neue Kontext-Seedblöcke.**
FM27 27.0.1+2503222, zwei feste synthetische Gegner, beide Teamseiten.
Vorregistrierte Interaktion `[STLESS10000−BASE10000]−[STLESS7000−BASE7000]`
bei originalem OOP4411: **−0,013320 xGD/Match**, 95-%-Welch-KI
**[−0,118593; +0,091953]**, p=0,803779; Bootstrap
[−0,118783; +0,090835]. Volle Breite0,210546 erreicht Ziel≤0,25.
Das gesamte Intervall liegt innerhalb der vorab festgelegten ±0,20:
praktisch große Interaktionen dieser Größenordnung werden im getesteten
Kontext nicht gestützt; kleinere Effekte und Übertragung bleiben offen.

Keine Holm6-Sekundärhypothese signifikant; Punkteinteraktion
−0,080078[−0,232091;+0,071935], Holm-p1,0. Keine globale Wirkungslosigkeit,
kein allgemeiner STLESS-Sieger und keine neuen Scoutinggewichte abgeleitet.
Omnipotente Positionsratings und zwei bekannte Gegner begrenzen die Aussage.
32 technische Vollmatches/16exakteA/A+Exit108, alle4.129Calls abgerechnet,
0 unerwartete Fehler/Fehlstellen/Ausschlüsse/Retry/Ersatz. Unveränderte Rohbelege
zweimal geprüft; Primäreffekt über separate skalare Arithmetik reproduziert.
[Vollständiger Ergebnisbericht](experiments/N3-SHARPSTRUCT-C1-results.md) ·
[Messungen](data/night-003-sharpstruct/main.jsonl) ·
[Nachrechnung](data/night-003-sharpstruct/independent-recalculation.json).

## 2026-11-15 – TACT-003-STLESS-R0, kontrollierte IP/OOP-Pakete

FM27 `27.0.1+2503222`, synthetische identische Rohprofile, zwei feste
Discoverygegner.512 gültige Hauptmatches bilden64 unabhängige neue Seedblöcke;
Seiten im Seed gemittelt. Primär IP×OOP **+0,074 xGD-DoD**,95-%-KI
**[−0,191;+0,340]**,p=0,577429. Präzisionsziel0,50 mit voller Breite0,530562
verfehlt. Praktisch positive Moderation+0,20 bleibt möglich; keine Äquivalenz.

Vorregistrierter Sekundärbefund: Das konkrete IP4231→IP4240-Paket senkt xGD
marginal über beide OOP-Stellungen um **−0,350/Match**,95-%-KI
**[−0,502;−0,198]**,Holm7-p=0,000162. Nur dieser Sekundärtest besteht Holm7.
OOP−0,167,Holm-p0,091; Punkteinteraktion+0,273[−0,122;+0,669],Holm-p0,861.
Tore/Gegentore/xGF/xGA vollständig berichtet, kein korrigierter Interaktionsnachweis.

Das IP-Paket verschiebt AMC→AMCL und ST→AMCR/SecondStriker; das OOP-Paket
verschiebt dieselben Akteure nach AMCL/AMCR mit OPAM. Es handelt sich um
Positions-/Rollenpakete einschließlich lateraler Neuordnung, keinen isolierten
ST-Abwesenheits- oder Laufwegmechanismus und keine Aussage gegen sämtliche
stürmerlosen Taktiken. Keine neue Scoutinggewichtung oder Karrierebestätigung.

32 technische Vollmatches+erwartete Exit108-Probe,16 exakte A/A-Paare bestanden.
545/545 eigene Jobs vollständig;0 unerwartete Fehler/Ausschlüsse/Missing Values/
Retry/Ersatz/Holdouts. Sämtliche512 Rohresultate,64 Blöcke, Welch-/Bootstrap-
intervalle, Holm7 und Bereinigungen unabhängig nachgerechnet. Alte terminale
MECH-004-Teilserie wurde nicht ausgewertet oder fortgesetzt.
[Ergebnis](experiments/TACT-003-stless-results.md) ·
[Rohmessungen](data/night-002-stless003/main.jsonl) ·
[unabhängiger Review](docs/night-002/STLESS003-RESULTS-REVIEW.md) ·
[Nachtbericht](docs/night-002/OVERNIGHT_REPORT.md).

## 2026-11-14 – MECH-004-SPLIT-R0, technische Identifizierbarkeit

FM27 `27.0.1+2503222`, unveränderter Observerhost, synthetischer D00-Kontext.
32 technische Matches mit vier gekreuzten C90/C7A-Armen, zwei Gegnern,
beiden Seiten und16 exakten A/A-Paaren bestanden. Beide Rohfelder überstehen
die ursprüngliche Vorbereitung und den ersten Fortschritt **getrennt**.
Cache8A ist bei C90=7000 stets70 und bei C90=10000 stets100, unabhängig von
C7A=7000/10000, für alle zehn Zielstarter in allen geprüften Startaufnahmen.

Das ist ein technischer Transferbefund, **noch kein Leistungsbefund**:
keine UI-Skala, Consumersemantik oder natürliche Karrierewirkung identifiziert.
Die32 Technikmatches bilden keine unabhängige Leistungsstichprobe; statistische
Effektintervalle für Fußballleistung sind hier nicht anwendbar. Eine erwartete
Exit108-Abweisung;0 unerwartete Fehler,0 Retry/Ersatz, alle Bereinigungen bestätigt.
[Technischer Bericht](experiments/MECH-004-split-validation.md) ·
[öffentliche Messungen](data/night-002-split004/technical.jsonl) ·
[unabhängige Rohabnahme](docs/night-002/SPLIT004-TECHNICAL-REVIEW.md).

**Nachfolgende Hauptserie terminal abgebrochen:**224 akzeptierte Matches,
1 vor der Engine gescheiterter Job,287 unbegonnene Plätze. Ein vom Director
eingeführter Versuch, abgeschlossene private Belege während des laufenden
Pfadscans zu archivieren, löste das Sicherheitsgate aus. Alle Belege wurden
bytegleich wiederhergestellt. Keine primären oder sekundären Leistungsschätzer
aus der unvollständigen Serie; kein Null-/Wirkungslosigkeitsbefund. Das obige
separate32-Match-Transferergebnis bleibt davon unterschieden.
[Terminalbeleg](data/night-002-split004/termination.json).

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

## 2026-11-14 – ATTR-009-Bridge, FM27 27.0.1+2503222

Vorregistrierter Masken×Rohattributpilot,384gültigeHauptmatches/32neueSeedblöcke:
`[JR−(Acc+Pace)/2]spezialisiert−[JR−(Acc+Pace)/2]omni`
**−0,162010xGD**,95-%-KI[−0,488421;+0,164401],p0,318851.
Bootstrap[−0,465728;+0,142482]. Primär-/Holm5-Nachweis fehlt;kleinsterHolm-p0,282016.
Punktekontrast−0,132813[−0,786684;+0,521059]. VollePrimärbreite0,65282
verfehlt Pilotziel0,50;praktisch relevante negative Effekte bleiben möglich.
Kein Äquivalenzbeweis und keine Erklärung der internationalen Rankingdiskrepanz.

Native Rohdosen60→80 bei zehn Feldspielern,aktiveIP/OOP-Familien20,
ungenutzte20versus1;D00,beidebekannteDiscoverygegner undbeideSeiten.
Keine FM-Anzeige12→16 kalibriert;passive Mechanismuszerlegung unidentifiziert.
32Technikmatches/8exakteA/A+Exit108 bestanden;alle417Versuchsplätze abgeschlossen,
0Ausfälle/Retry/Ersatz/Exklusion/Holdouts/Karriere. Unabhängig aus Rohdaten und
privaten Originalbelegen rekonstruiert. Historische ATTR-001–007 unverändert.
[Ergebnis](experiments/ATTR-009-results.md) · [Messungen](data/attr-009-bridge/main.jsonl) ·
[unabhängige Abnahme](docs/round3/RESULTS-REVIEW.md).
# 15.11.2026 – PD-CA-001, retrospektive Exportdiagnose

**Beobachtungsbasiert/explorativ; keine tatsächlichen CA-Grenzkosten.**
109öffentliche GK-Exportprofile,80Training/29diagnostischerHoldout, keine
Spielerüberschneidung/Missing/Ausschlüsse. Positionstabellen-Summenproxy mit
OLS: Holdout-MAE1,606,RMSE2,010,Bias+0,845 exportierteCA-Punkte. Gleich
komplexe OLS auf ungewichtetem Mittel derselben22Attribute: MAE4,630.
MAE-Abstand−3,024,bedingtes95-%-Spielerbootstrapintervall[−4,139;−1,908].

Der Autor hatte dieselben109Profile bereits analysiert; dies ist keine neu
gesammelte unabhängige Validierungskohorte. Build-/Save-/UI-Provenienz nicht
unabhängig abgenommen. BeobachteteCA15–118, Holdout41–109; keine Übertragung
auf Feldspieler/Eliteprofile/PA. Der Proxy identifiziert weder kausalen
Attributverbrauch noch nichtlineare Kosten oder Matchleistung proCA.
[Protokoll](experiments/PD-CA-001.md) ·
[Ergebnis und Grenzen](docs/player-development-001/CA_EFFICIENCY.md) ·
[Messauswertung](data/player-development-001-ca/profile-diagnostic.json).

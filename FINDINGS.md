# Findings – geprüfte Forschungsergebnisse

**Stand 2026-11-06 · Match- und Karrieredaten für FM27 27.0.0+2493426**

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
| TRAIN-001 | Wochenpläne | Profis P mit höherer Kondition und Spielschärfe. U19 I mit einem statt acht Verletzungseinträgen bei ähnlichen Rohwertzuwächsen. | 27.0.0+2493426 | Explorativ, ein Save-Ableger je Arm | [Karriereversuche](experiments/TRAIN-001-karriere.md) |

Die Effekte betreffen die Aufwertung desselben Attributs um vier Anzeigepunkte bei zehn Feldspielern. Dribbling und Beweglichkeit bleiben nach der Hauptreplikation unklar. Einsatzfreude belegte Screening-Platz 13 und hat keine neue Hauptreplikation. Der Aufbau erlaubt einzelne Rangvergleiche im Standardfixture. Eine übergreifende FM27-Meta-Rangliste bleibt offen.

## Bei jedem neuen Befund dokumentieren
1. Hypothese und präzise Intervention.
2. Primäre Zielgröße, Effektgröße, Konfidenzintervall, Stichprobe.
3. Wiederholbarkeit/Signifikanzkorrektur und Fehlerquote.
4. Gültigkeitsbereich (Build, Teams, Gegner, Taktiken).
5. Welche alternative Erklärung weiterhin möglich ist.
6. Link zu Experimentdokument, Manifest und Rohdaten.

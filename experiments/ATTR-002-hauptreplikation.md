# ATTR-002 – Hauptreplikation

**Stand 2026-11-06 · Bestätigte Einzeleffekte im getesteten Kontext · FM27 27.0.0+2493426**

Die fünf nach dem [Screening](ATTR-001-screening.md) ausgewählten Attribute wurden mit 240 neuen Seeds pro Attribut geprüft. Das Standardfixture, die zehn behandelten Feldspieler und der Kontrast von Anzeige 12 auf 16 blieben gleich. Die 240 Replikationsseeds überschneiden sich weder mit dem Screening noch mit den Gegner- und Venue-Listen. Alle 1.440 vorgesehenen Matches wurden akzeptiert. 240 Baselines standen jeweils fünf Interventionsläufen gegenüber.

Die Primäranalyse verwendet ΔxGD pro Seed-Paar und eine BH-Familie aus fünf Tests. Die 95-%-Intervalle sind paarweise Perzentil-Bootstrapintervalle ohne simultane Abdeckung. Die BY-Spalte zeigt die Sensitivität gegenüber beliebiger Abhängigkeit der Tests. Das [Effektarchiv](../data/matches/effects.json) enthält zusätzlich Stichproben-SD, Roh-p-Werte und alle zehn Zielgrößen. Jede Sekundärzielgröße hat ihre eigene BH-Familie. Aussagen über einen gemeinsamen Fehleranteil über alle Metriken und Szenarien lassen sich daraus nicht ableiten.

| Attribut | Δ xGD | 95-%-KI | BH-q | BY-q |
|---|---:|---:|---:|---:|
| JumpingReach | +0,316 | [0,203; 0,432] | 0,00010 | 0,00023 |
| Acceleration | +0,229 | [0,107; 0,348] | 0,00050 | 0,00114 |
| Pace | +0,144 | [0,033; 0,254] | 0,01847 | 0,04217 |
| Dribbling | +0,038 | [−0,072; 0,150] | 0,62755 | 1,00000 |
| Agility | +0,006 | [−0,105; 0,119] | 0,91404 | 1,00000 |

Sprunghöhe, Antritt und Tempo haben positive Einzeleffekte im getesteten Setup und bleiben auch unter BY unter 0,05. Die Intervalle für Dribbling und Beweglichkeit enthalten null. Ein Äquivalenztest mit praktischer Schwelle steht aus.

## Direkte Attributvergleiche

Für jeden der zehn Kontraste gehen dieselben 240 Seeds ein. Pro Seed wird der geschätzte Interventionseffekt von A um den Effekt von B vermindert. Die geteilte Baseline fällt rechnerisch weg. Diese Kontraste erhalten eine eigene BH-/BY-Familie und sind sekundäre Rangvergleiche. Die ursprüngliche Dokumentation weist für sie keine separate Vorregistrierung nach.

| A minus B | Δ xGD | 95-%-KI | BH-q | BY-q |
|---|---:|---:|---:|---:|
| Pace − Acceleration | −0,085 | [−0,202; 0,034] | 0,1997 | 0,5849 |
| Pace − JumpingReach | −0,172 | [−0,291; −0,052] | 0,0094 | 0,0275 |
| Pace − Dribbling | +0,107 | [−0,004; 0,217] | 0,0940 | 0,2754 |
| Pace − Agility | +0,138 | [0,030; 0,247] | 0,0212 | 0,0620 |
| Acceleration − JumpingReach | −0,087 | [−0,218; 0,042] | 0,2153 | 0,6306 |
| Acceleration − Dribbling | +0,191 | [0,078; 0,305] | 0,0026 | 0,0075 |
| Acceleration − Agility | +0,223 | [0,108; 0,338] | 0,0008 | 0,0023 |
| JumpingReach − Dribbling | +0,278 | [0,160; 0,398] | 0,0001 | 0,0003 |
| JumpingReach − Agility | +0,310 | [0,186; 0,434] | 0,0001 | 0,0003 |
| Dribbling − Agility | +0,032 | [−0,085; 0,146] | 0,5960 | 1,0000 |

Sprunghöhe liegt im direkten Vergleich vor Tempo. Für Sprunghöhe gegenüber Antritt sowie Antritt gegenüber Tempo bleibt die Rangfolge offen. Der Kontrast Tempo gegen Beweglichkeit liegt nach BH unter 0,05 und nach BY darüber. Die gruppenweite Intervention erlaubt keine Schätzung pro Einzelspieler oder pro zusätzlichem Attributpunkt.

[Matchmessungen](../data/matches/confirmation.jsonl) · [Manifest](../data/matches/manifest.json) · [Effektarchiv](../data/matches/effects.json) · [Rechenprüfung](../analysis/verify_matches.py)

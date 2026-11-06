# TRAIN-001 – Conditioning und Wochenpläne in der Karriere

**Stand 2026-11-06 · Explorativ · FM27 27.0.0+2493426**

Die Karriereversuche verwendeten Ableger eines Bayern-Saves, Kalender-Readback und einen lokalen Decoder (fmsave 0.10.0). Der Build wurde anhand des Saves und des Engine-Hashes erfasst. Die importierten Messwerte wurden aus den lokalen Beobachtungen nachgerechnet. Die Daten enthalten Veränderungen pro zufällig zugeordnetem Teilnehmerkürzel. Kürzel gelten nur innerhalb eines Versuchs und einer Kohorte. Absolute Spielerprofile, Namen, Quell-IDs, Alter und individuell zuordenbare Verletzungseinträge fehlen im öffentlichen Archiv. Spielbelastung und Verletzungen sind als Gruppenwerte dokumentiert.

| Versuch | Zeitraum im Save | Auswertung und Exposition |
|---|---|---|
| Zweiwochenpilot | 27. Juli bis 10. August 2026 | 22 Profis je Arm. A Conditioning, B Heavy Conditioning, C Rest, D Light Conditioning. Nur 2/5, 4/5, 1/5 und 1/5 der jeweils gesetzten Slots standen so im Endkalender. Auswertung als technischer Pilot. |
| Conditioning vs. Heavy | 27. Juli bis 7. September 2026 | 22 Profis je Arm, 12/12 gepaarte Slots im Endkalender erhalten, keine übrigen Kalenderunterschiede in den geprüften Wochen. |
| Conditioning vs. Rest | 27. Juli bis 24. August 2026 | 22 U19-Spieler je Arm, 8/8 gepaarte Slots im Endkalender erhalten, keine übrigen Kalenderunterschiede in den geprüften Wochen. |
| Fünf Wochenplan-Wochen | 24. August bis 28. September 2026 | Je 22 Profis und U19-Spieler pro Arm. 14/14 beziehungsweise 15/15 gezielte Slots erhalten. Zwei weitere Slots wichen bei den Profis ab. |

Endpunktdifferenzen sind arithmetische Mittel über gematchte Spieler. Bei den Profis ergab Heavy minus Conditioning für Tempo +0,227 Rohpunkte, für Beweglichkeit −0,136, für Antritt und Ausdauer jeweils 0 und für CA +0,091. Conditioning/Heavy erfassten 14.801/14.731 Spielminuten und 9/4 Verletzungseinträge. In der U19 ergab Rest minus Conditioning für Tempo −0,045, Beweglichkeit −0,318, Antritt −0,091, Ausdauer +0,318 Rohpunkte und CA +0,227. Conditioning/Rest erfassten 5.940/5.850 Minuten und jeweils vier Verletzungseinträge. Die beobachteten Endkalender belegen die gesetzten Einheiten, geben aber keine vollständige individuelle Teilnahmehistorie her.

### Fünfwochenvergleich

P umfasst bei den Profis taktische Einheiten und bei der U19 ausgewogene Einheiten für Angriff, Verteidigung und Torwart. I setzt individuelle Entwicklung und Conditioning ein, ergänzt um Pressing bei den Profis beziehungsweise ausgewogenen Angriff bei der U19. R ersetzt die ersten beiden ausgewählten Slots durch Ruhe. Die übrigen Termine folgen dem jeweiligen Kalender. „Individuelle Entwicklung“ ist hier der Name einer Teameinheit.

| Gruppe | Arm | Ø ΔCA | Ø Δ Attributrohwert | Δ Kondition | Δ Spielschärfe | Verletzungseinträge |
|---|---|---:|---:|---:|---:|---:|
| Profis | P | 0,00 | −0,049 | +816 | +354 | 4 |
| Profis | I | +0,05 | −0,118 | +734 | +260 | 3 |
| Profis | R | −0,09 | −0,121 | +623 | +112 | 5 |
| U19 | P | +2,00 | +0,296 | +414 | +647 | 8 |
| U19 | I | +2,18 | +0,297 | +665 | +669 | 1 |
| U19 | R | +2,27 | +0,299 | +646 | +559 | 8 |

Kondition und Schärfe sind Rohpunkte am Endtag. U19-Arm I hatte in diesem Lauf weniger erfasste Verletzungen bei ähnlichen Attributzuwächsen. P führte bei den Profis in diesem Lauf zu höherer Kondition und Spielschärfe als die beiden anderen Pläne. Verletzungseinträge sind Ereignisse, keine Ausfalltage. Spielminuten und Verletzungen entwickelten sich je Lauf unterschiedlich.

Die Intervention betrifft den gesamten Kader beziehungsweise den Save-Ableger. Die 22 Spieler sind Messungen innerhalb desselben Laufs und keine 22 unabhängigen Wiederholungen des Treatments. Bytegleiche A/A-Eingaben ergaben nach zwei Wochen identische Rohattributprofile bei 16/22 Spielern, identische CA und PA bei 22/22 und identische Kondition bei 8/22. Die Serie erlaubt daher keine inferenzstatistisch abgesicherte Rangfolge der Wochenpläne. Der erste umgeschriebene Save für Trainerqualität wurde beim Laden abgewiesen. Für Trainerqualität, persönlichen Zusatzfokus und individuelle Intensität liegt kein abgeschlossener Wirkungsvergleich vor.

[Trainingsmanifest](../data/training/manifest.json) · [Spielerdifferenzen](../data/training/player-deltas.jsonl) · [Kalender und Belastung](../data/training/exposure.json) · [A/A-Kontrolle](../data/training/repeatability.json)

# ATTR-003 – Gegnerprofil und Heim/Auswärts

**Stand 2026-11-06 · Kontexttests · FM27 27.0.0+2493426**

Getestet wurden die zwei höchsten Screening-Kandidaten Tempo und Antritt. Jedes Szenario enthielt 40 Baselines und 80 Interventionen. Alle 360 vorgesehenen Matches wurden akzeptiert. Die Gegnerliste verwendet eigene Seeds. Die Heim- und Auswärtsvarianten verwenden dieselben 40 Seeds für einen direkten Standortvergleich. Diese Seeds liegen außerhalb der Listen für Screening, Hauptreplikation und Gegnerprofil.

Das Gegnerprofil änderte bei gleichem Personal die Mentalität des Gegners auf Adapterwert 6. Für Heim/Auswärts wurden beide Kader auf 23 aktive Plätze angeglichen. Der Auswärtseingriff überträgt Spielerprofile auf feste native Plätze der Gegenseite und bewertet alle Messwerte aus Sicht des behandelten Teams. Ein erster einfacher Seitentausch scheiterte vor der Simulation an der ungleichen Kaderkapazität 23/26. Nach der Korrektur wurde auf den bereits akzeptierten Ergebnissen aufgebaut. Die protokollierten Einstellungen stehen im [Manifest](../data/matches/manifest.json).

| Szenario | Attribut | Δ xGD | 95-%-KI | BH-q |
|---|---|---:|---:|---:|
| Offensiverer Gegner | Pace | +0,068 | [−0,287; 0,439] | 0,7180 |
| Offensiverer Gegner | Acceleration | +0,304 | [−0,009; 0,607] | 0,1324 |
| Auswärts | Pace | +0,331 | [0,037; 0,639] | 0,0393 |
| Auswärts | Acceleration | +0,414 | [0,121; 0,726] | 0,0191 |
| Heim mit angeglichenem Kader | Pace | +0,297 | [0,076; 0,527] | 0,0147 |
| Heim mit angeglichenem Kader | Acceleration | +0,365 | [0,087; 0,648] | 0,0147 |
| Direkter Kontrast Auswärts minus Heim | Pace | +0,034 | [−0,347; 0,428] | 0,8663 |
| Direkter Kontrast Auswärts minus Heim | Acceleration | +0,048 | [−0,314; 0,412] | 0,8663 |

Jede der drei Szenarioanalysen korrigiert zwei Attributtests pro Zielgröße. Die zwei direkten Venue-Kontraste bilden eine separate Familie. Im Auswärtsszenario ist Tempo nach BH auffällig und liegt unter BY bei 0,0589. Für Antritt beträgt das BY-q dort 0,0287. Beide direkten Venue-Intervalle sind breit und enthalten null. Der Seitenwechsel erfasst auch mögliche Effekte der Fixture-Plätze. Für einen formalen Vergleich der Mentalitätswirkung wäre ein Paarvergleich mit identischen Seeds und jeweils einer Baseline pro Gegnerprofil nötig. Sprunghöhe war in den Zusatzszenarien nicht enthalten.

[Gegnerdaten](../data/matches/opponent.jsonl) · [Auswärtsdaten](../data/matches/away.jsonl) · [Heimdaten](../data/matches/venue_home.jsonl) · [Effektarchiv](../data/matches/effects.json)

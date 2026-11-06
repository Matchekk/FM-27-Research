# ATTR-004 – Ergebnisse der Cross-Tactic Attribute Validation

**6. November 2026 · FM27 27.0.0+2493426 · 3.360 vollständige Hauptmatches**

Die Anhebung von JumpingReach und die Anhebung von Acceleration verbesserten den xG-Saldo gegenüber Baseline im Mittel über die acht Szenarien. Der direkte Unterschied war praktisch klein. Das 95-%-Intervall lag vollständig zwischen den vorregistrierten Schwellen von −0,10 und +0,10 xGD pro Match.

## Lauf und Datenqualität

Die [Vorregistrierung](ATTR-004-cross-tactic.md) und der Analysecode wurden vor dem ersten Match in `ccfd630` gepusht. Das lokale Spielstartprotokoll meldete Build `27.0.0+2493426`. Der SHA-256 des geladenen Engine-Plugins, der Host-Hash und der Ressourcenfingerabdruck entsprachen VALID-001. [Laufmanifest](../data/attr-004/manifest.json)

Die 96 technischen Läufe prüften alle acht Szenarien und alle drei Arme. Alle 48 Wiederholungspaare stimmten bei Endstand, Teamstatistik und Endtick exakt überein. Die Prüfung deckte die Aufstellungs- und Rollenbindung, die kontrollierten Startprofile sowie alle 69 Attribute der jeweils 23 aktiven Spieler pro Team ab. Für die Auswärtsspiele wurden die aktiven Profile und taktischen Eingaben auf die jeweils anderen nativen Slots übertragen und dort geprüft. Die ungültige Konfiguration endete mit Exitcode 108. [Validierungsbericht](../data/attr-004/validation-summary.json)

Die Hauptserie lief von 22:38 bis 23:10 Uhr MEZ. Alle acht Szenarien lieferten je 140 vollständige Seed-Tripel. Jedes Tripel enthält Baseline, JumpingReach 12→16 und Acceleration 12→16. Es gab keine fehlgeschlagenen Hauptversuche, keine Wiederholungen und keine Ausschlüsse. Der Export prüfte die lokalen SHA-256-Belege sämtlicher akzeptierten Matches erneut. [Hauptmessungen](../data/attr-004/matches.jsonl)

## Primärer Endpunkt

| Gleichgewichteter direkter Kontrast | Δ xGD pro Match | 95-%-KI | p |
|---|---:|---:|---:|
| JumpingReach − Acceleration | +0,021 | [−0,038; +0,080] | 0,479 |

Der zweiseitige Primärtest verwirft H₀ bei α = 0,05 nicht. Die Welch-Schätzung hat einen Standardfehler von 0,030 xGD. Das vorregistrierte stratifizierte Bootstrap-Intervall beträgt [−0,037; +0,078]. Beide Intervalle liegen innerhalb der praktischen Schwellen. Die Aussage betrifft den Mittelwert der acht Szenarien.

## Sekundärtests gegen Baseline

| Arm gegen Baseline | Endpunkt | Δ [95-%-KI] | p | p (Holm) |
|---|---|---:|---:|---:|
| JumpingReach | xGD | +0,325 [+0,266; +0,383] | <0,001 | <0,001 |
| JumpingReach | xGF | +0,100 [+0,072; +0,127] | <0,001 | <0,001 |
| JumpingReach | xGA | −0,225 [−0,274; −0,176] | <0,001 | <0,001 |
| JumpingReach | Tore | +0,094 [+0,043; +0,144] | <0,001 | 0,006 |
| JumpingReach | Gegentore | −0,208 [−0,293; −0,123] | <0,001 | <0,001 |
| JumpingReach | Punkte | +0,184 [+0,102; +0,266] | <0,001 | <0,001 |
| Acceleration | xGD | +0,303 [+0,246; +0,361] | <0,001 | <0,001 |
| Acceleration | xGF | +0,101 [+0,073; +0,130] | <0,001 | <0,001 |
| Acceleration | xGA | −0,202 [−0,250; −0,154] | <0,001 | <0,001 |
| Acceleration | Tore | +0,100 [+0,048; +0,152] | <0,001 | 0,004 |
| Acceleration | Gegentore | −0,215 [−0,305; −0,126] | <0,001 | <0,001 |
| Acceleration | Punkte | +0,215 [+0,131; +0,299] | <0,001 | <0,001 |

Alle zwölf Kontraste bleiben nach Holm-Korrektur in der günstigen Richtung signifikant. Der mittlere xGD-Gewinn geht bei beiden Attributen stärker auf weniger gegnerisches xG als auf mehr eigenes xG zurück. Die Punktwerte beziehen sich auf ein einzelnes Match mit der Wertung 3/1/0.

## Vorregistrierte Kontextkontraste

Jede Zelle zeigt Δ xGD mit marginalem 95-%-KI und Holm-korrigiertem p. Die Einzelfaktoren sind 4-2-3-1 minus 4-3-3, offensiv minus defensiv und auswärts minus heim. Bei Mehrfaktor-Kontrasten gelten die vorregistrierten Produktgewichte.

| Kontextkontrast | JumpingReach − Acceleration | JumpingReach − Baseline | Acceleration − Baseline |
|---|---:|---:|---:|
| Formation | +0,012 [−0,105; +0,130] · 1,000 | −0,012 [−0,128; +0,105] · 1,000 | −0,024 [−0,139; +0,090] · 1,000 |
| Gegnerprofil | −0,008 [−0,125; +0,110] · 1,000 | +0,085 [−0,031; +0,202] · 1,000 | +0,093 [−0,022; +0,208] · 1,000 |
| Spielort | −0,047 [−0,164; +0,071] · 1,000 | +0,029 [−0,087; +0,146] · 1,000 | +0,076 [−0,039; +0,191] · 1,000 |
| Formation × Gegnerprofil | −0,015 [−0,133; +0,102] · 1,000 | +0,079 [−0,038; +0,195] · 1,000 | +0,094 [−0,021; +0,209] · 1,000 |
| Formation × Spielort | +0,051 [−0,067; +0,168] · 1,000 | −0,001 [−0,118; +0,115] · 1,000 | −0,052 [−0,166; +0,063] · 1,000 |
| Gegnerprofil × Spielort | −0,011 [−0,128; +0,107] · 1,000 | −0,061 [−0,178; +0,056] · 1,000 | −0,050 [−0,165; +0,065] · 1,000 |
| Formation × Gegnerprofil × Spielort | −0,020 [−0,137; +0,098] · 1,000 | −0,031 [−0,147; +0,086] · 1,000 | −0,011 [−0,126; +0,104] · 1,000 |

Keiner der 21 Kontexttests erreicht die Holm-Schwelle von 0,05. Die Intervalle lassen teils Unterschiede von mehr als 0,10 xGD zu. Die Präzision der gemittelten Rangschätzung überträgt sich daher nur begrenzt auf einzelne Kontexte.

## Deskriptive Zellschätzungen

Jede Zelle beruht auf 140 gepaarten Differenzen. Die Werte zeigen Δ xGD mit marginalem 95-%-KI. Die Vorregistrierung sieht für diese Zeilen keine separaten Hypothesentests vor.

| Formation | Gegnerprofil | Spielort | JumpingReach − Acceleration | JumpingReach − Baseline | Acceleration − Baseline |
|---|---|---|---:|---:|---:|
| 4-3-3 | Defensiv | Heim | +0,064 [−0,098; +0,226] | +0,297 [+0,148; +0,446] | +0,233 [+0,080; +0,385] |
| 4-3-3 | Defensiv | Auswärts | −0,042 [−0,199; +0,115] | +0,358 [+0,216; +0,499] | +0,399 [+0,255; +0,544] |
| 4-3-3 | Offensiv | Heim | +0,063 [−0,107; +0,233] | +0,334 [+0,162; +0,506] | +0,271 [+0,102; +0,439] |
| 4-3-3 | Offensiv | Auswärts | −0,026 [−0,192; +0,140] | +0,334 [+0,167; +0,501] | +0,359 [+0,211; +0,507] |
| 4-2-3-1 | Defensiv | Heim | +0,022 [−0,133; +0,176] | +0,177 [+0,025; +0,329] | +0,155 [−0,0003; +0,310] |
| 4-2-3-1 | Defensiv | Auswärts | +0,056 [−0,106; +0,218] | +0,297 [+0,138; +0,455] | +0,241 [+0,089; +0,392] |
| 4-2-3-1 | Offensiv | Heim | +0,029 [−0,135; +0,194] | +0,432 [+0,276; +0,589] | +0,403 [+0,231; +0,575] |
| 4-2-3-1 | Offensiv | Auswärts | +0,002 [−0,198; +0,203] | +0,369 [+0,149; +0,588] | +0,366 [+0,160; +0,573] |

Beide Baseline-Kontraste sind in allen acht Zellen positiv geschätzt. Alle acht Intervalle für den direkten Vergleich enthalten null. Die geprüfte Übertragbarkeit beschränkt sich auf das feste Lab-Fixture, die beiden Rollenaufstellungen, die Mentalitätswerte 2 und 6 und diesen Engine-Build. Der Standortkontrast schließt mögliche Effekte der festen nativen Fixture-Plätze ein.

## Reproduktion

```sh
python -m pip install numpy==2.3.5 scipy==1.16.3
python analysis/analyse_attr004.py
python -m unittest discover -s analysis -p test_attr004.py
```

Primärtest, alle 33 Sekundärtests und ihre Holm-Entscheidungen wurden zusätzlich unabhängig aus den exportierten Matchzeilen nachgerechnet. [Vollständige Effekte und p-Werte](../data/attr-004/effects.json) · [Analysecode](../analysis/analyse_attr004.py) · [Datenbeschreibung](../data/attr-004/README.md)

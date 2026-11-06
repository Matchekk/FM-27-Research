# ATTR-006 – Ergebnisse der Forward Jumping Reach Confirmation

**7. November 2026 · 300 vollständige Paare · FM27 27.0.0+2493426**

Sprunghöhe 12→16 für AMR, AML und ST verbesserte den xG-Saldo im getesteten Standardfixture um **+0,171 xGD pro Match**. Das 95-%-Intervall reicht von **+0,052 bis +0,290**, der zweiseitige gepaarte t-Test ergibt **p = 0,00498**. Damit ist der positive Effekt nach der Vorregistrierung bestätigt. Die untere Intervallgrenze liegt unter +0,10, sodass die praktische Schwelle offenbleibt.

## Durchführung und Prüfung

Die [Vorregistrierung](ATTR-006-vorregistrierung.md) und der Analysecode wurden vor dem ersten Match in `b9cb3e6` gepusht. Spielstartprotokoll, Engine, Adapter-Host, Fixture und Ressourcenfingerabdruck stimmten mit dem validierten Stand überein. Die binären SHA-256-Hashes beider Arme entsprechen den jeweiligen Setups in ATTR-005. Im nativen Readback belegten AMR, AML und ST die Kaderplätze 8, 9 und 10 (nullbasiert). Jeder gepaarte Readback in der Freigabeserie zeigte genau drei Attributänderungen an JumpingReach. Die Startelf, Rollen, Startprofile und vollständigen übrigen Attributvektoren entsprachen den jeweiligen Sollwerten. Vier Wiederholungspaare stimmten bei Endstand, Teamstatistik und Endtick exakt überein. Die separate Negativprobe endete mit Exitcode 108. [Technische Validierung](../data/attr-006/validation-summary.json)

Alle 600 Hauptmatches wurden akzeptiert. Die 300 neuen Seeds lieferten je eine Baseline und eine Intervention. Es gab keine fehlgeschlagenen Hauptversuche, Wiederholungen oder Ausschlüsse. Die neuen Seeds wurden gegen die früheren Matcharchive geprüft. [Manifest](../data/attr-006/manifest.json) · [Matchmessungen](../data/attr-006/matches.jsonl)

## Primärer Effekt und Sensitivität

| Kontrast | Paare | Δ xGD pro Match | Gepaarte SD | 95-%-t-Intervall | p |
|---|---:|---:|---:|---:|---:|
| Sprunghöhe im Angriff − Baseline | 300 | +0,171 | 1,049 | +0,052 bis +0,290 | 0,00498 |

Das gepaarte Bootstrap-Intervall reicht von +0,055 bis +0,292. Beim Weglassen jeweils eines Seed-Paars lagen die Mittelwerte zwischen +0,160 und +0,183, die p-Werte zwischen 0,00225 und 0,00781 und die unteren Intervallgrenzen zwischen +0,042 und +0,066. Alle 300 Sensitivitätsläufe führten zur selben Entscheidung für den positiven Effekt und für die praktische Schwelle.

ATTR-005 schätzte denselben Kontrast explorativ auf +0,232 xGD (95-%-KI +0,073 bis +0,392, 100 Paare). Die Bestätigungsschätzung liegt um 0,061 xGD darunter und zeigt dieselbe Richtung. Der Vergleich der Schätzungen ist deskriptiv. Der Primärtest verwendet ausschließlich die neuen ATTR-006-Paare. [ATTR-005-Screening](ATTR-005-ergebnisse.md)

## Explorative Sekundärmetriken

| Endpunkt | Mittlere Änderung pro Match | Marginales 95-%-KI | Holm-p |
|---|---:|---:|---:|
| xGF | +0,076 | +0,018 bis +0,134 | 0,0545 |
| xGA | −0,096 | −0,192 bis +0,0002 | 0,2021 |
| Tore | +0,080 | −0,025 bis +0,185 | 0,4018 |
| Gegentore | −0,127 | −0,293 bis +0,039 | 0,4018 |
| Punkte (3/1/0) | +0,107 | −0,064 bis +0,278 | 0,4018 |

Keiner der fünf Sekundärtests erreichte die Holm-Schwelle. Die Schlussfolgerung gilt für die gemeinsame Attributanhebung bei diesen drei Spielern im getesteten Rollen- und Mannschaftssetup auf diesem Build.

## Reproduktion

```sh
python -m pip install numpy==2.3.5 scipy==1.16.3
python analysis/analyse_attr006.py
```

Alle sechs Tests und die 300 Auswertungen mit je einem weggelassenen Paar wurden unabhängig aus den exportierten Matchzeilen nachgerechnet. Beim ersten JSON-Export musste der NumPy-Entscheidungswert in einen nativen Python-Wert umgewandelt werden (`a9a9113`). Die gepushten Analysefassungen liefern nach dieser Typkonvertierung identische Zahlen und Entscheidungen. Der native Laufstand ist in `3bca400` dokumentiert. [Effektarchiv](../data/attr-006/effects.json) · [Analysecode](../analysis/analyse_attr006.py)

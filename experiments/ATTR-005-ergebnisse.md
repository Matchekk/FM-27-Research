# ATTR-005 – Ergebnisse des Positionsscreenings

**6. November 2026 · Explorativ · FM27 27.0.0+2493426 · 900 Hauptmatches**

Der Angriff lieferte für beide Attribute die größten geschätzten xGD-Gewinne gegenüber Baseline. Sprunghöhe lag bei **+0,232 xGD pro Match** (marginales 95-%-KI +0,073 bis +0,392, Holm-p = 0,058), Antritt bei **+0,166** (−0,007 bis +0,338, Holm-p = 0,652). Die zwölf primären Tests blieben oberhalb der Holm-Schwelle von 0,05. Damit ist der Angriff ein Kandidat für eine unabhängige Prüfung.

## Durchführung und Qualität

Die [Vorregistrierung](ATTR-005-position-screening.md) und der Analysecode wurden vor dem ersten Match in `41460cc` gepusht. Spielstartprotokoll, Engine, Adapter-Host, Fixture und Ressourcenfingerabdruck stimmten mit dem validierten Stand überein. Das Testteam spielte im 4-3-3 zu Hause gegen das 4-2-3-1 mit Mentalität 4 auf beiden Seiten. Die Standardkader enthielten 23 bzw. 26 aktive Spieler.

Die vier Baseline-Prüfläufe bestätigten dieselbe native Startelf. Die Zuordnung aus nativer Ballbesitzposition und lokalem Identitätsabgleich ergab folgende Startelf- und Kaderplätze, jeweils ab null.

| Gruppe | Native Ballbesitzpositionen und Kaderplätze |
|---|---|
| Innenverteidiger | DCR 2, DCL 3 |
| Außenverteidiger | DR 1, DL 4 |
| Zentrales Mittelfeld | DMC 5, MCR 6, MCL 7 |
| Angriff | AMR 8, AML 9, ST 10 |

Alle 36 Prüfmatches wurden akzeptiert. Je Interventionsarm änderte sich ausschließlich das deklarierte Attribut an den nativ zugeordneten Kaderplätzen. Der vollständige Readback prüfte die Attributvektoren, Rollen, Startprofile und Mentalitäten. Alle 18 Wiederholungspaare lieferten identischen Endstand, identische Teamstatistik und denselben Endtick. Die getrennte Negativprobe wurde mit Exitcode 108 abgewiesen. [Validierungsbericht](../data/attr-005/validation-summary.json)

Die 100 disjunkten Hauptseeds lieferten je neun vollständige Arme. Es gab keine Fehlversuche, Wiederholungen oder Ausschlüsse im Hauptlauf. Die Analyse bildet alle Differenzen innerhalb desselben Seeds. [Manifest](../data/attr-005/manifest.json) · [Hauptmessungen](../data/attr-005/matches.jsonl)

## Primäre xGD-Kontraste

| Gruppe | Kontrast | Δ xGD | 95-%-KI | 95-%-Bootstrap-KI | Varianz | Holm-p |
|---|---|---:|---:|---:|---:|---:|
| Innenverteidiger | Sprunghöhe − Baseline | +0,129 | −0,048 bis +0,307 | −0,044 bis +0,306 | 0,801 | 1,000 |
| Innenverteidiger | Antritt − Baseline | +0,123 | −0,071 bis +0,317 | −0,066 bis +0,315 | 0,956 | 1,000 |
| Innenverteidiger | Sprunghöhe − Antritt | +0,007 | −0,174 bis +0,187 | −0,171 bis +0,186 | 0,829 | 1,000 |
| Außenverteidiger | Sprunghöhe − Baseline | +0,028 | −0,161 bis +0,216 | −0,158 bis +0,216 | 0,904 | 1,000 |
| Außenverteidiger | Antritt − Baseline | +0,084 | −0,090 bis +0,258 | −0,086 bis +0,255 | 0,767 | 1,000 |
| Außenverteidiger | Sprunghöhe − Antritt | −0,056 | −0,240 bis +0,128 | −0,236 bis +0,127 | 0,858 | 1,000 |
| Zentrales Mittelfeld | Sprunghöhe − Baseline | +0,127 | −0,052 bis +0,307 | −0,048 bis +0,305 | 0,822 | 1,000 |
| Zentrales Mittelfeld | Antritt − Baseline | +0,043 | −0,125 bis +0,210 | −0,122 bis +0,209 | 0,714 | 1,000 |
| Zentrales Mittelfeld | Sprunghöhe − Antritt | +0,085 | −0,083 bis +0,253 | −0,076 bis +0,253 | 0,716 | 1,000 |
| Angriff | Sprunghöhe − Baseline | +0,232 | +0,073 bis +0,392 | +0,076 bis +0,389 | 0,650 | 0,058 |
| Angriff | Antritt − Baseline | +0,166 | −0,007 bis +0,338 | −0,004 bis +0,333 | 0,754 | 0,652 |
| Angriff | Sprunghöhe − Antritt | +0,067 | −0,134 bis +0,267 | −0,129 bis +0,264 | 1,019 | 1,000 |

Die Punktschätzungen gegen Baseline waren in allen acht Armen positiv. Im direkten Vergleich reichten die Schätzungen von −0,056 bei den Außenverteidigern bis +0,085 im zentralen Mittelfeld. Alle vier direkten Intervalle schließen null ein und lassen praktisch relevante Differenzen zu. Die Punktreihenfolge bleibt explorativ. Angreifer und zentrales Mittelfeld umfassen drei behandelte Spieler, die beiden Verteidigergruppen jeweils zwei. Spielerprofile und Rollen unterscheiden sich ebenfalls. Die Effekte beziehen sich auf den jeweiligen Eingriff im getesteten Fixture.

## Sekundäre Endpunkte und Interaktionen

Keiner der 66 Sekundärtests unterschritt die Holm-Schwelle. Deskriptiv entfielen bei Sprunghöhe im Angriff +0,112 auf eigenes xG und −0,120 auf gegnerisches xG. Die Schätzungen für Tore, Gegentore und Punkte in diesem Arm waren +0,120, −0,190 und +0,160 pro Match. Die vollständigen sekundären Kontraste und Intervalle stehen im [Effektarchiv](../data/attr-005/effects.json).

Die folgenden Differenzen von Differenzen prüfen, ob sich der direkte Attributkontrast zwischen zwei Gruppen ändert. Die Stichprobenvarianz beruht auf der Differenz der beiden Kontraste innerhalb desselben Seeds.

| Gruppenunterschied der direkten Kontraste | Δ xGD | 95-%-KI | Varianz | Holm-p |
|---|---:|---:|---:|---:|
| Innenverteidiger − Außenverteidiger | +0,063 | −0,199 bis +0,324 | 1,738 | 1,000 |
| Innenverteidiger − Zentrales Mittelfeld | −0,078 | −0,325 bis +0,169 | 1,546 | 1,000 |
| Innenverteidiger − Angriff | −0,060 | −0,331 bis +0,211 | 1,860 | 1,000 |
| Außenverteidiger − Zentrales Mittelfeld | −0,141 | −0,387 bis +0,105 | 1,536 | 1,000 |
| Außenverteidiger − Angriff | −0,123 | −0,392 bis +0,147 | 1,844 | 1,000 |
| Zentrales Mittelfeld − Angriff | +0,018 | −0,243 bis +0,279 | 1,732 | 1,000 |

## Fallzahlen für eine unabhängige Bestätigung

Jede Fallzahl ist die Zahl vollständiger **neuer Seed-Blöcke** bei 80 % Power. Die erste Zahl nutzt die gemessene gepaarte SD. Die zweite nutzt deren einseitige 95-%-Obergrenze unter Normalitätsannahme. Die Planung setzt einen wahren Unterschied von 0,10 bzw. 0,15 xGD an. Das α von 0,0125 ist ein konservatives Szenario für bis zu vier zweiseitige Tests.

| Gruppe | Kontrast | SD | 0,10 xGD, α 0,05 | 0,15 xGD, α 0,05 | 0,15 xGD, α 0,0125 |
|---|---|---:|---:|---:|---:|
| Innenverteidiger | Sprunghöhe − Baseline | 0,895 | 631 / 810 | 282 / 361 | 400 / 514 |
| Innenverteidiger | Antritt − Baseline | 0,978 | 753 / 966 | 336 / 431 | 477 / 612 |
| Innenverteidiger | Sprunghöhe − Antritt | 0,911 | 653 / 839 | 292 / 374 | 415 / 532 |
| Außenverteidiger | Sprunghöhe − Baseline | 0,951 | 712 / 914 | 318 / 408 | 452 / 580 |
| Außenverteidiger | Antritt − Baseline | 0,876 | 604 / 776 | 270 / 346 | 384 / 492 |
| Außenverteidiger | Sprunghöhe − Antritt | 0,926 | 676 / 868 | 302 / 387 | 429 / 550 |
| Zentrales Mittelfeld | Sprunghöhe − Baseline | 0,906 | 647 / 831 | 289 / 371 | 411 / 527 |
| Zentrales Mittelfeld | Antritt − Baseline | 0,845 | 563 / 723 | 252 / 323 | 358 / 458 |
| Zentrales Mittelfeld | Sprunghöhe − Antritt | 0,846 | 564 / 724 | 252 / 323 | 358 / 459 |
| Angriff | Sprunghöhe − Baseline | 0,806 | 513 / 658 | 229 / 294 | 326 / 417 |
| Angriff | Antritt − Baseline | 0,869 | 595 / 763 | 266 / 341 | 378 / 484 |
| Angriff | Sprunghöhe − Antritt | 1,009 | 802 / 1030 | 358 / 459 | 509 / 652 |

Für eine Interaktion von 0,15 xGD erfordert ein einzelner Test bei α = 0,05 und 80 % Power je nach Gruppenpaar 538 bis 651 Seeds. Mit oberer SD-Grenze sind es 691 bis 836. Das Effektarchiv enthält zusätzlich 90-%-Power und das Szenario 0,20 xGD für alle 18 xGD-Kontraste. Die tatsächliche Fallzahl hängt vom vorab gewählten Kontrast, dem Zielunterschied und der Testfamilie ab. Der Bestätigungslauf bleibt ein eigener Forschungsauftrag mit neuen Seeds und eingefrorenem Analyseplan.

## Reproduktion

```sh
python -m pip install numpy==2.3.5 scipy==1.16.3
python analysis/analyse_attr005.py
```

Alle 78 Tests einschließlich Holm-Korrektur und die 432 Mindestfallzahlen wurden unabhängig aus den exportierten Messzeilen nachgerechnet. [Analysecode](../analysis/analyse_attr005.py) · [Datenbeschreibung](../data/attr-005/README.md)

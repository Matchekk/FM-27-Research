# ATTR-006 – Forward Jumping Reach Confirmation

**Vorregistrierung · 7. November 2026 · Konfirmatorische Hauptserie**

ATTR-005 schätzte für Sprunghöhe im Angriff +0,232 xGD pro Match (95-%-KI +0,073 bis +0,392, Holm-p = 0,058). ATTR-006 prüft denselben Kontrast unabhängig an neuen Seeds. Die Hypothese ist ein positiver mittlerer Effekt auf xGD.

## Fixture, Arme und Stichprobe

- Unveränderte standardisierte Baseline aus ATTR-005. Das Testteam spielt zu Hause im 4-3-3 gegen ein 4-2-3-1, beide gegen den Ball im 4-4-2, Mentalität 4 und 4, aktive Kader 23 und 26. Die kontrollierten Startprofile und alle weiteren Fixture-Einstellungen entsprechen ATTR-005.
- Intervention wie `FW-JumpingReach` in ATTR-005. Ausschließlich JumpingReach für die drei nativ zugeordneten Startspieler auf AMR, AML und ST steigt von Rohwert 60 auf 80 (Anzeige 12→16). Startelf, Rollen, Kader und sonstige Eingaben sind identisch. Beide vollständigen binären Setup-Hashes müssen mit dem [ATTR-005-Manifest](../data/attr-005/manifest.json) übereinstimmen.
- 300 neue gepaarte Seeds, insgesamt 600 vollständige Hauptmatches. Die ersten vier SHA-256-Bytes von `ATTR-006/{validation|main}/{Zähler}` ergeben einen Little-Endian-uint32. Je Phase startet der Zähler bei null. Übersprungen werden null, alle bereits vergebenen Seeds und die archivierten Matchseeds einschließlich technischer und historischer Serien bis ATTR-005. Die zwei technischen Seeds gehören zur separaten Validierungsphase.
- 300 Paare liefern bei der ATTR-005-SD von 0,806 und einem wahren Unterschied von 0,15 xGD eine geplante Power von rund 89 % für den zweiseitigen Nulltest. Die obere SD-Schätzung aus ATTR-005 erforderte 294 Paare für 80 % Power. Die Rechnung betrifft den Nachweis eines Unterschieds zu null. Die praktische Entscheidung verwendet zusätzlich die Intervallgrenze.

## Technische Freigabe und Vollständigkeit

- Vor dem ersten Match müssen diese Vorregistrierung und der Analysecode auf `main` liegen. Versionsmeldung `27.0.0+2493426`, Engine- und Host-SHA-256, Adapterprofil, Fixture, Matchressourcen und Lab-Quellhashes müssen mit dem validierten Stand übereinstimmen. Bei inkompatiblem Build oder abweichender Identität bleibt der Matchstart gesperrt.
- Zuerst vier Baseline-Prüfmatches (zwei Seeds mit je zwei Wiederholungen), dann vier Interventionsprüfmatches mit denselben Prüfseeds. Der native Readback bestätigt alle aktiven Attributvektoren, die drei tatsächlichen Angriffspositionen, Startelf, Rollen, Mentalitäten und kontrollierten Startprofile. Der binäre Vergleich und der gepaarte native Attributvergleich müssen genau die drei Änderungen zeigen. Wiederholungen je Arm und Prüfseed müssen bei Endstand, Teamstatistik und Endtick exakt übereinstimmen. Eine getrennte ungültige Binärkonfiguration muss mit Exitcode 108 scheitern.
- Im Hauptlauf werden pro Seed beide Arme mit wirksamem Seed-Override und vollständigem Readback ausgeführt. Lab-Quick-Modus, bis zu vier Worker, 90 Sekunden ohne Fortschritt als Timeout. Ein Match zählt bei Start 0:0, natürlichem Abschluss vor dem Watchdog, plausibler vollständiger Teamstatistik, gültigem Endstand und stimmigen Identitäts-, Eingabe- und Laufbelegen.
- Höchstens eine Wiederholung mit identischem Seed und Setup nach einem transienten Workerfehler. Alle Fehlversuche werden protokolliert. Abweichungen bei Identität, Eingabe oder Ergebnisaudit sperren die Serie. Keine Ersatzseeds, stillen Ausschlüsse, Zwischenanalyse oder optionales Stoppen. Bei dauerhaft unvollständigem Datensatz wird nur der technische Stand ausgewiesen. Die Hauptauswertung setzt alle 300 vollständigen Paare voraus.

## Primärer Test und Entscheidungen

Je Seed ist `ΔxGD = (xGF − xGA)Intervention − (xGF − xGA)Baseline` aus Sicht des Testteams. Die primäre Nullhypothese lautet mittlere Differenz gleich null. Der zweiseitige gepaarte t-Test prüft bei α = 0,05. Berichtet werden Mittelwert, Stichproben-SD und zweiseitiges 95-%-t-Intervall. Ein positiver Effekt gilt als bestätigt, wenn p < 0,05 und die untere Intervallgrenze über null liegt. Praktische Relevanz über +0,10 xGD wird nur bei einer unteren Intervallgrenze über +0,10 behauptet.

Die Sensitivitätsanalyse resampelt ganze Paare in 20.000 deterministischen Bootstrap-Replikaten und berechnet ein 95-%-Perzentilintervall. Für jeden Seed wird der Primärtest einmal ohne dieses Paar neu berechnet. Berichtet werden die Spannweiten der Mittelwerte, p-Werte und unteren Intervallgrenzen sowie die Anzahl veränderter Entscheidungen. Alle 300 Paare verbleiben im Primärtest.

Sekundär und explorativ werden xGF, xGA, erzielte Tore, Gegentore und Punkte (3/1/0) mit gepaarten t-Tests, marginalen 95-%-t-Intervallen und einer Holm-Korrektur über fünf Tests ausgewertet. ATTR-005 dient als separater deskriptiver Vergleich. Sein Effekt und sein Intervall werden neben ATTR-006 berichtet. Screening- und Validierungsseeds gehen nicht in den Primärtest ein.

[Analysecode](../analysis/analyse_attr006.py). Bericht, erlaubte JSONL-Matchmessungen, Manifest und Analysewerte werden unter `experiments/` und `data/attr-006/` archiviert. Die Schlussfolgerung gilt für den Eingriff an diesen drei Spielern im getesteten Fixture und Build.

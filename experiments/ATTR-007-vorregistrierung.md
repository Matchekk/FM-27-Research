# ATTR-007 – Individual Forward Position Sensitivity

**Vorregistrierung · 7. November 2026 · Exploratives 2³-Design**

[ATTR-006](ATTR-006-ergebnisse.md) bestätigte den positiven xGD-Effekt einer gleichzeitigen JumpingReach-Aufwertung bei AMR, AML und ST. ATTR-007 untersucht, welchen Beitrag jede Position in diesem Fixture leistet und wie sich die Aufwertungen gegenseitig beeinflussen.

## Fixture, Arme und Stichprobe

Identisches validiertes 4-3-3-Standardfixture wie ATTR-006, zu Hause gegen das 4-2-3-1. Beide Mannschaften nutzen gegen den Ball 4-4-2 und Mentalität 4. Die aktiven Kader umfassen 23 und 26 Spieler. Die binären Baseline- und ALL-Hashes müssen exakt [ATTR-006](../data/attr-006/manifest.json) entsprechen. Die nativen Zielpositionen sind AMR, AML und ST. Der jeweilige Spieler erhält JumpingReach Rohwert 60→80 (Anzeige 12→16). Startelf, Rollen, Startprofile, übrige Attribute, Gegner und Anweisungen bleiben gleich.

| Arm | AMR | AML | ST |
|---|---:|---:|---:|
| Baseline | 0 | 0 | 0 |
| AMR | 1 | 0 | 0 |
| AML | 0 | 1 | 0 |
| ST | 0 | 0 | 1 |
| AMR+AML | 1 | 1 | 0 |
| AMR+ST | 1 | 0 | 1 |
| AML+ST | 0 | 1 | 1 |
| ALL | 1 | 1 | 1 |

200 neue disjunkte Seeds, jeder in allen acht Armen, ergeben 1.600 Hauptmatches. Die ersten vier SHA-256-Bytes von `ATTR-007/{validation|main}/{Zähler}` ergeben einen Little-Endian-uint32. Je Phase startet der Zähler bei null. Null, bereits zugeteilte Seeds und alle archivierten Haupt-, Prüf- und historischen Matchseeds bis ATTR-006 werden übersprungen. Zwei separate Seeds dienen der technischen Prüfung. Die Job-Reihenfolge ist innerhalb einer Serie durch gehashte Schlüssel festgelegt.

## Technische Freigabe

- Vor jeglicher Simulation liegen diese Vorregistrierung und der [eingefrorene Analysecode](../analysis/analyse_attr007.py) auf `main`. Tatsächlicher Spielbuild `27.0.0+2493426`, Engine- und Adapter-Host-SHA-256, Adapterprofil, Fixture, Matchressourcen und Lab-Quellhashes müssen mit dem validierten Stand übereinstimmen. Ein inkompatibler Build oder eine Identitätsabweichung sperrt die Ausführung.
- Zuerst vier Baseline-Prüfmatches (zwei Seeds, je zwei Wiederholungen). Die native Positions- und Startelfzuordnung muss mit ATTR-006 übereinstimmen. Danach folgen 28 Prüfmatches der übrigen Arme. Der binäre Vergleich jedes Arms gegen Baseline darf ausschließlich die vorgesehenen Attributwerte ändern. Für beide Mannschaften werden alle aktiven Attributvektoren nativ ausgelesen. Paarweise Readbacks müssen genau die deklarierten Änderungen zeigen. Mannschaftsanweisungen, Rollen und Startprofile werden über den nativen Eingabe-Readback geprüft. Die nativ gemeldeten Phasenkonfigurationen müssen innerhalb jedes Prüfblocks übereinstimmen. Endstand, Teamstatistik und Endtick müssen je Seed und Arm exakt wiederholbar sein. Eine getrennte ungültige Binärkonfiguration muss mit Exitcode 108 scheitern.
- Jeder Hauptlauf erfordert wirksamen Seed-Override, Start 0:0, natürlichen Abschluss vor dem Watchdog, vollständige plausible Teamstatistik, gültigen Endstand, vollständigen nativen Attribut-Readback und stimmige Versions- und Eingabebelege. Lab-Quick-Modus, maximal vier Worker, 90 Sekunden ohne Fortschritt als Timeout.
- Höchstens eine Wiederholung desselben Seeds und Setups nach transientem Workerfehler. Alle Fehlversuche mit Grund und Belegen aufbewahren. Abweichungen der Identität, Eingabe oder Ergebnisaudits sperren die Serie. Keine Ersatzseeds, stillen Ausschlüsse, Zwischenanalyse oder optionales Stoppen. Bei dauerhaft fehlenden Armen wird nur der technische Stand publiziert. Die geplante Auswertung setzt alle 200 vollständigen Achtarmblöcke voraus.

## Kontraste und Testfamilien

Die Zielgröße ist `xGD = xGF − xGA` aus Heimsicht. Für jeden Seed sei `v(S)` die Zielgröße unter der Aufwertung der Teilmenge `S` der drei Positionen. Alle Differenzen entstehen innerhalb desselben Seed-Blocks.

- **Primäre explorative Familie (7 Tests).** Drei isolierte Effekte `v({i}) − v(∅)`. Drei Shapley-Beiträge als Summe der marginalen Differenzen `v(S∪{i}) − v(S)`, gewichtet mit `|S|!(2−|S|)!/3!` je Teilmenge ohne Position `i`. Das entspricht Gewicht 1/3 für die leere und volle Vergleichsmenge sowie 1/6 für jede der beiden einelementigen Mengen. Der siebte Test ist `Shapley(ST) − (Shapley(AMR) + Shapley(AML))/2`.
- **Effizienzprüfung.** Die Summe der Shapley-Koeffizienten muss exakt `ALL − Baseline` ergeben. Zusätzlich prüfen wir diese Identität für jeden Seed mit exakter rationaler Arithmetik auf den eingelesenen xGD-Werten. Die Summe in Gleitkommaarithmetik wird separat mit absoluter Toleranz 10⁻¹² geprüft. Der Gesamteffekt wird mit Intervall deskriptiv berichtet.
- **Faktorielle xGD-Familie (7 Tests).** Drei Haupteffekte sind die gleichgewichteten mittleren marginalen Änderungen über alle vier Kontexte der anderen zwei Faktoren. Jede Zweifachinteraktion ist die Differenz der beiden marginalen Änderungen eines Faktors bei Aus- bzw. Einschalten des anderen, gleichgewichtet über die zwei Stufen des dritten Faktors. Die Dreifachinteraktion ist die Zweifachinteraktion bei ein- minus ausgeschaltetem drittem Faktor. Alle Interaktionen stehen in xGD-Einheiten ohne weitere Skalierung.
- **Weitere explorative Endpunkte (70 Tests).** Für xGF, xGA, Tore, Gegentore und Punkte (3/1/0) werden dieselben 14 Kontraste geschätzt. Gemeinsam bilden sie eine sekundäre Testfamilie.

Berichtet werden gepaarter Mittelwert, Stichprobenvarianz, SD, marginales 95-%-t-Intervall und zweiseitiges p des gepaarten t-Tests. Ein gemeinsamer deterministischer Bootstrap mit 20.000 Resamples vollständiger Seed-Blöcke liefert marginale 95-%-Perzentilintervalle. Die Holm-Korrektur bei 0,05 läuft getrennt über die Familien mit 7, 7 und 70 Tests. Die Intervalle sind marginal. Als praktische Orientierung dienen 0,10 xGD. Die Ergebnisse beziehen sich auf konkrete Spieler und Rollen in diesem Fixture und sind explorativ.

## Bestätigungsplanung

Für die 14 xGD-Kontraste werden die benötigten vollständigen neuen Seed-Blöcke per nichtzentraler t-Verteilung berechnet. Szenarien verwenden Zielunterschiede von 0,10 und 0,15 xGD, 80 % oder 90 % Power und zweiseitiges α = 0,05 oder konservativ 0,05/7. Die Rechnungen verwenden die beobachtete gepaarte SD und als Sensitivität deren einseitige 95-%-Obergrenze unter Normalitätsannahme. Die Wahl eines Kandidaten und seiner Fallzahl erfordert einen eigenen vorab fixierten Plan. Frühere Experimente dienen als Kontext.

Bericht, Manifest, technische Belege, zulässige JSONL-Messungen und Effekte erscheinen unter `experiments/` und `data/attr-007/`. Vollständige native Dumps und Originalspielmaterial verbleiben lokal.

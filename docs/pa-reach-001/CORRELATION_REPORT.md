# Welche Ausgangsmerkmale mit kurzfristigem CA-Wachstum zusammenhängen

### Persönlichkeit am Ausgangstag

Für **60.548** der 60.550 identitätsgesicherten Feldspieler stimmen am 31.01. zusätzlich Professionalität, Ehrgeiz, Zielstrebigkeit, Natural Fitness und Verletzungsanfälligkeit zwischen Save und eigenständigem Scout-Readback überein. Bei zwei Spielern fehlt die eindeutige zusätzliche Scanzuordnung. Die native Spieluhr vor und nach dem Scanner bestätigt den 31.01., der Scanheader nennt fälschlich den 30.01. Die folgende Auswertung verwendet nur die Januarwerte als Prädiktoren und die tatsächliche CA-Differenz bis 30.03.2027 als Ziel. [Vorab festgelegte Zusatzanalyse](../../research/pa-reach-001/manifests/personality-plan.json)

| Ausgangsmerkmal | Pearson / Spearman mit ΔCA | Adjustierte CA-Differenz je Skalenpunkt, alle | Separates Modell in verifizierten Baseline-Klubs, 95-%-Intervall |
|---|---:|---:|---:|
| Professionalität, mit 20 Jahren | 0,075 / 0,067 | +0,056 | +0,058 [0,044 bis 0,071] |
| Ehrgeiz | 0,050 / 0,042 | +0,030 | +0,033 [0,023 bis 0,042] |
| Zielstrebigkeit | 0,077 / 0,078 | +0,022 | +0,026 [0,021 bis 0,030] |
| Natural Fitness | 0,019 / 0,022 | +0,004 | +0,005 [−0,001 bis 0,011] |
| Verletzungsanfälligkeit | −0,012 / −0,011 | +0,002 | +0,005 [−0,0004 bis 0,010] |

Korrelationen beziehen sich jeweils auf alle eingeschlossenen Altersgruppen. Beide linearen Modelle berücksichtigen Alter, Start-CA, Abstand zur PA, Position, die fünf Ausgangsattribute, Alter × Abstand sowie Alter × Professionalität. Im Modell für alle Spieler entspricht bei Alter 20 ein Unterschied von fünf Professionalitätspunkten rund **0,28 CA mehr in 58 Tagen**. Der geschätzte Zusammenhang pro Professionalitätspunkt fällt je zusätzlichem Altersjahr um 0,011 CA. Die beobachtete Altersinteraktion kann unter anderem von Spielpraxis und Auswahl beeinflusst sein. Sie ist kein Engine-Grenzwert. Bei zusätzlicher Kontrolle der beobachteten Bytekategorie und Byte × Abstand beträgt der Professionalitätskoeffizient bei Alter 20 noch +0,045 CA (60.088 Spieler). Die Modellierung einer möglichen Vermittlervariable verändert die Interpretation.

Die 95-%-Intervalle entstammen dem getrennten Modell mit 24.543 Spielern in 1.420 bestätigten Baseline-Klubs, bedingt auf diese Karriere. Im Beleg stehen punktweise Intervalle und über sämtliche Nicht-Intercept-Terme des Modells Holm-korrigierte Tests. Kein zwischen Karrieren gültiges Intervall und kein Kausaleffekt einer Persönlichkeitsänderung wurden geschätzt. [Vollständige Koeffizienten und Missing](../../research/pa-reach-001/manifests/personality-growth.json) · [Auswertung](../../research/pa-reach-001/analysis/personality_growth.py)

### Alter und verbleibende PA-Lücke

**In Zubieta hing der CA-Zuwachs über 58 Tage am stärksten mit Alter und verbleibendem PA-Abstand unter den vier untersuchten Ausgangsgrößen zusammen.** Der Zusammenhang blieb nach Kontrolle der jeweils anderen Größe, der Ausgangs-CA und der Position bestehen. CA, PA und Identität sind im Januar und März jeweils am Save und im Spiel unabhängig abgeglichen. Die historische 19-Tage-Auswertung stammt von einem anderen Build. Die zwei Zeitfenster können denselben Karriereursprung teilen. Es liegen null vollständige Spieler-Saisons und kein unabhängiges Testuniversum vor. [Zubieta-Beleg](../../research/pa-reach-001/manifests/zubieta-associations.json) · [TRAIN005-Beleg](../../research/pa-reach-001/manifests/train005-associations.json)

| Ausgangsmerkmal gegen ΔCA | Zubieta 58 Tage · Pearson / Spearman | TRAIN005 19 Tage · Pearson / Spearman |
|---|---:|---:|
| Alter | −0,413 / −0,445 | −0,249 / −0,267 |
| PA−CA | +0,402 / +0,415 | +0,252 / +0,256 |
| CA | −0,024 / −0,026 | −0,024 / −0,025 |
| PA | +0,177 / +0,203 | +0,094 / +0,112 |
| Kandidatenbyte als Rang 1–5 | keine semantisch validierte Exposition | +0,147 / +0,162 |

Zubieta umfasst 60.550 unterschiedliche, an beiden Spieltagen nativ bestätigte und an beiden Tagen identitätsgleiche U28-Feldspieler. TRAIN005 umfasst 59.704 gepaarte U28-Feldspieler. Für die Byte-Analysen sind dort 59.681 Spieler mit einem Baselinewert 1–5 verwertbar. Die übrigen 23 bleiben unbestimmt. Das Byte bezeichnet in dieser Zusatzanalyse den beobachteten Dateiwert. Seine Wirkung als manipulierbare Entwicklungsstufe ist ungeprüft. Die Ergebnisse sind explorativ.

### Bedingte Zusammenhänge

Nach linearer Bereinigung um Ausgangs-CA, Position und jeweils das andere Merkmal ergeben sich in Zubieta partielle Pearson-Korrelationen von −0,276 für Alter und +0,226 für die PA-Lücke. Bei TRAIN005 sind es −0,149 und +0,142. Schon dort korrelieren Alter und Lücke miteinander (Pearson −0,533). Die Programme geben die Zusammenhänge innerhalb jeder besetzten Positions- und Altersgruppe aus. Beispielsweise beträgt die Korrelation Lücke/ΔCA bei Innenverteidigern im historischen Zeitfenster +0,253 (n=10.517), bei Mittelstürmern +0,251 (n=9.305).

Für Zubieta enthält die lineare Regression Position, Ausgangs-CA, Alter, Lücke und Alter × Lücke. Alter ist um 20 Jahre, die Lücke um 20 CA-Punkte zentriert. Bei gleicher Position und CA gilt für einen 20-Jährigen: Eine um zehn Punkte größere Lücke ist mit durchschnittlich **+0,226** zusätzlichen CA in den 58 Tagen verbunden. Bei Lücke 20 ist ein weiteres Lebensjahr mit **−0,137** CA verbunden. Je weiterem Lebensjahr sinkt der Lückenkoeffizient je zehn Punkte um **0,034**. CA, PA und Lücke gleichzeitig aufzunehmen würde zu perfekter Kollinearität führen. Person, Kalender und Trainingsbedingungen wurden hier nicht zufällig zugeteilt.

| Zubieta, Basisverein separat nativ bestätigt | Koeffizient in CA je 58 Tage | Punktweises 95-%-Intervall innerhalb des Karriereuniversums |
|---|---:|---:|
| +1 Jahr bei Lücke 20 | −0,161 | [−0,171, −0,151] |
| +10 Lückenpunkte bei Alter 20 | +0,237 | [+0,216, +0,258] |
| Alter × Lücke je zehn Punkte | −0,047 | [−0,053, −0,040] |
| +10 Ausgangs-CA bei gleicher Lücke | +0,058 | [+0,047, +0,069] |

Die Club-Auswertung umfasst 24.543 Spieler in 1.420 unabhängig abgeglichenen Ausgangsvereinen. Bei 36.007 Spielern fehlt diese Bestätigung. Die Club-Intervalle und Punktschätzungen in dieser Tabelle beziehen sich daher auf eine ausgewählte Teilgruppe. Die 95-%-Intervalle für die Koeffizienten nutzen einen nach Ausgangsverein gruppierten CR1-Sandwich-Schätzer mit t-Verteilung und G−1 Freiheitsgraden. Für die Korrelationen wurden ganze Vereine 999-mal mit Zurücklegen gezogen und die mittleren Ränge in jeder Ziehung neu berechnet. So liegt im Club-Teilsample die Pearson-Korrelation für Alter bei −0,440 [−0,455, −0,424] und für die PA-Lücke bei +0,432 [+0,416, +0,448]. Diese Intervalle konditionieren auf diese Karriere, das beobachtete Zeitfenster und eine als korrekt vorausgesetzte Messung. Messfehler am ersten Stichtag können den Zusammenhang von Ausgangslücke und ΔCA beeinflussen, weil beide dieselbe Ausgangs-CA enthalten.

Im historischen Arm ergeben sich bei einem 20-Jährigen mit Byte 3 pro zehn zusätzliche Lückenpunkte +0,108 CA in 19 Tagen (n=59.681). Bei Lücke 20 unterscheidet sich Byte 5 von Byte 3 adjustiert um +0,133 CA. Im Teilsample mit beidseitig bestätigtem Baseline-Verein und verwertbarem Byte (24.378 Spieler in 1.365 Vereinen) beträgt letzterer Kontrast +0,134 [0,097, 0,172]. Die übrigen Baseline-Vereine fehlen bei 35.308 der 59.704 Spieler. Die Stichprobenselektion kann die Ergebnisse verändern. Es gibt keine native Intervention am Byte.

### Nichtlinearität, Unsicherheit und Reproduktion

Eine ergänzende stückweise lineare Zubieta-Anpassung an den bereits verwendeten Altersgrenzen 18, 21 und 24 erklärt im beobachteten Datensatz 0,258 der ΔCA-Varianz, das einfachere lineare Modell 0,240. Die Form hängt von den gesetzten Knoten und vom untersuchten Altersbereich ab. Eine natürliche Engine-Schwelle und die Vorhersagegüte auf anderen Karrieren bleiben offen. Bei TRAIN005 erklärt das Modell einschließlich kategorialem Byte und Byte × Lücke 0,115 der Varianz im Analysedatensatz.

Für die Club-Regressionskoeffizienten liegen Holm-korrigierte zweiseitige p-Werte in den Aggregatdateien. Je Modell bilden alle Nicht-Intercept-Koeffizienten gemeinsam die Testfamilie (Zubieta 16, TRAIN005 24). Die Intervallschätzungen sind punktweise. Für die zusätzlichen Korrelationstabellen und die nachträgliche Kurvenanpassung wurde kein konfirmatorischer Test beansprucht. Clubcluster behandeln keine gemeinsame Saison, Karriere, Build-Effekte oder Selektion. Eine zwischen Karrieren gültige 95-%-Spanne, Endpunktkorrelationen für Peak-/Saison-CA und kalibrierte Prognosegüte bleiben fehlend.

Reproduktion mit den privaten Datenbanken und den im Repository gebundenen NumPy-/SciPy-Versionen:

```text
python research/pa-reach-001/analysis/growth_associations.py PRIVATE_TRAIN_DB
python research/pa-reach-001/analysis/zubieta_associations.py PRIVATE_ZUBIETA_DB PRIVATE_NATIVE_DB
python -m unittest discover -s research/pa-reach-001/tests
```

[Historische Analysespezifikation](../../research/pa-reach-001/manifests/association-plan.json) · [Zubieta-Programm mit Kohortenfilter](../../research/pa-reach-001/analysis/zubieta_associations.py) · [Altersgruppen und Beobachtungsdauer](AGE_GROWTH_ANALYSIS.md)

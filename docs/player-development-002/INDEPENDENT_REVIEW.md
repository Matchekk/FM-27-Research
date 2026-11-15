# Unabhängiger Fachagentenreview – CA-002

15.11.2026. Separater Codex-Fachagent; keine unabhängige menschliche Begutachtung
und keine erneute FM-Engineausführung. Geprüft: eingefrorene externe TS-/Rust-
Funktion, CA-002-Protokoll, originale externe A/B/C/D-Belege und sämtliche
fertigen Matrixzeilen. [Maschinenlesbare Nachrechnung](../../data/player-development-002-ca/independent-review.json).

## Bedeutung des Berechnungswegs

Der Aufruf vermisst die Softwarefunktion `estimateCaExact`. Ihr Name enthält
keine unabhängige Genauigkeitsgarantie. Ohne FM27-UI-RCA-Vergleich bleibt die
Einheit **ganzzahlige Modell-RCA**, nicht tatsächlicher CA-Verbrauch. Die
ursprüngliche Editorherleitung betrifft FM26; der Transfer auf FM27 bleibt
eine zu prüfende Quellenannahme. Die externe Prüfung gegen gespeicherte CA
ist keine Validierung gegen RCA-Goldwerte.

Die Funktion verwendet positionsabhängige Gewichte, gezählte Füße,
verteilungsabhängige Korrektur und einen internen Positionsparameter P.
P ist keine direkt beobachtete CA-Differenz. Die äußere Funktion rundet,
begrenzt auf 1–200 und wählt bei AUTO das Maximum über zulässige Positionen.
Ein expliziter Positionsaufruf umgeht diese Maximumwahl. Sekundärpositionen
können daher sowohl den Positionsparameter als auch die gewählte Spalte ändern.

Die iterative Korrektur arbeitet höchstens 100 Runden. `iterations=100` ist
kein Konvergenzzertifikat. Auch eine ganzzahlige Nulldifferenz beweist weder
einen echten Nullpreis noch eine flache kontinuierliche Kostenfunktion;
Rundung, Korrektur und Begrenzung können beitragen. Fehlende Attribute werden
im TS-Original durch Rohwert 1 ersetzt. Reale Profile müssen vor dem Aufruf
auf Vollständigkeit geprüft werden, damit Missing nicht unbemerkt zu 1 wird.
In der tatsächlich erzeugten Matrix wurden höchstens 30 Runden benötigt;
die theoretische 100-Runden-Grenze wurde hier nicht erreicht.

Die konstruierte Zuordnung Rohwert=5×Anzeigewert wird als Szenario behandelt.
Das ist ausreichend für ein offengelegtes Softwareaudit, nicht für eine
behauptete unabhängige UI-Skalenabnahme. Alter und Persönlichkeit sind keine
Inputs; eine im Modell fehlende Abhängigkeit beweist keine Engineunabhängigkeit.

## Neuer externer Karrierebeleg

[Originaler Editorbericht](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/docs/editor-test-plan.md),
SHA256 `429ed04736473c4580da14d828ea68e7a9ee01cfc2b419c23493f5966fb50812`.
Die [abgeleiteten kompakten Messangaben](../../research/playerdev002-editor-evidence.json)
enthalten keine Namen, Spieler-ID, privaten Dateinamen oder Originalspielstände.

Ein Autor berichtet vier Arme desselben Spielers/Anfangssaves mit Savebuild
27.0.0+2486695 über 33 Tage. Die Ergebnisangabe 27.08. weicht vom geplanten
28.08. ab und bleibt ausdrücklich erhalten. A/B/C haben gemeinsam PA 200;
die ursprüngliche Quelle hatte PA 160. Ein unveränderter PA200-Kontrollarm
ist nicht beschrieben. D verwendet ebenfalls PA 200.

Bei gleichem Anfangswert 100 in sechs Attributen enden B mit CA110 bei 85
und C mit CA150 bei 96. Der berichtete Endabstand beträgt elf Rohpunkte
je Attribut beziehungsweise 66 für deren Summe. Die gesamte Attributsumme
unterscheidet sich um 323. Das ist ein zusätzlicher externer Hinweis auf
CA-abhängige Profilanpassung nach einem Edit; **keine Einzelattributkostenmessung,
keine Trainingswirkung und keine unabhängige Replikation**.

Die berichtete Stabilität vier möglicher kostenfreier Attribute in D bei
gleichzeitigem Rückgang von Ausdauer und Stärke ist hypothesengenerierend.
Sie belegt keine universelle Befreiung für alle Positionen, Builds und
Entwicklungszeiträume. Einsatzminuten, Trainingsplan, RNG-Paarung und
Verletzungen fehlen. Kein Konfidenzintervall oder p-Wert aus vier Armen oder
aus den Attributen als vermeintlichen unabhängigen Karriereeinheiten.

## Urteil zum Protokoll

Die geplante Trennung zwischen Modellaudit, bereits gesehenem Export und
extern berichtetem Karriereversuch ist sachgerecht. Ein erneuter OLS-Fit
auf denselben 109 Spielern wäre keine neue Bestätigung; der vorab festgelegte
ungefittete externe Funktionsvergleich kann dagegen eine neue begrenzte
Modelldiagnose liefern. Auch eine geringere MAE gegen Export-CA würde keine
kausalen Grenzkosten oder bessere Matchvorhersage beweisen.

## Vollständige unabhängige Nachrechnung

Alle 3.240 Ausgangs-/Interventionsrequests aus Metadaten selbst rekonstruiert,
sämtliche SHA256 geprüft und die eingefrorene Originalfunktion direkt über
Node erneut aufgerufen. Dabei weder den Analysewrapper noch dessen
Zusammenfassungsfunktion importiert. **0 Requesthash- und 0 Outputabweichungen**.
Die unabhängige Nachrechnung bestätigt:

- 1.620 geplante Zellen, 1.539 eindeutige Interventionen, 81 Aliase. MC20+DC20
  und DC20+MC20 erzeugen unter AUTO dieselben Requests. Die Präregistrierung
  wurde nach der technischen Duplikatabweisung ausdrücklich ergänzt;
  diese Zellen sind keine zusätzlichen unabhängigen Messungen.
- 339 von 513 eindeutigen Leveltripeln besitzen unterschiedliche Differenzen
  zwischen den drei Ausgangsniveaus. Das belegt Niveauabhängigkeit der
  diskreten Softwareausgabe in dieser Matrix, nicht der echten FM27-Kosten.
- Differenzen 0/1/2/3/4 treten 470/570/413/84/2-mal auf. Keine negative
  Differenz, kein Output an der oberen Begrenzung 200.
- Alle 109 Exportprofile sind wegen nicht numerischer Fußangaben für diesen
  unveränderten Schätzer nicht auswertbar. **0 Funktionsauswertungen auf realen
  Exportprofilen**, keine MAE oder Intervallberechnung. Alle Fehler bleiben
  maschinenlesbar erhalten. Das ist kein Ergebnis zugunsten oder gegen das Modell.

Die technische Wiederholung prüft Rechen-/Archivkonsistenz. Sie ist kein
zweiter unabhängiger Kostenalgorithmus, kein FM27-UI-Goldvergleich und keine
native Replikation. **PASS für das deklarierte Modellaudit; echte CA-Grenzkosten
und tatsächliche RCA-Kalibrierung bleiben offen.**

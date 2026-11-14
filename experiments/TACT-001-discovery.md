# TACT-001 – eigene 4-2-3-1 entdecken

**Vorregistrierungsentwurf · 14.11.2026 · nicht gestartet.**
Die konkreten Kandidatenhashes, Eingabeaudits, Seedreservierungen, Analysefassung
und das Rechenbudget müssen vor jeder Stufe veröffentlicht werden.
[Konfigurationsentwurf](../research/specs/TACT-001-draft.json) ist eine strukturelle
Vorlage für den Varianzpilot, kein ausführbares Manifest aller nachfolgenden Stufen.

## Ziel und Hypothesen

Ziel ist die robusteste nachgewiesene **eigene** IP-4-2-3-1 im tatsächlich
untersuchten Suchraum auf Build 27.0.1+2503222. „Stärkste“ bezieht sich auf
vorab festgelegte Kader-, Gegner- und Startkontexte, nicht alle FM-Spielstände.
OOP dürfen Vierer-, Fünfer- und Mittelfeldstrukturen variieren. GK, vier Verteidiger,
zwei Sechser, zwei Flügel, AMC und ST bleiben in der ersten IP-Suchklasse erhalten.
Eine stürmerlose Klasse ist separat, nicht stillschweigend Teil der Optimierung.

Vier vorab benannte wissenschaftliche Interaktionen:

1. Pressingintensität × Defensivlinie.
2. Tempo × Passdirektheit.
3. Stürmerrolle × Zehnerrolle.
4. Außenverteidigerrolle × Flügelrolle.

Nullhypothese je Vergleich: Der Unterschied der marginalen Eingriffe beträgt null.
Die genaue native Rolle, Duty, PI-Policy und Stufe jeder Option wird aus dem
**lokalen validierten Katalog** entnommen. Keine Annahme alter FM-Rollennamen.

## Stufe A/B – Baselines und zulässiger Raum

Eigene vom Lab-Default abgeleitete 4-2-3-1 als primärer Kontrollarm. Eine native
FM27-Preset-4-2-3-1 und die bereits technisch importierte Downloadreferenz dienen
zusätzlich als Referenzpunkte; daraus wird kein Zwei-Downloads-Turnier.
Spielerprofile, Verletzungen, Fitness, Spielschärfe, Moral und Gegnerpolitik
werden explizit eingefroren. Die Kaderidentitäten werden bei Seitenwechsel auf
feste native Plätze übertragen. Fixtureseite ist noch keine reine Stadionintervention.

Vor jedem neuen Typ von Eingriff: gleiche Seeds wiederholen, alle kodierten
Datensätze nach Originalvorbereitung lesen, Rollen-/Positionsmasken und
Spieleranweisungen beider Phasen prüfen. Im Suchraum `rules=game` verwenden;
Positions-/Rollen-/PI-Unvereinbarkeiten sperren den Kandidaten vor Simulation.
`validate_4231()` prüft zusätzlich die feste IP-Positionsmenge. Varianten mit
geänderter OOP-Abbildung müssen alle elf Spieler eindeutig binden.

Suchfaktoren: Pressing, Defensivlinie, Angriffspressinglinie, Passdirektheit, Tempo,
Breite, Umschaltregeln, Aufbau, Flügel-/Zentrumsfokus; Rollen für ST/AMC/Flügel/
Doppelsechs/AV/IV/GK; PI für Pressing, Deckung, Laufwege, Passrisiko, Dribbling
und Positionshalten. Änderungen werden zunächst in sachlich zusammenhängenden
kleinen Faktorgruppen getestet. Keine vollständige Enumeration aller Optionen.

## Erster begrenzter Pilot

Dieser nächste kleine Abschnitt erhält vor dem Start eine eigene eingefrorene
TACT-001-P0-Konfiguration und Analyse. Feste 2×2-Kombination aus zwei nativ
validierten Pressing- und zwei Defensivlinienstufen, gemeinsame Baseline, feste
übrige eigene 4-2-3-1. Zwei vorab fixierte Entdeckungsgegner (hohes Pressing und
tiefer Block), gleiche Kaderstärke, beide Seiten. Acht neue Seeds pro Gegner,
jeder in vier Armen auf beiden Seiten: **128 Hauptmatches**, 16 unabhängige
Seedblöcke, Seitenmittel je Block. Technischer A/A-/Readbackblock separat.

Primär ist die Pressing×Linie-Differenz-von-Differenzen auf xGD; sekundär Punkte,
Tore, Gegentore, xGF/xGA, Schüsse und Fouls/Karten soweit nativ geprüft.
Dieser Pilot schätzt vor allem Varianz und Eingabeverhalten. Er ist **nicht** für
einen 0,10-xGD-Nachweis gepowert; keine Bestätigung und kein finaler Sieger.
Gepaarte Kontraste, Szenariogewicht je 1/2, Seitengewicht je 1/2; t- und
Seedblock-Bootstrapintervall. Ein Primärkontrast, keine Primär-Multiplekorrektur;
Holm über die vorab vollständig benannten sekundären Tests. Keine Ausschlüsse
aufgrund ungünstiger Leistung. Bei fehlendem Arm nur technischen Status berichten.

## Stufe C/D – DoE und Interaktionen

Als erste größere, erst separat zu budgetierende Suchstufe: fünf binäre Faktoren
Pressing (A), Linie (B), Tempo (C), Direktheit (D), Breite (E),
`E=A×B×C×D`: 16 Punkte, Resolution V. `fractional_design()` erzeugt diesen Plan.
Alle Haupt- und Zweifachspalten sind untereinander orthogonal; Zweifacheffekte
sind mit Dreifachinteraktionen aliasiert. Das ist eine Annahme, kein Beweis
verschwindender höherer Interaktionen. Bei relevanten Anzeichen Foldover bzw.
gezielte volle 2×2-Nachprüfung. Kein Resolution-IV-Plan, der gerade die
interessierenden Zweifachinteraktionen miteinander verwechselt.

Rollenpaare zunächst in getrennten vollen 2×2-Blöcken prüfen. PI- und
OOP-Strukturvarianten folgen nach Rollen-/Mappingaudit. Sämtliche Faktoren und
Kontraste einer Stufe vor Datenzugriff festlegen. Für vier gemeinsame Primärfragen
Holm bei α=0,05; marginale 95-%-Intervalle als marginal kennzeichnen.
Geteilte Baselines und wiederholte Seiten/Gegner bleiben im Seedblock erhalten.

## Stufe E – begrenzte Optimierung

Implementiert ist ein reiner Vorschlagskern: Ridge-Modell mit Haupt- und
Zweifachmerkmalen, gewichtet nach Unsicherheit aus den Entdeckungsblöcken.
Maximal 256 bereits legal geprüfte Nachbarschaftskandidaten im Vorschlagspool,
maximal vier neue Vorschläge pro Runde. Keine vollständige kartesische Suche.
`propose()` nimmt ausschließlich `split=discovery` an und löst keine Matchläufe aus.

Rangmaß im Modell: vorhergesagter Mittelwert minus 1,96 Modell-SE.
**Zusätzliche Auswahlregel nach realer Nachprüfung:** untere Unsicherheitsgrenze
des gleichgewichteten Kontextmittels, schlechtester Gegner-/Stärkekontext,
Varianz und praktische Verbesserung gemeinsam ausweisen. Schlecht belegte
Kontexte können nicht durch ein einzelnes maximales Match kompensiert werden.
Modell-SE ist keine konfirmatorische Post-Selection-Unsicherheit.
Rundenzahl und Gesamtspielbudget vor jeder Suchserie fest fixieren; kein
leistungsabhängiges optionales Stoppen und kein Zwischenzugriff auf Holdouts.

xGD und optional modelliertes xPts dürfen Screeninghilfen sein. xPts braucht ein
benanntes Modell und eine Kalibrierungsprüfung; Poisson aus xG ersetzt keine Tore.
Der erste Kern verwendet daher nur xGD als Surrogat. Erkenntnisse zur Verwertung,
Torwartleistung und späten Spielständen werden an echten Resultaten überprüft.

## Stufe F – unabhängige Bestätigung

Höchstens ein nach der eingefrorenen Auswahlregel gewählter Kandidat gegen die
eigene Baseline. Kandidat, vollständige Konfigurationen und Analysecommit vor
dem ersten Holdout-Match einfrieren. Frische **unbenutzte** Seeds und getrennte
Gegnerprofile; zusätzliche Stärken: schwächer, gleich, stärker. Beide Seiten.
Kein Austausch eines enttäuschenden Holdoutgegners. Der Kandidat darf anschließend
nicht auf diesen Daten verbessert und erneut als unabhängig bestätigt gelten.

Primär: tatsächliche Punkte pro Match. Sekundär: Tore und Gegentore, xGD,
Kontextrobustheit; vorab Holm-Familie und praktische Punkteschwelle festlegen.
Fallzahl aus gepaarter Pilot-SD und ihrer 95-%-Obergrenze, Zielpower 90 %.
Bei angenommener Punkte-SD 1,5 braucht ein Unterschied von 0,15 Punkten etwa
1.053 unabhängige Blöcke bei einem Test; die endgültige Rechnung ist keine
Übernahme dieser Annahme. Wirkungsrichtung, Präzision und praktische Schwelle
getrennt entscheiden. Ein breites Nullintervall bedeutet „unklar“.

## Integrität und Artefakte

Pro Match Build, Tool-/Host-/Code-/Setuphash, Seed, Szenario, Stärke, Teamseite,
Arm, Rohlog-, Dump- und Startup-Receipthash; Ausfälle separat. Hauptserie stoppt
bei Identitäts-, Seed- oder Readbackabweichung. Keine Ersatzseeds oder stillen
Nullwerte. Vorregistrierung und Analysen auf GitHub vor Start; danach Ledger,
Effekte, Konfidenzintervalle, Korrekturen und alle negativen Ergebnisse publizieren.
Ergebnisstufe bis zur gehaltenen Bestätigung: **explorativ**.

Gültigkeit bleibt auf validierten nativen Startzustand begrenzt. Taktikausführung,
Training der Komplexität und Live-Management sind vor Karriereempfehlungen
separat zu prüfen. [Externe methodische Referenzen](../docs/EXTERNAL_RESEARCH.md).

# TRAIN-002 – Entwicklung und kurzfristige Leistung trennen

**Vorregistrierbarer Karriereentwurf · nicht gestartet · 14.11.2026.**
[Maschinenvertrag](../research/specs/TRAIN-002-draft.json).
Die automatische Karrierefortschreibung und Teilnahmeauslese sind noch nicht
validiert. Native Einzelmatches können diese Studie nicht ersetzen.

Hypothese: Heavy Conditioning verändert körperliche Entwicklung und Ermüdung
gegenüber Conditioning, mit unterschiedlicher Wirkung bei Profis und U19.
Zwei getrennte Altersstrata. Primär je Stratum: Veränderung eines vorab fixierten
Rohattributindex aus Antritt, Tempo, Beweglichkeit und Ausdauer nach sechs Wochen.
Index = ungewichteter Mittelwert der vier Rohwertänderungen, mit identischer
Skalierung in beiden Armen. CA, taktisches Verständnis, Matchpunkte, Fitness,
Ermüdung und Verletzungstage sind sekundär; Entwicklung und kurzfristige Leistung
werden nicht zu einem uninterpretierbaren Gesamtscore zusammengezogen.

Kontrolle: fest veröffentlichter Wochenplan mit zwei Conditioning-Slots/Woche.
Intervention: genau diese zwölf Slots durch Heavy Conditioning ersetzen.
Gleiche Coaches samt Zuteilung, Trainingsanlagen, Kader, Gegner, Spielkalender,
individuelle Schwerpunkte, Taktik, Matchminuten und Rotationsregel. Kalender-
Readbacks am Start und nach jeder Woche, tatsächliche Teilnahme je Spieler und
Session, Ausfälle, Nachholspiele und durch Spieltermine verdrängte Einheiten
erfassen. Nicht nur die geplanten Trainingseinheiten zählen.

Acht unabhängige Startzustands-Replikate je Stratum, jeweils bytegleiche
Startdatei **zwischen den zwei Armen eines Replikats**, ergeben 32 Karrierearme
und sechs Wochen Beobachtung. Alle Startzustände stammen aus derselben
kontrollierten Ausgangskarriere; ein tatsächlich unabhängiger Zufallszustand je
Replikat muss nativ belegt werden. Acht Kopien derselben Datei ohne neue
Zufallsrealisation sind keine acht unabhängigen Replikate. A/A-Zweig zunächst
zur Messung von Determinismus und stochastischer Varianz.

Spieler sind wiederholte Beobachtungen innerhalb eines Karrierearms. Analyse
primär auf gepaarten Ablegerdifferenzen, Alterstratum vorab getrennt; Holm über
die zwei primären Alterskontraste. Rohwertindex, Baselinealter und PA-Stratum
vor Start definieren; keine nachträgliche Auswahl der stärksten Entwickler.
95-%-Clusterintervalle, tatsächliche Exposition und effektive Replikatzahl berichten.
Bei nur acht Paaren sind Intervalle grob: dies ist ein Varianz-/Durchführungspilot.
Bestätigungsfallzahl per Simulation auf Ablegerebene unter SD-/ICC-Sensitivität,
Zielpower 90 % für eine vorab festgelegte praktische Rohwertänderung.

Verletzungen: Tage und Ereignisse je 1.000 tatsächlich exponierter Trainings- und
Matchstunden, Überdispersion und konkurrierende Ausfälle berücksichtigen.
Keine Nullersetzung für fehlende Attribute/Exposition, kein ergebnisabhängiger
Save-Restart. Verzerrte Matchminuten oder Kalenderabweichungen separat zeigen;
bei fehlender kontrollierter Durchführung keine kausale Trainingsbehauptung.
Ein späterer Optimierer erhält getrennte Ziele für Entwicklung, Matchleistung
und Belastung. Trainerqualität, Zusatzfokus und Intensität bleiben eigene Studien.

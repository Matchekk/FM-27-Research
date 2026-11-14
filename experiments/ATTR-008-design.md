# ATTR-008 – Attributgrenzwerte im taktischen Kontext

**Vorregistrierbarer Designentwurf · nicht gestartet · 14.11.2026.**
[Maschinenvertrag](../research/specs/ATTR-008-draft.json).

Hypothese: Der marginale Nutzen einer Sprunghöhenanhebung hängt von Ausgangsniveau,
Position und Taktik ab. Kontrollarm: gleiche eigene 4-2-3-1 bzw. kontrollierte
4-3-3, unverändertes Profil. Intervention: ausschließlich Sprunghöhe +2
Anzeigepunkte bei einem nativ zugeordneten ST oder DCR. Ausgangswert 10 oder 14;
Rohwerte und Umrechnung vorab lesen und einfrieren. Ein Spieler je Eingriff
verhindert unterschiedliche Gruppengrößen als Erklärung. Keine nachträgliche
Auswahl besonders günstiger Spieler.

2 Positionen × 2 Ausgangsniveaus × 2 Taktiken = acht Kontexte, je zwei Arme,
32 neue Seeds und beide Seiten: **1.024 Pilotmatches**. Das vollständige Design
wird nicht automatisch gestartet. Als erster kleiner Abschnitt kann genau ein
vorab benannter Kontext mit 128 Matches als Varianzpilot registriert werden;
die jetzige Plattformvorlage beschreibt noch keinen ausführbaren Gesamtlauf.
Reale Profilvariationen und Mannschaftsstärken folgen als gehaltene Replikation.

Primär: Änderung tatsächlicher Punkte pro Match; primärer Interaktionskontrast
ist der Unterschied des marginalen Attributeffekts zwischen Ausgangsniveau 10
und 14, gleichgewichtet über die vier Position-/Taktikkontexte. Sekundär xGD,
Tore, Gegentore, Tore minus xG, Kopfballabschlüsse und Verwertung soweit
ereignisnativ prüfbar. Ein reines xG-Ranking würde Chancenverwertung ausblenden.
Für Finishing und Torwartattribute separate spätere Studien mit Tor-/Saveendpunkten.

Native Prüfung: vollständige Attributvektoren, CA-/Positions-/Ausführungszustand,
Spielerbindung, beide Phasen; genau ein deklarierter Attributwechsel pro
Arm-Kontextpaar. CA und Fähigkeiten dürfen nicht unbemerkt mit der Intervention
neu standardisiert werden. Falls ein abgeleiteter Ausführungswert kausal mitändert,
als Mediator dokumentieren; keinen reinen Direkteffekt behaupten.

Auswertung: Seitenmittel pro Seed, gleichgewichtete Kontextkontraste,
95-%-t-/Blockbootstrapintervalle. Ein Primärtest α=0,05; alle vorab aufgelisteten
Sekundärinteraktionen als gemeinsame Holm-Familie. Praktisch relevantes Ziel
vor Bestätigung festlegen (Planungsszenario 0,15 Punkte). 32 Blöcke je Kontext
sind ein Streuungspilot, kein gepowerter Nachweis dieses kleinen Effekts.
Pilot-SD-Obergrenze und nichtzentrale t-Power 90 % bestimmen neue Fallzahl.

Negative Kontrollen: A/A, komplette binäre Differenzprüfung, eindeutige ST/DCR-
Zuordnung, keine Verschiebung übriger Profile. Keine aus Ergebnisgründen
verworfenen Matches; alle Fehler erhalten. Neue Bestätigungsseeds, andere
Gegner und andere Spielerprofile vorab einfrieren. Alte ATTR-001–007 bleiben
Build 27.0.0+2493426 zugeordnet. Externe Positions-/Schwellenstudien dienen der
Fragenauswahl, nicht als unabhängig bestätigte Gewichte für dieses Labor.

# SET-001 – eigene Eckroutine mit Expositionskontrolle

**Vorregistrierbarer Designentwurf · nicht gestartet · 14.11.2026.**
[Maschinenvertrag](../research/specs/SET-001-draft.json).
Vor dem Start fehlen noch auditierte Ereignis-/Besitzkettenzähler.

Hypothese: Eine selbst entworfene offensive Eckroutine steigert den Netto-xG-
Ertrag pro entstandener Ecke gegenüber einer eigenen festen Kontrollroutine.
Intervention: genau eine Aufgaben-/Zielzonenverteilung der offensiven Ecken;
Schützen, Fuß, defensive Restabsicherung, Spielerprofile und alle übrigen
Taktikeingaben konstant. Variiert die Restabsicherung, erhält das einen eigenen
Faktor statt einer versteckten Begleitänderung. Beide Mannschaftsseiten prüfen.

Fester Pilot: 64 neue Seeds, zwei Arme, beide Seiten = **256 vollständige Matches**.
Erwartet werden mindestens 200 tatsächlich entstandene eigene Ecken pro Arm;
das ist ein Zähler-/Varianzplan, keine Erlaubnis für nachträgliches Verlängern.
Alle entstandenen Ecken zählen; bei wenigen Situationen geringe Präzision berichten.
Eine Bestätigungsfallzahl wird aus beobachteter Exposition, Überdispersion und
vorab gewählter kleinster relevanter Rate per Simulation geplant.

Primär: (eigenes xG aus Eckketten minus gegnerisches xG aus unmittelbaren
Konterketten) / Zahl tatsächlich entstandener eigener Ecken, berichtet pro 100
Ecken. Eckkette vorab operationalisieren: vom nativen Eckereignis bis zur nächsten
Spielunterbrechung oder kontrollierten gegnerischen Ballbesitzphase; gegnerische
Konterkette ab Besitzwechsel bis Unterbrechung, erneutem eigenen kontrollierten
Besitz oder zehn Sekunden nativer Matchzeit. Genau diese Enden müssen der
Ereignisadapter und Handprüfungen aufzeichnen können. Andernfalls kein Start.

Sekundär: Tore/100 Ecken, xG/Ecke, Kontertore/-xG, Zahl Ecken/Match,
Netto-xG/Match und tatsächliche Punkte/Tore/Gegentore. Entstandene Ecken sind
potenziell selbst durch die Routine beeinflusst: der bedingte Situationsquotient
ist deshalb kein vollständiger kausaler Gesamteffekt. Den unbedingten Matchertrag
immer daneben ausweisen. Keine Multiplikation einer Rate mit einer anderen
Studienbasis als vermeintliche Saisonprognose.

Analyse auf gepaarten Seed-/Matchclustern, gemeinsame Resamples aller Ereignisse
eines Clusters. Primäre Ratendifferenz mit Clusterbootstrap und 95-%-Intervall;
Zählmodell mit Expositionsoffset als Sensitivität. Sekundärmetriken in einer
vorab vollständig gelisteten Holm-Familie. Corner-ID-, Ketten- und Torzählungen
mit nativen Ereignissen und Teamstatistik abgleichen. Negative Kontrolle: gleiche
Routine unter zwei Labels; ungültige Prioritäten/Taker müssen scheitern.

Routinen bleiben lokal; öffentliche Dateien enthalten nur Hashes und erlaubte
zählbare Beobachtungen. Weitere Studien zu defensiven Ecken, direkten/indirekten
Freistößen, Einwürfen und Elfmeterschützen werden getrennt registriert.

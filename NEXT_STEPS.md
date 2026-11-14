# Nächste Schritte – priorisierte Forschungsaufträge

## Aktueller Einstieg – 14.11.2026

1. [VALID-002](experiments/VALID-002-adapter.md) und den tatsächlich freigegebenen
   Fixturekontext beachten. Neue Rollen, PI oder Startprofile zuerst nativ auditieren.
2. [TACT-001-P0](experiments/TACT-001-discovery.md#erster-begrenzter-pilot) mit
   128 Hauptmatches separat vorregistrieren: eigener 4-2-3-1-Kontrollarm,
   Pressing × Linie, zwei fixierte Entdeckungsgegner, neue Seeds; keine OP-Aussage.
3. Karriere-PKM-Kapazitätsadapter und Standardsituationszähler sind technische
   Folgearbeiten. TRAIN-Längsschnitt erst nach echtem Kalender-/Teilnahmeaudit.
4. [Gesamtroadmap](docs/ROADMAP.md) und [externe Studien](docs/EXTERNAL_RESEARCH.md)
   nutzen; keine bloße Wiederholung bekannter globaler Attributranglisten.

Die folgenden Checklisten dokumentieren den bisherigen Forschungsstand auf dem
alten Build. Sie sind kein Startauftrag für neue Serien auf der aktualisierten Engine.

## P0 – Arbeitsumgebung und Baseline validieren
- [x] Lokale Rohdaten inventarisiert, Engine- und Adapterhash geprüft.
- [x] Baseline, native Eingaben, Wiederholungen und Negativprobe nachvollzogen. [VALID-001](experiments/VALID-001-adapter.md)
- [x] Öffentliches Archiv aus zulässigen Messfeldern und Prüfsummen erstellt.
- [ ] Den Lab-Host mit einer normalen Karrierepartie unter kontrolliertem Startzustand vergleichen. Live-Coaching, Urlaub und Instant Result getrennt prüfen.

## P1 – Attribut-Screening (nach P0)
- [x] 16 Attribute mit je 40 Paaren ausgewertet und die Auswahlregel nachvollzogen. [ATTR-001](experiments/ATTR-001-screening.md)

## P2 – Replikation
- [x] Fünf Kandidaten mit 240 neuen Paaren je Attribut ausgewertet. [ATTR-002](experiments/ATTR-002-hauptreplikation.md)
- [x] Antritt und Tempo bei alternativer Gegnermentalität und gepaartem Seitenwechsel geprüft. [ATTR-003](experiments/ATTR-003-zusatzszenarien.md)
- [x] ATTR-004 vorregistriert und den nativen Setup-, Seitenwechsel- und Wiederholbarkeitscheck bestanden. [Vorregistrierung](experiments/ATTR-004-cross-tactic.md) · [Validierung](data/attr-004/validation-summary.json)
- [x] ATTR-004-Hauptserie mit 3.360 vollständigen Matches ausgewertet. Beide Aufwertungen verbessern xGD im Mittel. Der direkte Unterschied liegt im praktisch kleinen Bereich. [Ergebnisse](experiments/ATTR-004-ergebnisse.md)
- [ ] Für präzisere Kontextschätzungen Gegnermentalitäten mit gemeinsamen Seeds und separater Baseline pro Profil vergleichen. Für den Seitenwechsel feste Fixture-Plätze gezielt von Standortmechanismen trennen.
- [x] ATTR-004-Analyseplan vor der Datenerhebung versioniert. Primärtest, Abhängigkeit geteilter Baselines und Holm-Familie festgelegt. [Analysecode](analysis/analyse_attr004.py)

## P3 – Positions-, Taktik- und Trainingsstudien
- [x] ATTR-005-Positionsscreening mit 900 Hauptmatches abgeschlossen. Der Angriff ist für beide Attribute ein explorativer Kandidat. [Ergebnisbericht](experiments/ATTR-005-ergebnisse.md)
- [x] ATTR-006 mit 300 neuen Paaren ausgewertet. Positiver xGD-Effekt der Sprunghöhenanhebung bei AMR, AML und ST im Standardfixture bestätigt. [Ergebnisbericht](experiments/ATTR-006-ergebnisse.md)
- [x] ATTR-007 mit 200 neuen Achtarmblöcken ausgewertet. ST zeigt einen positiven Shapley-Beitrag, der Abstand zum Flügelmittel bleibt nach Holm offen. [Ergebnisbericht](experiments/ATTR-007-ergebnisse.md)
- [ ] Einen unabhängigen Achtarmversuch mit Shapley(ST) minus Flügelmittel als einzigem Primärkontrast vorregistrieren. Für 0,10 xGD bei 90 % Power liegen die Planungsschätzungen bei 283 bis 337 neuen Seeds. [Fallzahlen](experiments/ATTR-007-ergebnisse.md#fallzahlen-und-vorgeschlagene-folgestudie)
- [ ] Die praktische Schwelle von +0,10 xGD und die Übertragbarkeit des Eingriffs auf andere Angriffsrollen oder Fixtures in getrennten Designs untersuchen.
- [ ] Pressing × Defensivlinie in 2×2-Design.
- [x] Bestehende Karriereversuche mit Kalender-Readback und A/A-Kontrolle archiviert. [TRAIN-001](experiments/TRAIN-001-karriere.md)
- [ ] Conditioning vs. Heavy mit mehreren unabhängigen Save-Ablegern pro Arm, vergleichbarer Spielbelastung und Ausfalltagen erneut prüfen.
- [ ] Für Trainerqualität, Zusatzfokus und individuelle Intensität jeweils einen separat schreib- und lesbaren Eingriff validieren.
- [ ] FM27-Buildwechsel erkennen und erforderliche Revalidierung planen.

## Nach jedem abgeschlossenen Meilenstein
`RESEARCH_LOG.md`, ggf. `FINDINGS.md` und diese Liste aktualisieren, committen und **pushen**. Push-Status und SHA angeben.

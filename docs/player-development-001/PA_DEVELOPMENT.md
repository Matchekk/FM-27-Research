# PA und erreichte Entwicklung

Status15.11.: **Kein kalibriertes Prognosemodell**. Keine zugänglichen,
validierten saisonübergreifenden Trainings-/Holdoutverläufe im Forschungsarchiv.
Die berichteten fünf Progression-Factor-Stufen werden nicht erneut getestet.
Ihre konkrete FM27-Codeprovenienz und kausalen Übergangswahrscheinlichkeiten
sind im aktuellen überprüften Material nicht belegt; nicht als Codebeweis zählen.
Weitere Quellenprüfung und getrennte Mechanismeneinordnung folgt.

## Was heute tatsächlich verifiziert wurde

Der konkret auffindbare [Progression-Factor-Beitrag](https://www.fmscout.com/a-progression-factor-in-football-manager.html)
ist vom **7.Oktober2020**, nicht von2026. Die Seite verweist auf einen
Videobeitrag und Gespräche mit SI; sie enthält keine identitätsgebundene
FM27-Codeanalyse. Suchbegriffe mit FM27, progression factor, development tiers
und eine begrenzte öffentliche Codesuche lieferten hier keinen überprüfbaren
FM27-Vertrag für fünf Stufen oder deren Übergänge. Das beweist keine
Nichtexistenz der Mechanik. Die berichtete Behauptung bleibt **extern berichtet,
für diesen FM27-Build nicht unabhängig verifiziert**. Ältere Engines werden
nicht still auf27.0.1 übertragen.

Die aktuellen öffentlichen [fmsave-Spielermodelle](https://github.com/rhiever/fmsave/blob/f4f70f62cccae27c63c8dc9610f50c16d5ddcc29/src/fmsave/models/players.py)
kennzeichnen `Ability.current`, `potential` und `potential_range_code`
ausdrücklich als **unconfirmed**. Das ist ein Reader-Metadatum und kein Beweis,
dass ein konkreter ausgelesener Wert falsch ist. Es verhindert aber eine
ungeprüfte Gleichsetzung mit validierten Goldmessungen. Im inventarisierten
Modell ist kein validierter Progression-Factor-Endpunkt ausgewiesen.
Der lokal installierte Reader bleibt0.9.0; der separate historische0.12.4-
Quellenaudit und heutiger Upstreamcommit sind keine lokale Saveabnahme.

## Mechanismen, Zusammenhänge, Kausalität

| Ebene | Aktueller belastbarer Status |
|---|---|
| Direkt durch FM27-Code belegt | In dieser Sitzung kein Entwicklungsmechanismus identitätsgebunden verifiziert |
| Beobachtete Karriereentwicklung | TRAIN-001: einzelne Ableger/Kohorten, alte Buildbindung, begrenzte Rohattribut-/CA-Deltas |
| Kausal identifizierte Änderung einer Entwicklungsstufen-Wahrscheinlichkeit | Keine |
| Professionalität, Ehrgeiz, Zielstrebigkeit, Trainer, Anlagen, Minuten | Kandidaten; keine hier kalibrierten Effektstärken oder Übergangswahrscheinlichkeiten |
| Wechsel/Vertrag/Managerwechsel als Auslöser | Ungeprüfte Hypothesen für den konkreten Build; Beobachtungen wären stark selektionsgefährdet |
| Alter und PA−CA-Abstand | Potenzielle Prädiktoren, keine aus diesem Archiv geschätzten Zukunftswahrscheinlichkeiten |

Höhere PA und eine große Lücke liefern keine Erfolgswahrscheinlichkeit.
Mehrere Snapshots desselben Spielers oder Saveklone sind keine unabhängigen
Karriere-Replikate. Eine Heuristik „aktueller CA plus Anteil der Lücke“ wäre
eine Szenarioannahme, keine kalibrierte Prognose. Künftige CA kann auch sinken.

## C2: prüfbares Prognoseziel, heute kein trainiertes Modell

CA nach1/2Saisons und `P(CA_t ≥ Schwelle)` brauchen vollständige,
zeitlich geordnete, versionierte Karriereverläufe. Trainings- und Testdaten
müssen Spieler trennen; zusätzliche Clustertrennung nach Save/Verein und
zeitlicher Holdout gegen Leakage. Transfer, Ruhestand, Ausfälle und fehlende
Endpunkte bleiben sichtbar. Gegen Baselines „CA bleibt gleich“ und einfache
Alters-/PA-Gap-Prognose: MAE/Bias, Kalibrierung, Brier-Score für Schwellen und
Coverage/Schärfe der Vorhersageintervalle auf gehaltenen Verläufen berichten.

**Heute n=0geeignete saisonübergreifende Testverläufe; MAE/Brier/Coverage=null.**
Kein Modellfit, keine Zukunfts-CA-Verteilung und keine PA-Erreichungsquote
veröffentlicht. Development Potential bleibt im Komponentenmodell unbekannt.

Die neu geprüfte [Scout-Reporter-Potenzialprojektion](https://github.com/SebastianFoder/fm-scoutreporter/blob/3144dd0a45eb4f994230700c8faee64d33665273/packages/core/fm27/potential.ts)
verteilt einen unterstellten CA→PA-Spielraum nach Tabellen- und Wachstumsgewichten.
Eine109-GK-Querschnittsanpassung ist keine saisonübergreifende Testkohorte.
Die Projektion beschreibt ein Szenario bei voller Potenzialausschöpfung;
sie liefert keine beobachtete Wahrscheinlichkeit, dass ein Spieler dort ankommt.
Auch unser neuer CA-Exportdiagnosetest ändert diesen PA-Status nicht.

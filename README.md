# FM27 Meta Research

Offenes, reproduzierbares Forschungsprojekt zur **Football Manager 2027**-Meta: Spielerattribute, Positionen, Taktiken und Training.

> **Forschungsstatus (2026-11-07):** Das Archiv enthält die bisherige Serie mit 2.504 geprüften Matchmessungen, die 3.360 Hauptmatches und 96 technischen Prüfläufe von ATTR-004 sowie separate Karriere-Trainingsversuche. ATTR-004 bestätigt die mittleren xGD-Gewinne von Sprunghöhe und Antritt über acht getestete Szenarien. ATTR-005 ergänzt 900 Hauptmatches und 36 Prüfmatches für vier Positionsgruppen. ATTR-006 bestätigt in 600 Hauptmatches den positiven xGD-Effekt einer Sprunghöhenanhebung für drei Angreifer im Standardfixture. [Befunde und Gültigkeitsbereich](FINDINGS.md)

## Arbeitsprinzip

- **Markdown-first:** Fragestellungen, Methodik, Entscheidungen, Ergebnisse und nächste Schritte in `.md`.
- **Reproduzierbare Rohdaten:** Maschinenlesbare Messungen in `.jsonl`, Versuchsmanifest und Konfiguration in `.json`. `.csv` nur bei Bedarf als abgeleiteter Export.
- **Keine überzogenen Schlussfolgerungen:** Strikte Trennung von Hypothese, Einzelbefund, vorläufiger Replikation und bestätigtem Ergebnis.
- **Buildgebunden:** Jede Aussage bezieht sich auf die tatsächlich getestete FM27-Version, Engine-/Adapterversion und Versuchsbedingungen.
- **Ein Faktor pro Vergleich:** Änderungen kontrollieren; gleiche Seeds und Startzustände bei gepaarten Vergleichen.
- **Kein geschütztes Spielmaterial:** Keine FM-Spielstände, Original-DLLs, Spielarchive, ausführbare Dateien oder Geheimnisse committen.

## Orientierung

| Dokument | Zweck |
|---|---|
| [AGENTS.md](AGENTS.md) | Verbindliche Arbeitsanweisungen für Codex |
| [METHODOLOGY.md](METHODOLOGY.md) | Versuchsdesign, Statistik und Qualitätssicherung |
| [FINDINGS.md](FINDINGS.md) | Evidenzbasierte Erkenntnisse und ihr Status |
| [HYPOTHESES.md](HYPOTHESES.md) | Hypothesen und zu testende Mechanismen |
| [RESEARCH_LOG.md](RESEARCH_LOG.md) | Chronologisches Forschungsjournal |
| [NEXT_STEPS.md](NEXT_STEPS.md) | Priorisierte Forschungsaufträge |
| [experiments/TEMPLATE.md](experiments/TEMPLATE.md) | Vorlage für jeden Versuch |
| [data/README.md](data/README.md) | Datenformate und Provenienz |

## Forschungsprogramm

1. **Attribut-Meta:** Welche Attribute verändern Ergebnisse unter kontrollierten Bedingungen?
2. **Positions-Meta:** Welche Attribute sind bei welchen Rollen und Positionen besonders wirksam?
3. **Taktik-Meta:** Welche Anweisungen und Kombinationen bringen messbare Vorteile?
4. **Trainings-Meta:** Welche Einheiten und Belastungsprofile entwickeln relevante Attribute effizient?

## Zusammenarbeit

Codex implementiert und führt Experimente lokal aus, prüft die Rohdaten, aktualisiert die Forschungstexte, **committet und pusht** abgeschlossene, überprüfte Arbeit. ChatGPT kann danach die auf GitHub veröffentlichten Änderungen lesen, kritisch überprüfen und Folgeexperimente konzipieren. GitHub-Pushes werden nicht automatisch von ChatGPT im Hintergrund beobachtet.

**Einstieg:** [NEXT_STEPS.md](NEXT_STEPS.md) lesen, dann [AGENTS.md](AGENTS.md) und [METHODOLOGY.md](METHODOLOGY.md).

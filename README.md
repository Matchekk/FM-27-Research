# FM27 Meta Research

Offenes, reproduzierbares Forschungsprojekt zur **Football Manager 2027**-Meta: Spielerattribute, Positionen, Taktiken und Training.

> **Forschungsstatus (2026-11-06):** Projektstruktur eingerichtet. Frühere Experimente existieren lokal, sind hier aber **noch nicht als Rohdaten importiert oder unabhängig validiert**. Es gibt daher noch keine bestätigte FM27-Meta-Rangliste.

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

# VALID-001 – Build, Eingabe und Wiederholbarkeit

**Stand 2026-11-06 · FM27 27.0.0+2493426**

| Komponente | Geprüfte Provenienz |
|---|---|
| FM27-Engine | `27.0.0+2493426` · SHA-256 `252ff8fb5b7a4a5a5464db6ba632e309eef9b6e65ffa992ae20575a189e66c6a` |
| Adapter | `fm27_desktop_2493426_adapter_v1` |
| Tactics Lab | v1106, Basis-Commit `756296240632cb71552271f0ae9e9e69d65e34bc` |
| Tatsächlich ausgeführter Host | SHA-256 `50c8eef1e3c560974070163ec2c1633508be314bdd31d69de5388470efc0f81a` |
| Fixture | SHA-256 `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6`, Aufzeichnungsformat `26.8.0.0` |

Der lokale Host stammt aus einem veränderten Lab-Checkout. Die Basisversion allein identifiziert daher die Ausführung nicht. Das Manifest enthält zusätzlich Quellhashes und den Fingerabdruck der Kompatibilitätsprüfung. Der Import hat den Engine-Hash der Installation erneut geprüft und die lokalen Startup-Belege aller 2.504 akzeptierten Matches mit Engine, Host und Build im Manifest abgeglichen. Die Fixture-Formatversion beschreibt das Eingabeformat.

Die Validierungsserie umfasst vier Seeds, zwei Eingaben (Baseline und Antritt) und drei Wiederholungen je Kombination. Alle 24 Matches endeten natürlich. Alle acht Wiederholungsgruppen stimmten bei Endstand, nativer Teamstatistik und Endtick exakt überein. Der lokale Audit verglich außerdem die 69 Attributwerte aller 23 beziehungsweise 26 Kaderspieler in den Readback-Dumps. Innerhalb jeder Wiederholungsgruppe stimmten diese Werte überein. Zwischen Baseline und Antrittsintervention änderten sich genau zehn Attributwerte an Index 49 auf der behandelten Seite, jeweils von 60 auf 80. Die anderen Studienszenarien haben pro Lauf einen nativen Readback-Beleg. Der lokale Import prüfte zusätzlich die codierten Unterschiede für alle Arme gegen ihre Baseline samt Adapter-Defaults.

Zwei Versuche mit derselben absichtlich fehlerhaften Konfiguration wurden mit Exitcode 108 abgewiesen. Beide sind getrennt erfasst und enthalten keine Ergebnisse. Die 2.504 akzeptierten Matches setzen sich aus 24 Validierungsläufen, 680 Screening-Läufen, 1.440 Hauptreplikationsläufen und 360 Zusatzläufen zusammen. Die Validierungswiederholungen fließen nicht in die Effektschätzung ein.

Der Lab-Quick-Modus verwendet den detaillierten Spielablauf bis zum natürlichen Ende und schränkt die Ereigniserfassung ein. Die Studie standardisiert unter anderem Fitness, Schärfe, Ermüdung und Moral. Die Wiederholbarkeit ist für den protokollierten Host, die zwei Validierungseingaben und die vier Seeds belegt. Für den kompletten Karriereablauf, Live-Coaching, Urlaub und Instant Result fehlt ein gepaarter Vergleich mit identischem Spielzustand. [Dokumentation des Tactics Lab](https://github.com/lqf0624/fm-tactics-lab/blob/main/docs/SIMULATION_FIDELITY.md)

Das öffentliche Archiv erlaubt die statistische Reproduktion der Matchdaten. Gehashte lokale Belege dokumentieren die Herkunft. Vollständige Eingabedumps, Fixture, ausführbarer Host und lokale Pfade verbleiben außerhalb des Archivs.

[Manifest](../data/matches/manifest.json) · [Wiederholungsprotokoll](../data/matches/validation-summary.json) · [Validierungsmatches](../data/matches/validation.jsonl) · [Abgewiesene Versuche](../data/matches/validation-failures.jsonl)

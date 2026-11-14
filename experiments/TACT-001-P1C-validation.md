# TACT-001-P1C – technische Freigabe vor dem Hauptlauf

14.11.2026. Vorregistrierung/Code/Eingaben/131Seeds vor dem ersten Vollmatch
gepusht in `bd3d9baa04b0a66ce8b80d37eb0b3c8f305849a5`.

**16/16 technische Vollmatches akzeptiert**, acht eindeutige
Gegner×Seite×Arm-Zellen jeweils zweimal vollständig geprüft. Acht exakte
A/A-Paare in Score, Endtick, vollständiger Teamstatistik, Setuphash und Seed.
Absichtlich ungültige Binäreingabe mit **Exit108** abgewiesen, kein Naturabschluss
und kein Nullresultat. Alle17 technischen Versuchsplätze verbraucht.

Acht Setups sind bytegleich zu D00/D15 aus P1B. Native Nach-Vorbereitungsreadbacks
bestätigen beide Phasen/Positionen/Rollen/Duties/PI,69 Attribute,1.058 Profilfelder,
Mentalität, sämtliche Instruktionsgruppen beider Teams und wirksame Seeds.
D15-Bits A66/B57/C47/D3/E0, D00 standard. Alle Creatorbits stimmen mit
Designmatrix/Vertrag/Analyse überein. Natürlicher Abschluss und Statsplausibilität
bestanden. FM27-Dateiversion27.0.1/Produkt27.0.1+2503222; Engine/Host/Fixture/
Ressourcen/Adapter v1114.6 sowie Katalog und Runtimequellen entsprechen VALID-002/P1B.
Vollständige SHA256 in den verlinkten Eingaben. Keine fremde Datei verändert.

Kumulierte beaufsichtigte Child-Wall-Time einschließlich Vorbereitung/Probes/Audits:
**24.623/900 Sekunden**. Studienfenster bis Technikabschluss
124.878/1800s; feste UTC-Deadline
`2026-11-14T14:48:16.844148+00:00`. Kein Zählerreset, kein Retry/Ersatzseed.
Maximal4Worker,90s Fortschrittstimeout. Alle512 Hauptjobs noch unbegonnen.

## CI-Befund und Behebung

Erste CI43604285753 scheiterte ausschließlich an einem neu hinzugefügten Test:
Der Test las die technische Seedplanung aus ignoriertem `local/`, das auf GitHub
nicht existiert. Der Offline-Test verwendet jetzt ausdrücklich die identische
**veröffentlichte** Seedplanung und prüft weiterhin alle16 technischen Jobs.
Kein Ausführungs-/Analysecode, Vertrag, Eingabe, Seed oder wissenschaftliches
Kriterium wurde geändert. Lokal erneut48/48 Tests bestanden; der Hauptlauf
wartet auf erfolgreiche CI dieses Freigabecommits. Kein nativer Fehlversuch.

Diese Freigabe betrifft ausschließlich das gebündelte synthetische Fixture und
die eingefrorenen acht Eingaben. Keine Karriere-/Holdoutfreigabe oder Leistungs-
aussage. Neue native Fehler/Identitätsdrift stoppen den Hauptlauf.

[Technikmessungen](../data/tact-001-p1c/technical.jsonl) ·
[Readback-/A/A-/Negativbelege](../data/tact-001-p1c/technical-summary.json) ·
[Registry](../data/tact-001-p1c/manifest.json) ·
[Abrechnung](../data/tact-001-p1c/job-accounting.jsonl) ·
[Budget](../data/tact-001-p1c/budget.json).

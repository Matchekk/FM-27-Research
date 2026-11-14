# MECH-004-SPLIT-R0 – öffentliche Rohmessungen und Provenienz

Separate NIGHT-002-Studie. [Vorregistrierung](../../experiments/MECH-004-split-preregistration.md)
und [unabhängiger Inputreview](../../docs/night-002/SPLIT004-INPUT-REVIEW.md).
Aktuell: TECH32+1 bestanden; Main nach224 akzeptierten Matches terminal gestoppt.
Keine Leistungsschätzung aus der Teilserie. Alle Rohbelege erhalten,257 echte
Nativeaufrufe bereinigt,545 geplante Plätze bleiben reserviert.
[Technischer Bericht](../../experiments/MECH-004-split-validation.md) ·
[Stoppbericht](../../experiments/MECH-004-split-stop.md) ·
[unabhängiger Abschluss](../../docs/night-002/SPLIT004-TERMINATION-REVIEW.md).

`main-summary.json` und `main-budget.json` geben ausdrücklich keine erfolgreiche
Hauptserie frei; `main-job-accounting.jsonl` enthält alle512 Plätze einschließlich
Fehlern/unbegonnenen Jobs. `native-call-time.json` zählt die tatsächlich257 Calls,
keine imputierten Ergebnisse. Kein `main.jsonl`/Effektarchiv wurde erzeugt.

- `contract.json`: eingefrorener Entwurf mit vier C90/C7A-Armen und Grenzen.
- `inputs.json`: Setup-/Code-/Ressourcen-/Kontrollhashes, tatsächliche Softwareversionen.
- `seed-plan.json`:64 neue Haupt- und vier getrennte Technikseeds; keine privaten IDs.
- `manifest.json`: tatsächlicher Registrierungsbeleg auf erfolgreichem öffentlichen
  Vorregistrierungscommit `0e535dc`, CI43648809178.
- `main-job-plan.json`, `technical-job-plan.json`: vollständige einmalige Jobpläne.
- `review-gate.json`: konkrete unabhängige Inputfreigabe, keine Mainfreigabe.
- `source-preflight-technical.json`: erneuter Quellen-/Patchabgleich vor Technik.

Spätere `technical.jsonl`/`main.jsonl` enthalten nur zulässige Matchstatistiken,
Seed-/Setup-/Buildmetadaten, Auditflags und zusammengefasste Roh-/Cachezustände.
Private Originaldumps, Speicherregionen und Spieleridentitäten werden nicht kopiert.
Fehler, unbegonnene Jobs und Budgetnachweise bleiben separat; keine Nullimputation.

Erst vollständige, erfolgreich bereinigte Mainserie erlaubt die feste Analyse:

```powershell
python -B analysis/report_split004.py
python -B analysis/review_split004.py public-technical
python -B analysis/review_split004.py public-main
```

Die Analyse besitzt einen Primär- und acht Sekundärkontraste, daher576 abgeleitete
Seedkontrastzeilen aus64 unabhängigen Blöcken.512Matches sind keine512Replikate.
Die privaten Reviewmodi sind nur für lokal vorhandene Originalbelege verfügbar;
die öffentliche wissenschaftliche Nachrechnung benötigt keine Spielinstallation.

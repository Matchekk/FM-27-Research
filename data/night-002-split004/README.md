# MECH-004-SPLIT-R0 – öffentliche Rohmessungen und Provenienz

Separate NIGHT-002-Studie. [Vorregistrierung](../../experiments/MECH-004-split-preregistration.md)
und [unabhängiger Inputreview](../../docs/night-002/SPLIT004-INPUT-REVIEW.md).
Noch keine nativen Ergebnisse bei Anlage dieses Indexes.

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

# TACT-001-P0 – publizierbare Pilotbelege

Build `27.0.1+2503222`, Tactics Lab v1114.6. Vorregistrierung
`650a89af4deada6feb4ea1164e3fc963280d90ed`, technische Freigabe vor der Hauptserie
`c9a4353d9ecd61b78bccdadb4a57d613d4e285e3`.

| Datei | Inhalt |
|---|---|
| `seed-plan.json` | 16 Hauptseeds, drei getrennte technische Reservationen, Hash der Ausschlussmenge |
| `inputs.json` | Eigene Phasen/Rollen/PI/Teamoptionen, synthetische Profilregel, 16 binäre Setuphashes, zwei ungespielte Holdouts und Quellhashes |
| `binary-diff-audit.json` | Zwölf Armvergleiche: ausschließlich die vorgesehenen Gruppen-9/10-Records geändert |
| `manifest.json` | Ausführbarer Registry-Receipt mit dem bereits veröffentlichten Vorregistrierungscommit; die originale Spezifikation bleibt eingefroren |
| `technical.jsonl` | 23 akzeptierte technische Matchmessungen |
| `technical-summary.json` | Native Freigabe, sieben exakte Wiederholungen, negative Binärprobe Code 108 |
| `main.jsonl` | 128 vollständige Hauptmatches, 16 unabhängige Seedblöcke |
| `effects.json` | Primär-/Sekundärkontraste, Intervalle, Holm, SD-Obergrenzen und neue Fallzahlplanung |
| `job-accounting.jsonl` | Alle 152 Versuchsplätze: 151 akzeptierte Matches und eine erwartete negative Eingabe; keine fehlenden/unbegonnenen Jobs |
| `budget.json` | Dauerhafte Reservierungen und 108,478/900 Sekunden konservativ verrechnete Wall-Time, einschließlich dokumentiertem Vorbereitungsfehler ohne Matchstart |
| `run-summary.json` | Abschlussstatus, Ausfälle/Ausschlüsse/Retries/Holdouts jeweils null; kein Gewinner ausgewählt |

Rohlogs, vollständige native Dumps, binäre Szenarien und Originalfixture bleiben
privat. Die öffentlichen Zeilen enthalten nur erlaubte numerische Messfelder und
Hashbelege. Der Export prüft Rawlog-, Dump- und Startup-Receipthashes erneut.

Rechenprüfung ausschließlich aus öffentlichen Messungen, ohne FM27:

```powershell
python -m pip install -r requirements-lock.txt
python analysis/verify_tact001p0.py
python -m unittest discover -s tests -v
```

Die unabhängige Prüfung importiert den eingefrorenen Analysator nicht und
reproduziert alle elf Kontraste, t-/Bootstrapintervalle, Holm-Familie,
SD-Obergrenzen und sechs Fallzahlminima. Der Analysator selbst ist zusätzlich
gegen das Effektarchiv und synthetische Referenzdaten getestet.

[Ergebnisbericht](../../experiments/TACT-001-P0-results.md) ·
[Vorregistrierung](../../experiments/TACT-001-P0-preregistration.md).

# TACT-001-P1B – negative Resolution-V-Halbfraction

**Abgeschlossen am14.11.2026:** 2.048 gültige Hauptmatches / 64 unabhängige
Seedblöcke, 72 technische Vollmatches und eine erwartete negative Abweisung.
16 Zellen, vier feste Gegner-/Seitenkontexte, 64 Binärhashes,
67 neue Seeds (64 Haupt-, drei technische Seeds), keine Holdoutausführung.

| Datei | Bedeutung |
|---|---|
| `design-matrix.json` | Explizit E=−ABCD, D00 all-standard, gemeinsame Matrix-SHA |
| `inputs.json` | Vier unveränderte P0-Kontextbeschreibungen, vollständige Faktoroptionen und 64 Zellübersteuerungen/Hashes; keine privaten Spieler-IDs |
| `binary-diff-audit.json` | Alle64 kodierten Eingaben unterscheiden sich ausschließlich in deklarierten fünf Instructionrecords vom jeweiligen D00 |
| `seed-plan.json` | Dauerhafte, gegen Historie/Reservierungen disjunkte 67-Werte-Reservation |
| `historical-archive.json` | 124 historische Forschungsdateien gegen Ausgangscommit, SHA256 Git-kanonische LF-Zeilenenden |
| `manifest.json` | Auf gepushten Vorregistrierungscommit gebundener Registry-Receipt und vollständiger ausführbarer Vertrag |
| `technical.jsonl`, `technical-summary.json` | 72 erlaubte Technikmessungen, 64 Zellen, acht exakte Wiederholungen, Exit108-Negativprobe |
| `technical-gate.json` | Referenz auf den vor Hauptstart gepushten Freigabecommit |
| `main.jsonl` | Alle2.048 erlaubten nativen Rohmessungen einschließlich Endständen, Teamstatistik, Faktorbits und Hashprovenienz |
| `job-accounting.jsonl` | Alle2.121 Matchversuchsplätze; keine fehlgeschlagenen oder unbegonnenen Jobs |
| `effects.json` | Fünf Hauptkontraste, zehn explorative Paar-DoDs und25 sekundäre Tests; Welch-/Bootstrap-/simultane Intervalle und Holm-Familien |
| `block-contrasts.jsonl` | 960 einzelne xGD-Seedkontraste (15×64) für unabhängige Rekonstruktion |
| `candidates.json` | Höchstens zwei explorative Vorschläge nach eingefrorener Regel; konkrete Optionen und vier Setup-Hashes je Kandidat |
| `budget.json`, `resource-summary.json`, `run-summary.json` | Dauerhafte Caps/Deadline, kumulierter Verbrauch, Prozess-/Warmworker-/Artefaktzähler und Vollständigkeit |

1.119,500/2.400 s Child-Wall-Time, 1.474,665/2.400 s Studienzeitfenster.
Keine Ausfälle, Retries, Ausschlüsse oder Ersatzseeds. Keine Siegerbestätigung.
Binärdateien, volle Dumps und Rohspielmaterial bleiben privat.

Reproduktion ohne native Ausführung:

```powershell
.venv/Scripts/python.exe analysis/analyse_tact001p1b.py
.venv/Scripts/python.exe analysis/verify_tact001p1b.py
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

[Vorregistrierung](../../experiments/TACT-001-P1B-preregistration.md) ·
[Vertrag](../../research/specs/TACT-001-P1B.json) ·
[Ergebnisse](../../experiments/TACT-001-P1B-results.md).

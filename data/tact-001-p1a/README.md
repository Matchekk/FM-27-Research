# TACT-001-P1A – abgeleitete Offline-Analyse

14.11.2026. Ausschließlich Wiederverwendung der 128 P0-Hauptmatches / 16
unabhängigen Seedblöcke. **Keine neuen nativen Matches oder Seedreservierungen.**
Alle neuen Auswertungen explorativ; Prognosen beruhen auf benannten Annahmen.

| Datei | Bedeutung |
|---|---|
| `source-manifest.json` | Ausgangscommit, Quell-SHA256, vollständiger technischer Archivaudit, Analysehash, Nullzahl neuer Läufe |
| `exploratory-effects.json` | 30 Effekte, Welch-t-/stratifizierte Bootstrapintervalle, Holm-30, Kontext-/Seitenstreuungen, Armkovarianzen, Endpunktkorrelationen, Sensitivitäten |
| `seed-influence.jsonl` | 96 Leave-one-out-Auswertungen für die sechs xGD-Kontraste; keine ausgeschlossenen Ergebnisse |
| `design-comparison.json` | Kosten, Allokation, Seitenpaarungs-Gegenmodelle, endliche Control-Variate-Kalibrierung, bedingte DoE-/Vollfaktor-/Rundenpräzision und Power |
| `resolution-v-design.json` | Nicht ausgeführte negative Halbfraction E=−ABCD, 16 Zeilen, keine FM-Seeds |
| `next-study-plan.json` | Nicht ausführbarer Planungsentwurf für P1B mit konkreten statischen Katalogstufen und zwei Budgets; fehlende Freigaben/Hashes/Seeds explizit |

Texthashes verwenden Git-kanonische LF-Zeilenenden; Windows-CRLF wird vor SHA256
normalisiert. Engine-/Host-/Fixture-/Ressourcenhashes bleiben Binär-SHA256.
Die Dateien unter `data/tact-001-p0/`, die P0-Vorregistrierung und der alte
Analysecode werden nicht geschrieben oder angepasst.

Reproduktion vom Repositoryroot:

```powershell
.venv/Scripts/python.exe analysis/analyse_tact001p1a.py
.venv/Scripts/python.exe analysis/report_tact001p1a.py
.venv/Scripts/python.exe -m unittest discover -s tests -p test_tact001p1a.py -v
.venv/Scripts/python.exe analysis/verify_tact001p0.py
```

Der Bootstrap-RNG ist ein Analyse-RNG, keine Reservierung/Verwendung eines
FM-Matchseeds. P1A-Bootstrapgrenzen müssen wegen anderer Ziehungen nicht exakt
den alten P0-Grenzen entsprechen; der alte Verifier prüft diese separat.

[Analysebericht](../../experiments/TACT-001-P1A-analysis.md) ·
[Design und Transferplan](../../docs/TACT-001-P1A-design.md) ·
[separater Folgeauftrag](../../experiments/TACT-001-P1B-order.md).

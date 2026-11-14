# TACT-002-R0 – kleiner vorregistrierter ST/AMC-Rollenpilot

Vier eigene Rollenarme CF/DLF×AttackingMidfielder/SecondStriker,D00-Baseline,
zwei bekannte synthetische Discoverygegner,beideSeiten,512Hauptmatches,
64unabhängigeSeedblöcke. Keine D15-Optimierung/Holdouts/Karriere oder Gewinnerwahl.

Vor erstem Vollmatch publiziert: [Vorregistrierung](../../experiments/TACT-002-R0-preregistration.md),
[JSON-Vertrag](../../research/specs/TACT-002-R0.json),Code,`role-manifest.json`,
`inputs.json`,`design-matrix.json`,`binary-diff-audit.json`,
`offline-negative-controls.json`,67 neue reservierte Seeds und Ausschlussmenge.
R00bleibt für alle vier Kontext-/Seitenkombinationen bytegleich P1B-D00.
Private Rohlogs/Binärinputs/PKM/Dumps und Spieleridentitäten bleiben lokal.

Ausführung ausschließlich zentral unterNativeLease.900s kumulierteChild-Zeit,
1800s unverrückbares UTC-Fenster,512Haupt-/33technischeVersuchsplätze,
max4Worker/90s Fortschritt. KeinRetry/Ersatzseed/Exklusion oder1024-Ausbau.
Technik:32Vollmatches/16exakteA/A-Paare,12offlineSchema-Negativproben,
eine native Exit108-Binärprobe. Vollständige Phasen-/Rollen-/PI-/Profilreadbacks.

Nach tatsächlicher Freigabe folgen `manifest.json`,`technical.jsonl`,
`technical-summary.json`,`technical-gate.json`,später`main.jsonl`,
`effects.json`,`block-contrasts.jsonl`,`job-accounting.jsonl`,`budget.json`.
Unvollständige Blöcke erlauben nur technischen Status,keine Teil-Leistungsanalyse.
Der momentane Vorbereitungsstand enthält keine neuen Vollmatchresultate.

Offline-Prüfung:
```
python analysis/verify_tact002r0.py
python analysis/review_tact002.py
```
Beide starten keine native Engine. Der separate Reviewer importiert keinen
Runner,Analyser oder gemeinsame Statistikfunktionen.

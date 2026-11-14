# SET-V0 – eigene synthetische Testdaten und reale Gapdiagnostik

**Keine neuen FM-Matches. Keine native Messfreigabe.**

- `gold-cases.json`: elf selbst verfasste synthetische Vertragstraces mit manuell
  vorgegebenen erwarteten Zählerwerten. Sie sind kein Spielmaterial und keine
  wissenschaftlichen FM-Leistungsergebnisse.
- `gold-results.json`: reproduzierbare Parserausgabe derselben synthetischen Fälle.
  Auch erfolgreiche Fälle behalten `native_validated=false,performance_ready=false`.
- `capabilities.json`: tatsächlicher Implementierungsstand; alle nativen Gates fehlen.
- `native-source-gap.json`: rein lesende Hash-/Diagnosebelege zweier früherer
  VALID-002-Logs und vorhandener Toolquellen. Rawlogs bleiben privat.52Auswahlmeldungen
  an26Ticks sind keine ausgeführten Standardexpositionen; Nenner/Attribution sind null.

[Vertrag](../../experiments/SET-V0-measurement.md) ·
[Parser](../../research/set_v0.py) · [Tests](../../tests/test_set_v0.py).

```powershell
python -m unittest discover -s tests -p test_set_v0.py -v
```

Keine native Runtime/Spielinstallation ist für die zehn Parsertests mit elf Goldfällen erforderlich.
Ein echter Nativeadapter braucht später ein eigenes gehashtes Mapping und native
Goldfallvalidierung. Ein caller-supplied `validated=true` kann V0 nicht freischalten.

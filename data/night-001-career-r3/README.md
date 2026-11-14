# VALID-004-CAREER-R3-DIAG: ausschließlich Offlinevorbereitung

Quelleninventur, Rekonstruktion bereits vorhandener R1/R2-Ledgers und neuer
Diagnosevertragsentwurf. Kein `.fm` wurde geöffnet/gehasht und kein Decoder gestartet.

- `source-audit.json`: AST-/Layout-/APIvergleich, keine ausgeführte Fremdquelle.
- `retained-ledger-audit.json`: rekonstruierte Probeabrechnung und belegte alte JSON-Hashes.
- `planned-ledger.json`: alle fünf künftigen Stufen unbegonnen;0Readerprozesse.
- `R3-draft-contract.json`: Quellen, Grenzen und noch unerfüllte Ausführungsgates.

Kein Saveopener oder Run-Befehl in dieser Stufe. Ein zukünftiger Supervisor
benötigt eigene Implementierung, endgültigen Freeze, Veröffentlichung, Review,
exakte CI und ausdrückliche Directorfreigabe. Private Offsets/Markerbeobachtungen
dürfen selbst nach einer späteren Freigabe nicht in diese öffentlichen Outputs.

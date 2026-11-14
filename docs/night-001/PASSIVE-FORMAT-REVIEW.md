# VALID-005 – separater Review des SVG-Whitespacefixes

14.11.2026. Formatkorrektur nach Veröffentlichung `930d4ac`; keine neue Analyse,
kein neuer Renderbefund und kein neuer nativer Lauf. Der alte
[PASSIVE-SUMMARY-REVIEW](PASSIVE-SUMMARY-REVIEW.md) bleibt unverändert und bindet
weiter seinen damaligen Renderbeleg im archivierten Gitcommit.

Den alten SVG-Gitblob aus `930d4ac` unabhängig gegen die tatsächlich geänderte
Datei geprüft. Die neue Datei entspricht **exakt** der alten Datei nach
CRLF→LF-Normalisierung und Entfernen von Whitespace am Ende jeder Zeile bei
erhaltenem abschließendem LF. Keine andere Byteänderung.

Zusätzlich beide SVGs als XML geparst:966Elemente mit identischen Tags,
Reihenfolge und Attributschlüsseln. Attribut-, Text- und Tailtokens stimmen
überein; sämtliche4667Pfaddatentokens sind identisch. Damit bleiben Geometrie,
Beschriftungen, Werte und Styleinhalt erhalten. Eine erneute visuelle Prüfung
war für diese nachgewiesen reine Whitespaceänderung nicht erforderlich.

`passive-state.json` ist nach LF-Normalisierung byteidentisch mit dem Gitblob
aus `930d4ac`. Die neue Auswerterfassung ergänzt ausschließlich zwei Zeilen nach
`savefig`, die denselben Whitespacefix für zukünftige SVGausgaben ausführen;
die numerische Analyse, Achsen, Datenpunkte und Exportdaten bleiben gleich.
`git diff --check` für die beiden korrigierten Dateien besteht.

LF-normalisierte Hashbindung:

| Artefakt | SHA256 |
| --- | --- |
| Alter SVG-Gitblob930d4ac | `25ba59680eaebf75bb2ca0edf20ce33fdb585669108750ed6df670b52cf3a322` |
| Neuer formatierter SVG | `f52ae8e3a84e7214f4fa7b5aa16888dd0230535681c6e996375f24fb825e1685` |
| Neuer Auswerter | `ee636da52b8a2bee6299abc6bcac855410a2d128da2c07ee8bd31a8f1b8daf97` |
| Unverändertes Daten-JSON | `26da5f3cdfcfa2c5be1eb5ff51fe70968c1cd1278991917dafd4c2f16de70a0c` |

Die zusätzliche Veröffentlichung erklärt den geänderten aktuellen Renderhash,
ohne alte Reviewbelege oder Ergebnisse umzudeuten. Keine UI-Kalibrierung,
Consumer-/Kausalbehauptung, Seedreservierung, Saveaktion oder Nativefreigabe.

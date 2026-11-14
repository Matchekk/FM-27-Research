# TACT-001-P1B – negative Resolution-V-Halbfraction

Vor Hauptstart: 16 Zellen, vier feste Gegner-/Seitenkontexte, 64 Binärhashes,
67 neue Seeds (64 Haupt-, drei technische Seeds), keine Holdoutausführung.

| Datei | Bedeutung |
|---|---|
| `design-matrix.json` | Explizit E=−ABCD, D00 all-standard, gemeinsame Matrix-SHA |
| `inputs.json` | Vier unveränderte P0-Kontextbeschreibungen, vollständige Faktoroptionen und 64 Zellübersteuerungen/Hashes; keine privaten Spieler-IDs |
| `binary-diff-audit.json` | Alle64 kodierten Eingaben unterscheiden sich ausschließlich in deklarierten fünf Instructionrecords vom jeweiligen D00 |
| `seed-plan.json` | Dauerhafte, gegen Historie/Reservierungen disjunkte 67-Werte-Reservation |
| `historical-archive.json` | 124 historische Forschungsdateien gegen Ausgangscommit, SHA256 Git-kanonische LF-Zeilenenden |

Registrierung, technische Belege, Jobabrechnung und Ergebnisse folgen separat
nach den tatsächlichen Phasen. Binärdateien, volle Dumps und Rohspielmaterial
bleiben unter dem ignorierten lokalen Arbeitsverzeichnis.

[Vorregistrierung](../../experiments/TACT-001-P1B-preregistration.md) ·
[Vertrag](../../research/specs/TACT-001-P1B.json).

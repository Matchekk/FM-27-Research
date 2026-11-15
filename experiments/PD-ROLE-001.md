# PD-ROLE-001 – CF/DLF × Sprunghöhe desselben Stürmers

15.11.2026 · Vorregistrierung vor Technik und Hauptmatches. Neues Programm
PLAYER-DEVELOPMENT-001; keine Wiederaufnahme von NIGHT-003.

## Frage, Neuheit und Einheit

`NOVEL_HYPOTHESIS`: Ist der Effekt von JR-Roh60→80 bei genau einem ST unter
DeepLyingForward anders als unter CentreForward? Primär:
`(DLF80−DLF60)−(CF80−CF60)` auf Team-xGD pro Match.
Nutzerklasse ebenfalls `NOVEL_HYPOTHESIS`. Quellenüberlappung MAC-13B,
FM27-PURITY-POS, MAC-12, eigene ATTR-006/007/009 und TACT-002-R0;
[Abgrenzung und heutiger Quellen-/Patchcheck](../docs/player-development-001/LITERATURE.md).
Bekannte Attribut-/Positionshaupteffekte werden nicht neu beansprucht.

## Eingriffe und Kontrollen

| Arm | IP-Rolle am ursprünglichen logischen ST-Slot10 | JR-Rohfeld54 |
|---|---|---:|
| A | CentreForward, Flags2048 | 60 |
| B | CentreForward, Flags2048 | 80 |
| C | DeepLyingForward, Flags1024 | 60 |
| D | DeepLyingForward, Flags1024 | 80 |

Ein identitätsgebundener Starter, beide Seiten gespiegelt; OOP-ST bleibt
OPCentreForward. Gleiche Position, Positionsratings, Spieleridentität, übrige
68 Attribute, sämtliche Profile inkl. CA120, Füße, Körper, Taktik, explizite PI,
Management und Startzustände. Die Rolle mitsamt intrinsischen Anweisungen ist
ein **Rollenpaket**. Keine Behauptung isolierter intrinsischer Einzelmechaniken.
Kein gleicher realer CA-Verbrauch: nominale CA wird konstant gehalten, Kosten
der Attributänderung sind nicht identifiziert. Raw60→80 wird nicht als neu
kalibriertes Karriere-UI12→16 verkauft.

Originales D00-IP4231/OOP4411, 23 aktive Akteure pro Team, unverändertes
synthetisches omnipotentes Positionsprofil. Gegner `high_press` und `deep_block`
sind zwei bekannte feste Discoverykontexte, keine unabhängige Gegnerpopulation.

## Stichprobe, Seeds, Primär- und Sekundäranalyse

2 Rollen × 2 Rohdosen × 2 Seiten × 2 Gegner × 256 neue Seeds je Gegner =
**4.096 Hauptmatches, 512 unabhängige Kontext-Seedblöcke**. Zwei Seiten und vier
Arme bleiben im Block; Seitenmittel, dann gleichgewichtete Kontexte. Disjunkte
4 Technikseeds und 512 Mainseeds, gegen sämtliche Archiv-/Registryreservierungen
geprüft. Keine alten, terminalen oder unbenutzten Seeds werden freigegeben.

Ein zweiseitiger Primärtest α0,05, Welch95 und stratifizierter 20.000-Block-
Bootstrap. Praktische Referenz±0,15 xGD für den Kontrast einer einzelnen
Spieleraufwertung, gewünschte volle KI-Breite≤0,20. Kein automatischer
Äquivalenzschluss aus p>0,05. Fallzahlsensitivität vor Ergebnissen:
`python analysis/analyse_playerdev001.py --planning`, veröffentlicht in
`data/player-development-001-role/planning.json`. SD-Annahmen0,6/1,0/1,2/1,5
sind Sensitivitäten; TACT-002-R0-Rolleninteraktion ist nur Varianzanker.
4.096 ist die feste gesamte wissenschaftliche Programmobergrenze; keine
Interimanalyse, Ergebnisverlängerung oder zweite wissenschaftliche Serie.

Eine Holm6-Sekundärfamilie: Interaktion auf tatsächlichen Punkten, GF, GA,
xGF, xGA und Kontextdifferenz der xGD-Interaktion. Alle KIs marginal.
JR-CF/JR-DLF und marginale Rollen-/JR-Kontraste werden vollständig als
deskriptive Schätzungen berichtet, nicht separat bestätigend getestet oder
zur Kandidatenauswahl genutzt. Kein Ranking, kein Scoutinggewichtsupdate aus
einem einzelnen Fixture. Separate skalare Nachrechnung ohne Tensor-/Haupt-
Statistikfunktionen; gleicher Analyst, kein separater Gutachter behauptet.

## Technische Freigabe und feste Abbruchregeln

Tatsächlich installierte DLL15.11.: FileVersion27.0.1,
ProductVersion27.0.1+2503222, SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Tactics Lab v1114.6/91f2eba, bestehender passiver Observer58e05a46,
vollständige Ressourcen-/Quell-/Katalog-/Host-/Setuphashes im Inputmanifest.
Keine fremden Codeänderungen, neuen Setter oder Parserarbeiten.

Vor Main: alle16 Eingabezellen zweimal (32 vollständige Technikmatches,
16 exakte A/A), eine malformed Exit108-Kontrolle. Pro Call vollständiger
Original-Readback nach Vorbereitung, 3.174 Attribute, 1.058 Profilfelder,
44 Phasenzellen/748 PI-Gruppen und Actor-/Phasen-/Seedbindung; Startkontrollen
an prepared/first_advance. Rollenlegalität nativ und statisch. Unveränderte
Nichtinterventionsfelder und exakte binäre Änderungen0/1/1/2 je Arm.
Erfolgreiche exakte veröffentlichte CI vor Technik und vor Main.

Neue exklusive NativeLease, höchstens4 kalte Worker, bestehendes Job3-
Containment, absolut30s/Call plus begrenzte Bereinigung. 33 technische und
4.096 wissenschaftliche Aufrufe, keine Retries/Ersatzseeds/Ausschlüsse.
7.200s kumulierte beaufsichtigte Phasenzeit, 10.800s unverrückbares Fenster
ab Technikstart. 16GiB neue Rohbelege, 20GiB freier Reserveplatz. Fehlendes
Gate, Build-/Inputabweichung, Ausfall, Cleanupmismatch oder Budgetende stoppt;
Teilserien erhalten ausschließlich technischen Status, keine Wirkungsschätzung.
Unbegonnene/fehlgeschlagene Jobs werden erhalten und abgerechnet. Keine
Komprimierung, Verschiebung oder Löschung laufender Belege. Keine Karriere,
Holdouts oder private Saves. Keine Hintergrundfortsetzung nach Sitzungsende.

## Artefakte und ausführbarer Code

- `analysis/playerdev001.py`: prepare/technical/main, publizierte Hashbindung.
- `analysis/playerdev001_design.py`: deklarierte Rolle-/Attributtransformation.
- `analysis/analyse_playerdev001.py`: vollständige Auswertung und Skalarprüfung.
- `data/player-development-001-role/`: Inputs, Pläne, Seedplan, Messungen,
  Technikfreigabe, Ergebnisse und unabhängige arithmetische Nachrechnung.
- `local/player-development-001/role/`: unveröffentlichte Originalbelege;
  keine privaten Pfade/Identitäten oder geschützten Bytes im öffentlichen Export.

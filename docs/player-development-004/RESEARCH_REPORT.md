# Spielerentwicklung004 – erster echter Karriereverlauf

**Zwischenstand, auf ausdrücklichen Nutzerwunsch pausiert.** Der Code-Zugang ist bewiesen. Im neuen
TRAIN-005-Kontrollarm steigt P001s gespeicherte CA bis zum gesicherten Stopp nach 19 realen Kalendertagen
von 134 auf 135, bei unveränderter PA 160. Alle 47 verwertbaren gerundeten
Attributanzeigen einschließlich Antritt/Tempo 14/14 bleiben bis dahin gleich.
Keine Aussage über einen zusätzlichen Quickness-Fokus ist bereits möglich:
B hat noch keinen Kalenderverlauf, beide 56-Tage-Endpunkte fehlen.

Der frühere technische Blocker wurde mit der bestehenden FM27-Spielthreadbrücke
und eng begrenzten Ergänzungen überwunden. Fokus −1 → 9 / „Schnelligkeit“ wurde
als technischer Eingriff mit separatem Readback nachgewiesen. Reguläres Fortfahren,
Vereins-Pflichtantworten, native Auto-Auswahl, angebotene Sofortergebnisse und
Erzeugung neuer eigener Save-Dateien funktionieren im tatsächlichen Spiel.
Keine externe Matchsimulationsreihe und kein Urlaub als Ersatz.

[Zugang/Fehler](INGAME_ACCESS.md), [Baseline](BASELINE.md),
[Pilotabrechnung](TRAINING_PILOT.md), [anonymisierter Export](PLAYER_DEVELOPMENT.csv),
[maschinelle Auswertung](../../data/player-development-004/analysis.json).
Die Vorregistrierung `095606d4b6beecaec141bc7082a9cb5e8dda74fc` hatte
[erfolgreiche CI](https://github.com/Matchekk/FM-27-Research/actions/runs/43756216213).
Neuere Messstände benötigen ihren eigenen Commit-/CI-Nachweis vor Mainintegration.

Die Daten stammen aus **einem** gemeinsamen Karrierecluster und **einem** Spieler.
Fünf A-Zeitpunkte sind keine vier unabhängigen Replikate. Keine Konfidenzintervalle,
p-Werte oder Trainingsrangliste. CA/PA stammen aus einem aktuellen nativen
Spielerobjekt mit unabhängig abgeglichener UI-Identität; keine MODEL_RCA- oder
EDITOR_RCA-Validierung. Das beobachtete +1 CA erlaubt keine Zuordnung zu einem
bestimmten Attribut und keine Behauptung kostenlos trainierbarer Attribute.

Der zukünftige Achtwochenplan wurde nicht vollständig eingefroren. Automatisch
entstehende Intensitäts-, Minuten-, Verletzungs- und Planunterschiede begrenzen
eine isolierte kausale Interpretation. Die tatsächliche Einheitenteilnahme ist
NOT_MEASURED. Verborgene Persönlichkeit, Trainerqualität und Meta-Score werden
nicht durch Schätzwerte ersetzt. Die frühere 51-Pläne-Auswertung wurde nicht
nochmals als neue Evidenz verwendet.

Die Originaldatei bleibt erhalten; alle Saves, Namen, konkreten Spieler-IDs,
Speicheradressen und vollständigen Profile liegen außerhalb Git. Öffentlich
stehen pseudonymisierte Messungen und Hashes privater Originalbelege. Mehrere
kontrollierte Neustarts, technische Setter-/Bestätigungsfehler und ein verworfener
falscher Kaderzeilenabruf bleiben in der privaten Befehlsabrechnung sichtbar.
Der Abschluss dieses Arbeitsabschnitts ist in
[shutdown.json](../../data/player-development-004/shutdown.json) abgerechnet:
759 Ledger-Einträge (752 completed, 7 stopped), rund 571 MB private Artefakte
zum Abrechnungszeitpunkt, ein begonnenes und kein abgeschlossenes Karrierepaar.
Diese technischen Zahlen sind keine wissenschaftliche Stichprobengröße.
FM und Controller sind beendet; temporäre installierte Änderungen restauriert.
A ist am 04.02.2027 gesichert, B und Original bleiben bytegleich zur Quelle.
Keine personenbezogenen Saves, DLLs oder Rohinventare wurden veröffentlicht.


Lokale Validierung: 480 Repository-Tests, drei vorgesehene Skips; fünf weitere
Analysetests bestanden. Drei neue konkrete Prüfungen schützen insbesondere
vor Spieler-/Armverwechslung, falschem Follow-up und Nullersatz für Missing.
Der geprüfte vorherige Datencommit `c5cd439dabb6cd98dbbefeaee873053b196f1ea0`
hat [grüne CI](https://github.com/Matchekk/FM-27-Research/actions/runs/43762298121).
Der gesicherte 19-Tage-Stopp wird erst nach eigener grüner CI nach main integriert.

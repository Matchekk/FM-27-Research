# MECH-003-STAMINA-R0: Technik bestanden, terminaler Stop vor Main

Aktueller Stand:32technische Vollmatches/16exakteA/A-Paare sowie insgesamt
2Loaderchecks,1Capabilitycheck und1erwarteteNegativabweisung bestanden.
512wissenschaftliche Hauptmatches plus2Mainprobes unbegonnen. Das eigene
Budget ist wegen fehlender rechtzeitiger Ressourcen-/CI-Zulassung geschlossen;
Frist und Zähler wurden nicht erweitert. Keine Leistungsschätzung.
[Ergebnis und Stopgrund](../../docs/night-001/STAMINA-TECH-RESULTS.md),
[unabhängiger Rohreview](../../docs/night-001/MECH003-TECHNICAL-REVIEW.md),
[Budgetreview](../../docs/night-001/MECH003-STOP-REVIEW.md).
`technical.jsonl` erhält32Messungen, `job-accounting.jsonl` sämtliche550Plätze,
`administrative-stop.json` den terminalen Stop. Private Rohlogs bleiben lokal.

## Ursprüngliche Offlinevorbereitungsstufe

`contract-draft.json` ist der maschinenlesbare wissenschaftliche Vertrag mit noch
leeren Identitäts-, Setup-, Ausführungs- und Commitfeldern. Die einzige Vertrags-
factory im Runner erzeugt nach zentralen Gates den konkreten `contract.json`.
Der Entwurf kann keine ausführbare Registrierung ersetzen.

`offline-preparation.json` dokumentiert einen rein lesenden Abgleich mit16 bereits
vorhandenen D00-Intentionen/Binäreingaben: genau10 Attributänderungen je Zelle,
zusätzlich eine Pressingänderung in den acht MoreOften-Zellen. Keine eigenen
Nativeencoderaufrufe oder Engine-Readbacks. Er enthält weder neue Seeds noch
Spieleridentitäten, geschützte Bytes oder private Pfade.

Noch keine neuen Matches, Seedreservierungen, Hauptmessungen oder Effektschätzer.
Die technischen Gates stehen offen. Später darf ausschließlich der zentrale
Director neue Belege ergänzen; bei Abbruch wird jede der550 vorgesehenen Stellen
als abgeschlossen, begonnen/ungeklärt, fehlgeschlagen oder unbegonnen abgerechnet.
Private Rohlogs/Dumps bleiben außerhalb Git. Öffentliche Effekte sind nur nach
vollständig gültigen512 Hauptmatches und bestandenen Gates zulässig.

[Vorregistrierung](../../experiments/MECH-003-stamina-preregistration.md) ·
[Technischer Status](../../docs/night-001/STAMINA.md).

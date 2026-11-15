# NIGHT-002 – eigenständige Forschungsmission

Beginn14.11.2026, Ausgangscommit062fa7e. Frist15.11.2026 08:00Europe/Berlin.
Der eingefügte Nutzerauftrag ist die Autorisierung; keine NIGHT-001-Verträge
werden verlängert. [Konsolidierter Bericht](OVERNIGHT_REPORT.md).

**Abschluss15.11.2026:** TACT-003 mit512 gültigen Hauptmatches/64 Blöcken
vollständig und unabhängig nachgerechnet. Konkreter IP-Paketeffekt−0,350xGD,
Holm7-p0,000162; primäre Moderation unklar. MECH-004 bleibt nach224 akzeptierten
Mainmatches terminal ohne Leistungsanalyse. Alle Belege restauriert/überprüft,
alle alten Reservierungen/Zeitwerte erhalten. Die geprüfte administrative
Transition erlaubte ausschließlich die andere TACT-Frage. Kein MECH-Retry,
keine Livearchivierung in TACT und keine weiteren nativen Serien dieser Mission.
[Vollständige Ergebnisse](../../experiments/TACT-003-stless-results.md).

## Forschungsentscheidung und Architektur

[Aktueller Primärquellenaudit](LITERATURE_AUDIT.md),
[maschinenlesbare Quellenbelege](../../research/night002-source-audit.json) und
[zehn Kandidaten/beste drei](NOVELTY_MATRIX.md) bestimmen die Auswahl.
Die erste separate Studie ist [MECH-004-SPLIT-R0](../../experiments/MECH-004-split-preregistration.md):
unabhängige Rohfeldübertragung vor jeder Leistungsschätzung.

Vorhandene Datenkette: ursprünglicher Recordcodec → private D00-Eingaben →
unveränderter nativer Host mit passivem Observer → identitygebundene Auditlogs →
sanitisierte öffentliche Matchzeilen → gepaarte Seedblockanalyse → unabhängiger
Review. Neue Dateien ergänzen ausschließlich den Splitkontrast und den eigenen
NIGHT-002-Ressourcenvertrag. Alte Daten, Runner und API-Verträge bleiben erhalten.

Betroffene Grenzen: `split004_design` kompiliert/auditiert zwei getrennte Felder;
`run_split004` hält die konkrete Studienfreigabe, Quellen-/Inputhashes, CI,
Jobplan und Bereinigung ein; `night002_control`/`night002_supervise` koordinieren
die neue Mission mit globaler Exklusivlease. Statistik verwendet die vorhandenen
geprüften Blockmethoden. Keine neue native Engine, kein Save-Executor und kein
UI-Steuerungspfad werden eingeführt.

Meilensteine: (1) Literatur/Entscheidung und geprüfte Offlinevorbereitung;
(2) publizierte Vorregistrierung, unabhängiger Inputreview und CI;
(3) technische Transfer-/A/A-/Negativserie mit eigener Freigabe;
(4) nur bei bestandenen Gates Mainpilot, unabhängige Auswertung und Veröffentlichung;
(5) verbleibende unabhängige Fragen nach Erkenntniswert und Restbudget auswählen.

## Budgets und Grenzen

Mission:≤2048Main,≤192technische Vollmatches,≤3600 beaufsichtigte
Childsekunden,≤4GiB neue private native Artefakte; maximal vier kalte Worker,
genau eine globale NativeLease. Die Negativprobe wird konservativ als zusätzlicher
technischer Budgetplatz reserviert. Studie enger:512Main,32Technik+1Negativ,
900Childsekunden/5400s feste UTC-Studienfrist,2GiB. Native Vorbereitung0.
Quelle: [Vorregistrierung](../../experiments/MECH-004-split-preregistration.md)
und [Sicherheitsprüfung](SAFETY_ASSESSMENT.md).

Kein Kalenderadvance, keine echten Karriereänderungen, keine Wiederaufnahme
terminal geschlossener Experimente, keine alten oder gehaltenen Seeds.
Öffentliche Hashes/Statistiken enthalten keine privaten Identitäten/Dumps.

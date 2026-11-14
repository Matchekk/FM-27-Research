# Karriereforscher: R3-Diagnosevorbereitung und TRAIN-Lücken

Eigener Branch `codex/night-career-r3`, Basis `4d2261fa661f1645cda30503e83683394aa37a12`.
Fachagent hat ausschließlich Quellen und erhaltene JSON-Belege gelesen.
Null Saveöffnungen/-hashes, Decoderstarts, native Starts, Seeds und Advances.
R0, eingefrorene R1/R2-Verträge und deren Daten bleiben unverändert.

[R3-DIAG-Vertrag](../../experiments/VALID-004-career-readonly-R3-DIAG.md) registriert
eine mögliche eng begrenzte künftige Fehlerortdiagnose. Implementiert sind ein
passiver äußerer Exception-Observer und eine ausschließlich offline arbeitende
Quellen-/Ledger-CLI. **Ein echter Save-Supervisor ist bewusst noch nicht
implementiert und diese Stufe ist nicht ausführungsfreigegeben.**

Statische Eingrenzung: identische Selectiongrammatik bis einschließlich des
Taker-Markers bei vendortem und offiziellem Reader; identische geerbte drei
3Byte-Marker. V10 nennt keine Markerüberschreibung. Die spätere Countflagänderung
in0.12.4 ist kein Beleg einer Ursache des vorherigen Fehlers. Eine andere reale
Markerfolge, vorheriger Cursorversatz oder falsche Blockgrenze bleiben offen.
Die intern abgefangenen Fehlkandidaten der Blocksuche bleiben unangetastet.

Alle24 alten öffentlichen Probezeilen wurden aus den privaten Ereignisledgers
rekonstruiert. Der neue Audit reproduziert vier Trainingsrecords mit155gespeicherten
Wochen,1085Tagen und3255Slots. [TRAIN-API-Lücken](TRAIN-API-GAPS.md) belegen anhand
der offiziellen Modelle/Methoden, weshalb dies weder individuelle Teilnahme
noch Coach-, Fokus- und Intensitätsbelege liefert. Keine neue Trainingswirkung.

Prüfungen: zehn neue synthetische Tests bestanden; insgesamt230Repositorytests
geprüft, davon229bestanden und eine vorhandene Auslassung; fünf historische Analysetests
bestanden. NIGHT-001-Archivschutz bestätigt340unveränderte Dateien. Original-
Returnobjekt/Argumente/Exceptionidentität, interne verworfene Kandidaten, Bounds,
überbreite Marker, fehlende Evidenz und verbotenes `.fm`-Hashing wurden geprüft.
Keine echte Exceptionframeaufnahme aus dem Save; sämtliche Observertests synthetisch.

Nächster separater technischer Meilenstein wäre ein eigener serieller R3-Supervisor
mit Einmalmarker, Lease, hartem180s-/3GiB-Budget, Vor-/Nachhash, Ressourcen- und
Crashledger. Danach endgültiger Freeze, Veröffentlichung, unabhängiges Review,
exakte erfolgreiche CI und ausdrückliches Director-Proceed. Keine automatische
Ausführung aus diesem Bericht. Fachagent erstellt nur lokalen Commit, keinen Push.

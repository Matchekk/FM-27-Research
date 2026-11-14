# VALID-004-CAREER-R3-DIAG: separater Ausführungsvertrag

Status: **Supervisor implementiert und offline geprüft; kein echter R3-Pass**.
Dieser neue Vertrag konkretisiert den unveränderten
[R3-Entwurf](VALID-004-career-readonly-R3-DIAG.md). Er ersetzt weder alte
Vorregistrierungen noch R0/R1/R2-Ergebnisse. Freigabe, Veröffentlichung, exakte CI
und unabhängiges finales Runnerreview stehen vor jeder echten Ausführung.

## Frage, Einheit und Eingaben

Primär ist genau eine begrenzte Positions-/Erwartungsaufnahme am final nach außen
propagierten Set-piece-Markerfehler des offiziellen Taktikreaders. Kein Reparatur-,
Wirksamkeits- oder Bestätigungsexperiment. Eine gespeicherte Testkarriere zählt
als ein unveränderter Datengegenstand, nicht als unabhängiges Replikat.
Keine statistische Hypothesentestfamilie, Fallzahl-/Powerbehauptung oder Taktikauswahl.

Einzige zulässige Datei ist die bereits bestehende private R0-Snapshotkopie:
147.130.636Bytes, SHA256
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
Keine neue Originalaufnahme oder andere Karriere. Ihr bekannter Last-writer-Claim
ist `27.0.1+2503222`, Tactics-Schema26. Diese Saveclaims sind keine neue Aussage
über installierte Engineidentität oder native Feldsemantik.

Reader: privat isoliertes offizielles fmsave0.12.4, unveränderter Wheelhash
`2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa`,
Releasecommit `e0704bc5d7e6bf687fecf85cd48b28c497bdef68`.
Alle86 offiziellen Pythonquellen müssen dem eingefrorenen R2-Inventar entsprechen.
Kein V10-/Draft-/Hostimport, keine alternativen Layouts oder zusätzlichen Probes.
Basis-fmsave0.9.0, Basisinterpreter, backports.zstd1.8.0 einschließlich Python-/Pyd-
Code und Distributionsmetadaten bleiben gehasht und unverändert. Ein falsches
Versionslabel, Paket-/Sourceupdate oder unbemerkte Bytecode-Cachemutation ist
kein zulässiger Vorbereitungsschritt; Decoder startet explizit mit `-I -S -B`.

Runner-v2 bindet auch das tatsächlich importierte `research/__init__.py`.
`-B` verhindert ausschließlich neue Cachewrites, keine vorhandenen Cacheimporte.
Deshalb erhalten Parent vor den ersten Researchimports und Childbootstrap vor
`runpy`, Siteeinbindung und Projektimports jeweils einen frischen privaten
UUID-`sys.pycache_prefix`, dessen sichere Lage und Nichtexistenz geprüft werden.
`sys.dont_write_bytecode=True`; die Prefixverzeichnisse werden nicht angelegt.
Bestehende globale Caches werden weder gelöscht noch verändert. Parent wird als
direkte Quelldatei gestartet; bereits durch Startuphooks vorgeladene Researchmodule
verhindern diesen CLI-Einstieg. Ein Cachefund allein ist kein Tampernachweis.

## Getrennte technische Freigabe

[final-contract.json](../data/night-001-career-r3/final-contract.json) bindet dieses
Dokument, den ursprünglichen Entwurf, den Runner, seine Tests, alle tatsächlich
importierten Forschungshelfer und die bisherigen Quellen-/Paketverträge. Eigene
Textquellen werden für Git-Checkouts vonCRLF aufLF normalisiert gehasht; Fremdcode,
Wheel, Interpreter und Binärabhängigkeit behalten rohe SHA256.

`run` ist ausschließlich im zentralen Checkout zulässig. Vor Snapshot-I/O und
`Popen` müssen alle folgenden Gates bestanden sein:

1. Unveränderte Quellen, Quelleninventare, Pins und exakte Budget-/Dateiidentität.
2. Veröffentlichter vollständiger Commit auf dem vorgesehenen GitHub-Remote;
   veröffentlichter Vertrag/Code/Prereg müssen den lokalen Hashes entsprechen.
3. Abgeschlossener erfolgreicher GitHub-CI-Lauf auf genau diesem Commit-SHA.
4. Neues finales Review in `docs/night-001/CAREER-R3-RUNNER-REVIEW.md`, dessen
   veröffentlichte Fassung den exakten normalisierten SHA256 des finalen Vertrags
   nennt. Ein Review des Offlineentwurfs allein genügt nicht.
5. Eigene private Directorfreigabe mit `passed=true`, exakt diesem Experiment,
   `director_proceed="published proceed"`, Commit/CI und finalen Review-/Vertragshashes.
6. Ausreichend Restzeit vor der unveränderlichen Nachtdeadline und kein früheres
   privates R3-Verzeichnis. Ein vorhandener Versuch oder auch ein partieller
   Ordner sperrt Wiederholung und Überschreiben.

Erst danach werden ReaderLease und persistenter Einmalmarker angelegt. Child
verifiziert Parent-/Lease-/Launch-PID, GO-Zulassung, Vertragsidentität und Quellen
erneut, bevor es die Snapshotdatei berührt. Die CLI bietet keinen alternativen
Savepfad, keinen Seedparameter, keine erweiterbare Matchzahl oder Budgetanhebung.

Vor dem ersten Inhaltslesen von `--release` wird dessen tatsächliches Ziel
aufgelöst und auf den festen privaten Bereich `local/night-001-career/releases/`,
Suffix `.json` und Größe1..65536Bytes begrenzt. Andere Pfade, Savepfade, übergroße
Metadaten und Symlinkziele außerhalb dieses Bereichs werden ohne Inhaltslesen
abgelehnt. Keine Dateiumbenennung oder Save-Neukodierung als Freigabemetadaten.

## Ablauf, Fehler und Ressourcen

Fünf feste Stufen:

1. Veröffentlichungs-, Quellen- und Directorgates.
2. Snapshotvorhash und exakte Bytegröße.
3. Einmal `fmsave.open(..., strict=True)` und Prüfung der bekannten Saveclaims.
4. Einmal `observe_final_call(save.tactics, original_read_selection_part, receipt)`
   an der äußeren Aufrufgrenze. Keine Fremdfunktion wird ersetzt. Identische
   Argumente, Rückgabe oder Exception bleiben erhalten; die Originalexception
   wird privat als Traceback protokolliert und der Taktikschritt als fehlgeschlagen
   abgerechnet. Interne abgefangene Kandidatenfehler sind keine finalen Fehler.
5. `Save.close`, soweit ein Objekt zurückgegeben wurde, und Snapshotnachhash.

Alle Savezugriffe einschließlich Vor-/Nachhash befinden sich im **einzigen
tatsächlichen Decoderprozess**. Der Supervisor berührt keinen Save. Ein kleiner
`-I -S -B`-Bootstrap importiert vor GO keine Projekt-/Readerquellen und liest nur
ein begrenztes privates stdin-Paket. Parent weist zuvor einen eigenen Windows-Job
zu und prüft dessen Mitgliedschaft, Kill-on-close, Ein-Prozess-Grenze und beide
Speicherlimits. Fremde Prozesse und die FM-Anwendung werden nicht angefasst.

Exklusiver globaler ReaderLease, insgesamt180s je einmaligem Versuch und3GiB
harte Prozess-/Job-Private-Memory. Der Decoder erhält höchstens175s ab dauerhaftem
Startmarker;5s bleiben für Cleanup und Abrechnung. Start nur mit185s Puffer vor
`2026-11-14T23:00:00Z`. Keine Zeitrückerstattung und kein neuer Versuch nach Fehler.
OS-/I/O-Verzögerungen über180s bleiben ausgewiesene Budgetfehler, keine gültigen
Diagnoseergebnisse.

Unmittelbar vor GO werden beide Uhren erneut geprüft. Die effektive Decoderfrist
ist das Minimum aus Start+175s und aktueller Monotonzeit plus verbleibender
UTC-Zeit minus5s Cleanupreserve. Ohne positive Restzeit wird kein GO gesendet.
Die laufende Schleife prüft zusätzlich die absolute UTC-Grenze mit5s Reserve;
ein Uhrsprung oder verspätete Jobvorbereitung darf Mitternacht nicht umgehen.

Höchstens1MiB neue private Artefakte. Bekannte Writer sind vor Schreibbeginn
enger partitioniert: Parentmetadaten128KiB, Childmetadaten256KiB,
Stufenledger64KiB, stdout/stderr64KiB. Diese Summe liegt unter1MiB. Ein begrenzter
Pipewriter speichert auch bei übermäßigem Childoutput höchstens64KiB und setzt
einen expliziten Truncationfehler; der Supervisor beendet darauf den Job.
Zusätzlich überwacht er die gesamte Verzeichnisgröße. Der endgültige Bytezähler
schließt seine eigene Completiondatei ein. Keine großen Dumps/Tabellen/Rawbytes.

Die ursprüngliche Grammatik und alle Upstreamgates bleiben aktiv. `UnknownBuildWarning`
wird erwartet und belegt keine Freigabe. Öffentlich technisch gültige Fehlerort-
Diagnose erfordert genau diese eine Warnung; zusätzliche/trunkierte Warnungen,
falsche Eingaben, andere Exception, Drift, unvollständige Belege, Zeit-/Artefakt-
überschreitung oder ungültige Ledgerzeilen verhindern diesen Status.

Jeder Ausnahmefall stoppt die fachliche Folge. Close und Nachhash werden auch nach
Taktik-/Readerfehler versucht; bei nicht bestandener initialer Identitätsprüfung
erfolgt kein weiterer Snapshotzugriff. Bei hartem OS-Kill sind finally-Belege
möglicherweise nicht vorhanden: dann Missing, kein Ersatzread. Fehler beim
Ledgerabschluss verhindern Close/Nachhash nicht absichtlich und bleiben erhalten.

Der eingefrorene native Cleanuphelfer wird nur über einen eigenen Analyseadapter
verwendet. Seine öffentlichen nativen3..10-Prozess-Freigaberegeln werden nicht
aufgeweicht. Der Reader benötigt eigenen Proof: Flags0x2308, Prozesslimit1,
beide3GiB-Caps, tatsächlich beendeter Decoder, finaler Policyreadback und
Kernel-Active-Process-Count0 **vor** Schließen des Jobhandles. Kill-on-close allein
beweist keinen leeren Job. Fehlt dieser Beleg, bleibt die exklusive Lease erhalten;
keine automatische Wiederaufnahme oder manuelle Leasebereinigung durch den Runner.

## Auswertung und Veröffentlichung

Das Ledger erhält alle fünf Stufen, Fehlversuche, unaufgelöste Starts,
unbegonnene Stufen, ungültige/überbreite Belege und fehlende Abschlussreceipts.
Vorhandene Daten werden nicht repariert. `export` liest ausschließlich erhaltene
Artefakte, startet keine Prozesse, öffnet/hasht keinen Save und räumt keine Lease auf.

Privat bleiben absolute Abschnittsoffsets, Cursor, begrenzte Markerbelege,
Warnungstexte, Tracebacks und lokale Pfade. Diese neue Run-Spezifikation erlaubt
gegenüber der engeren Draftbeschreibung zusätzlich öffentliche **abgeleitete
Bereichszählwerte**: Blockbytezahl, Cursordezil im Block und obere Zweierpotenz
der verbleibenden Bytes sowie begrenzte Markerbreiten-/Gleichheitsbooleans.
Keine absoluten Offsets oder Rohwerte werden exportiert. Dies ist eine explizite
Publikationskonkretisierung des neuen Auftrags, keine Parseränderung.

Öffentlich nur feste Status-/Fehlercodes, anonyme Zählwerte, geprüfte Boolwerte,
Hashes und obige begrenzte Aggregate. Rohbytes, Personen-/Spieler-IDs, Namen,
Fremdobjektrepräsentationen, freie Strings und private Pfade sind ausgeschlossen.
Jeder unvollständige/malformed Beleg bleibt Missing beziehungsweise invalid;
keine stillen Nullen. Eine erfolgreich erfasste erwartete Exception bedeutet
lediglich Fehlerortdiagnose, keinen erfolgreich gelesenen Taktikdatensatz.

Native Taktik-/IP-/OOP-Wirksamkeit, Trainingsteilnahme, Coach-/Fokus-/Intensitäts-
bindung, Karriere-RNG, Replay, Kalenderadvance und alle wissenschaftlichen
Leistungsbehauptungen bleiben gesperrt.0Native/Seeds/Kalender, keine Hauptstudie.
Nach einem tatsächlichen Pass erneut unabhängiges Ergebnisreview und dann stoppen.

# VALID-004-CAREER-R3-DIAG: strenger Markerdiagnoseentwurf

Status: **Offlinevorbereitung; kein ausführbarer Save-Supervisor, keine Freigabe**.
Neue diagnostische Teilstufe von [VALID-004 Phase 1](VALID-004-test-fm-research.md).
Kein R1-/R2-Retry. Deren unveränderte [Messungen und Grenzen](../docs/night-001/CAREER-R1-RESULTS.md)
bleiben eigenständige archivierte Ergebnisse. Diese Vorbereitung liest nur
Pythonquellen und bereits gespeicherte JSON-/JSONL-Belege, keine `.fm`-Datei.

## Forschungsfrage und vorhandener Beleg

Primär: Liefert genau ein künftiger begrenzter Diagnosepass am nach außen
propagierten Taktikmarkerfehler eine eindeutige Cursor-/Blockgrenze und die
Gleichheitsresultate der bereits registrierten Marker an genau diesem Cursor?
Keine alternative Grammatik, Taktikbewertung oder Trainingswirkung.

Vorhandener R2-Fehler: `ReaderCheckError` beim erwarteten Set-piece-Marker in
`tactics_man`. Die gespeicherte Fehlermeldung passt zur eingefrorenen offiziellen
Funktion `_read_selection_part`. R2 hatte vier Trainingsrecords gelesen und danach
abgebrochen; sechs weitere Probeplätze sind unbegonnen. R1 scheiterte bereits am
nicht unterstützten Trainingheader, hat also keine Taktikprüfung geliefert.
Ein Fehlerstring enthält keinen Cursor und beweist weder neue Markerbytes noch
eine konkrete Layoutreparatur. Ein falsch bestimmter Block oder ein vorausgehender
Cursorversatz bleibt neben einer Markeränderung möglich.

Einheit: genau eine bestehende Snapshotdatei, keine unabhängigen Replikate,
keine statistische Effektschätzung, Powerplanung oder Mehrfachtestfamilie.
Sekundär: Quellenidentität, Warnungen, Ressourcen und vollständige Abbruchabrechnung.

## Statische Eingrenzung

Der offizielle0.12.4-Pfad übernimmt seine drei jeweils3Byte breiten Taker-Marker
vom FM26-Basislayout. FM27 ersetzt den Selection-Endmarker, diese Taker-Marker
jedoch nicht. Das ist eine nachvollzogene Deklaration, keine bewiesene Gültigkeit
für unseren Savebuild `27.0.1+2503222`/Tactics-Schema26.

Vendorter Reader und offizieller Reader haben denselben AST bis einschließlich
der Markerprüfung. `_read_text`, `_read_selector_list`, `_block_starts` und
`_stored_block_starts` sind ebenfalls AST-gleich. Die gesamte Selectionfunktion
ist nicht identisch:0.12.4 erfasst zusätzlich einen späteren Countflag-Befund.
Diese nachgelagerte Änderung erklärt den vorangehenden Markerfehler nicht.

V10 erweitert unter anderem Buildregistrierung, Taktiksignaturen, Stiltextlänge,
Blockerkennung und sekundäre Slotmaps. Seine eingefrorene Kompatibilitätsdatei
enthält keine Taker-Markerüberschreibung. Deshalb ist V10 weder als bestätigte
Reparatur dieses Fehlers noch als gleichwertige Taktikfreigabe anzusehen.
Unterschiedliche Blockerkennung könnte dennoch Cursor-/Grenzkontexte beeinflussen.

## Transparenter Observer

`research/career_diag004r3.py` ersetzt keine Fremdfunktion. Ein äußerer Wrapper
ruft die unveränderte Operation mit denselben Argumenten auf und liefert deren
identisches Rückgabeobjekt oder wirft dieselbe Exception weiter. Nur nach einer
**final nach außen propagierten** passenden Exception wird deren exakt über
Codeobjekt identifizierter `_read_selection_part`-Frame inspiziert.

Das ist wesentlich: `_stored_block_starts` probiert intern Kandidaten und fängt
deren `ReaderCheckError` selbst ab. Solche verworfenen Kandidaten sind kein
finaler Fehler; der neue Observer darf diese Suche weder instrumentierend stoppen
noch Ergebnisse daraus als endgültige Markerfehler ausgeben.

Maximal64 Tracebackframes, genau ein Zielcodeframe, maximal vier Marker mit
höchstens16Bytes. Nur der bereits vorhandene Cursor wird verglichen. Privat:
Abschnittslänge, Start-/Endoffset, Cursor, verbleibende Bytes, Markerindex/-breite,
Bereichs- und Gleichheitsbooleans. Keine Rawbytes, IDs, Labeltexte, Rohdump- oder
Nachbarmarkersuche. Ungültige oder mehrdeutige Frames werden als Observerfehler
markiert; die Originalexception bleibt erhalten. Ein Capturefehler darf keine
erfolgreiche Diagnose vortäuschen. Keine Defaults, Recovery oder weiteren Probes.

## Verbindliche Voraussetzungen eines späteren Einzelpasses

[R3-draft-contract.json](../data/night-001-career-r3/R3-draft-contract.json) bindet
Quellen, offizielle Paketidentität und Snapshotclaim. Die vorhandene CLI bietet
**ausschließlich `prepare`**, keinen `run`-Befehl und keinen Saveopener.
Ein tatsächlicher Supervisor ist ein weiterer klar abgegrenzter Meilenstein und
muss vor dessen Veröffentlichung/finaler Registrierung vollständig implementiert,
unabhängig geprüft und erneut eingefroren werden. Der jetzige Entwurf genügt
ausdrücklich noch nicht zur Ausführung.

Vor dem künftigen Pass zwingend:

1. Derselbe bereits vorhandene R0-Snapshot,147.130.636Bytes, SHA256
   `1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
   Keine neue Originalaufnahme, kein anderer Save, kein R1-/R2-Ausgabeverzeichnis.
2. Offizieller0.12.4-Wheelhash und sämtliche Quellen unverändert; R1/R2-Manifeste
   dürfen nicht angepasst werden. Direkter tatsächlicher Interpreter, kein
   Windows-Venv-Redirector als Decoderprozess.
3. Vorab veröffentlichter endgültiger Vertrag/Code, erfolgreicher GitHub-CI-Lauf
   auf genau dessen vollständigem SHA, unabhängiges veröffentlichtes Review und
   ausdrückliches Director-`published proceed`. Diese Freigabe ist separat von R2.
4. Eigener exklusiver Reader-Lease und dauerhafter Einmalmarker. Ein tatsächlicher
   Decoderprozess,180s Gesamtbudget,3GiB harte Prozess- und Job-Private-Memory-
   Grenzen, Kill-on-close, maximal1MiB neue private Diagnoseartefakte,0Retries.
   Spätester Start mit185s Puffer vor `2026-11-14T23:00:00Z`.
5. Vor-/Nachhash des Snapshots und Quellen; Drift, Hardlimit, Warnungs-/Messlücke
   oder Eingabefehler stoppen und sperren die betroffene Interpretation. Kein
   Folgeversuch, kein Ersatzlayout, kein stiller Nullwert.

Geplanter enger Ablauf: Gatebeleg → Snapshotvorhash → `open(strict=True)` → genau
ein äußerer `tactics()`-Aufruf mit passivem Observer → Close/Nachhash und Abrechnung.
Der unveränderte Taktikaufruf benötigt intern verwalteten Club, Clubs und Spieler;
diese Abhängigkeiten bleiben vollständig den bestehenden Upstreamgates unterworfen.
Training, Staff, Verletzungen, Kalender und weitere API-Probes sind nicht geplant.
Alle Warnungen bleiben privat vollständig erhalten und öffentlich kategorisiert.
Keine `strict=False`-Option und keine gezielte Wiederholung interner Teilparser.

Das vollständige [Fünf-Stufen-Ledger](../data/night-001-career-r3/planned-ledger.json)
beginnt mit fünf unbegonnenen Stufen. Gestartet, fehlgeschlagen, blockiert,
unaufgelöst und unbegonnen bleiben erhalten. Ressourcen fehlen nach Crash als
Missing; sie werden nicht aus Stageevents als0 rekonstruiert. Öffentliche
Diagnoseoutputs beschränken sich auf Status, Counts, Limits und Quellen-/Beleghashes;
Cursor/Offsets und Markerbooleans bleiben privat. Jeder reale Versuch erhält
eigene neue Outputs, auch wenn der ursprüngliche Fehler erneut auftritt.

## Interpretation und aktueller Stand

Maximal erreichbar wäre ein begrenzter struktureller Fehlerortbefund. Kein
Nachweis nativer Taktikinterpretation, IP/OOP-Bindung, aktiver Taktik, SET-Wirkung,
Karriere-Replay, Kalenderadvance, RNG-Unabhängigkeit oder Trainingsteilnahme.
Alle entsprechenden Releaseflags bleiben false. Null Seeds, native Starts und
Kalenderfortschreibungen. Keine Source-/Paketmutation.

Die Offlinevorbereitung rekonstruiert alte öffentliche Probezeilen aus privaten
JSON-Ledgers, hasht nur Quellen/JSON und erzeugt einen neuen Quellenvergleich.
Der Reader wird dabei nicht importiert oder ausgeführt. Die [TRAIN-API-Lücke](../docs/night-001/TRAIN-API-GAPS.md)
trennt gespeicherte Wochen/Sessioncodes von individuellen Expositionsbelegen.

# VALID-004-R3-DIAG: unabhängiger Ergebnisreview

Stand 2026-11-14. **Der einmalige echte Diagnosepass ist vollständig abgerechnet;
der erwartete finale Markerfehler ist als Diagnose erfasst.** Die Taktiklesung
selbst bleibt mit dem ursprünglichen `ReaderCheckError` fehlgeschlagen. Kein
Parser-, Taktik-, Trainings-, Replay-, Native- oder Karriereadvance-Release.

Geprüft wurden ausschließlich erhaltene JSON-/Textbelege, Pythonquellen,
Verträge, Gitblobs und das bereits vorhandene offizielle Paketwheel. Der Reviewer
hat keinen Spielstand geöffnet, decodiert oder erneut gehasht und keinen Decoder
oder nativen Host gestartet. R0/R1/R2 bleiben unveränderte archivierte Ergebnisse.

## Quelle und vorgängige Zulassung

Der Versuch verweist auf den veröffentlichten Commit
`0744238cbcbd429dd59602f0470b18a1d9f52057` und die unabhängig abgefragte erfolgreiche
[CI43636256046](https://github.com/Matchekk/FM-27-Research/actions/runs/43636256046).
Privates Directorreceipt und erhaltenes Attemptreceipt stimmen überein:
`published proceed`, der separate finale Runnerreview und exakt dieser Vertrag.
Der LF-normalisierte Vertragshash ist
`116caf7e203c6a6735218b4f712f4fcf732bba0525cd0e8b6b9ac2087307f5ee`;
Reviewhash `53e37ec38265798112e094c351e26c823a367af20922ff862609d1e846051f02`.

Alle zwölf gebundenen Source-/Dokument-/Input-/Reviewdateien passen sowohl zu
ihren veröffentlichten Gitblobs als auch zu den tatsächlichen Dateien. Der finale
Vertrag ist als JSON gleich seinem veröffentlichten Blob. Alle86 offiziellen
Reader-Pythonquellen passen bytegenau zum eingefrorenen Inventar und zu den
entsprechenden Dateien des vorhandenen offiziellen fmsave0.12.4-Wheels.
Wheel-SHA256 `2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa`.
Für diese Paketprüfung wurde fmsave nicht importiert.

Der Childsetupbeleg bestätigt den offiziellen Reader0.12.4. Der vollständig
erhaltene Warnungsbeleg enthält genau eine `UnknownBuildWarning`, ohne
Abschneidung. Der Save-Metadatenclaim `27.0.1+2503222` und sein Schema bedeuten
weiterhin keine unabhängig validierte Readerstruktur für diesen exakten Build.

## Tatsächlicher Ablauf und erhaltene Originalexception

Neun private Stageevents projizieren ohne ungültige Zeilen oder Receiptprobleme
auf den öffentlichen Fünfstufenledger:

| Stufe | Zustand |
| --- | --- |
| veröffentlichte Quellen und Releasegates | observed |
| Snapshot vor Readeröffnung | observed |
| einmaliges striktes open | observed |
| einmaliger finaler tactics-Aufruf | failed: ReaderCheckError |
| close und Snapshotnachhash | observed |

Der eingefrorene Childpfad enthält genau eine strikte `module.open`-Stelle und
eine Übergabe des ursprünglichen `save.tactics` an den äußeren Observer. Die
erhaltene Exception läuft im Traceback durch diese Grenze, den offiziellen
Taktikreader und `_read_selection_part`; der finale Fehler betrifft den erwarteten
Set-piece-Marker. Der passive Observer ersetzt keine Readerfunktion. Sein
Sourcepfad ruft die ursprüngliche Operation mit identischen Argumenten auf und
propagiert die gefangene Exception mit einem bloßen `raise` weiter.

Die Objektidentität einer vergangenen Exception kann aus JSON allein nicht
nochmals gemessen werden. Hier binden unveränderte Quelle, Originaltraceback
und erneut bestandene synthetische Identitätsprüfungen den transparenten
Aufrufpfad. Alle elf reinen Diagnose-Regressionsfälle bestanden, einschließlich
gleicher Exception/Rückgabe/Argumente, interner verworfener Kandidatenfehler,
fremder Fehler, ungültiger Frames und fehlender Such-/Recoverypfade.

Close wurde nach dem Taktikfehler versucht und als `closed` protokolliert;
Quellreihenfolge und Abschlussstage binden den Nachhash danach. Beide erhaltenen
Snapshotreceipts sind gleich:147.130.636Bytes und SHA256
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
Dies ist die Nachprüfung der gespeicherten Decoderreceipts, kein eigener neuer
Savehash des Reviewers. Readeröffnungen1, Taktikaufrufe1, Retries0.

## Enge Bedeutung des Markerbefunds

Die erhaltene finale Zielframe-Diagnose enthält einen Abschnitt mit2.267.258Bytes
und einen ausgewählten Block mit9.644Bytes. Der Cursor liegt im ersten
Blockdezil; die öffentliche obere Zweierpotenzgrenze der verbleibenden Bytes
ist16.384. Die abgeleiteten öffentlichen Bereichswerte wurden unabhängig aus
dem privaten Receipt nachgerechnet. Absolute Cursor-/Blockoffsets und tatsächlich
gelesene Bytewerte werden hier nicht veröffentlicht.

Alle drei bereits deklarierten Marker sind je3Bytes breit. Jeder Vergleich liegt
vollständig innerhalb des ausgewählten Blocks, und alle drei Gleichheitstests
am exakt erfassten Cursor sindfalse. Das passt zur tatsächlichen originalen
Markerfehlerstelle und ist kein bloß fehlender Restpuffer für diese Vergleiche.
Der Pass scannt keine alternativen Offsets, sammelt keine Markerrohbytes und
ändert keine Grammatik. Ein vorausgehender Cursorversatz, eine falsche
Blockzuordnung oder tatsächliche Layoutabweichung bleiben offen. Weder neue
Markerbytes noch eine konkrete Reparatur sind belegt.

## Ressourcen, Integrität und Grenze

Erhaltene Laufzeit13,922s innerhalb180s; ein tatsächlicher Readerstart, GO nach
geprüfter Jobmitgliedschaft, Childexit20 wegen des Originalfehlers. Flags0x2308,
Prozesslimit1, harte Prozess- und Jobgrenzeje3GiB, Kill-on-close ohne Breakaway.
Peak-Job-Private-Memory881.004.544Bytes liegt darunter. Kapselexit,
Kernel-Active-Process-Count0, finale Jobpolicy und Cleanup sind bestätigt;
keine aktive Readerlease bleibt zurück. stdout1.953Bytes ohne Abschneidung,
gesamte elf private Dateien7.069Bytes innerhalb des1MiB-Limits.

Alle elf tatsächlich vorhandenen privaten Dateihashes stimmen exakt mit dem
öffentlichen `evidence_sha256` überein. Kanonischer SHA256 der sortierten
Namens-/Hashabbildung:
`73b8a557147fce6132c511d8edf444ffe0bea5b1dccb68e705e3b31d2208cd1a`.
Eigener reproduzierbarer Lesepfad:
`analysis/review_night001.py --career-r3-results-root <central-root>`.
Er gleicht zusätzlich die öffentliche Marker-, Ressourcen-, Warnungs- und
Stageprojektion mit den privaten Receipts ab und öffnet keinen Save.

Kein blockierender Widerspruch zwischen erhaltenen Belegen und öffentlichem
Diagnosebericht. Der Erkenntnisgewinn ist die begrenzte Lokalisierung des final
propagierten Fehlers. Ein erfolgreicher Taktikdatensatz oder eine valide
native Feld-/Karrieresemantik wurde dadurch nicht gewonnen. Alle fünf
wissenschaftlichen/Karriere-Releaseflags bleibenfalse; keine Seeds oder
Kalenderadvances gehören zu diesem Diagnosepass.

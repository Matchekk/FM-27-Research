# VALID-004-R3-DIAG – unabhängiger Offline-Review

14.11.2026. Geprüfte Ausgangsbasis `d3ad665`; anschließende Hashkorrektur
`b6b09b1d9de124df99e0a66178b9164ef76084b6` unabhängig übernommen.
**Die begrenzte Offlinevorbereitung ist nachvollzogen. Ein echter
Reader-Supervisor ist weiterhin nicht implementiert und kein Savepass freigegeben.**

Der Reviewer arbeitete im eigenen Branch `codex/night-career-r3-review`.
Keine Save-Datei geöffnet oder gehasht, kein fmsave importiert, kein Decoder,
nativer Host, UI-Eingriff, Seed oder Kalenderadvance gestartet. DLL-Dateimetadaten
rein lesend geprüft: FileVersion27.0.1, ProductVersion27.0.1+2503222;
Reviewinterpreter Python3.12.10. Dies ist keine neue native Abnahme.

## Unabhängige Quellen- und Belegprüfung

Der eigene [Auditor](../../analysis/review_career004r3.py) prüft die tatsächlich
vorhandenen86 offiziellen Pythonquellen gegen das eingefrorene R2-Inventar und
den Vendorbaum gegen R1. Er importiert diese Pakete nicht. Die fünf berichteten
Taktikfunktions-ASTs wurden unabhängig neu gebildet; alle Hashes und
Gleichheitsbehauptungen stimmen. Der Selectionpräfix bis einschließlich
Taker-Markerprüfung ist identisch, die gesamte Selectionfunktion unterscheidet
sich erst danach. Drei geerbte Marker von jeweils3Bytes wurden aus den
Layoutdeklarationen rekonstruiert; FM27 überschreibt diese Deklaration nicht.
Das beweist weder ihre Gültigkeit für unseren Save noch die Ursache des Fehlers.

Die tatsächlichen Upstreamquellen bestätigen: `_stored_block_starts` fängt
Fehler verworfener Kandidaten selbst ab. `Save.tactics()` liest beim ersten
Aufruf unmittelbar über seinen Cacheaufbau und benötigt intern auch Club- und
Spielerreader. Der vorgesehene äußere Wrapper verändert diesen Aufrufpfad nicht.
Der Section-Kontext liefert `bytes`; die strikte Typprüfung des Fehlerframes
passt damit zur eingefrorenen Schnittstelle.

Alle24 öffentlichen R1/R2-Probezeilen wurden erneut direkt aus den privaten
Ereignisledgers rekonstruiert. R1:4beobachtet einschließlich Openwarnung,
1fehlgeschlagen,7unbegonnen. R2:5beobachtet einschließlich Openwarnung,
1fehlgeschlagen,6unbegonnen. Die R2-Trainingssummen ergeben unabhängig
4Teamrecords,155gespeicherte Wochen,1085Tage und3255Slots. Keine neue Messung.

Private rohe Ereignisledgerhashes:

- R1: `d92dc6b91810975752f48fcffa228e8aa1228f7a148d8c20bc23fbde99be7e65`
- R2: `411a5818b46d8a6f7f168143e7d468192681700613a14aac7d8e656f127de8e7`

Öffentliche Coveragehashes, für Git-Nachprüfung LF-normalisiert:

- R1: `eded164e2a9ad491a3300e642df2f50cfe48575d99567dc42749bfd879f75987`
- R2: `3880fe39c44c080cd6476c21059724b84292507008343466fa716c21855b4c9f`

## Transparenz des Diagnosebausteins

`observe_final_call` liefert das identische Rückgabeobjekt oder wirft dieselbe
Originalexception weiter. Er ersetzt keine Fremdfunktion. Nur eine nach außen
propagierte passende Exception mit exakt einem passenden Codeobjektframe wird
diagnostiziert. Interne Fehlkandidaten bleiben intern. Maximal64 Frames,
vier Marker und16Bytes je Marker begrenzen die zusätzliche Beobachtung.
Verglichen wird ausschließlich am bereits vorhandenen Cursor; weder Suche,
Alternativoffset noch alternative Markergrammatik werden eingeführt.

Die privat vorgesehenen Outputs sind Grenzen, Längen und Booleans. Rohbytes,
Namen, IDs und Fehlermeldungstexte werden nicht in den Receipt übernommen.
Ein überbreiter, fehlender oder mehrdeutiger Frame wird abgewiesen. Auch bei
einem Fehler im Observer bleibt die Originalexception erhalten. Ein fehlender
Capture ist keine erfolgreiche Diagnose; ein späterer Supervisor muss dies im
vollständigen Ledger ausweisen. Die Vergleichsslice folgt der unveränderten
Upstreamprüfung, zusätzlich wird deren Lage innerhalb der Blockgrenze separat
gekennzeichnet. Daraus folgt keine neue Layoutannahme.

Sechs eigene adversariale Tests ergänzen die Autorprüfungen: intern verworfener
Markerfehler vor anderem finalem Fehler, fehlender exakter Frame, Fehler im
Observer selbst, überlange Tracebackkette, unveränderte `BaseException` sowie
16Byte-Marker ohne Nachbarsuche. Alle Fälle erhalten Objekt-/Argument- oder
Exceptionidentität und verhindern unberechtigte Diagnosebehauptungen.

## Befund vor dem endgültigen Freeze korrigiert

Die ursprüngliche Vorbereitung hashte eigene Quellen roh. Ihr Draft entsprach
LF-Gitblobs, während der neue Windows-Checkout CRLF enthielt. Das ist kein
inhaltlicher Quellwechsel, muss aber vor einem ausführbaren Gate eindeutig sein.
Root korrigierte dies in `b6b09b1`: nur eigene Quellen und Dokument werden
explizit LF-normalisiert; Paketquellen und private Belege bleiben roh.
Der regenerierte Vertrag und die zusätzliche LF-/CRLF-Regression wurden
unabhängig geprüft. Alle Own-/Dokumenthashes stimmen mit der neuen Regel.
Kein R1/R2-Vertrag oder historisches Messergebnis wurde dafür geändert.

## TRAIN-Lücken und Freigabegrenze

Die deklarierte Feldinventur von zehn Modellklassen und37 öffentlichen
Save-Methoden wurde unabhängig aus dem AST rekonstruiert. Die berichtete
Abgrenzung ist korrekt: gespeicherte Tage und Sessioncodes sind keine
individuelle Teilnahme, Team-/Kaderzuordnung kein Coach-Session-Join,
Personalpräferenz keine individuelle Intensitätszuweisung. Fokus- und
Teilnahmeschnittstellen sowie ein belegter Karriere-RNG-Stream fehlen in dieser
geprüften typisierten API. Undekodierte Bereiche werden damit nicht als leer
oder informationslos erklärt. Gespeicherte Kalender enthalten Zukunftswochen;
eine Expositions- oder Wirkungsanalyse bleibt gesperrt.

17gezielte Tests nach Hashkorrektur bestanden:11Autor- und6eigene Tests.
Zuvor bestand die gesamte Suite der Ausgangsbasis mit249Tests, davon einer
wegen fehlender privater historischer Golddatei ausgelassen; außerdem fünf
historische Analysetests. Archivprüfungen bestätigen340 NIGHT-Basisdateien und
272 Round3-Basisdateien unverändert. Der eigene Source-/JSONauditor bestand nach
Übernahme der Korrektur erneut.

Vor einem echten R3-Pass fehlen weiterhin ein separat implementierter
Supervisor, endgültiger Quellen-/Vertragsfreeze, exakte erfolgreiche
veröffentlichte CI, unabhängige Ausführungsprüfung und Director-Proceed.
Einmalmarker, Reader-Lease, Windows-Job vor Decoding,180s/3GiB, Vor-/Nachhash,
private Feldallowlist und Crashabrechnung sind bisher Anforderungen des
Entwurfs, keine bereits bestandenen R3-Laufgates. Keine Decoder-, Taktik-,
SET-, Replay-, Karriereadvance-, RNG- oder Trainingswirkungsfreigabe.

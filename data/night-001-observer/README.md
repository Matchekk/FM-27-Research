# VALID-005 – sichere Observervorarbeit

- `contract-draft.json`: kleiner Root-zu-registrierender technischer Vertrag,
  keine Seedreservierung oder Ausführung.
- `snapshot-schema.json`: eigene Rohfeld-/Stufenbeschreibung mit sichtbaren
  Missing-/Kalibrierungs-/Releasegrenzen.
- `build-report.json`: echte isolierte Compiler-/Quell-/Hosthashbelege; alle
  früheren Entwicklungsversuche bleiben dokumentiert. Kein Hoststart.
- `static-dataflow.json`: Original-DLL-RVA-/Datenflussbefunde, Hashes privater
  begrenzter Disassemblate; keine Assemblate/Gamebytes öffentlich.

Eigene Implementation/Tests: `research/passive_observer.py`,
`adapters/passive_observer_v1.h`, minimaler `passive-observer-v1.patch`,
`analysis/build_passive_observer.py`, `analysis/audit_passive_observer.py`.
Kein früherer Runner oder freigegebener Host wird überschrieben.

Nach einer späteren technischen Ausführung dürfen nur numerische Zusammenfassungen,
Zähler, anonyme Zellen und Hashes ergänzt werden. Originale Spieleridentitäten,
Dump-/Logbytes, Kompatibilitätsheader, Executable und Spieldateien bleiben privat.
Parser-/Buildsuccess ist keine native Freigabe.

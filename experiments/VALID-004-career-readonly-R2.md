# VALID-004-CAREER-R2: isolierter offizieller fmsave0.12.4

Status: **vorbereitet, nicht zur Save-Ausführung freigegeben**. Separate
rein lesende Teilstufe von [VALID-004 Phase 1](VALID-004-test-fm-research.md).
Gemeinsame Zielgröße, Probeordnung, Datenschutz-, Abbruch- und Ressourcenregeln
sind im [R1-Vertrag](VALID-004-career-readonly-R1.md) vollständig festgelegt.
R2 ist ein eigener einmaliger Prozess, keine Wiederholung von R0 oder R1.

## Quellenidentität

Der [offizielle PyPI-Release](https://pypi.org/project/fmsave/0.12.4/)
wurde am 2026-11-13 veröffentlicht. Ausschließlich das offizielle Wheel wurde
privat mit `--no-deps --no-compile --target` isoliert installiert. Basis-fmsave0.9.0
und Paketpins bleiben unverändert. Das isolierte Python-Quelleninventar muss
bytegenau mit dem Wheelinventar übereinstimmen.

- Wheel: `fmsave-0.12.4-py3-none-any.whl`.
- SHA256: `2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa`.
- [Release-Tag v0.12.4](https://github.com/rhiever/fmsave/releases/tag/v0.12.4),
  per Git-Remote geprüft: Commit `e0704bc5d7e6bf687fecf85cd48b28c497bdef68`.
- PyPI-Provenienzstatement nennt denselben Wheelhash und das GitHub-Publishing.
  Keine eigene kryptographische Attestierungsverifikation wird behauptet.
- Quelle/Version werden über Wheel, Metadaten, Importpfad und vollständige
  Pythonquellenhashes gebunden, nicht nur über `__version__`.

Der [Upstream-Changelog](https://rhiever.github.io/fmsave/changelog.html)
beschreibt seit0.9.1 unbekannte FM27-Builds mit Schemaübernahme und seit0.12.3
zusätzliche unbekannte Schemas mit Warnung. Seit0.10.1 sind Integritätsgates
blockierend, während Populations-/Coverageprüfungen advisory bleiben können.
Damit ist fehlende Exception unter `strict=True` ausdrücklich kein vollständiger
Validierungsnachweis. Versionsneuheit allein bestätigt weder Layout noch native Semantik.

## Eigener eingefrorener Pass

[R2-contract.json](../data/night-001-career-r1/R2-contract.json) bindet Sourcehashes,
Dokumenthash, Basisinterpreter, geschützte Basisquellen und Wheel. Frischer Prozess
importiert ausschließlich die isolierte Version; keine Runtime-V10-Patches.
Alle12 Probeplätze werden separat dokumentiert. Warnungskategorien und Anzahl,
Upstream-Gatecodes/Counts/Grenzen, fehlende Nenner, Advisorystatus sowie
`ReaderLayout.region/build/schema/save_schema` bleiben erhalten. Rohtexte bleiben
privat. Unbekannte Builds und ausgeliehene Layouts sind explizite Prüfbedarfe.

Paketinterne Dekompressionsgrenzen sind expansionsbezogen: 64 MiB kleine
Teil-Allowance, maximaler Partfaktor64 und Gesamtfaktor32; keine fixen Paketcaps.
Deshalb bleibt der äußere harte **3-GiB-Windows-Job** zwingend. Eigenes Budget:
**180 s**, ein tatsächlicher Prozess, neue Artefakte höchstens512 MiB, null Retries.
Exklusiver Reader-Lease, Start vor globalem Deadlinepuffer und persistente
Zähler/Abbruchbelege gelten identisch zu R1. Kein zweiter Decoder gleichzeitig.

Nur die unveränderte bereits eingefrorene private R0-Kopie ist zulässig.
Vor-/Nachhash müssen dem R0-SHA entsprechen; keine erneute Originaldateiaufnahme.
Root publiziert Vertrag/Code und unabhängiges Review, prüft exakt passende CI
und erteilt `published proceed`, bevor ein echter R2-Pass ausgeführt wird.
Bei blockierender Eingabe-/Integritätsprüfung keine Fortsetzung oder Ersatzversuche.

## Vorab festgelegte Vergleichsauswertung

Verglichen werden ausschließlich gemeinsame anonyme Felder: Build-/Datumclaims,
Abschnittsangaben, Tabellenzahlen, verwaltete Team-/Kaderkapazitäten,
Attributpaar-Coverage, gespeicherte Trainingswochen/-codes und getrennte
Verletzungsrecordarten. Identitätsjoins werden privat verglichen und nur als
gleich/verschieden/nicht verfügbar veröffentlicht. Missing wird niemals als
Übereinstimmung oder Null gezählt. Beide Berichte müssen stabile gleiche
Snapshotbytes nachweisen; sonst keine Vergleichsauswertung.

Gleiche Werte zweier Reader auf denselben Bytes wären Konsistenz, keine
unabhängige Replikation, kein UI-/Enginebeleg und keine Trainingswirkung.
Alle nativen, Replay-, Kalender-, RNG- und Teilnahmefreigaben bleiben false.
Bis zur ausdrücklichen Freigabe existieren **null R2-Saveversuche**; bisherige
reale Arbeit umfasst ausschließlich Paket-/Quellenprüfung und isolierte Installation.

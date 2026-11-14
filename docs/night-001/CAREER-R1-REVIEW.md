# VALID-004-R1/R2 – unabhängiger Quellen- und Vorbereitungsreview

14.11.2026, Quellbasis `85b5ded`. **Code-/Metadatenvorbereitung freigegeben;
keine Freigabe eines echten Save-Lesepasses.** R1/R2 sind vorbereitet, nicht
ausgeführt. R0 und seine Belege bleiben unverändert.

## Tatsächlich unabhängig geprüft

Reader-/Supervisorquellen, beide Verträge, öffentliche Feldverträge und Tests
gelesen. Eigener `verify_frozen`-Abgleich gegen die tatsächlich vorhandenen
Runtime-, Basisreader- und isolierten Quellen sowie den Basisinterpreter bestand
für beide Profile. Der private Wheelhash entspricht
`2bb7a674decbcb48d0c37e13cafe22d0e6dba995493b97046411e94a74854baa`;
alle86 isolierten Pythonquellen stimmen bytegenau mit dessen Wheelinventar überein.
Das schützt Paketidentität, ist keine eigene kryptographische Attestierungsprüfung.
Kein fmsave importiert, kein Save geöffnet/gehasht/decodiert und keine Quelle geändert.

Alle28 neuen Karriere-/Staminafachtests bestanden, darunter elf Karrieretests und
die beiden Windows-Kerneltests mit harmlosen eigenen Pythonprozessen. Zusätzlich
fünf historische Analysetests bestanden. Die Kerneltests belegen tatsächliche
Speicherabweisung und Kill-on-close; sie sind keine Save- oder Semantiktests.

## Quellbindung, Ressourcen und Abbruch

R1 bindet das bestehende V10-Kompatibilitätsprofil samt vendorten Quellen und
beiden Wrappern. Version0.9.0 aus Distributionsmetadaten wird zutreffend nicht als
eigenständige Releaseidentifikation dieser vendorten Quellen ausgegeben.
Passive Wrapper zählen Summary-/Draftfallbackaufrufe einschließlich Annahme und
Ausnahme, ohne Rückgabeobjekte oder Exceptions zu ersetzen. Akzeptierter Fallback
bleibt eine Parserannahme und kein nachgewiesener nativer Feldinhalt.

R2 bindet offizielles Wheel0.12.4, Quellinventar und isolierten Importpfad und
wendet keine V10-Patches an. Neue Versionsnummer, ausgeliehenes Layout oder
fehlende Exception unter `strict=True` allein bestehen kein Semantikgate.
Advisory-Prüfungen, fehlende Nenner, Warnkategorien/-anzahl und Herkunft der
geliehenen Layouts bleiben sichtbar. R1/R2 werden in frischen getrennten
Prozessen betrieben; gleiche Snapshotbytes sind ein Quellabgleich, kein neues
unabhängiges experimentelles n.

Zwölf feste Probeplätze, dauerhaftes `started` vor jeder Probe, Stop beim ersten
Fehler oder angewendeten blockierenden Integritätsgate. Missing, unbegonnene und
unaufgelöste Probes bleiben getrennt. Erhaltene Attemptmarker verhindern Retry
und Überschreiben. `export-status` liest ausschließlich gespeicherte Ledgers und
startet keinen Ersatzreader. Vor-/Nachhash müssen denselben autorisierten
R0-Snapshot binden; Hashabweichung sperrt die Vergleichsauswertung.

Ein exklusiver Readerlease, je180s einschließlich Snapshotchecks/Abschluss und
harte3GiB pro Prozess und Job. Ein tatsächlicher Decoderprozess: direkter
Basisinterpreter statt Windows-Venv-Redirector. Der Child wartet auf einen
Tokenhandshake; der Parent sendet ihn erst nach erfolgreicher Jobzuordnung und
Kernelreadback. ActiveProcessLimit1 sowie Kill-on-close bleiben aktiv.512MiB neue
private Artefakte; mindestens185s Abstand zur unverrückbaren23:00UTC-Deadline.
Tatsächliche Laufzeit, Returncode, Peak und Überschreitungen sind auszuweisen;
ein gemessener Overshoot wäre kein bestandener180s-Lauf.

## Öffentliche Grenzen und verbleibendes Laufgate

Öffentliche Feldallowlist enthält Counts, Codes, Hashes und Strukturclaims;
private Namen, IDs, Pfade, Warnungstexte und Savebytes bleiben lokal.
Historische Verletzungsrecords und TYPED-Records der tatsächlich gejointen
aktuellen Kohorte sind getrennt; fehlende Clubzugehörigkeit wird nicht zum
verwalteten Club erklärt. Gespeicherte Trainingscodes sind keine individuelle
Durchführung. Roh-/Anzeigewertpaare sind keine UI-Kalibrierung.

Der echte `run` verlangt veröffentlichten vollen Commit, identischen Vertrag,
Code-/Dokumenthashes, erfolgreiche CI exakt diesesSHA, Remote-main-Abstammung
und veröffentlichten unabhängigen Reviewhash. Director muss ausdrücklich den
Lesepass anordnen. Der Worktree wird vor Savehash oder Prozessstart abgewiesen.
Zusätzlich soll der angekündigte Rootfix `central.resolve()==ROOT.resolve()`
vor einem echten Lauf geprüft werden; er verhindert abweichende private
Quellwurzeln. Bei Quelländerung sind die vorbereiteten Sourceverträge vor
Publikation neu zu erzeugen und erneut gegen die tatsächlichen Dateien zu prüfen.

Dieser Review erlaubt ausschließlich Code-/Quell-/Paketmetadatenvorbereitung.
Echte R1/R2-Lesepässe bleiben bis diesen Publikations-/CI-/Quell-/Director-Gates
gesperrt. Keine Seeds, Hoststarts, Matches, Kalenderfortschreibung oder
Karriere-Replays durch diesen Review. UI-/native Semantik, unabhängige RNG,
individuelle Teilnahme, Trainingseffekt und sämtliche Leistungsfreigaben bleibenfalse.

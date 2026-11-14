# Nachtmission – passiver Engine-Observer

Eigener Fachagent/Branch `codex/night-observer`, Basisadb708e.
Die Implementierung blieb von anderen Arbeitsbereichen getrennt; keine Registry-
oder nativen Starts. [Technischer Vertrag](../../experiments/VALID-005-passive-observer.md).

**Forschungsfrage:** Können originale Actor-, Profil-, Cache- und rohe
Tactical-Effectiveness-Zustände unmittelbar nach Vorbereitung/erster
Fortschreibung/natürlichem Ende beobachtet werden, ohne Ergebnisse zu verändern?

**Quellen:** sauberer MIT-Upstreamv1114.6/91f2eba und aktuelle DLL8c697...;
direkt gelesene Host-/Statistik-/Executionquellen sowie begrenzte rein statische
Disassemblierung der tatsächlichen DLL. [Hashes und Datenfluss](../../data/night-001-observer/static-dataflow.json).
Keine neu gelesene Quelle behauptet eine Karriere-/UIeinheitenvalidierung.

**Neuer Mehrwert:** Profilrohwerte und Runtime-Caches sind konkret getrennte
Speicherquellen. Originalroutine0x36a20 verbindet Actorc8a/c7a/c90 mit einem
Statistikobjekt über1880 und Bytes89/8a. Deshalb ist „Profil7000 kommt im Dump an“
keine ausreichende Freigabe eines nach Vorbereitung wirksamen Schärfeeingriffs.
Der Recorder stellt Messung bereit; Setter/Consumer-Nachweis bleiben eigenständig.

**Version:** Sampler-Versionszweig ist statisch belegt; bestehendes Kind62 setzt
aber bereits Matchversion1b000000. Carrier26.8 allein ist kein Gegenbeweis.
ActualVersionReadbacks und raw33Bytes werden ohne neue Versionspatches eingefroren.

**Implementiert:** eigener C++-Header und fünf minimal eingefügte Aufrufstellen,
source-disabled identity, strikter Parser/Dumpbinder/Viermodusvergleich,
read-only Audit-CLI und isolierter Builder mit bestehendem MSVC/SDK.
Der Originalupstream und installierte Runtime/Host/DLL wurden nicht geändert.
Private Build3-Datei572928Bytes, SHA256
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`.
Der neue Host wurde **nicht ausgeführt** und ist nicht vom alten Hosthash freigegeben.

**Tests:** elf eigene synthetische Fälle für Stage-/Tick-/Seed-/Identitätsbindung,
Profil-/Raw-/Cachetypen, Missing, Versiondrift, verbotene Executionevents,
natürliches Ende, A/A, Sourceeinfügestellen/Offidentität und read-only Header.
Compilerfehler `mt.exe` im ersten Entwicklungsbuild wurde mit vorhandenem SDK-PATH
in einem separaten zweiten Verzeichnis korrigiert; vor Freeze folgte Build3
mit Consumer-Cachefenstern. Keine nativen oder wissenschaftlichen Retries.

**Fallzahl/Kosten:** vorgeschlagen16Vollmatches in4gepaarten technischen Zellen,
2negativeProbes,2vorangestellteLoaderchecks =20logischeCLI-Probes,genau4neueSeeds.
180Child-/900UTC-s,ein Worker,globaleCap4.
Keine Power- oder Wirkungsbehauptung aus technischem Gleichheitstest.

**Blocker bis Rootabnahme:** neue Hostidentität/Loader, originale Inputs und Seeds,
exakte16erErgebnisgleichheit, echte vollständige3StageReadbacks, unabhängigerReview,
Publikation und CI. UIkalibrierung und tatsächliche Consumeraufrufe sind dadurch
noch nicht automatisch belegt. Sämtliche Freigaben bleiben vorerstfalse.

Nächster Schritt: Root integriert die geprüften Dateien, registriert frische
technische Seeds und eigenen persistenten Supervisor und führt die kleine
vorveröffentlichte Prüfung seriell aus. Kein automatischer MECH-002-Mainlauf.

## Supervisorhärtung vor Registrierung

Der unabhängige Quellenreview fand eine ungesicherte Fehlerkante nach dem
Host-Popen sowie fehlende Nach-Lock-Hashes. Beide sind vor einem echten Start
bearbeitet: eigener [Windows-Jobbaustein](CONTAINMENT-005.md) mit blockiertem
Capsulestart vor Jobzuweisung, dreiprocessigem Limit und nachgewiesenem
Kernel-ActiveProcesses=0. Unbestätigte Bereinigung erhält Marker, Budgetblocker
und globale Lease dauerhaft. Der Wrapper verlangt einen persistierten
bestätigten Abschlussbeleg auch nach scheinbar normaler Rückgabe.
Der neue Baustein gehört zum Codefreeze.

Fixture, beide Hosts, alle vier Eingabebinaries, Katalog und Konfigurationen
werden nach Erwerb sämtlicher lesender Handles erneut gehasht. Negative Probes
müssen neben Exitcode auch den tatsächlichen Ablehnungsgrund belegen.
Ein Offlineexport erhält selbst bei ungeklärtem Crash alle20Probeplätze und
kennzeichnet unvollständige Zeitabrechnung; er setzt kein Gate oder Budget zurück.

13 reale Windows-Kerneltests mit harmlosen Pythonprozessen sowie separate
Wrapper-/TOCTOU-/Crashledgerregressionen bestanden. Das sind weiterhin null
FM-Starts. Erneuter unabhängiger Review und exakte veröffentlichte CI bleiben
vor Registrierung beziehungsweise nativer Ausführung erforderlich.

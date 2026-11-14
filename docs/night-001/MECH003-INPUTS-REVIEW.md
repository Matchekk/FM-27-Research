# MECH-003 – unabhängiger Review der konkreten Vorbereitungsartefakte

14.11.2026 nach beaufsichtigter Preparephase. **Konkrete35Probe-Technikphase
fachlich freigegeben, erst nach Veröffentlichung, erfolgreicher exakter CI und
Registrierung. Keine512Mainfreigabe.** Ein erfolgreicher Prepareloader,
0neue technische oder wissenschaftliche Vollmatches zu diesem Prüfzeitpunkt.

## 16Eingaben unabhängig auf Recordebene rekonstruiert

Alle16privaten Konfigurationen/Binärdateien direkt gegen die ursprünglichen
vier D00-Zellen geprüft, ohne Normalizer-/Serverimport oder Hoststart.
Jede Datei behält5557Records, Header, Reihenfolge und vollständige übrige Bytes.

Die tatsächlichen Änderungen sind exakt:

| Arm | Stamina52 der zehn aufgestellten Feldspieler | Pressing-ID / Bit | geänderte Records |
| --- | ---: | --- | ---: |
|R00|40|1313689463 /0|10|
|R10|80|1313689463 /0|10|
|R01|40|2000905329 /66|11|
|R11|80|2000905329 /66|11|

Insgesamt acht Dateien mit zehn und acht Dateien mit elf Recordänderungen.
Zielslots stammen tatsächlich aus `lineup[1:]`, jeweils zehn unterschiedliche
Starter. Nach Rücksetzen nur dieser Attribute auf60 und Pressing auf Standard
sind sämtliche Konfigurationen exakt D00. Beide Seiten, Gegner, Torwart, Bank,
inaktive Auswärtsslots, sämtliche anderen Attribute, Profilfelder, IP/OOP-
Positionen, Rollen, Duties, PI, Management und Versionrecords sind gleich.
Keine neuen Kind61-/Execution-, Setter- oder Clamprecords.

Die Binärdiffs wurden eigenständig aus allen geordneten5×uint32Records erzeugt
und als vollständige Mengen mit den erwarteten zehn Stamina- und optional
einem Pressingrecord verglichen. Alle16Dateihashes stimmen mit ihren konkreten
Setups überein. Im tatsächlich vorhandenen Katalog ist Attribut52 `Stamina`;
die beiden Pressing-IDs binden die deklarierten Bits0/66. Neue native Dosis-/
Phasen-/PI-Readbacks sind dadurch noch nicht ersetzt und folgen in der Technik.

## 66Seedreservierungen und wissenschaftlicher Vertrag

Öffentliche, private und zentrale Registryreceipts stimmen exakt überein:
66einzigartige neue uint32Seeds, davon2technische und64Mainseeds. Beide Listen
mit dem deklarierten namespacebasierten Allocator unabhängig rekonstruiert:
Technik zuerst aus2458Ausschlüssen, Main unter zusätzlichem Ausschluss der zwei
Technikseeds. Ausschlussmenge, Anzahl und Set-Hash stimmen. Eine zusätzliche
rein lesende Historien-/Registrierungsinventur findet keine Überschneidung.

Technikseeds: `3467865036` für high_press und `3060477054` für deep_block.
Die64Mainseeds bleiben ausschließlich reservierter zukünftiger Plan, keine
ausgeführten Matches und keine durch dieses Dokument freigegebene Serie.
32Seeds pro Kontext, vier Arme und zwei Seiten ergeben erst bei späterer eigener
Mainfreigabe512Matches/64Seedblöcke. Kein Holdout, Ersatzseed oder Seedreset.

Der konkrete Vertrag entspricht exakt der geprüften Vertragsfactory, abgesehen
vom danach ergänzten Executionmanifest. Stamina-xGD primär, gleiche Seiten-/
Kontextgewichte und genau Holm7 bleiben unverändert. Keine Ergebnis-, Effekt-,
Power- oder Varianzbehauptung aus diesen Eingabeartefakten.

## Sourceframe, tatsächlicher Loader und Ressourcen

Alle16eigenen eingefrorenen Codehashes stimmen sowohl mit den tatsächlichen
Dateien als auch den Gitblobs aus `930d4ac` überein. Alle eingefrorenen Runtime-
Quellhashes passen; keine nachträgliche Forschungsmoduländerung. Katalog und
der normale Originalhost gehören zur bekannten v1114.6/91f2eba-Identität und
Engine27.0.1+2503222. Der neue Observer wird nicht als MECH-Warmhost benutzt.

Private Preparebelege unabhängig gelesen: Hostinventar exakt `loader:1`,
Loaderreceipt `ok`, tatsächliches `native_engine_compatibility.compatible=true`
und DLL-Fingerprint8c697…e340. Der gesamte Preparechild hat bestätigten
KernelActiveProcessCount0, bestätigten Kapselexit, Limit10, Kill-on-close und
kein Breakaway. Kein verbliebener Cleanupmarker oder globaler NativeLease.

Inneres Budget reconciliert, nicht halted:15,9887757/600s, ausschließlich
`loader-check-image-prepare` dauerhaft reserviert. Master78,9599919/1800s.
Studienfenster seit19:10:38,762040UTC, unverändertes Ende
19:30:38,762040UTC; Publikations-/Review-/CI-Zeit verlängert diese1200s nicht.
Vor Technik müssen alle35Keys reserviert werden. Maximal vier Engineworker;
Kernelmaximum10 zählt zwei Steuerprozesse plus vier Launcher-/Enginepaare.

## Gehashte öffentliche Artefakte

CRLF→LF-normalisierte SHA256:

| Artefakt | SHA256 |
| --- | --- |
|contract.json|`d2d6c99eb80934810319d5f0cbff3007d155b47a2a5a848d0e0b9d9e71113248`|
|inputs.json|`43544d984511579c9042bfe23d1ce964302762a822df6abfe4a359ade419bcc4`|
|seed-plan.json|`5cba87c85bfe053229138c1af129ea53e9c94ee6813801e1b03bee7bad23f816`|
|excluded-seeds.json|`25379f4c5feb8cf06909b7d0bc5ee58068939e7f09affd936e1c7faea6e0b9d2`|
|design-matrix.json|`758dc2d066e847b75a0841a726c9d4145eda8355c49aa0aeb99cbc57f14b9007`|
|binary-diff-audit.json|`1a44cadf3ef46bb9945e4db220408548fbb55232dd4bb319b1a7eb199a92fc77`|

## Enger nächster Schritt

Director darf nach vollständiger Veröffentlichung dieser konkreten Artefakte
und dieses Reviews, erfolgreicher CI am exakten vollen Registrierungscommit
und bestandenem `register` ausschließlich35Technikprobes ausführen:
Loader+Capabilities+32Vollmatches/16A/A+eine108-Negative. Kein paralleler
Startpolicy- oder anderer nativer Supervisor; Master und NativeLease bleiben
zwingend. Bei erstem Gatefehler alle Restplätze erhalten, kein Retry/Ersetzen.

Tatsächliche Eingabe-/Dosis-/Repeat-/Seed-/Phasen-/PI-/Capabilities- und
Bereinigungsbelege werden anschließend separat unabhängig geprüft. Erst deren
erfolgreicher veröffentlichter Review und exakte CI können einen eigenen
Mainentscheid ermöglichen. Keine automatische Main-, Mechanismus-, UI-, Setter-
oder Karrierefreigabe. Reviewer:0Hosts,0Matches,0Seeds,0Savezugriffe.

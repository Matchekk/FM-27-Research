# MECH-003: unabhängiger Review des Archivverifiers

Stand 2026-11-14. **Freigegeben für die rein lesende Archivprüfung und deren
CI-Einbindung.** Kein blockierender Befund in den drei neuen Dateien von
`dc29845372921292bbad9be3e62f618565b59fa1` (Fachcommit `de99b86`). Die bestehende
Vorregistrierung, ursprüngliche Verifier-/Statistikquellen und Messdaten werden
dadurch nicht geändert. Workflowänderung und Veröffentlichung liegen beim
Research Director; dieser Review ändert keine Workflowdatei.

## Quellenbindung und heutige Daten

Die geprüften aktuellen Dateien stimmen nach alleiniger CRLF/LF-Normalisierung
mit ihren Gitblobs im genannten Integrationscommit überein. Der neue Wrapper
`analysis/verify_mech003_archive.py` hat SHA256
`97ee3bf02a0e0177b040a58ebd755699a81e13585c1af6dd232074aa81541112`.
Die Testquelle hat SHA256
`9ef642c8cd66a5a2e5aa11fa72b61015a511e8fc144727a7a6b87e7ef04908f8`.

Der echte Leselauf rekonstruierte den vollständigen historischen Baum von
`9a5424fe77f465c0b5b3bd3d84e89300a1fe3ec4`: **494 Dateien, 27.806.101 Bytes**.
Die sechzehn erwarteten Codepfade werden zunächst gegen ihre eingefrorenen
SHA256 geprüft; anschließend stimmt jeder extrahierte Dateiinhalt zusätzlich mit
der tatsächlichen Git-Blob-OID des vollständigen Baums überein. Weder ein
Hash-Monkeypatch noch ein Ersatz des ursprünglichen Verifiers wird verwendet.

Der unveränderte historische Verifier erhält ausdrücklich den **heutigen**
öffentlichen Datenordner als absolutes `--directory`. In einem unabhängigen
synthetischen Gegenversuch enthielt der archivierte Datenordner den Wert1,
der externe heutige Ordner Wert2 und die historische Prüfregel erwartete2:
der Lauf bestand. Der vorhandene Regressionstest verändert danach die heutigen
Daten auf3 und erhält die erwartete Ablehnung. Dies prüft tatsächlich neue
Messdaten gegen alte Regeln.

Vor und nach dem echten Lauf war der öffentliche Inhaltsfingerprint gleich:
`fc3587c6e7eb3e0e84669ff414a4ceb198f7ff5e764c4ba4dcb0e292abd4fdda`.
Dieser Wert dokumentiert den geprüften Lesestand und ist kein neuer Datenvertrag.
Die ursprüngliche Ausgabe war `contract_verified=true`, `completed=false`,
`planned_main_matches=512`, `independent_main_blocks=64`,
`native_starts_by_verifier=0`. Die Zahlen512/64 beschreiben den geplanten Umfang.
Separat erneut geprüft:550 öffentliche Jobzeilen, alle514 Hauptphasenplätze
`not_started`, leere `main.jsonl`. Tatsächlich durchgeführte Hauptmatches und
wissenschaftliche Seedblöcke bleiben jeweils0; der administrative Studienabschluss
aus [MECH003-STOP-REVIEW.md](MECH003-STOP-REVIEW.md) bleibt maßgeblich.

## Isolation, Grenzen und Bereinigung

Der historische Prozess startet aus einem neuen temporären Snapshot, mit dessen
Verifierpfad und Arbeitsverzeichnis. Historische ROOT-/Importpfade zeigen dorthin;
`PYTHONPATH`, `PYTHONHOME`, User-Site und die bezeichneten nativen Zulassungstoken
werden entfernt, Bytecodewrites deaktiviert. Der echte historische Gitbaum
enthält keine `.pyc`, `.pth`, `__pycache__`, `sitecustomize.py` oder
`usercustomize.py`. Ein zusätzlicher eigener Mini-Git-Versuch vergiftete die
heutige Forschungsquelle samt kompiliertem Bytecode, ersetzte den heutigen
Verifier durch eine sofortige Exception und setzte `PYTHONPATH` auf diese Quelle.
Trotzdem wurden historische Regel2 und heutiger Datenwert2 gelesen; sämtliche
aufgezeichneten eigenen Snapshotverzeichnisse waren danach entfernt.

Das heutige und historische Dependency-Lock müssen identisch sein, und alle14
installierten Distributionsversionen müssen genau passen. Der echte Lauf bestand;
Lock-SHA256 ist
`5c8b7a5e5678bfa18f86f15bebac808518e6841f158eefb82ccb17bd1ba71953`.
Die Regressionen lehnen Lock- und Versionsdrift ab. Dieser Nachweis bindet
Versionen, nicht sämtliche installierten Paketbytes: das bestehende Lock enthält
keine Wheelhashes. Der verwendete Python-/Git-/Venv-Unterbau bleibt Voraussetzung.

Vor Extraktion werden Baum, Dateizahl, Pfade, Typen und Größen begrenzt:
2048 Dateien,4096 ZIP-Einträge,64MiB expandiert,8MiB je Datei,66MiB Archiv.
Traversals, absolute/mehrdeutige Windowsnamen, Alternate Streams, Case- und
Datei/Verzeichnis-Kollisionen, Links, Submodule, verschlüsselte oder unerwartete
ZIP-Einträge scheitern. Inhalte werden exklusiv neu geschrieben und gegen Größe
und Git-Blob-OID geprüft; unvollständige oder durch Exportattribute veränderte
Archive scheitern. Git-/Verifierprozesse haben jeweils60 Sekunden Timeout.

Die rekursive Bereinigung verlangt vorab den unveränderten aufgelösten absoluten
eigenen Tempzielpfad innerhalb seines ursprünglichen Temp-Elternverzeichnisses,
den eigenen Namenspräfix und das Fehlen eines Links/Junctions am Ziel.
Abweichende Ziele werden nicht gelöscht. Die öffentlichen Daten werden gelesen
und vor/nach dem Kindprozess gehasht. Das ist ein Integritätsnachweis für diesen
vertrauten historischen Analysepfad, keine Sandbox für beliebigen fremden Code.
Der geprüfte Importpfad konstruiert keinen NativeLab und startet keinen Host.

## Tatsächliche Prüfung

Bestanden: sieben Archiv-Regressionsfälle mit eigenen Mini-Gitrepositories/ZIPs,
der echte Wrapperlauf auf den heutigen öffentlichen MECH-Dateien sowie der oben
beschriebene zusätzliche Import-/Bytecode-/Cleanup-Gegenversuch. Die sieben Tests
decken außerdem falschen Commit, Codehash/-inventar, Drift, unsichere ZIPs,
Inhaltsabweichungen, Größenlimits und unzulässige Cleanupziele ab.

Keine Native-/Spiel-/Serverstarts, Savezugriffe, Seedreservierungen, Registry- oder
öffentlichen Datenänderungen durch diese Prüfung. Sie erweitert ausschließlich
die historische Nachprüfbarkeit; keine erneute Studienzulassung und keine
Stamina-Effektanalyse. Commit-/Pushstatus wird im Übergabebericht separat genannt.

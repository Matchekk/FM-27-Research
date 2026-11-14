# MECH-003: historisch gebundene Archivprüfung

Stand2026-11-14. Der neue `analysis/verify_mech003_archive.py` löst ausschließlich
die Versionsbindung der Archivprüfung. Der ursprüngliche Verifier, seine Imports,
Statistik, Vorregistrierung und Messdateien bleiben unverändert. Keine weitere
Simulation, Freigabe oder wissenschaftliche Effektanalyse wird dadurch ausgelöst.

Der ursprüngliche `verify_mech003.py` vergleicht eingefrorene Codehashes mit seinem
eigenen `ROOT`. Künftige zulässige Plattformänderungen würden daher bei Ausführung
aus dem aktuellen Checkout historische Prüfungen scheitern lassen. Der neue Pfad
führt genau diesen alten Verifier in einem rekonstruierten historischen Repository
aus und übergibt ihm die **aktuellen öffentlichen Messdateien** als `--directory`.
Es gibt weder Hash-Monkeypatching noch Ersatzstatistik oder ein erfundenes Erfolgsflag.

## Ablauf und Grenzen

1. Der aktuelle Manifestcommit muss genau
   `9a5424fe77f465c0b5b3bd3d84e89300a1fe3ec4` sein. Alle16 eingefrorenen Codepfade
   und ihre SHA256 werden gegen die Gitblobs dieses Commits geprüft.
2. Das heutige `requirements-lock.txt` muss mit dem archivierten Lock identisch
   sein; ausschließlich CRLF/LF wird normalisiert. Zusätzlich müssen alle14 aktuell
   installierten Distributionsversionen genau den Pins entsprechen. Bei Drift
   stoppen, keine automatische Installation oder Nutzung anderer Abhängigkeiten.
3. Der vollständige öffentliche Repositorybaum wird mit `git archive` in einen
   eigenen privaten System-Tempordner exportiert. `core.autocrlf=false/core.eol=lf`
   gilt nur für diesen Gitaufruf und verändert keine Gitkonfiguration. Dadurch
   stimmen auch unter Windows die exportierten Bytes mit den Gitblobs überein.
4. Vor Ausführung werden sämtliche Pfade und ZIP-Metadaten geprüft: maximal2048
   Dateien,4096 ZIP-Einträge,64MiB unkomprimiert,8MiB je Datei,66MiB Archivdatei.
   Keine absoluten Pfade, Traversals, Windows-Alternativstreams, mehrdeutigen
   Dateinamen, Case-/Datei-Verzeichnis-Kollisionen, Links oder Submodule.
   Jede extrahierte Datei wird zusätzlich gegen ihre echte Git-Blob-OID geprüft.
   Export-Substitutionen/-Auslassungen, die den exakten Baum ändern, blockieren.
5. Der historische unveränderte Verifier läuft als separater Pythonprozess aus
   dem Snapshot. Seine eigenen Imports und sein `ROOT` zeigen dort hin.
   `PYTHONPATH`, User-Site und native Zulassungstoken werden nicht übernommen;
   Bytecodewrites sind deaktiviert. Pro Prozessaufruf gilt ein60-Sekunden-Limit.
   Der Aufruf enthält ausschließlich den Verifier und den aktuellen Datenpfad.
6. Der aktuelle öffentliche Datenordner wird vor und nach Ausführung gehasht und
   muss unverändert bleiben. Temporäre Dateien liegen außerhalb des Repositorys.
   Vor rekursiver Bereinigung muss das aufgelöste absolute Ziel noch exakt dem
   selbst erzeugten Tempordner innerhalb seines ursprünglichen Temp-Elternpfads
   entsprechen; bei Abweichung wird keine rekursive Löschung ausgeführt.

CLI aus dem zentralen Checkout:

```text
python analysis/verify_mech003_archive.py
# Optional expliziter aktueller öffentlicher Messdatenordner:
python analysis/verify_mech003_archive.py --directory <public-mech-003-directory>
```

`analysis/verify_night_archive.py` und `analysis/verify_round3_archive.py` bleiben
separate Prüfungen des heutigen Checkouts. Der neue Verifier ersetzt weder diese
Archivschutzprüfungen noch den privaten unabhängigen Review nativer Rohbelege.
Die Workflowintegration gehört dem Research Director; dieser Arbeitsbereich
ändert keine Workflowdatei.

## Tatsächlicher Lesetest

Mit den aktuellen öffentlichen MECH-Dateien erfolgreich geprüft:16 Codehashes,
vollständiger Snapshot mit494 Dateien und27.806.101 Bytes,14 identische installierte
Abhängigkeiten. Unveränderter historischer Rückgabestatus:

```json
{"contract_verified":true,"completed":false,"planned_main_matches":512,"independent_main_blocks":64,"native_starts_by_verifier":0}
```

Die Hauptserie wurde nicht gestartet; der Status bestätigt keinen Staminaeffekt.
Die vorliegenden32 technischen Matches und die550er-Jobabrechnung werden vom
historischen Code auf den heutigen öffentlichen Belegen geprüft. Kein Effektbericht
wird erzeugt. Die Daten blieben während des Lesetests bytegleich. Ihr dabei
berechneter Inhaltsfingerprint war
`fc3587c6e7eb3e0e84669ff414a4ceb198f7ff5e764c4ba4dcb0e292abd4fdda`;
er ist ein dokumentierter Leseteststand und kein zusätzlicher eingefrorener Vertrag.

## Tests

Sieben eigene Tests verwenden kleine selbst erzeugte Gitrepositories und ZIPs.
Sie zeigen, dass spätere aktuelle Quellen nicht importiert werden, während
Änderungen an aktuellen Daten tatsächlich zur Ablehnung führen. Falscher Commit,
Codehash/-inventar, Lock-/Installationsdrift, unsichere ZIP-Pfade, Links, Kollisionen,
falsche Inhalte, Größenlimits und unzulässige Cleanupziele blockieren die Prüfung.
Keine Spielstände, Runtimeimporte, NativeLab-Konstruktoren, Hosts, Seeds oder
Registryänderungen. Gesamttest-/Pushstatus steht im Übergabebericht des Commits.

Lokal bestanden:7 eigene Tests innerhalb298 Repositorytests (zwei private
Goldprüfungen mangels Dateien im Worktree übersprungen), zusätzlich fünf historische
Analysetests. Separater Archivschutz:340 NIGHT- und272 Round3-Dateien unverändert.
Native Starts und neue Seeds dieses Arbeitsabschnitts:je0. Ein Pinvergleich prüft
Distributionsversionen; das vorhandene Lock enthält keine archivierten Wheelhashes.

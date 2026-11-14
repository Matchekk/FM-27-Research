# MECH-003: Review der kanonischen Datenpfade

Stand 2026-11-14. **Der enge Pfadfix ist für Archivprüfung und CI freigegeben.**
Geprüft wurde der uncommittete Folgediff auf `90a19463924ac42f9e24e3b2c2682141669b526c`:
eine Produktionszeile `directory = Path(directory).resolve()` am Anfang von
`public_data_fingerprint`, dazu ein neuer Regressionstest. Die bestehenden
Symlink-, Außenpfad-, Anzahl-, Größen- und Vorher/Nachher-Hashprüfungen bleiben
unverändert. Der [ursprüngliche Archivreview](MECH003-ARCHIVE-REVIEW.md) bleibt
als historischer Quellenstand erhalten.

Der unabhängig gelesene Fehlerlog von
[CI43635564640](https://github.com/Matchekk/FM-27-Research/actions/runs/43635564640)
zeigt einen einzigen Testfehler unter308 Tests, bei zwei Skips:
`test_historical_imports_and_current_data_are_both_real` scheitert bereits beim
Fingerprint seiner eigenen heutigen Testdaten mit
`Public measurement link forbidden`. Der bisherige Code verglich aufgelöste
Dateipfade mit einem nicht kanonisierten Root. Ein Windows-Kurzname oder
`..`-Alias kann dadurch einen eigenen regulären Unterpfad fälschlich ausschließen.
Der Fix kanonisiert beide Seiten vor demselben Enthaltenseinstest.

Unabhängig bestanden:

- Alle acht Archivtests, einschließlich des neuen Windows-Tests mit echtem
  `GetShortPathNameW` und des plattformübergreifenden `..`-Alias.
- Ein eigener zusätzlicher Windowsversuch mit einem tatsächlich vom Langnamen
  verschiedenen Kurznamen: beide Aliase ergeben denselben Fingerprint wie der
  kanonische Root. Der alte Vergleich scheitert nachweislich am `..`-Alias.
- Ein realer temporärer Windows-Junction auf ein eigenes externes Testverzeichnis
  wird bei Enumeration durchlaufen und weiterhin mit `link forbidden` abgelehnt.
  Das externe Testfile bleibt unverändert; anschließend wird nur die eigene
  Junction entfernt. Ein gesondert eingespeister Außenpfad wird ebenfalls abgelehnt.
- Ein als Symlink markiertes reguläres Dateifixture wird weiterhin abgelehnt.
  Ein echter Dateisymlink konnte lokal wegen Windowsfehler1314 nicht erzeugt
  werden; für diese spezifische Eigenschaft ist der Gegenversuch daher ein
  Guardfixture. Die echte Junction liefert den zusätzlichen Betriebssystemtest
  für das weiterhin wirksame Außenpfadverbot.
- Der echte historische Archivlauf auf den heutigen öffentlichen MECH-Daten:
  sechzehn Codehashes,494 Dateien/27.806.101 Bytes,14 installierte Dependency-Pins,
  `contract_verified=true`, `completed=false`, keine nativen Starts. Vorher und
  nachher bleibt der Datenfingerprint
  `fc3587c6e7eb3e0e84669ff414a4ceb198f7ff5e764c4ba4dcb0e292abd4fdda`.

Die nach alleiniger CRLF/LF-Normalisierung geprüften neuen Quellen-SHA256 sind:

| Quelle | SHA256 |
| --- | --- |
| `analysis/verify_mech003_archive.py` | `8a982ccd67bc7c981b15fa6f8232230c0156ba75ec8340b8719571dfb6e1b4bd` |
| `tests/test_mech003_archive.py` | `7ab899e24a2f722b359fd3c228bb0ba6e11b11243bc8630834df4e3eea2d5aef` |

Kein Blocker in diesem Folgediff. Die normalisierte Rootreferenz erlaubt
äquivalente Schreibweisen desselben gewählten Datenordners; sie erlaubt keine
auflösenden Unterpfade außerhalb dieses Ordners. Weder Snapshotbindung noch
historische Regeln oder Messdaten wurden verändert. Keine Native-/Savezugriffe,
neuen Seeds, Forschungsquellen-, Registry- oder Workflowänderungen durch den Review.
MECH-003 bleibt administrativ beendet mit0 Hauptmatches. Dieser Review ersetzt
keine neue erfolgreiche veröffentlichte CI und keine getrennten Studiengates.

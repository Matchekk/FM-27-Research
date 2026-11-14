# MECH-003: Stamina-Vorbereitung

Stand2026-11-14: Implementierung für separaten Review; **nicht nativ ausgeführt**.
Keine neue Seedreservierung, keine Registrymutation, keine Host-/Spielstarts,
keine Holdouts oder Karrierefortschreibung durch diesen Fachagenten.

Der unabhängige Erstreview blockierte die erste Runnerfassung: der echte Loader
beim NativeLab-Konstruktor war nicht reserviert, und Timeout/Leasefreigabe belegten
kein Ende aller Nachfahren. Diese überarbeitete Fassung ändert keine wissenschaft-
lichen Faktoren, Seeds oder Fallzahlen. Sie erfasst zusätzlich drei Loader- und
zwei Capabilitychecks: Phasekeys1/35/514, Caps36/514, insgesamt550 logische Slots.
74 native Hoststarts (darunter68 Warmhostparents) werden separat protokolliert.
Eine echte technische Abnahme dieser Änderung steht weiter aus.

## Eigener, abgegrenzter Pfad

`research/stamina003.py` enthält ausschließlich die vier Intentionen, exakten
Stamina-/Pressing-Binärdifferenzen und vollständigen Phasen-/PI-Audits.
`analysis/run_mech003.py` verwendet bestehende Reader/Audit-/Budget-/Leasebausteine,
ohne diese zu ändern. Er bindet Prepare/Technik/Main an den äußeren NIGHT-Master,
friert66 ausschließlich neue Seeds ein und sperrt Wiederaufnahme nach Gatefehler.
Der Director liefert den separaten Masterwrapper vor Codefreeze; der Import des
Studienmoduls startet weder Runtime noch Host. Register und alle nativen Phasen
sind auf den zentralen Checkout begrenzt.

`analysis/analyse_mech003.py` prüft den exakten Vertrag und alle512 Vollbelege,
berechnet gepaarte Seedkontraste und exakt Holm7 sowie bedingte zukünftige
Fallzahlen. `analysis/export_mech003.py` hasht private Belege erneut, verwendet
eine öffentliche Feldallowlist und erhält550 vollständige Jobstatus. Ohne
Registrierung erzeugt es nur technische Planungslots; fehlende Seeds bleiben
`null`. `analysis/verify_mech003.py` rekonstruiert öffentliche Ergebnisse unabhängig
vom exportierten Effektbericht; private Nativebelege benötigen zusätzlich Review.

## Tatsächlicher Offline-Abgleich

16 Zellen wurden rein lesend gegen vorhandene D00-Konfigurationen/Binärinputs
geprüft: zehn geänderte Stamina52-Records pro Zelle und bei MoreOften ein weiteres
Instruktionsrecord; keine zusätzlichen Änderungen. Eigene Python-Recordpackung
prüfte die deklarierte Differenz, nicht die aktuelle native Encoding-/Readback-
Wirkung. Die26 serialisierten Auswärtsslots mit23 aktiven Spielern bleiben erhalten.
Der Originalhost, NativeLab und existierende Archive wurden nicht verändert.

## Offene technische Gates vor Ausführung

1. Director integriert aktuellen NIGHT-Master, `analysis/night_supervise.py` und
   `research/native_process005.py`, lässt den separaten Review bestehen und
   veröffentlicht Entwurf/Code erfolgreich. Schon vor Prepare ist
   `prepare-gate.json` mit vollem publiziertem Commit, erfolgreicher exakter CI,
   Reviewdokument/Hash und passenden Code-/Prereg-/Draftblobs erforderlich.
2. Zentraler Preparepfad unter Master/Lease: live DLL/Originalhost/Fixture/Tool/
   Ressourcen/Kataloghashes prüfen; aktuellen Normalizer/Encoder prüfen; nur die
   vorgesehenen16 Eingaben erzeugen; atomar66 frische Seeds reservieren. Alle
   Codehashes einschließlich Master und Supervisor einfrieren. Publizieren und
   vor technischen Vollmatches mit veröffentlichtem Commit registrieren.
3. Technik separat freigeben:32 Vollmatches,16 A/A,80 tatsächliche native
   low/high-Dosen über acht Vergleiche, vollständige Readbacks und Exit108.
   Auf Originalhost laufen, keinen Observer als Warmworker einsetzen.
4. Technikbelege exportieren, separaten unabhängigen Review mit Dokumenthash im
   exakten technischen Freigabecommit veröffentlichen; CI dieses Commits muss
   erfolgreich sein. Hauptserie bleibt sonst gesperrt.
5. Nur dann512 Hauptmatches über zentralen Master, nachfolgend Export, eigener
   öffentlicher Verifier, private Rekonstruktion durch Reviewer, Archivschutz/CI.

Alle Phasen teilen600 überwachte Childsekunden und eine1200-Sekunden-UTC-Deadline;
Publikations-/CI-Pausen zählen in letztere. Zusätzlich Master1800sek/23:00UTC.
Kein Budgetreset, automatischer Retry, Ersatzseed oder Ausbau. Bei zu langer
Prüfung/Publikation stoppen und Abrechnung veröffentlichen.

Director-Startmuster (hier **nicht ausgeführt**):

```text
python analysis/night_supervise.py run --study MECH-003-STAMINA-R0 --phase prepare --keys-file <private-1-jobkey.json>
python analysis/run_mech003.py register --commit <published-preregistration-SHA>
python analysis/night_supervise.py run --study MECH-003-STAMINA-R0 --phase technical --keys-file <private-35-jobkeys.json>
python analysis/export_mech003.py
# Separate technische Veröffentlichung, Review und CI; technical-gate.json erforderlich.
python analysis/night_supervise.py run --study MECH-003-STAMINA-R0 --phase main --keys-file <private-514-jobkeys.json>
python analysis/export_mech003.py
python analysis/verify_mech003.py
```

Echte Phasenkeys liefert der reine `phase_keys()`-Reader nach zentraler
Vorbereitung/Registrierung. Keine Direktumgehung des Masterwrappers.
Prepare benötigt bereits eine private Keysdatei mit exakt
`["loader-check-image-prepare"]`; ein leerer Schlüsselplan ist hier unzulässig.

Die Kapsel besteht vor Import des Runtimeservers. Erst nach Kernelzuweisung und
privater GO-Freigabe startet Base-Python den Studienchild. Der ursprüngliche
NativeLab-/WarmRunnerpfad bleibt unverändert. Bestätigtes KernelActive0 plus
Kapselende ist Voraussetzung für Leasefreigabe. Fehlendes/unklares Receipt erzeugt
einen dauerhaften Cleanupmarker und hält die Lease, auch bei Pythonfehler/Timeout.
Der Negativhost verwendet zusätzlich dieselbe API in einer eigenen Kapsel.

## Wissenschaftliche Grenze

Primär ist der marginale totale Stamina-raw80−40-Effekt auf xGD bei unveränderten
D00-Taktiken; keine Vergleichsbehauptung zur ursprünglichen raw60-Stamina.
Gegenüberprofil, Seite und Pressing werden gepaart, aber Resultate gelten nur für
die zwei synthetischen Discoverykontexte. Keine UI-Skalenkalibrierung, Ermüdungs-
mediation, universellen Attributgewichte oder Karriereübertragung. Der Pilot hat
unbekannte Kontrastvarianz;0,30xGD ist praktische Referenz, keine Powergarantie.

## Offline-Prüfung

Die Fachtests prüfen Matrix/Kontraste, exakt begrenzte Eingriffe, tatsächliche
Lineupbindung und Auswärtstail, vollständige Phasen-/PI-Audits, fehlende/duplizierte/
falsche Belege, unveränderliche Ressourcen-/Holmregeln, A/A-Schedule, Master-/Worktree-
Sperren vor NativeLab/Budget, erhaltene Crashbelege,550er-Ausfallabrechnung,
deterministische Analyse und bedingte Fallzahlplanung. Der synthetische bekannte
Effektdatensatz dient nur einem Softwaretest und ist kein FM-Messdatensatz.
Ein eigener Prüftest verhindert Abweichung zwischen JSON-Entwurf und Vertragsfactory;
der öffentliche Budgetverifier prüft echte Jobkeys, Zeitverbrauch und feste Deadline.

Lokal bestanden:23 eigene Fachtests innerhalb201 Repositorytests (ein anderer
Observer-Goldtest mangels privater historischer Datei übersprungen), fünf historische
Analysetests,340 unveränderte Dateien im NIGHT-Archiv und272 im Round3-Archiv.
`git diff --check` bestanden. Diese Tests starten keine Engine und reservieren
keine Seeds. GitHub-CI, separater Review und native Freigabe bleiben offen.

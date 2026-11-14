# MECH-003 – unabhängiger Vorbereitungsreview

14.11.2026, Quellbasis `d295ff8`/`85b5ded`. **Wissenschaftlicher Entwurf und
Offlinevorbereitung nachvollzogen; ausführender Prepare-/Technik-/Mainpfad
weiter gesperrt.** Keine neuen Seeds oder nativen Starts durch diesen Review.

## Wissenschaftlicher Vertrag

Vier volle2×2-Arme rawStamina40/80×Standard/MoreOften, nur zehn tatsächlich
aufgestellte Feldspieler über `lineup[1:]`, kein Eingriff auf Torwart/Bank/Gegner
oder inaktive Auswärtsslots. Beide Seiten und zwei bekannte synthetische Gegner.
Die Recorddiffprüfung erlaubt zehn Staminaänderungen und gegebenenfalls genau
ein Pressingrecord. raw60 bleibt Ausgangspunkt der Eingabeherstellung, nicht
ungetesteter zusätzlicher Vergleichsarm oder kalibrierter FM-Anzeigewert.

512Hauptmatches ergeben64Seedblöcke mit je acht gekoppelten Matches, keine
512unabhängigen Replikate. Primärer marginaler Stamina-xGD-Kontrast,
Seitenausgleich innerhalb Seed und gleiche Kontextgewichte sind konsistent.
Genau Holm7 für fünf zusätzliche Staminaendpunkte, Pressing-xGD und physische
Stamina×Pressing-DoD; kein nachträglich ausgewählter Sieger. Fehlende, doppelte,
fehlgeschlagene oder semantisch nicht verifizierte Matches verhindern die
wissenschaftliche Auswertung, statt still nullgesetzt oder ausgeschlossen zu werden.

Die Analyseimplementierung wurde gelesen und auf den vollständigen synthetischen
512-Zeilen-Softwaretestdaten unabhängig nachgerechnet: eigene Gruppierung aus
Team-xG, Armkontraste, Seiten-/Seedmittel und Welch-Varianz/Freiheitsgrade/KI
stimmen mit der Implementierung überein. Das ist ein Softwaretest, kein FM-Befund.
20.000stratifizierte Blockbootstrapziehungen, Leave-one-seed-out und deskriptive
Kontext-/Seitenzerlegung erhalten die Analyseeinheit. Bedingte Zukunftsplanung
verwendet neue Seeds, korrekte16nMatchkosten und keine automatische Erweiterung.
Kontrastvarianz unbekannt;0,30xGD und volle KI-Breite0,50 sind praktische
Referenzen ohne behauptete90-%-Powergarantie.

17MECH-Fachtests sowie fünf historische Analysetests bestanden. Eigene Inspektion
der Quellen bestätigt konkrete Setup-/Seed-/Readback-/PI-/Profilprovenienz,
Allowlist-Export und vollständige545Match-/Negativslot-Abrechnung im bisherigen
Entwurf. Diese Zahlen enthalten noch nicht alle zusätzlichen CLI-Probes unten.

## Ausführungsbefunde, vor einem Lauf zu beheben

1. `NativeLab` importiert `fm27_tactics_server`, dessen Modulinitialisierung
   `desktop_engine.initialize` mit echtem `--check-image` ausführt. Damit ist der
   Preparepfad nicht rein statisch und erzeugt bereits einen nativen CLI-Probe.
   Technik und Main starten jeweils erneut einen Loader; außerdem prüft
   `DesktopWarmRunner` einmal pro Hosthash/Prozess `--worker-capabilities`.
   Die bisherigen33Technik-/512Mainkeys und545Abrechnungsslots erfassen diese
   zusätzlichen Probes nicht. Alle tatsächlichen geplanten Loader-/Capabilities-
   Probes benötigen deklarierte Keys, dauerhafte Reservierung und Abrechnung.
   Matchfallzahl und unabhängige Seedzahl ändern sich dadurch nicht.
2. Der bisherige Negativlauf verwendet `subprocess.run(timeout=45)` auf einem
   Launcher, der einen eigenen Enginechild starten kann. Timeout-/Supervisorfehler
   müssen den gesamten eigenen Prozessbaum bestätigt beenden. Eine Exception bei
   zugleich automatisch freigegebener NativeLease genügt nicht. Nicht bestätigbare
   Bereinigung muss die Lease dauerhaft sperrend erhalten. Dieselbe Absicherung
   gilt für die übrigen zulässigen neuen nativen Aufrufe.
3. Der aktuelle `published_registration`-Pfad bindet publizierte Inhalte, prüft
   vor der Technikphase aber selbst keinen erfolgreichen CI-Run. Der Director
   muss die vorgeschriebene erfolgreiche CI und unabhängigen Codereview vor jedem
   ersten nativen Aufruf einschließlich Prepareloader tatsächlich nachweisen;
   der separate Maingate prüft zusätzlich den exakten Technikcommit/CI/Review.

Die Autoren wurden über diese Befunde informiert und bereiten getrennte Fixes
vor. Neue Grenzen/Probepläne müssen erneut reviewed, eingefroren und publiziert
werden; die hier dokumentierte alte Ausführung ist nicht freigegeben.

## Unveränderte Grenzen

Masterzulassung, innere600Child-/1200UTC-Grenzen, globales Nachtbudget und
exklusive NativeLease bleiben kumulativ. Maximal vier Worker,90s ohne Fortschritt,
keine Wiederholung, Ersatzseeds oder Budgetrückerstattung. Tatsächliche technische
Readbacks/A/A/Negativkontrollen und neue Seed-/Inputregistrierung fehlen weiterhin.
Ein späterer echter Technikbefund benötigt einen separaten unabhängigen Review.
Keine native Observer-/Setter-/Consumer-/UI-/Ermüdungsmediation, Karriereübertragung,
Holdouts, allgemeine Attributrangliste oder automatische Hauptserienfreigabe.

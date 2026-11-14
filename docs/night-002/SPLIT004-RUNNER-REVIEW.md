# MECH-004-SPLIT-R0 – unabhängiger Runnerreview vor nativer Technik

14.11.2026 · Validation Agent, getrennt vom Autor des Studienrunners und der
Analyse. **Runner für die konkret beschriebene technische Phase akzeptiert;
keine Mainfreigabe und noch kein Nachweis nativer Splitübertragung.**

Der Validation Agent hat den neuen globalen NIGHT-002-Controller selbst erstellt.
Diese beiden Dateien werden deshalb zusätzlich vom Director unabhängig geprüft;
dieser Review behauptet keine unabhängige Selbstabnahme des Controllers.
Die konkrete Inputabnahme folgt nach der rein offline durchgeführten Vorbereitung.
Öffentliche Vorregistrierung und erfolgreiche CI bleiben obligatorische Gates.

## Geprüfter unveränderlicher Quellstand

SHA256 jeweils über LF-normalisierte Dateibytes. Das später erzeugte
Inputmanifest bindet diese Dateien und dieses Reviewdokument zusätzlich vollständig.
Der Review hasht sich nicht selbst.

| Datei | SHA256 |
| --- | --- |
| `analysis/run_split004.py` | `180e64fb30f45e228d69d9507a9b55fdc4ba6e5175bc57aad9edcd8270a146f4` |
| `analysis/split004_design.py` | `91d4ab55c199565451c364a78ff21337f85a0475e16e674abd74910ccfc0de4a` |
| `analysis/analyse_split004.py` | `b5b3355824dd4afbe3755c255f4bb8082704f305a094620be467f64835379abd` |
| `research/night002_control.py` | `3dfb799b6b59540941d493591203ed47c70bb47aa56a3dda050ac0abeb696885` |
| `analysis/night002_supervise.py` | `84403545f315f2aa1311d242b3470f030706fe5fd04b272288fb833d828952b5` |
| `tests/test_split004.py` | `810c5f14e5b48ed76fbdbf8be13b4765f844fa69d31e18d01765613d11b63b4c` |
| `tests/test_split004_runner.py` | `fb5c129c8d1fecd6082c0b6e5ac4da915ac86bc7cd6e86485c50ad688bdd5974` |
| `tests/test_night002_control.py` | `5073c2d8d79fab16f9a6b33c15a1c338af6d4d839b44d41af483cff9cb8bb2fd` |

## Korrigierte Reviewbefunde

1. Der erste verschachtelte Seedscan hätte den eigenen neuen Missionsunterbaum
   als historische Daten wieder eingelesen. Er schließt nun ausschließlich den
   eigenen Studienunterbaum aus und berücksichtigt alte sowie benachbarte
   Reservierungen weiter. Ein eigener Regressionstest prüft diese Konstellation.
2. Der Aufrufparser könnte standardmäßig abgekürzte `--child`-Schalter akzeptieren.
   Der innere Parser besitzt jetzt `allow_abbrev=False`; der äußere Supervisor
   leitet ausschließlich exakte Publikations-SHA-/CI-Argumente weiter.
3. Der globale Controller verwendet eigene Identität, Datei, Tokenvariable und
   Frist. Ein alter NIGHT-001-Vertrag wird nicht geöffnet oder verlängert.

Keiner dieser Befunde verursachte einen nativen Aufruf oder verbrauchten Matchseed.

## Studiengrenze und wissenschaftliche Integrität

Der Compiler verändert allein die ursprünglichen Profilrecords16/17 für zehn
gebundene Startfeldspieler. HH ist byteidentisch mit D00; Keeper, Bank, Gegner,
Rollen, PI, Phasen und alle46Stamina60-Records bleiben gleich. Die Offdiagonalen
werden weder durch neue Setter noch durch Clamps oder Nachbereitung erzwungen.
Der technische Audit verlangt getrennte Erhaltung beider Rohfelder nach
Originalvorbereitung und erstem Tick. Das Cachebyte8A wird beobachtet; dessen
Zuordnung zu einem Feld ist keine Admissionannahme. Jede Normalisierung oder
ein Kontrollmismatch beendet den Studienpfad.

Primär wird `HL−LH` auf xGD getestet. Dieser Kontrast entspricht der Differenz
der beiden marginalen Faktoreffekte. Die physische Interaktion besitzt
`(+1,−1,−1,+1)`; keine Faktorhalbierung wurde übersehen. Seiten werden innerhalb
jedes Seeds gemittelt, zwei feste Gegnerkontexte gleich gewichtet. Die512Matches
sind64unabhängige Seedblöcke. Acht Sekundärtests bilden gemeinsam Holm8;
Punkte/Tore/Gegentore ersetzen keinen Primärnachweis. Die Analyse verweigert
fehlende, doppelte, fremde oder unvollständige Beobachtungen und imputiert keine
Nullen. Unbekannte Splitvarianz wird ausdrücklich als Pilotgrenze behandelt.

## Admission, Prozess- und Fehlerpfad

Vor Technik sind konkrete Inputs, unabhängiger Inputreview, Quellen-/Noveltygate,
veröffentlichter Code und erfolgreiche CI des exakten Commits gebunden. Vor Main
sind zusätzlich vollständige32+1Technikjobs,16exakte A/A-Paare, neues unabhängiges
technisches Rohreview, veröffentlichte Freigabe und erfolgreiche CI erforderlich.
Vor jedem Engineaufruf werden Token, lebender Supervisor, exakte Reservierung,
gemeinsame Lease, UTC-Rest und Artefaktgrenzen geprüft. Der unmittelbar erste
Mainaufruf benötigt erneut mindestens600Sekunden verfügbare Restzeit.

Der unveränderte Scheduler begrenzt auf vier zugelassene kalte Aufrufe.
Windows-Jobobjekte mit Limit3 und90Sekunden ohne Fortschritt bleiben unverändert.
Nativer Start kann erst nach Jobzuordnung stattfinden. Pendingmarker werden bei
unbestätigter Bereinigung erhalten; der Supervisor gibt die gemeinsame Lease dann
nicht frei. Alle gestarteten Fehler, offene Jobs und unbegonnene Slots bleiben in
der Abrechnung. Weder Retries noch Ersatzseeds oder Budgetrücksetzungen sind
implementiert. Private Logs/Dumps werden nicht als öffentliche Rohdaten kopiert;
Budgetexporte verwenden eine explizite Feldauswahl ohne Tokens oder private Pfade.

## Validierung und verbleibende Gates

Unabhängig ausgeführt: acht Tests aus `tests.test_split004`, fünf aus
`tests.test_split004_runner`, alle bestanden. Die neun Controllertests bestanden
ebenfalls; deren unabhängige fachliche Abnahme liegt beim Director. Alle Tests
dieses Abschnitts sind offline und verwenden synthetische Fixtures oder Mocks.
Kein nativer Host, Buildprozess oder Karrierezugriff wurde ausgeführt.

Die [Sicherheitsbewertung](SAFETY_ASSESSMENT.md) dokumentiert tatsächliche
Build-/Ressourcenhashes und die konservative globale Sperre nach fehlgeschlagener
Phase. Noch offen: konkrete Inputs/Seeddisjunktheit, öffentliche CI, neue native
Splitreadbacks und deren unabhängige technische Abnahme. Ohne diese Gates keine
wissenschaftlichen Hauptmatches. Die ausgeführten Tests sind kein Beweis der
nativen Identifizierbarkeit und keine FM-UI-Kalibrierung.

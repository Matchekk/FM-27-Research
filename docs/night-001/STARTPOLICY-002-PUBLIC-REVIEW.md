# MECH-002-STARTPOLICY-TECH: portable öffentliche Nachprüfung

Stand 2026-11-14. Der eigene zusätzliche Lesepfad
`analysis/review_night001.py --public-startpolicy` besteht auf den tatsächlichen
öffentlichen TECH17-Artefakten. Optional kann ein expliziter Checkoutroot als
Flagargument angegeben werden. Dieser Modus liest ausschließlich das öffentliche
Studienverzeichnis und die bezeichneten historischen Gitblobs; private CLI-Optionen
können damit nicht kombiniert werden. Kein Prozessstart außer lesenden
`git show`-Aufrufen, kein Native-/Reader-/Savezugriff oder Writerpfad.

Alle22 Codehashes werden gegen
`0744238cbcbd429dd59602f0470b18a1d9f52057` geprüft. Heutige Router-/Plattformquellen
werden dafür weder gehasht noch importiert. Vorregistrierte Input-, Seed-, Job-
und Reviewgate-Dateien stimmen mit ihren historischen Blobs überein; der
unabhängige Inputreview, Codereview und Observer-Ergebnisreview sind ebenfalls
an ihre historischen Blobhashes gebunden. Die bestehende erfolgreiche
Ausführungs-CI ist in der Registrierung benannt. Dieser Offlinepfad fragt keinen
Remote-/CI-Service ab und ersetzt kein Publikationsgate für neue Studien.

Die Prüfung bildet den17er-Jobplan erneut aus vier Seeds, zwei Kontexten/beiden
Seiten, zwei Rohstufen und je zwei Wiederholungen. Sie bindet alle öffentlichen
Job-/Accountingzeilen an Schlüssel, Status, Seed, Setuphash, tatsächliche
Aufrufkennzeichnung und Engine-/Hostidentität. Sechzehn Vollmatches und genau
eine seedlose108-Abweisung sind erforderlich. Die vollständigen Counts3174
Attribute,1058Profile,44Phasenzellen und748PI-Gruppen je Match müssen vorliegen.

Die acht A/A-Paare werden anhand ihrer tatsächlich publizierten Scores,
Endticks/Clocks und sämtlicher sieben Teamstatistikfelder exakt verglichen;
der zusätzliche Resultathash wird nachgerechnet. Beide Anfangsstages benötigen
je46Actors, zehn Targetfeldstarter,22Startercaches und die passende Cache8A70/100-
Angabe. Capturehashes zwischen Anfangs-/Passivereport müssen übereinstimmen.
Die High-/Low-Seitenaggregate beider Rohfelder und unveränderte Condition/Fatigue
werden numerisch nachgerechnet. Alle acht Kontrollbelege und die festgelegten
Interpretationsgrenzen sind erforderlich; Finished-Rohwerte werden nicht auf
den Anfangswert geklemmt.

Das Budget muss genau17Reservierungen, eine erfolgreiche technische Operation,
kein active/halted/unklares Cleanup,180s Childlimit und ein unverändertes900s-
UTCfenster ausweisen. Tatsächliche Zeitbelastung, kumulierte Aufrufzeiten,
Childdeadline, Abschlusszeit, Zeitdifferenzen, Finalreconciliationkennzeichnung
und beide öffentlichen Budgetgates müssen zusammenpassen. Ein `passed=true`
in der Summary genügt nicht für Erfolg.

Sechs neue Regressionen unter `tests/test_startpolicy002_public_review.py`
kopieren ausschließlich die tatsächlichen öffentlichen Studienartefakte in
eigene Tempverzeichnisse. Der positive Fall ignoriert eine absichtlich defekte
heutige Routerquelle, sperrt private Lesepfade und prüft unveränderte Datenbytes.
Falscher Anfangscache, abweichender A/A-Score, falscher Seed,180,1s trotz
Erfolgsflags und fehlgeschlagene Initialkontrolle werden jeweils abgelehnt.
Zusätzlich bestehen alle fünf bisherigen Reviewerregressionen. Insgesamt elf
gezielte Tests und der echte öffentliche CLI-Lauf bestanden. Für einen separaten
Reviewerworktree kann `FM_RESEARCH_PUBLIC_TEST_ROOT` ausdrücklich auf den
zentralen öffentlichen Datenstand zeigen; veröffentlichte CI nutzt ihre eigenen
Repositorydateien. Die Tests kopieren kein Upstreamrepository.

Diese portable Format-/Provenienzprüfung rekonstruiert keine privaten Actorlogs.
Raw-State-A/A-Hash und TF-Kontrollbelege sind öffentliche Claims, deren
Actorinhalt hier nicht aus Rohbytes neu gewonnen werden kann. Die unabhängige
[direkte Rohrekonstruktion](STARTPOLICY-002-RESULTS-REVIEW.md) bleibt dafür der
gesonderte Nachweis. Der Bericht kennzeichnet diese Grenze maschinenlesbar als
`private_actor_logs_reconstructed_by_this_portable_check=false`.
Keine neue Main-, UI-, Warm-, Consumer- oder Karrierefreigabe entsteht.

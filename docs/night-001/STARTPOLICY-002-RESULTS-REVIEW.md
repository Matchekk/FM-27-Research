# MECH-002-STARTPOLICY-TECH-V1: unabhängiger Ergebnisreview

Stand 2026-11-14. **Alle17 technischen Versuche unabhängig aus erhaltenen
Rohbelegen rekonstruiert, kein blockierender Befund.** Die neue enge Fähigkeit
ist technisch belegt: im getesteten gebündelten D00-Fixture mit Engine
`27.0.1+2503222` und unverändertem Observerhost überträgt das ursprüngliche
Profilpaket gemeinsam rawC90/C7A7000 statt10000 bei zehn Feldstartern in beide
Actorrohfelder und Cache8A70 statt100, nach Originalvorbereitung und beim ersten
erfolgreichen Fortschrittsschritt. Der serielle Cold-Caller ist dabei geprüft.

Eine öffentliche Release-Gate-Datei darf genau diese Fähigkeit nach Veröffentlichung
dieses Reviews und erfolgreicher CI freigeben. **Keine wissenschaftliche Mainserie
wird durch diesen Review freigegeben.** Ein eigener Folgevertrag samt Input-/Seed-,
Code-, Ressourcen- und Technikgates bleibt erforderlich. Keine getrennte Wirkung
der beiden gemeinsam veränderten Felder, UI-Skalenkalibrierung, Warm-Worker-,
Setter-/Hook-, generelle Consumer- oder Karrierefreigabe.

## Unveränderte Quellen und vorab festgelegte Inputs

Ausführungscommit `0744238cbcbd429dd59602f0470b18a1d9f52057`; erfolgreiche
[CI43636256046](https://github.com/Matchekk/FM-27-Research/actions/runs/43636256046)
mit exakt diesem SHA unabhängig abgefragt. Alle22 CODE-Gitblobs stimmen mit
`inputs.json` und `registration.json` überein. Zum Prüfzeitpunkt stimmen zusätzlich
alle22 heutigen Dateien damit überein, einschließlich Masterrouter-SHA256
`63bbf08ce8d19474bba956140deca44ab43cef70f7c719cec229090d10148791`.
Input-, Seed-, Job- und Reviewgate-Dateien stimmen mit ihren veröffentlichten
Gitblobs überein. Spätere Plattformänderungen gehören zu einer neuen Sourcegeneration.

Die acht privaten Binaries wurden unabhängig als5557 geordnete Records
rekonstruiert. Die vier Highinputs entsprechen vollständig den historischen
D00-Bytes. In jeder Lowvariante ändern sich exakt20 Werte: ausschließlich Kind15,
Felder16/17, bei den zehn tatsächlichen absoluten Kind11-Feldstartern der getesteten
Seite. Header, Reihenfolge und alle anderen Records bleiben gleich. Torwart,
Bank, Gegner, Attribute, Condition, Fatigue, übrige Profile, Taktiken, Phasen,
Rollen/PI, Management und Kind62-Version bleiben kontrolliert. Kein Kind61-Record.

Private Registry, privater und öffentlicher Seedplan sind gleich. Die
historischen/anderweitig reservierten Werte wurden erneut aus den vorgesehenen
öffentlichen und privaten JSON-/JSONL-Bereichen inventarisiert:2524 Ausschlüsse,
Set-SHA256 `72ac0a590b160d830448d26b50e24d5cf6eed060b6b5197441b408c0e0ca54cd`.
Die Namespace-/SHA256-Allokation wurde unabhängig rekonstruiert und liefert die
vier disjunkten nichtnull-uint32-Seeds in der vorab festgelegten Reihenfolge:

| Kontext | getestete Seite | Seed |
| --- | --- | --- |
| high_press | 0 | 1872406977 |
| high_press | 1 | 1245076665 |
| deep_block | 0 | 2075475079 |
| deep_block | 1 | 999124409 |

Der vorhandene Observerhost hat weiterhin SHA256
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`.
Seine tatsächlichen C++-/Headerbytes passen zum unveränderten privaten
Buildmanifest und zum eingefrorenen öffentlichen Header. Die DLL-Identität
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`
steht zusätzlich in jedem tatsächlichen nativen Imagefingerprint. Keine neue
native Schreibmethode oder Instrumentierung gegenüber dem vorgeprüften Host;
der Eingriff läuft vor Originalvorbereitung über die vorhandenen Profilrecords.

## Nachrechnung der Rohzustände

Der private17-Zeilen-Ledger entspricht vollständig den öffentlichen Messungen.
Alle geplanten Schlüssel, Reservierungen und Zustände stimmen;16 erfolgreiche
Vollmatches und eine erwartete Negativabweisung, keine Ausfälle, fehlenden
Messungen, Retries oder Ersatzseeds. Native Seeds, tatsächlich5557 gelesene Records,
Originalvorbereitung, natürliche Enden und Originalteamstatistiken sind direkt
an die jeweiligen Rohereignisse gebunden. Nachgerechnet wurden:

| Prüfung | tatsächlicher Umfang |
| --- | ---: |
| Attribute in nativen Inputdumps | 50.784 |
| Profilwerte in nativen Inputdumps | 16.928 |
| Positions-/Rollen-Phasenzellen | 704 |
| PI-Gruppen | 11.968 |
| passive Snapshots, je46 eindeutig zugeordnete Actors | 48 |
| gesamte Actor-/Stagebeobachtungen | 2.208 |
| Anfangssnapshots: prepared und first_advance | 32 |
| Target-Actor-/Stageprüfungen, je zehn Feldstarter | 320 |
| tatsächliche Anfangscaches der22 Starter | 704 |

Für alle Anfangsactors sind Condition10000, Fatigue0, Akkumulator1000000 und
Abzug0 bestätigt. Low trägt ausschließlich bei den zehn Targetfeldstartern
beide Rohwerte7000 und Startercache8A70. High beziehungsweise alle unveränderten
Actors tragen Rohwerte10000; ihre vorhandenen Startercaches8A betragen100.
Startercache89 bleibt100. prepared liegt bei Tick0,
first_advance ist die erste erfolgreiche Anforderung0→1 mit Ordinal1.
Prepared-Rohprofile und33TF-Bytes stimmen zusätzlich mit dem vollständigen
Inputdump überein. In jedem Snapshot bestehen40 Cachebeobachtungen und sechs
explizite Nullcaches; alle22 tatsächlichen Startercaches sind vorhanden.

Acht A/A-Paare stimmen exakt in Score, Endtick, Clock und allen sieben
Originalteamstatistikfeldern überein. Zusätzlich stimmen alle drei Stages in
identifizierten Rohprofilen, Akkumulator/Abzug,33TF-Bytes, Cache89/8A,
Identitäten, Stage-/Fortschrittsangaben und Matchversion überein. Das112Byte-
Fenster wird entsprechend Vorregistrierung nicht als A/A-Endpunkt verwendet.
Acht separate High/Low-Kontrollpaare stimmen in beiden Anfangsstages bei allen46
Identitäten und sämtlichen nicht intervenierten Anfangsfeldern einschließlich
33TF-Bytes überein. Matchversion bleibt0x1b000000; diese Rohbeobachtung beweist
keinen deaktivierten TF-Consumer oder eine UI-Familiarityskala.

Finished-Beobachtungen werden vollständig erhalten, ohne Low=7000 zu verlangen.
Über alle Finishactors beträgt rawC90 mindestens7783, rawC7A mindestens7000 und
der Conditionakkumulator mindestens683585. Die tatsächliche Entwicklung ist mit
einem unveränderten ursprünglichen Enginepfad vereinbar; ein dauerhafter
Low-Clamp wurde weder eingeführt noch als Gate verlangt. Aus High/Low-Resultaten
dieser technischen Stichprobe wird kein Leistungs- oder Effektbefund abgeleitet.

## Negative Probe, Bereinigung und Budget

Die seedlose defekte Eingabe endet mit108, genau einem `scenario_rejected` im
Originalstage `initial` und ohne natürliches Matchende. Alle17 Kernelreceipts
bestätigen Kapselexit und aktive Prozesszahl0, Limit3, Kill-on-close und kein
Breakaway. Prozesszugehörigkeit vor GO ist jeweils bestätigt. Die aufgezeichneten
Aufrufintervalle überlappen nicht: ein serieller Worker. Kein zusätzlicher
Loader- oder Capabilityaufruf gehört zu diesen17 Versuchen.

Das private Budget hat exakt eine erfolgreiche technische Operation, exakt17
Reservierungen, kein Main, kein active/halted oder Cleanupmarker; die globale
NativeLease ist freigegeben. Tatsächliche Childbelastung58,0844142s≤180s.
Das feste900s-Fenster läuft von20:15:53.528385 bis20:30:53.528385UTC;
Finalreconciliation20:16:51.631878UTC liegt darin. Der private Budget-SHA256
`dccd774c8a5a09b564a868c8f0e0f0748bd13c0340ff9f36fb93c2295c884361`
stimmt exakt mit Finalreceipt und öffentlichem Budget überein. Keine Rückerstattung,
verlängerte Uhr, neue Operation oder Verschiebung aus der geschlossenen Staminastudie.

Reproduzierbarer eigener Lesepfad:
`analysis/review_night001.py --startpolicy-runs-root <central-root>`.
108 private Roh-/Metadateien sind über Namen und echte SHA256 gebunden; der
kanonische Manifest-SHA256 ist
`45727b961bba03305add0a1ea720752d5076eaf6debe527f8f2c9928567ea4a1`.
Rohbytes, Trägeridentitäten, Prozess-/Pfadtexte und private Dateiliste bleiben lokal.
Keine Native-/Saveöffnung, Registryänderung oder Seedreservierung durch den Reviewer.

Ergebnis: der ursprüngliche **gemeinsame Zwei-Feld-Inputpfad und serielle
Cold-Caller** bestehen diesen technischen Test. UI, Warmbetrieb, Karriere,
allgemeine Consumersemantik und wissenschaftliche Mainzulassung bleiben getrennte
ungeprüfte beziehungsweise gesondert zu prüfende Fähigkeiten.

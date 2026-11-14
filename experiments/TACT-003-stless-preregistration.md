# TACT-003-STLESS-R0: IP/OOP-Pakete eines stürmerlosen Systems

Vorregistrierung vom 14.11.2026 für die eigenständige Mission NIGHT-002.
**Entwurf bis Veröffentlichung, Codefreeze, erfolgreicher CI und unabhängiger
Abnahme; keine Hauptmatchfreigabe durch dieses Dokument allein.**
Manifest und spätere Messungen: `data/night-002-stless003/`.
[Reiner Compiler/Vertrag](../analysis/stless003_design.py) ·
[eingefrorene Analyse](../analysis/analyse_stless003.py) ·
[Design und Quellenvergleich](../docs/night-002/STLESS003-DESIGN.md).

## Frage, Neuheit und getesteter Kontext

**Hypothese:** Der Effekt des deklarierten stürmerlosen IP-Pakets auf xGD
unterscheidet sich zwischen unverändertem OOP4411 und dem deklarierten OOP4420-Paket.
Ein positiver Interaktionswert bedeutet einen größeren IP-Paketeffekt bei OOP4420.
Der zweiseitige Test erlaubt ausdrücklich beide Richtungen.
Ein positiver DoD kann auch aus zwei negativen einfachen IP-Effekten entstehen
und beweist weder einen stürmerlosen Sieger noch Überlegenheit gegenüber D00.

Novelty-Kandidat `N2-02`, Entscheidung `NOVEL_HYPOTHESIS` innerhalb der tatsächlich
geprüften Literatur. Überschneidungen: `MAC-06`, `MAC-07`, `MAC-07B`, `MAC-19`,
`FM27-FMAX-LAB`, eigenes `TACT-002-R0`. Die externen Quellen vergleichen
Gesamttaktiken; TACT-002 veränderte Rollen innerhalb fester IP/OOP-Positionen.
Hier werden vorab eng definierte IP- und OOP-Pakete gekreuzt. Die Änderung ist
kein unverändertes Ranking und identifiziert keinen einzelnen Rollenmechanismus.
Originalquellen und aktueller Patchstand sind im
[NIGHT-002-Quellenaudit](../docs/night-002/LITERATURE_AUDIT.md) dokumentiert.

Pflichtkontext: FM27 `27.0.1+2503222`, Engine-SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`,
unveränderter passiver Observerhost
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`,
lokal validierter Tactics-Lab-Quelltag `v1114.6`/Commit
`91f2eba57fac0b7fbd3dff616056907e3ce461be`. Fixture, Katalog, Ressourcen und
alle tatsächlich verwendeten Quellen werden vor Vorbereitung/jeder Phase
erneut gegen ihre gespeicherten Hashes geprüft. Ein abweichender Build stoppt
die Studie. Es wird kein neuer Host gebaut oder fremdes Projekt importiert.

## Interventionen und konstante Eingaben

Vier Arme in verbindlicher Reihenfolge:

| Arm | IP-Paket | OOP-Paket | Geänderte Originalrecords gegenüber D00 |
| --- | --- | --- | ---: |
| I0-O0 | IP4231 unverändert | OOP4411 unverändert | 0 |
| I1-O0 | IP4240 | OOP4411 unverändert | 3 |
| I0-O1 | IP4231 unverändert | OOP4420 | 3 |
| I1-O1 | IP4240 | OOP4420 | 6 |

**IP4240:** Der ursprüngliche Akteur in Startslot8 zieht von AMC nach AMCL und
behält `AttackingMidfielder`. Der ursprüngliche Akteur in Startslot10 zieht
von ST nach AMCR; `CentreForward` wird `SecondStriker`.
**OOP4420:** Dieselben ursprünglichen Akteure werden von AMC/ST nach AMCL/AMCR
gesetzt, beide mit `OPAttackingMidfielder`. Die ursprüngliche seitenspezifische
OOP-Permutation bestimmt die nativen Records; Akteure werden nicht ausgetauscht.

Das erste Paket verändert zwei IP-Positionen und eine IP-Rolle, das zweite
zwei OOP-Positionen und eine OOP-Rolle. Es ist ein kausaler **Paketvergleich**.
Position, Rolle, intrinsisches Rollenverhalten, Bewegungen oder interne
Complexity werden nicht als getrennte Mechanismen identifiziert.
Die nativen Readbacks beweisen zugewiesene Positionen/Rollen und deren
Actorbindung; tatsächliche Laufwege werden in diesem Experiment nicht gemessen.

Kontrollarm I0-O0 ist in jeder Zelle bytegleich D00. Alle sonstigen Records
bleiben gleich: Anzahl/Reihenfolge5557, Identitäten,23 aktive Spieler je Seite,
anfängliche Startelf,69 Attribute und23 Profilfelder je Akteur, Keeper/Bank,
Gegnerprofile, Team Instructions, Mentalität, explizite PI/Targets/Duties,
Spielmanagement, Matchumgebung und Seed. Zehn Feldstarter besitzen dieselben
omnipotenten Positionsratings; kein geänderter Eignungswert oder Stärkeboost.
Alle46 kodierten Staminawerte bleiben60. Die getestete Seite behält Standardpressing;
der Gegner sein eingefrorenes Profil. Intrinsische Rollenweisungen sind Teil des
Pakets; explizite PI0 behaupten ihre Abwesenheit nicht.

## Stichprobe, Seeds und Reihenfolge

Technik: vier neue Seeds, je bekanntem Kontext×Seite einer. Alle16 Eingabezellen
zweimal auf demselben zugeordneten Technikseed:32 Vollmatches,16 exakte A/A-Paare;
anschließend eine separate erwartete Negativabweisung. Keine technische
Leistungsmessung wird in die wissenschaftliche Effektschätzung aufgenommen.

Main nur nach eigener neuer technischer Freigabe:32 neue Seeds je `high_press`
und `deep_block`; je Seed vier Arme auf beiden Seiten. **512 Hauptmatches,
64 unabhängige Seedblöcke.** Seiten werden innerhalb eines Seeds gemittelt;
die beiden festen Kontexte erhalten je Gewicht½. Es sind keine512 unabhängigen
Replikate und keine zufällig gezogene Gegnerpopulation.

Eigene Namespaces `TACT-003-STLESS-R0/main-v1` und `/technical-v1`, insgesamt
68 neue disjunkte uint32-Seeds. Historische, fehlgeschlagene, technische,
reservierte und terminal unbenutzte Seeds bleiben ausgeschlossen. Keine
automatische Wiederverwendung, Ersatzseeds, Retries, Holdouts oder Seedauswahl
nach Ergebnissen. Die Registry reserviert erst nach Literatur-/Freigabeprüfung.

## Endpunkte und eingefrorene Auswertung

Ein Primärtest, zweiseitig α0,05:

`INTERACTION:xgd = (I1O1−I0O1) − (I1O0−I0O0)`

Koeffizienten in der Tabellenreihenfolge `(1,−1,−1,1)`. Dies ist die volle
physische Differenz der Differenzen, kein halbierter faktorieller Koeffizient.
xGD wird aus ursprünglichem Team-xG als xGF−xGA berechnet.

Eine vollständige sekundäre Holm7-Familie:

1. Marginaler IP-Paketeffekt auf xGD, Koeffizienten `(−½,+½,−½,+½)`.
2. Marginaler OOP-Paketeffekt auf xGD, Koeffizienten `(−½,−½,+½,+½)`.
3. Derselbe INTERACTION-Kontrast auf tatsächliche Punkte3/1/0.
4. INTERACTION auf erzielte Tore.
5. INTERACTION auf tatsächliche Gegentore.
6. INTERACTION auf xGF.
7. INTERACTION auf xGA.

Positive GA/xGA-Werte bedeuten mehr Gegentore/Chancenabgabe. Alle sieben
Sekundärtests werden einschließlich negativer/unklarer Resultate veröffentlicht.
Keine nachträgliche günstigste Metrik oder Armauswahl.

Welch-/Satterthwaite95%-Intervalle für feste gleiche Kontextgewichte;
stratifizierter20.000-Seedblock-Bootstrap als festgelegte Sensitivität. Gleiche
Seeds bedeuten keine identischen Matchereignisse. Kontext-/Seitenmittel, deren
SD/Kovarianz, Leave-one-seed-out, Armmittel und passive Cache-/Rohzustände sind
rein explorativ/deskriptiv. Endliche ursprüngliche Score-/Statistikwerte und
natürlicher Matchabschluss werden pro Lauf geprüft. Nullimputation ist verboten.

Praktische Referenz: Betrag0,20xGD der Interaktion; gewünschte volle primäre
95%-Intervallbreite≤0,50. Die unbekannte Kontrastvarianz verhindert eine
90%-Powergarantie. Bei gleicher Block-SD0,6/1,0/1,5 wären unter dem Modell
volle Breiten0,300/0,500/0,750 und Power für0,20 von74,7%/35,0%/18,3% zu erwarten.
Ein Pilot mit breitem Intervall wird nicht wegen knapper Nichtsignifikanz
automatisch erweitert. Zukünftige Fallzahlen sind bedingte Planung, kein Auftrag.
Nichtsignifikanz beweist weder Wirkungslosigkeit noch Äquivalenz.

## Technische Gates, Fehler und Abbruch

Vor Main erforderlich: veröffentlichte unveränderte Vorregistrierung/Analyse,
erfolgreiche CI, unabhängiger Code-/Inputreview, eigener nativer TECH32+1-Lauf,
unabhängiger Rohreview und veröffentlichte technische Freigabe mit erfolgreicher CI.
Eine historische TACT-/MECH-Freigabe ersetzt diese neue Paketabnahme nicht.

Der reine Compiler prüft die originale statische Rollen-/Positionseignung,
beide vollständigen69er-Attributsätze, ursprüngliche44 Rollen-/44 Positionsrecords,
OOP-Permutationen und alle übrigen Records. Nur Kind4/5 dürfen sich ändern.
Originale native `game_constraints` bleiben auf beiden Seiten eingeschaltet;
die Engine muss neue Rollen-/Positionskontexte akzeptieren. Nach Originalvorbereitung
müssen Eingaben, tatsächliche Actor-/Phasenbindung,1058 Profilfelder,3174
Attributwerte,44 Phasenzellen und748 PI-Gruppen dem Plan entsprechen.

Alle16 A/A-Paare müssen Endstand, ursprüngliche Statistik und identifizierte
passive Zustände exakt reproduzieren. Nach Vorbereitung und erstem tatsächlichem
Fortschritt müssen Startzustände und unveränderte Raw-TF33-Kontrollhashes der
jeweiligen eingefrorenen D00-Zelle entsprechen. Jede Abweichung stoppt diese
Studie; sie wird nicht nachträglich als erlaubte Paketänderung umdefiniert.
Die negative Binärprobe verlangt Exit108, genau ein `scenario_rejected` und
keinen natürlichen Abschluss.

Ein fehlender/duplizierter Job, Seed-, Build-, Input-, Legalitäts-, Readback-,
Ressourcen- oder Wiederholbarkeitsfehler stoppt neue Zulassungen. Bereits
zugelassene Calls werden beaufsichtigt bereinigt/abgerechnet. Alle Fehler,
unbegonnenen Jobs und Abbrüche bleiben erhalten. Keine Ausschlüsse nach
Ergebnis; bei unvollständigen512 Hauptmatches nur technischer Zwischenstand.

## Eigene und globale Ressourcen

Studie: maximal512 wissenschaftliche und32 technische Vollmatches plus eine
Negativabweisung,900 kumulierte beaufsichtigte Childsekunden,5400 Sekunden
unveränderliches UTC-Fenster ab erstem nativem Technikcall,2GiB neue private
Artefakte,20GiB freie Diskreserve,90s Fortschrittstimeout, maximal vier kalte
Worker, pro Call bestehende Job3-Prozesscontainmentregeln.

Zusätzlich gilt vor dem ersten TACT-Seed und jedem nativen Call eine strengere,
eigenständige Zulassungsgrenze: `per_call_absolute_timeout_seconds=30`,
`per_call_reserved_envelope_seconds=40`,
`global_native_call_elapsed_limit_seconds=3600`. Der enthaltene Call erhält
`total_timeout=min(verbleibende_Zulassung,30)`; das40-Sekunden-Envelope reserviert
zusätzlich Zeit für die begrenzte Prozessbereinigung. Dieser absolute Timeout
ist enger als der weiterhin konfigurierte90-Sekunden-Fortschrittstimeout.

Vor jedem Claim prüft der Scheduler unter seiner zentralen Zulassungssperre:

`Summe_abgeschlossener_Calls_früherer_Studien + Summe_eigener_abgeschlossener_Calls + 40 × (eigene_gestartete_Jobs − eigene_aufgelöste_Ledgerjobs + 1) ≤ 3600`

Die erste Summe stammt aus der geschlossenen ersten NIGHT-002-Studie; die
zweite aus tatsächlichen `native_elapsed_seconds` der eigenen Dispatchledger.
Die40-Sekunden-Reservierung umfasst jeden noch unaufgelösten begonnenen Job
und den zusätzlich beabsichtigten Claim. Tatsächliche Aufrufzeiten werden
dauerhaft berechnet, auch bei Fehlern. Der Wechsel von einer Reservierung
zur tatsächlich gemessenen abgeschlossenen Aufrufzeit ist eine Abrechnung
des Envelopes, keine Rückerstattung bereits belasteter Zeit. Ein Fehler
bleibt terminal und begründet weder Retry noch Budgetneustart.

Diese zusätzliche Summengrenze ersetzt oder definiert die vorhandene globale
3600-Sekunden-Abrechnung ganzer beaufsichtigter Phasen nicht neu. Eigene
900 Childsekunden, unveränderliches5400-Sekunden-Fenster und600-Sekunden-
Mainrestgrenze bleiben gleichzeitig bindend. Neuer Runner und unabhängiger
Review müssen die Timeout-/Bereinigungshülle vor nativer Freigabe bestätigen.

Erste Mainadmission braucht mindestens600 Sekunden Rest in eigenen und globalen
Child-/UTC-Budgets, erneut unmittelbar vor dem ersten Call geprüft. Ein zentraler
Supervisor/exklusive NativeLease, keine gleichzeitig laufende andere native Phase.
NIGHT-002 bleibt zusätzlich bei2048 Main/192 technischen Vollmatches insgesamt,
3600 Childsekunden,4GiB privaten Artefakten und spätestens15.11.2026 08:00CET
(`07:00Z`) begrenzt. Die Maxima sind keine Arbeitsziele. Kein altes NIGHT-001-
Budget/Deadline/Seed wird reaktiviert oder umetikettiert.

## Publikation und Grenzen

Öffentlich: Setup-/Quellhashes, Build-/Adapteridentität, reservierte Seeds,
Sanitized Matchresultate, vollständige Job-/Budgetabrechnung, Blockkontraste,
Auswertungscode, Review-/CI-Belege und Ergebnisbericht. Native Dumps, DLLs,
Fixtures, Spieleridentitäten und persönliche lokale Pfade bleiben privat.
Keine Änderung oder Simulation eines echten Karrieresaves.

Ein gebündeltes Fixture, zwei bekannte Gegner und omnipotente synthetische
Profile begrenzen die Übertragbarkeit. Das Paket kann intrinsische Rollenbewegung
und situationsabhängige Reaktion des originalen Managements enthalten. Keine
universelle Formationsempfehlung, kein unabhängiger Karriere-/Trainingsnachweis,
kein Nachweis einer isolierten Rolle oder einer OP-Mechanik. Meta-Score v0.1
wird aus diesen Taktikdaten nicht neu gewichtet.

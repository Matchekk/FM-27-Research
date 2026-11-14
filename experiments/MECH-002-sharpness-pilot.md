# MECH-002-SHARPNESS-P0: Originales Startpaket × Pressing

Stand2026-11-14: **Vorregistrierungsentwurf, blockiert bis TECH17 tatsächlich
bestanden und unabhängig veröffentlicht freigegeben ist.** Dieser Fachauftrag
startet keine nativen Prozesse und reserviert keine Seeds. Der terminal geschlossene
MECH-003-Staminaversuch wird weder fortgesetzt noch neu gestartet. Dies ist eine
andere, vorab definierte Intervention mit eigenem Namespace und eigenen Budgets.

## Fragestellung und Behandlung

Wie verändert das verifizierte originale Rohwert-Startpaket10000 gegenüber7000
das mittlere xGD, gemittelt über zwei Pressingstufen, bei unveränderter D00-Taktik?
Ziel ist der totale Matcheffekt eines gemeinsam veränderten Zwanzig-Record-Pakets,
kein isoliert bewiesener Consumer-, Mental-, Ermüdungs- oder Mediationsmechanismus.

| Arm | Beide Raw-Profilfelder16/17 | TriggerPress Gruppe10 | Native Bit |
| --- | ---: | --- | ---: |
| S70-P0 | 7000 | Standard, ID1313689463 | 0 |
| S100-P0 | 10000 | Standard, ID1313689463 | 0 |
| S70-P1 | 7000 | MoreOften, ID2000905329 | 66 |
| S100-P1 | 10000 | MoreOften, ID2000905329 | 66 |

Die Namen S70/S100 sind Rohpaket-Kürzel und keine kalibrierte FM-UI-Prozentskala.
Zehn getestete Startfeldspieler, über absolute `lineup[1:]`-Records identifiziert,
erhalten beide Rawfelder gemeinsam. Torwart, Bank, Gegner, weitere Profilwerte,
Attribute und Positionsratings bleiben unverändert. **Stamina52 bleibt in allen46
kodierten aktiven Spielern beim ursprünglichen raw60**, genau23 Records je Seite.
Weitere Trägerslots werden nicht als Attributrecords übergeben; für sie wird kein
kodierter Staminawert behauptet. Die Factory schreibt keine Records für diese Slots.

D00-IP4-2-3-1 und OOP4-4-1-1, Rollen, PI, Mannschaftsstärke, beide Taktikphasen,
Aufstellung und Matchmanagement bleiben innerhalb eines Kontexts gleich. Keine
externen Wechsel/Shouts/Liveanpassungen oder Karrierefortschreibung; die eingefrorene
ursprüngliche native Matchmanagementpolitik wird beibehalten und gehasht.
Zwei bekannte Discoverygegner `high_press` und `deep_block`; keine Holdouts.

## Native Voraussetzungen und vollständige Kontrollen

Voraussetzung: `MECH-002-STARTPOLICY-TECH-V1` (TECH17) mit seinen17 Versuchen ist
tatsächlich bestanden, parentseitig abgeglichen, unabhängig reviewed und am exakten
publizierten Freigabecommit mit erfolgreicher CI abgenommen. Draftbooleans oder
Quellenplausibilität ersetzen diese Freigabe nicht. Der registrierte Vertrag
bindet TECH17-Summary-/Reviewhash, vollen Releasecommit und erfolgreichen CI-Run.

Unveränderter Observerhost:
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`.
Keine neue C++-Änderung, kein neuer Setter, keine Kind61-/Executionrecords,
kein permanenter Clamp und keine Warmworker. Aktuelle Engine-, Adapter-, Fixture-,
Ressourcen-, Katalog-, Quellen- und Buildmanifesthashes müssen vor Ausführung
mit dem separat freigegebenen technischen Kontext übereinstimmen. Die in früheren
Dokumenten genannte Version allein ist keine neue Liveprüfung.

Der bestehende originale Codec überträgt Profilrecords vor der Originalvorbereitung.
Er wird nicht nachträglich als post-preparation Setter bezeichnet. Explizit10000
muss bytegleich mit D00 sein. Raw7000 verändert genau20 Werte, unveränderte5557
Recordpositionen/-anzahl. Der MoreOften-Carrier stammt aus publiziertem MECH-003-R01;
vor Verwendung müssen dessen genau zehn Stamina40-Werte auf60 zurückgeführt werden.
Danach darf er sich von D00 ausschließlich im einen Pressingrecord unterscheiden.
Alle Quellen- und Ergebnisbytes werden gehasht. Keine anderen Trägereingriffe.

Jeder neue Vollmatch benötigt die originalen Readbacks: alle3174 aktiven
Attributwerte,1058 Profilfelder,44 tatsächliche Phasen-/PI-Zellen,748 PI-Gruppen,
absolute Spieleridentität, Setup, kontrollierten wirksamen Seed und natürliches
Matchende mit Score und Originalstatistik. Prepared und erster echter Advance
müssen bei46 Akteuren C90/C7A und die unveränderten Kontrollfelder zeigen;
bei22 Startakteuren die tatsächlichen Caches89/8A. Die zehn Testfeldspieler tragen
das deklarierte Rohpaket und Cache8A70 oder100, andere Akteure bleiben bei10000.
Condition10000, Fatigue0, Accumulator1000000, Penalty0 und die rohe TF33-Region
müssen initial den eingefrorenen Kontrollen entsprechen. Keine UI-/Consumerlabels
werden aus den Raw-/Cachezahlen abgeleitet.

## Stichprobe, neue Seeds und Technikreihe

**32 neue Seeds pro Gegnerkontext**,64 unabhängige Seedblöcke. Jeder Block enthält
vier Arme auf beiden Teamseiten:512 Hauptmatches. Kontexte haben Gewicht1/2,
Teamseiten Gewicht1/2 innerhalb des Seeds. Gemeinsame Seeds kontrollieren einen
Startzustand, garantieren jedoch keine identischen Ereignisfolgen zwischen Armen.

Separat vier weitere neue technische Seeds, einer je Kontext×Seite:32 technische
Vollmatches,16 exakte A/A-Paare über alle16 Eingabezellen, plus eine Negativkontrolle
mit Exit108, eindeutigem `scenario_rejected` und ohne natürlich beendetes Match.
Gesamt:68 neue Seeds und545 Match-/Negativplätze. Ein vorher erforderlicher
Loadercheck darf ausschließlich aus separat eingefrorener, weiterhin gültiger
Exact-Host-Abnahme stammen; ein versteckter neuer Loader-/Capabilityaufruf ist
unzulässig. Jeder weitere native Prozessaufruf wäre gesondert zu registrieren.

Namespace `MECH-002-SHARPNESS-P0/main-v1`, Technik entsprechend `/technical-v1`.
Ausgeschlossen werden alle historischen, technischen, fehlgeschlagenen und bereits
reservierten Seeds sowie alle laufenden Registryreservierungen. Insbesondere:
alle vier TECH17-Seeds, alle64 unbenutzten terminal reservierten Stamina-Mainseeds,
alle vier neuen Schärfe-Technikseeds gegenüber Main und alle Holdout-Seedmetadaten.
Holdoutgegner bleiben ungeöffnet. Keine Wiederverwendung, Ersatzseeds, Retries,
Rückerstattung von Versuchen oder automatische Vergrößerung.

## Primärkontrast und Unsicherheit

Ein vorregistrierter zweiseitiger Primärtest: marginaler raw10000−7000-Effekt
auf xGD (xGF−xGA). Armanordnung `[S70-P0,S100-P0,S70-P1,S100-P1]`.
Koeffizienten `[-.5,+.5,-.5,+.5]`. Zuerst den Kontrast je Seite/Seed bilden,
danach beide Seiten mitteln, dann die beiden Kontextmittel gleich gewichten.
64 Seedblöcke sind die unabhängigen Replikate;512 Matches werden nicht als512
unabhängige Einheiten behandelt.

Berichtet werden Mittelwert, gepaarte Kontext-SD, zweiseitiges95-%-Welchintervall
mit Satterthwaite-Freiheitsgraden und zweiseitiger p-Wert. Zusätzlich20.000
stratifizierte Bootstrapziehungen vollständiger Seedblöcke, deterministischer
namespacebasierter Bootstrapseed. Bootstrapintervalle sind zusätzliche Unsicherheits-
darstellungen, keine zweite unabhängige Stichprobe oder weitere Signifikanzfamilie.
Kontext-/Seitenschätzungen, Seitenkovarianzen und Leave-one-seed-out-Spannweite
werden ausdrücklich explorativ ausgewiesen.

Genau eine **Holm7-Sekundärfamilie**:

1. Schärfepaket: tatsächliche Punkte pro Match.
2. Schärfepaket: erzielte Tore.
3. Schärfepaket: Gegentore.
4. Schärfepaket: xGF.
5. Schärfepaket: xGA.
6. Pressing: xGD, Koeffizienten `[-.5,-.5,+.5,+.5]`.
7. Schärfepaket×Pressing: xGD, physische DoD `[+1,-1,-1,+1]`.

Der eine Primärkontrast gehört nicht zur siebenfachen Sekundärfamilie.
Keine zusätzlichen Signifikanztests der folgenden deskriptiven Größen.

## Eingefrorene Plausibilitäts-/Deskriptivfamilie

Jeweils Mittelwerte der zehn getesteten Startfeldspieler:

- `prepared_condition_cache89_mean`, `prepared_sharpness_cache8a_mean`.
- `first_condition_cache89_mean`, `first_sharpness_cache8a_mean`.
- `finished_condition_cache89_mean`, `finished_sharpness_cache8a_mean`.
- `prepared_tf33_matches_frozen_d00`, `first_tf33_matches_frozen_d00`:
  boolescher initialer Vergleich aller46 Akteure, kein Familiarity-UIwert.
- `finished_tf33_distinct_hashes`: Anzahl verschiedener SHA256 der33 Rawbytes bei
  den zehn Testakteuren. Das All-zero-Muster zählt als ein Muster; niemals als
  fehlende oder null Familiarity interpretieren.
- `finished_condition_raw_mean`, `finished_sharpness_raw_mean`,
  `finished_sharpness_secondary_raw_mean`, `finished_fatigue_raw_mean`,
  `finished_condition_accumulator_raw_mean`, `finished_sharpness_penalty_raw_mean`.

Nur die zwei Finished-Cachemittel dürfen bei tatsächlich nicht verfügbarem Cache
`null` mit explizitem Grund sein. Fehlende Initialreadbacks oder Profile blockieren.
Öffentlich nur erlaubte Messgrößen, Hashes, Fehlstellen und Gründe; keine privaten
Spieler-IDs, Rohregionen oder Spieldateien. Keine Consumer-/Mediationsaussagen.

## Präzision, Power und weitere Entscheidung

Varianzpilot, **keine90-%-Powergarantie**. Praktische Referenz0,30xGD;
gewünschte volle95-%-KI-Breite0,50. Die Kontrastvarianz ist vor Main unbekannt.
Nach vollständiger Serie bedingte Planung für neue Bestätigungsseeds bei
Effektgrößen0,20/0,30xGD und90% Power: beobachtete Kontext-SD sowie simultane95-%-
Normalmodell-SD-Obergrenzen (je97,5%,df31). Nichtzentrale Welchapproximation,
gleiche feste Kontextgewichte; n neue Seeds je Kontext kosten2n unabhängige
Blöcke und16n Matches. Diese Planung löst keine Folgeausführung aus.

Kein Kandidat, Sieger, neues Attributranking oder optimaler Pressingplan wird
ausgewählt. Keine Holdout-/Karrierebestätigung und keine allgemeine Übertragbarkeit
aus zwei synthetischen Gegnerkontexten. Technische A/A-Ergebnisse werden nur
für Reproduzierbarkeit/Inputfreigabe verwendet, nicht zur Dosis-/Armauswahl.

## Ressourcen, Freigabe und Ausfälle

Ein nativer Supervisor mit globaler NativeLease, maximal vier **kalte** Worker,
90s ohne Fortschritt je Worker. Eigene Grenzen:900 überwachte Childsekunden,
3600s feste UTC-Frist. Das eigene Zeitfenster beginnt erst mit dem ersten nativen
Technikaufruf; inerte Vorbereitung startet es nicht. Anschließende Publikations-,
Review-, CI- und Verwaltungszeit zählt zur UTC-Frist. Zusätzlich NIGHT-Master:
1800 Childsekunden und harte Deadline2026-11-14T23:00:00Z. Kein Budgetreset.
Private Rohartefakte höchstens2GiB, freier Speicher mindestens20GiB.

Vor Main müssen mindestens600s sowohl eigener als auch globaler Childallowance
und sowohl eigener als auch globaler UTC-/Deadlinezeit verbleiben. Fehlt irgendein
Budget oder Gate, Main nicht starten. Ressourcengates und Parentabrechnung sind
vor Veröffentlichung durch den separaten Runner/Verifier zu belegen; eine reine
vollständige Datentabelle genügt nicht als Ressourcenfreigabe.

Vor Technik: tatsächliche TECH17-Freigabe, unveränderte Identitäten, veröffentlichte
Vorregistrierung, Code, Inputs, neue Seedreservierung, Inputreview und exakte
erfolgreiche Publikations-CI. Vor Main zusätzlich32/32 valide eigene Technikmatches,
16 A/A-Paare, Negativabweisung, abgeglichene Budgets, eigenständiger Technikreview,
veröffentlichte technische Freigabe und deren erfolgreiche exakte CI.
Reviewhashes binden Inputs/Manifest, ohne zyklische Selfhashes.

Erster Input-, Identitäts-, Seed-, Readback-, Prozess-, Cleanup- oder Budgetfehler
stoppt die Serie. Alle begonnenen, fehlgeschlagenen und unbegonnenen Jobs erhalten;
keine stillen Nullen oder Ergebnisausschlüsse. Nur vollständig gültige512 Mainmatches
und bestandene technische/Ressourcengates erlauben Effektauswertung. Andernfalls
ausschließlich technischen Status und545er-Ausfallabrechnung veröffentlichen.
Rohmaterial bleibt privat, erlaubte kompakte JSONL-Messungen öffentlich.

[Vertragsentwurf](../data/mech-002-sharpness-p0/contract-draft.json) ·
[Design/Compiler](../analysis/sharpness002_design.py) ·
[Analyse](../analysis/analyse_sharpness002.py) ·
[Planungsstatus](../docs/night-001/SHARPNESS-PLAN.md).

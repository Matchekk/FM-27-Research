# Agent 6 – Validation Engineer

Stand14.11.2026. **Technische Bestandsaufnahme und Offline-Vorarbeit; keine
nativen Starts, Seed-/Registryänderungen, Holdoutzugriffe oder Karriereausführung
durch diesen Agenten.** VALID-002 bleibt unverändert. P1C wird separat zentral
abgeschlossen. Neue wissenschaftliche Gates sind geplant, nicht bestanden.

## Forschungsfrage und Erkenntnisgewinn

Welche Spieler-, Start-, Fixture- und Ereigniszustände lassen sich schreiben
und nach Originalvorbereitung auditieren, damit realistische TACT/ATTR/MECH-
Vergleiche, Standards mit Exposition und kontrollierte TRAIN-Karriereversuche
möglich werden? Wichtigster Gewinn ist das Erkennen unwirksamer Eingriffe und
unbemerkter Normalisierung. Ein JSON-Schema oder erfolgreicher Reader genügt nicht.

## Identität und geprüfte Quellen

DLL rein lesend geprüft: FileVersion27.0.1, ProductVersion27.0.1+2503222,
SHA256 `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Lokale Upstream-Quellkopie: Commit91f2eba57fac0b7fbd3dff616056907e3ce461be,
v1114.6-Freigabestand. Kein Host zur erneuten Validierung gestartet.

Primärquellen dieses exakten Commits, read-only geprüft:

- [Fidelity](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/docs/SIMULATION_FIDELITY.md): nativer Detail-Matchloop und normalisierte Startprofile, keine nachgewiesene Gleichheit vollständiger Karriereabläufe. Maintainerbeschreibung, keine unabhängige Karriere-Leistungsstudie.
- [Servernormalisierung](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_tactics_server.py#L210), [Profilfelder](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_profiles.py#L23), [optionale Poolnormalisierung](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_tactic_pool.py#L171): tatsächliche Eingabepfade, keine Effektgrößen.
- [Host-Standardauswahl](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp#L847), [Episodenpfad](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_setpiece_episode.h) und [experimentelle Ausführungsreceipts](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/desktop_execution.py): mögliche Mess-/Interventionspfade, keine automatisch für unsere Forschung bestandenen Gates.

Lokale Runtime-Dateibyte-SHA256, Dateien unter `source/`:

| Datei | SHA256 |
|---|---|
| fm27_tactics_server.py | `5f2be140f30d576872351e7c397102b0b5a3de7d0b05f8d4e5011a65e94ea590` |
| fm27_profiles.py | `28f163f21c9aa80e9323e9b245127c3c48958218c1337cddb6ac6aae399c511f` |
| fm27_match_events.py | `3a2256a31c2be5dc98fc3d126ae5e861d09b640f75447945848a8c80d11fe3d9` |
| fm27_tactic_pool.py | `2de7d47bf9b040ac47547797524d415787aeb26234be008b7f745d39aa29aad0` |
| desktop_execution.py | `ac1589b5b23aac0ed5771dc8bb3e04b526d21996ba3d25357c9a477569a8311b` |
| desktop_generation_catalog.py | `d223a5077b454e2e07ac086192ce3b53fe5ceec95e1cd7fafa996aee4fa35724` |

## Technische Befunde und Forschungsgates

| Bereich | Tatsächlich geprüfter Stand | Konsequenz |
|---|---|---|
| Fitness/Schärfe/Moral | Runtime Server:210 normalisiert und überschreibt anschließend mit `CONTROLLED_START`; Profile:23 setzt condition/sharpness/sharpness_secondary10000, fatigue0, team_cohesion80, club_cohesion100, morale20. | Ein anderer gewöhnlicher JSON-Wert bewirkt noch keinen anderen Start. Neuer opt-in Schreibpfad und natives Nach-Vorbereitungsreadback nötig; keine stillschweigende Entfernung dieser Kontrollpolitik. |
| Spieler/Kapazität | Server:176 verlangt bundled_match_pkm; :198/:205 begrenzen Kader/Liste anhand DEFAULT, feste native IDs und69 Attribute. Upstream generation_catalog:63/:73 begrenzt bzw. schneidet Kader auf23. VALID-002: gespeicherter PKM-Transfer scheitert an Record17/Exit108. | Saveimport ist kein kapazitätserhaltender Karriereadapter. Kein stilles Abschneiden/Auffüllen oder Ersatzfixture. |
| Taktische Effektivität | `desktop_execution.py` prüft understanding/buy_in/opposition/ability und Records. Native experimenteller Build-/Samplerpfad kann Gesamtwert, buy_in/opposition oder33Bytes überschreiben. | Direkte experimentelle Komponenten und erlernte Karrierevertrautheit getrennt benennen. Ohne interventionsspezifischen Audit keine Freigabe. |
| Standards | Host:847–863 meldet ausgewählte Deadball-/Routinezustände mit Zustandskey-Deduplikation. Episodenpfad betrachtet erste passende Situation + Fenster und beendet ohne Vollmatch. Eventcollector reconciliert primär Tore/Karten. | Aus Routineauswahl oder einer Episode folgt kein Zähler aller tatsächlich ausgeführten Standards. Ausführung/Abbruch/Attribution/Exposition und Konterketten brauchen eigenen Nachweis. |
| Karriere/Training | `research/career.py` importiert vollständige Replikat×Arm×Woche-Checkpoints mit Kontrollhashes und Kalender-/Expositionsflags; liefert `automatic_game_execution_validated=False`. | Flags brauchen belegte Readerherkunft. Kein validierter Kalender-/Teilnahme-/Entwicklungsexecutor vorhanden. |
| Globale Koordination | Registry hat `.allocation.lock`, Budgets sind studienspezifisch; alte Spezialrunner haben keine gemeinsame globale Engine-Sperre. | Vier Worker pro Studie garantieren bei Parallelstudien keine globale Vierergrenze. Director serialisiert operativ; neue Runner brauchen gemeinsamen Lease-/Budgetpfad. |

### ATTR-009-Bridge: Positionseignung und GK separat auditieren

Gewöhnliche Servernormalisierung:208–210 übernimmt die ersten15 Attributwerte
als Positionsratings im Bereich0..20. Die IP/OOP-Vereinigungsmenge muss pro
nativer Spieleridentität unter Berücksichtigung des seitenabhängigen OOP-Slotmappings
gebildet werden, nicht aus ungeprüft gleichen Slotnummern. Hier werden **Positionsratings nicht durch
CONTROLLED_START überschrieben**; die separate Startprofilnormalisierung betrifft
andere Felder. Optionaler `away_tactic_pool.uniform`-Pfad (`fm27_tactic_pool.py:171–223`)
setzt dagegen aktive IP/OOP-Positionsratings auf20 und Fähigkeitindices15..68
pauschal. Er muss für den vorgeschlagenen Bridge-Versuch fehlen/deaktiviert sein,
mit Nachweis in normalisiertem JSON, Binärrecords und nativem Readback.

Mapping (`fm27_tactic_pool.py:10–14`): GK0, Sweeper1, DL2, DC3, DR4, DM5,
ML6, MC7, MR8, AML9, AMC10, AMR11, ST12, WBL13, WBR14. DCL/DCR und
DML/DMR sind jeweils dieselbe Ratingfamilie; „exakt beide Positionen“ meint die
Vereinigungsmenge ihrer Ratingindizes, nicht zwei künstlich unabhängige Werte.
Das öffentliche P1B-Profil enthält GK in Slots0/11 nur mit GK20 und sonst0;
Feldspieler haben GK/Sweeper0 und Positionsfamilien2..14 jeweils20.

Bridge-Gate: GK-Ratings/Spieleridentität und Abilitywerte konstant halten;
Feldspieler nur hinsichtlich vorab definierter ungenutzter Positionseignungen
ändern, aktive IP/OOP-Familien voll beherrschen lassen. Alle15 Ratings je Spieler,
69 Attribute insgesamt, native Slot-/Rosterbindung, beide Phasen und die
GK-Ausnahme nach Vorbereitung prüfen. Bestehender Attribute-/Phasendump hilft,
beweist aber nicht automatisch die **abgeleitete** taktische Effektivität.
Diese kann sich legitim mit Profil ändern; experimenteller_execution darf sie
nicht unbemerkt neutralisieren. Für jede Profilklasse wären originale rohe
Ability-/Role-Suitability-Komponenten und Gesamtwert sowie aktive/nichtaktive
experimentelle Policy vor/nach Vorbereitung und Sampling gesondert zu erfassen.
Ein passiver, für alle Startspieler vollständiger Effektivitätsaudit ist in
unserem normalen `NativeLab` bisher nicht ausgewiesen. Ohne ihn ist ein
Profilinteraktionseffekt messbar, aber seine Zerlegung in Position versus
abgeleitete Effektivität nicht identifiziert. Nichts davon wurde hier nativ geprüft.

## VALID-003: konkreter kleiner Budgetentwurf

Ergänzt den [zentralen Plan](../../experiments/VALID-003-plan.md), ersetzt ihn
nicht. Keine neuen Seeds reserviert; alle folgenden Serien bleiben ungestartet.

| Gate | Geplanter Umfang | Annahme / Stopp |
|---|---|---|
| V3A Profile |2 eingefrorene Profilsets×2 Seiten×2 neue Seeds×2 Wiederholungen=16 Vollmatches | Rohvektoren/Binärdiff,69 Attribute/Positionsratings, Profile, beide Phasen/Rollen/Duties/PI/Identität nach Vorbereitung exakt. Nicht lesbare Felder blockieren zugehörige Behauptung. |
| V3B Stärke |2 eigene low/high-Kadervektoren×2 Seiten×2 neue Seeds×2 Wiederholungen=16 Vollmatches | Stärke nicht als lineare CA-Skala behaupten; Änderungen einzeln dokumentieren. Große Stärkedifferenz nur Plausibilität, kein erzwungener Sieg pro Seed. |
| V3C PKM |2 geeignete private Dateien×2 Seiten×2 neue Seeds je Dateikontext×2 Wiederholungen=16 Vollmatches | Nur wenn Kapazität/Identität/Seitenübertrag vorher geklärt; Originalkontext/Startscore/Seed/Phasen und verfügbare Managerzustände auditieren. Sonst unbegonnene Jobs erhalten, kein Ersatz. |

Zusammen≤48 Vollmatchversuche +6 negative Probes,900s beaufsichtigte Child-Zeit,
1800s feste UTC-Frist,≤4 Worker/90s ohne Fortschritt,4GiB Artefaktcap/20GiB frei.
Code/Vertrag/Seeds/Budget vorab veröffentlichen; keine Retries/Seedersetzung.
Nach Host-/Startpolitikänderung VALID-002-Kernkontrollen mit neuen Seeds erneut
bestehen. Dies ist ein Budget, keine gemessene Laufzeit und kein wissenschaftlicher
Powernachweis. Technische Tests schätzen keine Taktikleistung.

V3D SET-Zähler separat: eigene synthetische Traces für Duplikat/Abbruch/VAR/
Gegentor/Konter, danach künftig≤16 Vollmatchversuche +4 negative Probes,
600s Child-/1200s UTC-Cap und≤4 Worker/90s. Kein Zusatz zum48er-Paket ohne
eigenen Vertrag. Ausführungstick, Typ/Seite/Abbruch, Ketten-ID und xG/Tor/
Konterfenster vorab definieren; unabhängig annotieren oder gegen zweite native
Quelle und Endstand/Stats abgleichen. Bei fehlender Ereignisquelle kein Routine-
Leistungsvergleich und keine Nullersetzung. Ereignisraten/Varianz erst danach
pilotieren; keine erfundene Fallzahlpower für seltene Standardtore.

## TRAIN: ungelöstes RNG-, Kalender- und Expositionsgate

Paarweise bytegleiche Startdatei/Coaches/Kader/Kalender/Gegner innerhalb eines
Replikats; **zwischen** Replikaten validierte unabhängige Karriere-RNG-Streams
oder echte unabhängige Saves/Clubs. Saveklone mit demselben Zufallszustand und
demselben deterministischen Pfad sind keine unabhängigen Replikate. Ein solcher
RNG-/Replikatexecutor ist bisher ungelöst; die bloße Zahl von Kopien ist kein n.
Kein Schluss von Matchengine-Seeds auf gesteuerte Karriere-Zufallszustände.

Maschinenlesbare Checkpoints müssen tatsächliche Session/Tag/Slot/Teilnahme/
Abbruch, individuelle Intensität, Spieler-Minuten/Matchlast, Fitness/Schärfe/
Ermüdung, Verletzungsbeginn/-ende und lesbare Familiarityfelder belegen.
Kalenderzuweisung ist keine Teilnahme; unbekannt bleibt unbekannt. A/A-
Fortschreibung aus bytegleichem Startsave ist eigenes technisches Gate.
Spieler sind wiederholte Beobachtungen innerhalb von Save-/Clubclustern.
Einzelmatchsimulationen liefern keine Spielerentwicklung oder Trainingseffizienz.

## Implementierte Vorarbeit und echte Tests

Neu: [research/coordination.py](../../research/coordination.py), eine opt-in,
kooperative lokale Exklusivlease. Exklusive Dateierstellung, Eigentumstoken,
PID/UTC/angeforderte1..4 Worker und fsync. Crashdatei bleibt blockierend;
kein automatisches Entfernen oder PID-Stealing. Manipulierte/kaputte Belege
verhindern die Freigabe durch eine Instanz. Nur Tempdateien in Tests.

**Nicht integriert:** Kein existierender Runner/Registry/Budget geändert.
Alle künftigen kooperierenden Supervisoren müssten denselben privaten Ordner
nutzen. Die Lease begrenzt deklarierte Worker, überwacht keine tatsächlichen
Prozesse, zählt keine globalen Wallseconds/Seeds und schützt nicht vor
nicht kooperierenden Programmen, externer Dateilöschung oder ungetesteten
Netzwerkdateisystemen. Keine aktive globale Vierergrenze wird behauptet.
Director hält erst in einem neuen Runner die Lease über dessen NativeBudget-
Supervisor, koordiniert Seedallocation separat mit gemeinsamer Registrylock und
persistenter Programmbudgetreservation. Archivierte Runner bleiben unverändert.
Crashaufklärung prüft Prozesse/Ledger/Budget vor einer manuellen Leaseaufhebung;
keine automatische Wiederaufnahme.

[tests/test_coordination.py](../../tests/test_coordination.py): **4/4 echte
Offline-Tests bestanden**, konkurrierender zweiter Pythonprozess, normale
Freigabe, abrupter Pythonprozessabbruch mit weiter blockierender Lease,
manipulierte/kaputte Eigentumsbelege, Workercap/Reentranz und Exceptionfreigabe.
Befehl: `python -m unittest discover -s tests -p test_coordination.py -v`.
Keine native Anwendung oder echte Registry wurde benutzt.

## Unsicherheiten und nächste konkrete Schritte

1. Independent Reviewer prüft Gap-Tabelle und Lease; Director integriert nach CI.
2. Neue kontrollierte/experimentelle Startpolitik und passive Effektivitätsreceipts spezifizieren; keine stille Normalisierungsänderung.
3. PKM-Kapazität/Originalkontext nur lesend inventarisieren, keine Replayfreigabe aus Readererfolg.
4. SET spezifiziert tatsächliche Expositions-/Attributionszähler, VALID prüft Quellenabdeckung.
5. TRAIN spezifiziert Replikat-RNG, Kalender-/Teilnahmeherkunft und unabhängige Cluster; Executor gesondert validieren.
6. Erst nach veröffentlichten technischen Verträgen und bestandenen nativen Gates wissenschaftliche Performanceversuche beginnen. Hier: keine solchen Versuche, keine neuen Simulationen.

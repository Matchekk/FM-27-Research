# VALID-003 – technischer Plan für realistischere Profile und Karriere-PKM

**Nur Planung, 14.11.2026. Keine neue Eingabe implementiert, kein Karriere-PKM
simuliert und keine Erweiterung der VALID-002-Freigabe.** P1C benutzt unverändert
das gebündelte Fixture. Dieses Dokument ist kein ausführbarer Forschungsauftrag.

## Ausgangspunkt und Grenzen

VALID-002 akzeptiert den Originalreader gespeicherter PKM, scheitert aber beim
Transfer der fest vorgeschriebenen23-Spieler-Kader: Recordtyp17, Exit108.
Nicht durch anderes Fixture, andere Kadergröße oder anderen Seed umgehen.
P1B/P1C kontrollieren künstlich gleiche, positionsübergreifend geeignete Profile.
Sie isolieren Eingriffe, bilden aber heterogene Vereine nicht repräsentativ ab.

Die Upstreambeschreibung unterscheidet nativen Detail-Matchloop, normalisierte
Profile und vollständige Karriereabläufe. Readerakzeptanz oder ein natürlicher
Endstand sind daher kein Nachweis eines originalgetreuen Karriere-Replays.
Quelle: [Upstream Fidelity, geprüfter Toolcommit](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/docs/SIMULATION_FIDELITY.md).
Diese methodische Grenze gilt auch ohne Implementierungsänderung.

## Drei getrennte, künftig zu genehmigende Gates

| Gate | Technische Arbeit | Abnahme vor Forschung |
|---|---|---|
| V3A: positionsabhängige synthetische Profile | Eigene, versionierte GK/IV/AV/DM/AM/Flügel/ST-Vektoren, getrennte Positionsvertrautheit/Rollen/Attribute/Profile. Native-ID nur privat an feste Slots binden. Keine pauschale CA-Normierung als vermeintlich gleiche Stärke. | Alle69 Attribute, Positionsmasken/Vertrautheit, beide Phasen/Rollen/Duties/PI und Startzustände nach Originalvorbereitung exakt auditieren; unerlaubte Rolle/Attribut/Position ablehnen. |
| V3B: Stärkekontexte | Vorab eigene low/medium/high-Kadervektoren definieren. Verhältnis30/50/70 oder ähnliche Labels erst nach Definition; Attributpunkte sind keine lineare Leistungsstärke. Testmannschaft und Gegnerstärke getrennt faktorisieren, Fitness/Moral/Schärfe/Alter/Größe/Gewicht konstant oder explizite Faktoren. | Gleichstärken-A/A, Übertrag beider Seiten, exakte Seedwiederholung, deklarierte Binärdifferenzen. Plausible Richtung bei großem kontrolliertem Stärkeabstand als Sanitycheck, kein Zwang zur Seed-Einzelsiegfolge. |
| V3C: gespeicherte Karriere-PKM | Eigenes Kapazitäts-/Roster-/Träger-/Manager-/Phasenmanifest pro Datei; tatsächliche Teams/Kaderanzahl/Startpositionen lesen. Keine Zwangsübertragung23, kein stilles Abschneiden/Auffüllen. Reader und Adapterpfad getrennt versionieren. | Byte-/Semantikrundlauf, native Kapazitäten und IDs/Anzahl nach Vorbereitung, sämtliche verfügbaren Profile/Fitness/Schärfe/Moral, Fixture-/Managerzustand, Taktiken beider Phasen, Seedoverride und natürlicher Abschluss verifizieren. Nicht verfügbare Felder blockieren Gleichheitsbehauptungen. |

Zuerst technische Fähigkeiten inventarisieren, bevor ein Schreibfeld als wirksam
behauptet wird. `research/career.py` bietet Checkpoints, keinen validierten
Karriereexecutor. Laufende neue V3-Eingaben bekommen eigenen Vertrag und neue
Seeds; bestehende Discovery-/Holdoutprofile und deren Reservierungen bleiben frei.

## Kleine künftige technische Reihenfolge und Budgetentwurf

1. Nur lesende Dateiinventur im privaten Verzeichnis: Eigentums-/Nutzungsfreigabe,
   Hashes, Build, tatsächliche Kapazität, Ausgangszeitpunkt, Startscore, Quelle.
   Kein Export personenbezogener IDs, PKM/Spielstand oder Originaldatensätze.
2. V3A mit je einer eigenen GK-/Feldspielerprofilvariante testen: beide Seiten,
   neue Seeds, zwei exakte Wiederholungen. Rollen und Profile getrennt verändern.
3. V3B Seiten-/Stärkematrix mit festen eigenständigen Entdeckungsprofilen prüfen.
4. V3C zunächst eine bekannte private Datei lesend dekodieren und den konkreten
   Record17-Fehler kausal erklären. Anpassung möglichst im eigenen Adapter,
   Upstreamkopie/Spielinstallation unverändert. Wenn Hostschreibpfad fehlt,
   einen reproduzierbaren minimalen eigenen Patch separat reviewen und neu hashen.
5. Vor dem ersten V3-Nativmatch neuen technischen Vertrag/Code/Seeds pushen:
   Budgetvorschlag≤48 Vollmatchversuche +≤6 negative Probes,≤4 Worker,
   90s Fortschrittstimeout,900s Child-Zeit und1800s feste UTC-Deadline,
   persistente Zähler ohne Ersatzseeds. Separate Blöcke je Gate; keine Nutzung
   dieser bloßen Planung als Freigabe. Scheitert ein Gate, abhängige Läufe stoppen.

A/A: bytegleiche Eingabe+Seed zweimal, gleiche Scores/Stats/Endticks.
Seitenwechsel: nachweislich transplantierte native Identität, kein behaupteter
isolierter Heimvorteil. Negative Tests: falscher Build, Kaderkapazität, fehlender
Spieler, ungültige Position/Rolle, beschädigte PKM/Binärdatei; erwarteter Fehler
ohne Nullresultat. Alle gestarteten/fehlgeschlagenen/unbegonnenen Versuche erhalten.
Eventvollständigkeit und ggf. FMF-Rundlauf unabhängig prüfen, falls für neue
Rollen/Standards erforderlich. Nach jeder Hoständerung VALID-002-Kernkontrollen
mit neuen technischen Seeds erneut bestehen.

## Praxisvalidierung nach technischen Gates

Vier Ebenen getrennt benennen: synthetisches Einzelmatch → realistisches
positionsabhängiges Laborprofil → Re-Simulation gespeicherten PKM-Kontexts →
kontrollierter vollständiger Karriereablauf. Keine Ebene ersetzt die nächste.
Exaktes Replay des historischen Spiels setzt vollständige Eingabe-/Zufalls- und
Live-Managementzustände voraus; unbekannte Daten dürfen nicht durch Defaults
als identisch ausgegeben werden. Stattdessen als normalisierte Re-Simulation
mit vollständig benannten Abweichungen registrieren.

Spätere Forschung: eingefrorene Kandidaten gegen Baseline, neue unbenutzte
Gegner/Stärken/Saves, tatsächliche Punkte primär. Clubs/Save-Ableger sind Cluster,
Matches innerhalb eines Saves keine unabhängigen Wiederholungen. Handspiel,
Instant Result, Urlaub und Training brauchen separate Executor-/Kalenderaudits.
Taktische Vertrautheit, Wechsel/Karten/Verletzungen und persistente Zustände
als Wirkmechanismen messen statt ohne Nachweis konstant anzunehmen.

## Öffentliche Artefakte und Stopregel

Geplant: `research/profiles.py` für eigene Vektoren+Schemavalidierung,
`research/pkm_context.py` für rein lesende Kapazitäts-/Kontextdeskriptoren,
`experiments/VALID-003-validation.md` mit realen Gates sowie numerischem
Whitelist-Archiv mit Code-/Inputhashes. Diese Komponenten existieren dadurch
noch nicht und werden in P1C nicht implementiert. Private Manifestpfade/IDs bleiben
lokal, öffentlich nur eigene anonymisierte Profile, Versions-/Hashbelege und
zulässige numerische Messungen. Drift/Eingabefehler stoppen. Freigabe erst nach
vollständiger technischer Abnahme, kein automatischer Karriereforschungsstart.

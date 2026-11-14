# MECH-001 – Spielschärfe × Pressing und Mechanikregister

**Vorregistrierbarer Designentwurf · nicht gestartet · 14.11.2026.**
[Maschinenvertrag](../research/specs/MECH-001-draft.json).

Hypothese: Geringere Spielschärfe mindert den Punktgewinn stärker bei hohem
Pressing. Vollständiges 2×2-Design: Spielschärfe-Rohwert 10000 vs. 7000 und
zwei aus dem aktuellen Katalog eingefrorene Pressingstufen. Nur zehn Feldspieler
des Testteams behandeln; Fitness, Ermüdung, Moral, Positionsvertrautheit und
übrige Profile konstant. Rohwertinterpretation vorab durch native Readbacks
prüfen; bei nicht belegter Skalierung den Vertrag vor Start ändern und neu publizieren.

32 neue Seeds, vier Arme, beide Seiten = **256 Pilotmatches**, 32 unabhängige
Seedblöcke. Eine eigene feste IP-4-2-3-1 mit einem fixen Entdeckungsgegner.
Primär: Differenz-von-Differenzen tatsächlicher Punkte pro Match; sekundär xGD,
Tore/Gegentore, Endfitness, Fouls, Karten und Verletzungen soweit nativ geprüft.
Ein Primärtest bei α=0,05, Holm über benannte Sekundärtests, 95-%-t- und
Seedblock-Bootstrapintervalle, Seitenmittel innerhalb des Seeds.

32 Blöcke sind Varianzpilot, keine Bestätigung eines 0,15-Punkte-Effekts.
90-%-Powerplanung für neue Bestätigung aus gepaarter Kontrast-SD und deren
einseitiger 95-%-Obergrenze; praktische Schwelle vor finaler Registrierung
festlegen. Held-out Gegner und Stärken separat. A/A sowie alleinige Schärfe-
und alleinige Pressingänderung als Plausibilitätskontrollen.

Der Standardisierer des Labs setzt Startprofile: Die Intervention muss **nach
der beabsichtigten Normalisierung tatsächlich bestehen** und nach Original-
vorbereitung ausgelesen werden. Ein verändertes JSON allein ist kein Eingriff.
Alle Fehler/ausstehenden Arme dokumentieren; keine Ersatzseeds und kein
Ergebnisfilter. „Kein erkennbarer Effekt“ ist keine Äquivalenzbehauptung.

## Register offener Mechanismen

| Frage | Priorität | Isolierbarkeit / Voraussetzung |
|---|---|---|
| Spielschärfe × Pressing | 1 | Direkter Profilreadback; kleiner vollständiger Faktorplan |
| Fitness × Tempo und Ausdauer | 2 | Startfitness und Ermüdung getrennt; Matchzeitwerte auditieren |
| Positionsvertrautheit je Phase | 2 | Native Spieler-/Phasenbindung, GK gesondert; keine künstlich überall natürlichen Spieler als einzige Basis |
| Heimvorteil vs. feste Fixtureseite | 2 | Identische Teams allein reichen nicht; Stadion-/Wettbewerbskontext gezielt variieren |
| Moral und Mannschaftskohäsion | 3 | Startwerte vs. Karriereverläufe trennen; mutmaßliche Wirkung vor Matchvorbereitung beachten |
| Taktische Ausführung / Komplexität | 1 als Transfergate | Aktuelle Rolle/Attribute und Original-Ableitungen prüfen; Mac-Komplexitätsgrenze nicht ignorieren |
| Wechselzeitpunkt und Spielmanagement | 3 | Nativer Management-/Substitutionsadapter; Zeit und Spielstandpolitik vorab fixieren |
| Konsistenz / wichtige Spiele | 3 | Versteckte Attribute und Anlassgate getrennt; mehrere echte Fixturekontexte |
| Detaillierte Engine vs. Karriere / Urlaub / Instant Result | P0 vor Praxisbehauptung | Vollständige Eingaben, RNG und Management abgleichen; aktuell nicht validiert |

Jede Zeile bekommt bei Umsetzung eine eigene ID und einen eigenen nativen
Eingabeaudit. Das Register ist eine Hypothesenliste, keine bestätigte Mechanikliste.

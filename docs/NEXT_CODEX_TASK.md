# Nächster Codex-Auftrag: TACT-001-P0

Arbeite im Repository `https://github.com/Matchekk/FM-27-Research`.
Beginne mit AGENTS.md, aktuellem Git-/Remote-/Änderungsstatus, VALID-002,
docs/PLATFORM.md und experiments/TACT-001-discovery.md.
Bestehende ATTR-001–007 und fremde Änderungen erhalten.

Führe ausschließlich den ersten wissenschaftlichen **Varianzpilot TACT-001-P0**
für eine selbst entwickelte IP-4-2-3-1 durch. Kein Downloadturnier und keine
abschließende Behauptung einer optimalen Taktik.

1. Prüfe aktuelle FM27-DLL, Host, Ressourcen, Fixture, Tooltag und letzten
   Freigabekontext. Bei Drift erst revalidieren. Gespeicherte Karriere-PKM sind
   noch nicht freigegeben; nutze nur das validierte gebündelte Fixture.
2. Erstelle eine eigene 4-2-3-1 in `rules=game`, zwei zulässige Pressingstufen
   und zwei Defensivlinienstufen aus dem aktuellen nativen Katalog. Vier Arme
   als vollständiges 2×2. IP-Grundordnung bleibt fest; alle anderen Eingaben
   innerhalb eines Kontexts unverändert.
3. Friere zwei kontrollierte Entdeckungsgegner ein: hohes Pressing und tiefer
   Block, identische Kaderstärke. Konkrete doppelte Phasen, Rollen, PI, Profile,
   Seitenwechsel und Matchmanagementpolitik vollständig benennen und hashen.
   Separate spätere Holdoutprofile vorab kennzeichnen, nicht simulieren.
4. Schreibe und pushe Vorregistrierung, konkreten JSON-Vertrag, deterministischen
   Analysecode und Seedreservierung vor dem ersten Hauptmatch. Acht **neue** Seeds
   je Gegner, alle vier Arme auf beiden Seiten: 128 Hauptmatches, 16 unabhängige
   Seedblöcke. Frühere, technische und reservierte Seeds vollständig ausschließen.
5. Höchstens 24 zusätzliche technische Prüfmatches für A/A, Wiederholbarkeit,
   native Readbacks und negative Eingaben. Maximal vier Worker, 90 Sekunden ohne
   Fortschritt je Worker, höchstens 15 Minuten gesamte native Ausführungszeit.
   Vor Beginn für beide Grenzen einen tatsächlichen Zähler/Deadline einbauen;
   keine Schleife, die durch Neustart oder Retry das Gesamtbudget umgeht.
6. Primär: Pressing×Linie-Differenz-von-Differenzen auf xGD. Szenarien je 1/2,
   Seitenmittel innerhalb des Seeds. Sekundär: tatsächliche Punkte, Tore,
   Gegentore, xGF/xGA und vorab vollständig benannte native Plausibilitätsgrößen.
   Gepaarte 95-%-Intervalle und stratifizierter Seedblock-Bootstrap; ein
   Primärkontrast, Holm über die eingefrorene Sekundärfamilie.
7. Die Fallzahl ist ein Varianzpilot und nicht für 0,10 xGD gepowert.
   Keine finale Kandidatenauswahl oder Bestätigung. Berichte Kontrast-SD,
   deren einseitige 95-%-Obergrenze und benötigte neue Bestätigungsfallzahlen
   für vorab benannte Effekte bei 90 % Power.
8. Native Eingabe-/Seed-/Identitätsfehler stoppen die Serie. Keine Ersatzseeds,
   Ergebnisexklusion oder stillen Nullen. Alle begonnenen, fehlgeschlagenen und
   unbegonnenen Jobs sowie Budgetverbrauch erhalten. Bei unvollständigen
   Blöcken nur technischen Status publizieren.
9. Rohspielmaterial bleibt privat. Publiziere erlaubte JSONL-Messungen,
   Provenienz, negative Kontrollen, Analyse, Grenzen und nächsten Vorschlag.
   Tests, historischen Archivschutz und Git-Diff prüfen; gemäß AGENTS.md
   committen/pushen, SHAs und reale Laufzahlen nennen.

Stoppe nach diesem Pilot. Keine DoE-Großserie, Modelloptimierungsrunde,
Holdoutbestätigung oder Karrierefortschreibung in diesem Auftrag.

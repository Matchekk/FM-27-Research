# Nächste Schritte – priorisierte Forschungsaufträge

## P0 – Arbeitsumgebung und Baseline validieren
- [ ] Lokales Arbeitsverzeichnis und bestehende Forschungspfade ermitteln.
- [ ] Vorliegende FM27-Experimente und Rohdaten aus dem lokalen Projekt inventarisieren (nichts ungeprüft importieren).
- [ ] Aktuellen Spiel-Build sowie FM Tactics Lab-Adapterversion erfassen; Referenzbuild der bekannten v1106-Doku: `27.0.0+2493426` (nicht automatisch aktueller lokaler Build).
- [ ] Startzustände, Matchengine-Eingaben und tatsächlich veränderte Attribute gegenprüfen.
- [ ] Mehrfach identisches Baseline-Setup mit identischen Seeds rechnen und Ergebnisse auf Reproduzierbarkeit prüfen.
- [ ] Ungeeignete Dateien aus Git ausschließen; Geheimnisse und lizenzierte Spielressourcen nicht pushen.
- [ ] Valide Altversuche jeweils in `experiments/<ID>.md` rekonstruieren und Evidenzstufe korrekt vergeben.

## P1 – Attribut-Screening (nach P0)
- [ ] Versuchsplan mit den 16 Attributen und Kontrollbedingungen festschreiben.
- [ ] Neue Paarungen von Baseline und Intervention (+4, z. B. 12→16) für dieselben zehn Feldspieler, zuerst 40 Seeds je Attribut.
- [ ] Je Lauf Setup-Hash, Seed, Status, Ergebnis und Interventionsdetails persistieren.
- [ ] Primäre xG-Differenz, Konfidenzintervalle und Mehrfachvergleiche auswerten.
- [ ] `FINDINGS.md` nur nach bestandenen Qualitätssicherungen ergänzen.

## P2 – Replikation
- [ ] Fünf Screeningkandidaten plus methodisch begründete Kontrollen **vorher** festlegen.
- [ ] 240 neue gepaarte Seeds pro Kandidat; zusätzliche Gegnerprofile und Heim/Auswärts.
- [ ] Sensitivität nach Szenario und Effektgröße berichten.

## P3 – Positions-, Taktik- und Trainingsstudien
- [ ] Attributvergleich pro Positionsgruppe.
- [ ] Pressing × Defensivlinie in 2×2-Design.
- [ ] Conditioning-vs-Heavy unter kontrollierter Karrierebelastung erneut beurteilen.
- [ ] FM27-Buildwechsel erkennen und erforderliche Revalidierung planen.

## Nach jedem abgeschlossenen Meilenstein
`RESEARCH_LOG.md`, ggf. `FINDINGS.md` und diese Liste aktualisieren, committen und **pushen**. Push-Status und SHA angeben.

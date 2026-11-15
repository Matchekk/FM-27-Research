# Gemeinsame Ausgangsbasis

TRAIN-005-INGAME, eine Karriere, P001; Start 16.01.2027, geplantes Ende
13.03.2027. A und B wurden aus derselben unveränderten Ausgangsdatei erzeugt:
147.130.636 Bytes, SHA256
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
Namen, konkrete Spieler-IDs, Geburtsdatum, Speicheradressen und Saves bleiben privat.

| Merkmal | Beobachtung |
|---|---|
| P001 | 20 Jahre; Defensivfamilie; kein Austauschspieler |
| Antritt / Tempo | 14 / 14; gerundete UI-Anzeige |
| STORED_CA / PA | 134 / 160; unabhängiger Live-Objektread, kein RCA |
| Kondition / Schärfe | 64 / 99; angezeigte Skala, nicht erfundene Rohwerte |
| Trainingsverhindernde Verletzung | Leere aktuelle UI-Anzeige |
| Historische Verletzungsanzeige | „6 Tage“; keine sechs im Pilot verursachten Ausfalltage |
| Individueller Fokus A | −1 / „–“ |
| Geprüfte Option B | 9 / „Schnelligkeit“ |
| Intensitätsregel | `IndividualTrainingIntensityAutoSelected = True`; aktueller Startcode −2 |
| Ohne-Ball-Trainingsrolle | Selektionscode 50 / „–“; Bedeutung nicht überkalibriert |
| Trainingsanlage | Spielanzeige „Erstklassige Trainingseinrichtungen (9/10)“ |
| Jugendanlage / Jugendcoaching | Dynamischer Wert jeweils 18; eigene Skalenkalibrierung NOT_MEASURED |
| Erfasster Kader / Personal | 27 Spieler, 40 Personalreferenzen, 11 Coaching-Mitarbeiter |
| Einzelne Trainerqualität / Arbeitslast | NOT_MEASURED; Zuweisungsansicht privat gesichert |
| Professionalität / Ehrgeiz | NOT_MEASURED; fehlgeschlagene UI-Abfragen ergeben keine Werte |
| Zielstrebigkeit | Als Attributanzeige im privaten vollständigen Profil erhalten |
| Positionsbezogener Meta-Score | NOT_MEASURED; kein nachträglich ausgewählter Score |
| Kalenderuhrzeit | NOT_MEASURED; protokolliert werden Kalenderdatum und reale UTC-Abfragezeit |

Die 58 angefragten Attributpfade enthalten elf nicht verwertbare Anzeigen,
darunter Agenteneigenschaften und verborgene Persönlichkeit. Nur 47 liefern
verwertbare Attributanzeigen. „58 Attribute unverändert“ wäre daher zu weitgehend.
Vorläufiger B-Readback: diese Anzeigen, Identität, Alter, Kondition, Schärfe und
aktuelle Trainingswoche unverändert; Fokuscode −1 → 9. Die numerischen Selektionen
für Rolle und automatische Intensitätsregel stimmen überein. Dynamische
Verfügbarkeitsflags aus noch nicht aufgelösten UI-Kontexten sind keine geänderten
Trainingsanweisungen.

Der bestehende Wochenplan enthält 21 Sessionplätze plus sieben Tagesnamen.
Der vorregistrierte Export mit allen 28 Elementen steht in
[preregistration.json](../../data/player-development-004/preregistration.json),
SHA256 des kanonischen Sessionlistenexports
`043878f896a195294403fd2f64c90a29d4423d75164e73e8032773c3dde3b476`.
Der zukünftige Achtwochenplan wurde nicht vollständig eingefroren. Die bisherige
Plan- und automatische Intensitätspolitik bleibt erhalten; sichtbare Wochenstände,
Pflichtentscheidungen, Spiele und Abweichungen werden protokolliert. Individuelle
Teilnahme an allen Trainingseinheiten ist nicht beobachtet.

# Nächster priorisierter Auftrag – ATTR, MECH und TRAIN

Vorschlag nach Runde2, **nicht in diesem Auftrag gestartet**. Reihenfolge nach
neuem Erkenntniswert und technischer Reife; keine automatische Seedreservation,
Matchserie oder Karrierefortschreibung. D00 bleibt festgelegter Kontext, keine
nachträgliche Übernahme eines ausgewählten Rollenarms ohne neuen Vertrag.

## 1. ATTR-009-Bridge: gezielter technischer Maskenaudit, dann kleiner Pilot

Frage: Verändern ungenutzte Positionsratings den relativen xGD-Nutzen von JR
gegenüber Acceleration/Pace? Reine Positionsrating-Haupteffekte sind extern
bereits untersucht; neu ist der gekreuzte relative Attributkontrast.

Konkreter nächster Codex-Auftrag: Entwickle auf `research/validation003.py`
aufbauend einen eigenen, versionierten Profilencoder und nativen Auditor für
zwei Testteam-Masken. Aktive IP/OOP-Ratingfamilien20, ungenutzte Feldfamilien20
versus1; GK/Sweeper und alle übrigen Eingaben unverändert. Seitenabhängige
OOP-Spielerbindung und gemeinsame DCL/DCR-/DML/DMR-Familien einzeln beweisen.
Erste15Positionsratings nutzen0..20, übrige54Fähigkeitsrohwerte1..100.
Eine Anzeige12→16 ist kein ungeprüfter Rohwert12→16: Rohinkrement und
Anzeigekalibrierung müssen explizit mit nativen Vor-/Nachreadbacks belegt werden.

Zwingende Gates: keine Uniform-Poolnormalisierung, keine experimentelle
Effektivitätsneutralisierung; alle69 Werte/23Profilfelder/Rollen/Phasen/PI und
Originalvorbereitungsreceipts prüfen. Abgeleitete Effektivitätswerte passiv
messen oder Mechanismuszerlegung ausdrücklich unidentifiziert lassen.
Die heutigen eigenen21Vektoren sind nur Absichten, noch keine native Freigabe.

Sparvariante vorab wählen: zwei Masken×J/A/P×beideSeiten=12Matches je Seed,
16neueSeeds je bekanntem Gegner=32 unabhängige Blöcke/**384Hauptmatches**.
Primär `[J−(A+P)/2]_spezialisiert−[J−(A+P)/2]_omni` auf xGD;
Seitenmittel im Seed, Gegnergewichte½. Genau fünf sekundäre Endpunkte desselben
Kontrasts: Punkte/GF/GA/xGF/xGA(Holm5). Keine absoluten Baselinevergleiche;
diese wurden für25% weniger Hauptjobs bewusst gestrichen. Kein gemessener
Varianzgewinn. Alternative mit Baseline512Matches/Holm11 nur vorab separat wählen.

Technik konkret24Eingabezellen einmal+8vorab benannte A/A-Wiederholungen=32
Vollmatches,plus1Binärnegativprobe. Neue zentrale Seeds, vollständige persistente
Zähler; Vorschlag600s Child/1200s fixeUTC-Frist,≤4Worker/90s Fortschritt,
2GiBprivat/20GiBReserve. Vor Hauptserie eigener JSON-Vertrag/Code/Seedplan pushen,
CI+Technik bestehen und unabhängig reviewen. Ziel0,30xGD ist eine Pilotplanung;
neue Kontrast-SD unbekannt, keine90-%-Powergarantie. Bei Gatefehler stoppen.

## 2. MECH-002: opt-in Startpolicy vor Schärfe×Pressing

Konkreter Auftrag: Implementiere einen separaten eigenen Startpolicy-Encoder samt
Runner-/Readbackbindung. Der normale Server setzt CONTROLLED_START erneut und
`NativeLab.run` re-enkodiert; nachträgliches Binärpatchen ist kein zulässiger Pfad.
Historischer Default muss binärgleich bleiben. Bestehender Host unterstützt
begrenzte Profilrecords, ihre tatsächliche Wirksamkeit ist neu zu validieren.

Intervention erst nach Gate: beide Schärfefelder16/17 gemeinsam10000/7000,
Startfeldspieler des Testteams; GK/Bank/Gegner unverändert, Condition10000,
Fatigue0. Start-only nach Originalvorbereitung, kein dauerhafter Clamp.
Rohe7000 sind ohne Kalibrierung keine behaupteten70% einer Karriereanzeige.
Kein gleichzeitiger Rollen-/Positions-/Executioneingriff. Experimental-Dict-
Overall ist kein isolierter Understanding-/Karrierefamiliarity-Setter.

Danach gesondert registrierbarer voller2×2-Pilot mit Standard/MoreOften-Pressing:
32neueSeeds/Gegner,beideSeiten,**512Hauptmatches/64Blöcke**. Primär marginaler
Vorteil voller Schärfe auf xGD, genauHolm8 gemäß MECH-Bericht. Technik32Vollmatches
und3negativeProbes,900s Child/1800s UTC,≤4Worker/90s,2GiBprivat.
Originalzustände beider Felder nach Vorbereitung und erster Fortschreibung
belegen, ohne Verlauf künstlich konstant zu halten. Rollenpilot-/P1B-SDs nicht
als gemessene Schärfevarianz übernehmen. Kein automatischer1024er-Ausbau.

## 3. TRAIN-002: Reader-, RNG- und Teilnahmefundament vor Karrierepilot

Konkreter Auftrag: Kalibriere Roh-/Anzeigeattribute, Karrierecheckpoint-Reader,
Kalender und tatsächliche individuelle Trainingsteilnahme mit Quell-/Buildreceipts.
Ein boolesches Teilnahmeflag ist kein Herkunftsbeleg. Erfasse Session/Tag/Slot,
Coach/Anlagen/Fokus/Intensität, tatsächliche Minuten, Rest/Reha/Absage und
Verletzungsbeginn/-ende. Vorhandener `career.py` ist kein validierter Executor.

Unabhängigkeitsgate: paarweise bytegleiche Starts innerhalb eines Replikats;
zwischen Replikaten nachgewiesene neue Karriere-RNG-Streams oder echte unabhängige
Save-/Clubcluster. Identische RNG-Savekopien und22Spieler zählen nicht als
zusätzliche unabhängige Behandlungen. Isolierte Matchseeds lösen dies nicht.

Erst nach passendem separaten Vertrag technischer Benchmark≤2A/A-Paare×2Wochen
=8Armwochen,ein serieller Karriereexecutor,30Minuten-Gesamtcap. Kein Replay oder
Kalenderadvance aus Readererfolg freigeben. Falls RNG-/Teilnahme-/Einheitengate
nicht erfüllt ist, nur technischen Status publizieren und keine Ersatzreplikate.

Späterer wissenschaftlicher Pilot ausschließlich separat: Conditioning/Heavy,
6Wochen,8unabhängigePaare je Altersstratum=32Karrierearme/192Armwochen;
Primär kalibrierter Entwicklungsindex,Holm2. Körper-/Fitness-/Verletzungsfolgen
als Gesamteffekt erhalten, nicht durch nachträgliches Minutenmatchen entfernen.
Holm20-Sekundärfamilie braucht vorher lesbare Endpunkte und geeignete Cluster-/
Zählmodelle. Laufzeit erst aus Karrierebenchmark planen, nicht aus512Labormatches.
Keine Karrierehauptserie oder Jugendjahresfortschreibung in der nächsten
technischen Vorarbeit automatisch starten.

## Gemeinsame Freigabe

Alle drei Aufgaben verwenden ausschließlich zentrale, neue Namespaces/Seeds und
denselben globalen NativeLease-Pfad. Nur ein nativer Forschungsauftrag,≤4Worker;
Crash-/Budgetbelege behalten, keine Resets,Retries oder stillen Nullen.
Vorregistrierung, Code, konkrete Eingaben und Budget vor Hauptmatches veröffentlichen;
Technik+CI+unabhängiger Review zwingend. Keine Holdoutdaten öffnen/ausführen,
keine alten Forschungsarchive überschreiben und keine neuen optimalen Taktiken/
Trainingspläne aus bloßen Pilot- oder synthetischen Parserdaten behaupten.

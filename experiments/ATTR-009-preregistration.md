# ATTR-009-Bridge – Rohattribut × Positionsmasken, kleine Variante

Stand14.11.2026; vor wissenschaftlicher Ausführung. Verbindliche Grundlage:
[Round3-Auftrag](NEXT-ATTR-MECH-TRAIN-round3.md). Technische Freigabe ist erst nach
echten Readbacks, Kontrollen, Veröffentlichung, CI und unabhängigem Review möglich.
Dieses Dokument registriert keine bereits beobachteten Effekte.

## Frage und estimierter Effekt

Verändert die Spezialisierung ungenutzter Positionsratings den relativen Nutzen
einer **nativen Rohwertänderung60→80** von Jumping Reach gegenüber Acceleration
und Pace? Keine globale Attributrangliste, keine D15-Optimierung und keine neue
Taktikauswahl. D00: eigene IP4-2-3-1/OOP4-4-1-1 aus P1B unverändert.

Die 54 Fähigkeitsfelder verwenden native Ganzzahlen1..100; die ersten15
Positionsratings0..20. Tactics Lab zeigt Fähigkeit/5 und schreibt Anzeige×5;
das ist der überprüfte Labformatter und **keine Kalibrierung einer FM-Karriereanzeige**.
Es wird ausdrücklich keine im Spiel gemessene Änderung12→16 behauptet.

Die verlangte passive Effektivitätsprüfung umfasst zunächst die tatsächliche
Messfähigkeit. Der vorhandene Host liefert `execution_snapshot` nur bei aktivem
experimentellem Eingriff; dieser setzt Version/Hooks und Effektivitätsfelder.
Er ist deshalb verboten. Die im verbindlichen Auftrag ausdrücklich erlaubte
Alternative „oder Mechanismuszerlegung ausdrücklich unidentifiziert lassen“
wird hier sichtbar gewählt: Ziel ist die **totale Masken×Rohattributwirkung**;
passive abgeleitete Effektivität und kausale Mediation bleiben unidentifiziert.
Das ist keine Freigabe fehlender Eingabeaudits. Diese Scopeauslegung wird vor
Technikstart unabhängig geprüft.

## Sechs Arme, feste Bedingungen

| Arm | Ungenutzte Feldratings | Dosis bei denselben zehn Startfeldspielern |
|---|---|---|
| OJ |20|Jumping Reach54:60→80|
| OA |20|Acceleration49:60→80|
| OP |20|Pace53:60→80|
| SJ |1|Jumping Reach54:60→80|
| SA |1|Acceleration49:60→80|
| SP |1|Pace53:60→80|

Aktive Ratingfamilien beider Phasen bleiben20; je Spieler die Vereinigung der
logischen IP-/OOP-Position. DCL/DCR teilen DC3, DML/DMR teilen DM5 und MCL/MCR
teilen MC7. GK/Sweeperratings, GK, Bank, Gegner, alle anderen Fähigkeiten und
alle23 Profilfelder bleiben unverändert. Die je Seite unterschiedliche native
OOP-Permutation wird separat auf denselben tatsächlichen MATCH_PLAYER gebunden;
logische OOP-Zeilen werden nicht nochmals mit dem nativen Slot umsortiert.

23 aktive Spieler je Team. Der Auswärtsträger enthält26 serialisierte Slots;
drei inaktive Tail-Slots werden erhalten und nicht als eingesetzte Spieler gezählt.
Kein `away_tactic_pool`, auch kein deaktivierter Schlüssel; kein
`experimental_execution`. `rules=game`, gebündeltes validiertes Fixture,
gleiche Rollen/PI/Team Instructions/Standards/Startprofile und native
Benchmark-Matchmanagementpolitik wie D00. Kein eigener Liveeingriff.

Kontexte ausschließlich `high_press` und `deep_block`; beide bisherige
Discoverygegner, Gewicht½. Keine Holdoutprofile oder Karriere-Replays. Die
vollständigen eingefrorenen Kontexte und Maskenbindungen werden durch
`inputs.json` und `mask-manifest.json` gehasht.

## Stichprobe und Seeds

16 **neue** zentrale Seeds je Kontext;32 unabhängige Seedblöcke. Pro Block sechs
Arme×beide Seiten=12 Matches; **384 Hauptmatches**. Neue Namespaces
`ATTR-009-Bridge/main-v1` und `/technical-v1`. Zwei zusätzliche technische Seeds;
insgesamt34 disjunkte Reservierungen. Archiv, technische Fehlversuche und alle
anderen Reservierungen werden ausgeschlossen. Keine Ersatzseeds/Resets/Retry.
Gleicher Seed garantiert keine identischen Ereignisfolgen.

Keine Baseline-B-Arme. Die algebraisch gemeinsame Baseline entfällt für den
relativen Attributkontrast; absolute Baselineeffekte sind damit nicht identifiziert.
32 Blöcke sind ein Varianzpilot, keine garantierte90-%-Power. Praktische
Zielgröße0,30xGD, gewünschte volle95-%-KI-Breite≤0,50. Keine verbindliche
Präzisionszusage aus fremden Rollen-/Instruktions-SDs.

## Eingabegates und Kontrollen

Aktuelle DLL-/Host-/Fixture-/Ressourcen-/Katalog-/Adaptersourceidentität gegen
VALID-002/P1B prüfen. Konkrete Version/Hashes werden erst in `inputs.json`
nach tatsächlicher Prüfung eingefroren, nicht aus Gesprächsangaben übernommen.

24 Eingabezellen (2Kontexte×2Seiten×6Arme) einmal; danach die acht vorab
benannten OJ/SJ-Zellen (2Kontexte×2Seiten×2Arme) als exakte A/A-Wiederholung.
**32 technische Vollmatches und eine ungültige Binärprobe** mit erwartetem
Exit108, ohne natürliches Matchende. Offline negatives: Positionsrating21,
Ability101, boolesche Ability. Zusätzliche technische Matches sind nicht erlaubt.

Alle69 Attribute/Spieler und23 Profilfelder×46=1058 nach Originalvorbereitung;
46 native Identitäten und Kapazitäten,22 tatsächliche Spielerbindungen in beiden
Phasen,44 Positions-/Rollen-/Duty-/PI-Zellen mit748 PI-Gruppen, beide Teams,
effektiver Seed und natürliches Ende müssen passen. Binäränderungen sind exakt
die deklarierten Kind1-Attributrecords. Normalisierung darf keine weitere
Eingabe verändern.

Native Roh60/80 werden innerhalb der technischen Zellen verglichen: für einen
J-Arm dient der gleiche Masken-/Kontext-/Seiten-/Seed-A-Arm als beobachteter
J60-Vorbeleg, für A/P der J-Arm. Das ist ein Rohdosisnachweis, kein zusätzlicher
Baseline-Leistungsvergleich. Alle übrigen Attribute werden gegen ihre jeweilige
vollständige beabsichtigte Konfiguration geprüft. Kein boolesches Flag oder
synthetischer Test allein erteilt native Freigabe.

## Vorregistrierte Analyse

Primär xGD, Kontrast in Armreihenfolge OJ/OA/OP/SJ/SA/SP:
`(-1,+½,+½,+1,-½,-½)` = `[J−(A+P)/2]S−[J−(A+P)/2]O`.
Zuerst beide Teamseiten innerhalb jedes Seeds mitteln; danach gleichgewichtete
Kontexte. Genau ein primärer Test, zweiseitigα0,05. Welch-/Satterthwaite95-%-KI
und20.000 stratifizierte vollständige Seedblock-Bootstrapziehungen, fester
RNG-Salt `ATTR-009-Bridge/bootstrap-v1`. Keine Matchlevel-Pseudoreplikation.

Genau fünf sekundäre Endpunkte **desselben** Kontrasts: tatsächliche Punkte,
GF,GA,xGF,xGA; Holm5. Keine zusätzlichen isolierten Attribut-Hypothesentests.
Arm-/Kontextmittel, Seitenstreuung und -kovarianz, Leave-one-seed-out sowie
kontextweise Kontrast-SD und einseitige95-%-SD-Obergrenzen sind deskriptiv.
SD-Grenzen benötigen die benannte Normalmodellannahme. Spätere90-%-Powerplanung
für0,20/0,30xGD: neue vollständige Blöcke, beobachtete SD und simultane95-%-
Obergrenzen (je97,5%), nicht „beobachtete Power“ als Ergebnisbeweis.

Keine Ergebnisexklusion, keine stillen Nullwerte. Doppelte, fehlgeschlagene,
unverifizierte, fremde oder unvollständige Blöcke sperren **jede wissenschaftliche
Auswertung**; nur technischer Status/Jobabrechnung wird veröffentlicht.

## Ressourcen, Veröffentlichung und Stop

Ein zentraler Supervisor unter gemeinsamer NativeLease, maximal4 Worker,
90s ohne Fortschritt, **600s kumulierte beaufsichtigte Childzeit und1200s feste
UTC-Studienfrist** inklusive Vorbereitung/Zwischenphasen. Dauerhafte Zähler
werden vor dem ersten nativen Prozess angelegt. Private Artefakte≤2GiB,
freier Speicher≥20GiB. Keine Rücksetzung durch Neustart, kein Worktree-Start.

Vor Hauptmatches: Vertrag/Analyse/Code/Seedplan auf GitHub; Technikbericht,
CI und unabhängiger Review. Eingabe-/Identitäts-/Seed-/Budgetfehler stoppen.
Alle begonnenen/fehlgeschlagenen/unbegonnenen Jobs behalten. Rohspielmaterial
bleibt privat; öffentliche JSONL nur erlaubte Messfelder und Beleg-Hashes.

Ausführung: `analysis/run_attr009.py prepare`, Veröffentlichung/Registrierung,
`technical`, technische Abnahme/Veröffentlichung, `main`; getrennt
`analysis/export_attr009.py`. Kein automatischer Ausbau, keine Holdouts,
keine weitere Forschungsrunde nach384 Hauptmatches.

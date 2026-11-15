# PA-002 – reale Verlaufsdaten und Quellenprovenienz

15.11.2026. **Keine geeignete unabhängige Saisonverlaufsstichprobe gefunden;
kein PA-Prognosemodell trainiert.** MAE, Coverage und PA-Erreichungsquote
bleiben unbekannt. Weder51Trainingsplanmittel noch109GK-Snapshots sind
51beziehungsweise109unabhängige Karriereverläufe.

Zusätzlich neu gefunden: Der [externe Editorbericht](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/docs/editor-test-plan.md)
verfolgt einen Spieler in vier Ablegern über 33 Tage auf Savebuild
27.0.0+2486695. Gemeinsam wurde PA auf 200 angehoben; CA und Attribute wurden
ebenfalls je Arm editiert. Das liefert einen Hinweis auf Profilrückanpassung,
keine natürliche Saisonentwicklung oder unabhängige PA-Ausschöpfungsverteilung.
[Kompakte vollständige Extraktion](../../research/playerdev002-editor-evidence.json).

## Progression Factor und historische Mechanismen

Der [ursprüngliche Progression-Factor-Beitrag](https://www.fmscout.com/a-progression-factor-in-football-manager.html)
ist weiterhin auf07.10.2020 datiert; direkter Webabruf lieferte403, Suchindex
bestätigte Datum und Fox-Videoherkunft. Er ist keine identitätsgebundene
FM27-Codequelle. Fünf Stufen, Übergangsregeln und behauptete Trigger durch
Vertrag, Transfer oder Managerwechsel sind für unseren FM27-Build damit
**nicht unabhängig nachgewiesen**. Keine Nichtexistenzbehauptung.

Die [offizielle FM27-Beschreibung](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness)
bestätigt die Bedeutung individueller Entwicklung innerhalb des erneuerten
Trainingsangebots. Sie quantifiziert keine PA-Ausschöpfung und keine Effekte
von Alter, Ehrgeiz, Professionalität, Zielstrebigkeit, Anlagen oder Minuten.
Solche Variablen bleiben sinnvolle Hypothesen/Prädiktoren, keine hier gemessenen
kausalen Effektstärken. Bei Transfers/Leihen ist Talentselektion ein Confounder.

## Neu geprüfte konkrete Datenwege

| Originalquelle, am15.11. erneut abgefragt | Tatsächlich verfügbar | Grenze |
|---|---|---|
| [FM-Player-Analyzer, eeef907](https://github.com/ElectroHugin/FM-Player-Analyzer/tree/eeef907400ac2d3c340d2e2cec0bd478884bafa3) | Entwicklungs-/Importhistoriencode und Tests, monatliche Spielattribute laut README seit2.2.0; FM27-Import mit Spieltag | Uploadzahl ist keine Zeitdauer; Code-/Synthetiktests liefern keine öffentliche Saison-CA/PA-Kohorte |
| [FMSuperScout, 4dc3abb](https://github.com/mavarobli/FMSuperScout/tree/4dc3abb8f94e2ea882ccbfe58be35e689703b874) | Originalprojekt beschreibt lokal gespeicherte Scan-Snapshots und CA-Veränderung über6/12Monate; lesender Windows-/Mac-Reader | Nutzer müssen tatsächlich zeitlich getrennte Scans besitzen; kein geeigneter öffentlicher Laufkorpus in der geprüften Baum-/Testinventur |
| [fmsave, f4f70f62](https://github.com/rhiever/fmsave/tree/f4f70f62cccae27c63c8dc9610f50c16d5ddcc29) | Save-Snapshots; Ability-Felder sind in der Quelle weiterhin `unconfirmed` | Snapshot/Decoderfunktion ist kein verifizierter Saisonverlauf oder Wachstumsexecutor |
| [Harvestgreen Originalworkbook](https://pixeldrain.com/u/92NJyBDb) | Zwölfmonatsmittel von51Trainingsplänen,20–30Spieler laut A10 | Keine individuellen CA-Starts/PA-Verläufe; PA130/150-Widerspruch; Build, Streuung und unabhängige Karrierezahl fehlen |

Diese zwei neu identifizierten Historienwerkzeuge sind konkrete Exportwege
für künftige Datenakquise, keine eigenen Goldmessungen. Keine Installation,
Live-Speicheraufnahme oder Öffnung einer Originalkarriere vorgenommen.
Quellcommits und HTTP-Prüfungen stehen im
[Maschinenbeleg](../../research/playerdev002-career-sources.json).

## Welche Fragen die echte Tabelle noch nicht beantwortet

TRAIN-003-SOURCE liefert neue, nachvollziehbare Planunterschiede, aber kein
CA/PA-Verhältnis: absolute CA-Ausgangswerte fehlen und die PA-Angaben widersprechen
sich. Selbst eine konsistente End-CA/PA-Quote dieses einen künstlichen
18jährigen-Settings wäre keine normale Ausschöpfungsverteilung. Der Vergleich
von Alter, Persönlichkeit oder Wechsel ist damit nicht identifiziert.

Eine seriöse Prognose `CA nach einer Saison` benötigt Personen- und
Karrierekennzeichen, echte Spieltage, CA/PA/Alter am Start, CA am Jahresende,
Buildbindung und beobachtete Ausfälle. Trennung von Spielern **und** Saves
sowie spätem Zeitfenster muss vor dem Fit erfolgen. Gegen `CA bleibt gleich`
und eine nur auf Trainingsdaten geschätzte Alters-/PA-Gap-Baseline testen.
Diese Arbeit hat n=0solcher unabhängiger Testverläufe; keine synthetischen
Werte oder Querschnittsprofile werden als Ersatz verwendet.

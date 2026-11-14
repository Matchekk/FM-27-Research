# Test FM Research – privates Real-Save-Erfassungsprotokoll

**14.11.2026 · Vorbereitung, keine native Karrierefreigabe.**

Der Wegwerfspielstand **Test FM Research** soll den Übergang vom synthetischen Labor zu realistischen Karrieresituationen ermöglichen. Er ist zunächst eine **Kalibrierungsquelle**, kein unabhängig repliziertes Karriereexperiment. VALID-002 gibt weiterhin nur das gebündelte kontrollierte Fixture frei; ein akzeptierter FM-Save oder PKM-Reader ist kein Beleg für originalgetreue Replays.

## Am PC: Datensatz für genau eine Partie vorbereiten

1. In `Test FM Research` einen stabilen, separaten **PRE-Save unmittelbar vor einem konkreten Match** erstellen, beispielsweise `Test FM Research - PRE.fm`. Den Schreibvorgang vollständig abschließen lassen. Einen bereits wichtigen Save nicht überschreiben.
2. Privat notieren: tatsächlichen Spiel-Build, Club/Liga/Saison, Matchdatum/Gegner, Teamseite, IP-/OOP-Taktik, Aufstellung und Bank, Fitness/Schärfe/Vertrautheit sowie Wechsel-/Matchmanagementpolitik. Fehlende Originalwerte als `unknown` dokumentieren, nicht durch Defaults ersetzen.
3. **Ein** Spiel im normalen Karriereablauf durchführen; alle manuellen Änderungen mit Minute notieren. Anschließend einen getrennten **POST-Save** erstellen, ohne den PRE-Save zu überschreiben. Für die reine Erstinventur reicht auch schon PRE allein.
4. Die zugehörige **PKM** und optional **REC** sichern. Der automatische Ordner liegt in vielen FM-Versionen unter `Documents\Sports Interactive\<Football Manager title>\matches\automatic`, aber den tatsächlich verwendeten FM27-Pfad prüfen. REC-Dateien können kurzlebig sein. Keinen Matchdateinamen als Beweis der Zugehörigkeit betrachten: Matchzeit/Gegner/Spielstand später mit einer unabhängigen Quelle abgleichen.
5. Nur explizit ausgewählte private Dateien lokal hashen, zum Beispiel in PowerShell von der Repositorywurzel:

```powershell
python analysis/capture_test_fm_research.py `
  --pre-save 'C:\PFAD\Test FM Research - PRE.fm' `
  --post-save 'C:\PFAD\Test FM Research - POST.fm' `
  --pkm 'C:\PFAD\mein-match.pkm' `
  --rec 'C:\PFAD\mein-match.rec' `
  --output 'local/test-fm-research/capture-001.json'
```

`--post-save`, `--pkm` und `--rec` sind optional. Für jede weitere Aufnahme einen **neuen** Output-Namen verwenden, z. B. `capture-002.json`; kein Überschreiben. Pfade müssen tatsächlich existieren und die jeweiligen Endungen tragen. Läuft FM noch und verändert gerade einen Save, die Datei erst nach abgeschlossenem Speichern erfassen.

Der Erfassungsbefehl startet **weder FM noch eine native Matchsimulation**, liest keine Spielinhalte, verändert keine Originaldatei und reserviert keine Seeds. Sein JSON-Receipt enthält nur Rollen, Dateiformat, Bytezahl, Hash, UTC-Zeit und ausdrücklich **nicht freigegebene** Fähigkeiten. Keine Originalnamen/Pfade werden in das JSON aufgenommen. Es liegt ausschließlich im durch `.gitignore` ausgeschlossenen `local/`-Ordner. Auch `.rec`-Dateien bleiben vom öffentlichen Repository ausgeschlossen.

## Aussagegrenzen

- Datei-Hashes beweisen Byteidentität; **nicht** die fachliche Bedeutung einzelner Felder, die Matchzugehörigkeit, Originalmanagerentscheidungen oder Replay-Treue.
- Gespeicherte Karriere-PKM können unterschiedliche Kaderkapazitäten besitzen. Den historischen Record-17-/23er-Transferfehler **nicht** durch Kürzen/Auffüllen umgehen.
- Unveränderte Saveklone mit gleichem RNG sind keine unabhängigen Replikate. Spieler/Wochen innerhalb eines Saves sind ebenfalls keine unabhängigen Karriereversuche.
- Es fehlen bis auf Weiteres validierte Karrierefortschreibung, individuelle Trainingsbeteiligung, vollständige SET-Ausführungs-/xG-/Besitzkettenzähler sowie passive Erstschritt-/Familiarity-Belege.
- Weder Saves noch PKM, REC, EXE, DLL, FMF, private Namen/IDs oder Rohdumps ins öffentliche GitHub-Repository stellen.

## Forschung und Weiterentwicklung

[VALID-004-Plan](../../experiments/VALID-004-test-fm-research.md) trennt privaten Capture, Decoder-/Kapazitätsinventur, korrekte Rohfeldzuordnung, späteren technischen Native-Gate und echte Karriereexperimente. Ein externer Agent kann die Dateien **nur** lesen, wenn die lokale Codex-Sitzung die betreffenden Pfade tatsächlich sieht; dieser GitHub-Connector kann sie nicht aus dem laufenden PC abholen.

Quellen zur Bedienung: [SEGA Save-Speicherorte](https://support.sega.com/hc/en-us/articles/29294682943633-Where-can-I-find-my-Football-Manager-save-game-files), [Sports Interactive PKM/REC](https://community.sports-interactive.com/bugtracker/1644_football-manager-26-bugs-tracker/1872_fm26-bug-tracker-introduction/how-to-upload-pkms-rec-files-r23721/), [SEGA Backups](https://support.sega.com/hc/en-us/articles/29579386335889-How-to-back-up-Football-Manager-game-files). Die beiden FM26-spezifischen Hinweise sind **nicht** automatisch eine validierte FM27-Pfadgarantie.

# VALID-004-CAREER-R1: eingefrorener Runtime-V10-Reader

Status: **vorbereitet, nicht zur Save-Ausführung freigegeben**. Eigene rein
lesende Teilstufe von [VALID-004 Phase 1](VALID-004-test-fm-research.md).
[R0](VALID-004-career-readonly.md) bleibt mit seinem Buildzulassungsfehler
unverändert; dieser Vertrag ersetzt weder dessen Ergebnis noch VALID-002.

Fragestellung: Welche strukturellen Tabellen und Metadaten kann der vorhandene
Runtime-Kompatibilitätspfad auf genau einer bereits autorisierten, eingefrorenen
Testkarriere lesen? Primär ist das vollständige Ledger aller zwölf Probeplätze;
sekundär sind anonyme Feld-/Zählwertkonsistenz mit dem separat registrierten
[R2](VALID-004-career-readonly-R2.md), Warnungen und vorhandene Strukturprüfungen.
Keine Leistungs-, Trainings- oder kausale Hypothese; eine Datei, keine
unabhängigen experimentellen Replikate, keine Effektgröße oder Powerplanung.

## Identität und Grenzen

- Ausschließlich bestehende private R0-Kopie, 147.130.636 Bytes,
  SHA256 `1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
  Keine Neuaufnahme des Originals und keine andere Karriere.
- R0 berichtete Last-writer-Build `27.0.1+2503222`, Summaryschema 31.
  Dies ist keine Aussage über installierten nativen Engine-Build. R0 scheiterte
  an exakter Buildzulassung; strukturelle Schemaänderung wurde dadurch nicht bewiesen.
- Runtime-Profil `fm27-save-2486695-2503222-v10`, dessen beide Wrapperdateien und
  sämtliche vendorten Pythonquellen werden gehasht. Die dort ausgegebene
  fmsave-Version `0.9.0` stammt aus geschützter Basis-Distributionsmetadatei und
  ist **keine unabhängige Releaseidentifikation der vendorten Quellen**.
- Fremdquellen, Basisvenv und R0 bleiben unverändert. Keine Low-level-Guardpatches,
  kein falsches Buildlabel, keine nativen Hostimporte.

Der V10-Pfad registriert bekannte spätere Builds und verändert gespeicherte
Layoutzuordnungen. Sein Summarypfad fängt `ReaderCheckError` aus
`read_summary_facts` ab und versucht `desktop_save_draft.read_summary`.
Eigene passive Wrapper zählen Summaryaufrufe, Draftversuche, angenommene
Draftresultate und Draftausnahmen; Rückgabewerte und Ausnahmen bleiben erhalten.
Ein akzeptiertes Draftresultat ist eine Parserannahme, keine native Validierung.
Testfälle prüfen diese Instrumentierung mit synthetischen Objekten.

## Eingefrorener Ablauf und Gates

Vertrag und Quellenmanifest: [R1-contract.json](../data/night-001-career-r1/R1-contract.json).
Vor einem echten Pass müssen Code, Vertrag, dieses Dokument und unabhängiges
Review auf `origin/main` veröffentlicht sein; eine Freigabedatei bindet vollen
Commit-SHA, erfolgreich abgeschlossenen CI-Lauf auf genau diesem SHA und
veröffentlichten Reviewhash. Zusätzlich erteilt der Research Director ausdrücklich
`published proceed`. Der Arbeitsbaum-Worktree darf keinen echten Pass starten.

Ein Decoderprozess liest in fester Reihenfolge:
`open`, `managed_clubs`, `clubs`, `players`, `training`, `tactics`, `selections`,
`set_pieces`, `staff`, `staff_lists`, `injuries`, `fixtures`.
`strict=True`; jede Ausnahme oder angewendete fehlgeschlagene blockierende Prüfung
stoppt den Rest. Warnungen, ausgeliehene Layoutangaben, Coverage-Gates ohne Nenner
und Advisory-Ausfälle bleiben explizit erhalten und verlangen spätere Prüfung.
Fehlende Checks bedeuten fehlende Evidenz, keinen bestandenen Test.

Je Probe wird zuerst `started` dauerhaft geschrieben. Fehler, unaufgelöste Starts,
unbegonnene Plätze, ungültige Ledgerzeilen und Supervisorabbrüche bleiben erhalten.
`export-status` rekonstruiert ausschließlich gespeicherte Ledgers; es öffnet keinen
Save und startet keinen Ersatzprozess. Kein Retry, kein Überschreiben eines
vorhandenen Attemptmarkers. Hashabweichung vor Start verhindert das Decoding;
Hashabweichung danach sperrt die Vergleichsauswertung.

## Ressourcen, Daten und Interpretation

Ein exklusiver Reader-Lease serialisiert R1 und R2 unabhängig von nativen Jobs.
Budget **180 s pro Profil einschließlich Snapshotprüfungen und Abschluss**,
**3 GiB Prozess- und Job-Private-Memory**, maximal **ein** tatsächlicher
Decoderprozess, **512 MiB neue private Artefakte**, null Wiederholungen.
Nur bei mindestens 185 s Restzeit vor `2026-11-14T23:00:00Z` starten.
Bei Deadline/Artefaktgrenze wird ausschließlich der eigene Prozess beendet.
Ressourcenüberschreitung bleibt ausgewiesener technischer Fehlschlag.

Der Supervisor startet den tatsächlichen Basisinterpreter direkt und bindet die
eingefrorene Venv-Site explizit ein. Windows-Venv-Redirectoren können zusätzliche
Prozesse erzeugen und werden deshalb nicht als Decoder gestartet. Ein Windows
Job Object erzwingt Prozessanzahl 1, beide Speicherlimits und Kill-on-close;
Kernelreadbacks werden dokumentiert. Harmloser Test: 128-MiB-Allokation unter
64-MiB-Limit wird abgewiesen; zweiter Test belegt Kill-on-close. Diese Tests
öffnen keinen Save. R0s Launcher-Speicherbeobachtung ist kein tatsächlicher
Decoderpeak und wird durch diese Vorbereitung nicht nachträglich geändert.

V10 begrenzt Dekompression zusätzlich auf 768 MiB pro Frame und 1536 MiB insgesamt.
Die Probe kann trotzdem vor vollständigem Decoding abbrechen. Die anonymen
öffentlichen Outputs nennen Quelle und Einheit je Feldgruppe; private Namen,
IDs, Pfade, Warnungstexte, Savebytes und Rückgabeobjekte bleiben lokal.
Parser-Roh- und Anzeigewerte bleiben als solche gekennzeichnet, ohne UI-Kalibrierung.
Historische Verletzungsrecords und aktuelle TYPED-Kohorten werden getrennt gezählt;
ein fehlender Clubwert wird niemals als verwalteter Club identifiziert.

RNG-Unabhängigkeit, tatsächliche Trainingsteilnahme, Coach/Fokus/Intensitätsbindung,
Verletzungsdauer, aktiver Taktikkontext, native Feldsemantik, Karriereadvance und
Replay bleiben gesperrt. Ein vollständiger Parserlauf wäre nur ein struktureller
Lesbarkeitsbefund. Keine Seeds, nativen Starts, Matchsimulationen oder Kalenderaktionen.

## Vorbereitungsstatus

CLI: `analysis/audit_career004r1.py prepare` erzeugt nur Metadaten-/Quellenverträge;
es öffnet oder hasht keinen Save. Tests sind synthetisch beziehungsweise verwenden
harmlose eigene Prozesskinder. Bis zur ausdrücklichen Freigabe existieren **null
R1-Saveversuche**. Fachagent liefert lokalen Commit; Integration, Review, CI und
Push erfolgen durch den Research Director.

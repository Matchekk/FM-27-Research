# VALID-005-OBSERVER-V1 – passiver Zustandsrecorder

14.11.2026. **Offline implementiert und privat kompiliert, noch nicht nativ
validiert.** Keine neue wissenschaftliche Leistungsstudie und keine MECH-002-
oder Karrierefreigabe. [Entwurfsvertrag](../data/night-001-observer/contract-draft.json),
[Buildbelege](../data/night-001-observer/build-report.json),
[Quell-/Datenflussbefund](../data/night-001-observer/static-dataflow.json).

## Technische Hypothese und Geltungsbereich

Ein opt-in Recorder kann nach Originalvorbereitung, nach der ersten tatsächlich
erfolgreichen Tickfortschreibung und vor dem natürlichen Matchteardown rohe
MATCH_PLAYER-Zustände lesen, ohne das native Ergebnis zu verändern.
Kontrolle bleibt die unveränderte ausgelieferte Hostdatei mit D00;
Behandlung sind ausschließlich zusätzliche Lese-/Logoperationen eines getrennten
Hosts. **Keine Setter, Clamps, Executionhooks oder neuen Versionsumschreibungen.**

Vorhandener Build: Engine27.0.1+2503222, DLL-SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Quellbasis Tactics Lab v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be,
sauberer MIT-Upstream. Historische Runtime und Host bleiben unangetastet.
Der neue Beobachterhost hat SHA256
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`;
dieser Hash gehört **nicht** zur bestehenden VALID-002-Freigabe.

## Beobachtungsarchitektur

```mermaid
flowchart LR
  A[Unveränderte D00-Bytes] --> B[Originale Eingabe und Vorbereitung]
  B --> C[Originale Readbacks und Inputdump]
  C --> D[Passiv: prepared]
  D --> E[Originaler erster Advance-Aufruf]
  E --> F[Passiv: first_advance nach Erfolg]
  F --> G[Unveränderte Simulation]
  G --> H[Passiv: finished vor Teardown]
```

Fünf minimale Einfügestellen: Include, opt-in/input gate vor Source-/Execution-
Installation, `prepared`, `first_advance` unmittelbar nach erfolgreichem originalem
`0x4764ac0`-Aufruf und dessen Stallcheck, `finished` innerhalb des natürlichen
Endzweigs vor Statsausgabe/Teardown. Der Header schreibt nur in Host-Logdateien
und eigene Stackvariablen. Kein Aufruf originaler Enginesetter; keine neuen
Hooks oder Schutz-/Versionsänderungen. Speicherlesbarkeit und26erObergrenze werden geprüft.

`FM27_PASSIVE_OBSERVER_V1=1` aktiviert den Recorder. Fehlender Wert bedeutet
keine neuen Snapshots; andere Werte werden mit252 abgewiesen. Kind61-Execution
und Source-Generation-Blobs sind bei aktiviertem Recorder verboten. Der Rootrunner
muss die übrigen `FM27_*`-Variablen entfernen und nur ENGINE_ROOT/GAME_ROOT/
EXPECTED_DLL_SHA256/PASSIVE_OBSERVER_V1 explizit setzen. Keine anderen Diagnosehooks.

Es gibt zwei verschiedene Defaultaussagen: `instrument_source(..., enabled=False)`
erhält die Quelldatei bytegleich; der bereits instrumentierte Host mit Laufzeit-
Opt-in aus hat zusätzliche Rückkehrguards. **Dieser neue Host ist nicht binärgleich
zum ausgelieferten Host.** Ergebnisgleichheit muss erst der vorgegebene native
Viermodusvergleich belegen. Der historische Encoder/NativeLab.HOST wird nicht verändert.

## Was gelesen wird und was damit nicht belegt ist

Pro Stage beide aktiven23erKader mit privaten IDs zur eindeutigen Zuordnung:

| Datenquelle | Rohfelder / Regionen | Grenze |
|---|---|---|
| Aktueller MATCH_PLAYER aus Team+0x138 | Condition+c8a,Sharpness+c90,secondary+c7a,Fatigue+c84 als16bit | Eingabespeicher ist keine automatisch kalibrierte UI-/Consumerwirkung |
| Derselbe Actor | +1c74 als32bit,+1aa6 als16bit | Statisch beteiligte Akkumulator-/Abzugsrohwerte; keine bestätigten UIeinheiten |
| Actor+0xcba |33Bytes roh | Keine Prozent-/Understanding-/Abilityinterpretation |
| Actor+0x1df0 |112Bytes roh nahe bereits bekanntem Runtime-Morale-Feld | Uninterpretierter privater Explorationsbereich, kein Endpunkt |
| Pointer Actor+0x1880 | Statistikspeicher+0x80..0x90; Bench kann `null` sein | Byte89/8a sind native Datenflusskandidaten, keine unabhängig kalibrierten UIwerte |

Prepared-Werte der vier Felder und33Bytes werden direkt gegen die bestehende
private `input_tail_hex`-Region gebunden. Erstfortschreibung verlangt Ordinal1,
erfolgreich erhöhten Tick und angefordertes Ziel `before+1`. Finish ist an das
tatsächliche `natural_match_finished` samt Tick/Clock gebunden. Aktive Spieler
brauchen einen tatsächlichen Runtime-Cache; `null` wird nicht als Null ersetzt.
Kader-/Identitätsmengen bleiben erhalten; reine Slotvertauschungen am Ende
werden über private Identitäten gebunden.

**Wichtiger statischer Befund:** Originalfunktion RVA0x36a20 liest unter anderem
Actor+c8a/c7a und hat separate Ableitungen: Actor+c90 sowie Bytes89/8a des über
Actor+1880 erreichbaren Statistikobjekts. Ein nachträglicher Schreibzugriff nur
auf Profilfelder könnte daher bereits gebildete Caches auslassen. Dieser Recorder
implementiert keinen solchen Setter und beweist dessen Wirkung nicht.
Private aktuelle DLL-Disassemblate und ihre Hashes bleiben lokal.

Der Originalsampler0x465b0 hat einen Versionsvergleich an0x47a01 gegen
0x1a080018 vor Zugriffen auf CBA/CD8/CD9/CDA. **Die alte Carrierangabe26.8
beweist keine inaktive Tactical-Effectiveness-Verarbeitung:** bereits vorhandenes
Kind62 setzt vor Vorbereitung MATCH+a3a auf0x1b000000 und Manager-PI-Versionen;
der ursprüngliche Verifier prüft dies. Der Recorder erhält diese D00-Bytes und
liest die tatsächliche Version in allen drei Stages. Das erfüllte Versionsprädikat
allein beweist wegen weiterer Zweige noch keine Ausführung aller Consumer.

## Vorab festgelegte kleine technische Prüfung – nur durch Root

Vier Eingabezellen: high_press/deep_block × Testteam Heim/Auswärts.
Jede bekommt genau einen frischen technischen Seed und dieselben D00-Bytes in
vier Modi: ausgelieferter Referenzhost, neuer Observer aus, Observer an,
Observer an wiederholt. **16Vollmatches**, keine Leistungsinferenz.
Vier unabhängige technische Seedzellen, keine16 unabhängigen Wirkungsreplikate.

Zwei weitere erwartete Abweisungen: Observerwert2→252 und beschädigtes Binärformat
→108, ohne natürliches Ende. Es werden genau vier frische Seeds reserviert:
die Umgebungsnegativprobe nutzt den Seed der ersten technischen Zelle ohne
einen weiteren Seed; die beschädigte Binärprobe verwendet keinen Seed.
Keine historischen/anderen reservierten Seeds und keine Ersatzseeds. Zwei
Loader-/Imageprüfungen (Originalhost/neuer Host) erfolgen vor den Vollmatches.
Damit sind **20logische native CLI-Probes =2Loader+16Vollmatches+2Negative**
vorab begrenzt; die Loader sind keine zusätzlichen Matches.

Primäres technisches Kriterium: exakt gleiche Scores, Endticks/Clock und sämtliche
originalen Teamstatistiken zwischen den vier Modi jeder Zelle. Sekundäre Gates:
0Snapshots in Referenz/aus, genau3 korrekte Snapshots in an/Wiederholung,
vollständige Originaleingabereadbacks und Prepared-Dumpbindung; die identifizierten
vier Profilrohfelder, zwei Akkumulator-/Abzugsrohfelder,33Bytes und Cachebytes89/8a
in den beiden An-Läufen exakt gleich. Das uninterpretierte112Byte-Fenster wird
erhalten und gehasht, aber wegen möglicher unidentifizierter Pointer/Metadaten
nicht als deterministischer A/A-Endpunkt verwendet.
Keine p-Werte, Powerplanung oder kleinen Leistungsunterschiede aus diesen Daten.

Root muss Vertrag/Code/konkrete Seeds vor Ausführung veröffentlichen,
CI/Independent Review und alle Identitätsgates prüfen. **180s kumulierte Childzeit,
900s unverrückbare UTC-Frist, ein gewählter Worker (globale Obergrenze4),90s ohne
Fortschritt,512MiB private Artefakte/20GiB Speicherreserve.** Globales Nachtbudget
und bestehende zentrale NativeLease zusätzlich zwingend; Root ist alleiniger
nativer Supervisor. Alle20CLI-Probeplätze (18Match-/Negativplätze und2Loader) erhalten;
Gatefehler stoppen,kein Retry/Reset/Ersetzen. Kein gebündelter automatischer Mainlauf.

## Tatsächlicher Implementierungsstand

Eigener Header, Minimalpatch, isolierter Builder, strikter Offlineauditor und
synthetische Regressionen vorhanden. Compilerdatei19.42.34433.0/Product14.42.34433.0,
MSVC2022 mit vorhandenem SDK10.0.22621.0. Kein Download/Installer.
Erster Entwicklungsbuild scheiterte am fehlenden SDK-bin-PATH für `mt.exe`,
unverändert behalten. Build2 kompilierte; vor jedem nativen Start um die
Runtime-Caches ergänzt und als neuer Build3 kompiliert. Alle Entwicklungsbelege
bleiben erhalten. **0neue native Hoststarts/Matches,0Seeds,0Spieländerungen.**

Ein synthetischer Parsererfolg erteilt ausdrücklich keine native Freigabe;
alle Release-/Consumer-/UI-/Startpolicy-/Karriereflags bleibenfalse.
MECH-002-512erHauptserie, Karriere-Replays/Advance und Holdouts bleiben gesperrt.

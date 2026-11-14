# Forschungsrunde 3 – ATTR, MECH und TRAIN

Geprüfter Abschluss 14.11.2026, Europe/Berlin. Drei tatsächliche Codex-Fachagenten
arbeiteten parallel in getrennten Worktrees/Branches; danach folgte ein separater
unabhängiger Reviewer. Director integrierte,publizierte und führte als einziger
Supervisor die native Forschung unter gemeinsamer NativeLease aus.

**ATTR-009-Bridge vollständig:384Hauptmatches/32unabhängigeSeedblöcke,
32Technikmatches/8exakteA/A-Paare plus Exit108-Negativkontrolle.** Alle417Jobs
erhalten,0Ausfälle/Retry/Ersatz/Exklusion/Holdouts/Karriereadvances. Keine Erweiterung.

Primär `[JR−(Acc+Pace)/2]spezialisiert−[JR−(Acc+Pace)/2]omni`:
**−0,162xGD**,95-%-KI**[−0,488;+0,164]**,p0,31885. Die Interaktion bleibt
unklar. VolleBreite0,65282 verfehlt das Pilotziel0,50. Kein sekundärer Holm5-Nachweis;
Punktekontrast−0,133[−0,787;+0,521]. Kein Äquivalenzbeweis,keine globale neue
Attributrangliste und keine Erklärung der internationalen Diskrepanz.
[Ergebnisbericht](../../experiments/ATTR-009-results.md),[Rohmessungen/Provenienz](../../data/attr-009-bridge/README.md).

MECH-002 liefert einen geprüften Offline-Startpolicycodec,bleibt aber wegen
fehlender Nach-Vorbereitungs-/Erstschritt-/Familiaritybelege blockiert:0nativeStarts,
0neueSeeds. TRAIN-002 liefert strikte Checkpointdiagnostik ohneSave-Decoder/Executor;
RNG-/Teilnahme-/Einheitengates bleiben blockiert:0Advances/0Seeds. Keine Ersatzstudien.

124integrierteRepositorytests und5historischeAnalysetests bestehen. Zwei echte
Reviewbefunde wurden **vor Freeze** korrigiert: fehlende33unbegonneneTechnikplätze
im Vorbereitungsexport und unstrengeTRAIN-Session-/Slottypen. Die erste CI
scheiterte am flachen Checkout des neuen Gitblob-Archivvergleichs; vollständige
Historie korrigiert,kein Hashgate abgeschwächt und kein nativer Retry.

## Verantwortlichkeiten

| Bereich | Branch | Exklusive neue Dateien | Freigabegrenze |
|---|---|---|---|
| ATTR | `codex/round3-attr` | `research/attr009.py`, eigene ATTR-009-Analyse/Tests/Vertrag, `ATTR.md` | Masken-/Rohdosis-Audit vor 384 Hauptmatches |
| MECH | `codex/round3-mech` | `research/startpolicy.py`, eigene MECH-002-Dateien, `MECH.md` | Passive erste Fortschreibung und Familiarity zwingend |
| TRAIN | `codex/round3-train` | `research/training002.py`, eigene TRAIN-002-Dateien, `TRAIN.md` | Keine Kalenderfortschreibung oder Hauptserie |
| Review | `codex/round3-review` | Eigener `analysis/review_round3.py` und getrennte Reviewberichte | Rohbelege selbst nachrechnen,keine native Ausführung |
| Director | `main` | Integration, gemeinsame Übersicht/Queue/Baseline, native Ausführung | Ein Supervisor, maximal vier Worker |

Getrennte Fachberichte: [ATTR](ATTR.md),[MECH](MECH.md),[TRAIN](TRAIN.md).
Diese dokumentieren die jeweiligen ursprünglichen Fachbeiträge;die zentralen
Ausführungsergebnisse stehen in dieser Übersicht und im Ergebnisbericht.

Verbindlich ist [der Round-3-Auftrag](../../experiments/NEXT-ATTR-MECH-TRAIN-round3.md).
Keine Holdoutausführung, alten Seeds, Ersatzsimulationen oder automatische
Folgerunde. Historische Quellen und Messungen werden durch
`baseline.json` gegen Commit `7767d859e3a66a9aedcf9c1574f3e48dc8dc841f`
mit LF-normalisierten SHA256 geschützt.

## Zu Beginn erneut geprüft

Main war sauber und auf `origin/main`; dessen CI 43612939765 war erfolgreich.
DLL-Dateiversion 27.0.1, Produktbuild 27.0.1+2503222. DLL, Host, gebündeltes
Fixture und Katalog stimmen im direkten Dateihash mit VALID-002 überein:

| Artefakt | SHA256 |
|---|---|
| DLL | `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340` |
| Host | `2d5b5f3a49860faa091141e265554e70fd7f41eaced6aab5d263df548fc8500e` |
| Fixture | `39c594c7e876cc0ad325dfa51c377f4cf360840612479ed72d800ec548e504b6` |
| Katalog | `c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c` |

Auch der erneut aus elf tatsächlichen Dateien berechnete Ressourcenfingerprint
`6b47303bf12762f83dc0d83485de44ce139363d0a399959bcf496370e18c8883`
stimmt überein. Upstreamquelle sauber auf v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be.
Dies ist ein statischer Identitätscheck, keine vorweggenommene Freigabe neuer
Eingriffe. Die nachfolgenden ATTR-Loader-/Input-/Laufzeitgates wurden tatsächlich
geprüft;MECH/TRAIN bekommen daraus keine zusätzliche Freigabe.
Private Engine-/Spielmaterialien bleiben lokal.

## Technische Abgrenzung

MECH findet derzeit keine passive Profilaufnahme nach dem ersten Simulationsschritt
und keine unveränderten Familiarity-Receipts. TRAIN findet keinen validierten
Karriere-Executor und keine unabhängigen RNG-/individuellen Teilnahmebelege.
Diese Lücken werden durch sichere Offline-Module diagnostiziert; daraus folgt
keine Freigabe der jeweiligen Hauptserie.

ATTR definiert rohe Abilitywerte 60→80 ausdrücklich als native Dosis. Die
Lab-Anzeige `raw/5` ist kein Beweis einer FM-Karriereanzeige. Der verbindliche
Auftrag erlaubt einen totalen Masken×Attributkontrast bei ausdrücklich
unidentifizierter Mechanismuszerlegung; fehlende passive Effektivitätsgrößen
werden weder synthetisch ergänzt noch experimentell neutralisiert.

## Unabhängige Abnahme und Budgets

[Offline-Preflight](REVIEW.md) → [24konkreteInputs/Seeds](INPUT-REVIEW.md) →
[32echteTechnikmatches](TECH-REVIEW.md) → [384erErgebnis-/Belegprüfung](RESULTS-REVIEW.md).
Eigener Rechenkern ohne Projektanalyse-/Statistikimporte rekonstruiert6Endpunkte,
Welch-/Bootstrapintervalle,Holm5,Kontext-SDs,alle192Blockwerte und zukünftige
Fallzahlminima. Alle384privatenLogs/Dumps zusätzlich geprüft:
1.218.816Attributwerte/406.272direktdecodierteProfilfelder/16.896Phasenzellen/
287.232PI-Gruppen. Alle13eingefrorenenAutorenquellen/7Inputs und272historische
Dateien gegen ihre Gitblobs unverändert.

Preregfc14746685f0a1f6475b1968912317d9ffabdfb6/CI43616995356 vorTechnik;
Techrelease06f1aeb22c88eb1188c35cae5a7cdb3b453c7740/CI43617519052 und
unabhängigerReview vorMain. Gateverweis e9ac939 ebenfalls vorMain veröffentlicht.
Code/Seedplan/Eingriff nach Beginn unverändert. Nur dieser neue Runner nutzt
den eigenen zentralen Budgetpfad;historische Runner sind nicht nachträglich global gesperrt.

Verbrauch **231,558/600Child-Sekunden**,Studienfenster **753,168/1200s**,
unverrückbareFrist18:00:36,423CET eingehalten;höchstens4Worker/90sFortschritt.
PrivateRohartefakte≈182,44MiB unter2GiB,kein verbleibenderaktiverLease/Prozess.
LizenzierteBytes/privateSpieleridentitäten bleiben lokal.

[Agenten-/Commit-/Statusledger](QUEUE.json),[aktuelleModulprioritäten](PRIORITIES.md).
Vorrang haben passive Messgates und realistische Profile,SET-Exposition und
TRAIN-Replikatgrundlagen;danach neueTACT-Rollen/OOP-Fragen. Keine automatische
1176–6216Match-Bestätigung,Holdouts,Karriere-Replays oder Runde4. Nach finaler CI stoppen.

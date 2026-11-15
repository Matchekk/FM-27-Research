# TACT-003-STLESS-R0 – IP/OOP-Paketpilot

Aktuell:512/512 Mainmatches mit64 neuen Seedblöcken vollständig und unabhängig
nachgerechnet. TECH32+1 und16 exakte A/A-Paare bestanden; alle Rollen-/Positions-
zuordnungen nativ bestätigt. Keine unerwarteten Ausfälle, Missing Values oder Retries.
68 neue Seeds gegen2665 frühere/reservierte Werte gebunden.
[Vorregistrierung](../../experiments/TACT-003-stless-preregistration.md) ·
[Neuheitsprüfung](../../docs/night-002/STLESS003-NOVELTY-REVIEW.md) ·
[Runnerprüfung](../../docs/night-002/STLESS003-RUNNER-REVIEW.md).

Primäre IP×OOP-Interaktion+0,074xGD-DoD[−0,191;+0,340] bleibt unklar;
konkretes marginales IP-Paket−0,350xGD[−0,502;−0,198],Holm7-p0,000162.
[Ergebnisbericht](../../experiments/TACT-003-stless-results.md) ·
[unabhängiger Ergebnisreview](../../docs/night-002/STLESS003-RESULTS-REVIEW.md).
`main.jsonl` enthält ausschließlich zulässige kompakte Matchmessungen;
`effects.json`,512 abgeleitete Kontrastzeilen und Provenienz sind reproduzierbar.

Vier Arme: unveränderte IP4231/OOP4411, IP4240 allein, OOP4420 allein und beide
Pakete. Es ändern sich ausschließlich0/3/3/6 ursprüngliche Positions-/Rollen-
Records; keine Spieler, Attribute, Eignungswerte oder expliziten PI.
Das ist ein Paketvergleich einschließlich lateraler Neuordnung und intrinsischer
Rollenwirkung, keine isolierte Entfernung eines Stürmers und kein Laufwegtracking.

`inputs.json` bindet Dateien, Software-/Engine-/Host-/Ressourcenidentitäten und
den tatsächlich ausgeführten administrativen Fortsetzungsbeleg. Der alte
MECH-004-Stopp wird nicht aufgehoben:257 Calls/838,064s, alle545 Reservierungen
und589,7353507 globale Childsekunden bleiben erhalten. Der neue Vertrag besitzt
zusätzlich30s absoluten Calltimeout und40s Envelope je ungelöstem Claim,
missionweit höchstens3600 summierte Calls sowie unverändert die engere eigene
900s/5400s-Studienfrist und die globale Phasen-/Byte-/Workergrenze.

`mission-administration.json` ist ein zulässiger Receipt ohne Tokens/PIDs/private
Pfade. `seed-plan.json` enthält ausschließlich neue wissenschaftliche Seeds;
keine alten oder gehaltenen Seeds werden verwendet. Private Binäreingaben und
Originaldumps bleiben lokal.

Erst vollständige freigegebene Mainmessungen erlauben die feste Analyse:

```powershell
python -B analysis/report_stless003.py
python -B analysis/review_stless003.py public-technical
python -B analysis/review_stless003.py public-main
```

Primär physische IP×OOP-xGD-DoD; sieben Sekundärtests gemeinsam Holmkorrigiert.
512 Matches sind64 unabhängige neue Seedblöcke; beide Seiten im Seed gemittelt,
zwei feste Kontextgewichte je1/2. Acht vorab definierte Kontraste ergeben512
abgeleitete Seedkontrastzeilen. Positive Interaktion allein beweist weder einen
positiven einfachen Paketeffekt noch einen universellen Taktiksieger.

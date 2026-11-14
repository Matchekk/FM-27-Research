# Forschungsrunde2 – TACT, VALID und SET

14.11.2026. Drei tatsächliche Codex-Subagents arbeiten parallel in getrennten
Branches/Worktrees. Research Director integriert, publiziert und führt allein
native Phasen aus. Unabhängiger Review folgt nach Implementierung und erneut
nach TACT-Ergebnissen. Keine Holdout- oder Karriereausführung.

## Verantwortungsgrenzen

| Agent | Branch / Worktree unter ignoriertem local/worktrees | Schreibbereich |
|---|---|---|
| TACT | codex/tact002-r0 / tact002-r0 | neue TACT002R0-Runner/Analyse/Exporter/Verifier/Tests/Experimentunterlagen |
| VALID | codex/valid003-round2 / valid003-round2 | neue validation003/coordination_testpath-Module, eigene Tests und Offline-Diagnostik |
| SET | codex/set-v0 / set-v0 | neuer set_v0-Parser, eigene synthetische Goldtraces und Tests |
| Independent Reviewer | eigener späterer Reviewpfad | unabhängige Rechen-/Quellprüfung, keine nativen Starts |
| Director | main | Integration, CI/Push, zentrale Seedreservation und einziger nativer Supervisor |

Studienvertrag: TACT-002-R0 klein, vier vollständige Rollenarme, D00-Baseline,
32neue Seeds je bisherigem Discoverygegner, beide Seiten,512Hauptmatches/64Blöcke.
32technische Vollmatches/16A/A-Paare plus eine Binärnegativprobe. Maximal4Worker,
90s ohne Fortschritt,900s kumulierte Child-Zeit und1800s feste UTC-Frist.
Keine Erweiterung auf1024, keine Ersatzseeds oder ergebnisabhängige Exklusion.
Vor Hauptmatches veröffentlichte Vorregistrierung/Code/Seeds, bestandene native
Gates und erfolgreiche CI. Native Lease um den gesamten beaufsichtigten Childlauf.

VALID und SET beginnen ausschließlich offline. Eigene Profilvektoren sind noch
keine native Wirksamkeitsfreigabe; PKM-Kapazität bleibt ohne tatsächlichen Reader
unbekannt. SET-V0 akzeptiert zur Zählerberechnung ausschließlich klar eigene
synthetische Vertragstraces, native Eingaben bleiben unresolved.

[Historischer Ausgangsstand](baseline.json):193 unveränderte wissenschaftliche
Archivdateien gegen790727f. Aktualisierungen der Übersichtsdokumente stehen
getrennt von den erhaltenen Studien. Dieser anfängliche Koordinationsstand wird
nach tatsächlicher Ausführung um Test-/Gate-/Ergebnis- und Reviewbelege ergänzt.

## Geprüfter Offline-Stand vor nativer Vorbereitung

[TACT-Implementierung](TACT.md),[VALID](VALID.md),[SET](SET.md) und
[unabhängiger Preflightreview](REVIEW.md) sind integriert.86Repositorytests,
5historische Analysetests und sämtliche alten Match-/TACT-Verifier bestehen.
Vier echte frühere D00-Dumps wurden ohne Serverimport nachauditiert:
je44Rollen-/44PI-Zellen/748Gruppen. Das ist kein neuer Rollenarmtest.

Zwei Reviewbefunde wurden vor Registrierung/Nativevorbereitung korrigiert:
SET verlangt lückenlose illegale Vorgängerlinks bei Wiederholungen; TACT darf
vor einem abgewiesenen Retry keinen alten Leasebeleg überschreiben.
Regressionen bestehen. VALID korrigierte außerdem seine erste Offline-
Skalenannahme: Abilityrohwerte gehen bis100 statt20. Keine nativen Fehlmatches.

Zentraler VALID-Smoke:21eigene Vektoren und zwei harmlose Python-Probes,
0nativeStarts/0Seeds. [Erlaubte Offlinebelege](../../data/valid-003-preparation/offline-report.json).
SET verfügt über elf eigene synthetische Goldfälle; native Quellen bleiben
zwingend unresolved/null. Keine Karriere-, Profil- oder SET-Wirksamkeitsfreigabe.

Nächste Phase erst nach erfolgreicher Veröffentlichungs-CI: TACTprepare unter
zentraler Lease, neue Seeds und konkrete Eingaben veröffentlichen, technische
32Vollmatches+Negativprobe bestehen und publizieren, CI, dann genau512Hauptmatches.
[Geplanter Folgeauftrag ATTR/MECH/TRAIN](../../experiments/NEXT-ATTR-MECH-TRAIN-round3.md)
ist ein separater Vorschlag ohne Ausführung oder Seedreservation.

# Runde3 – Match Engine Researcher

**Ergebnis: MECH-002 technisch blockiert; sichere Offlinevorarbeit geprüft.**
Eigener Codex-Subagent im getrennten Worktree/Branch `codex/round3-mech`.
[Vollständiger Gate-/Studienbericht](../../experiments/MECH-002-startpolicy-gates.md)
mit konkreten Quellen, [Entwurfsvertrag](../../data/mech-002/contract-draft.json)
und [Kodierungsprüfungen](../../data/mech-002/offline-report.json).

| Lieferpunkt | Eigener Beitrag / Grenze |
|---|---|
| Forschungsfrage | Gemeinsames Zwei-Schärfefelder-Startpaket×Pressing bei festem D00. Keine globale Mechanikrangliste. |
| Geprüfte externe Evidenz | Lokale Mac-Study5 am849b16f9: Bericht nennt bei75%−0,37Punkte/−0,49xGD; Setter ändert beide Felder. [Studie](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/05-everything-else.md), [Setter](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/port/validation/study5_everything.py#L31). Nicht unsere Replikation, kein Windows-/Karrierebeleg. |
| Forschungslücke / Erkenntnisgewinn | Windows-Eingriff wirksam und zeitlich korrekt beweisen; Start-only von Clamp unterscheiden; Verlust mit Pressinginteraktion messen. Mac-Wirkungsgrößen sind keine eigene Powerbasis. |
| Experiment / Stichprobe | Voller2×2-Pilot,32neueSeeds je zwei bekannten Gegnern,beideSeiten;512Matches/64Blöcke. Primär F auf xGD,Holm8 sekundär. Neue Kontrast-SD unbekannt. |
| Kosten / Zustand | Vorschlag32technischeVollmatches+3negativeProbes,900Child-/1800UTC-s. Tatsächlich0nativeStarts/0reservierteSeeds,alle547Plätzeunbegonnen. Kein nativer Budgetverbrauch. |
| Implementierung | Eigener strikt opt-in Offline-FM27CFG1-Recordcodec; sichere Read-only-CLI; keine Runtime-/NativeLab-/Registry-/Leaseänderung. |
| Reale Tests |7neue portableUnit-Tests;93Repositorytests und5historischeAnalysetests bestanden;vier echte archivierte D00-Binaries privat roundtrip/full-identisch;low jeSeite genau20 erlaubte Feld16/17-Diffs. Keine neue native Validierung. |
| Harte Blocker | Host schreibt vor statt nach Originalvorbereitung; passive Profile bei ersterFortschreibung fehlen; passive Original-Familiarity fehlt; eigener nativer Runner/Auditor fehlt. Nicht durch Boolflags oder synthetische Testdaten ersetzbar. |
| Nächste Schritte | Separater versionierter Host-/Receiptadapter mit eigener Abnahme. Erst danach zentrale neue Seeds,unverrückbareBudgets,publiziertePrereg/Analyse,CI/Review/Technik und512erPilot. |

DLL-/Host-/Fixtureidentitäten wurden neu rein lesend gehasht und stimmen mit
VALID-002 überein. Das beseitigt keinen neuen Eingabepfad-/Timingblocker.
Keine Ersatzsimulation, Holdoutöffnung, Karriereausführung oder nachträgliche
Effektivitätsneutralisierung. Historische Ergebnisse und öffentliche Archive
bleiben unverändert. Independent Review/Integrations-CI und Push liegen beim
Research Director; dieser Fachbranch liefert einen lokalen geprüften Commit.

# Agent VALID – Forschungsrunde2

14.11.2026. Exklusiver Branch `codex/valid003-round2`, eigener Worktree,
Ausgangscommit790727f. Hauptrepo/private Quellen ausschließlich lesend.
Alle wissenschaftlichen Vorarbeiten und der Independent Review wurden berücksichtigt.

Implementiert und geprüft:

- [validation003.py](../../research/validation003.py): eigene21Profilvektoren,
  korrekte native0..20-/1..100-Skalen, private Kapazitäts-/ID-Bindung,
  öffentliche Hash-Whitelist und Missing/Readback-Comparator.
- [coordination_testpath.py](../../research/coordination_testpath.py): separater
  Testpfad mit unveränderter NativeLease+DeadlineBudget und festen harmlosen
  Pythonchildren. Keine FM-Hostkommandos/Registry-/Live-Lease-Verwendung.
- [Offline-CLI](../../analysis/run_valid003_offline.py):2tatsächlich ausgeführte
  Python-Probes und21eigene Vektoren,0nativeStarts/0Seedreservierungen.
- [8Profiltests](../../tests/test_validation003.py) und
  [5Koordinationstests](../../tests/test_coordination_testpath.py): echte
  Konkurrenz, Crashretention, Timeout/Fehler, Cap-/Retry-/Workergrenzen;
  keine hypothetischen Testresultate. Vollständige lokale Suite:65/65 Tests bestanden.

Der [ausführliche Vorbereitungbericht](../../experiments/VALID-003-preparation.md)
benennt Quellhashes, den rein lesend verifizierten historischen Bundled-Dump,
Profilskalierung, Scope und verbleibende Gates. Kapazitäten26/18 werden nur als
synthetische Testfälle benutzt; historisch beobachtet23/23 aus bestehendem
P1C-Dump. Opaque PKM-Bytes liefern bewusst keine erfundene Kapazität.

Kein neuer nativer Profil-/Stärke-/Karriereaudit bestanden. Keine Karriere-
Replayfreigabe. ATTR braucht noch native Masken-/Effektivitätsaudits, MECH einen
opt-in Startpolicy-Schreibpfad, TRAIN unabhängige Karriere-RNG-/Teilnahmebelege.
TACT bleibt der einzige später zentral gestartete native Forschungsauftrag.

Ein korrigierter erster Offlineentwurf setzte die Rohfähigkeitsskala irrtümlich
auf20. Der reale alte Dumpvergleich und die Quellprüfung klärten100; öffentlicher
Regressionstest schützt nun die Grenze. Keine nativen Fehlmatches oder Daten-
ersatzmaßnahmen. Keine Upstream- oder historische Forschungsdatei verändert.

Nur eigener lokaler Commit; Push/CI/Integration erfolgen durch den Director.

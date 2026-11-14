# Separater Schärfepilot: Implementierungsplan

Stand2026-11-14, ausschließlich Offlinevorbereitung. Keine neuen nativen Matches,
Seeds oder Registryänderungen. TECH17 bleibt eine notwendige tatsächliche,
unabhängig veröffentlichte Vorfreigabe; dieser Entwurf erteilt keine Freigabe.

## Neue, abgegrenzte Dateien

`analysis/sharpness002_design.py` enthält die reine4×2×2-Eingabefactory,
CORE-kompatiblen Vertrag, exakte Faktoren/Kontraste, Budget- und TECH17-Gates sowie
den33er-Technikplan mit vier separaten Seeds. Der bestehende originale Codec wird
unverändert importiert. Keine Änderung an `research/`, Setter oder C++-Host.

Die Factory nimmt historische D00- und originale R01-Recordbytes entgegen,
restauriert ausschließlich zehn Staminawerte40→60 im R01-Carrier und verlangt danach
genau eine Pressingrecord-Differenz. Low verändert genau20 Profilfeldwerte16/17;
High/Standard ist bytegleich mit D00. Der Guard verlangt exakt46 aktive kodierte
Stamina52-Records,23 je Seite, alle raw60. Zusätzliche unkodierte Trägerslots sind
kein Bestandteil dieser Attributrecordliste; für sie wird kein kodierter Wert
behauptet. GK, Bank, Gegner und weitere Trägerslots bleiben unangetastet.
Das ist ein Offline-Intentionsbeweis, keine native Abnahme.

`analysis/analyse_sharpness002.py` liest ausschließlich vollständige registrierte
Seedblöcke, die vereinbarten nativen Auditmarker und Originalresultate. Welch95,
stratifizierter20.000er-Bootstrap, exaktHolm7, Kontext/Seite/LOO und bedingte neue
Powerplanung sind deterministisch. Die15 Cache-/Rawgrößen werden rein deskriptiv
mit expliziten Fehlgründen behandelt. Private Rawregionen und Spieler-IDs werden
nicht benötigt.

Die Hauptanalyse blockiert Drafts, fehlende unabhängige TECH17-Releasebelege,
abweichende Host-/Input-/Seedidentitäten und unvollständige Hauptserien. Die
zusätzliche Prüfung tatsächlich gültiger Ressourcen-/Review-/Publikationsgates
bleibt verpflichtende Aufgabe des getrennten Supervisors/Verifiers vor Export.

## Vereinbarte Schnittstelle zum parallelen Runnerautor

Eigene Factoryexports: `EXPERIMENT`, `ARMS`, `CONTEXTS`, `OBSERVER_HOST`, `matrix()`,
`treatment(arm)`, `build_inputs(d00_bytes, original_r01_bytes, tested_side)`,
`contract_definition(identity=None, setups=None)`, `validate_design(c, executable)`,
`technical_jobs(four_new_seeds)`. Letzteres reserviert selbst nichts.

Registrierungsreceipt: `{config, config_sha256, seeds}` mit64 zentral reservierten
Mainseeds; CORE-`schedule()` erzeugt512 eingefrorene Matchkeys.
Kanonische Messrow:

```text
job_id, context, team_side, seed, arm, status, config_sha256, setup_sha256,
identity, observer_host_sha256,
result = {score, team_statistics, tick, clock},
native_audit = {input_verified, seed_verified, sharpness_start_verified,
  stamina60_verified, pressing_verified, controls_verified,
  attribute_values_verified:3174, profile_fields_verified:1058,
  phase_cells_verified:44, pi_groups_verified:748, sharpness_raw, pressing_bit},
descriptive = {die15 vorregistrierten Felder}, descriptive_missing_reasons = {}
```

`analyse(data, receipt)` liefert Ergebnisobjekt und512 Kontrast-Blockzeilen
(acht Kontrast/Endpunktkombinationen×64 Seeds), ohne einen nativen Prozess zu
starten oder Daten/Registries zu schreiben. `controls_verified` schließt initiale
Nichtschärfefelder und den RawTF33-Abgleich mit eingefrorenem D00 ein; nur Rohregion,
keine validierte Tactical-Familiarity-/UI-/Consumerinterpretation.

Runnercode, Inputmanifest und Seedplan werden mit Hashes in `execution` eingefroren.
Das nach Prepare verfasste Inputreview bindet separat an Inputs/Manifest, ohne
Selfhashzyklus. Vor Main zusätzliche unabhängige technische Reviewdatei und
publizierter Release mit erfolgreicher exakter CI. Der tatsächliche Runner liegt
im getrennten Arbeitsbereich des Runnerautors; dieser Fachagent verändert ihn nicht.

## Weitere Freigabeschritte

1. TECH17 aus echten nativen Belegen/abgeglichenem Parentbudget unabhängig abnehmen.
2. Liveidentitäten und Quellen prüfen, neue68 Seeds unter zentralem Lock reservieren;
   vier TECH17- und64 terminale Staminaseeds plus sämtliche übrigen Reservierungen
   ausschließen. Inputs/Vertrag/Prereg/Code/Inputreview veröffentlichen und CI abwarten.
3. Eigene32 Technikmatches plus Negativkontrolle kalt und zentral ausführen,
   native Start-/Erstschritt-/Inputgates vollständig prüfen. Kein Warmworker.
4. Technik parentseitig abrechnen, unabhängig reviewen, publizieren und CI bestehen.
5. Nur mit allen Gates und jeweils≥600s eigener/globaler Child- und UTC-Allowance
   die512er-Mainserie zulassen. Eigener3600s-Clockstart erst beim ersten nativen
   Technikaufruf, danach zählen auch CI-/Verwaltungspausen. NIGHT23UTC bleibt hart.
6. Vollständige Serie unabhängig rekonstruieren; bei jedem Fehler ausschließlich
   technischen Status veröffentlichen. Keine automatische Folgestudie.

## Offline-Tests

Eigene synthetische5557-Record- und mathematische512-Row-Fixtures prüfen ausschließlich
Softwareverhalten. Sie sind keine FM-Messergebnisse. Kontraste liefern bekannte
eingesetzte Testeffekte und reproduzierbare Intervalle; falsche Nativebelege,
unvollständige Blöcke, stille Fehlstellen, Budget-/Armdrift und fehlende TECH17-
Abnahme werden abgewiesen. Reale Übertragung7000/10000 in die Engine wird ausschließlich
im getrennten TECH17-/Studientechnikpfad geprüft, nicht aus diesen Tests gefolgert.

Lokal bestanden:12 eigene Tests innerhalb314 Repositorytests (zwei private
Goldprüfungen ohne Dateien im Worktree übersprungen), zusätzlich fünf historische
Analysetests.340 NIGHT- und272 Round3-Archivdateien unverändert. Dieser Fachagent
startete0 native Matches und reservierte0 Seeds; keine Registry-/Altdateiänderungen.

## Korrektur der aktiven Recordinventur

Der erste Entwurf verwechselte die Anzahl von Trägerarray-Slots mit tatsächlich
kodierten aktiven Attributrecords. Die vier echten D00/R01-Zellen enthalten exakt46
Stamina52-Records,23 je Seite; der falsche49er-Guard wurde strikt ersetzt, ohne
Fallback. Fehlende, duplizierte oder zusätzlich kodierte Trägerslots werden abgewiesen.

Ein optionaler rein lesender Goldtest prüft die privaten vier D00/R01-Paare gegen
ihre veröffentlichten Setup-SHA256 aus `data/tact-001-p1b/inputs.json` und
`data/mech-003-stamina/inputs.json`. Der lokale Nachlauf bestand für alle vier
Zellen: insgesamt16 kompilierte Inputs,46 aktive Staminawerte60 pro Input,
Armdifferenzen `[20,0,21,1]` in festgelegter Reihenfolge. Keine Aussage wird über
Staminawerte außerhalb der kodierten aktiven Spielerliste getroffen.
Die Prüfung liest ausschließlich bestehende eigene Research-Binaries und startet
keine Simulation. Ohne expliziten `FM27_OFFLINE_GOLD_ROOT` wird nur diese optionale
private Goldprüfung übersprungen; die synthetischen Guard-/Kontrasttests bleiben aktiv.

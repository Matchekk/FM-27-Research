# Forschungsrunde2 – geprüfter Abschluss TACT, VALID und SET

14.11.2026. Drei tatsächliche Codex-Subagents arbeiteten parallel in eigenen
Branches/Worktrees; ein vierter unabhängiger Reviewer prüfte Implementierung,
konkrete Inputs,native Technik und Ergebnisse. Director integrierte,publizierte
und führte als einziger Supervisor die native Forschung aus.

**TACT-002-R0 vollständig:512 Hauptmatches,64 unabhängige Seedblöcke,
32 technische Vollmatches/16exakteA/A-Paare plus Exit108-Negativkontrolle.**
Keine nativen Ausfälle,Retries,Ersatzseeds,Exklusionen,Holdouts oder Karriereausführung.
Alle545Versuchsplätze erhalten. Keine Erweiterung auf1024 oder weitere Optimierung.

## Wissenschaftliches Ergebnis

Primär DLF−CF,gemittelt über AttackingMidfielder/SecondStriker und beide
Discoverygegner: **-0.018 xGD**,95-%-KI
**[-0.160;+0.124]**,p=0.80072.
Volle Breite0.283 unter Pilotziel0,50. Weder primär noch
in der vorab eingefrorenen Holm7-Sekundärfamilie Nachweis; alle7Holm-p=1.
ST-Punkteffekt−0,098,95-%-KI[−0,283;+0,088]. Kein Rollensieger ausgewählt.

Das schränkt große durchschnittliche ST-Vorteile im getesteten Kontext ein,
beweist aber keine allgemeine Wirkungslosigkeit oder formal getestete Äquivalenz.
Interaktion(ST×AMC)−0,211xGD,95-%-KI[−0,544;+0,122],weiterhin unklar.
Synthetische omnipotente Profile,feste Managementpolitik und zwei bekannte
Gegner begrenzen Übertragung. Native Readbacks belegen die deklarierte Eingabe;
ein vollständiger passiver Audit aller abgeleiteten Rollen-/Effektivitätsgrößen
ist noch kein separat validierter Endpunkt. Keine Karriere-/Meta-/Optimalitätsbehauptung.

[Rollenbericht und alle8Kontraste](../../experiments/TACT-002-R0-results.md) ·
[Rohmessungen/Provenienz](../../data/tact-002-r0/README.md) ·
[technische Freigabe](../../experiments/TACT-002-R0-validation.md).

## Getrennte Arbeitsbereiche und reale Beiträge

| Agent / Branch | Ergebnis |
|---|---|
| [TACT](TACT.md),codex/tact002-r0 | Eigener kleiner voller2×2-Runner,exakterD00-Kontrollhash,44Rollen-/44PI-Zellen/748PI-Gruppen je Match,konkreter Vertrag,eingefroreneAnalyse,67neueSeeds und dauerhafteBudgets. |
| [VALID](VALID.md),codex/valid003-round2 |21eigene Profilvektoren,korrekte0..20-/1..100-Skalen,kapazitätserhaltende privateBindung,Missing-/Readback-Comparator,separater Lease+Budget-Python-Testpfad. |
| [SET](SET.md),codex/set-v0 | Strikter synthetic-only Ereignisparser,elfGoldfälle,Execution-/Clock-/Schuss-/VAR-/Besitz-/Konterlogik. Native Mapping weiterhin hart blockiert. |
| [Review](REVIEW.md),codex/round2-review | Unabhängige Implementierungs-/Input-/Technik- und Ergebnisprüfung,keine eigene nativeAusführung oder Registrywrites. |
| Director,main | Exklusive Integration,Veröffentlichung/CI,gemeinsameRegistry und einziger nativerSupervisor;193alteArchivdateien geschützt. |

Die Branches/Worktrees bleiben erhalten. Wissenschaftliche Quellen/Archive
wurden nicht überschrieben. Source-/Zeitbelege und tatsächliche Agentenfolge
werden im Abschlussledger `QUEUE.json` gebunden.

## Technische und unabhängige Abnahme

86Repositorytests und5historische Analysetests bestanden. Vorbereitungsreview
prüfte vier echte frühere D00-Dumps ohneServerimport. Zwei echte Codebefunde
wurden vor Registrierung korrigiert: SETs fehlender Repeat-Vorgänger und TACTs
überschreibbarer Retry-Leasebeleg. Entsprechende Regressionen bestehen.
VALID korrigierte vorab seinen ersten Offline-Skalierungsentwurf auf Abilityrohwerte
bis100. Keine dieser Entwicklungsprüfungen startete ein natives Match.

Vorregistrierung/Code/Inputs/67Seeds vor Vollmatches in1667463 publiziert,
CI43611014780 vor Technik erfolgreich. Native Techgate7188687,
CI43611426911 vor Hauptstart erfolgreich; Input-Review9b07d7b,
[unabhängiger echter Technikreview](TECH-REVIEW.md)4540c28.
Reviewer kontrollierte alle32Logs/Dumps und23936PI-Gruppen direkt.
Separater unabhängiger Rechenkern rekonstruiert8Kontraste/t-/Bootstrapintervalle,
Holm7,192Blockwerte,Power-Minima und545Jobs ohneProjektanalyseimporte.

Ein administrativer Registeraufruf mit verkürzterSHA wurde vor jedemSchreiben
abgewiesen; derselbe veröffentlichteCommit anschließend mit vollerSHA registriert.
Keine Seed-/Budgetmutation oder native Wiederholung. Der Befund bleibt dokumentiert.

NativeLease ist in **diesem neuen TACT-Runner** um jede gesamte beaufsichtigte
Phase integriert,Child prüft Supervisor-/Leaseidentität. Historische Runner sind
unverändert und werden dadurch nicht nachträglich global gesperrt. Operative
Zentralisierung und≤4Worker wurden eingehalten. KumulierteChild-Zeit
**295.737/900s**,Studienfenster**851.954/1800s**.
Nach Abschluss keine aktive Lease/Nativeoperation. Private Rohartefakte≈234MiB,
unter2GiB; Spielmaterial bleibt privat.

## Was jetzt verfügbar ist und was gesperrt bleibt

VALIDs eigener [zentraler Offline-Smoke](../../data/valid-003-preparation/offline-report.json)
erzeugte21Vektoren und zwei harmlose Python-Probes,0nativeStarts/0Seeds.
Synthetische Kapazitäten26/18 werden ohne Kürzen erhalten; bestehender Bundled-
Dump zeigt23/23. Opake Karriere-PKM werden nur gehasht,keinDecoder/keine
behauptete tatsächlicheKapazität. **Keine native Profil-/Stärke-/Replayfreigabe.**

SET-V0 liefert für eigene synthetische Traces geprüfte Zähler/Attribution.
Echte Selektionslogs bleiben `unresolved_native_mapping`,Exposition/Attribution
`null`,native/performanceFlagsfalse. Ein Callerflag kann dies nicht freischalten.
Tatsächliche native Ausführung,Schuss-xG/Besitzketten/Clockmapping und positive
Goldfälle brauchen eigenen versionierten Adapter und Abnahme. Keine Wirksamkeitsstudie.

## Nächster priorisierter Auftrag

[Konkreter Folgeauftrag ATTR→MECH→TRAIN](../../experiments/NEXT-ATTR-MECH-TRAIN-round3.md):
ATTR-Masken-/Rohskalenaudit,dann vorab gewählte384-Match-Brücke; MECH eigener
Startpolicy-Encoder/Auditor vor512Schärfe×Pressing-Matches; TRAIN zuerst Reader,
unabhängige Karriere-RNG und tatsächlicheTeilnahme vor irgendeinem Kalenderadvance.
Die Zahlen sind getrennte zukünftige Vorschläge,keine gestarteten Studien.
Rollen-SDs werden nicht als gemessene ATTR-/MECH-/Karrierevarianzen übernommen.

Nach dieser Runde gestoppt: keine Holdoutserie,D15-Optimierung,weitere Rolle-
Suche oder Karrierefortschreibung.

[Unabhängiger Ergebnis-/Gesamtreview](RESULTS-REVIEW.md) · [Agenten-/Commit-/Statusledger](QUEUE.json).

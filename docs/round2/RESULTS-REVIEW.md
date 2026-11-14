# Runde2 – unabhängiger Ergebnis- und Veröffentlichungsreview

**14.11.2026: TACT-002-R0 und die geprüften Runde2-Module zur kontextgebundenen
Veröffentlichung freigegeben, vorbehaltlich finaler Integrations-CI. Keine
Freigabe einer weiteren Studie oder allgemeinen Karrierewirkung.**

## Umfang und Unabhängigkeit

Eigener Codex-Subagent mit Review-Worktree. Der separate
`analysis/review_tact002.py` wurde tatsächlich auf alle512 öffentlichen Hauptzeilen
ausgeführt. Kein Import des Projektanalysers/Verifiers/Runners oder
`research.stats` in diesem Rechenkern. Eigene direkte vierarmige Differenzbildung,
SciPy-t und vollständige stratifizierte Bootstrapindexmatrizen; zukünftige
Fallzahlminima mit linearer Ganzzahlsuche statt binärer Autorensuche.
Keine native Ausführung, Seed-/Registryänderung oder Holdout-/Karrierenutzung.

[Preflight](REVIEW.md), [konkrete Inputs](INPUT-REVIEW.md) und
[technische Abnahme](TECH-REVIEW.md) bleiben als frühere Belege erhalten.
Die technische Prüfung las alle32 Original-Logs/Dumps und prüfte1408 tatsächliche
Rollen-/PI-Zellen sowie23936 PI-Gruppen direkt. Dieser Abschluss ergänzt die
vollständigen Hauptdaten; ein Codeaudit hatte keine nativen Gates vorweggenommen.

## Aus Rohzeilen rekonstruierte Ergebnisse

512 eindeutige erwartete Matches,32 neue Seeds je festem Gegner,64 vollständige
unabhängige Seedblöcke. Alle vier Arme und beide Seiten innerhalb eines Seeds
gebunden; erst Seitenmittel, dann beide Gegnergewichte je1/2. Die512 Matches sind
keine512 unabhängigen Replikate. Rollenflags, Identitäten, Setup-/Confighashes,
Scores, Readbackzählungen und natürliche Endticks aller Zeilen geprüft.

| Kontrast:Endpunkt | Effekt | Marginales95-%-t-KI | Roh-p | Holm7-p |
|---|---:|---|---:|---:|
| ST:xGD | -0,017944188 | [-0,160; +0,124] |0,800716023| — |
| AMC:xGD | +0,048631403 | [-0,090; +0,187] |0,484200249|1|
| STxAMC:xGD | -0,210766009 | [-0,544; +0,122] |0,210050994|1|
| ST:Punkte | -0,097656250 | [-0,283; +0,088] |0,295934836|1|
| ST:GF | -0,074218750 | [-0,266; +0,118] |0,441713020|1|
| ST:GA | +0,019531250 | [-0,171; +0,211] |0,838684411|1|
| ST:xGF | -0,042442833 | [-0,153; +0,068] |0,444716104|1|
| ST:xGA | -0,024498645 | [-0,135; +0,086] |0,659573212|1|

Alle acht Effekt-/SE-/t-/Bootstrapwerte stimmen numerisch mit dem Archiv überein;
alle sieben sekundären Holmwerte sind1. Der ST-Schätzer istDLFminusCF, gemittelt
über beide AMC-Rollen. Die DoD ist physische(+1,-1,-1,+1), kein um Faktor2/4
verwechselter Regressionskoeffizient. Punkte3/1/0 aus tatsächlichen Scores.

Die volle Primärintervallbreite0,283 erfüllt das Pilotziel0,50. Das Intervall
umfasst null; weder Äquivalenz noch Wirkungslosigkeit aller Rollen folgt daraus.
Ein positiver Mindestgewinn0,30 ist nicht nachgewiesen. Deskriptive Armmittel
begründen keine Kandidaten-/Siegerwahl. Alle192 xGD-Seedkontrastzeilen direkt
abgeglichen;20000 vollständige Bootstrapblöcke getrennt je Gegner reproduziert.
Marginale Intervalle sind keine gemeinsame95-%-Absicherung beider Testfamilien.

## Bedingte zukünftige Powerplanung

| SD-Annahme | Fester Effekt gegen0 | Neue Seeds/Gegner | Neue2x2-Matches |
|---|---:|---:|---:|
| beobachtet |0,20|44|704|
| beobachtet |0,30|20|320|
| gemeinsame95-%-Normalmodell-Obergrenzen |0,20|76|1216|
| gemeinsame95-%-Normalmodell-Obergrenzen |0,30|35|560|

Alle vier Minima durch unabhängige lineare Suche bestätigt; Kosten16n und
unabhängige Blöcke2n korrekt. Obere SDs verwenden je97,5-%-einseitige
Chi-Quadrat-Grenzen mit31df. Nichtzentrale Welch-t-Näherung bei gleicher
Kontextstreuung, keine beobachtete Power aus dem kleinen Effektschätzer und
keine Transfergarantie. Keine Wiederverwendung dieser Daten oder automatische
Fallzahlverlängerung aus der Tabelle.

## Provenienz, private Hashbelege und Archiv

67 reservierte gültige uint32Seeds inklusive3 Technikseeds,64 Mainseeds disjunkt
zum gehashtenExcludedSet sowie unabhängig gescannten früheren öffentlichen und
Registryreservierungen. Jede Hauptzeile verwendet genau ihren zugewiesenen Seed.
Keine Ersatzseeds, Exklusionen oder stillen Nullen.

Alle14 eingefrorenen Quellen und6 Input-/Seedartefakte stimmen sowohl mit ihren
registrierten SHA256 als auch den tatsächlich gelesenen Gitblobs des Commits
1667463286cdcb4c8d139d6d71c496799281882e überein. Die192 TACT-Archivdateien
stimmen mit aktuellen Dateien und ursprünglichen790727f-Gitblobs überein.
Zusätzlich alle193 Dateien des Director-Baselinesnapshots unverändert; dieser
enthält auch das frühere externe Quellenregister.

Alle512 privaten Haupt-Rohlogs und512 Inputdumps wurden erneut gehasht und gegen
die öffentlichen SHA256 geprüft. Material/Spieleridentitäten bleiben privat.
R00 ist in allen vier Gegner-/Seitenzellen hashidentischP1B-D00. Neue native
Rollenarme wurden im technischen Gate tatsächlich geprüft; Hauptzeilen tragen
44/44/748-Zählungen und1058 Profilreadbacks. Kein Karriere-/SET-/neues Profilgate
wird daraus abgeleitet.

## Abrechnung, Leases und Publikationschronologie

545 eindeutige Versuchsplätze:512 Main und32 Technikok, ein erwarteterExit108.
Alle16 A/A-Paare exakt; keine offenen/fehlgeschlagenen Ersatzjobs. Drei erfolgreiche
beaufsichtigte Phasen,295,7366557/900s Child-Zeit,851,954045/1800s Studienfenster.
UTC-Deadline2026-11-14T16:03:01.170046+00:00 unverändert.

Alle drei Leasebesitzer-PIDs stimmen mit den privaten Supervisorbudgetbelegen
überein; Erwerbszeit vor Start, Workerdeklaration4. Keine verbleibende Crashlease.
Die Integration gilt für diesen neuen TACT-Pfad; historische Runner sind dadurch
nicht automatisch global integriert.

GitHub-Status/HeadSHAs/Zeitpunkte selbst perCLI/API geprüft, expliziteUTC:

| Beleg | Erfolgreich abgeschlossen | Folgender nativer Start |
|---|---|---|
| [1667463/CI43611014780](https://github.com/Matchekk/FM-27-Research/actions/runs/43611014780) |15:36:49UTC|Technik15:37:58,977UTC|
| [7188687/CI43611426911](https://github.com/Matchekk/FM-27-Research/actions/runs/43611426911) |15:41:40UTC|Main15:42:47,316UTC|

Publikation und erfolgreicheCI liegen jeweils vor der abhängigen Serie.
Die administrative kurze-SHA-Zurückweisung geschah vor Schreibmutation;
voller identischerSHA wurde anschließend registriert. Das Budget enthält keine
native Wiederholung oder neue Seedvergabe. Kein Gatefehler wurde still umgangen.

## Runde2-Module und Round3-Auftrag

Die frühere Code-/Offlinefreigabe bleibt gültig:21 eigene Rohprofilvektoren und
kapazitätserhaltende Interfaces sind keine native Profil-/Stärke-/Replayfreigabe.
Opake PKM-Kapazität bleibtNone. SETs elf Goldfälle ausschließlich synthetisch;
reale Logs bleibenunresolved/null und Freigabeflagsfalse. Beide unabhängig
gefundenen Parser-/Leaseprovenienzlücken sind vor Vorbereitung korrigiert.

Der [Round3-Auftrag](../../experiments/NEXT-ATTR-MECH-TRAIN-round3.md) wurde
vollständig als getrenntes, noch nicht gestartetes Vorhaben geprüft:

1. ATTR:384=2Masken x3Attributarme x2Seiten x32Kontextseeds;32 unabhängige
   Blöcke. PrimärJR-(Acc+Pace)/2-Differenz zwischenMasken, Baseline algebraisch
   entfallen, deshalbHolm5 statt11. Technik24Zellen+8A/A=32Vollmatches+1negative.
   25% weniger Hauptjobs durch andere Nebenfragen, kein gemessener Varianzgewinn.
   AktiveFamilien/GK,69Rohwerte0..20/1..100, Effektivität und ausgeschlossene
   Uniform-/Executionnormalisierung bleiben vorab zu auditieren. Neuheit nur
   gegenüber geprüften Spezifikationen, keine weltweite Garantie.
2. MECH:512Matches/64Blöcke, Zweifelderstartschärfe xPressing,Holm8,
   32Technik+3Negativprobes konsistent. Erst opt-in Encoder/Runner/Auditor,
   Default binärgleich, Nach-Vorbereitungs-/Startbelege beiderFelder; kein
   Clamp, keine ungeprüfte70%-Anzeige und kein Understanding-Scheinsetter.
3. TRAIN:Reader/Einheiten/RNG/Teilnahmeherkunft vor jedemAdvance; gleicheRNG-
   Klone und22Spieler keine Replikate. AchtArmwochen/30min nur nach passender
   separater Abnahme; kein PKM-Replay-/Kalenderadvance aus Readererfolg und
   keine automatische32Arm-Hauptserie. Verletzungen/Minuten nicht nachträglich
   als mögliche Mediatoren wegmatchen.

Reihenfolge und Opportunitätskosten sind nachvollziehbar. Kein neuer Auftrag
reserviert hier Seeds oder startet automatisch eine Match-/Karriereserie.

## Veröffentlichungsentscheidung

Keine verbleibende fachliche Blockade gegen Veröffentlichung tatsächlicher
R0-Messungen mit negativen/unklaren primären Schlüssen und ausdrücklich
begrenzter Runde2-Vorarbeit gefunden. Director prüft final Diff/Dateigrößen/
Geheimnisse/CI und pusht. Danach stoppen; keine1024-Erweiterung, Holdouts oder
Optimierungsrunde. Dies ist keine neue native Re-Ausführung oder externe
Replikation des Labors.

## Snapshot der final gelesenen Artefakte

SHA256 nach LF-Normalisierung:

| Datei | SHA256 |
|---|---|
| data/tact-002-r0/main.jsonl | `6ffe70e2a051b2b450ef77c3fc444ac3d1dae0acaf500a866676d37d757f6e2a` |
| data/tact-002-r0/manifest.json | `15d9ef6f57e08b16dd33d8fc4bea09789487b6ce3ca1d0aee91e585f44b60e17` |
| data/tact-002-r0/effects.json | `e5a258ee17a5df1bd2d49f466285cbb10cbaa8d64270961b9a54dc73d56b7cf2` |
| data/tact-002-r0/block-contrasts.jsonl | `bbdf91ee717aebd38281d2cd00d88054a30dda9a35986afdb0475957b2dada68` |
| data/tact-002-r0/job-accounting.jsonl | `c8015d7e4f256e378294a3053988a4102b8c57690d305a833e0c6aff6cf9866d` |
| data/tact-002-r0/budget.json | `19ba7902542c10dc801c2e3814402dba7198877eba8445f9e96e50e5ee14c594` |
| data/tact-002-r0/run-summary.json | `dd77bd029d4e14af58fa22fd0f7d163025b596154ea17b4bc89548e21b998b1f` |
| experiments/NEXT-ATTR-MECH-TRAIN-round3.md | `fc7aab3a1b90d9951e375c937aad48fefe4b5fcce6c0464f38b6407da40010f4` |

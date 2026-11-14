# Runde 3 – unabhängiger Ergebnisreview

14.11.2026. **ATTR-009 vollständig und unabhängig nachgerechnet. Die tatsächlichen
Ergebnisse samt finalen Directorübersichten sind mit den unten genannten Grenzen
veröffentlichbar, vorbehaltlich erfolgreicher Integrations-CI.** Keine Freigabe zusätzlicher
Studien, Seeds, Holdouts oder Karriereausführung. MECH und TRAIN bleiben gesperrt.

## Umfang und Unabhängigkeit

Separater Reviewer nach drei Facharbeiten, eigener Worktree und eigene
Commits. Der Rechenkern `analysis/review_round3.py` wurde tatsächlich auf alle384
öffentlichen Hauptzeilen ausgeführt: direkte Scores/xG, sechsarmiger Kontrast,
eigene Seed-/Seiten-/Kontextbildung, Welch95,20000 vollständige stratifizierte
Bootstrapindexmatrizen, Holm5 und zukünftige Fallzahlminima durch lineare
Ganzzahlsuche. Kein Import des Projektanalysers, Verifiers, Runners oder
`research.stats` für diese Rechnung. `published_effects_verified=true`.

Zusätzlich sämtliche384 privaten Original-Logs/Dumps direkt geprüft, nicht nur
öffentliche Erfolgsflags. Die eigenen Prüfer starteten keine nativen Prozesse,
veränderten keine Registry, öffneten keine Saves und nutzten keine Holdouts.
Unabhängige Nachprüfung derselben Ausführung ist keine externe Replikation.

## Aus Rohzeilen rekonstruierte Ergebnisse

384 eindeutige erwartete Matches;32 vollständige unabhängige Seedblöcke,
16je bekanntem Kontext. JeBlock alle sechs Arme und beide Seiten. Zuerst
Seitenmittel innerhalb des Seeds, danach Kontextgewichte je½. Keine384
unabhängigen Beobachtungen und keine selektiven Exklusionen.

Physischer Kontrast: `[J−(A+P)/2]S−[J−(A+P)/2]O`, Armgewichte
`(-1,+½,+½,+1,−½,−½)`. Keine Baselineeffekte oder isolierten Attributsieger.

| Endpunkt | Effekt | marginales95-%-Welch-KI | Roh-p | Holm5-p |
|---|---:|---|---:|---:|
| xGD, primär |−0,162009616|[−0,488421;+0,164401]|0,318851457|—|
| Punkte |−0,132812500|[−0,786684;+0,521059]|0,679444375|1|
| GF |−0,328125000|[−0,907895;+0,251645]|0,256718644|1|
| GA |−0,156250000|[−0,619997;+0,307497]|0,495430335|1|
| xGF |−0,226436273|[−0,459456;+0,006583]|0,056403230|0,282016149|
| xGA |−0,064426657|[−0,265006;+0,136152]|0,516387617|1|

Alle sechs Mittelwerte/SE/df/t-Intervalle/p-Werte und20000erBootstrapintervalle,
fünf Holmwerte sowie alle192 Seed×Endpunkt-Kontrastwerte stimmen numerisch mit
der Veröffentlichung überein. Primärer SE0,159826013;df29,994252.
Primärer Bootstrap95-%-Bereich[−0,465728;+0,142482].

**Kein primärer oder Holm5-korrigierter Nachweis.** Primäre volle Intervallbreite
**0,652821776** überschreitet das Pilotziel0,50. Der Punktschätzer ist negativ;
Richtung/Größe bleiben unsicher. Keine Äquivalenz oder allgemeine Wirkungslosigkeit
bewiesen. xGFs unadjustiertes marginales Bootstrapintervall[−0,441033;−0,008345]
liegt zwar unter0, begründet aber keinen familienkorrigierten Nachweis; vorab
festgelegter Welch-/Holmtest bleibt ohne Ablehnung. Keine nachträgliche Auswahl
des günstigeren Intervalls als Erfolgsregel.

Kontextmittel des primären Kontrasts: high_press−0,311250871,
deep_block−0,012768361. Kontrast-SDs nach Seitenmittel0,910348816 bzw0,897832795.
Dies sind erstmals gemessene Varianzen dieser engeren Interaktionsfrage,
keine übernommenen Rollen-/Instruktionsvarianzen und keine Bestätigung neuer Meta.

Alle deskriptiven Armmittel sowie Seiten-SDs/Kovarianzen und marginale95-%-
SD-Obergrenzen wurden ebenfalls unabhängig aus den384Rohzeilen geprüft.
Primärer Leave-one-seed-out-Bereich[−0,226771312;−0,091660559], größte Änderung
0,070349057; stimmt mit dem Archiv überein. Kein Seed ausgeschlossen.

## Bedingte Zukunftsplanung, keine neue Ausführung

| SD-Annahme | Effekt gegen0 | neue Seeds/Gegner | unabhängige Blöcke | sechsarmige Matches |
|---|---:|---:|---:|---:|
| beobachtete Kontext-SDs |0,20|109|218|2616|
| beobachtete Kontext-SDs |0,30|49|98|1176|
| simultane95-%-SD-Obergrenzen |0,20|259|518|6216|
| simultane95-%-SD-Obergrenzen |0,30|116|232|2784|

Alle vier90-%-Minima, zugehörigen Power-/Breitenwerte und Kosten24n unabhängig
mit linearer ganzzahliger Suche bestätigt. SD-Obergrenzen verwenden je97,5-%-
einseitige Normalmodell-/Chi-Quadrat-Grenzen mit15df. Nichtzentrale Welch-
Näherung ist eine bedingte Planung, kein Effektbeweis oder automatische Folgeserie.
Eine bloße Vergrößerung derselben Serie ersetzt keine neue
Messfähigkeit, realistischeren Profile oder unabhängig gehaltene Bestätigung.

## Direkte Hauptlaufbelege und vollständige Abrechnung

Alle384Originalbelege: **1218816Attribute**, **406272Profilfelder** direkt aus
Prefix-/Tail-Dumpbytes decodiert, **16896Phasezellen** und **287232PI-Gruppen**.
Alle69 Attribute/23Profile pro46Spielern, tatsächliche MATCH_PLAYER-Phasenbindung,
Maskenfamilien und Rohdosis stimmen. Natürliche Scores/Endticks und originale
Teamstatistiken direkt verglichen. Alle384 privaten Ledgerzeilen stimmen in
jedem öffentlich exportierten Messfeld mit den öffentlichen Rohzeilen überein.

48tatsächliche Workerstartreceipts über12sequentielle32erBatches an alle384Jobs
gebunden; je8/8erfolgreich, erwartete Host-/DLLidentität. Keine Experimental-
Executionbelege. Technik mit32Logs/Dumps erneut geprüft: acht exakte A/A-Paare
und Exit108 ohne natürliches Ende bleiben gültig.

**417eindeutige Plätze vollständig:**384Hauptmatchesok,32Technikmatchesok,
1erwarteteNegativabweisung.0Ausfälle,0unresolved/unbegonnen,0Retries,
0Ersatzseeds,0Exklusionen,0Holdouts. Negative Probe ist kein Nullmatch.

## Freeze, Budget und Veröffentlichung

Alle13 eingefrorenen Autorencodehashes gegen aktuelle tatsächliche Dateien
**und** Gitblobs von Vorregistrierungfc1474 geprüft; sieben Eingabeartefakthashes
unverändert. Alle272 geschützten Archivdateien gegen tatsächliche Dateien und
historische Gitblobs erneut geprüft. Privates Registryreceipt entspricht dem
öffentlichen Manifest. Vorheriger eigenständiger Inputreview belegt die34
disjunkten zentralen Seeds gegen2418historische Ausschlusswerte.

Drei erfolgreiche dauerhafte Operationen (prepare/technical/main), Summe
**231,5575563/600s** Childzeit. Studienfenster **753,168374/1200s**;
unveränderte feste UTC-Frist17:00:36,422962. Drei ursprüngliche Leasebelege
passen zu Supervisor/Phase/4Workern und wurden jeweils vor Phasenbeginn erworben.
Öffentliche/private Budgetwerte stimmen. Kein aktiver NativeLease oder Child.

Technikbericht und unabhängiger Review wurden in
`06f1aeb22c88eb1188c35cae5a7cdb3b453c7740` veröffentlicht. Zugehörige
CI43617519052 tatsächlich perGitHub geprüft:completed/success,exakterheadSha,
Ende16:48:52UTC. Maschinenfreigabe
`e9ac9393a09565366ba249c35aa9142ff13dc507` veröffentlicht16:49:44UTC;
Mainstart **16:49:48,993504UTC**, nach der erfolgreichen technischen CI und
gebundenen Veröffentlichung. Technische Zusammenfassung im Releasegitblob
stimmt exakt mit tatsächlicher Datei; unabhängiger Reviewhash stimmt ebenfalls.
Vorregistrierungs-/Prepare-/Technikchronologie im früheren Technikreview.

Die CI43617730448 des späteren reinen Maschinen-Gateverweises e9ac939 endete
16:51:22UTC und damit nach Mainstart. Das ist nicht die vor Main verlangte
Technikrelease-CI: diese war am unveränderten06f1aeb bereits16:48:52 erfolgreich.
Der Gateverweis selbst war vor Main öffentlich; keine eingefrorene Autorenquelle
oder Eingabe wurde dadurch geändert. Keine nachträgliche CI als vorgängig behauptet.

## Zulässige Schlussfolgerung und Abschlussstatus

Der engere totale Masken×Roh60→80-Kontrast ist hier technisch wirksam umgesetzt,
aber wissenschaftlich unklar. Omnipotente synthetische Grundprofile, festes D00,
zwei bekannte Discoverygegner und kontrollierte Managementpolitik begrenzen
Übertragung. Kein direkter FM-Anzeige12→16-Nachweis, keine passive Mediation,
keine Karriere-, OP-, Ranglisten- oder optimaleTaktikbehauptung.

Fünf eigene Reviewer-Tests und `git diff --check` bestehen. Bei Erweiterung des
eigenen Belegprüfers wurde eine lokal beschattete Schleifenvariable korrigiert;
danach vollständiger384erBeleglauf und erneuter32erTechnikbeleglauf erfolgreich.
Keine eingefrorene Autorenfunktion oder Ausführungseingabe geändert.

Die finalen Directorartefakte wurden anschließend direkt gelesen: vollständiger
ATTR-Ergebnisbericht, Plotcode und tatsächlich dargestellte Grafik,
`docs/round3/README.md`, `PRIORITIES.md`, `QUEUE.json`, Root-README/FINDINGS/
NEXT_STEPS/RESEARCH_LOG, PLATFORM/ROADMAP und der Daten-README. Gemessene Zahlen,
Präzisionsfehlschlag, Nichtnachweise und Scopegrenzen sind konsistent. Grafik
trennt Einheiten und kennzeichnet marginale Intervalle. MECH/TRAIN bleiben
gesperrt; Prioritäten sind künftige technische Vorschläge, kein neuer Auftrag.
Der erste Shallowcheckout-CIfehler und seine Korrektur vor Vorbereitung sind
offengelegt. Alte Ergebnisse werden mit Versionsbezug erhalten.

**Finale fachliche Veröffentlichungsfreigabe für diesen gelesenen Stand**, nach
abschließenden Directorprüfungen/erfolgreicher Integrations-CI. Keine offene
wissenschaftliche oder Dokumentationsblockade. Danach stoppen; keine zusätzliche
native Serie aus den hier berechneten Planungszahlen ableiten.

## Geprüfter Rohdaten-/Analyse-Snapshot

SHA256 nach LF-Normalisierung zum Ergebnisreview:

| Datei | SHA256 |
|---|---|
| main.jsonl | `f309a507e41007849ab3ea223f8314411ca0d4026c68b5fa43832e64395bc0be` |
| manifest.json | `e0fad6a55c86da12704a772d78b2183e9adb8edc8d5a83568bbf3fe1e15e42f1` |
| effects.json | `b38d7275adeebf8821b94a6a769c2f4626e9521007f2f2cf12084a82fb2fcbbd` |
| block-contrasts.jsonl | `6c83fd6dc8d513e5c80cb7b651a0b42155583696589b6be1d66dcec0d50f8eb3` |
| job-accounting.jsonl | `1ce65fd23e67d5778d53f1485bc1cdfb36e967eb4ab08e13869b9acc5d8196b8` |
| budget.json | `a97ac0115b35bbd5791c3655f0edb032a79121115a1827924b910644c82f2883` |
| run-summary.json | `442eb03d5ca12ff485e595ce36005f26ab2e5c1b9c033c027827e4578b4f8361` |

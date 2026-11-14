# TACT-001-P1C – Vorregistrierung des unabhängigen Seedpiloten

14.11.2026, vor dem ersten technischen Vollmatch. D15 wird als **einziger**
Kandidat eingefroren; D09 bleibt der unveränderte archivierte P1B-Vorschlag.
Dies ist ein unabhängiger Seed-/Präzisionspilot in den **bisherigen synthetischen
Discoverykontexten**, keine Bestätigung allgemeiner Karriereübertragbarkeit.
Kein Holdout-, Karriere- oder weiterer Optimierungsauftrag.

## Frage und feste Eingaben

Verbessert das unveränderte D15-Paket gegenüber D00 tatsächliche Punkte/Match?
Ein zweiseitiger primärer Test, α=0,05, kleinste praktisch relevante Verbesserung
**+0,15 Punkte/Match** (5,7 Punkte auf 38 Matches als reine Einheitenumrechnung).
Gewünschte volle marginale 95-%-KI-Breite ≤0,30. Keine Äquivalenzprüfung.

D00: Standard in A/B/C/D/E. D15: häufiger pressen (Gruppe10, ID2000905329,
Bit66), höhere Linie (9,1329018200,57), höheres Tempo (21,1345339954,47),
kürzere Pässe (1,1146434657,3), Standardbreite (4,1951095402,0).
Dies ist ein direkter Paketvergleich; keine Haupteffekt-/Interaktionszerlegung.
Alle acht Setups müssen bytegleich zu P1B sein. Der eingefrorene JSON-Vertrag
und `inputs.json` benennen für beide Gegner/Seiten die vollständigen Hashes.
Eigene IP-4-2-3-1/OOP-4-4-1-1, Rollen/Duties/PI, sämtliche übrigen
Teamanweisungen, Mentalität, Standardroutinen, Profile und Matchmanagement
bleiben exakt P0/P1B. `rules=game`. Beide Mannschaften haben dieselben
synthetischen 23-Spielerprofile. Kein zusätzlicher Live-Coaching-Eingriff.
Die vollständigen eigenen, anonymen Phasen-/Profil-/Managementdeskriptoren
bleiben in `inputs.json` an die unveränderte P1B-Quelle gebunden.

Zwei bisherige Gegner `high_press` / `deep_block`, Zielgewicht je ½.
Seiten0/1 als feste native Fixtureplätze, je ½ innerhalb eines Seeds;
kein kausal isolierter Heimvorteil. Holdoutprofile `holdout_midblock` und
`holdout_direct_counter` und ihre Reservierungen bleiben unangetastet.

## Umfang, neue Seeds und Randomisierung

**64 neue unabhängige Seeds pro Gegner**, 128 vollständige Seedblöcke.
Jeder Seed: D00 und D15 auf beiden Seiten = vier Hauptmatches.
**512 Hauptmatches**, keine bisherigen oder reservierten Seeds, keine
Ersatzseeds, keine Wiederaufnahme mit neuen Seeds und keine Retries.
Technik separat: zwei neue technische Seeds (einer je Kontext), je acht
Matches (beide Arme/Seiten zweimal), insgesamt **16 Vollmatches** und acht
exakte A/A-Wiederholungsvergleiche. Ein dritter neuer technischer Seed bleibt
reserviert für die Negativkontrolle, die ungültige Binärprobe startet ohne
wirksamen Seed. Somit 131 reservierte Seeds und **17 technische Versuchsplätze**.
Alle früheren öffentlichen/private Studien und offenen Registryreservierungen
werden ausgeschlossen; die ausgeschlossene Wertemenge wird gehasht veröffentlicht.

Scheduler: kanonische SHA256-Jobreihenfolge aus `schedule`, danach
`random.Random(2026111404).shuffle`; Technik analog RNG2026111405.
Diese Analyse-/Scheduler-RNGs sind keine zusätzlichen FM-Matchseeds.
Feste Reihenfolge, Batches≤64, maximal vier Worker, keine Effekt-Zwischenanalysen.
Code, Eingaben, Analyse und Seedreservierung müssen vor Prüf-/Hauptmatches
auf origin/main publiziert sein; technische Freigabe vor dem Hauptlauf separat.

## Identität, native Gates und Ressourcen

FM27 Dateiversion27.0.1 / Produkt27.0.1+2503222, Tactics Labv1114.6,
Commit91f2eba57fac0b7fbd3dff616056907e3ce461be,
Adapterfm27_desktop_8c6971ce_adapter_v1. Engine/Host/Fixture/Ressourcen,
Katalog und sämtliche Runtime-Pythonquellen müssen VALID-002/P1B entsprechen.
Die realen SHA256 stehen in `inputs.json`; Drift stoppt vor Hauptmatches.
Keine Aktualisierung oder Veränderung fremder Projekte.

Jedes Hauptmatch benötigt vollständige native Nach-Vorbereitungsreadbacks:
Seed und Identität, alle kodierten Records, beide Phasen/Positionen,
Rollen/Duties/PI, alle69 Attribute, 1.058 Profilfelder, Mentalität und
sämtliche Instruktionsgruppen beider Teams. Creatorbits müssen dem
D00/D15-Vertrag entsprechen. Naturabschluss, Statsquelle und numerische
Plausibilität erforderlich: endliche nichtnegative xG, SOT≤shots,
completed_passes≤passes, Besitz0..1 und Summe1, ganzzahlige Tore≥0,
0<Endtick<47996. A/A verlangt exakt gleiche Scores/Endticks/Statistik;
ungültige Binäreingabe muss Exit108 und keinen Naturabschluss liefern.

Dauerhafte, vor nativer Vorbereitung initialisierte Zähler:
512 Hauptversuche, 17 technische Versuche, **900s kumulierte beaufsichtigte
Child-Wall-Time** einschließlich Vorbereitung/Probes/Audits; zusätzlich
**1.800s unverrückbares UTC-Studienzeitfenster** einschließlich Publikationspausen.
90s ohne Workerfortschritt, Prozessbaumabbruch, höchstens vier Worker,
2GiB private Artefakte, 20GiB freier Speicher. Kein Reset durch Retry/Neustart.
Vorbereitung, Technik und Hauptlauf reservieren im selben Budget.
Native Input-/Seed-/Identitätsfehler stoppen; alle begonnenen, fehlgeschlagenen
und unbegonnenen Jobs bleiben in der Abrechnung. Keine Ergebnisexklusion
und keine stillen Nullen. Unvollständige Blöcke: ausschließlich technischer Status.

## Eingefrorene Analyse und Entscheidung

Primär Punkte3/1/0 aus tatsächlichem Endstand. Pro Seite D15−D00,
dann Seitenmittel im Seed; anschließend beide Gegner je½.
SE²=¼(s_H²/64+s_D²/64); Welch-Satterthwaite-df, zweiseitiges95-%-t-KI/p.
Zusätzlich20.000 stratifizierte vollständige Seedblock-Bootstrapresamples,
RNG erste8 Bytes little-endian SHA256(`TACT-001-P1C/bootstrap-v1`).
Sekundär genau **xGD, GF, GA, xGF, xGA**, Holm über fünf Tests;
marginale95-%-Intervalle und Bootstrap, kein neuer Kandidatenvergleich.
Native Schüsse/SOT/Besitz bleiben deskriptive Plausibilitätsgrößen.
Kontrast-SDs je Kontext, gepoolte innerhalb-Kontext-SD, Seitenmittel/-SD/
Kovarianzen, tatsächliche Armmittel und Leave-one-seed-out ohne Ausschluss berichten.
512 Matches sind **128 unabhängige Seedblöcke**, nicht512 unabhängige Replikate.

Ein ausreichend präziser/praktischer Pilothinweis verlangt **alle** Kriterien:
Punkteschätzer≥+0,15, untere95-%-t-Grenze>0, volle Breite≤0,30,
positive Punkteschätzer in beiden Gegnerkontexten. Nur D15 wird beurteilt;
keine nachträgliche Wahl von D09 oder Modifikation an P1C-Daten.
Auch bei Erfolg keine Behauptung allgemeiner oder Karrierebestätigung.
Bei Nichterfüllung ausdrücklich **zu Rollen/OOP-Strukturen wechseln**, statt
dieselbe Instruktionskombination unbegrenzt weiter zu simulieren.

Planung vorab aus dem selektierten P1B-Paar, daher bedingt: Punkte-Kontrast-SD
1,317/1,587, erwartete volle95-%-Breite0,510, Power≈21,1% für+0,15 bei n64/Gegner.
Dieser Pilot ist **nicht** für90% Power ausgelegt; keine beobachtete Posthoc-Power
auf Basis seines Effektschätzers. Spätere neue Bestätigungsblöcke planen für feste
Effekte **0,10/0,15/0,20 Punkte**, Power90%, α0,05 und volle Breiten0,20/0,30.
Nichtzentrale Welch-t-Näherung, gleiche n pro Kontext, Kosten8n Matches.
Einmal beobachtete SDs, einmal gemeinsame95-%-Normalmodell-SD-Obergrenzen
(Bonferroni: jede einseitig97,5%, χ² mit n−1df), zusätzlich konservatives
Punkte-Range-Szenario SD3. Diskrete Punktekontraste sind nicht exakt normal;
SD-Grenzen und t-Power sind Modellnäherungen, keine garantierte Power in neuen
Stärke-/Kader-/Gegnerkontexten. Neue Praxisbedingungen brauchen eigenen Pilot.

## Archiv und Veröffentlichung

Historische Messungen, Vorregistrierungen und Analysen bleiben unverändert;
Hashsnapshot gegen Ausgangscommit317dec75d37eeef4199c4e6082a9da87b6396fc7.
Nur eingefrorene Whitelist-JSONL, Hashprovenienz, negative Kontrollen,
alle529 Versuchsplätze, Budget, Analyse/Unsicherheit und technische Grenzen
veröffentlichen. Rohspielmaterial, PKM, Dumps und Binärinputs bleiben privat.
Tests und unabhängiger öffentlicher Verifier, Diff/Secrets prüfen, commit/push.
Nach P1C stoppen. VALID-003 in diesem Auftrag ausschließlich planen.

[Vertrag](../research/specs/TACT-001-P1C.json) ·
[Runner](../analysis/run_tact001p1c.py) · [Analyse](../analysis/analyse_tact001p1c.py) ·
[Export](../analysis/export_tact001p1c.py) · [Verifier](../analysis/verify_tact001p1c.py).

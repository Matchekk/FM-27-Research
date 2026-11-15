# TACT-003-STLESS-R0 – unabhängiger Ergebnisreview

15.11.2026 CET · Research Agent, unabhängig von Runner und eingefrorener
Produzentenanalyse. **PASS für die vollständige Auswertung des registrierten
Piloten.**512 gültige Hauptmatches,64 neue unabhängige Seedblöcke,0 Ausfälle,
0 Ausschlüsse,0 Ersatzseeds. Native Aufrufe dieses Reviewers:0.

Die vorregistrierte IP×OOP-Interaktion bleibt unklar. Das konkret getestete
IP-Positions-/Rollenpaket senkt die marginale xGD nach Holm7. Daraus folgt keine
allgemeine Aussage gegen stürmerlose Systeme, kein isolierter Rollenmechanismus
und keine Karriereprognose.

## Unabhängige Rekonstruktion und Provenienz

Geprüft wurden [alle512 Messungen](../../data/night-002-stless003/main.jsonl),
[Mainabschluss](../../data/night-002-stless003/main-summary.json),
[Jobabrechnung](../../data/night-002-stless003/main-job-accounting.jsonl),
[Budget](../../data/night-002-stless003/main-budget.json),
[Effekte](../../data/night-002-stless003/effects.json),
[512 abgeleitete Kontrastzeilen](../../data/night-002-stless003/seed-contrasts.jsonl)
und [Analyseprovenienz](../../data/night-002-stless003/analysis-provenance.json).

Zusätzlich wurden **alle512 privaten Original-Logs direkt** gelesen: proMatch
genau ein natürlicher Abschluss und eine Statistik aus `original_team_statistics`.
Endstand, Tick, Clock und beide ursprünglichen xG-Werte stimmen mit dem
öffentlichen Export überein. Logbytes wurden gegen gespeicherte Hashes geprüft.
Punkte entstehen ausschließlich aus dem tatsächlichen Endstand als3/1/0;
xGD ist ursprüngliches xGF−xGA, jeweils aus Sicht der deklarierten Testseite.
Keine Produzentenformel oder `research.stats` wurde hierfür importiert.

Die eigene Nachrechnung bildet vier Arme auf beiden Seiten jeSeed und mittelt
die Seiten **innerhalb** des Seeds. Je32 Seeds gehören zu den beiden festen
Kontexten `high_press` und `deep_block`, beide mit Gewicht½.512 Matches sind
somit64 unabhängige Analyseblöcke. Alle8 vorab festgelegten Kontraste wurden
mit Welch/Satterthwaite95%-KI, zweiseitigem p, stratifiziertem20.000-Seedblock-
Bootstrap und der vollständigen Holm7-Familie rekonstruiert. Der registrierte
Bootstrapseed ist4773275660306070691. Alle gespeicherten Mittelwerte, SE, df,
p-Werte, Intervalle und Holmwerte stimmen bis auf Rundung überein.

Der ebenfalls ausgeführte Read-only-Verifier `review_stless003.py private-main`
besteht. Er importiert keine Produzentenanalyse; seine Wiederverwendung des
niedrigen nativen Inputaudits ist offengelegt. Er bestätigt sämtliche512 privaten
Input-/Positions-/Rollen-/Kontrollbelege, vollständige öffentliche/private
Übereinstimmung, Kontrastzeilen, Kontext-/Seiten-SD und Kovarianzen,
Leave-one-out, deskriptive Nenner und bedingte Fallzahlplanung. Alle36 eingefrorenen
Projektquellen stimmen. Die gehashte Analyse ist außerdem im ursprünglichen
Präregistrierungscommit `8fe0c56bbc225317c085eb06ae78cc95ca390265` nachgewiesen.

## Primäre Frage und praktische Unsicherheit

Der volle physische Kontrast ist `(I1O1−I0O1)−(I1O0−I0O0)`, ohne Halbierung.

| Primär: IP×OOP auf xGD | Unabhängig rekonstruiert |
| --- | ---: |
| Mittelwert | +0,0742819 |
| Welch95%-KI | [−0,190999; +0,339563] |
| Zweiseitiges p | 0,577429 |
| SE / Satterthwaite-df | 0,132591 /59,3579 |
| Stratifiziertes Bootstrap95%-KI | [−0,185630; +0,328572] |
| Volle primäre KI-Breite | 0,530562 |
| Vorab gewünschte volle Breite | ≤0,50: verfehlt |

Der Punktschätzer liegt unter der praktischen Referenz0,20. Das Intervall lässt
einen praktisch relevanten positiven Interaktionswert ebenso zu wie Null und
negative Werte. Es liegt nicht vollständig innerhalb [−0,20;+0,20]. Weder
Wirkungslosigkeit noch Äquivalenz oder eine positive Moderation sind belegt.
Ein positiver DoD ist außerdem kein Beweis positiver einfacher IP-Effekte.
Die beiden beobachteten einfachen xGD-Effekte sind deskriptiv−0,386968 beiOOP0
und−0,312687 beiOOP1; ihre Differenz erklärt den positiven DoD ohne Siegerbehauptung.

## Vollständige vorregistrierte Sekundärfamilie

Die95%-Intervalle unten sind punktweise; die Entscheidungen verwenden Holm7.
Positive GA/xGA bedeuten mehr tatsächliche Gegentore/Chancenabgabe.

| Kontrast /Endpunkt | Effekt | Punktweises95%-KI | p roh | p Holm7 |
| --- | ---: | --- | ---: | ---: |
| Marginales IP-Paket /xGD | −0,349828 | [−0,501871; −0,197784] | 0,0000231065 | **0,000161745** |
| Marginales OOP-Paket /xGD | −0,166636 | [−0,300065; −0,033207] | 0,0152388 | 0,0914331 |
| Interaktion /Punkte | +0,273438 | [−0,122343; +0,669218] | 0,172118 | 0,860592 |
| Interaktion /GF | +0,109375 | [−0,223482; +0,442232] | 0,513637 | 1 |
| Interaktion /GA | −0,187500 | [−0,516262; +0,141262] | 0,258389 | 1 |
| Interaktion /xGF | +0,002354 | [−0,201531; +0,206238] | 0,981655 | 1 |
| Interaktion /xGA | −0,071928 | [−0,298078; +0,154221] | 0,527254 | 1 |

Nur das vorab definierte marginale IP-xGD-Ergebnis erreicht seine korrigierte
Schwelle. Es ist der gemittelte Effekt dieses ganzen IP-Pakets über beide
OOP-Zustände und festen Gegnerkontexte. Sein Punktschätzer überschreitet0,20
im Betrag; das punktweise Intervall garantiert jedoch keinen Nachteil von
mindestens0,20, da seine obere Grenze−0,197784 beträgt. Die Primärreferenz0,20
wird nicht nachträglich in eine neue sekundäre Bestätigungsregel umgedeutet.
Das OOP-Ergebnis ist trotz negativem punktweisem Intervall nach Holm unklar.
Punkte/GF/GA bestätigen keine Interaktionsrichtung. Kein unregistrierter
IP-Punktetest wurde ergänzt; fehlende Signifikanz wurde nicht als Null behandelt.

## Armwerte und Sensitivität: deskriptiv

Gleiche Kontextgewichte, jeArm128 Matches beziehungsweise dieselben64 Seedblöcke.
Diese Werte wählen keinen besten Arm und liefern keine zusätzlichen Tests.

| Arm | xGD | Tatsächliche Punkte/Match | GF | GA |
| --- | ---: | ---: | ---: | ---: |
| I0-O0 | +0,153970 | 1,5078125 | 1,484375 | 1,3828125 |
| I1-O0 | −0,232999 | 1,1015625 | 1,1640625 | 1,4687500 |
| I0-O1 | −0,049807 | 1,2265625 | 1,1796875 | 1,4296875 |
| I1-O1 | −0,362494 | 1,0937500 | 0,968750 | 1,3281250 |

Die primäre Interaktion beträgt deskriptiv+0,264487 gegen high_press und
−0,115923 gegen deep_block. Die Seitenmittel sind dort+0,026362/+0,502612
beziehungsweise+0,106705/−0,338551; keine feste Moderationsrichtung über
Kontexte/Seiten. Block-SD1,167274 und0,942213, Seitenkovarianzen−0,139353
und−1,337095. Die Seiten separat als unabhängige Replikate zu zählen wäre falsch.
Beim Weglassen genau eines Seeds unter Beibehaltung gleicher Kontextgewichte
liegt die primäre Schätzung zwischen+0,039611 und+0,115720, maximale Änderung
0,041438. Das ist eine explorative Stabilitätsbeschreibung, kein Ersatztest.

Die marginale IP-xGD ist in beiden Kontexten negativ (−0,418598/−0,281057)
und in allen vier Kontext×Seitenmitteln negativ. Das begrenzt eine Erklärung
durch nur eine einzelne beobachtete Seite, erweitert jedoch nicht die Population
auf andere Gegner, Profile oder Karrierebedingungen. Keine deskriptiven
Missing Values im vollständigen Mainexport; keine Nullimputation.

Die registrierte bedingte Planung wurde ebenfalls nachgerechnet: bei beobachteter
Block-SD für0,20/90% Power149 neue Seeds jeKontext beziehungsweise2384 Matches;
mit simultaner95%-SD-Obergrenze263 jeKontext/4208 Matches. Das sind modellabhängige
Planungszahlen für dieselben Kontexte, keine zugesagte Power oder Fortsetzungsfreigabe.

## Vollständigkeit, Prozessbereinigung und Ressourcen

Alle512 geplanten Mainjobs sind genau einmal gültig, natürlich abgeschlossen
und abgerechnet.0 fehlerhafte/fehlende/unbegonnene Jobs,0 Retries,0 aktive
Claims am Ende. Alle512 tatsächlichen Kernelcontainmentreceipts wurden direkt
auf bestätigten Kapselabschluss, Cleanup und0 Kernelrestprozesse geprüft.
0 Pendingmarker, keine gemeinsame NativeLease und keine gefundenen
Observer-/Simulatorrestprozesse. Vier gleichzeitige Claims sind im Ledger
belegt; dies ist kein gemessener Engine-PID-Peak.

Die512 Admissionproofs wurden zusätzlich direkt in ihrer sperrserialisierten
Concurrencyreihenfolge nachgespielt. Jede Zulassung enthält40s je bereits
unaufgelöstem/neuem Claim; abgeschlossene tatsächliche Calls bleiben belastet.
Höchste Mainobergrenze2700,387s/3600s. Längster tatsächlicher Maincall3,813s,
alle512 unter30s absolut und40s reservierter Hülle. Der unveränderte gehashte
Runner setzt `total_timeout=min(allowance,30)` und Job3.

- Maincall-Summe1609,884s; zusammen mit105,142s neuer Technik und838,064s
  terminaler alter Calls ergibt das2553,090s/3600s tatsächliche Callsumme.
- Eigenes Whole-phase-Budget658,0032682s/900s =75,6647733s Technik +
  582,3384949s Main. Global1310,2193456s/3600s; alte589,7353507s bleiben erhalten.
- 1090 globale Reservationen =545 alte +545 neue; keine Rücknahme alter
  unbegonnener MECH-Plätze. MECH-eigenes Haltledger bleibt528,8133745s,
  `halted=true`, global weiterhin als terminale Studie geführt.
- Abschluss15.11.00:12:50,427500UTC vor unveränderter eigener Frist01:19:09,243151UTC
  und Missionsgrenze07:00UTC. Erstes Mainrestgate767,628073s≥600s.
- Geprüfter privater Snapshot298.353.116TACT-Bytes beziehungsweise445.429.523
  Missionsbytes, unter2/4GiB. Alle Originalbelege erhalten, keine Livearchivierung.

Die Hauptphase folgte dem veröffentlichten technischen Releasecommit
`bae2e15c1428135f706756a55782c890f195f26c`; das Actions-API bestätigt
[CI43655940573](https://github.com/Matchekk/FM-27-Research/actions/runs/43655940573)
success15.11.00:01:49UTC, vor Mainaufsicht00:03:08UTC und erster nativer
Admission00:03:54UTC. Die neue Abbildung wurde erst nach vollständigem Export
erzeugt, ist kein eingefrorener Ausführungscode und wurde visuell geprüft:
vier korrekte deskriptive Armmittel, korrektes Primärintervall und Paketlabels.
Sie fügt keinen Test hinzu.

## Wissenschaftliche Freigabegrenze

Akzeptiert ist ein vollständiger vorregistrierter **Paketpilot** auf FM27
`27.0.1+2503222`, Tactics Lab v1114.6, unverändertem passivem Observer und
gebündeltem synthetischem D00-Fixture. IP1 verschiebt denselben AMC nachAMCL
und denselben ST nachAMCR samtCF→SecondStriker; OOP1 verschiebt dieselben
Akteure nachAMCL/AMCR samtOPCF→OPAM. Lateralisierung, Position und intrinsisches
Rollenverhalten bleiben gemeinsam verändert. Zugewiesene Zellen sind belegt;
Laufwege, UI-Effectiveness und isolierte interne Mechanismen sind nicht gemessen.

Kein bestätigter allgemeiner Taktiksieger, keine OP- oder Anti-Stürmerlos-Regel,
keine unabhängige Karrierebestätigung. Die beiden bekannten Gegner und
omnipotenten Positionsratings begrenzen den Transfer. Der signifikante
sekundäre Paketbefund rechtfertigt eine eng formulierte Beobachtung, keine
nachträgliche Umdeklaration zum erfolgreichen Primärtest.

**MECH-004 bleibt dauerhaft unvollständig und terminal.** Seine224 Hauptresultate
wurden hier weder gelesen noch statistisch verwendet; seine257 tatsächlichen
Calls erscheinen ausschließlich als erhaltene historische Ressourcenlast.
Dieser Review gibt keine neuen Seeds, keine Serie und keine Wiederaufnahme frei.

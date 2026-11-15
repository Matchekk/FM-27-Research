# N3-SHARPSTRUCT-C1 – Matchschärfe × IP-Struktur

Vorregistrierung 15.11.2026, NIGHT-003. Neue unabhängige Frage, neue Budgets und
Seeds. Historische Studien, insbesondere terminales MECH-004, bleiben unverändert.
[Quellen-/Duplikatentscheidung](../docs/night-003/LITERATURE.md): NOVEL_HYPOTHESIS.

## Einziger primärer Gegenstand

`(xGD(C)−xGD(A))−(xGD(D)−xGD(B))`, zweiseitig α=0,05.
Positive Werte: STLESS gewinnt gegenüber BASE relativ mehr bei hoher Schärfe.

| Arm | IP-Paket | Gemeinsame C90/C7A-Startrohwerte |
|---|---|---:|
| A | originales 4231 | 10000 |
| B | originales 4231 | 7000 |
| C | archiviertes TACT-003 IP4240 | 10000 |
| D | archiviertes TACT-003 IP4240 | 7000 |

Originaler Slot8 AMC→AMCL/AttackingMidfielder; Slot10 ST→AMCR/SecondStriker.
Alle OOP-Records bleiben originales 4411. Ausschließlich drei IP-Records und
gegebenenfalls zwanzig Profilrecords der zehn Feldstarter ändern sich.
Keeper, Bank, Gegner, Identitäten, 69 Attribute, Positionsratings, explizite PI,
Team Instructions, Standardpressing der Testseite und Originalmanagement gleich.
Kein Kind61, kein Setter nach Vorbereitung, keine Clamps, keine Karrieresaves.
Bestehende Compiler werden unverändert aufeinander angewandt.

## Stichprobe und Auswertung – vor dem ersten wissenschaftlichen Match fest

**4096 Hauptmatches = zwei feste Gegner × 256 neue Seeds × zwei Seiten × vier Arme.**
512 unabhängige Kontext-Seedblöcke; je Block Seitenmittel, Kontexte gleich gewichtet.
Alle Arme werden innerhalb des Blocks gepaart; vollständige Blockreihenfolge
mit festem Schedulerseed 2026111503 gemischt. Keine Pilot-Leistungsdaten,
keine Zwischenanalyse, keine p-Wert-basierte Erweiterung oder Teilgruppenauswahl.

Primär Welch/Satterthwaite-95%-KI über die zwei festen Kontextmittel; Sensitivität
20000 stratifizierte Seedblock-Bootstraps, RNG 2026111503. Praktische Referenz
±0,20 xGD; volle KI-Breite ≤0,25 angestrebt. Ein KI vollständig innerhalb ±0,20
schränkt Effekte dieser Größenordnung im Kontext ein, beweist keine universelle
Wirkungsfreiheit. Ein unpräziser Nullbefund bleibt offen.

Eine vorregistrierte **Holm6-Sekundärfamilie**: derselbe Interaktionskontrast auf
tatsächliche Punkte3/1/0, Tore, Gegentore, xGF, xGA; außerdem Interaktion
high_press minus Interaktion deep_block auf xGD. Kontextunterschied ist ein
Vergleich zweier fester Profile, keine zufällige Gegnerpopulation. Einfache
IP-Effekte bei hoher/niedriger Schärfe, marginale Effekte und Armmittel nur
deskriptiv mit ausdrücklich unadjustierten Intervallen; keine weiteren Sieger-
oder Signifikanzentscheidungen. Sekundäre KI sind marginal, Holm nur für p-Werte.

Planungsanker: archivierte Block-SD der TACT-003-IP×OOP- und MECH-002-Schärfe×Pressing-
Interaktion sowie des MECH-002-Haupteffekts. Erwartete Power für 0,20 und volle
KI-Breite stehen **vor Main** in `data/night-003-sharpstruct/planning.json`.
Zusätzlich simultane95%-Normalmodell-SD-Obergrenzen (je97,5%,df31).
Andere Kontraste sind keine garantierte Varianz der neuen Interaktion.
4096 wird vor Daten festgelegt; kein optionaler statistischer Pilot vorgesehen.

## Eingabe, Gates und Ressourcen

FM27 `27.0.1+2503222`, Engine `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`,
Observer `58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`,
Tactics Lab v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be. Pro Phase
gesperrte Ressourcen-/Inputdateien, pro Call geladener DLL-Hash und volle Readbacks.

Technik32+1: vier eigene neue Seeds, alle16 Kontext×Seite×Arm-Zellen zweimal,
16 exakte A/A-Paare einschließlich ursprünglicher Statistik/passiver Zustände;
eine erwartete Exit108-Negativprobe. Alle3174Attribute,1058Profilfelder,
44Phasenzellen,748PI-Gruppen und ursprüngliche Actorbindungen geprüft.
C90/C7A und tatsächliche Startercache8a nach Vorbereitung/erstem Fortschritt
10000/100 bzw.7000/70; Nichtschärfe-/Raw-TF33-Kontrollen bleiben D00 gleich.
Originale native Legalitätsprüfungen aktiv. Keine neuen allgemeinen VALID-Module.

Vor Main: veröffentlichte eingefrorene Vorregistrierung/Code/konkrete Inputs,
erfolgreiche exakte CI, alle technischen Gates und zweiter Rohbelegpass nach
vollständiger Prozessbereinigung. Separate arithmetische Nachrechnung des
Primäreffekts aus ursprünglichem Team-xG; gleicher Analyst, keine behauptete
unabhängige Person. Rohbelegprüfungen und statistische Nachrechnung getrennt.

Eigene feste Limits:7200s kumulierte beaufsichtigte Phasenzeit,10800s UTC-Fenster
ab erster nativer Technikphase,33Technik-/4096Mainjobs,4 kalte Worker und eine
globale exklusive NativeLease. Je Call unverändertes Windows-Jobcontainment3,
absolut30s plus vorhandene begrenzte Bereinigung;90s Fortschrittslimit bleibt.
16GiB private Belege,20GiB freie Reserve. Zu Beginn waren etwa390GiB frei.
Historische TACT-003-Hauptphase582,34s/512Matches; lineare Planungsprojektion
4658,71s für4096 plus Technik/Prüfungen passt in7200s, keine Laufzeitgarantie.

Erster Input-/Build-/Seed-/Readback-/A/A-/Legalitäts-/Budget-/Cleanupfehler stoppt
neue Zulassungen. Begonnene Calls beaufsichtigt bereinigen; unbegonnene/fehlende
Jobs und Gründe erhalten. Keine Retries/Ersatzseeds, Nullimputation oder
Ergebnisausschlüsse. Nur vollständige4096 ermöglichen Bestätigungsanalyse.
Keine Komprimierung, Verschiebung, Löschung oder Pfadänderung während der Phase.

Manifest: `data/night-003-sharpstruct/inputs.json`, `seed-plan.json`,
`technical-plan.json`, `main-plan.json`. Messungen: `technical.jsonl`, `main.jsonl`.
Analyse: `analysis/analyse_night003.py`; Runner: `analysis/night003.py`.
Geschützte Rohdumps/Originalressourcen bleiben ausschließlich lokal.

## Gültigkeitsgrenzen

Ein gebündeltes synthetisches Fixture, zwei bekannte Gegner, omnipotente
Positionsratings, keine reale Karriere/Urlaub/Instant-Result-Gleichsetzung.
IP-Paket verändert Positionen und Rolle gemeinsam; kein isolierter Bewegungs-
oder Rollenmechanismus, kein allgemeiner Formationssieger oder Scoutingranking.

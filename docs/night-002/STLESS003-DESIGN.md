# TACT-003: kontrollierte stürmerlose IP/OOP-Pakete

**Vorbereitung, keine native Freigabe.** Die neue Frage `N2-02` prüft eine
konkret veränderbare Paketinteraktion statt ein weiteres Taktikranking.
[Vollständige Vorregistrierung](../../experiments/TACT-003-stless-preregistration.md) ·
[Compiler und Audit](../../analysis/stless003_design.py) ·
[Analyse](../../analysis/analyse_stless003.py).

## Wissenschaftlicher Unterschied zur Vorarbeit

Das eigene [TACT-002-R0](../../experiments/TACT-002-R0-results.md) kreuzte
ST-/AMC-Rollen bei unveränderten Positionen. Der Primärrolleneffekt blieb unklar;
das beantwortet keine Frage zu stürmerlosen IP-/OOP-Strukturen.
[Mac06](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/06-tactics-x-familiarity.md),
[Mac07/07b](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/07b-tactic-league-18.md)
und [Mac19](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/19-a-season-per-tactic.md)
vergleichen Gesamttaktiken beziehungsweise Presets. Das aktuelle
[FMAX-Leaderboard](https://getfmax.com/en/lab/) motiviert eine Mechanismusfrage,
isoliert aber diesen Faktorvergleich nicht. Der
[aktuelle Originalquellenaudit](LITERATURE_AUDIT.md) berücksichtigt den
unveränderten Mac-HEAD, weitergewanderte FMAX-Ränge und den offiziellen Patchstand.

Entscheidung: `NOVEL_HYPOTHESIS` innerhalb der überprüften lokalen/externen
Quellen, keine Behauptung weltweiter Erstmaligkeit. Überlappende Quellen-IDs:
MAC-06/07/07B/19, FM27-FMAX-LAB, TACT-002-R0. Neu ist das gekreuzte,
reproduzierbare IP-/OOP-Paket mit denselben Akteuren und unveränderten Profilen.

## Konkreter Eingriff und Identifizierbarkeit

| Faktor | Niedrig / ursprüngliches D00 | Hoch / eigenes Paket |
| --- | --- | --- |
| IP | 4231: Slot8 AMC/AttackingMidfielder, Slot10 ST/CentreForward | 4240: derselbe Slot8 AMCL/AttackingMidfielder, derselbe Slot10 AMCR/SecondStriker |
| OOP | 4411: dieselben Akteure AMC/OPAttackingMidfielder und ST/OPCentreForward | 4420: dieselben Akteure AMCL/AMCR, beide OPAttackingMidfielder |

Vier Arme I0-O0/I1-O0/I0-O1/I1-O1. Primär die volle xGD-Differenz der Differenzen,
Koeffizienten1/−1/−1/1. Sekundär IP- und OOP-xGD sowie derselbe Interaktionskontrast
auf tatsächliche Punkte/Tore/Gegentore/xGF/xGA, eine Holm7-Familie.

Die beiden Faktoren sind ausdrücklich **Pakete aus Positionen und einer Rolle**.
Ein isolierter Rollen-, Formations-, Bewegungs- oder Complexityeffekt lässt sich
daraus nicht ableiten. Der Nutzen liegt darin, festzustellen, ob die konkrete
stürmerlose IP-Umstellung von einer gleichzeitig passenden OOP-Zuordnung abhängt.
Das würde einen folgenden engeren Mechanismustest begründen, keinen allgemeinen
Sieger oder direkten Import einer öffentlichen Spitzentaktik.

## Technische Ausführbarkeit und Sicherung gegen Confounder

Der originale validierte Observerhost unterstützt schon getrennte Kind4-Rollen-
und Kind5-Positionsrecords. Es braucht keinen neuen Host, Setter, Serverimport
oder Laufzeiteingriff. Der ursprüngliche native Game-Legalitätscheck bleibt
eingeschaltet. Die vorhandenen vollständigen Input-/Actual-Actor-Readbacks
prüfen Positionen/Rollen in beiden Phasen nach Originalvorbereitung.

Die seitenspezifische OOP-Permutation wird erhalten: Akteur8 ist in den zwei
ursprünglichen Seitenkontexten auf unterschiedliche native OOP-Slots abgebildet.
Ein ungemappter identischer Index würde die falsche Person bewegen und wird
vom Compiler abgewiesen. Alle69 Attribute und23 Profilfelder jedes aktiven
Akteurs, Kapazitäten, Startelf, Team Instructions, Keeper, Bank, Gegner,
Management und sonstigen Startzustände bleiben gleich. Omnipotente Feldpositions-
ratings verhindern eine zwischen den Armen geänderte Positionseignung, bilden
aber realistische Spielerprofile nur begrenzt ab. Explizite PI bleiben0;
intrinsisches Rollenverhalten ist Bestandteil des Pakets.

Alle vier tatsächlich vorhandenen D00-Eingaben wurden **offline** durch den
Compiler geprüft:0/3/3/6 geänderte Records je Arm; alle Unterschiede betreffen
ausschließlich die deklarierten Kind4/5-Einträge. Komplette ursprüngliche
3174 Attributwerte und44 Rollen-/44 Positionsrecords müssen zu Config und
OOP-Permutation passen. Diese Prüfung ist noch keine native Abnahme.

Nach Vorbereitung und erstem tatsächlichem Fortschritt müssen dieselben
nonsharpness-/Raw-TF33-Kontrollhashes wie in D00 vorliegen. Eine unerwartete
Änderung stoppt die Studie; das Gate wird nicht nachträglich gelockert.

## Aufwand, Präzision und Veröffentlichung

TECH32+1: vier neue Kontext×Seiten-Seeds,16 Eingabezellen zweimal,16 exakte
A/A-Paare plus Negativabweisung. Danach nur mit unabhängigem Rohreview,
veröffentlichtem Gate und erfolgreicher CI512 Hauptmatches:32 neue Seeds je
bekanntem Gegner, vier Arme/beide Seiten,64 unabhängige Blöcke. Keine Ersatzseeds,
Retries, Holdouts oder Erweiterung bei knapper Nichtsignifikanz.

Praktische Referenz0,20xGD; gewünschte volle95%-Breite≤0,50. Die unbekannte
Interaktionsstreuung verhindert eine garantierte90%-Power. Seiten werden im
Seed gemittelt, Gegner fest gleichgewichtet. Welch95 und20.000-Block-Bootstrap,
vollständige Ausfälle, Blockkontraste und tatsächliche Scoreendpunkte werden
öffentlich nachvollziehbar; native Rohspielressourcen bleiben privat.

Eigener enger Vertrag:900 kumulierte Childsekunden,5400 Sekunden ab erstem
nativem Technikcall,2GiB private Artefakte,maximal vier kalte Worker. Die ersten
Maincalls benötigen mindestens600 Sekunden eigene/globale Child-/UTC-Restzeit.
Der Director allein führt unter einem zentralen Supervisor/exklusiver Lease aus.
Die globale NIGHT-002-Frist07:00Z/08:00CET und alle globalen Limits bleiben bindend.

Vor TACT-Seedreservierung wird außerdem eine zusätzliche konservative Summe
aller nativen Aufrufzeiten eingefroren:3600 Sekunden für die gesamte Mission.
Ein Call erhält höchstens30 Sekunden absoluten Ausführungstimeout; vor jedem
Claim werden40 Sekunden inklusive begrenzter Bereinigung reserviert. Zulässig
ist der Claim nur, wenn die tatsächliche Aufrufsumme der abgeschlossenen ersten
Studie plus die eigenen abgeschlossenen Dispatchledgerzeiten plus40 Sekunden
je eigenem unaufgelöstem begonnenem Job und neuem Claim höchstens3600 ergeben.
Die Prüfung erfolgt unter der zentralen Scheduler-Zulassungssperre. Nach
Abschluss wird das reservierte Envelope mit der tatsächlichen Aufrufzeit
abgerechnet; bereits belastete tatsächliche Zeit wird nie zurückerstattet.
Fehler bleiben terminal. Die drei Vertragswerte heißen
`per_call_absolute_timeout_seconds=30`, `per_call_reserved_envelope_seconds=40`
und `global_native_call_elapsed_limit_seconds=3600`.

Die bestehende globale3600-Childsekunden-Abrechnung ganzer Phasen bleibt
unverändert zusätzlich aktiv; diese zweite Summengrenze definiert sie nicht
neu. Eigene900 Childsekunden und mindestens600 Sekunden Mainrest bleiben
ebenfalls bindend. Ein separater unabhängiger Runnerreview muss die neue
Zulassung einschließlich Bereinigungsgrenze bestätigen, bevor Native startet.

Die acht fokussierten Synthetiktests prüfen exakte Änderungen und stabile
Profile, OOP-Aktorzuordnung, illegale Rollen/Positionen, PI-/Eignungsabweichungen,
fehlende Game-Checks, falsche Originalrecords, DoD-Skalierung, Holm7, fehlende
Beobachtungen und Vertragsdrift. Sie bestehen in der Projektumgebung.
Noch ausstehend: finale Runner-/Inputfreigabe, neue native TECH32+1-Abnahme,
separater Mainrelease und wissenschaftlicher Ergebnisreview. Kein geplanter
Schritt wird als ausgeführtes Match oder neue Meta-Erkenntnis bezeichnet.

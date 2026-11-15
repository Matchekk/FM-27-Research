# Training – Belege und Ausführungsgrenze

Status15.11.: **Karriereexperiment technisch blockiert**, Entscheidung bereits
im ersten Machbarkeitscheck. Keine private Saveöffnung/Änderung,0Advances.
TRAIN-001 bleibt explorativ, TRAIN-002 unbegonnen. Kalenderbestand ist kein
Nachweis individueller Teilnahme; Spieleranzahl ist keine Karriere-Replikatzahl.
[API-Lücken](../night-001/TRAIN-API-GAPS.md) wurden gegen aktuelle öffentliche
fmsave-Modelle geprüft.

## Direkter Quellenvergleich

| Quelle | Was sie beiträgt | Wesentliche Grenze |
|---|---|---|
| [Harvestgreen22](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test) | Autor bevorzugt Conditioning+Attacking Ball Work beziehungsweise Light Conditioning+Conditioning+beide Ball-Work-Arten; beschreibt Fokus/Intensität als Wachstumsverteilung | Eigene Aussage: begrenzte Plankombinationen getestet. Anhänge/Rohläufe nicht unabhängig nachgerechnet; Trainings-/Fokus-/Belastungspaket statt isolierter Fokuskausalität |
| [ZaZ](https://fm-arena.com/threads/training-schedules.60/) | Praktische Growth-/TU-Pläne, gebündelte Trainingstage und Ruhe; konkrete Intensitätsregeln | Guide und Bezug auf andere Forschung, keine verifizierte unabhängige Karriere-RNG-Serie; selbst ausdrücklich ungetestete Spezialfälle |
| [Zergos](https://sortitoutsi.net/content/78226/optimal-training-schedules) | Aktualisierte Growth-, TU+Growth- und U21-Pläne; Rollen-/Fokus-/Intensitäts-/Kalenderempfehlungen | Mehrkomponentenpaket, keine hier prüfbaren Rohdaten unabhängiger gepaarter Karrierearme; Nutzerberichte sind keine kontrollierten Replikate |
| [SI](https://www.footballmanager.com/fm27/features/fm27-training-and-tactical-effectiveness) | Offizielle Beschreibung von Training und Tactical Effectiveness | Featurebeschreibung, keine quantitative Wachstums-/Verletzungsstudie |
| [TRAIN-001](../../experiments/TRAIN-001-karriere.md) | Tatsächlich archivierte Deltas und Kalender-/Belastungsbelege | Je Arm einzelner Saveableger, fehlende Teilnahmehistorie, kein kausales Alters-/Planranking |

Die drei Communityquellen sind nicht drei unabhängige Bestätigungen desselben
Effekts: Sie beziehen sich teilweise auf dieselbe Forschung und kombinieren
unterschiedliche Pläne, Fokus, Minuten und Intensität. Wir bestätigen oder
widerlegen daraus keine Behauptung über effizientes Training.

## Was die eigenen Daten erlauben

TRAIN-001 vergleicht bei Profis Heavy−Conditioning nach6Wochen mit einem
deskriptiven CA-Abstand+0,091 und einem vierteiligen Rohindex+0,022727.
U19 Rest−Conditioning nach4Wochen: CA+0,227 und Rohindex−0,034091.
Die unterschiedlichen Alterskohorten, Horizonte und Eingriffe identifizieren
**keinen kausalen U19-versus-Profi-Unterschied**. Keine KIs aus22Spielern
als vermeintlich22unabhängigen Trainingswiederholungen. Verletzungseinträge
sind keine Ausfalltage. Diese Zahlen sind historische Ergebnisse und keine
neuen bestätigten Trainingseffekte dieser Sitzung.

## Entscheidung gegen einen Scheinkarrierepiloten

Keine heutige validierte Session×Spieler-Teilnahme mit Abwesenheitsgründen,
belegte Fokus-/Coach-/Intensitätszuteilung, beobachtete Verletzungsintervalle,
unabhängige Karriere-Zufallszustände oder erlaubte isolierte Pilotkohorte.
Gespeicherte Wochen können nach dem Parser-Datumsclaim liegen. Ein neuer
Matchseed, Savehash oder Single-Match-Host behebt diese Lücken nicht.
Bis zur45-Minuten-Entscheidungsgrenze war die Wahl daher bereits gefallen:
**0neueKarrierearme,0Armwochen,0Fortschreibungen; Rollenstudie stattdessen.**

Die Ziele ΔCA, Δleistungsgewichtetes Profil und Verletzungstage bleiben getrennt.
Individueller Fokus ist erst dann kausal vergleichbar, wenn regulärer Plan,
Intensität, Exposition und Spielminuten kontrolliert werden. U18/U21/22–27/ältere
Profis verlangen eigene Altersstrata und mehrere unabhängige Karrierepaare.
Kein quantitativ belegter „bester Trainingsplan“ und kein Trainingsscore2.0
aus den derzeit vorhandenen Daten.

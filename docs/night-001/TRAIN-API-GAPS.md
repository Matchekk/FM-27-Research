# TRAIN: Was die eingefrorene Reader-API tatsächlich abdeckt

Offline-Quellenprüfung des offiziellen fmsave0.12.4, Releasecommit
`e0704bc5d7e6bf687fecf85cd48b28c497bdef68`. Keine erneute Saveöffnung, kein
Trainingsexperiment. [Maschinenlesbare Feld-/Methodeninventur](../../data/night-001-career-r3/source-audit.json)
enthält deklarierte Felder und öffentliche `Save`-Methoden; bloße Feldnamen und
Upstream-Statusregister belegen keine lokale native/UI-Semantik.

Die aus vorhandenen R2-Ledgers erneut aufsummierten vier Teamrecords enthalten
155gespeicherte Wochen,1085Tage,3255Sessioncodes. Einige Wochen reichen über den
Parser-Savedatumclaim hinaus. Das ist ein gespeicherter Kalenderbestand und keine
Zählung tatsächlich durchgeführter Einheiten oder155 experimenteller Replikate.
Der bestehende [Codeabdeckungsbericht](../../data/night-001-career-r1/training-code-coverage.json)
erhält auch unbekannte Sessioncodes; neue Prüfung überschreibt ihn nicht.

| Benötigter Beleg | Eingefrorene API/Quelle | Tatsächliche Reichweite |
|---|---|---|
| Wochen/Termine/Sessioncodes | `Save.training` → `TeamTraining.weeks` → `TrainingWeek.days` → `TrainingDay.sessions` | Teamkalender und gespeicherte Codes; keine individuelle Anwesenheit |
| Individuelle Teilnahme je Einheit | Kein entsprechend typisiertes Feld in den inventarisierten Trainings-/Spielermodellen und keine eigene öffentliche Save-Methode | Weiter Missing; Kalender und Kaderzuordnung reichen nicht |
| Coachzuordnung pro Einheit/Spieler | `Save.staff`, `Save.staff_lists`; Staff enthält Job, Attribute und Präferenzen | Personal-/Listenmodell ohne Session-/Spieler-Expositionsjoin; in R2 nach Fehler nicht ausgeführt |
| Individueller Fokus | Weder `Player` noch Trainingsmodelle deklarieren einen solchen Fokusbeleg | Keine geprüfte typisierte API für diese Anforderung |
| Individuelle Intensität | `StaffPreferences.hardness_of_training` ist eine Personalpräferenz | Kein individueller Intensitätsplan und kein durchgeführter Belastungsnachweis |
| Mentoring | `Save.mentoring` → `MentoringGroup` mit Mitgliedern | Gespeicherte Gruppenzuordnung, keine Trainingsteilnahme oder kausale Entwicklung; bisher nicht ausgelesen |
| Entwicklung | `Player.attributes/raw_attributes`, Ability sowie Rohzustände für Kondition/Schärfe | Ein Snapshot ist kein gemessener Verlauf; Roh-/Anzeigeskalen bleiben lokal unkalibriert |
| Verletzungen | `Save.injuries`, separate Injury-Modelle | APIexistenz allein beweist keine beobachteten Abwesenheitsintervalle; R2-Probe unbegonnen |
| RNG-/Replikat-Unabhängigkeit | Keine typisierte öffentliche Save-Methode für einen belegten Karriere-RNG-Stream | Bytekopien und neue Labels erzeugen keine unabhängigen Replikate |

Diese Aussage betrifft die geprüfte **öffentliche typisierte API** und ihre
inventarisierten Modelle, nicht das vollständige binäre Saveformat. Undekodierte
Bytebereiche oder `unknown`-Mappings könnten zusätzliche Informationen enthalten;
ihnen wird hier keine neue Bedeutung zugeordnet. Methoden können außerdem
intern gemeinsame Decoder nutzen. Eine vorhandene Methode ist weder eine
erfolgreiche lokale Messung noch eine vollständige Datengrundlage.

Quellen, jeweils exakt eingefroren:
[Trainingmodelle](https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/models/training.py),
[Spielermodelle](https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/models/players.py),
[Personalmodelle](https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/models/staff.py),
[Save-API](https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/_save.py).
Die eigenen Reports geben deren Quellenhashes über das unveränderte R2-Manifest
wieder. Kein neuer Upstreamstatus wird als eigener Validierungsbeweis übernommen.

Nächste notwendige technische Schritte: eine kleine UI-/Export-Goldstichprobe für
Sessiondatum und Codes, separat belegte Session×Spieler-Teilnahme mit Ursache
der Nichtteilnahme, effektive Coach-/Fokus-/Intensitätszuordnung und echte
Verletzungsstart-/Rückkehrbelege. Erst danach ein eigener Kalenderadvancevertrag
mit Vor-/Nachzustand, Zeit-/Abbruchbudget und belastbarer RNG-Replikatstrategie.
Keine Trainingshauptserie oder Karrierefortschreibung aus dieser Bestandsaufnahme.

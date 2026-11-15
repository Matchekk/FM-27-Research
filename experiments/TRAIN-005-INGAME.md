# TRAIN-005-INGAME – ein kontrolliertes Karrierepaar

15.11.2026. Status **BASELINE_FROZEN_BEFORE_TIME_ADVANCE**; technische Vorbereitung auf ausdrücklichen
Nutzerauftrag. Eigenes neues Einpaar-Experiment, keine terminale Studie fortgesetzt.

Hypothese: Ein zusätzlicher individueller Quickness-Fokus erhöht beim selben
jungen Spieler unter unverändertem Mannschaftstraining die Achtwochenentwicklung.
A ohne Quickness, B mit Quickness; sonst identische Einstellungen. Primär
`[(Acc_56−Acc_0)+(Pace_56−Pace_0)]/2` in B minus A.
Sekundär CA/PA, übrige Attribute, Minuten, Ausfalltage, Kondition/Schärfe.
Keine Werte schätzen; nur UI-Attribute gegebenenfalls mit Rundungsgrenze.

Ein gemeinsamer Ausgangssave, zwei bytegleiche Kopien; **ein** Karrierecluster,
keine unabhängige Bestätigungsstudie, keine KI-/p-Wert-Schätzung. Ziel: derselbe
belegte Starttag plus 56 Kalendertage in beiden Armen, kein Urlaub-Ersatz für
reguläres Fortfahren. Keine Matchseedreservierung.

Vor Start Spieler, vollständige Baseline, konkreten Wochenplan, Intensität,
Fokuspaket, Verantwortlichkeiten und Umgang mit Pflichtentscheidungen einfrieren.
Originalhash sichern, jeweilige A/B-Zielkopie live identifizieren. Nur deklarierte
Fokusänderung, Setz-Readback und identische übrige Baseline abnehmen. Neu kaufen,
absichtliche Vertrags-/Trainer-/Anlagen-/Taktikwechsel ausgeschlossen.
Minuten/Verletzungen und unvermeidbare Abweichungen dokumentieren. Transfers
nachverfolgen, unlesbare Endpunkte null/NOT_MEASURED, keine Ersatzspieler oder
stille Wiederholung. Kontext-/Buildwechsel oder verlorene Kontrolle stoppen.

Atlas/Index, FINDINGS und heutige vorhandene Originalquellenbelege geprüft.
Überlappung FM27-HARVEST-ATTR, FM27-ZAZ-TRAIN, FM27-SI-TRAIN,
TRAIN-003-SOURCE und nicht gestartetes TRAIN-004. **REPLICATION_WITH_TRANSFER**:
erste eigene gepaarte Karriereintervention; keine neue Auswertung derselben
51 Pläne. Vor einem tatsächlichen wissenschaftlichen Start Quellen-/Patchstand
erneut prüfen. [Eingefrorene Eingaben](../data/player-development-004/preregistration.json).

## Konkretisierung vor der ersten Fortschreibung

Test A ist im Spiel als 16.01.2027 abgenommen. P001: 20-jähriger Feldspieler
aus der Defensivfamilie, UI-Antritt/Tempo 14/14, unabhängig aus der geladenen
nativen Spielerstruktur gelesenes CA/PA 134/160. UID und Geburtsdatum wurden
zwischen UI-Referenz und nativem Objekt abgeglichen und bleiben privat.
76 von 77 angeforderten Baselinepfaden lieferten Belege; der fehlende Pfad
bleibt Missing. Vollständiges Profil samt privaten Hashbelegen vor Eingriff gesichert.

Kontrolle bereits ohne Zusatzfokus (Code −1). B soll ausschließlich die im
Spiel angebotene Option „Schnelligkeit“ (Code 9) erhalten. Setzbefehl zunächst
als technisches Gate prüfen, dann A und B bis 13.03.2027 fortschreiben.
Kein Zeitfortschritt vor Fokus-/Readbackabnahme. Keine native Attributänderung.

Der bestehende Wochenplan ist mit 28 Anzeigeelementen/21 Sessionplätzen gehasht.
Der vollständige zukünftige Achtwochenkalender ist noch nicht unabhängig
eingefroren. Jede während des Laufs beobachtete Planabweichung bleibt sichtbar
und begrenzt eine isolierte kausale Interpretation; nicht nachträglich als
identisch ausgeben. Pro Arm Tages-/Wochenfortschritt und Pflichtentscheidungen
protokollieren; bei verlorener Kontrolle den Lauf als unvollständig ausweisen.

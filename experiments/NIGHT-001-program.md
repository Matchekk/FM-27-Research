# NIGHT-001 – autonomes Forschungsprogramm bis Mitternacht

Neuer ausdrücklicher Nutzerauftrag vom14.11.2026 nach Abschluss von Runde3:
bis **15.11.2026 00:00 Europe/Berlin =14.11.2026 23:00UTC** weiterforschen,
Fragestellungen eigenständig auswählen und die bereitgestellte Wegwerfkarriere
„Test FM Research“ einbeziehen. Dieser Auftrag erlaubt neue Forschungsarbeit;
er überschreibt keine alten Messungen und ersetzt keine technischen Gates.

## Ausgangslage und Architektur

Ausgangspunkt ist Commit `adb708e99c6cb284b493fb7cee1c60ae9361546b`.
Gitstatus sauber,origin/main abgeglichen. DLL-Dateiversion27.0.1, Produktversion
27.0.1+2503222 erneut tatsächlich gelesen. Runtime v1114.6 bleibt unverändert.
Die alten eigenen Runner,Studienbudgets und reservierten Seeds werden nicht wiederverwendet.

Während der Vorbereitung erschien unabhängig Remotecommit
`fd954ba442ec64371779f55ed6d124e97fede2f3` mit privatem Capture-/VALID-004-Plan.
Der erste Push wurde daher regulär zurückgewiesen. Remote wurde ohne Force-Push
integriert;alle fremden Dateien bleiben erhalten. Die eigene Karriere-Readback-
Vorarbeit wird als separate Teilstufe dieses VALID-004-Plans geführt.

Die Plattform besteht aus vier getrennten Grenzen:

1. Historisches wissenschaftliches Archiv: ursprüngliche Daten/Code/Protokolle
   bleiben erhalten; neue Quellen und Ergebnisse erhalten eigene IDs/Verzeichnisse.
2. Externe Evidenz: datierte Primärquellen mit Build,Design,Stichprobe,Endpunkt,
   Rohdatenzugang und Grenzen; Herstellerbeschreibung ist kein eigener Kausaltest.
3. Karriere: ausschließlich die ausdrücklich benannte Testdatei rein lesend
   einfrieren/prüfen. Quellenhash und Struktur beweisen keine native Feldsemantik,
   RNG-Unabhängigkeit oder tatsächliche individuelle Trainingsteilnahme.
4. Nativer Observer: eigener minimaler MIT-Quellpatch/privater isolierter Build,
   keine Veränderung von Spiel-DLL,Originalhost oder fremdem Repository. Neue
   Hostidentität erfordert eigene technische Abnahme vor jeder Leistungsstudie.

## Delegation und exklusive Verantwortung

| Agent | Eigener Branch | Ausschließlicher neuer Arbeitsbereich |
|---|---|---|
| Evidence |codex/night-evidence|docs/night-001/EVIDENCE.md,data/night-001-evidence,gegebenenfalls eigener Evidenzvalidator |
| Career |codex/night-career|research/career_readonly004.py,analysis/audit_career004.py,VALID-004-Protokoll,eigene Tests/Daten/CAREER.md |
| Observer |codex/night-observer|adapters/passive-observer-v1.patch,eigener passiver Reader/Comparator/Tests,VALID-005-Protokoll/OBSERVER.md |
| Director |main|Gemeinsame Koordination,Publikation,NativeLease/Seeds/Budgets,native Ausführung und Integration |

Maximal drei Fachagenten parallel,danach unabhängiger Review in separatem Bereich.
Keine parallelen Registerschreibzugriffe. Nur Director darf native Versuche starten.
Agents dürfen keine eigenständigen Host-/Spielstarts oder Kalenderadvances ausführen.

## Aktuelle reale Beobachtungen

Das laufende FM27-Fenster wurde über den Computer-Use-Skill gefunden. Zwei
zulässige Bildaufnahmeversuche scheiterten mit `FrameArrived timed out` bzw.
`window capture timed out`. Keine blinden Tastatur-/Mauseingriffe.
Die ausdrücklich benannte Testdatei existiert und war147.130.636Bytes groß,
letzter Schreibzeitpunkt14.11.2026 18:07:38lokal. Dies belegt eine Datei,
noch nicht die aktive UI-Identität oder deren aktuelle ungespeicherte Zustände.
Andere private Karrieren werden nicht geöffnet. Privates Spielmaterial bleibt lokal.

## Ressourcen, Registrierung und Stopregeln

Ein eigener äußerer `NightBudget` ergänzt die inneren Studienbudgets:

- Unverrückbare Deadline23:00UTC. Keine neue native Operation am oder nach
  diesem Zeitpunkt;fünf Sekunden werden zur Prozessbeendigung reserviert.
- Höchstens1800s kumulierte beaufsichtigte Childzeit über sämtliche neuen
  nativen Studienprozesse,konservativ inklusive Vorbereitung/Audits im Child.
- Gemeinsame Obergrenzen192technische Versuchsplätze und2048Hauptmatches.
  Das sind **keine geplanten oder freigegebenen Hauptserien**;jede Studie
  benötigt weiterhin einen konkreten kleineren Vertrag und eigene neue Seeds.
- Gemeinsame NativeLease,ein nativer Supervisor,maximal4Engineworker und
  höchstens90s ohne Fortschritt. Keine Wiederholung abgeschlossener oder
  unterbrochener Phasen,keine Budgetrückerstattung,kein Ersatzseed.
- Der erste Observervorschlag ist lediglich eine technische A/A-Abnahme mit
  höchstens16Vollmatches plus Negativproben;keine automatische MECH-002-Hauptserie.
- Karriere-Reader rein lesend,maximal180s je dokumentiertem ersten Coveragepass,
  mit Prozess-/Speicherüberwachung. Kalenderadvance erst nach eigenem technischen
  Vertrag und tatsächlich erfüllten Reader-/Identitäts-/Eingabe-/Expositionsgates.

Der äußere Budgetbaustein ist allein kein globaler OS-Lock. Jeder konkrete neue
Runner muss unter eigener Lease und eigenem Studienbudget integriert werden.
Vor nativen Hauptmatches: veröffentlichte Hypothese,Eingaben,Analyse,Seedreservierung,
native Technik,unabhängiger Review und erfolgreicheCI. Fehler stoppen den Zweig;
andere unabhängige Vorarbeiten können fortgesetzt werden. Holdouts bleiben unangetastet.

## Forschungsfragen und Interpretation

Erster Schwerpunkt ist Messbarkeit statt massenhafter Wiederholung unklarer
Kontraste: passiv tatsächliche Zustände nach Vorbereitung/erster Fortschreibung
erfassen,die echte Testkarriere quellengebunden inventarisieren und aktuelle
FM27-Evidenz von übernommenen FM24/26-Rankings trennen.

Neue Leistungsversuche werden nur mit eigenem vorab veröffentlichtem Design
ausgewählt. Mögliche neue Faktoren sind Stamina×Pressing,positionsabhängige
Ausgangsniveaus und OOP-/Rollenmechanismen;keiner davon ist durch dieses Dokument
bereits zur Simulation freigegeben. Keine globale Meta-/Karrierebehauptung aus
synthetischen Fixturetests,Herstellertexten oder fremden Punktschätzern.

Nach jedem validierten Meilenstein Tests,Diff,Archiv-/Veröffentlichungsschutz,
Commit/Push/CI. Zum Zeitende geprüften Erkenntnisstand,Blocker,Ausfälle und echte
Laufzahlen berichten;keine unfertigen oder bloß geplanten Ergebnisse erfinden.

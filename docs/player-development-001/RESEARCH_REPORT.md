# Spielerentwicklung001 – abgeschlossener Forschungsbericht

15.11.2026 · zwei neue Auswertungen: ein kontrolliertes Rollenexperiment und
eine retrospektive CA-Exportdiagnose. **4.096 wissenschaftliche Native-Matches,
512 unabhängige Seedblöcke; zusätzlich109 öffentliche GK-Exportprofile.**
Keine Karrierefortschreibung, keine Wiederaufnahme alter terminaler Studien.

## Was wissen wir jetzt zusätzlich?

**Rolleninteraktion:** Beim selben ST verändert DLF gegenüber CF den xGD-Nutzen
von JR-Roh60→80 im gleichgewichteten Mittel zweier Gegner um **+0,031461**,
95-%-KI **[−0,081658;+0,144580]**,p=0,585028. Bootstrap
[−0,081990;+0,143865]. Das grenzt große mittlere Interaktionen außerhalb der
vorab±0,15 im Testkontext ein. Kleinere Effekte und größere gegnerspezifische
Unterschiede bleiben möglich. Kein allgemeiner Rollensieger. Die volle Breite
0,226238 verfehlt das gewünschte Präzisionsziel≤0,20. Kein Holm6-Sekundärnachweis.
[Vollständige Rollenresultate](ROLE_ATTRIBUTE_RESEARCH.md).

**CA-Proxy:** Aus109bereitgestellten GK-Profilen wurden80Trainings- und29fest
getrennte diagnostische Testspieler gebildet. Gewichteter OLS-Summenproxy:
Holdout-MAE **1,606** gegen **4,630** einer gleich komplexen ungewichteten OLS.
MAE-Abstand **−3,024**,bedingtes95-%-Spielerbootstrapintervall
**[−4,139;−1,908]**. RMSE2,010,Bias+0,845 exportierteCA-Punkte. Getrennter
OLS-Löser bestätigt die Koeffizienten. Das ist eine erfolgreiche begrenzte
Exportdiagnose, **keine identifizierte echte CA-Kostenfunktion**.
Der Quellautor kannte bereits alle109Profile; Build-/Save-/UI-Provenienz
ungeprüft, beobachteteCA15–118. Kein neuer unabhängiger Bestätigungskorpus,
kein Feldspieler-/Elite-/Langzeittransfer. [CA-Bericht](CA_EFFICIENCY.md).

## Antworten auf die acht Forschungsfragen

| Frage | Tatsächliche Antwort | Evidenzstatus |
|---|---|---|
| 1. Größte Matchleistung pro verbrauchtemCA? | Unbekannt. Weder die Referenztabelle noch der GK-Exportproxy identifizieren echten marginalen Verbrauch. | Unbekannt; begrenztes Kostenproxy-Modell |
| 2. Nichtlineare CA-Kosten? | Nicht identifiziert. Konstante Tabellenwerte oder eine lineare Querschnittsanpassung beweisen keine gleichen Kosten8→9/17→18. | Unbekannt |
| 3. Rollenabhängig optimale Profile? | CF/DLF×JR-Interaktion im geprüften Setting eingegrenzt; keine vollständigen optimalen Profile. Bedingte JR-Effekte deskriptivCF+0,112/DLF+0,144xGD. | Experimentell eingegrenzt im Testkontext |
| 4. Wahrscheinlichkeit,PA zu erreichen? | Keine kalibrierte Quote/Verteilung. Auffindbare Progression-Factor-Seite ist von2020; kein FM27-Codebeweis daraus. | Unverifiziert/unbekannt |
| 5. Effizientestes Training? | Keine kausal abgesicherte neue Rangfolge. Communitypakete und eigene historische Einzelsaveversuche reichen nicht. | Extern berichtet/historisch explorativ |
| 6. U19 gegenüber Profis? | Alte Kohorten zeigen unterschiedliche Rohentwicklungen, aber Alter,Plan,Horizont und Karriere sind nicht kausal getrennt. | Beobachtungsbasiert, Kausalität unbekannt |
| 7. Besserer Meta-Score durch CA-Verteilung? | Nicht nachgewiesen. Proxy sagt ExportCA besser voraus; das ist keine Matchprognoseverbesserung. | Szenario modelliert; Outcomevalidierung fehlt |
| 8. Öffentliche Resultate bestätigt/widerlegt? | Nahezu lineare GK-Exportbeziehung in einem retrospektiven Split nachvollzogen; kein unabhängiger neuer Korpus. Positive bedingte JR-Schätzungen sind mit bestehender Evidenz vereinbar. Keine allgemeine externe Attribut-/Trainingsaussage widerlegt. | Begrenzte Nachrechnung, keine universelle externe Replikation |

## Design, tatsächliche Ausführung und Unsicherheit

PD-ROLE-001:2Rollen×2JR-Rohwerte×2Seiten×2Gegner×256neueSeeds je Gegner.
Ein identitätskonstanter ST, feste Position/OOP und alle übrigen Attribute,
Profile,explizitenPI sowie Management konstant. Rollenpaket inklusive
intrinsischer Anweisungen; keine isolierte Einzelmechanik. NominaleCA120
konstant, reale Kostengleichheit nicht behauptet. Keine neue UI-Skalenkalibrierung.
Seiten im Seed gemittelt, zwei feste Kontexte je1/2, Welch95 und stratifizierter
20.000-Block-Bootstrap. Ein Primärtest und eine vollständige Holm6-Familie.
Keine Interim-Leistungsanalyse, Auswahl, Ersatzseeds oder Fallzahlerweiterung.
[Unveränderte Vorregistrierung](../../experiments/PD-ROLE-001.md).

Tatsächlich32Technikmatches/16exakteA/A plus erwartete Exit108-Negativprobe;
alle16Inputzellen abgenommen. Je Hauptmatch3.174Attribute,1.058Profilfelder,
44Phasenzellen/748PI-Gruppen und Actor-/Phasen-/Seedbindung nativ geprüft.
Nach Cleanup erneut sämtliche unveränderten Originalbelege geprüft. Separate
skalare Rekonstruktion aller sieben formalen Welchschätzer und Holm6 stimmt;
gleicher Analyst, kein unabhängiger menschlicher Gutachter behauptet.
**0Ausfälle,Retries,Ersatzseeds,Ausschlüsse,fehlende Messwerte oder unbegonnene
Jobs.** Keine Komprimierung,Verschiebung oder Löschung laufender Rohbelege.

4.129nativeAufrufe=4.128volleSimulationen+1erwarteteNegativabweisung.
4.096wissenschaftliche Matches verbrauchen die gesamte Programmobergrenze.
Maximal4kalteClaims, exklusiveNativeLease und unverändertesJob3-Containment.
Engine-PID-Peak nicht separat gemessen. Beaufsichtigte Phasenzeit3441,182s
(57,353min); nicht die ganze Sitzung und ohne anschließenden Offline-Rohaudit.
Alle nativen Phasen innerhalb der festen Deadline.2,240GBOriginalbelege lokal
erhalten, nur kompakte erlaubte Messungen und Hashes öffentlich. Lease frei,
keine laufenden nativen Jobs oder Hintergrundfortsetzung.
[Budget/Abrechnung](../../data/player-development-001-role/execution-provenance.json).

PD-CA-001:109/109zulässige Zeilen,0Duplikate/Missing/Ausschlüsse,80/29feste
Spielertrennung. OLS mit zwei Parametern je W/U, konstantes Trainingsmittel
als weitere Baseline.20.000gepaarte Holdoutspieler-Bootstrapzüge; Intervalle
bedingt auf Training/Split, keine Save-/Vereinscluster- oder Trainingsunsicherheit.
Rohprofile/Namen/IDs bleiben außerhalb des öffentlichen Forschungsarchivs.
[Protokoll](../../experiments/PD-CA-001.md) ·
[alle Ergebnisse](../../data/player-development-001-ca/profile-diagnostic.json).

## Warum keine Karriere-Pseudostudie?

Die Entscheidung gegen TRAIN/PA-Karriereausführung fiel im ersten
Machbarkeitscheck, deutlich vor Minute45. Individuelle Teilnahme, tatsächlich
wirksame Fokus-/Coach-/Intensitätszuordnung, Verletzungsintervalle und unabhängige
Karriere-Zufallszustände fehlen. Kein ausdrücklich erlaubter isolierter
Pilotkorpus mit diesen Belegen vorliegend. Keine privaten Saves geöffnet oder
geändert,0Advances/Arme/Armwochen. Statt Readerreparatur begann die neue
Native-Hauptserie rund16Minuten nach Missionsstart.
[PA-Evidenz](PA_DEVELOPMENT.md) · [Trainingsvergleich](TRAINING_EVIDENCE.md).

## Meta-Score2.0: getrennte Komponenten, kein Scheinerfolgswert

[Maschinenlesbares Komponentenmodell](../../research/meta_score_v02_components.json):
Current Performance enthält die gemessene lokale Rolleninteraktion samt
Unsicherheit; Development Potential und Training Efficiency bleiben unbekannt.
Die getrennte CA-Exportdiagnose ist kein kalibrierter Leistungsbeitrag.
Meta-Scorev0.1 und seine Gewichte bleiben unverändert. Kein validierter
kombinierter Score, keine Erfolgschance und kein behaupteter zusätzlicher
Matchprognosenutzen gegenüberCA,Attributmittel oder öffentlichen Gewichten.
Der integerbasierte Referenzbudget-Optimierer bleibt ausschließlich Szenariomodell.

## Reproduktion, Prüfung und Veröffentlichung

Tatsächliche DLL:FileVersion27.0.1,ProductVersion27.0.1+2503222,
SHA2568c6971ce…; Tactics Labv1114.6/91f2eba, passiverObserver58e05a46.
Python3.12.10,NumPy2.3.5,SciPy1.16.3; installierterReaderfmsave0.9.0,
kein Saveexperiment daraus. Vollständige Hashes/Quellen in
[source-audit.json](source-audit.json) und [Inputmanifest](../../data/player-development-001-role/inputs.json).

466lokale Testfälle:463bestanden,3erwartete historische Skips; zusätzliche
5Analysetests bestanden. Vollständige Originalbeleg- und skalare Ergebnisprüfung
bestanden. Abbildung visuell geprüft. Keine geschützten Assets, Spielstände,
DLLs,Binaries,Zugangsdaten oder Spieleridentitäten veröffentlicht.

```powershell
.venv/Scripts/python.exe analysis/analyse_playerdev001.py
.venv/Scripts/python.exe analysis/review_playerdev001.py role
.venv/Scripts/python.exe analysis/render_playerdev001.py
.venv/Scripts/python.exe -m unittest discover -s tests -v
```

CA-Diagnose zusätzlich über die unveränderlich referenzierten Originaldateien
und den ausführbaren Befehl im CA-Bericht. Native Wiederholung benötigt legale
lokale Ressourcen und eine neue eigene Freigabe; kein Neustart dieses Vertrags.

| Abschnitt | Commit | Exakte erfolgreiche CI |
|---|---|---|
| Rollen-Vorregistrierung |197527d|[43734775642](https://github.com/Matchekk/FM-27-Research/actions/runs/43734775642)|
| Native Technik/Mainfreigabe |927f2f5|[43735167774](https://github.com/Matchekk/FM-27-Research/actions/runs/43735167774)|
| Evidenz-/Komponententrennung |fae459c|[43735784973](https://github.com/Matchekk/FM-27-Research/actions/runs/43735784973)|
| CA-Protokoll |8f26064|[43736217032](https://github.com/Matchekk/FM-27-Research/actions/runs/43736217032)|
| CA-Ergebnis |1b83ce3|[43736644402](https://github.com/Matchekk/FM-27-Research/actions/runs/43736644402)|

Der vollständige wissenschaftliche Archivcommit und seine erfolgreiche CI
werden in [publication.json](publication.json) gebunden. Branch
`codex/player-development-001`; Integration nach main nur mit erfolgreichen
Prüfungen, ohne Force-Push. Ausgangsstand3cd4317 war sauber und identisch mit
origin/main nach Fetch; alle angeforderten Einstiegspfade existierten.

[Nächste maximal drei Experimente](NEXT_EXPERIMENTS.md) ·
[alle Rollenresultate und Abbildung](ROLE_ATTRIBUTE_RESEARCH.md) ·
[Quellen-/Neuheitsprüfung](LITERATURE.md).

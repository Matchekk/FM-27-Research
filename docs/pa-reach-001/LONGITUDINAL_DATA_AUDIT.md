# Datenherkunft und Beobachtungsdauer

**Eine Karriere, vier Save-Spieltage, 19 Tage.** 95.197 verschiedene Identitäten liefern 376.045 abgeglichene Spieler-Zeitpunkte. 93.113 sind an allen vier Tagen messbar. Von den 93.161 Ausgangsspielern fehlen 48 am letzten Tag. 2.036 Identitäten erscheinen erstmals nach der Baseline. Datengrundlage ist ausschließlich der Kontrollarm A von TRAIN-005. Der identische B-Start, der weitere bytegleiche Lesesnapshot und ein nativer Tag-14-Abzug ohne hier gepaarten Save ergeben keine zusätzlichen unabhängigen Karrieren. [Vorversuch](../player-development-004/RESEARCH_REPORT.md) · [Manifest mit je zwei Quellhashes pro Tag](../../data/pa-reach-001/manifest.json)

| Spieltag | Save-Records | Native Referenz | Kein passender nativer UID-Eintrag | Ohne schließende ID | Geburt fehlt/weicht ab | Akzeptierte CA/PA |
|---|---:|---:|---:|---:|---:|---:|
| 16.01.2027 | 113.815 | 93.168 | 20.646 | 1 | 7 | 93.161 |
| 19.01.2027 | 113.146 | 93.597 | 19.548 | 1 | 14 | 93.583 |
| 23.01.2027 | 113.567 | 94.212 | 19.353 | 4 | 58 | 94.152 |
| 04.02.2027 | 113.734 | 95.209 | 18.523 | 4 | 58 | 95.149 |

Die Differenzen vor dem Geburtsabgleich betreffen auch die Reichweite des nativen Inventars. In den letzten beiden Referenzinventaren liegen je zwei IDs außerhalb des Save-Abgleichs. Unter den korrekt zugeordneten Paaren gab es keinen CA-/PA-Mismatch. Dateinamen zweier rotierter Sicherungen bezeichnen den Tag der Ablösung. Der eingebettete Kalendertag und die ältere, gehashte In-Game-Messung bestimmen die Zuordnung. Die finale Arbeitskopie wurde vor dem Lesen mit dem Hash im Shutdown-Protokoll abgeglichen. Die historische Intervention blieb pausiert. [Stoppbeleg](../../data/player-development-004/shutdown.json) · [Vollständige Abrechnung](../../data/pa-reach-001/summary.json)

### Weitere Datenwege und Builds

- Der installierte Client ist laut lokalem Game-Log 27.1.0+2505117 (Steam-Build 26620374). Die vier Save-Header und die TRAIN-005-Referenz gehören zu 27.0.1+2503222. Ein weiterer TRAIN-001-Forschungsstart trägt 27.0.0+2493426. TRAIN-001 besitzt auch echte Wochenverläufe auf seinem eigenen Build. Gleiche Ableger und unterschiedliche Trainingspläne würden die unabhängige Fallzahl künstlich erhöhen. [TRAIN-001](../../experiments/TRAIN-001-karriere.md)
- In den überprüften lokalen Scout-Forschungsartefakten enthält die größere Historie 124.067 Spieler an einem Datum. Zwei QA-Historien umfassen je ein Datum. Die Exportablage enthält unter anderem Tabellenstand und Scoutinglisten. Die Sportstatistiken und einmaligen Profile liefern keine historischen CA-Endpunkte. Persönliche Karriereoriginale sind nicht Teil der Stichprobe.
- Im geprüften Fork (App 1.6.0) speichert die Historie CA, PA und Marktwert als Delta je Managerkennung, fasst nach 120 Daten den ältesten Stand zusammen und entfernt beim Zurückladen spätere Punkte. Ein Managername identifiziert unabhängige Karriereableger nicht sicher. Die neue private Erfassung schreibt in eine eigene Datenbank. [Historiencode](https://github.com/Matchekk/FMSuperScout/blob/977ecefe623a3d4081871a0f558ab12d9bce850d/app/server.js)
- Caiograco hat einen relevanten externen Mehrsaisonbestand beschrieben. Im geprüften Thread stehen Gruppentabellen, kein zugängliches, einwilligungsgeklärtes Spielerpanel für unabhängige Modellvalidierung. Der frühere externe Editortest hat manipulierte Ableger über 33 Tage. Saisonstatistiken aus den Readern enthalten keine belegte CA-Historie. Die Suche nach einem verwendbaren externen Testkorpus blieb ohne Treffer. [FM-Arena](https://fm-arena.com/threads/the-hidden-variable-probabilistic-cap-to-ca-growth.115/#post-375) · [Früherer Datenaudit](../player-development-002/PA_ANALYSIS.md)
- fmsave 0.14.1 führt 27.0.0+2486695 mit vollständiger Layoutregistrierung. Auf unserem historischen Build warnt es vor geliehenen Layouts. Für 27.1.0+2505117 gibt es unter anderem einen expliziten Finanzblock. CA und PA sind im generischen Ability-Modell weiterhin als unbestätigt gekennzeichnet. shlk20/fm27-scout-code 1.6.1 beschreibt die Spielerstruktur für 27.0.0+2486695/+2493426, 27.0.1+2494687/+2503222 und 27.1.0+2505117 (Schema 4000). Das Dokument nennt CA+0, PA+2 und Reputation+8. Es qualifiziert +7 nicht semantisch. Der Rust-Reader wurde als Quelle geprüft. Der unabhängige lokale Referenzweg war der archivierte native Readback. [fmsave-Layout](https://github.com/rhiever/fmsave/blob/9dd60521042e9c5a33a14725da59023eb3ad8dfa/src/fmsave/_layouts/fm27_27_1_0.py) · [Feldstatus](https://github.com/rhiever/fmsave/blob/9dd60521042e9c5a33a14725da59023eb3ad8dfa/src/fmsave/models/players.py) · [Rust-Layout](https://github.com/shlk20/fm27-scout-code/blob/7fb12175f59b4d41b4418bf0378c3855a5bab4bd/docs/fm27-layout.md)

### Reproduzieren und weitere Spieltage erfassen

Python 3.12.10 und fmsave 0.14.1 wurden für diese Runde verwendet. Je Spieltag sind die private Wegwerfkopie, das zeitgleiche native Referenzinventar, deren eingefrorene Hashes sowie die Herkunft der Karriere erforderlich. Folgendes Beispiel verwendet Platzhalter für die privaten Eingaben.

```text
python -m pip install fmsave==0.14.1
python analysis/pa_reach_capture.py local/panel.sqlite data/pa-reach-001/manifest.json 2027-01-16 SAVE INVENTAR
python analysis/pa_reach_summary.py local/panel.sqlite TRAIN005-A
```

Die Tabelle ist pro Karriere und Spieltag transaktional und unbegrenzt fortschreibbar. Ein wiederholter Import derselben Kombination wird abgewiesen. Zur Prüfwiederholung eine frische private Datenbank verwenden. Die Sicht `research_panel` hält die erste PA pro Karriere, ID und Geburt fest. Bestätigte Klubkennungen stammen aus zwei Quellen. Ungeprüfte Persönlichkeit, Anlagen, Vertragsdaten, Leihstatus, Minuten, Verletzungstage und semantische Stufe bleiben SQL-NULL. Für spätere Landmark-Prognosen wird die Ziel-PA am jeweiligen Prognosetag erneut fixiert. SQLite-Dateien, native Inventare und Einzelprofile verbleiben privat. [Erfassungsprogramm](../../analysis/pa_reach_capture.py) · [Aggregatauswertung](../../analysis/pa_reach_summary.py)

Die private Panelsicht ab Schema 3 gibt auf 27.1.0+2505117 den gespeicherten Faktor 0–5 aus. Nur Werte 1–5 gelangen in das Stufenmerkmal. Bei anderen Builds bleibt das Merkmal fehlend. Die Migration der Sicht erhält die aufgenommenen Rohzeilen. [Nativ benannter Wert und Feldanker](NAMED_PROGRESSION_READBACK.md)

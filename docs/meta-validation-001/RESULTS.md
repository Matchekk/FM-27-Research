# Ergebnisse · META-VALIDATION-001

**Die Matchleistung der beiden Spielerwahlregeln ist offen.** Es wurden 16 natürliche Matchenden auf dem Zielbuild gemessen. Alle gehören der vorregistrierten technischen Abnahme für B an. Beide wissenschaftlichen Serien endeten vor ihrem ersten Match.

| Endpunkt | Wissenschaftliche Stichprobe | Schätzung / Unsicherheit |
|---|---:|---|
| A · Auswahlgewinn G und vorgegebenes V | 0 Konfliktpaare, 0 repräsentative Paare, 0 Matches | Beide Schätzer und 95-%-Intervalle fehlen |
| A · CB gegen ST, sekundäre Spielerwahlmetriken | 0 getestete Spielerpaare in jeder Gruppe | Keine Positionsdifferenz oder Trefferquote schätzbar |
| B · Krümmung C bei JR 7/9/16/19 | 0 wissenschaftliche Seedblöcke, 0 von 128 bedingt geplanten Pilotmatches gestartet | C, Steigungen und Konfidenzintervalle fehlen |

## Tatsächliche technische Endstände

Je Tabellenzelle gab es zwei identische Wiederholungen. Die Tore sind aus Heimsicht angegeben. Alle acht Zellen teilen denselben Technikseed, denselben Gegner und dieselbe Seite.

| Heimstarter | Roh-JR 35 | Roh-JR 45 | Roh-JR 80 | Roh-JR 95 |
|---|---:|---:|---:|---:|
| ST, Slot 10 | 1:0 | 0:1 | 2:0 | 0:1 |
| CB, Slot 2 | 0:1 | 3:1 | 1:1 | 0:1 |

Die ursprünglichen xG für beide Teams, Tore, Tick und Hashes stehen je Aufruf in den [16 technischen Messzeilen](technical-matches.jsonl). Punkte und xGD lassen sich aus Toren bzw. xG je Seite ableiten. Aus diesen Wiederholungen einen Wirksamkeitskontrast oder eine Powerrechnung zu erstellen, würde die fehlenden unabhängigen Blöcke verdecken. Der technische ST hatte auf dieser Position ein Rating von 1/20. Der Abgleich der vier Rohstufen mit der Karriereanzeige blieb unvollständig. [Abnahme und Abweichungen](MATCH_VALIDATION.md)

Die Grenze von 0,05 GD pro Match bezieht sich auf die tatsächlich gewählte Option (G). Die Paarstreuung und die erreichbare Präzision bei der Obergrenze von 1.024 Hauptmatches konnten nicht gemessen werden. Es gibt weder einen Überlegenheits- noch einen Äquivalenztest. [Protokoll](RESEARCH_DESIGN.md) · [Maschinenlesbare Ergebnisse](results.json)

Öffentliche Nachrechnung: `python analysis/review_meta_validation001.py`. Nachrechnung aus den lokalen Originalen: derselbe Befehl mit `--private local/meta-validation-001/technical`. Gezielte Tests: `python -m unittest discover -s tests -p test_meta_validation001.py`. Die Funktionstests der statistischen Definitionen verwenden eigene kleine Kontrollbeispiele.

Die private Kontrollrechnung rekonstruierte zusätzlich alle neun dokumentierten Skalenvergleiche aus dem gehashten Originalsave, UniqueId, Spieltag und den drei Original-Anzeigefeldern. Das schließt auch die maskierten Antworten ein. Unter Python 3.12.10 verliefen 485 Repositorytests mit drei vorgesehenen Skips sowie fünf Analysetests erfolgreich. Beim ersten lokalen Lauf führten fehlende Werte in der geerbten Git-Prozesskonfiguration zu neun Testfehlern. Die Wiederholung mit bereinigter Git-Prozessumgebung bestand. Der Produktionsstand bestand separat alle 97 FMSuperScout-Tests.

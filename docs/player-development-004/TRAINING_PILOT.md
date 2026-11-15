# TRAIN-005 – auf Nutzerwunsch pausierter Einpaarpilot

Vertrag: [TRAIN-005-INGAME](../../experiments/TRAIN-005-INGAME.md).
Eine Ausgangskarriere, ein Spieler, zwei geplante Arme; keine unabhängigen
Karriere-Replikate. Ziel: 16.01. bis 13.03.2027, je 56 Kalendertage.

Publizierter Messzwischenstand: A an Tag 0, 3, 7, 14 und 19. Ein gestarteter
Kalenderarm, kein abgeschlossener Achtwochenarm. B wurde als technische
Fokusprobe verändert und separat zurückgelesen, aber noch nicht fortgeschrieben.
Der endgültige B-Lade-/Fokus-/Speicherzyklus steht aus. Keine stille Wiederholung
eines ungünstigen Trainingsergebnisses.

| A-Kalendertag | Antritt | Tempo | STORED_CA | PA | Kondition | Schärfe |
|---|---:|---:|---:|---:|---:|---:|
| 0 | 14 | 14 | 134 | 160 | 64 | 99 |
| 3 | 14 | 14 | 134 | 160 | 92 | 99 |
| 7 | 14 | 14 | 134 | 160 | 98 | 99 |
| 14 | 14 | 14 | 135 | 160 | 100 | 99 |
| 19 | 14 | 14 | 135 | 160 | 96 | 97 |

An Tag 19 sind alle 47 verwertbaren Attributanzeigen gegenüber Tag 0 gleich.
Das ist tatsächliche Karriereentwicklung auf zwei unterschiedlichen Messskalen:
gespeicherte CA +1, gerundete Attributanzeigen noch unverändert. Weder die
unsichtbaren Attributanteile noch marginale CA-Kosten sind damit identifiziert.

Primärkontrast B−A: **null / NOT_MEASURED**. Die Nulländerung der beobachteten
A-Quickness bis Tag 14 ist kein gemessener Nullunterschied zwischen zwei Armen.
Sekundäre Minuten konnten an Tag 14 als Saisonwert ausgelesen werden; eine
Baseline dafür wird aus der unveränderten gemeinsamen Ausgangskopie ergänzt,
bevor ein Pilot-Minutenkontrast berechnet wird. Historische Verletzungstage
werden nicht als neue Pilot-Ausfalltage ausgegeben.

Management: unveränderte Trainingspolitik und automatische Intensitätswahl;
Auto-Auswahl plus vom Spiel angebotenes Sofortergebnis für Pflichtspiele.
Transfers ablehnen, neue Vertragsforderungen absagen, Vereinsphysio bei
Verletzungen; Auslosungsdarstellung überspringen. Andere Entscheidungen zunächst
inspizieren. Reine Nachrichten dürfen über die angebotene „Alle gelesen“-Aktion
markiert werden; notwendige Antworten bleiben eigene, protokollierte Eingriffe.
Nicht jede Trainingsteilnahme, Reiseersetzung oder Belastungseinheit ist beobachtet.

Ein wegen veränderter Kaderreihenfolge zunächst falsch gebundener Wochenabruf
wurde durch die Identitätsprüfung verworfen, vor Annahme eines Spielerendpunkts.
Die anschließende Messung löste P001 anhand seiner stabilen privaten Identität
neu auf. Technische Fehlversuche sind erhalten; keine zusätzlichen Spieler oder
Karrierepaare dadurch erzeugt.

[JSONL](../../data/player-development-004/observations.jsonl),
[CSV](PLAYER_DEVELOPMENT.csv), [Auswertung](../../data/player-development-004/analysis.json).
Reproduktion: `python analysis/training_ingame005.py`; gezielte Prüfungen:
`python -m unittest tests.test_training_ingame005 -v`.


## Gesicherter Stopp vor dem Ausschalten

Der Nutzer hat die Arbeit zum Ausschalten ausdrücklich unterbrochen.
A ist am **04.02.2027 (Tag 19)** regulär gespeichert; Dateihash
`c67eab6aea1642887d83c2e6955841235889d31be45927110239b69ec02c279c`.
B und Original sind unverändert. FM wurde nach der Speicherprüfung beendet,
kein Karrierecontroller läuft weiter. Temporäre Loader-Konfiguration und
installierte Labhost-DLL sind bytegenau restauriert. Der Quellcode und sämtliche
privaten Belege sind gespeichert. [Maschinenlesbarer Stoppnachweis](../../data/player-development-004/shutdown.json).

Bei später ausdrücklich gewünschter Fortsetzung A bei Tag 19 fortsetzen,
nicht wiederholen; B bleibt der Startarm. Vor B weiterhin Fokus-/Speicher-
Ladeabnahme durchführen. Kein automatischer Wiederanlauf. Die 56-Tage-Studie
bleibt unvollständig; der Stopp ist keine wissenschaftliche Armverwerfung.

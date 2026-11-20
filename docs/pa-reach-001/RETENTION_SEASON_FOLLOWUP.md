# Retentionszweig nach dem ersten Quartal

Diese Fortsetzung verwendet dieselbe im März 2027 fixierte Karriere und FM27 `27.1.0+2505117`. Der erste 92-Tage-Abschnitt und die Prüfung des Saisonübergangs stehen im [Quartalsbericht](RETENTION_FIRST_QUARTER.md). Die folgenden Stichtage wurden im Retentionszweig gemessen. Alle Personen- und Quellenpfade bleiben privat.

## 30. September 2027

Vom 30. Juni bis zum 30. September vergingen **92 Spieltage**. 90.130 Personen sind im nativen CA-/PA-Abgleich gepaart. Von 7.623 im nativen Endinventar fehlenden Juni-Identitäten bleiben 7.323 im strukturellen Weltsave eindeutig auffindbar. 300 fehlen in beiden Messwegen. Unter den nativen Paaren änderte sich CA bei 30.732 und der gespeicherte Faktor bei 10.105. PA blieb bei allen gleich. Der Septemberstand enthält 111.788 akzeptierte strukturelle und 91.991 separat CA-/PA-geprüfte Spieler. Die native Abdeckung unterscheidet sich zwischen den Stichtagen. [Messmanifest September](../../research/pa-reach-001/manifests/zubieta-retention-september.json)

Unter den 72.425 am 30. Juni geeigneten Feldspielern unter 28 sind 67.713 gepaart und 4.712 am Endtag nicht nativ bestätigt. Für die Spieler mit mehr als 30 CA-Punkten Ausgangslücke gilt folgende Bilanz.

| Alter am 30. Juni | Spieler | Mittlere ΔCA | Median | Standardabweichung |
|---|---:|---:|---:|---:|
| Unter 18 | 13.133 | +1,8261 | +1 | 2,4515 |
| 18–20 | 3.962 | +1,7322 | +1 | 2,0253 |
| 21–23 | 1.365 | +0,7678 | 0 | 1,5758 |
| 24–27 | 372 | +0,0699 | 0 | 1,3159 |

Der 184-Tage-Vergleich mit dem 30. März umfasst 76.284 native CA-/PA-Paare. Bei gleicher Lückendefinition beträgt der mittlere gemessene Zuwachs +6,0403 CA für U18 (n=4.416, Median 6, SD 4,6458) und +0,5030 CA für 24–27-Jährige (n=328, Median 0, SD 1,6361). Die Altersgruppen der beiden Fenster werden an ihrem jeweiligen Anfang bestimmt. Die eingetretenen und fehlenden Spieler unterscheiden sich zwischen den Fenstern. [Messmanifest September](../../research/pa-reach-001/manifests/zubieta-retention-september.json)

Für 68.947 U28-Feldspieler sind alle zehn ausgewählten Anzeigeattribute am 30. Juni und 30. September bestätigt, 1.482 qualifizierte Baseline-Profile fehlen beim Folgeabgleich. In dieser Auswahl legten 19.674 Spieler in CA zu. Durchschnittliche Änderungen auf der 1–20-Skala für alle bzw. für die Spieler mit CA-Gewinn betragen bei Antritt +0,0205 bzw. +0,1429, bei Tempo +0,0402 bzw. +0,1780, bei Sprunghöhe +0,0456 bzw. +0,1197 und bei Stärke +0,0971 bzw. +0,2891. Beim Abschluss sind es −0,0237 bzw. +0,0556. Die übrigen fünf Attribute, die Streuung und die Ausfälle je Stichtag stehen im Manifest. [Messmanifest September](../../research/pa-reach-001/manifests/zubieta-retention-september.json)

Der unabhängig von den Spielerminuten gelesene Save-Spielplan liefert einen eigenen Beleg für den Saisonübergang. `fmsave` 0.14.1 las für Team-Slot 0 des eigenen Klubs ab dem 1. Mai am 30. Juni und am 2. Juli jeweils acht gespielte Begegnungen mit Saisonstartjahr 2026. Am 30. September sind zusätzlich neun gespielte und 38 ausstehende Begegnungen mit Saisonstartjahr 2027 sichtbar, sowie drei gespielte ohne eingetragenes Saisonstartjahr. Damit ist die neue Saison im eigenen Klubkalender spätestens am 30. September sichtbar. Der exakte Umschlagtag liegt zwischen den relevanten Stichtagen. Die Abgrenzung verwendet die im Save gelesene Team-Slot-Zuordnung und das Feld `season_start_year`. [Messmanifest September](../../research/pa-reach-001/manifests/zubieta-retention-september.json)

## Reproduktion

Der CLI-Aufruf verwendet das private native SQLite-Panel, das private strukturelle SQLite-Panel, das datierte native Eingabemanifest, den gewünschten Endtag und das zugehörige Struktur-Tag. Er prüft Build, Datum und Quellen-Hashes und beschränkt die Auswertung explizit auf die damals verfügbaren Stichtage. Die Identität beim Strukturabgleich verwendet Datenbank-ID und Geburtsdatum für die gesamte Spielwelt.

```text
python research/pa-reach-001/analysis/retention_windows.py <native.sqlite> <struktur.sqlite> <native-input.json> 2027-09-30 ZD-RET-0930
```

Die Attributprüfung ruft `observed_meta.read_scan` für die datierten Save-Tags mit den zugehörigen unabhängigen Scans und Kontextklammern auf. Pro Vergleich werden die qualifizierten Identitäten anhand von Datenbank-ID, Geburtsdatum und Namensprüfung verbunden. Die Ausgangsauswahl sind Feldspieler unter 28. Differenzen werden pro Anzeigeattribut mit Anzahl, Mittelwert, Standardabweichung und Richtung ausgewiesen. Die ausfallsensitive Erhebung gehört zu genau einem Karriereuniversum. [CLI-Auswertung](../../research/pa-reach-001/analysis/retention_windows.py) · [Attributprüfung](../../research/pa-reach-001/analysis/observed_meta.py)

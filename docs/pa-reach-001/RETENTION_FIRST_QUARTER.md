# Erstes beobachtetes Retentionsquartal

Vom 30. März bis zum 30. Juni 2027 vergingen im selben Karrierezweig **92 Spieltage**. Am 2. Juli folgte ein zweiter datierter Save zur Prüfung des Saisonübergangs. FM27 schrieb beide Endstände unter `27.1.0+2505117`. Gehashte, schreibgeschützte Kopien, native CA-/PA-Inventare und die ruhenden Spielkontexte vor und nach den Erfassungen binden die Werte an den jeweiligen Spieltag. Der Zweig folgt der dokumentierten Retentionspolitik, mit delegierter Kalenderfortschreibung nach April und ohne neuen gleich langen Kontrollzweig. [Vertrags- und Laufkontext](CONTRACT_RETENTION.md) · [Messmanifest](../../research/pa-reach-001/manifests/zubieta-retention-june-july.json)

## Altersgruppen und Ausgangslücke

83.716 Spieler sind am 30. März und 30. Juni mit Datenbank-ID, Geburtsdatum, CA und PA eindeutig abgeglichen. Unter 62.047 zu Beginn geeigneten Feldspielern unter 28 liegen für 61.241 beide Endpunkte vor. Die Altersgruppe und PA−CA beziehen sich auf den 30. März. Bei einer Ausgangslücke über 30 CA-Punkten ergeben sich folgende Änderungen.

| Alter am Start | Spieler | Mittlere ΔCA | Median | Standardabweichung |
|---|---:|---:|---:|---:|
| Unter 18 | 4.418 | +2,8017 | +2 | 2,5371 |
| 18–20 | 4.417 | +1,6120 | +1 | 1,8427 |
| 21–23 | 1.411 | +0,6556 | 0 | 1,3886 |
| 24–27 | 426 | +0,2582 | 0 | 0,7081 |

60.201 geeignete Baseline-Spieler haben ein exakt beobachtetes Drei-Kalendermonats-Fenster bis einschließlich zum 28. Geburtstag. Bei 6.480 stieg die CA in diesem Fenster um mindestens drei Punkte. Die Zwischenmessungen tragen zum beobachteten erstmaligen Erreichen der festen Ausgangs-PA bei. 434 Spieler hatten ihre volle Ausgangs-PA bereits erreicht, 45 erreichten sie neu, 60.556 sind rechtszensiert und bei 1.012 wurde der Altershorizont ohne beobachteten Treffer bei lückenhafter Erfassung überschritten. 152 erreichten neu mindestens 95 % der Ausgangs-PA. Die Standardabweichungen beschreiben Spieler in einem Karriereuniversum. Unsicherheit über unabhängige Karrieren und eine individuelle PA-Wahrscheinlichkeit bleiben offen. Exakte 12- und 24-Monatswerte fehlen für diese Baseline. [Endpunktdefinition](../../research/pa-reach-001/analysis/player_endpoints.py) · [Messmanifest](../../research/pa-reach-001/manifests/zubieta-retention-june-july.json)

## Anzeigeattribute im Quartal

59.891 Feldspieler unter 28 am Start haben die zehn für den Feldspielerindex benötigten Anzeigeattribute an beiden Tagen. 3.110 qualifizierte Baseline-Profile fehlen im Folgeabgleich. Die geprüften Paare verwenden eindeutige Identität einschließlich Geburtsdatum und privater Namenskontrolle, übereinstimmende CA/PA und den separaten Vergleich von Scout- und Save-Werten. Die folgende Auswahl beschreibt Veränderung auf der Anzeigeskala 1–20. Das Manifest enthält alle zehn Attribute, Streuungen und Richtungszählungen.

| Attribut | Alle 59.891 Paare | 15.974 Paare mit CA-Gewinn |
|---|---:|---:|
| Antritt | +0,0104 | +0,1094 |
| Tempo | +0,0283 | +0,1466 |
| Sprunghöhe | +0,0109 | +0,0708 |
| Stärke | +0,0875 | +0,2679 |
| Abschluss | −0,0034 | +0,0636 |

Der Abgleich vom 30. April bis zum 30. Juni umfasst 61 Tage, 95.762 native CA-/PA-Paare und 69.296 qualifizierte Attributpaare. Die Attributauswahl nach beobachtetem CA-Gewinn ist deskriptiv. [Attributprüfung](../../research/pa-reach-001/analysis/observed_meta.py) · [Messmanifest](../../research/pa-reach-001/manifests/zubieta-retention-june-july.json)

## Abdeckung und Saisonstatistik

| Spieltag | Strukturell akzeptierte Spieler | Mit nativer CA/PA bestätigt |
|---|---:|---:|
| 30.06.2027 | 112.956 | 97.753 |
| 02.07.2027 | 112.877 | 83.209 |

Von den 13.542 am 30. Juni nativ fehlenden Baseline-Spielern sind 10.440 im gesamten strukturellen Save weiterhin eindeutig vorhanden. 3.102 fehlen in beiden Wegen. Alle 14.581 Juni-Identitäten, die am 2. Juli nativ fehlen, sind weiterhin im strukturellen Save zu finden. Unter den 83.716 nativen Quartalspaaren änderten sich CA bei 24.231 und der gespeicherte Faktor bei 7.283. PA blieb bei allen Paaren gleich. Vom 30. Juni bis zum 2. Juli änderten sich unter 83.172 nativen Paaren CA bei 323 und der gespeicherte Faktor bei 1.087. PA blieb auch dort unverändert. Die Faktorwechsel beziehen sich auf das identifizierte Savefeld. [Feldvalidierung](NAMED_PROGRESSION_READBACK.md) · [Messmanifest](../../research/pa-reach-001/manifests/zubieta-retention-june-july.json)

Zwischen dem 30. Juni und dem 2. Juli können 46.241 explizite Saisonstatistiken derselben Spieler beim selben Team verglichen werden. Bei 560 Paaren fielen positive Einsatz- und Minutenstände gemeinsam auf null. Bei 43.438 blieben die Minuten gleich und bei 2.243 stiegen sie. Bei den 41 gepaarten Spieler-Team-Zeilen des eigenen Klubs gab es keinen Minutenrückgang. Der Zählerneustart ist damit für einen Teil der Spielwelt beobachtet. Der genaue Saisonwechsel des eigenen Klubs bleibt offen. Die Auswertung verwendet Gesamtzeilen, deren Minuten, Starts und Einwechslungen aus den eindeutigen Wettbewerbszeilen nachvollziehbar waren. [Erfassungslogik](../../research/pa-reach-001/analysis/zubieta_exposure.py) · [Messmanifest](../../research/pa-reach-001/manifests/zubieta-retention-june-july.json)

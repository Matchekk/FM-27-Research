# Angekündigte Klubwechsel um den 1. Juli 2027

**22 von 39 Spielern mit vorab angekündigtem und anschließend beobachtetem Wechsel zum genannten Zielklub hatten am 02.07. einen anderen gespeicherten Entwicklungsfaktor als am 30.06.** Bei 14 stieg der Wert, bei acht sank er. CA und PA waren für alle 39 an beiden Stichtagen gleich. Der Befund stammt aus einem Retentionszweig auf FM27 `27.1.0+2505117`. [Abrechnung und Quellhashes](../../research/pa-reach-001/manifests/retention-transfer-0702.json)

| Klubprüfung | Wechsel zum angekündigten Ziel | Stabiler Klub, keine positive Ankündigung in beiden Scans |
|---|---:|---:|
| Eindeutige Übereinstimmung zwischen Scannername und struktureller Save-ID | 22 / 39 | 145 / 70.445 |
| Zusätzlich anderer identitätsgeprüfter Spieler je Klub und Stichtag zur Namensbestätigung | 22 / 39 | 142 / 65.865 |
| Zusätzlich separat nativ bestätigte Klub-ID am 30.06. und 02.07. | 9 / 16 | 64 / 28.128 |

Die Juni-Datei enthält 158 vollständige Ankündigungszeilen. 67 eindeutige Spieler-IDs mit Geburtsdatum haben einen angegebenen Termin vom 30.06. bis 02.07., davon 59 am 01.07. Bei 39 stimmt die strukturelle Zielklub-ID am zweiten Stichtag mit dem angekündigten Vereinsnamen überein und weicht von der Ausgangs-ID ab. Für zehn ist derselbe Klub belegt. Bei 16 fehlt ein hinreichender Spieler- oder Klubabgleich, bei zwei ist die Zielklubauflösung offen. Das angekündigte Datum beschreibt den Plan. Der neue Klub ist am 02.07. beobachtet. Ein exakter Transferzeitpunkt wird durch diese beiden Stichtage nicht identifiziert.

Bei 37 der 39 beobachteten Wechsel begann laut gespeichertem Vertrag im selben Fenster ein Vertrag beim Zielklub. Alle 37 Beginndaten stimmen mit dem angekündigten Transferdatum überein. Bei 33 dieser Verträge entspricht das ausgelesene Ende zusätzlich dem Scannerwert. Bei 21 der 37 wechselt der Faktor. In der stabilen Vergleichsgruppe wechselt er bei 33 von 173 Spielern mit einem im Fenster begonnenen Vertrag beim beobachteten Klub und bei 112 von 70.272 ohne einen solchen strukturellen Startnachweis. Altersgruppen und CA-/PA-Änderungen sind im JSON getrennt ausgewiesen. Die überlappenden Ereignisse und die unterschiedliche Zusammensetzung der Gruppen lassen den isolierten Effekt eines Klubwechsels offen.

Die Identitätsprüfung verwendet Datenbank-ID, Geburtsdatum und einen savebasierten Namensprüfwert sowie den Abgleich von CA/PA mit den unabhängigen Inventaren. Das Ergebnis vergleicht das gespeicherte Feld bei CA+7. Frühere benannte Stichproben identifizieren dieses Feld buildbezogen. Für die beiden Transferstichtage liegen keine zusätzlichen benannten Faktor-Readbacks vor. Ein Neuwurf mit gleichem Ergebnis und die genaue Ursache eines Faktorwechsels bleiben unbeobachtet. [Benannte Feldprüfung](NAMED_PROGRESSION_READBACK.md) · [Reproduktion](../../research/pa-reach-001/analysis/retention_transfer_window.py)

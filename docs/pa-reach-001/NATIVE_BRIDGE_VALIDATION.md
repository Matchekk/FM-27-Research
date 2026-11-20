# Nativer Karrierezugang und Sicherung der Kontrollkarriere

## Messweg

Die laufende Steam-Installation meldete FM27 `27.1.0+2505117`. Auf diesem Build antwortete die vorhandene LabHost-Brücke 0.4.7 auf dem Spielthread auf reine Kontextabfragen. Der Prozess lieferte in derselben Antwort den tatsächlich aktiven Speicherpfad, das Spieldatum, Manager- und Mannschaftsidentität sowie die Zustände für Verarbeitung, laufende Partie und Speichern. Die privaten Protokolle bewahren die vollständigen Werte. Öffentlich erscheinen nur logische Bezeichnungen und Prüfsummen. Die Modulprüfsummen und Maschinenbelege stehen im [Bridge-Manifest](../../research/pa-reach-001/manifests/bridge.json).

Der Build-Filter der Brücke erlaubt für das vorliegende native Modul `context`, `read-properties` und `deck-praise`. Die in TRAIN-005 eingesetzte Kalender-/Speichersteuerung ist für diese Modulversion nicht freigegeben. Wir haben die Arbeitskopien über den regulären Ladedialog geöffnet und neue Speicherstände über die Speicherfunktion des Spiels erstellt. Für den Kalenderpilot rotierte die eingebaute, zeitlich begrenzte Urlaubsfunktion die Spielwelt mit delegierten Traineraufgaben weiter. Die laufende Spielinstanz und ihr nativer Kontext blieben eindeutig adressierbar.

## Persönlicher Ausgangsstand und Dateikopien

Das persönliche Original, die eingefrorene Sicherung, die anfängliche März-Arbeitskopie und die unbenutzte Reserve hatten beim Kopieren dieselbe SHA-256 und Bytezahl. Alle Forschungsdateien liegen lokal außerhalb der Original- und Cloudordner. Vor dem ersten Wechsel der geladenen Karriere sicherte der normale **Speichern unter**-Dialog zusätzlich den aktuell geöffneten Spielzustand unter einem neuen, privaten Namen. Diese Rückkehrdatei trägt denselben eingebetteten Spieltag und Build. Ihre Bytes unterscheiden sich erwartungsgemäß von der früher gespeicherten Datei. Die Originale identifizierte ausschließlich das private Pfad-/Prüfsummenmanifest.

Am 31. Januar öffneten wir eine separat benannte Ladekopie des historischen Stands. Danach öffneten wir die März-Arbeitskopie. Vor und nach den nativen Inventaren stimmten aktiver Pfad und Datum überein. Bei der Erhebung stand das Spiel, es lief weder eine Speicherung noch eine Partie. Die externe BuildProbe öffnete den Prozess ausschließlich lesend und lieferte Spieler-ID, Geburtsfeld, CA und PA. Sie las im Januar 94.776 und im März 97.555 Rohdatensätze. Als Doppelbestätigung zählen erst die vom Dateileser und vom nativen Leser eindeutig derselben Identität zugeordneten Werte. Abdeckung, Ausschlüsse und Feldvergleiche dokumentiert die [Faktorvalidierung](PROGRESSION_FACTOR_VALIDATION.md).

## Vollständige Attributmessungen und Zeitbasis

Zusätzlich lief FMSuperScout Scanner 1.7.3 einmalig pro Messung. Seine bestehenden FM27-Feldleser verwendeten die auf dieser Maschine vorliegende 27.1-Arbeitsversion. Für die Studie wurde nur das Ausgabeziel auf einen neuen privaten Ordner umgelenkt. Das verhindert ein Überschreiben der normalen Exporte und der Scout-History. Das aktive Spiel wurde über die BuildProbe und die Kontextbrücke unabhängig vom Scanner geprüft.

Der März-Vollscan trug intern den 20. März ein. Die gespeicherte Datei und die Pfad-/Zeitabfragen vor und nach dem Vollscan ergaben übereinstimmend **30. März 2027**. Der Vollscan lief im selben Prozess bei stillstehender Welt. Für solche Messungen kommt der bestätigte Stichtag aus Speicherdatei und eingerahmtem Spielthreadkontext. Der Scannerkopf allein genügt zur vollständigen Datierung eines Altexports nicht.

## Entwicklungsmodifikation

Die Spielinstanz hatte FMLivingPotential Seasons 0.13.0 geladen. Die lokale Saisonkonfiguration enthielt den persönlichen Ausgangsspielstand unter ausdrücklich zulässigen Zielen. Für die bisherigen historischen Vergleiche bleibt daher eine frühere Modexposition möglich. Eine konkrete frühere Änderung einzelner Spieler-PA setzt ein datiertes Schreibprotokoll voraus. Die privat umbenannten Forschungsstände lagen außerhalb beider zulässigen Zielpfade. Der Runtime-Status bestätigte die Pfadbeschränkung. Wir änderten keine Modkonfiguration. Der Kontrollarm erfasst das delegierte Spiel in dieser Umgebung.

## Prospektiver Monatscheckpoint

Am 30. März begann auf der überprüften März-Arbeitskopie ein Urlaub mit festem Rückkehrdatum 30. April 2027. Anfragen anderer Vereine wurden deaktiviert, eingehende Transfergebote abgelehnt und die aktuelle Taktik beibehalten. Eine bestimmte Aufstellung war nicht erzwungen. Laut Spielanzeige hatte die persönliche Karriere bereits vor der Abzweigung 171 Urlaubstage in dieser Saison. Der Kalender lief bis zum 30. April um 00:00. Vom unmittelbar nach Bestätigung gesetzten Zeitmarker bis zur ersten ruhenden Endabfrage vergingen 204,3 Sekunden einschließlich der Prüfintervalle. Zu diesem Zeitpunkt waren rund 399 GB auf dem lokalen Laufwerk frei. Die eingebaute Speicherfunktion schrieb den Stichtag in eine neue, 169.308.652 Byte große Kontrollarmdatei. Kontext, eingebetteter Dateitag und getrennte Leseinventare erlauben einen prospektiven 31-Tage-Vergleich innerhalb dieser Karriere. Der Kontrollarm hielt dort an.

Die nach diesem Lauf angeordnete aktive Vertrags- und Jugendbindung beginnt auf einer eigenen Kopie vom 30. März. Der Kontrollarm dokumentiert den Verlauf vor dieser Behandlung. Beide Arme teilen denselben historischen Stamm und dieselbe Ausgangsdatei.

## Aussagegrenzen

Jan–März sind zwei Zeitpunkte derselben Karriere. Der prospektive Kontrollarm stammt von derselben Wurzel. Natives Auslesen prüft die gespeicherten CA-/PA-Messungen. Die Progression-Factor-Semantik, eine Auslosung, der Einfluss von Ereignissen und die Wahrscheinlichkeit eines zukünftigen PA-Erfolgs erfordern weitere Beobachtungen. Der [Versuchsplan](../../research/pa-reach-001/manifests/zubieta-pilot-design.json) legt die Zielgrößen und Stoppregeln fest.

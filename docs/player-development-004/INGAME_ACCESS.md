# TRAIN-005 – nachgewiesener Code-Zugang

Stand 15.11.2026; laufender Einpaarpilot, noch kein fertiger Trainingseffekt.
Die Wegwerfkarriere wurde ausdrücklich für Code-Eingriffe autorisiert. Nach der
Nutzerkorrektur wurde keine weitere Windows-Desktopsteuerung verwendet.

| Zugang | Nachweis |
|---|---|
| Spiel | Football Manager 27, 27.0.1+2503222; Steam-Build 26577676 |
| Native Datei | SHA256 `8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340` |
| Laufender Spielthread | Frischer FM27-Labhost 0.4.5; IPC an PID, Prozessstart, Modulhash, Nonce und Ablaufzeit gebunden |
| Training | Einspieler-Setter über das tatsächliche FM27-Clientereignis; separates Readback −1 → 9 / „Schnelligkeit“ |
| Fortschreibung | `ContinueGameEvent` im tatsächlichen Karriereprozess; mehrere verschiedene Kalenderdaten nachgewiesen |
| Spieltage | Sichtbare aktivierte native Sofortergebnis-Option, zugehörige gebundene Ereignisse und Rückkehr aus dem Matchablauf |
| Speichern | Reguläres `SaveGameHandlerModule.DoSaveGame`; neue native A-Dateien mit geändertem Hash erzeugt |
| Attribute | 47 verwertbare Attributanzeigen; UI-Auflösung, keine behaupteten Rohattribute |
| CA/PA | Frisch entdecktes natives Spielerobjekt, mit UI-Identität und Geburtsdatum abgeglichen; STORED_CA und gespeicherte PA |
| Editor-RCA | Nicht gemessen; STORED_CA ist kein unabhängiger RCA-Goldwert |

Die FM-SuperScout-Trainingsbrücke 0.2.0 enthält FM26-26.3.2-Adressen und wurde
nicht auf FM27 übertragen. Genutzt und eng ergänzt wurde die bereits vorhandene
FM27-Spielthreadbrücke. BepInEx 6.0.0-be.791 und Unity 6000.3.18f1 werden vom
laufenden Prozess gemeldet. Der externe Living-Potential-Saisonmod wurde vor der
Fortschreibung angehalten; keine absichtlichen CA-/PA- oder Attributschreibzugriffe.

Der frühere Prozess hatte keinen frischen Lab-Heartbeat. Nach überprüfter
Sicherung der drei bytegleichen Dateien wurde die autorisierte Wegwerfkarriere
neu gestartet und eine frische Brücke nachgewiesen. Der anfängliche Desktopweg
hatte zwei Capture-Timeouts; daraus wurde keine erfolgreiche GUI-Bedienung behauptet.

Der Eingriff ist auf `FM27-RESEARCH-TRAIN-A` und `FM27-RESEARCH-TRAIN-B`
beschränkt. Aktueller Kopienname, Datum, Spieleridentität, erlaubte Option und
Leerlaufzustand werden vor Änderungen geprüft. Nach einer Kaderumsortierung
wurde eine Messung durch den Identitätscheck abgewiesen und korrekt neu nach
stabiler Identität gebunden; kein falscher Spielerendpunkt akzeptiert.

Zwei vergebliche Überschreibbestätigungen werden als technische Fehlversuche
bewahrt. Statt Erfolg zu unterstellen, wird die bisherige eigene A/B-Datei
gehasht und außerhalb Git erhalten; der reguläre Spielbefehl erzeugt am nun
freien, ausschließlich eigenen A/B-Ziel eine neue Save-Datei. Originaldatei
und private Messbelege bleiben außerhalb des öffentlichen Repositories.

Das Laden/Speichern allein ersetzt keinen Persistenznachweis des Fokus. Der
Ladezyklus für die endgültige B-Zuweisung und die Achtwochenendpunkte sind noch
ausstehende Gates. Temporäre Loader-Konfiguration und eingesetzte Labhost-Datei
werden nach Sicherung des Versuchs gegen ihre privaten Sicherungen abgerechnet.

# ATTR – Runde3, ATTR-009-Bridge

Vorarbeit implementiert; dieser Spezialagent hat **0 native Prozesse/Matches,
0 Seedreservierungen** ausgeführt. Native Freigabe/Ergebnis erst zentral nach
Review, tatsächlicher Identitätsprüfung und technischen Gates.

Forschungsfrage: Moderieren ungenutzte Positionsratings den relativen Nutzen
von Jumping Reach gegenüber Acceleration/Pace? Eine reine globale Rangliste
würde bestehende ATTR-001–007 und externe Positionsstudien wiederholen;
der gezielte Masken×Attributkontrast ist die neue Frage. Externe Übertragung
bleibt Hypothese, keine hier neu bestätigte Meta-Aussage.

[Vorregistrierung](../../experiments/ATTR-009-preregistration.md),
[Masken-/Rohdosisencoder](../../research/attr009.py),
[zentraler Runner](../../analysis/run_attr009.py),
[deterministische Analyse](../../analysis/analyse_attr009.py),
[kontrollierter Export](../../analysis/export_attr009.py).

## Tatsächlich geprüfte Quellfähigkeiten

Read-only Quellen des bestehenden Tactics Lab v1114.6:

| Quelle | Befund / Reichweite |
|---|---|
| `fm27_tactics_server.py`209 |15Ratings0..20,54Abilities1..100; kein Display-Umskalieren im nativen Encoder. CONTROLLED_START wird erneut gesetzt und bleibt unverändert. |
| `tactics_ui/app.js`35/72 |Labanzeige raw/5, Rückschreiben×5. Keine empirische FM-Karriereanzeigekalibrierung. |
| `desktop_host.cpp`439/485–512 |Kind12 prüft seitenspezifische Managerpermutation; tatsächliche MATCH_PLAYER-IP-/OOP-Position/Rolle/PI nach Originalvorbereitung mit Input verglichen;22Spieler/2Phasen. |
| `desktop_execution.py` |Ohne experimental_execution keine Executionreceipts. |
| `native_execution_experiment.h`125–160 |Ohne Kind61 früh zurück; aktiv verändert Versionsfeld und Hook-/Effektivitätszustand. Kein erlaubter passiver Gesamtaudit. |
| `research/native.py` |Vollständige Attribute/IDs, Originalvorbereitungsreceipt, Profile/Phasen/Seed; keine native Freigabe durch eigene boolesche Marker. |

Byte-SHA256 geprüfter Runtimequellen:

- Server `5f2be140f30d576872351e7c397102b0b5a3de7d0b05f8d4e5011a65e94ea590`.
- Profile `28f163f21c9aa80e9323e9b245127c3c48958218c1337cddb6ac6aae399c511f`.
- Desktopexecution `ac1589b5b23aac0ed5771dc8bb3e04b526d21996ba3d25357c9a477569a8311b`.
- LabUIapp `336373923570ac95cdcde6410e5af9cd0cec0e69e9870eeba9c43e032371d073`.

Die Implementierung prüft später zusätzlich alle in P1B eingefrorenen
LF-normalisierten Sources. Bytehash und LF-normalisierter Hash sind verschieden
definiert. Quellenlektüre ist keine nachträgliche Behauptung eines neuen nativen
Runs oder Beweis, dass jede gelesene Upstreamsource den Binärhost kompiliert hat.

## Scopeentscheidung und offene Gates

Director akzeptiert explizit native Roh60→80. Der erlaubte totale Eingriff ist
von einer nicht identifizierten passiven Mechanismenzerlegung getrennt.
Keine12→16-FM-Anzeige-,CA-Neuverteilungs-,Karriere- oder Mediationsbehauptung.
Fehlende passive Messfähigkeit wird sichtbar dokumentiert und nicht durch
experimentelle Neutralisierung kaschiert. Native Eingabegates bleiben zwingend.

Die tatsächlichen vier D00-Dateien wurden ohneServerimport gelesen:24 eigene
Arminterventionen lassen sich erzeugen;10–126 Attributrecords ändern sich je
Zelle. Seitenspezifische OOP-Maps sind `[0,1,2,3,4,9,5,6,7,8,10]` und
`[0,1,2,3,4,5,6,7,9,8,10]`. MCR/MCL→MC7 ergänzt; DCL/DCR→DC3,
DML/DMR→DM5. LogischeZelle und native OOP-Adresse werden getrennt gehalten.
Auswärtsträger26 Slots/23aktive, ungenutzterTail wird erhalten.

Offen bis zentraler Technik: aktuelle Engine-/Hostidentität,24 echte native
Eingabezellen,1058Profilfelder,748PI-Gruppen, Roh60/80-Vor-/Nachbelege,
acht deterministische Wiederholungen, erwartete Negativabweisung und Budget-/
Publikationsbelege. Quellen und synthetische Tests ersetzen diese Gates nicht.

## Design / Kosten / Erkenntnis

384Hauptmatches/32 unabhängigeBlöcke;32technischeVollmatches+1Negativprobe.
600s kumulierteChildzeit/1200sUTC,4Worker/90sFortschritt,2GiBprivateArtefakte,
20GiBReserve. Kein Karrierekalender oder Holdout. Verzicht auf Baselinearme
spart25% gegenüber512Jobs für dieselbe relative Frage; kein gemessener
Varianzgewinn und keine absoluten Attribut-Haupteffekte behauptet.

Primär S[J−(A+P)/2]−O[J−(A+P)/2] aufxGD, genauHolm5 sekundär. Pilot-SD erst
zu messen; keine garantierte90-%-Power. Ergebnis wird auf dieses synthetische
Fixture/Build und D00 begrenzt. Nächster Schritt ist unabhängiger Codereview,
danach zentrale Vorbereitung/Veröffentlichung/Technik; erst dann Hauptfreigabe.

Offlineabnahme dieses Arbeitszweigs:14neue ATTR-Tests,100Repositorytests und
5historischeAnalysetests bestanden;24echte D00-abgeleitete Absichtskonfigurationen
ohne Serverimport geprüft. Diese Zahlen sind Software-/Absichtsprüfungen,
keine neu gestarteten nativen technischen oder wissenschaftlichen Matches.

# VALID-004-R1/R2 – unabhängige Ergebnisprüfung

14.11.2026. Beide veröffentlicht freigegebenen einmaligen Lesepässe nach
Commit `2172b76faaeb7db7f38e1dbf693b69e2757cc1fd` und erfolgreicher CI43626055825
abgeschlossen. **Partielle strukturelle Lesbarkeit bestätigt; keine Trainings-,
Taktik-, UI-, native oder Karrierefortschreibungsfreigabe.**

## Rekonstruktion der tatsächlichen Läufe

Alle24 öffentlichen Probezeilen einschließlich Counts, Checks, Warnungen,
Layoutangaben und Fehlerklassen gegen die beiden privaten Ereignisledgers
feldgleich nachvollzogen. Private Attemptdateien bestätigen die veröffentlichten
Ressourcen- und Snapshotreceipts. Der Reviewer öffnete, haschte oder decodierte
keinen Save und startete keinen Ersatzreader. Originale Parserobjekte wurden
nicht erneut erzeugt; die folgenden Tabellenzahlen sind erhaltene Parserclaims,
keine zweite unabhängige Inhaltszählung des Spielstands.

| Merkmal | R1 Runtime-V10 | R2 offizielles0.12.4 |
| --- | ---: | ---: |
| Protokollierte Laufzeit |13,985s|14,453s|
| Tatsächliche Decoderprozesse |1|1|
| Peak Job Private Bytes |1177456640|1181728768|
| Beobachtete Probes inklusive `open` mit Warnung |4|5|
| Fehlgeschlagene Probes |1|1|
| Unbegonnene Probes |7|6|
| Angewendete/bestandene protokollierte Gates |26/26|28/28|
| Davon advisory |0|25|

Beide Ressourcenreceipts weisen180s,3GiB Prozess-/Jobspeicher, Ein-Prozess-Limit,
Kill-on-close, null Retries und keine ungültigen Ledgerzeilen aus. Beide
Vor-/Nachhashreceipts binden denselben stabilen R0-Snapshot
`1e6dfc4ec647f7c02ff7f527f4696e91dec14f9b79086a1c038d0a97eaf40d0d`.
`resources.status=completed` beschreibt den beaufsichtigten Pass, nicht zwölf
erfolgreiche Readerendpunkte.

Beide Reader melden denselben Last-writer-Build27.0.1+2503222, Parserdatum
2027-01-16 und `UnknownBuildWarning`. R1 verzeichnet einen Summaryaufruf und
**keinen** Draftfallbackaufruf; der vorhandene Fallback darf damit weder als
ausgeführt noch als validiert gelten. R2 verwendet keine V10-Instrumentierung.

Gemeinsame Counts: ein verwalteter Club,42001Clubrecords,113815Spielerrecords,
vier gespeicherte verwaltete Teamzuordnungen und77 zugeordnete Spielerrecords.
Die privaten Joinbindings sind zwischen R1/R2 byteidentisch. Das bestätigt die
beiden Parserjoins auf denselben Bytes, keine reale aktive UI-Karrierezuordnung.
Roh-/Anzeigebereiche der77Spieler bleiben parserabgeleitet und unkalibriert.

## Fehler und zusätzliche R2-Abdeckung

R1 stoppt bei `training` mit `UnsupportedGameError`: nichtleere Trainingheader-
Einträge werden vom gewählten Layout nicht unterstützt. Der private Fehler
stimmt mit der entsprechenden vendorten Quellprüfung überein. Das ist ein
konkreter Reader-/Layoutblocker, keine Trainingswirkungsbeobachtung.

R2 liest vier Trainingrecords und stoppt anschließend bei `tactics` mit
`ReaderCheckError`: erwarteter Set-piece-Marker steht nicht an der angenommenen
Position. Der private Fehler entspricht der eingefrorenen Tactics-Quellprüfung.
Kein stilles Übergehen, Ersatzlayout oder weiterer Versuch. `selections`,
`set_pieces`, `staff`, `staff_lists`, `injuries` und `fixtures` bleiben bei R2
unbegonnen; bei R1 zusätzlich `tactics`. Das sind keine Nullbeobachtungen.

R2-Trainingscounts unabhängig aufsummiert:

| Anonymes Team | gespeicherte Wochen | Tage | rohe Sessioncodes | Parser-Zeitfenster |
| --- | ---: | ---: | ---: | --- |
|T00|61|427|1281|2026-06-22 bis2027-08-16|
|T01|30|210|630|2026-06-29 bis2027-01-18|
|T02|30|210|630|2026-06-29 bis2027-01-18|
|T03|34|238|714|2026-06-22 bis2027-02-08|
|Gesamt|155|1085|3255|gespeicherte Fenster|

Je Record stimmen7Tage/Woche und3Sessioncodes/Tag. Die Fenster reichen über das
Parser-Savedatum hinaus, besonders T00 bis August2027. **Gespeicherte Planungs-
oder Historienfenster belegen keine155 tatsächlich absolvierten Wochen.**
Individuelle Teilnahme, Coach/Fokus/Intensität und Verletzungsexposition fehlen.
Auch Bedeutung und UIzuordnung der Rawcodes sind damit nicht unabhängig belegt.

Der veröffentlichte24Felder-Vergleich enthält13gleiche Parserwerte und11wegen
Missing/Abbruch nicht vergleichbare Felder; keine beobachtete Differenz.
Alle gemeinsamen Coveragefelder stimmen überein, die Checkpolitik unterscheidet
sich deutlich.25Advisory-Gates im neueren Reader sind nicht mit zusätzlichen
blockierenden Integritätsbelegen gleichzusetzen. `borrowed_layout=null` ist
fehlende Herkunftsdiagnostik, kein Beweis eines exakt bekannten Layouts.
Eine Datei, zwei Reader bleiben ein Quell-Snapshot ohne unabhängige kausale n.

## Gehashte Ledgerbindung und Wiederholung der Prüfung

| Privater Beleg | R1 SHA256 | R2 SHA256 |
| --- | --- | --- |
|events.jsonl|`d92dc6b91810975752f48fcffa228e8aa1228f7a148d8c20bc23fbde99be7e65`|`411a5818b46d8a6f7f168143e7d468192681700613a14aac7d8e656f127de8e7`|
|attempt.json|`decd3ef29c03c81352b40bac0818dbeb8fc12155b30e1ee2c21b02313a01e18d`|`63269055e0d320b7e9aec94c7058383a02f2f1e8c6e6eb4b13d6ee0b4f161e31`|
|private-bindings.json|`bf1cf853f5eda409b7d7c8e469238b303bc38f1272ff40293d9ff93f256dd96c`|`bf1cf853f5eda409b7d7c8e469238b303bc38f1272ff40293d9ff93f256dd96c`|

Öffentliche Coveragereceipts: R1
`db5fe8c2b7c5cc0932f5692fb476be9846e7bec444a3430af7f38b0430fc3315`, R2
`f9c723f1624b49c1e458b189f96b404f8bf6d11069d292d18c30d518709ce22a`.
Cross-reader-Receipt
`5d5deb67551de91494fba377970c0350ed8f707ef46d425a417dd59c8db4049c`.
Quellbelege: [R1](../../data/night-001-career-r1/R1/coverage.json),
[R2](../../data/night-001-career-r1/R2/coverage.json),
[Vergleich](../../data/night-001-career-r1/cross-reader.json).

Der eigene [Reviewauditor](../../analysis/review_night001.py) unterstützt
`--career-runs-root <zentraler Checkout> --verify-private-career-runs`.
Er liest ausschließlich öffentliche Receipts und ausdrücklich ausgewählte private
JSON-/JSONL-Ledgers, niemals `.fm`. Status-, Ressourcen-, Fehler-, Trainingcode-
und Ledgerprüfung bestanden. Privattexte und Trägeridentitäten bleiben lokal.
Alle nativen, UI-, RNG-, Teilnahme-, Replay- und Advancefreigaben bleibenfalse.

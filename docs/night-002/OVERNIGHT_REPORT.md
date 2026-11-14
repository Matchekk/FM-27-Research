# NIGHT-002 – konsolidierter Forschungsbericht

**Zwischenstand 15.11.2026 Europe/Berlin.** MECH-004 ist terminal gestoppt;
die eigenständige Mission ist noch aktiv. Keine Teilserien-Leistungsauswertung.

## A. Neue Forschungsfragen

[Zehn Kandidaten](NOVELTY_MATRIX.md) enthalten Hypothese, Quellenüberlappung,
Novelty-Entscheidung, Kontrolle, Einheit, Endpunkt, Confounder, Aufwand und Nutzen.
Beste drei: getrennte C90/C7A-Attribution; gekreuzte stürmerlose IP/OOP-Pakete;
Nettoertrag je tatsächlich ausgeführter Ecke. [Aktueller Quellenreview](LITERATURE_AUDIT.md)
ergänzt Puritys neuen Keepernachtrag und trennt FMAX-Livedaten vom Suchcache.
Externe Zahlen sind Autorenangaben, keine eigenen Replikationen.

MECH-004 und TACT-003 sind `NOVEL_HYPOTHESIS` innerhalb der geprüften Literatur,
kein Anspruch weltweiter Erstmaligkeit. Joint-Sharpness-Wiederholung und alter
Staminavertrag sind `DUPLICATE_STOP`; ihre Budgets/Seeds bleiben geschlossen.

## B. Tatsächlich ausgeführte Studien

### MECH-004-SPLIT-R0: Technik bestanden, Hauptserie abgebrochen

Frage: Unterscheiden sich C90- und C7A-Rohstartwirkungen? Vier gekreuzte Arme
7000/10000 je Feld, zehn Startfeldspieler, D00, zwei feste Gegner, beide Seiten.
FM27 27.0.1+2503222, unveränderter passiver Observerhost, Tactics Lab v1114.6.

- Technik:32 Vollmatches, vier separate Seeds,16 exakte A/A-Paare und eine
  erwartete Exit108-Abweisung. Beide Rohfelder überstehen Vorbereitung und
  Erstfortschritt getrennt. Alle Kontrollen/Actorbindungen/Nativeinputs bestanden.
- Neuer technischer Befund: Cache8A ist70 bei C90=7000 und100 bei C90=10000,
  unabhängig von C7A, in allen geprüften Start-/Erstschrittaufnahmen. Keine
  UI-Skala, Consumersemantik oder natürliche Karrierewirkung nachgewiesen.
- Main:224 akzeptierte Matches,1 vor Engineaufruf fehlgeschlagener Job,
  287 unbegonnene Plätze.28 vollständige8er-Blöcke ausschließlich `deep_block`;
  die geplante64-Block-/Zweikontextserie fehlt. **Keine primären oder sekundären
  Leistungseffekte, Intervalle oder Äquivalenzaussagen aus dieser Teilserie.**
- Fehlerursache: Der Director versuchte wegen steigender Scanlaufzeit, bereits
  abgeschlossene private Belege während des unveränderten laufenden Pfadscans
  verlustfrei zu archivieren. Das löste `Mission artifact path escaped` aus.
  Eine echte Pfadflucht ist nicht belegt. Dies war ein vermeidbarer Fehler des
  Directorablaufs, keine Wirkung der wissenschaftlichen Intervention.
- Alle1024 archivierten Originaldateien wurden bytegleich wiederhergestellt;
  alle257 tatsächlichen nativen Calls sind bereinigt. Keine verlorenen Rohdaten,
  offenen Pendingmarker oder globale Lease. Alle545 Plätze/68 Seeds bleiben
  reserviert; eigener Studienetat `halted`, keine Wiederholung oder Ersatzseeds.

Eigene belastete Phasenchildzeit528,8133745s, globale589,7353507s; zusätzlich
separat838,064s summierte Native-Callzeit. Diese Größen werden nicht addiert.
Die technische Teilstudie bleibt gültig; die Fußball-Feldattribution bleibt offen.
[Technikbericht](../../experiments/MECH-004-split-validation.md),
[Stoppbericht](../../experiments/MECH-004-split-stop.md),
[Terminalbeleg](../../data/night-002-split004/termination.json),
[unabhängige Abschlussprüfung](SPLIT004-TERMINATION-REVIEW.md).

Vorregistrierung0e535dc/CI43648809178, Registrierungb53c56e/CI43649328317 und
Technikfreigabe5ea00c8/CI43650461926 lagen jeweils vor ihren freigegebenen
Aufrufen vor. Der spätere Infrastrukturabbruch wird dadurch nicht beschönigt.

### TACT-003-STLESS-R0: unabhängiger nächster Gegenstand, noch nicht ausgeführt

Primärfrage: Moderiert das OOP4420-Paket den Effekt des IP4240-Pakets gegenüber
IP4231/OOP4411? Vorregistrierter2×2-DoD, keine isolierte Rollen-/Positionswirkung.
[Design](STLESS003-DESIGN.md) und [unabhängiger Neuheitsreview](STLESS003-NOVELTY-REVIEW.md)
liegen vor.0 neue TACT-Matches;68 neue Seeds gegen2665 frühere/reservierte Werte
gebunden und16 konkrete Eingaben offline erzeugt.
[Konkreter unabhängiger Inputreview](STLESS003-INPUT-REVIEW.md) bestanden;
native Rollen-/Positionslegalität bleibt vor Main zu prüfen.

Die überprüfte globale Administrationsfortsetzung wurde nach Veröffentlichung
`d143d3e` und erfolgreicher CI43653104526 tatsächlich ausgeführt. Kein Reset:
bisherige Zeit, alle545 Reservierungen, Fehloperation und eigener MECH-Stopp
bleiben erhalten. Dauerhaftes MECH-004-Admissionverbot. TACT erhält anschließend
eigene Input-/Code-/Review-/Publikations-/CI-Gates vor irgendeinem neuen Engineaufruf.
[Administrativer Receipt](../../data/night-002-stless003/mission-administration.json).

## C. Technische Fortschritte und Grenzen

Native Splitidentifikation ist tatsächlich bestanden. Die Archivierung war kein
Erfolg des Laufzeitpfads; erfolgreich war nur die überprüfte bytegleiche
Wiederherstellung. Der ausgeführte eigene Hilfsquellstand ist unter
`archive/night-002/archive_completed_native_v0.py` erhalten und wird nicht erneut
während einer aktiven Phase eingesetzt.

Der neue, erst nach dem Stopp geänderte Controller zählt Artefakte mit einer
geprüften Scandir-Traversierung statt einzelnen Windows-Pfadauflösungen.
Read-only-Identität146.920.935Bytes, ein Messdurchlauf0,633s vorher/0,013s nachher
(etwa48fach); keine neue native Validierung durch diesen Mikrobenchmark.
Reparse-/Linkverbote, Bytecaps und alte Abrechnung bleiben unverändert.

[SET-Readiness](SET-READINESS.md): Drei vorhandene Logs und Originalcode geprüft.
Der Host liefert keine vollständige Eckkontakt-/Retake-/Shot-xG-/Besitzkette.
Zusätzlich konkurrieren Stats-/Eventhooks um Debugregister; Episoden-xG und
Torfenster stimmen nicht überein.0 neue SET-Wirksamkeitsmatches, kein Nennergate.

## D. Praktische Konsequenzen

Noch keine neue eigene Spieler-, Rollen- oder Trainingsempfehlung. Der technische
C90-Cachebefund ersetzt keine Fußballleistungsschätzung. Meta-Scorev0.1 bleibt
unverändert und unvalidiertes Prognosemodell. Natürliche Karriereübertragung,
UI-Prozentbedeutung und echte Rollenlaufwege bleiben unbewiesen.

## E. Kritische Bewertung

Neue bestätigte Fußballwirkung: bislang keine. Neuer technischer Transferbefund:
getrennte Rohfelder und beobachtete C90-Cachekopplung. Explorative Leistungshinweise:
keine aus der unvollständigen Serie berechnet. Widerlegte Wirkungshypothesen:
keine; Infrastrukturfehler ist kein Nullbefund. Der Directorfehler hat224 gültige
Messungen ohne vorregistrierte Gesamtauswertung verbraucht und ist ein realer
Forschungsverlust. Andere unabhängige Fragen werden nicht dafür umetikettiert.

## F. Nächste Prioritäten

1. TACT-003 mit eigenen überprüften Gates als unabhängigen begrenzten Pilot
   ausführen und vollständig auswerten; niemals MECH-004 fortsetzen.
2. SET: tatsächliche Kontakte/Legalität/Retakes, danach einzelne Schuss-/Finaltor-
   und Besitz-/Konterbindung reparieren und gegen echte unabhängige Goldfälle prüfen.
3. Neue natürliche Schärfe-/Profilfrage erst mit eigenem Kontext-/Consumer-/UI-Gate
   planen; die fehlgeschlagene identische Serie nicht neu benennen oder nachfüllen.

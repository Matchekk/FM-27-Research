# NIGHT-003 – Zeit- und Fortschrittsprotokoll

15.11.2026, alle Zeiten UTC (CET=UTC+1).

| Zeit | Abschnitt | Tatsächlicher Stand |
|---|---|---|
|07:58:36|Beginn/Inventur|Fetch erfolgreich; main und origin/main764764b, sauber. Neue Mission, kein altes Budget reaktiviert.|
|08:00:09|Machbarkeit|Unveränderte IP-/Startpolicycompiler und Vier-Worker-Containment identifiziert. Kein neuer nativer Setter nötig.|
|08:04:20|Gezielte Vorbereitung|Feste Kombination und Analyse implementiert; Systempython ohne numpy erkannt, vorhandene .venv wird verwendet. Keine Simulation bisher.|
|08:08:09|Vorregistrierung geprüft|436 lokale Tests bestanden (2 bedingte Skips),5 Analysetests bestanden.516 neue disjunkte Seeds reserviert;0 Nativecalls.|
|08:11:15|Native Technik gestartet|Vorregistrierungs-CI43693138863 erfolgreich; eigener neuer Supervisor/exklusive Lease.|
|08:11:48|Native Technik abgeschlossen|32Vollmatches+Exit108;16exakteA/A;alleReadbacks und zweiterRohpass bestanden. Keine wissenschaftlichen Matches.|
|08:13–08:15|Publikation/CI|Archivtest-Encodingfehler im neuen Test korrigiert (0f997d5→f57c193), keine nativen Änderungen. CI43693487274 fürf57c193 erfolgreich; vorherigeCI43693468796 scheiterte am Testtippfehler.|
|08:15:52|Hauptserie gestartet|4096neueMatches,512Blöcke; neuer Quellen-/Patchcheck unverändert. Beginn nach rund17Minuten Vorbereitung, innerhalb30-Minuten-Grenze.|
|08:29–08:35|Während Main: nächste Frage vorbereitet|N3-SHARPPOS-C1:4096geplanteMatches/1024Blöcke, zwei feste Zweispielergruppen.5gezielteTests und synthetische separate Nachrechnung bestanden.1028disjunkte neueSeeds reserviert;0Nativecalls der zweitenStudie. ErsterMain unverändert aktiv.|
|09:11:27|Erste Hauptsimulation vollständig|4.096Matches/512Blöcke, keine nativen Fehler; Rohbelege unverändert.|
|09:14:21|Erste Studie angenommen/ausgewertet|Zweiter Rohpass bestanden, alle Prozesse bereinigt.−0,013320xGD[−0,118593;+0,091953], separate Arithmetik stimmt überein.|
|09:15:25|Zweite technische Phase bestanden|Nach vollständiger erster Auswertung:16Vollmatches+Exit108,achtA/A,korrekteZweispielerbindung.15,060s Phasenzeit;Main0.|
|09:26|Erste Ergebnis-/zweite Freigabe-CI erfolgreich|a58e11d/CI43699039037:445Tests lokal bestanden,drei bedingteSkips;publizierte4.096Messungen undzweiteTechnik geprüft.|
|09:27|Zweite Hauptserie gestartet|4.096neueMatches/1.024Blöcke;Quellenstand unverändert,Missionsrest über4.200s. Nur aktive Sitzung gemäß Nutzerantwort.|
|09:29:50|Vollständige separate Statistikprüfung Studie1|Alle sieben formalen Welch-Schätzer einschließlich sechsSekundärtests und unabhängigerHolm6-Rechnung stimmen überein.|
|09:43–09:55|Bedingte dritte Frage vorbereitet|AMC→AMCL allein, Rolle/ST/OOP und alle Startzustände gleich.2.048Matches/512Blöcke geplant,516neueSeeds reserviert,0Nativecalls.3gezielteTests und synthetische Nachrechnung bestanden;8Inputs geprüft mit genau0/1Recorddiff.|

Dritte Nativeadmission ausschließlich nach vollständiger zweiter Studie:
mindestens2.700s Missionsrest vor Technik,2.400s vor Main. Keine Anpassung
nach Kenntnis zweiter Leistungsdaten und keine Verlängerung der Frist.
Die separate Skalarprüfung wurde um den neuen2.048er-Plan ergänzt; alle sieben
bereits veröffentlichten Schätzer der ersten Studie bleiben numerisch unverändert
und wurden unter dem neuen Prüfsourcenhash erneut reproduziert.

Die [zweite Vorregistrierung](../../experiments/N3-SHARPPOS-C1.md) wurde ohne
Einblick in wissenschaftliche Ergebnisse der ersten Serie vorbereitet. Eigene
vier Profilrecords je Arm; kein neuer nativer Setter. Native Phasen der zweiten
Studie verlangen vollständige erste Hauptserie plus deren Auswertung und
skalare Nachrechnung. Gemeinsame feste Missionsfrist bleibt11:11:21UTC;
keine Verlängerung durch ein neues Studienbudget. Zweite Mainadmission verlangt
mindestens4200s Rest, um4096Matches realistisch vollständig ausführen zu können.

Die [Vor-Main-Änderung zur tatsächlichen sortierten Dispatchreihenfolge](TECHNICAL_RELEASE.md)
ist veröffentlicht. Primär-/Sekundäranalyse, Arme und Seeds unverändert.
Quellenrefresh: Mac-HEAD erneut e92cf141; SI-Updateforum erneut geprüft,
kein neuer veröffentlichter Patch in den geprüften Quellen. Build-/Ressourcen-
fingerprint vor Main erneut gleich. Eigene absolute UTC-Frist11:11:21UTC,
zusätzlich7200s kumulierte beaufsichtigte Phasenzeit. Keine behauptete
unbegrenzte Hintergrundsitzung und keine laufende Archivierung.

Vorabplanung bei4096: TACT-003-Interaktionsvarianz ergibt98,9% Power für0,20,
volle KI-Breite0,184; mit simultanen SD-Obergrenzen89,3%/0,245. Der größere
MECH-002-Interaktionsanker ergibt87,6%/0,252, konservativ64,9%/0,335.
Das ist keine garantierte90%-Power.4096 ist ein sinnvoller großer neuer
Interaktionstest; kein offensichtlich aussichtsloser Umfang, keine datengesteuerte
Vergrößerung. Der Haupteffektanker wird ausdrücklich nicht als Interaktions-
Powergarantie benutzt. Vorbereitete Inputs haben je Arm0/20/3/23 geänderte
Records, unveränderte OOP und keine fremden Attribute.

HTTP-Direktabruf des SI-Forums traf eine Challenge; lesbarer Inhalt wurde über
das Webwerkzeug geprüft. Kein lokaler Inhalts-Hash für diesen Abruf behauptet.

Aktive Technikfrist: spätestens08:28:36UTC Gateentscheidung bzw. Wechsel.
Zeitzuordnung folgt den tatsächlichen Abschnitten; keine behauptete dauerhafte
Hintergrundausführung. Eigener Phasensupervisor liefert Checkpoints und Fristen.

Zweite Serie10:24:14UTC vollständig simuliert; Rohpass und beide Rechenwege
bestanden. Dritte Technik10:26:36UTC mit16+1/achtA/A bestanden; mindestens2.700s
Rest vor dieser Phase eingehalten. Veröffentlichung/CI vor dritter Mainadmission.

# Agent 5 – Match Engine Researcher

**14.11.2026 · Recherche, Quellprüfung und Experimententwurf.** Keine nativen
Starts, Seedreservierungen, Registry-/Runneränderungen, Karriereausführung oder
Holdoutzugriffe. Nur dieser Bericht wurde geschrieben. Gitstatus/Remote und die
beauftragten Methodik-, Plattform-, Roadmap-, Findings- und MECH-Unterlagen gelesen;
fremde Änderungen bleiben erhalten. Lokale DLL-Dateiversion rein lesend27.0.1,
Produkt27.0.1+2503222; [zentraler Hashbeleg](../../data/tact-001-p1c/environment.json).
Keine neue technische Freigabe durch diesen Agenten.

## Forschungsfrage, Forschungslücke und Prioritäten

Wie groß ist der Verlust eines **klar definierten Startschärfepakets** in unserer
eigenen IP-4-2-3-1, und verändert häufigeres Pressing diesen Verlust?
Eine erneute Rangliste vieler Startzustände wäre wenig neu. Zusätzlicher Wert:
unter Windows tatsächlich wirksame Eingaben nachweisen, beide Schärfefelder
explizit kontrollieren, Start-only von dauerhafter Erzwingung trennen und eine
Pressinginteraktion in einem kleinen vollständigen Design mitmessen. Zuerst
muss der Normalisierungsblocker behoben und technisch freigegeben werden.

| Reihenfolge | Frage | Zusätzlicher Wert / heutiges Gate |
|---|---|---|
|1 Spielschärfe | Gemeinsames Startpaket sharpness/secondary und Pressing | Hoher mutmaßlicher Hebel; aktueller gewöhnlicher JSON-Pfad überschreibt beide Felder. Kein ausführbarer neuer Eingriff. |
|2 Fitness | Startcondition separat, fatigue_raw konstant; später Tempo/Pressing als eigene Faktoren | Condition und latente Ermüdung nicht vermischen. Neue Nach-Vorbereitungs- und Zeitverlaufsbelege nötig. |
|3 Tactical Understanding/Familiarity | Gelernte Bereichszustände versus aggregierte Anzeige | Bestehende Experimental-API isoliert die Bereichswerte nicht; passiver Originalrecordaudit und gezielter Bereichspfad fehlen. |
|4 Pressinginteraktionen | Schärfe×Pressing zuerst, Fitness×Pressing später getrennt | Kleine Interaktionen nicht blind hochskalieren; primär verständlichen Haupteffekt/Präzision messen. |
|5 Positionseignung | Unterstützt den ATTR-Brückenkontrast statt erneutem Haupteffektranking | Externe Study17/17b untersucht aktive/ungenutzte Ratings bereits. Neu ist deren JR-vs-Speed-Interaktion. |
|6 Wechsel/Management | Feste Wechselpolitik versus echte native Entscheidungen | Aufstellung, Zeitpunkt, Spieleridentität und Managerpfad getrennt auditieren. Keine Gleichsetzung mit Urlaub/Instant Result. |
|7 Heim-/Kontext | Venuewechsel bei gleicher Trägeridentität und kontrolliertem Fixture | Unsere Seitenmittel sind feste Fixtureplätze; kein isolierter universeller Heimvorteil. PKM-/Kontextadapter fehlt. |

P1C liefert keinen ausreichend präzisen Punktgewinn für D15; er ersetzt keinen
Schärfeversuch. Rollen/OOP bleiben im Gesamtprogramm höher priorisiert. Dieses
MECH-Design ist ein eigener späterer, technisch blockierter Vorschlag.

## Geprüfte externe Evidenz

Abruf/Quellprüfung14.11.2026. Mac-Quellkopie tatsächlich auf Commit
`849b16f9c4057598da33b255649c86d8cecb525b`; Berichte und relevante Setter lesend
geprüft. Keine externen Jobs ausgeführt, keine private Rohdatenreplikation.

| Primärquelle / Version | Berichtete Datengrundlage und Befund | Evidenzniveau / Grenze |
|---|---|---|
| [SI: Tactical Effectiveness](https://www.footballmanager.com/the-dugout/tactical-effectiveness-understanding-fm27s-key-new-feature),06.11.2026, FM27 | Hersteller erläutert Understanding, Player Ability, Buy-In und Next Match Info sowie Training und IP-/OOP-Eignung. | Produkt-/Mechanikbeschreibung, keine kontrollierte Stichprobe oder quantitative Wirkungsgröße. |
| [Mac Study5](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/05-everything-else.md),11.11.,27.0.1 | Autor meldet35.400Screen- und18.300Folgematches;10 gespeicherte Fixtures×30Seeds bzw.90neue Seeds für ausgewählte Bedingungen. Schärfe75% gegenüber natürlichen Werten:−0,37Punkte/−0,49xGD; Condition80%:−0,80/−1,21. | Extern berichtete starke Startzustandseffekte; breite Mehrfachsuche und selektierte Folgetests. Rohjobs fehlen öffentlich. Berichtete125Änderungen lassen sich aus der Kopfzahl allein nicht vollständig abrechnen; keine von uns bestätigte Versuchsbilanz. Keine Windows-/Karrierefreigabe. |
| [Mac Study3](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/03-tactical-familiarity.md),10./11.11.,27.0.1 |6.900Matches erster Dosisteil, später8.400Bereichs-/Levelsweep;300Paare/Bedingung. Direkte Erzwingung von Recordbereichen zwischen Steps; Traininganteile und Exposition getrennt. | Stützt Hypothesen zu Bereichszuständen/Sättigung, beweist keine Trainingsdosis pro Kalenderwoche und keine Gleichheit mit Start-only-Profiländerung. Viele getestete Levels/Bereiche. |
| [Mac Study17/17b](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/17-positions-in-and-out-of-possession.md),13.11.,27.0.1 |3.200+1.600Matches;400/320Paare je Bedingung, vier Gegner/Seiten. Bericht trennt aktive IP/OOP-, ungenutzte Feldpositionen und GK-Rating; letztes verändert Tore/Saves bei ähnlichem xG. | Bloße Wiederholung von Positionsrating-Haupteffekten wäre Doppelarbeit. Nichtsignifikante aktive Ratings beweisen keine Wirkungslosigkeit; Effekte unter gehaltenen Familiarityrecords und Assistentenmanagement sind kontextgebunden. |
| [Mac Study15](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/docs/studies/15-home-advantage-morale.md),13.11.,27.0.1 |2.480Matches insgesamt;1.200Heimvergleiche über12Fixturekontexte,100Seeds je Kontext. Bericht:+0,21xG Heim−Auswärts; Morallevels auf üblichen Presetkontexten. | Fixturebündel/Crowd/Venue/Seitenregeln nicht einzeln identifiziert; nullnahe Moraleffekte beweisen keine Karriereinvarianz oder fehlende Schiedsrichtereffekte. |
| [Windows Fidelity](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/docs/SIMULATION_FIDELITY.md), v1114.6 | Originaler Detail-Matchloop mit normalisierten Eingaben. | Weder vollständiger Karriereablauf noch game-UI/Urlaub/Instant Result dadurch gleichgesetzt. |

Der [Mac-Study5-Setter](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/port/validation/study5_everything.py)
ändert **sharpness und sharpness_secondary gemeinsam**. Das Mac-Projekt besitzt
[custom/natural Startpolitik](https://github.com/caiograco289/Fm-Match-Lab/blob/849b16f9c4057598da33b255649c86d8cecb525b/src/fm27_profiles.py),
die der hier freigegebenen Windows-Runtime nicht gleichgesetzt werden darf.
Die externen großen Schärfeeffekte sind deshalb Hypothesen-/Größenordnungsanker,
keine übertragenen Effekt-/SD-/Powerannahmen für unseren eigenen Versuch.

## Read-only technische Prüfung: tatsächliche Schreibpfade und Lücken

Windows-Toolcommit `91f2eba57fac0b7fbd3dff616056907e3ce461be`.
`fm27_profiles.py` Byte-SHA256
`28f163f21c9aa80e9323e9b245127c3c48958218c1337cddb6ac6aae399c511f`,
`desktop_execution.py`
`ac1589b5b23aac0ed5771dc8bb3e04b526d21996ba3d25357c9a477569a8311b`.
Lokale C++-Quelldatei `native_execution_experiment.h` SHA256
`400d39c359f851591c29436b749cb54fb376057db342c7a63d3beb2f87497f13`.
Diese sind Quellbelege, kein eigener reproduzierbarer Hostbuild.

1. [Profilfelder](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_profiles.py):
   condition=Feld15, sharpness16, secondary17, fatigue_raw18; rohe Wertebereiche
   sind geprüft. `validate_scenario()` setzt nach `profiles.normalize()` erneut
   CONTROLLED_START, darunter **beide Schärfefelder10000**, condition10000,
   fatigue0. Ein JSON-7000 wird damit im gewöhnlichen Pfad kein7000-Start.
2. Der Server kodiert Profile als begrenzte Records **kind15**, mit
   Profilfeld-ID; [Host](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/desktop_host.cpp)
   unterstützt diese Records. Aber `NativeLab.run()` verlangt binär exakt
   `server.encode_scenario(config,absolute=True)`, das erneut normalisiert.
   Nachträgliches JSON-/Binärpatchen wäre kein zulässiger bestehender Runnerpfad.
   Nötig ist ein **eigener versionierter opt-in Startpolicy-Encoder samt
   passendem Vertrag, Runnerbindung und Auditor**, nicht stilles Entfernen der
   historischen Standardisierung. Default muss binärgleich bleiben.
3. [Experimental execution](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/native/native_execution_experiment.h)
   ist kein gezielter Bereichs-Familiarityadapter. Dict-Policy benutzt
   `understanding` für die Berechnung des aggregierten Overall, schreibt aber nur
   Overall/Buy-In/Opposition; **nicht** die24Bereichsbytes. Scalar-Policy setzt
   dagegen alle33Bytes gemeinsam. Sie installiert Builder-/Samplerhooks und
   setzt einen internen Versionsmarker; Receipt nennt `production_supported=false`.
   Ein Effekt dieses Bündels wäre kein isolierter gelernter Trainings-/Understandingeffekt.
4. `desktop_execution.py` prüft experimentelle Receipts und Spieleridentitäten;
   das ist nicht der fehlende passive Originalrecordaudit aller Spieler unter
   normalem Betrieb. Erst rohe Original-Bereichs-/Komplexitäts-/Abilitywerte vor
   und nach Vorbereitung sowie bei Sampling erfassen, dann einen gezielten
   Bereichseingriff separat validieren. Keine Übertragung von Mac-Adressen.
5. Gegenstände Positionseignung und GK werden mit [ATTR](ATTR.md)/[VALID](VALID.md)
   koordiniert. Nicht gleichzeitig Rollen, aktive Positionen und Effektivität
   neutralisieren. Native reale Manager-/Wechselpolitik braucht eigene Receipts;
   supplied-plan versus AI-Regeneration ist noch kein vollständiger Karriereexecutor.

Der archivierte MECH-001-Entwurf bleibt unverändert. Vor Registrierung ist ein
neuer konsistenter Vertrag nötig: der alte JSON nennt Punkte auch sekundär,
während seine Powerbasis0,10xGD nennt und die Dokumentsekundärliste abweicht.
Nicht ungeprüft den generischen Entwurf ausführen.

## MECH-002-sharpness-P0 – vorgeschlagener Varianz-/Mechanismenpilot

**Nicht registriert, nicht implementiert, nicht gestartet.** Ersatzdesign zur
Präzisierung, kein Überschreiben des historischen MECH-001.

Voller2×2-Plan im unveränderten D00-IP4-2-3-1/OOP4-4-1-1, zwei bisherige
Discoverygegner `high_press`/`deep_block`, beide Seiten, gleiche Kader.
FaktorS: Startpaket **beide** sharpness-Felder10000 versus7000 bei den zehn
Startfeldspielern des Testteams; GK/Bank/Gegner unverändert. Dies ist ein
**gemeinsames Zweifelderpaket**, kein Effekt eines einzelnen Feldes. Ohne belegte
UI-Kalibrierung nur Rohwerte benennen, nicht behaupten7000 sei exakt70% einer
Karriereanzeige. FaktorP: Standardpressing (Gruppe10,ID1313689463,Bit0)
versus MoreOften (ID2000905329,Bit66), bereits aus TACT bekannt.

Condition10000/fatigue0, Moral/Kohäsion, Attribute/Positionseignung/Rollen/PI,
übrige Team Instructions und native Managementpolitik bleiben unverändert.
Der Eingriff ist **Start-only nach Originalvorbereitung**, kein permanenter Clamp.
Nach dem Start darf der native Verlauf einschließlich Wechseln reagieren;
das ist Teil des Gesamteffekts der Startzuweisung. Nicht nachträglich auf gleiche
Spielminuten/Wechsel matchen oder nur Nichtausgewechselte auswerten.
Neue native Kontextereignisse/Wechsel-/Profilverläufe nur deskriptiv, soweit
separat validiert; keine erfundenen Endfitness-/Verletzungswerte.

Arme in fester Reihenfolge: R00=voll/Standard, R10=niedrig/Standard,
R01=voll/MoreOften, R11=niedrig/MoreOften.

- **Primär:** positiver Vorteil voller Startschärfe auf xGD,
  `F=(R00−R10+R01−R11)/2`. Ein Testα0,05, praktische Screeninggröße0,30xGD,
  gewünschte volle95-%-Breite≤0,50. Nicht aus niedriger P1B-Faktor-SD ableiten.
- **Explorativ sekundär, genau Holm8:** F auf Punkte/GF/GA/xGF/xGA (5),
  Pressing-Haupteffekt `(R01−R00+R11−R10)/2` auf xGD (1),
  Schärfeverlust×Pressing-DoD `R11−R01−R10+R00` auf xGD und Punkte (2).
  Negative DoD bedeutet stärkeren Verlust durch niedrige Schärfe bei MoreOften.
  Primär- und Sekundärfamilie sind getrennt, keine gemeinsame95-%-Absicherung
  über alle neun Tests behaupten. Sekundärbefunde ersetzen keinen Primärnachweis.
- Pro Seite Kontrast, dann Seitenmittel innerhalb des Seeds; danach beide Gegner
  je½. Unabhängige Seeds je Kontext. Welch-Satterthwaite-t,20.000stratifizierte
  vollständige Seedblock-Resamples; alle Kontrast-SDs, LOO und tatsächlichen
  Scores erhalten. Fehlende Arme: nur technischer Status, keine stillen Nullen.

### Stichprobe, Präzision, Kosten

Ein Seedblock umfasst vier Arme×zweiSeiten=achtMatches. Die SD des primären
Seedkontrasts F ist **unbekannt**;0,8/1,2/1,8 sind bloße Szenarien.
Die Interaktions-SD kann größer sein und erhält keine gleiche Powerbehauptung.

| Variante | Neue Seeds/Gegner | Unabhängige Blöcke | Hauptmatches | Technische Plätze separat | Child-/UTC-Capvorschlag |
|---|---:|---:|---:|---|---|
| Klein zuerst |32|64|512|32Vollmatches+3negativeProbes|900s/1800s|
| Größer, nur separat wählen |64|128|1024|32+3|1200s/2400s|

Technik:16Gegner×Seite×Arm-Zellen jeweils zweimal,16exakte A/A-Paare;
negativ: ungültiger Rohwert, unbekannte Profilfeld-ID, beschädigte Binäreingabe.
Feste Versuchszähler **35technisch** und512/1024Haupt, keine Ersatzseeds/Retry.
Maximal4Worker global,90s ohne Fortschritt,2GiB private Artefakte/20GiB frei.
Konservativer Durchsatzanker0,7Child-s/Vollmatch ergibt etwa381/739s für alle
Vollmatches plus Vorbereitungs-/Probekosten; keine neue Laufzeitmessung.
Vorbereitung, Probes, Audit und Publikationspausen im jeweils festgelegten
Child-/UTC-Budget berücksichtigen, kein Reset zwischen Phasen.

| Angenommene F-SD | Kleine volle95-%-Breite / Power für0,30 | Große volle95-%-Breite / Power für0,30 |
|---:|---|---|
|0,8|0,400 /83,97%|0,280 /98,78%|
|1,2|0,600 /50,36%|0,420 /80,15%|
|1,8|0,900 /25,93%|0,630 /46,47%|

Offline mit SciPy-t/nct berechnet: gleiche Kontext-SD als Annahme,
SE=SD/√(2n),df=2n−2, zweiseitigα0,05. Kein garantierter90-%-Pilot.
Pro1000Hauptmatches etwa125komplette Achtmatchblöcke und drei xGD-Kontraste
(F,Pressing,DoD); das ist eine Kosten-/Kontrastzahl, kein gemessener
Varianzgewinn oder125unabhängige Gegnertypen. Bei SD1,2 wäre die erwartete
volle95-%-Breite für F grob0,425. Ein Zweiarmversuch könnte mit gleicher
Matchzahl mehr Seeds prüfen, beantwortete aber die Pressinginteraktion nicht.

**Stop-/Fortsetzungsregel:** feste Fallzahl, kein Ergebnis- oder Signifikanzstopp.
Native Identitäts-/Input-/Seedfehler stoppen sofort, alle gestarteten,
fehlgeschlagenen und unbegonnenen Jobs erhalten. Keine adaptive weitere Suche.
Nach vollständigem Pilot SDs samt modellbegründeten Obergrenzen und benötigte
neue Bestätigungsblöcke für vorab feste0,20/0,30xGD berichten. Bei breiten
Interaktionsintervallen nicht auf kleine DoDs hochskalieren; zuerst Mechanismus
oder Kontext vereinfachen. Ein Anwendungsnachweis braucht später Punkte primär,
neue Kontexte und eigenen Powerplan, keine automatische Karriere-/Holdoutserie.

## Gate, Implementierungs-/Teststatus und nächste Schritte

**Jetzt sicher offline möglich:** Quellen-/Schemavergleich, erlaubte Recorddiff-
Sollmengen spezifizieren, beide Schärfefelder explizit benennen und negative
Schemafälle entwerfen. Kein neuer Encoder/Auditor wurde hier implementiert.

**Vor irgendeinem neuen Hauptmatch zwingend:**

1. Director/VALID spezifiziert eigenen opt-in Startpolicyvertrag und zugehörige
   Encoder-/Runner-/Auditversion; kontrollierter Default bleibt binärgleich.
2. Alle erlaubten Profil-/Pressingrecords und unveränderten Eingaben prüfen,
   beide Schärfefelder nach Originalvorbereitung für jeden betroffenen Spieler
   nativ auslesen. Keine stille experimentelle_execution-/Uniform-Policy.
3. Neue Identität/Code-/Input-/Kataloghashes, zentrale neue Seedreservierung,
   persistente Zähler und Deadline sowie reproduzierbaren Analysecode publizieren.
4. Alle16Zellen,16A/A-Paare und drei negative Probes bestehen; jeder Hauptlauf
   bekommt denselben vollständigen Eingabe-/Identitätsaudit.
5. Independent Reviewer prüft Kontrastzeichen/Skalierung, Holm8 und Power;
   erst dann technische Gatefreigabe und separate Ausführungsentscheidung.

**Tatsächlich geprüft in diesem Teilauftrag:** Quellpfade/Profilfeldgrenzen und
Experimental-API lesend nachvollzogen; angegebene Sourcehashes berechnet;
Power-/Breitentabelle offline ausgeführt. Keine native Wirksamkeitsprüfung und
keine neue Repositorytestsuite als bestanden behauptet.0nativeStarts/0Seeds.
Ein zunächst vermuteter Headerdateiname existierte nicht; die korrekte Datei
`native_execution_experiment.h` wurde anschließend geprüft, keine Mutation.

**Offen:** rohe Schärfeskalierung, Bedeutung beider Felder, dynamische Wechsel-
und Zustandsbelege, passive vollständige Effektivitätsrecords, Streuung neuer
Kontraste, reale Kader-/Kontextübertragbarkeit. Schärfeeffekte im Einzelmatch
sind keine Trainings-/Verletzungs-/Karriereentwicklungseffekte.

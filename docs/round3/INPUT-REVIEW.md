# ATTR-009 – unabhängige Prüfung der konkreten Eingaben

14.11.2026, nach zentraler Vorbereitung und vor technischen Vollmatches.
**Inputgate bestanden; 32 technische Vollmatches plus eine Negativprobe dürfen
nach erfolgreicher Vorregistrierungs-CI zentral erfolgen. Keine Hauptfreigabe.**
Reviewer startet keine nativen Prozesse, reserviert keine Seeds und verändert
weder Eingaben noch Registry, Runtime oder eingefrorenen Autorencode.

## Direkt geprüfte konkrete Artefakte

Alle24 privaten absoluten FM27CFG1-Binaries selbst decodiert und vollständig
mit den tatsächlichen vier früheren D00-Binaries verglichen. Je5557Records;
eigene Sollmatrix bildet aus den logischen IP/OOP-Zellen die aktive
Positionsfamilienvereinigung und bindet sie über die tatsächliche Startelf an
Rosterplätze. Keine Autorenfunktion zur Erzeugung dieser Sollwerte importiert.

Ergebnis: pro Zelle genau10 bzw.126 erlaubte Kind1-Attributänderungen,
**0 nicht deklarierte Recordänderungen**. Roh60→80 trifft jeweils genau
JumpingReach54/Acceleration49/Pace53 bei zehn Startfeldspielern. Spezialisierte
ungenutzte Feldfamilien1, aktive Familien20; Omni20. GK/Sweeper, Torwart,
Bank, Gegner, alle Profile, Team Instructions, beide Phasen, Rollen, Duties,
PI, Standards und Managementrecords bleiben außerhalb des deklarierten
Eingriffs exakt gleich. Auswärtsträger26/23 aktive bleibt erhalten.

Alle24 vollständigen JSON-Konfigurationen zusätzlich gegen eine unabhängig
gebildete D00-Kopie mit ausschließlich diesen Änderungen geprüft. Manifest-
Rosterbindung, logische IP-Zelle und seitenspezifischer nativer OOP-Slot sowie
aktive DC-/DM-/MC-Familien stimmen. Binärhashes stimmen mit `inputs.json` und
Vertrag; Maskmanifeständerungen entsprechen exakt der eigenen Sollmenge.

## Neue Seeds und Freeze

7957 tatsächlich gelesene historische JSON-/JSONL-Dateien aus öffentlichem
Archiv, Registry und bisherigen lokalen Forschungsserien geprüft; eigene
ATTR-009-Dateien/Reservationen bewusst ausgeschlossen. Das unabhängig gebildete
Ausschlussset enthält **2418** eindeutige Werte einschließlich gesperrtem0 und
stimmt vollständig mit `excluded-seeds.json` überein. Kanonischer SHA256:
`3117bfe338832bea83826c16174fbcfd2d6f0aa108961c6d0553820904bfae46`.

Alle34 reservierten Seeds sind eindeutig, gültig und disjunkt:2 technische und
32 wissenschaftliche,16 je bekanntem Kontext. Öffentliches Seedplanobjekt
entspricht der privaten unveränderlichen Registryreservation. Keine neuen
Seeds, Ersatzseeds oder Holdoutausführung durch den Reviewer.

Alle13 eingefrorenen Autorencodehashes und sieben öffentlichen Artefakthashes
gegen die tatsächlichen Dateien erneut geprüft. Vertrag entspricht der vorher
geprüften384-Match-/32-Block-/Holm5-Variante; kein Baselinearm oder Scopewechsel.
Konkreter Vorregistrierungspush laut zentralem Gitstand:
`fc14746685f0a1f6475b1968912317d9ffabdfb6`. Dessen erfolgreicher CI-Abschluss
ist vor technischem Start separat zu belegen; der Inputreview ersetzt ihn nicht.

Vorbereitung kostete11,1898 von600s Childbudget. Die feste1200s-Frist endet
**2026-11-14T17:00:36.422962+00:00** und umfasst Publikation, CI und Review.
Keine Budgetrücksetzung, keine Änderung am Ablauf oder Eingriff genehmigt.

## Reproduzierbarkeit und nächstes Gate

Die eigene neue `inputs`-Funktion in `analysis/review_round3.py` erzeugt nur
Zähler/Hashes und keine privaten Pfade, Spieleridentitäten oder Rohspielbytes.
Sie importiert keinen Autorencoder, Projektanalyser, Runner oder `research.stats`.
Fünf eigene Reviewer-Tests und `git diff --check` bestehen weiterhin.

Dieser Bericht beweist vorbereitete Eingaben, **noch keine native Annahme**.
Erst tatsächliche32Logs/Dumps prüfen69Attribute/1058Profile/44Phasezellen/
748PI-Gruppen je Match, Originalvorbereitung, effektiveSeeds, natürliches Ende,
acht exakte A/A-Wiederholungen, Exit108-Negativkontrolle, Budget und Publikation.
Danach eigene Entscheidung in `TECH-REVIEW.md` vor irgendeinem Hauptmatch.

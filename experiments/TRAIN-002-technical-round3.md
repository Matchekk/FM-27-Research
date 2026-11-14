# TRAIN-002-R0 – Reader-, Teilnahme- und Replikatfundament

14.11.2026 · **technische Offlinevorarbeit abgeschlossen; Karriereversuch blockiert**.
Kein Trainingseffekt, keine neue Rangfolge. [Auftrag](NEXT-ATTR-MECH-TRAIN-round3.md),
[Fachbericht](../docs/round3/TRAIN.md), [Diagnosen](../data/train-002-technical/README.md).

## Identität und unveränderte Quellen

Die installierte DLL wurde ausschließlich als Datei gelesen: FileVersion27.0.1,
ProductVersion27.0.1+2503222, SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Kein Hoststart und kein Test der Karrierekompatibilität aus dieser Prüfung.
Installierter Save-Reader ist **fmsave0.9.0**, wie beide Requirementsdateien
vorsehen. TRAIN-001 nennt dagegen fmsave0.10.0 und Build27.0.0+2493426;
dieser historische Bezug bleibt erhalten und wird nicht als aktueller Erfolg ausgegeben.

Vier öffentliche TRAIN-001-Dateien vollständig gelesen; ihre Dateibyte-SHA256
stehen in [archive-diagnostic.json](../data/train-002-technical/archive-diagnostic.json).
Die Rohzeilen enthalten Deltas, keine vollständigen Start-/Endprofile oder
heutigen Decoderreceipts. Keine private Save-Datei gesucht oder geöffnet.
Die tatsächlichen lokalen fmsave-Quelltexte wurden statisch gelesen; Version,
SHA256 und ausgewählte Modellfelder dokumentiert
[reader-inventory.json](../data/train-002-technical/reader-inventory.json).
Keine Paketinstallation, kein Upgrade, kein fremder Code geändert/importiert.

## Implementierter Vertrag

`research/training002.py` liest ausschließlich unser normalisiertes
`train002.checkpoint.v1`-JSON, **kein proprietäres .fm-Format**. `.fm` wird vor
dem Öffnen abgewiesen. Maximal2MB, doppelte Schlüssel, NaN/Infinity,
unbekannte Felder, boolesche Zahlen, widersprüchliche Einheiten, Duplikate und
Hashmismatchs werden abgewiesen. Keine Datenbanksuche, keine Saveänderung,
kein Executor, keine Registry- oder Leaseänderung.

Pflichtmetadaten: schema/origin/build/decoder, Start-/Checkpointhash,
replicate/arm/day, RNG-Claim, Coaches/Anlagen/Kader/Gegner/Policy,
Kalender, Teilnahme, Spieler und Verletzungen. Listen dürfen ausdrücklich
`null` sein. Ein leeres Array ist nur eine deklarierte leere Sammlung,
kein Nachweis vollständiger Quelle. Leerer Kader/Kalender wird als Missing
gemeldet; vollständige individuelle Abdeckung wird separat gezählt.

Jeder Messwert ist entweder `null` oder
`{value,unit,source_sha256,locator}`. Der explizit bereitgestellte lokale
Quellpfad wird tatsächlich rein lesend gehasht, nicht in das Ergebnis exportiert.
Ein Hash belegt **Bytes, keine Feldbedeutung oder native Wirksamkeit**.
Locators bleiben unvalidierte Extraktionsclaims, bis ein unabhängig geprüfter
Adapter sie gegen echte Quellen bindet. `origin` erlaubt nur `synthetic` oder
`unvalidated_export`; ein Callerflag oder vollständig ausgefülltes JSON kann
die native/Karrierefreigabe niemals einschalten.

Kalender: Tag/Slot0..2/Sessioncode. Teilnahme: anonymes Kohortenkürzel,
Tag/Slot/Session, tatsächlicher Status (attended/rest/rehab/cancelled/absent),
Minuten und Coach. Geplante Slots allein erzeugen keine Teilnahme.
Individuell: vier feste Roh-/Anzeigeattribute, CA/PA, Condition/Schärfe,
Ermüdung, Matchminuten, Fokus und Intensität, jeweils mit expliziten Einheiten.
Es wird keine unbekannte Rohskala in Anzeigepunkte umgerechnet.
Verletzungen: eigenes Ereignis, Teilnehmer, Beginn/Ende, tatsächliche versus
erwartete Rückkehr und Ursache; erwartete Rückkehr ist keine beobachtete Dauer.
Kalibrierungsdiagnose prüft absolute Roh-/Anzeigepaar-Konflikte, leitet aber
aus wenigen Paaren oder historischen Deltas keine Umrechnungsformel ab.

Replikatdiagnose meldet mehrfach verwendete Startbytes/RNG-Labels und
abweichende Kontrollhashclaims innerhalb eines Paares. Unterschiedliche Labels
oder Savehashes beweisen keine RNG-Unabhängigkeit; verifiziertes unabhängiges n
bleibt `null`. Spieler und wiederholte Wochen werden nie zusätzliche Replikate.
Alle Ausgaben behalten `source_semantics_verified=false`,
`native_released=false`, `career_released=false`.

## Echte technische Ergebnisse

11gezielte Offline-Tests sowie97Repositorytests/5historische Analysetests bestanden;
`git diff --check` ohne Befund. Gezielte Fälle: Belegmismatchs, falsche Einheiten,
Callerflags, native-Origin-Claims, fehlende Teilnahme, Duplikate, falsche Session,
Nichtteilnahme mit Minuten, Verletzungssemantik, RNG-Klone/Kontrolldrift,
JSON-/Dateiformat-Negativfälle und historische660Zeilen.
Die synthetischen Felder existieren nur in temporären Testverzeichnissen und
verleihen keine native Freigabe. Der Archiveingang reproduziert:

| Historischer deskriptiver Kontrast | Rohindex Intervention−Kontrolle | ΔCA-Abstand |
|---|---:|---:|
| Heavy−Conditioning,6Wochen |+0,022727|+0,090909|
| Rest−Conditioning,U19,4Wochen |−0,034091|+0,227273|

Der vierteilige Index ist das Spielermittel aus Antritt/Tempo/Beweglichkeit/Ausdauer,
danach Kohortenmittel. Kein KI/Power aus22Spielern, kein kausaler Gewinnnachweis.
Historische Expositionszeilen sind **kumulativ**: Endcheckpoint statt Summe.
Der erste neue Regressionstest fand eine fehlerhafte Summierung; vor Veröffentlichung
korrigiert. Endstände Heavy/Conditioning14.731/14.801Minuten,4/9Verletzungseinträge;
Rest/Conditioning5.850/5.940Minuten,4/4Einträge. Einträge sind keine Ausfalltage.
660Zeilen sind264Heavyvergleich,176Restvergleich,132Wochenplan und88Pilot.

## Blocker und Abrechnung

Nicht vorhanden/nicht abgenommen: aktuelles reales Reader-/Einheitenmapping,
unabhängige Karriere-RNG/Cluster, tatsächliche individuelle Trainingsteilnahme,
Coach-/Fokus-/Intensitätsbelege, beobachtete Verletzungsintervalle und
Kalenderexecutor mit Originalzustandsreadbacks. Karriere-PKM-Replay bleibt gesperrt.
Ein Readererfolg ist keine Kalenderadvance-/Replayfreigabe.

**Tatsächlich0nativeStarts,0nativeMatches,0Kalenderadvances,0Seeds,
0Karrierearme,0Armwochen.** Kein Hauptjob begonnen, fehlgeschlagen oder ersetzt.
Es wurden keine Karrierejobs registriert; der spätere8Armwochen-Vorschlag bleibt
ausdrücklich Entwurf. Vor Blockerauflösung wird kein Uhrzeitbudget eröffnet.
Bestehende `research/career.py`, TRAIN-001 und sämtliche Archive unverändert.

## Exakter nächster technischer Auftrag – noch nicht freigegeben

Ermittle zunächst eine explizit benannte erlaubte private Startdatei und dokumentiere
Quelle/Build/Readerhash. Validiere einen **read-only** Export durch unabhängige
UI-/zweite Quellbelege für Roh-/Anzeigeeinheiten, individuelle absolvierte Einheiten
inklusive Ausfälle, Coaches/Fokus/Intensität und tatsächliche Verletzungszeiträume.
Belege zwischen Replikaten Karriere-RNG-/echte Clusterunabhängigkeit; ein neues
Matchseedlabel genügt nicht. Falls nicht möglich, Readerstatus mit Missing
publizieren und ohne Advance stoppen.

Erst danach separaten technischen Vertrag/Code/Review/CI veröffentlichen:
höchstens2unabhängigeA/A-Paare×2Arme×2Wochen=8Armwochen,
12Checkpoints einschließlich Starts, ein serieller Karriereexecutor,
30Minuten unverrückbares Gesamtfenster samt persistentem Advancezähler und
globaler NativeLease. Keine Neustart-/Retrybudgets oder Ersatzreplikate.
Kalender-/Input-/Identitätsfehler stoppen; alle unbegonnenen Wochen erhalten.
Dieser Auftrag autorisiert weder diesen Benchmark noch die spätere32Arm-Studie.

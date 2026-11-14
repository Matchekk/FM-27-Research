# Externer Replikationsaudit: unabhängiger Quellenreview

14.11.2026, eigene Originalzugriffe ab21:15UTC. Geprüft wurde der neue Audit aus
`6610b81` (Fachcommit `7ad703e`). **Kein korrigierender Sachbefund erforderlich.**
Quellenbindung, neun bedingte SD-Näherungen und die begrenzte Interpretation
sind nachvollziehbar. Eine unabhängig ausgeführte externe Rohdatenreplikation
unserer Studien wurde auch durch diesen Review nicht gewonnen.

Die tatsächlichen drei Auditdateien stimmen mit ihren Gitblobs überein.
LF-SHA256 des Registers:
`38d4e595ed65c14c00f2c5d541cd3e5259b7d07b3461cfe27b91274a1fb610f4`;
des [Auditberichts](EXTERNAL-REPLICATION-AUDIT.md):
`8ee4e234b9ce881bbc3af7878a8281b116ebb925314e88665310b1f7fbd8ae2a`.
Neun Registereinträge gehören zu drei benannten Provenienzfamilien;
Seiten-/Codezahl und Zahl unabhängiger Replikationen sind unterschiedliche Größen.

## Originale und genaue Versionsgrenze

Alle18 verschiedenen registrierten Gitblob-SHA1 wurden unabhängig aus den
tatsächlichen Originalbytes mit dem Git-Header `blob <length>\0` nachgerechnet.
Macquellen sind an `e92cf1416ca5c8c4b13009f8cf7d695f290b0368` gebunden,
Editor-Notizen an `c597c89fc4f41b9bf9fd5e12fc6a71045f97c6b6`. Berichte und
zugehöriger Ausführungs-/Analysecode wurden gelesen und nicht ausgeführt.
Ein Sourcecommit belegt nicht die tatsächlich damals verwendete Engine- oder
Hostdatei; die im Register unbekannten Runidentitäten bleiben unbekannt.

HarvestGreens [Originalbeitrag](https://sortitoutsi.net/content/78219/fm27-attribute-test-tactical-understanding-training-system-preset-tactics-ai-reverse-engineering-engine-for-test)
trägt das angezeigte Datum04.11.2026. Seine Saison-/Spieler-/Dosisbeschreibung
passt zur Zusammenfassung;51.000 ist eine genannte Mindest-/Nominalgröße,
keine durch Originaljobs hier nachgezählte Fallzahl. FMRTE-Locks benannter
Zustände beweisen weder konstante Attribute über zwölf Monate noch tatsächlich
eingetretene Entwicklungsstörungen. Das verlinkte Workbook wurde nicht geladen.

Die [Editorquelle](https://github.com/barak14/fm-editor/blob/c597c89fc4f41b9bf9fd5e12fc6a71045f97c6b6/docs/fm27/memory-layout.md)
enthält anderswo genaue Build-/Modulbelege, bezeichnet die betreffenden
Condition-/Sharpness-/Fatigue-Leads jedoch weiterhin als ungeprüft. Ihre
Live-PLAYER-Struktur und UIbeobachtungen validieren keine MATCH_PLAYER-Caches
unseres Adapters und keine lokale Prozentkalibrierung.

Der vollständige Mac-Gitbaum wurde separat über die GitHub-API gelesen:
176Einträge, `truncated=false`, keine getrackten JSONL-Reihen oder erkannten
Jobresultattabellen/Design-NPZ. Eine Ergebnisgrafik und ein C++-Resultatheader
existieren; deren Dateinamen sind kein Ersatz für Jobrohdaten. Der Befund gilt
für diesen getrackten Baum. Releases, ignorierte Dateien und andere Speicherorte
wurden nicht vollständig inventarisiert.

## Alle neun SD-/Rundungsrechnungen

Die drei Attribute und neun Mittel-/t-Werte stimmen mit der
[Originaltabelle von Mac02](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/02-real-vs-levelled.md)
überein. Der [Originalcode](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study2_levelled.py)
bildet `(plus-minus)/2` und berechnet seinen t-Wert als Mittel durch
Stichproben-SD/√n. Unter der angenommenen Zahl300 tatsächlich verfügbarer Paare
folgen die invertierten SD-Näherungen in xGD dieses Halbdifferenzkontrasts:

| Arm | Pace | Acceleration | JR |
| --- | ---: | ---: | ---: |
| A | 0,795807 | 0,753763 | 0,718167 |
| B | 0,781121 | 0,725812 | 0,702861 |
| C | 0,351091 | 0,341162 | 0,384900 |

Alle neun SEs, SDs und18 Rundungsgrenzen stimmen bis auf numerische
Gleitkommatoleranz. Die Randformeln verwenden Mittel±0,005 und t±0,05;
sie beschreiben ausschließlich angezeigte Rundung. Dies sind weder neue
Konfidenzintervalle noch verifizierte lokale Stichproben-SDs. Das Algebraergebnis
bestätigt auch keine Unabhängigkeitsannahme des ursprünglichen Standardfehlers.
Kreuzkovarianzen für JR-minus-Speed oder den lokalen Maskeninteraktionskontrast
fehlen; lokale Power lässt sich daraus nicht ableiten.

Mac02 übernimmt ArmA aus Mac01; der Wechsel zuC ändert mehrere Kontextmerkmale
gleichzeitig. Er isoliert keinen Positionsmaskeneffekt. Die gelesene
[Dosisanalyse](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/dose_response.py)
verwendet tatsächlich eine Kovarianzmatrix gemeinsam referenzierter Dosen in
GLS und durchsucht Knickpunkte. Die vorsichtige explorative Einordnung im Audit
ist angemessen. Fehlende Heterogenität in Mac14 begründet keine Äquivalenz.

## Seeds, Schärfepaket und Missing Pairs

Im [Originalgenerator von Mac13b](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/random_study.py)
folgt das Setting `c % 16` und der Engine-Seed `c // 16 + 1`.
50.000Konfigurationen ergeben3.125 verschiedene numerische Seeds; Setting/Seed
bleibt eindeutig. Gemeinsame Zahlen beweisen weder identische Ereignisfolgen
noch empirische Fehlerkorrelation. Eine effektive Fallzahl3.125 oder umgekehrt
50.000 unabhängige Fehler lässt sich daraus nicht festlegen. Der Code verwendet
homoskedastische OLS-Kovarianz und blockweise Split-Hälften; das ersetzt keine
extern geprüfte Rohdatenreplikation oder kontrollierte Mehrfachtestbestätigung.

Der [Mac05-Encoder](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_everything.py)
verändert beide benannten Sharpnessprofilfelder gemeinsam für den gesamten
aktiven Kader einschließlich GK und Bank. Der
[Bestätigungscode](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/study5_confirm.py)
nimmt für diese Auswahl ausschließlich100% auf neuen Seeds31–120 gegenüber
Natural auf.50/75%-Arme bleiben Screeningergebnisse. Andere Baseline, Dosis,
Kaderumfang und Plattform verhindern die Gleichsetzung mit unserem gemeinsamen
7000/10000-Paket bei zehn Startfeldspielern. Einzelne Consumer, Vermittlungswege
oder eine UIskala werden durch die gemeinsame Feldänderung nicht identifiziert.

Der [Originalrunner](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/port/validation/overnight.py)
kann ein fehlgeschlagenes Match überspringen und fortfahren. Die gelesenen
Analysen schneiden verfügbare Paarschlüssel beziehungsweise vollständige
Dosiszeilen. Das begründet eine Anforderung an Originaljobs und Logs. Ohne sie
ist weder eine reale Ausfallzahl noch selektives Missingnessverhalten bewiesen.
Der Audit hält diese Grenze korrekt ein.

## Reproduzierbarer Prüfumfang und Abschluss

Eigener zusätzlicher Auditor:
`analysis/review_external_replication001.py`, optional `--online`.
Offline prüft er Registergrenzen und neun Rechnungen; online liest er18
unveränderlich adressierte Originaldateien und den176er-Gitbaum. Externe Source
bleibt im Speicher und wird nicht importiert oder gespiegelt. Für die Baumabfrage
wird der konfigurierte GitHub-Client genutzt: der lokale Python-APIzugriff
scheiterte an seiner Zertifikatskette; TLS wurde nicht deaktiviert.

Der vollständige Onlineprüflauf und drei eigene Regressionen bestanden,
einschließlich Ablehnung einer falschen SD, einer erfundenen Rohreplikation und
eines falschen Gitblob-Hashes. Zusätzlich340NIGHT- und272Round3-Archivdateien
unverändert. Nur neue eigene Review-/Prüfdateien; keine Änderungen am Autorbericht,
Register, bestehenden Daten oder laufenden Experimenten. Native-/Save-/Seed-
und Registryaktionen dieses Reviews jeweils0. Kein Kontakt zu Quellenautoren.

Bestätigt ist die Nachvollziehbarkeit dieses begrenzten Quellenaudits. Andere
benannte Autoren/Programme, zugänglicher Code und autorinterne neue Seeds werden
weiterhin von unabhängig nachvollzogener Datenerhebung/Replikation getrennt.
Der Audit begründet keine Änderung laufender Verträge oder neue Ausführung.

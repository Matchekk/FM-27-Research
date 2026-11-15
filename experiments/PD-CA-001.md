# PD-CA-001 – retrospektiver CA-Proxytest eines öffentlichen GK-Exports

15.11.2026 · Protokoll vor eigener Modellanpassung und Holdout-Auswertung.
**Explorativ und beobachtungsbasiert**, keine native Studie/Seedreservierung.

Neue Quelle `PD-EXT-SCOUT-CA`: [Scout Reporter potential.ts](https://github.com/SebastianFoder/fm-scoutreporter/blob/3144dd0a45eb4f994230700c8faee64d33665273/packages/core/fm27/potential.ts)
berichtet ein lineares GK-Modell mit109Profilen und ungefähr2,48CA-RMSE im
Gesamtsample. Die zugängliche Fixturedatei
`packages/core/fixtures/attribute-fm27-hidden.csv` enthält109Zeilen;
`attribute-fm27.csv` enthält dieselbe Anzahl ohneCA, `attribute-fm27-outfield.csv`
74Zeilen ohneCA. Nur die Hidden-Datei wird benutzt; keine Doppelzählung.

Nutzerklasse `METHODOLOGY_BLOCKED` für **tatsächliche Grenzkosten** bleibt;
Archivklasse `UNCERTAIN_SOURCE`. Für die engere Frage „Wie gut sagt ein
gewichteter Attributsummenproxy exportierte CA-Zahlen voraus?“ ist eine
retrospektive Auswertung möglich. Atlas/Index/FINDINGS und MAC-20/13B geprüft;
Überlappung fm-scoring-CA-Tabelle, keine eigene Kostenintervention. Der Autor
hat dasselbe Gesamtsample bereits untersucht: **keine neue unabhängige
Bestätigungskohorte**. Zusätzliche Information ist eine explizite spielergetrennte
Diagnose gegen gleich komplexe Baselines, Fehler/Kalibrierung und Unsicherheit.

## Daten, Einschluss und Provenienz

Unveränderlicher Commit3144dd0, Rohquelle nur im ignorierten lokalen Cache;
öffentliche Ausgabe enthält URL, SHA256 und Aggregate, keine Namen, IDs,
Spielerzeilen oder Original-CSV. Öffentlich bereitgestellte Fixture ist kein
privater Nutzersave. FM27-Herkunft ist ein Autorenclaim; exakter Build, Save,
Vereins-/Savecluster, UI-/Editor-Goldbelege und Roh-/Anzeigemapping sind lokal
nicht unabhängig abgenommen. Kein Karriereadvance, kein Savezugriff.

Alle109Zeilen prüfen: eindeutige nichtleere Unique ID, Position exaktGK,
CA1..200,22gelistete GK-Tabellenattribute vollständig numerisch1..20.
Fehler behalten mit Zeilennummer/Grund; kein Nullersatz. Eine doppelte ID
stoppt die Auswertung. Ohne ausreichend vollständige Daten nur Datenqualitäts-
bericht, keine Modellleistung. Ziel≥1.000über mehrere Kontexte ist nicht
erreicht; diese kleinere einzelne Fixture eignet sich nur zur Pilotdiagnose.

## Eingefrorene Aufteilung und Modelle

Spieler nach SHA256(`PD-CA-001/player-split/v1:`+UniqueID) sortieren;
erste80für Training, restliche29für diagnostischen Holdout, sofern alle
109zulässig. Keine Identität in beiden Mengen. Split ist ein Offline-Salt,
kein Engine- oder Karriere-Seed. Bei weniger als109zulässigen Zeilen stoppen,
keine adaptive andere Aufteilung. Namentliche Listen werden nicht publiziert.

Modell W: OLS `exportierte CA = a + b·Σ(w_j·Attribut_j)` mit den22gelisteten
GK-Gewichten der eingefrorenen fm-scoring-Tabelle.
Baseline U: OLS auf einfachem Mittel **derselben22Attribute**, ebenfalls
Intercept+Slope, gleicher Trainingssatz; keine nachträglich optimierten Features.
Baseline C: konstantes Trainings-CA-Mittel. Das ist ein CA-Zielproxy und
**kein Matchleistungsmodell/Meta-Score-Vergleich**.

Einziger primärer deskriptiver Vergleich: Holdout-MAE(W)−MAE(U).
Keine formale Bestätigungshypothese/p-Wert-Suche. Zusätzlich MAE/RMSE/Bias,
Kalibrierungsintercept/-slope für feste Holdoutprognosen, Trainingsfehler und
alle Baselines. 20.000gepaarte Spieler-Bootstrapreplikate der29Holdoutfehler,
fester RNG2026111541. Intervalle sind bedingt auf diesen Split, dieses
Trainingssample und Austauschbarkeit der Exportspieler, nicht auf neue Saves.
Keine Clusterkorrektur nach Save/Verein möglich: entsprechende Metadaten fehlen.
Trainingsunsicherheit ist in diesen Intervallen nicht enthalten.

Mögliche Modellableitung `b·w_j` wird ausschließlich als **bedingte lineare
Proxy-Ableitung** bezeichnet. Kein kausaler Grenzpreis, keine Editor-RCA-
Validierung, keine Niveau-Nichtlinearität oder Fuß-/Mehrpositionsidentifikation.
109Profile erlauben keine allgemeine Outfieldfunktion. Vorab bekannte externe
Gesamtsamplekorrelation ist keine eigene Holdoutgenauigkeit.

Code `analysis/ca_profile001.py`, getrennte OLS-Nachrechnung via NumPy,
Testfälle für Leakage/Duplikate/fehlende Werte und bekannte synthetische
Regressionsbeziehungen. Ergebnis/Manifest unter `data/player-development-001-ca/`.
Keine synthetischen Profile werden als reale Validierungsdaten verwendet.

# CA-003 – kein unabhängiger Editor-RCA-Goldwert verfügbar

**INDEPENDENT_EDITOR_RCA_UNAVAILABLE**, 15.11.2026. Null zulässige
Goldbeobachtungen; kein Pilotfall und keine Hauptserie gestartet.
[Vertrag](../../experiments/CA-003-GOLD.md), [Zugangscheck](RESEARCH_REPORT.md).

| Gate | Beobachtung |
|---|---|
| FM27 vorhanden | Prozess/Fenster und Installationsdateien vorhanden |
| Separater Editor | In begrenzter Installations-/Prozessinventur nicht gefunden |
| Ingame-Editor zugänglich | UNKNOWN: AX nur Pane, beide Bildcaptures Timeout |
| Unabhängig berechnete RCA | Nicht nachgewiesen |
| CA und RCA getrennt | Kein gemeinsamer verifizierter Readback |
| 40 rohe Attribute | Quellschemas vorhanden, kein vollständiges neues Goldprofil gemessen |
| Beide numerischen Füße | Quellschemas vorhanden; kein neuer kalibrierter Readback |
| Alle 15 Positionsratings | Modell vorhanden; kein neues vollständiges Goldprofil |
| Spiel-/Editorbuild | Installations-DLL gemessen; Editor-/Runtime-/Savebuild unbekannt |
| Reproduzierbarer Export | Kein vollständiger Input+Gold-Export mit unabhängiger Herkunft |

Die [Scout-Funktion](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/apps/desktop/src/lib/ca.ts)
und ihr Rust-Pendant gehören derselben rekonstruierten Quellenfamilie an.
Ein zweiter Aufruf oder Port validiert keine Engine-RCA. Der öffentliche
[Savertest](https://github.com/shlk20/fm27-scout-code/blob/084d7f0a18ac790d7c4087c5b6bdff008186d4fa/crates/fm27-core/tests/ability_real_save.rs)
vergleicht weiterhin gegen gespeichertes CA. Alte 109 GK-Exporte haben keine
belastbaren numerischen Füße; sie wurden nicht erneut analysiert.

Ein Drittanbieterlabel reicht ebenfalls nicht: [FMRTE erklärt RCA als eigene
Schätzung anhand konfigurierbarer Ability Weights](https://docs.fmrte.com/players/ability/).
Dies weist weder Identität mit Engine-RCA noch Unabhängigkeit vom Scout-
Algorithmus nach. Talent Seer/FMAX bleiben ohne überprüften lokalen
Herkunfts-/Exportnachweis ungeeignet; keine neue Software installiert.

## Ergebnisabrechnung

Eindeutige Basisprofile 0; zulässige Gold-Vor-/Nachzustände 0; Interventionen 0.
Exakte Treffer **null bei Nenner 0**, MAE/RMSE/Bias/Maximalabweichung **null**;
keine Fehlerverteilungen nach Position/Niveau/Füßen/Mehrpositionen,
Deltaübereinstimmungen oder Vorzeichenkonflikte messbar. Kein „0 Fehler“-Claim.
Keine Goldzeile ausgeschlossen: Es wurde keine erhoben. Die GUI-Zugriffsfehler
sind technische Fehlversuche, keine fehlgeschlagenen Spielerinterventionen.

Der reine Comparator-Smoke wiederholt den alten Inputhash
`adcc18e56c86abcd967443d80df75903c4cb00ace68e27bb71d832738bf7e6f6`:
MODEL_RCA 107, EDITOR_RCA/STORED_CA null. Damit ist nur die vorhandene
Software ausführbar. Die 12 gezielten Fälle sind eine **unbefüllte Übergabe**;
die zusätzlichen 48 werden erst nach bestandenem Goldpilot vorregistriert.

Absolute Exaktheit, Modellfehler und tatsächliche marginale CA-Kosten bleiben
unbekannt. Selbst eine künftige statische RCA-Validierung beweist noch keine
Kosten-/Entwicklungswirkung nach Karrierefortschreibung.

# Spielerentwicklung001 – Forschungsstand

15.11.2026 · Ausgangsarchiv3cd4317, neuer Branch `codex/player-development-001`.
Der Arbeitsbaum war sauber und origin/main identisch; tatsächlicher Fetch und
GitHub-Remoteprüfung durchgeführt. Alle angeforderten Einstiegspfade existieren.

Entscheidung: Rollen×Attributinteraktion ist jetzt wissenschaftlich ausführbar.
CA-Kostenquellen werden daneben geprüft. TRAIN/PA sind durch fehlende validierte
Karriereteilnahme, Replikat-RNG und Längsschnittdaten blockiert; keine Saveöffnung
oder Kalenderfortschreibung. Keine Readerreparatur und kein neuer VALID-Bereich.

[PD-ROLE-001](../../experiments/PD-ROLE-001.md) ist vorregistriert, Inputs/Seeds
vorbereitet und offline geprüft. **Noch0 neue wissenschaftliche Matches.**
Die technische Native-Freigabe und erfolgreiche exakte CI stehen noch aus.
4.096 ist die feste wissenschaftliche Programmobergrenze, kein Ergebnis.

Architektur: deklarierte binäre Rollen-/Attributänderung → bestehender kalter
Host mit Originalreadbacks und Containment → unveränderliche private Belege →
erlaubter öffentlicher JSONL-Export → gepaarte Blockstatistik und Skalarprüfung.
Bestehende Runner, Datenschemata und historische Studien bleiben unverändert.

Meilensteine: (1) veröffentlichte Vorregistrierung/CI, (2)32Technikmatches und
Negativprobe, (3) nur nach Freigabe feste Hauptserie, (4) Nachrechnung,
sechs Fachberichte, getestete Modelle, Veröffentlichung/Integration.

[Quellenabgleich](LITERATURE.md) · [Abrufe/Versionen](source-audit.json).

## Abgeschlossener technischer Abschnitt

Vorregistrierung197527d und [exakte CI43734775642](https://github.com/Matchekk/FM-27-Research/actions/runs/43734775642)
bestanden. Tatsächlich32vollständige Technikmatches,16exakteA/A und eine
erwartete Exit108-Abweisung. Alle16Zellen native geprüft; vollständiger zweiter
Pass gegen unveränderte private Rohbelege nach Prozessbereinigung bestanden.
28,471s beaufsichtigte Technikphase; Peak4Claims, keine Ausfälle/Retry.
Kein wissenschaftlicher Effekt aus Technikdaten geschätzt. Hauptserie noch
unbegonnen; es folgt die Veröffentlichung dieser konkreten Freigabebelege.

Die Dispatcherreihenfolge ist wie im bestehenden Runner sortiert nach
Kontext/Seed; die vorgelagerte Planmischung ändert sie nicht. Alle acht Zellen
eines Blocks bleiben zusammen. Keine datenabhängige Blockreihenfolge.

## Neue empirische CA-Exportauswertung abgeschlossen

PD-CA-001:109bereitgestellte GK-Exportprofile,80Trainingsspieler und29fest
getrennte diagnostische Holdoutspieler. Gewichteter Summenproxy W erzielt
MAE1,606 gegen4,630 einer gleich komplexen ungewichteten OLS; Abstand−3,024,
bedingtes95-%-Bootstrapintervall[−4,139;−1,908]. Keine Missing/Duplikate/
Ausschlüsse. Getrennter OLS-Löser bestätigt beide Koeffizientenanpassungen.
**Explorativ, vorher vom Quellautor analysiertes Gesamtsample, Build-/Save-
Provenienz ungeprüft, CA-Spanne15–118.** Keine tatsächliche Grenzkostenfunktion,
kein Transfer auf Feldspieler oder zukünftige Entwicklung.
[Vollständige Ergebnisse](CA_EFFICIENCY.md#pd-ca-001-zusätzliche-empirische-exportdiagnose).

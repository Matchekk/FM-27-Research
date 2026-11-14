# ATTR-009-Bridge – tatsächliche technische Validierung

14.11.2026. Build27.0.1+2503222, Tactics Lab v1114.6,
Adapter `fm27_desktop_8c6971ce_adapter_v1`. Identität und sämtliche eingefrorenen
Sources/Eingaben stimmen mit [Vertrag](../data/attr-009-bridge/contract.json)
und [Inputs](../data/attr-009-bridge/inputs.json) überein. Keine neue allgemeine
Freigabe von VALID-003, Karriere, Schärfesettern oder passiver Effektivitätsmessung.

Vorregistrierung/Code/konkrete Inputs/34neueSeeds wurden in
`fc14746685f0a1f6475b1968912317d9ffabdfb6` veröffentlicht; CI43616995356
war vor dem ersten Technikmatch erfolgreich. Die vorherige Code-CI43616762281
war bereits vor der zentralen Vorbereitung erfolgreich. Der unabhängige
[Inputreview](../docs/round3/INPUT-REVIEW.md) prüfte alle24Binaries vollständig
gegen D00 und eine eigene Interventionsmatrix sowie den Seed-Ausschlussscan.

## Reale Ergebnisse

| Kontrolle | Tatsächlich beobachtet |
|---|---|
| Technische Vollmatches |32/32 gültig,24 unterschiedliche Eingabezellen |
| A/A |8/8 OJ-/SJ-Paare exakt in Score,Endtick,Teamstatistik,Setup und Seed |
| Native Eingaben je Match |46aktive Identitäten/69Attribute,1058Profilfelder,22tatsächliche Spielerbindungen in2Phasen,44Positions-/Rollen-/PI-Zellen und748PI-Gruppen |
| Rohdosis |24Zellen mit zehn nativen60/80-Vor-/Nachvergleichen aus den vorbenannten Geschwisterarmen; alle Sollwerte passen |
| Negativprobe |Ungültiges Binärformat mit Exit108 abgewiesen,kein natürliches Matchende |
| Fehler/Retry/Ersatz/Exklusion |Je0 |
| Hauptmatches zum Technikabschluss |Alle384unbegonnen |

Alle32Logs und Dumps bleiben privat; öffentliche Messungen und SHA256 in
[technical.jsonl](../data/attr-009-bridge/technical.jsonl),
[Zusammenfassung](../data/attr-009-bridge/technical-summary.json),
[vollständigen417Versuchsplätzen](../data/attr-009-bridge/job-accounting.jsonl)
und [Negativkontrolle](../data/attr-009-bridge/negative-control.json).
Kein öffentlicher Dump mit Spieleridentitäten oder Spielmaterial.

## Dauerhafte Ressourcen und Freigabegrenzen

Vorbereitung11,1897836s plus Technik19,7699405s = **30,9597241/600Child-Sekunden**.
Studienfenster bis Ende der Technik200,071489/1200s; feste Frist
**14.11.2026 18:00:36,423CET** unverändert. Reservierte33Technikplätze werden
nicht zurückerstattet. Ein zentraler Supervisor je Phase,NativeLease,4Worker,
90sFortschrittsgrenze,2GiBprivateArtefakte/20GiBfreierSpeicher. Keine parallele
MECH-Ausführung,kein Kalenderadvance,keine Holdouts.

Roh60→80 ist geprüft; eine entsprechende FM-Anzeige12→16 ist nicht identifiziert.
Passive abgeleitete Effektivität bleibt nicht messbar ohne verbotenen Eingriff;
der vorregistrierte totale Masken×Rohattributkontrast bleibt von kausaler
Mechanismuszerlegung getrennt.

Hauptfreigabe erst nach unabhängigem Echtdaten-Technikreview und erfolgreicher
CI des veröffentlichten Technikstands. Dieses Dokument allein ersetzt keines
dieser Gates. Code,Analyse,Seedplan und Eingriff werden nach Beginn nicht geändert.

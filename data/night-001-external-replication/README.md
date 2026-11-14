# NIGHT-001: externer Replikationsaudit

[sources.json](sources.json) ergänzt die frühere Evidenzsammlung mit neun
neuen Originalberichten beziehungsweise Codeprüfungen.
[Wissenschaftliche Einordnung](../../docs/night-001/EXTERNAL-REPLICATION-AUDIT.md).
Basiscommit `95d94a4`,14.11.2026. Keine externe Rohstudie lokal ausgeführt.

## Inhalt und Provenienz

- `sources`: Autorangaben, Vergleichsdesign, Population, Dosis, Taktik,
  Zielgrößen, RNG-/Clusterfragen und unbekannte Felder.
- GitHubdateien sind an volle Commits und Gitblob-SHA1 gebunden.
  Das sind keine Transport-SHA256 oder damaligen Engineidentitäten.
- Zugriff hat einen tatsächlichen UTC-Zeitraum. Dynamisches Forum:
  URL/angezeigtes Datum, keine behauptete unveränderliche Version.
- `repository_inventory`: vollständiger176-Einträge-Gitbaum an einem Commit;
  Abwesenheitsbefund ausschließlich für dessen getrackte Dateien.
- `summary_arithmetic`: neun deterministische SD-Näherungen aus gerundeten
  Autorenwerten. Rundungsbereiche sind keine Konfidenzintervalle.
- Unbekannt bleibt `null`; keinerlei Rohmessung wird durch Nullwerte ersetzt.

Alle externen Messzahlen sind Autorangaben. `raw_job_rows_audited=0` und
`independently_reproduced=false` gelten für jede Quelle. Autorinterne
Bestätigung, anderer Autor, verfügbarer Code und extern geprüfte Replikation
sind unterschiedliche Evidenzstufen.

Die MIT-Lizenz des Mac-Codes deckt spielbezogene Daten nicht pauschal ab.
Nur Links, Metadaten, knappe eigene Paraphrasen und Summary-Arithmetik werden
gespeichert. Keine Assets, FMF/PKM/Saves/DLLs, Tabellen-Downloads, Quellkopien
oder personenbezogenen Spieler-IDs. Kein nativer Start, keine Seedreservierung,
kein Karriereadvance; unveränderte historische Archive.

## Lokale Prüfung

Tatsächlich lokal bestanden:

- Neun eindeutige Quellen-IDs, HTTPS-/Commit-/Gitblobformate, Unknown-/
  Nichtreplikationsflags und neun SD-/Rundungsrechnungen direkt geprüft.
- 355 Repositorytests in22,016s, drei private-Goldfälle übersprungen;
  fünf historische Analysetests in0,137s. Harmloses Python-Prozesscontainment
  ist Teil der Tests, keine FM-Host-/Engineausführung.
- Round-3-Archiv:272 Dateien unverändert. NIGHT-001-Archiv:340 Dateien
  unverändert. Keine alte Datei geändert; nur drei neue Auditdateien.
- Dateigrößen, Diff und Veröffentlichungsgrenzen lokal geprüft.

Es wurde kein neuer Auditor implementiert und kein eingefrorener Studiencode
verändert. GitHub-CI für die spätere Integration ist durch den Director zu prüfen.
Push: nicht durch diesen Fachagenten; Director integriert und veröffentlicht.

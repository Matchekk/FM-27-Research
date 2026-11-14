# MECH-002-STARTPOLICY-TECH-V1 – unabhängiger Eingabereview

14.11.2026. Dieser ergänzende Review prüft ausschließlich die konkret
vorbereiteten Artefakte nach dem [Quellen-/Static-Review](STARTPOLICY-002-REVIEW.md).
Kein nativer Aufruf, Karriere-Savezugriff oder Registry-Schreibzugriff durch den Reviewer.
Eine technische Ausführung bleibt bis veröffentlichtem Gate, exakter CI und
zentraler Zulassung gesperrt; keine wissenschaftliche Mainfreigabe.

Die tatsächlichen privaten Binaries wurden unabhängig als `FM27CFG1` mit5557
geordneten Fünf-uint32-Records decodiert. Alle acht Dateihashes stimmen mit
`inputs.json` überein. Die vier10000-Varianten sind byteidentisch zum jeweiligen
historischen D00. Jede7000-Variante entspricht vollständig der selbst neu
gebildeten Erwartung: exakt20 Wertänderungen, ausschließlich Kind15/Felder16
und17, je zwei Werte für die zehn ursprünglichen Feldstarter der getesteten
Seite. Die absoluten Kind11-Lineups wurden direkt aus dem Binary rekonstruiert
und gegen die eingefrorenen JSON-Lineups gebunden. Kein angenommener Slotbereich.

Header, Recordanzahl, Recordreihenfolge und alle übrigen Records sind unverändert.
Damit bleiben Attribute, Torwart/Bank/Gegner, übrige Profile, Positionen, Rollen,
beide Phasen, PI und Versionsrecords gleich. Kein Kind61-Executionrecord wurde
eingeführt. Alle vier ursprünglichen Konfigurationen sind hashgleich zur
abgeschlossenen Observerabnahme. Das belegt Eingabebytes, noch keine native
Wirksamkeit der7000-Intervention nach Originalvorbereitung.

Die Seedregistrierung stimmt zwischen privater Registry, privatem Seedplan und
öffentlichem Seedplan vollständig überein. Historische sowie andere reservierte
Seedwerte wurden unabhängig aus den vorgesehenen JSON-/JSONL-Bereichen neu
inventarisiert:2524 ausgeschlossene Werte, kanonischer Set-SHA256
`72ac0a590b160d830448d26b50e24d5cf6eed060b6b5197441b408c0e0ca54cd`.
Die vier Werte
`1872406977`, `1245076665`, `2075475079`, `999124409`
sind eindeutig, gültige nichtnull-uint32 und disjunkt. Die deterministische
Namespace-/SHA256-Allokation wurde unabhängig neu berechnet und liefert exakt
diese Reihenfolge. Keine Seeds wurden durch diesen Review neu reserviert.

Der Jobplan wurde ohne Projekt-Planfunktion neu gebildet: zwei bekannte
Gegnerkontexte, beide Setupseiten,10000/7000 und je zwei A/A-Läufe ergeben16
Vollmatches. Je Kontext-/Seitenzelle derselbe neue Seed; acht A/A-Paare insgesamt.
Danach genau eine seedlose `negative-malformed`-Probe. Alle17 Schlüssel stimmen
mit der privaten Keydatei überein. Keine Holdoutgegner, Loaderzusatzläufe,
Ersatzseeds oder Erweiterung. Maximal ein Worker, drei begrenzte OS-Prozesse,
90s ohne Fortschritt,180s innere Childzeit und900s festes Studienfenster;
zusätzlich gemeinsamer Nachtmaster und exklusive NativeLease.

Die tatsächlich vorhandenen Original-/Observerhosts, DLL, gebündeltes Fixture,
elf Ressourcendateien, Katalog und sämtliche deklarierten Runtimequellen wurden
neu gehasht und passen zu den eingefrorenen Identitäten. Der private Buildmanifest-
Hash sowie seine C++-/Headerbelege passen zum unveränderten Observerhost.
Alle neuen CODE-Hashes, alte Observer-Releasebelege und beide Reviewhashes stimmen.
Zum Prüfzeitpunkt existierten weder privates technisches Attemptverzeichnis noch
inneres Startpolicy-Budget; es wurden noch keine17Technikplätze ausgeführt.

LF-normalisierte Artefaktbindungen:

| Artefakt | SHA256 |
|---|---|
| inputs.json | `12454c3f2ab76d6a83be908a4266041b555df7346d00cbdfa259dd909a573aa9` |
| seed-plan.json | `d61ccd23db48cb9b86d805185cc96211f15bc555bfdbe0980d52d38dbb8b8806` |
| job-plan.json | `ad268f57a14a453d4e9f7886d3fc35d9597a7270c92931b7470239058ab7b881` |
| Quellen-/Static-Review | `7343dff02d6233e94727ad57cdb5dfe437ef6bf06a82b7739eec5a3ef8541b71` |
| Observer-Ergebnisreview | `7e95cdda0a90947d16121ba91d2a448bb56b1e8a6f87bd813f77fd3b75fe524c` |

Nach Publikation genau dieser Inputs und Reviews darf Root das separate
Reviewgate erstellen, erfolgreiche CI des konkreten veröffentlichten Commits
nachweisen, registrieren und ausschließlich die17Technikproben zentral starten.
Jeder echte Stage-/Cache-/TF-/Seed-/A/A-/Negativ-/Cleanupfehler stoppt die Serie.
Die neue interventionelle Übertragung ist vor diesen Rohbelegen weiterhin
unbewiesen. Anschließend eigener Ergebnisreview; kein Consumer-/UI-, Setter-,
Karriere-, Holdout- oder Leistungsfreigabeschluss aus diesem Eingabereview.

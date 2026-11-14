# NIGHT-002: konkrete Versuchsentscheidung

Stand 14.11.2026, Beginn nach `062fa7e`. Statische Prüfung durch den getrennten
Experiment Agent; **keine nativen Prozesse, Matches, Builds oder Seedreservierungen**
durch diesen Agenten. Director entscheidet und führt allein aus.

Die vorangegangene MECH-002-Serie bleibt abgeschlossen. Ihr positiver gemeinsamer
C90/C7A-Rohpaketeffekt identifiziert keines der beiden Felder einzeln. Der
[Originalbericht Mac05](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/05-everything-else.md)
und sein im lokalen [Reproduzierbarkeitsaudit](../night-001/EXTERNAL-REPLICATION-AUDIT.md)
geprüfter Encoder ändern ebenfalls beide Felder gemeinsam. Eigene FINDINGS,
Studienatlas, JSON-Index, MECH-002-Resultate, ATTR-009, Roadmap und Meta-Score v0.1
wurden vor dieser Entscheidung gelesen. Die aktuelle Quellenfortschreibung
liegt separat in `LITERATURE_AUDIT.md`; die Neuheit gilt ausschließlich innerhalb
der tatsächlich geprüften Quellen.

## Architektur und unveränderte Grenzen

Die versionierte Forschung umfasst reine Recordcompiler, Vertrags-/Seedplanung,
einen zentralen Supervisor, private Native-Belege und öffentliche Matchmessungen.
Das bestehende lokale Observerhost-Original besitzt getrennte Profilsetter für
Feld16/C90 und Feld17/C7A. Sein passiver Observer liest beide nach Originalvorbereitung,
nach tatsächlichem erstem Tickfortschritt und am natürlichen Matchende; zusätzlich
erfasst er den Cache8A. Bestehende globale Library-/Hostdateien werden nicht verändert.

Der neue [Compiler und Audit](../../analysis/split004_design.py) nutzt nur diese
vorhandenen Recordpfade. [Auswertung](../../analysis/analyse_split004.py) und
[Synthetiktests](../../tests/test_split004.py) gehören ausschließlich MECH-004.
Vier tatsächlich vorhandene D00-Eingaben wurden offline gegen den Compiler geprüft:
jeweils20/10/10/0 geänderte Records für LL/HL/LH/HH. Dies ist **keine native
Splitfreigabe**. Ob die Engine unterschiedliche Rohfelder unabhängig erhält,
entscheidet erst TECH32+1 mit separatem Review und veröffentlichter CI.

## Prioritäten nach Messbarkeit und Erkenntnisbeitrag

| Rang | Frage | Neuheit/Mehrwert | Technischer Stand |
| --- | --- | --- | --- |
| 1 | Unterscheiden sich die totalen Wirkungen einer getrennten C90- und C7A-Startintervention? | `NOVEL_HYPOTHESIS`, Überlappung MAC-05/MECH-002, erstmals getrennte Faktoren innerhalb der geprüften Literatur | Originalsetter und drei unabhängige passive Zeitpunkte vorhanden; unabhängige Rohwerterhaltung noch ungeprüft |
| 2 | Ändert ein vorab bestimmtes stürmerloses IP-Paket seine Wirkung bei festgehaltener versus angepasster OOP-Struktur? | Eigene TACT-001/002 untersuchten andere feste Formationen/Rollen; Benchmarkranglisten isolieren diesen Kontrast nicht | Neue Formation/Legalität/OOP-Permutation und gleiche Actor-/Profilbindungen noch nativ abzunehmen |
| 3 | Verändert ein vorab festgelegtes positionsspezifisches Attributprofil den JR-gegen-Speed-Kontrast eines festen ST-Slots? | MAC-13b/Purity/ATTR-009 überschneiden sich; spezifischer Profilmoderator statt weiteres Ranking | VALID-003 ist offline; neue69er-Vektoren, beide Phasen und alle23 Profilfelder benötigen erst eine enge Nativeabnahme |

Der praktische Nutzen des Splits ist zunächst die Interpretation der bereits
belegten Startzustandswirkung und die korrekte Definition künftiger Versuche.
Er ist kleiner als eine unmittelbar übertragbare Taktikentscheidung, aber der
native Messpfad ist wesentlich reifer. Eine Feldbezeichnung oder Cachekorrelation
ist kein identifizierter Engine-Consumer und keine kalibrierte UI-Prozentzahl.

## MECH-004-SPLIT-R0: enger Pilot

- Originalfelder C90 und C7A je7000/10000, zehn Startfeldspieler derselben Seite;
  vier Arme LL/HL/LH/HH. HH bytegleich D00. Keeper, Bank, Gegner, Attribute,
  Rollen, IP/OOP, Management und alle sonstigen Startwerte bleiben unverändert.
  Standardpressing gilt für die getestete Seite; der jeweilige Gegner behält sein
  eingefrorenes Profil. Alle46 kodierten Staminawerte bleiben60.
- Technisch vier neue Seeds, je Kontext×Seite einer, jede der16 Eingabezellen
  zweimal;32 Vollmatches/16 exakte A/A-Paare plus eine Exit108-Negativkontrolle.
  Für jeden Eingriff müssen **beide Felder getrennt** nach Originalvorbereitung
  und erstem Fortschritt exakt erhalten sein. Kollaps/Normalisierung stoppt
  die Studie vor Main. Cache8A wird empirisch beobachtet; keine angenommene
  C90-/C7A-Zuordnung wird als Gate eingebaut.
- Bei bestandener und veröffentlichter technischer Freigabe:32 neue Seeds je
  bekanntem Gegner, beide Seiten und vier Arme;512 Hauptmatches,64 unabhängige
  Seedblöcke. Technische Seeds und Daten bleiben getrennt. Keine Holdouts,
  Ersatzseeds, Retries, automatische Vergrößerung oder echte Karrieresaves.
- Ein primärer Kontrast: C90-Haupteffekt minus C7A-Haupteffekt auf xGD,
  algebraisch `HL−LH`. Positive Werte bedeuten im geprüften Rohzustandskontext
  einen größeren C90-Effekt; negative Werte einen größeren C7A-Effekt.
- Acht feste Sekundärtests mit Holm: C90-xGD, C7A-xGD, physische xGD-Interaktion
  und derselbe Attributionskontrast auf tatsächliche Punkte, Tore, Gegentore,
  xGF und xGA. Alle Intervalle sind marginal, sofern nicht anders bezeichnet.
- Seiten zuerst innerhalb jedes Seeds mitteln, dann feste Kontextgewichte½.
  Welch-/Satterthwaite95%-KI und stratifizierter20.000-Block-Bootstrap; keine
  Schätzung bei unvollständigen512 Hauptmessungen oder Fehlern.
- Praktische Referenz0,20xGD; gewünschte volle95%-Breite≤0,50. Bei angenommener
  gleicher Block-SD0,6/1,0/1,5 beträgt die Breite ungefähr0,300/0,500/0,750
  und die Power für0,20 ungefähr74,7%/35,0%/18,3%. Diese Annahmen sind keine
  Rohdaten-Schätzungen des neuen Kontrasts und keine90%-Powergarantie.
- Eigener Höchstverbrauch900 beaufsichtigte Childsekunden/5400UTC-Sekunden,
  maximal vier kalte Worker,2GiB neue private Artefakte. Erste Mainadmission
  mindestens600 Sekunden eigene/globale Child-/UTC-Restzeit. Globale NIGHT-002-
  Limits bleiben zusätzlich bindend. Ein einziger nativer Supervisor/exklusive
  Lease; keine Reaktivierung alter Budgets oder MECH-003-Seeds.

## Bestätigte Offlineprüfungen und verbleibende Gates

Acht fokussierte Tests prüfen Record-Diffs, getrennte Rohwerte, tatsächliche
Actorbindung, Kollaps-/Kontrollfehler, Familien-/Budgetdrift, Kontrastskalierung,
komplette Seedblöcke, fehlende Daten und tatsächliche Scoreendpunkte. Sie bestehen
in der vorhandenen Projektumgebung. Eine numerische SciPy-Negativtail-CDF-Instabilität
in der zukünftigen Powerplanung wird in der **neuen** Analyse durch mathematisch
identische Survival-Symmetrie umgangen; nichtendliche Powerwerte werden abgewiesen.

Noch offen: endgültiger Runner-/Supervisorreview, Veröffentlichung/CI,
native technische Ausführung, unabhängiger Rohreview und separate Mainfreigabe.
Die unveränderten `false`-Flags im vorregistrierten Manifest beschreiben dessen
damals ausstehende Splitabnahme; der tatsächliche spätere technische Release
ist ein gesondertes, veröffentlichtes Evidenzartefakt. Historische TECH17-
Voraussetzungen können zusätzlich mit ihrer tatsächlichen Provenienz gebunden
werden; sie ersetzen die neue Splitabnahme nicht.
Dieser Bericht gibt keine bereits bestandene native oder wissenschaftliche
Validierung aus. Fehlende Signifikanz wäre keine Äquivalenz, und ein signifikanter
Rohfeldeffekt bewiese keinen realen Karriere-/Trainingseffekt.

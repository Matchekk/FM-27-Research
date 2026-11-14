# TACT-003-STLESS-R0 – unabhängiger Neuheits- und Designreview

14.11.2026 · Research Agent, nicht Autor des Compilers, der Analyse oder der
Vorregistrierung. **`NOVEL_HYPOTHESIS` und wissenschaftliches Pilotdesign
akzeptiert.** Dies ist keine konkrete Input-, Runner-, native Technik- oder
Mainfreigabe. Keine Simulation oder Seedreservierung durch diesen Reviewer.

## Neues Wissen gegenüber tatsächlich geprüften Quellen

Der [Studienatlas](../FM27_EXTERNAL_STUDY_ATLAS_2026-11-14.md),
[maschinenlesbare Index](../../research/fm27-external-study-index-20261114.json),
[lokale Befunde](../../FINDINGS.md) und die relevanten Originalquellen wurden
berücksichtigt. Die aktuelle Quellenfortschreibung steht im
[Literaturaudit](LITERATURE_AUDIT.md). Der Mac-HEAD wurde für diese Auswahl
erneut geprüft und bleibt
[`e92cf1416ca5c8c4b13009f8cf7d695f290b0368`](https://github.com/caiograco289/Fm-Match-Lab/commit/e92cf1416ca5c8c4b13009f8cf7d695f290b0368).

| Überschneidende Quellen-ID | Was die Originalquelle beantwortet | Was dieser Pilot zusätzlich identifiziert |
| --- | --- | --- |
| MAC-06 | [23 Gesamttaktiken/Familiarity und geänderte Startelfauswahl](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/06-tactics-x-familiarity.md) | Kein gezielter IP×OOP-Paketvergleich mit konstanten Akteuren. |
| MAC-07/07B | [Taktikliga mit synthetischen Kadern und Communitypaketen](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/07b-tactic-league-18.md) | Ein Rang kann Änderungen an Formation, Rollen und Anweisungen nicht kausal trennen. |
| MAC-19 | [Presets über Fixturekalender dreier Klubkontexte](https://github.com/caiograco289/Fm-Match-Lab/blob/e92cf1416ca5c8c4b13009f8cf7d695f290b0368/docs/studies/19-a-season-per-tactic.md) | Kein kontrollierter OOP-Moderator der hier deklarierten IP-Umstellung. |
| FM27-FMAX-LAB | [Änderliches Taktikleaderboard](https://getfmax.com/en/lab/) mit mehreren stürmerlosen Paketen | Motiviert die Frage; weder Rang noch Matchzahl belegt einen isolierten stürmerlosen Mechanismus. |
| TACT-002-R0 | [ST-/AMC-Rollen innerhalb fester4231/4411-Positionen](../../experiments/TACT-002-R0-results.md) | Der alte Rollenpilot prüfte weder4240 noch eine gleichzeitig veränderte OOP-Struktur. |

**Entscheidung:** neu innerhalb dieser geprüften Literatur ist die Frage, ob
die Wirkung **eines exakt definierten IP-Pakets** von einem gleichzeitig
gekreuzten **OOP-Paket** abhängt. Keine Behauptung weltweiter Erstmaligkeit.
Kein unverändertes Ranking, kein Wiederholen des abgeschlossenen TACT-002.

## Identifizierter Kontrast und verbleibende Confounder

Die [Vorregistrierung](../../experiments/TACT-003-stless-preregistration.md)
benennt die vier Arme I0-O0/I1-O0/I0-O1/I1-O1 eindeutig:

- IP4231→4240 bewegt denselben ursprünglichen Akteur8 von AMC nach AMCL und
  Akteur10 von ST nach AMCR; zusätzlich CF→SecondStriker bei Akteur10.
- OOP4411→4420 bewegt dieselben Akteure nach AMCL/AMCR und ändert beim früheren
  ST OPCentreForward→OPAttackingMidfielder. Die seitenspezifische Actorpermutation
  bleibt erhalten.

Das sind jeweils **zwei Positionsänderungen und eine Rollenänderung**.
Auch die laterale Neuordnung und intrinsische Rollenweisungen gehören zum
Paket. Explizite PI0 bedeuten nicht identisches intrinsisches Verhalten.
Dieser Versuch isoliert weder Abwesenheit eines ST noch eine einzelne Rolle,
Formation, Laufbewegung, Complexity oder OOP-Zone als alleinige Ursache.
Phasenreadbacks belegen zugewiesene Positionen und Rollen; tatsächliche Laufwege
werden hier nicht gemessen.

Die Primärgröße ist die vollständige physische Differenz der Differenzen:
`(I1O1−I0O1)−(I1O0−I0O0)` auf xGD, Koeffizienten `(1,−1,−1,1)`.
Eine positive Interaktion ist **kein Beweis eines stürmerlosen Siegers**:
Sie kann auch entstehen, wenn beide einfachen IP-Effekte negativ sind.
Alle vier Armmittel sind deshalb zu berichten. Marginale IP-/OOP-Effekte
beantworten andere, vorab sekundäre Fragen; kein nachträgliches Umschalten
des Primärtests auf die günstigste Diagonale oder Metrik.

Unveränderte Akteure, Startelf, Gegner, Attribute, Profile und alle übrigen
Records vermeiden eine zwischen Armen veränderte Kaderstärke oder Eignung.
Omnipotente Feldpositionsratings20 und Rohfähigkeiten60 bleiben synthetische
Kontrollen; keine kalibrierte FM-UI12-Skala und kein realistischer Kadertransfer.
Zwei bekannte Gegner, ein Fixture und ursprüngliches Management begrenzen die
Übertragbarkeit. Reaktionen des Managements sind Teil des totalen Paketeffekts.

## Auswertung, Präzision und Fehlertoleranz

Ein Primärtest bei zweiseitigemα0,05; genau sieben Sekundärtests bilden eine
gemeinsame Holm7-Familie: marginale IP-/OOP-xGD und derselbe Interaktionskontrast
auf tatsächliche Punkte, GF, GA, xGF und xGA. Die tatsächlichen Scoreendpunkte
sind damit enthalten, obwohl xGD als Explorationsendpunkt sinnvoll primär bleibt.

512 geplante Matches ergeben **64 unabhängige Seedblöcke**,32je festem Gegner;
Seiten werden im Seed gemittelt, Kontexte fest je½ gewichtet. Welch/Satterthwaite
und20.000stratifizierte Blockresamples erhalten die Abhängigkeiten. Koeffizienten
und Analyse implementieren die volle DoD, nicht die Viertelinteraktion einer
±1-Regressionsparametrisierung. Die Definitionen in Dokument, Vertrag und
Auswertung stimmen überein.

Praktische Referenz0,20xGD, volle gewünschte95%-Breite≤0,50. Die genannten
SD-/Powerwerte sind explizite Annahmen, keine Messungen der neuen Interaktion.
Der64Block-Pilot garantiert keine90%-Power; breite Intervalle oder
Nichtsignifikanz beweisen keine Wirkungslosigkeit. Keine Ergebnisexklusion,
Nullimputation, automatische Erweiterung, Ersatzseeds oder nachträgliche Auswahl.

Vor Main muss ein separater TECH32+1-Lauf alle neuen Positions-/Rolleninputs,
Game-Legalität, tatsächliche Actorbindungen, Attribute/Profile,16A/A-Paare,
Start-/RawTF33-Kontrollen und Negativabweisung belegen. Unveränderte RohTF33
gegenüber D00 ist ein vorab gesetztes Gate; ein Mismatch darf nicht nachträglich
als erlaubte Paketkomponente umdefiniert werden. Der900Childsekunden-/5400UTC-
Vertrag und globale NIGHT-002-Limits bleiben gleichzeitig bindend.

## Geprüfter Quellstand und tatsächlich ausgeführte Checks

SHA256 über LF-normalisierte Dateibytes:

| Datei | SHA256 |
| --- | --- |
| `analysis/stless003_design.py` | `b89145974e52a0b5f71c5a1dc3d0daea2d19205eb8b8bbd8f36c243cc526aa73` |
| `analysis/analyse_stless003.py` | `58da6f79cb1e262f113158455e9767f2bc88b6e9d8999b8b3d5d4a4fc14166b6` |
| `tests/test_stless003.py` | `937b7e3e39a8eff9d0e39de2685269def0306faa64ea053ce0fffe449c55422a` |
| `experiments/TACT-003-stless-preregistration.md` | `f9f2c9373306d72ace66dc1875fa4728609195408b48bc734c9adadd5636bb21` |
| `docs/night-002/STLESS003-DESIGN.md` | `82a632ce83e50f042d7fe4ae60681498ec115827cc4fade73822d87e2306b818` |

Alle fünf Hashes stimmen. Acht fokussierte Synthetiktests des wissenschaftlichen
Designstands unabhängig ausgeführt und bestanden: begrenzte Recordänderungen,
Actor-/OOP-Permutation, Profil-/PI-Konstanz, illegale Rolle/Position,
fehlende Game-Checks, falsche Inputs, vollständige Blöcke, DoD-Skalierung,
Holm7 und Vertrags-/Budgetdrift. Synthetik ist keine native Legalitätsabnahme.

**Budgetnachtrag vor ersten TACT-Seeds:** Auf neuen Directorauftrag wird nur
der Ressourcenvertrag verschärft; die unveränderte Analyse behält ihren Hash.
Zusätzlich zu ganzen beaufsichtigten Phasen werden nun alle tatsächlichen
nativen Callzeiten missionsweit gegen3600s verrechnet.30s absolut pro Call,
40s konservatives reserviertes Envelope je begonnenem, noch nicht abgerechnetem
Job; abgerechnete frühere Studiencalls bleiben enthalten. Fehlende/unbekannte
Zeiten dürfen nicht als null gelten. Die ursprünglichen900/5400/600-Grenzen
und das bestehende globale Ledger bleiben bindend. Dieser engere Vertrag ist
wissenschaftlich unbedenklich. Seine tatsächliche race-freie Umsetzung und
Bereinigungs-/Summenbelege sind Gegenstand des separaten Runner-/Inputreviews;
dieser Nachtrag behauptet noch keine implementierte Nativefreigabe.

**Offen vor Start:** separater Runnerreview, konkrete Input-/Seedprüfung,
Publikation/CI und neue native Technik. Vor Main zusätzlich unabhängiger
technischer Rohreview und veröffentlichter Release mit CI. Dieser Review
erteilt nur Neuheits-/Designakzeptanz und ändert keine MECH-004-Quellen.

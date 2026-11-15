# NIGHT-003 – Forschungsbericht vom 15.11.2026

**Zwischenstand nach abgeschlossener erster Hauptstudie.** Nutzerfenster:
nur diese aktive Sitzung. Keine geplante Fortsetzung nach deren Ende.

## Was wissen wir über FM27 jetzt, was wir vorher nicht wussten?

Im geprüften synthetischen Fixture verändert raw10000 statt7000 den relativen
xGD-Effekt des konkreten STLESS-IP-Pakets nicht um die vorab als praktisch
relevant definierten ±0,20: geschätzte Interaktion −0,013,
95-%-KI [−0,119; +0,092]. Das ist neue präzise Information über eine
Wechselwirkung, keine erneute Entdeckung des bekannten Schärfe-Haupteffekts.

## Tatsächlich durchgeführte Studien

| Studie | Wissenschaftliche Matches / unabhängige Blöcke | Stand |
|---|---|---|
| N3-SHARPSTRUCT-C1: Schärfe×IP bei fester OOP | 4.096 / 512 | vollständig, Rohbelege geprüft, beide Rechenwege stimmen überein |
| N3-SHARPPOS-C1: marginaler Nutzen zweier Positionsgruppen | 0 / 0 | eigene Technik16+1 und acht A/A-Paare bestanden; Main folgt nach CI |

Erste Studie zusätzlich32 technische Vollmatches/16 A/A und eine erwartete
Negativabweisung. Keine unerwarteten nativen Fehler, Ausschlüsse, Retries,
Ersatzseeds oder fehlenden Messwerte der vollständigen ersten Serie.
[Vollständiger Ergebnisbericht](../../experiments/N3-SHARPSTRUCT-C1-results.md)
enthält alle sechs Holm-korrigierten Sekundärtests, Kontextwerte, deskriptive
Einzeleffekte, Build, Abrechnung, Rohdaten- und Nachrechnungslinks.

Primärer Welch-Schätzer −0,013320 xGD, 95-%-KI[−0,118593;+0,091953],
p0,803779, volle Breite0,210546; Bootstrap[−0,118783;+0,090835].
Präzisionsziel≤0,25 erreicht. Keine sekundäre Holm6-Hypothese signifikant.
Punkteinteraktion −0,080[−0,232;+0,072], Holm-p1,0 bleibt weniger präzise.

## Taktik, Scouting und Gültigkeitsbereich

Das konkrete STLESS-IP-Paket hat deskriptiv bei beiden Schärfestufen einen
ähnlich negativen xGD-Abstand zum Originalsystem. Daraus folgt im getesteten
Kontext keine besondere STLESS-Freischaltung durch volle gemeinsame Startschärfe.
Andere STLESS-Pakete und kleinere Interaktionen bleiben offen. Scoutinggewichte
werden aus diesem Eingriff nicht verändert. Die Positionsfrage wird separat
untersucht und hat zu diesem Berichtsstand noch keine wissenschaftlichen Daten.

Ein gebündeltes Fixture, zwei feste bekannte Gegner, synthetische Profile mit
omnipotenten Positionsratings, FM27 27.0.1+2503222. Kein universeller Formations-
oder Attributsieger und keine Gleichsetzung mit Karriere, Urlaub oder Instant
Result. Die separate Nachrechnung verwendet eine andere Arithmetik; gleicher
Analyst, kein separater Gutachter behauptet. Native Originalbelege bleiben privat.

## Fehler, Änderungen und Publikationsbelege

- Vor Main dokumentiert: bestehender Dispatcher sortiert die gemischte
  Planliste erneut. Tatsächliche Blockreihenfolge sortiert; keine Änderung
  der Arme, Seeds, Fallzahl oder Analyse. [Abnahme/Änderung](TECHNICAL_RELEASE.md).
- Ein Encoding-Tippfehler im neuen Archivtest führte zu CI-Fehler auf0f997d5;
  f57c193 korrigierte ihn vor Main mit erfolgreicher CI. Keine native Serie
  oder Reservierung deswegen zurückgesetzt.
- MECH-004 und alle alten terminalen Reservierungen bleiben unverändert.
  Keine Komprimierung, Verschiebung oder Löschung während nativer Phasen.

| Abschnitt | Commit | Erfolgreiche CI |
|---|---|---|
| Erste Vorregistrierung | ac5b993330b49734d49088045ea55fd6a6a3385d | [43693138863](https://github.com/Matchekk/FM-27-Research/actions/runs/43693138863) |
| Erste Mainfreigabe | f57c193489a4824dc76f4cb5ead828408e5fc84c | [43693487274](https://github.com/Matchekk/FM-27-Research/actions/runs/43693487274) |
| Zweite Vorregistrierung | 0a2089e758fceb51033f7fd3161c111d4e29107f | [43695266210](https://github.com/Matchekk/FM-27-Research/actions/runs/43695266210) |

Ergebnis-/zweite Freigabe-CI folgt mit dem nächsten veröffentlichten Commit.
Branch `codex/night-003`; Integration auf main nach vollständiger Validierung.

## Drei wertvollste nächsten Forschungsfragen

1. Überträgt sich die eingegrenzte Schärfe×IP-Interaktion auf zusätzliche
   Gegner, Stärken und natürlichere Positionsratings?
2. Unterscheidet sich derselbe Zweispieler-Schärfenutzen zwischen AMC/ST und CB,
   und wie lassen sich danach Position, Rolle und feste Akteuridentität trennen?
3. Welchen Beitrag leisten die beiden Positionsänderungen und der Rollenwechsel
   einzeln beziehungsweise gemeinsam zum konkreten STLESS-Paketabstand?

[Zeit-/Fortschrittsprotokoll](PROGRESS.md) · [Literatur](LITERATURE.md) ·
[Positionsvertrag](../../experiments/N3-SHARPPOS-C1.md).

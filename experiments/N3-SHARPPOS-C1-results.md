# N3-SHARPPOS-C1 – gleiche Schärfedosis bei zwei Positionsgruppen

15.11.2026. **4.096 gültige neue Hauptmatches, 1.024 unabhängige Seedblöcke.**
Primär marginaler Schärfenutzen AMC/ST minus marginaler Nutzen DCR/DCL:
**0,053613 xGD/Match**, 95-%-Welch-KI **[-0,003894; 0,111120]**,
p=0.0676289. Separate skalare Nachrechnung aller sieben formalen
Schätzer einschließlich Holm6 stimmt überein.

Das gesamte primäre KI liegt innerhalb der vorregistrierten ±0,15. Ein größerer
Gruppenunterschied dieser Größenordnung wird im Kontext nicht gestützt;
ein kleinerer Vorteil bei AMC/ST bleibt möglich. Kein Primärnachweis bei α0,05.
Volle KI-Breite 0,115014, Ziel≤0,15 erreicht.
Bootstrap95%-KI [-0,003663; 0,111098].

## Identifizierter Vergleich

[Vorregistrierung](N3-SHARPPOS-C1.md): DEFENCE_LOW minus ATTACK_LOW.
Je Arm genau zwei ursprüngliche Starter mit beiden Rohfeldern7000, alle anderen
Akteure10000. Angriff: Slots8AMC/AttackingMidfielder und10ST/CentreForward;
Verteidigung: Slots2DCR und3DCL/CentreBack. Alle IP/OOP-Positionen, Rollen,
Attribute, Positionsratings, Gegner und Managementpolitik bleiben identisch.

Ein gemeinsamer Hochschärfe-Kontrollwert kürzt sich in der Differenz marginaler
Nutzen heraus. **Separate absolute Gruppeneffekte sind nicht identifiziert.**
Positive xGD-Werte entsprechen relativ größerem Schärfenutzen bei AMC/ST.
Für GA/xGA bedeutet positive DEFENCE_LOW−ATTACK_LOW mehr Abgabe in DEFENCE_LOW.

## Vollständige vorregistrierte Holm6-Familie

| Endpunkt/Kontrast | Effekt/Match | Marginales95%-KI | Holm6-p |
|---|---:|---|---:|
| points | 0,075684 | [0,000659; 0,150708] | 0,1921 |
| gf | 0,133789 | [0,064005; 0,203573] | 0,000890399 |
| ga | 0,033203 | [-0,037347; 0,103753] | 0,7119 |
| xgf | 0,085995 | [0,046569; 0,125420] | 0,000122717 |
| xga | 0,032382 | [-0,007036; 0,071800] | 0,321798 |
| CONTEXT_DIFFERENCE:xgd | 0,013953 | [-0,101061; 0,128967] | 0,811889 |

Erzielte Tore und xGF bestehen Holm6; der primäre xGD-Kontrast und tatsächliche
Punkte bestehen ihre festgelegten Schwellen nicht. Kein nachträglich ausgewählter
Positionssieger. Die sekundären Angriffsindikatoren sind ein Hinweis im festen
Setup, keine universelle Priorisierung von Angreifern für Training/Scouting.

## Technik, Stichprobe und Grenzen

512 neue Seeds je festem Gegnerkontext, zwei Seiten, zwei Arme; Seitenmittel im
Seed, Kontextgewichte½. 4.096 sind **1.024**, nicht4.096 unabhängige Beobachtungen.
Keine Interim-Analyse, Erweiterung, Ausschlüsse, Retries oder Ersatzseeds.
16 technische Vollmatches, acht exakteA/A-Paare und eine erwartete Exit108-Probe
vor Main. Alle4.113Jobs vollständig; keine unerwarteten nativen Ausfälle,
unbegonnenen oder unaufgelösten Jobs. Fehlstellen separat im Provenienz-JSON.
Alle Actor-/Phasenbindungen,3.174Attribute,1.058Profile,44Phasenzellen und748PI-
Gruppen nativ verifiziert; genau zwei deklarierte Akteure raw7000/cache70.
Rohbelege nach bestätigter Prozessbereinigung erneut vollständig geprüft.

FM27 **27.0.1+2503222**, TacticsLabv1114.6, unveränderter Observer und gepinnte
Ressourcen wie im [Inputmanifest](../data/night-003-sharppos/inputs.json).
Max4kalteWorker/exklusiveLease, originalesJob3-Containment. Kein gemessener
Engine-PID-Peak behauptet. Beaufsichtigte Phasenzeit 3438.230/7200s.
Keine Archivierung oder Pfadänderung während nativer Phasen.

Ein Fixture, zwei bekannte Gegner, synthetische omnipotente Positionsratings,
feste Akteure und Rollen: kein universeller reiner Positionseffekt, keine
Karriere-/Urlaub-/Instant-Result-Gleichsetzung und keine neuen Attributgewichte.
Independenter Arithmetikpfad, gleicher Analyst; kein separater Gutachter behauptet.

[Messungen](../data/night-003-sharppos/main.jsonl) ·
[Effekte/Armmittel](../data/night-003-sharppos/effects.json) ·
[1.024Blockkontraste](../data/night-003-sharppos/seed-contrasts.jsonl) ·
[primäre Nachrechnung](../data/night-003-sharppos/independent-recalculation.json) ·
[alle sieben Schätzer](../data/night-003-sharppos/independent-statistics-review.json) ·
[Abrechnung/Software/Fehlstellen](../data/night-003-sharppos/execution-provenance.json).

Vorregistrierung0a2089e/CI43695266210; Mainfreigabea58e11d mit erfolgreicher
[CI43699039037](https://github.com/Matchekk/FM-27-Research/actions/runs/43699039037).
Ergebnis-CI wird im [Missionsbericht](../docs/night-003/RESEARCH_REPORT.md) ergänzt.

# Agent 1 – Tactics Researcher

**14.11.2026 · Recherche/Offlineprüfung und Entwurf.** Keine native Simulation,
Seedreservierung, Registryänderung oder Holdoutnutzung. Nur diese Datei wurde
bearbeitet; Review, Integration, CI und Publikation erfolgen zentral.

## Forschungsfrage und Ausgangslage

Welche zulässigen IP-/OOP-Rollenänderungen verbessern eine eigene IP-4-2-3-1,
und wann ergänzen sich ST/AMC beziehungsweise AV/Flügel? Ziel ist ein kausal
zuordenbarer Rollenmechanismus, keine globale Rangliste.

AGENTS, Methodik, Plattform, Roadmap, Findings, TACT-001 und P0/P1A/P1B wurden
geprüft. Aktuelle lokale DLL-Dateiversion tatsächlich27.0.1, Produkt27.0.1+2503222;
Toolkontext v1114.6/91f2eba57fac0b7fbd3dff616056907e3ce461be. Dieser Agent hat
keine native Kompatibilitätsprobe gestartet. P1B lieferte keine Holm-signifikanten
Haupt-/Paarwirkungen; D15/D09 bleiben aus denselben xGD-Daten ausgewählte Vorschläge.

Zusätzlich berücksichtigt: [P1C](../../experiments/TACT-001-P1C-results.md)
beobachtet für das vorab einzige Paket D15+0,098Punkte,95-%-KI[−0,137;+0,333],
p0,41246, volle Breite0,470 statt≤0,30. Die Hinweisschwelle ist nicht erfüllt.
**Rollen/OOP priorisieren, D15 nicht unbegrenzt nachtesten, D09 nicht nachschieben.**
P1C-Zahlen sind hier gelesene zentrale Resultate; unabhängige Nachrechnung liegt
beim Reviewer. Synthetischer Seedpilot ist keine Karrierebestätigung.

## Geprüfte externe Evidenz und Forschungslücke

| Primärquelle / Version | Geprüfter Inhalt | Evidenzgrenze |
|---|---|---|
| [Sports Interactive, FM26-Taktikentwicklung](https://www.footballmanager.com/fm26/features/possession-out-possession-fm26s-new-tactical-evolution), Zugriff14.11.2026 | Getrennte IP-/OOP-Formationen sind ausdrückliches Produktkonzept. | FM26-Herstellerbeschreibung, kein kausaler FM27-Rollenvergleich. |
| [Tactics-Lab-Server, geprüfter Commit](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/src/fm27_tactics_server.py), v1114.6 | Phasen-/Positions-/Formationsabhängige Eligibility und PI-Policy; absolute Kodierung berücksichtigt Rollenflags. | Technische Quelle, kein Leistungsnachweis. Konkrete Rollen unten aus lokalem gehashtem Katalog. |
| [Upstream Fidelity](https://github.com/lqf0624/fm-tactics-lab/blob/91f2eba57fac0b7fbd3dff616056907e3ce461be/docs/SIMULATION_FIDELITY.md), gleicher Toolcommit | Einzelmatch-Detailberechnung ist von vollständigem Karriereablauf zu trennen. | Keine Karrierevalidierung. |
| [NIST, vollständige Zweistufendesigns](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3331.htm), Zugriff14.11.2026 | Vollständige Faktorpläne ermöglichen orthogonale Haupt-/Interaktionsspalten. | Matrixorthogonalität beweist keine unabhängigen Matchfehler oder kostenlose Varianzreduktion. |

Die geprüften Quellen liefern keine kontrollierte FM27-Schätzung unserer
Rollenpaare. Downloadrankings ändern oft mehrere Rollen, Profile und Anweisungen
zugleich. Neue Lücke: ST-Rückfall×Zehner-Nachrücken sowie AV-Vorstoß×Flügel-
Einrücken unter vollständig festgehaltenen übrigen Bedingungen.

## Tatsächlich geprüfter Katalog und reproduzierbare Offlineprüfung

Nur JSON/Quelltext gelesen, **kein Serverimport**, weil dessen Initialisierung
native Prüfungen auslösen kann. Lokaler Katalog:
`local/runtime-v1114.6/source/tactics_ui/catalog.json`, SHA256
`c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c`.
Unsere öffentliche eigene Baseline hat in beiden Phasen zwei IV und nicht genau
einen DM. Eligibilitykennung laut `role_options()` daher `0:0`.

| Frage | Position/Phase | Basis-ID / Flags | Alternative-ID / Flags |
|---|---|---|---|
| ST-Rückfall | ST/IP0 | CentreForward /2048 | DeepLyingForward /1024 |
| AMC-Nachrücken | AMC/IP0 | AttackingMidfielder /512 | SecondStriker /2199023255552 |
| ST-Defensivarbeit | ST/OOP1 | OPCentreForward /4398046511104 | OPTrackingCentreForward /8796093022208 |
| AMC-Defensivarbeit | AMC/OOP1 | OPAttackingMidfielder /1073741824 | OPTrackingAttackingMidfielder /2147483648 |
| AV-Vorstoß | DR,DL/IP0 | FullBack /4 | WingBack /8 |
| Flügelbewegung | AMR,AML/IP0 | Winger /128 | InsideForward /134217728 |

Erste vier Zeilen:4Kontexte×2Phasen×2Positionen×2Rollen=
**32 Offline-Mitgliedschaftsassertions bestanden**. AV-/Flügel-IDs wurden lesend
in denselben Listen gefunden, nicht als Teil der32 gezählt. Mitgliedschaft ist
**keine neue native Freigabe**. Öffentlich nur funktionale IDs/Flags, keine
privaten Spieleridentitäten oder kopierten vollständigen Kataloge.

Reproduktion ab Repositorywurzel, Python, ohne Serverimport:

```python
import hashlib, json
from pathlib import Path
path = Path('local/runtime-v1114.6/source/tactics_ui/catalog.json')
assert hashlib.sha256(path.read_bytes()).hexdigest() == (
    'c08a8aa77c371aaafb29956c6c794b1580f7751547720dc6da4b83b63b32480c')
c = json.loads(path.read_text(encoding='utf8'))
x = json.loads(Path('data/tact-001-p1b/inputs.json').read_text(encoding='utf8'))
positions = {p['id']: p for p in c['positions']}
pairs = {
    0: [('ST', ['CentreForward', 'DeepLyingForward']),
        ('AMC', ['AttackingMidfielder', 'SecondStriker'])],
    1: [('ST', ['OPCentreForward', 'OPTrackingCentreForward']),
        ('AMC', ['OPAttackingMidfielder', 'OPTrackingAttackingMidfielder'])]}
checks = 0
for name, context in x['fixed_contexts'].items():
    team = context['teams'][int(name.rsplit('-', 1)[1])]
    for phase, cells in enumerate(team['phases']):
        cb = sum(bool(positions[v['position']]['mask'] & 16) for v in cells)
        dm = sum(bool(positions[v['position']]['mask'] & 0x80) for v in cells)
        key = f'{3 if cb >= 3 else 0}:{int(dm == 1)}'
        assert key == '0:0'
        for position, roles in pairs[phase]:
            assert set(roles) <= set(c['role_eligibility_context'][key][position][phase])
            checks += len(roles)
assert checks == 32
print('32 offline membership assertions passed; native starts 0')
```

## Begrenzter eigener Suchraum und native Voraussetzungen

IP bleibt GK,DR,DCR,DCL,DL,DMR,DML,AMR,AMC,AML,ST. Keine stürmerlose Klasse.
Priorität1: IP-ST×AMC aus den ersten beiden Tabellenzeilen, OOP vollständig
unveränderte4-4-1-1. Priorität2: OOP-Trackingrollen derselben ST-/AMC-Slots bei
konstanter Formation; so Phasenrollen vor Strukturwechseln isolieren.
Priorität3: AV×Flügel; beide AV symmetrisch FullBack/WingBack und beide
IP-Flügel Winger/InsideForward. Das ist ein bewusstes Zwei-Spieler-Paket,
keine isolierte Aussage über links/rechts. OOP-Rollen bleiben konstant.

OOP4-4-2/4-1-4-1 erst danach als eigene Faktoren: alle elf Spieler eindeutig
abbilden und Eligibility neu berechnen. Ein-DM-/Drei-IV-Kontexte können sich
ändern. Für diese Strukturen wurde hier noch kein vollständiger legaler
Rollensatz eingefroren; sie sind technisch blockiert.

Explizit `rules=game`, Duty0 und alle17 PI-Gruppen je Slot/Phase deklarieren.
PI0 beweist nicht die Abwesenheit rolleninterner Vorgaben. `cell_policy()`
nach Rollenänderung erneut prüfen; unerlaubte Kombination ablehnen, keine
stille automatische Rollenreparatur. Keine gleichzeitige Attributänderung.

Geplant, **noch nicht implementiert**: Rollenmanifestprüfung von Kataloghash
über Formation/Eligibility, Role-ID/64bit-Flags/Duty/PI-Policy und normalisiertes
Setup bis zu erlaubten Binärrecords. Danach nativer Nach-Vorbereitungsreadback
aller Spieler beider Teams: Positionsmasken, Rolle OR Duty, effektive PI,
IP-/OOP-Slotbindung und unveränderte Attribute/Profile/Teaminstruktionen.
Bestehender `NativeLab` prüft Rollen-/Positionsflags; ein neuer Versuch braucht
zusätzlich interventionsspezifische PI-/Recorddiff-Audits. JSON allein reicht nicht.

Technikentwurf:16Zellen(4Arme×2Gegner×2Seiten) jeweils zweimal mit neuen
technischen Seeds =32Vollmatches/16exakte A/A-Vergleiche und eine Exit108-
Binärprobe,33Versuchsplätze. Falsche Phase/Rolle/PI zunächst offline negativ
prüfen. Eigener Vertrag, neue zentrale Seeds, veröffentlichter Code, dauerhafte
Budgets; keine P1C-Registrierung wiederverwenden. Drift/Inputfehler stoppen.

## TACT-002-R0 – vorgeschlagener Rollenvarianzpilot, nicht registriert

**Frage:** Wie wirkt IP-DeepLyingForward statt CentreForward marginal über die
zwei vorab festgelegten AMC-Rollen? ST-Rückfall×AMC-Nachrücken ist zusätzlich
explorativ, damit nicht wieder eine kleine Interaktion allein die Serie dominiert.

Vollständiges2×2 mit ST=CentreForward/DeepLyingForward und
AMC=AttackingMidfielder/SecondStriker. Alle Team Instructions bleiben D00-
Standard, nicht D15. Zwei bisherige Discoverygegner, gleiche synthetische
Profile, beide Seiten, neue Seeds; keine Holdouts.

Primär ST-Haupteffekt auf xGD, physische Koeffizienten R00/R10/R01/R11:
(−½,+½,−½,+½),α0,05, praktische Screeningwirkung0,30xGD.
Sekundär genau sieben explizite Kontrast×Endpunkt-Paare als **Holm7**:
(1)AMC-Haupteffekt×xGD, (2)ST×AMC-DoD×xGD,
(3)ST-Haupteffekt×Punkte, (4)ST-Haupteffekt×GF,
(5)ST-Haupteffekt×GA, (6)ST-Haupteffekt×xGF,
(7)ST-Haupteffekt×xGA. Kein zusätzlicher Punkte-DoD-Test.
 Physische DoD:
(+1,−1,−1,+1), keine Faktor2-Verwechslung. Armmittel/Punkte deskriptiv,
keine finale Paketwahl. Erst Seitenmittel innerhalb vollständiger Seeds,
dann Gegnergewicht je½; Welch-t und stratifizierter vollständiger Blockbootstrap.
Gemeinsame Seeds garantieren keine Varianzreduktion. Fehlender Arm erlaubt
nur technischen Status, keine Exklusion/Ersatzseeds oder adaptive Rollenwahl.

### Stichproben, Kosten und Informationsgewinn

SD bezieht sich auf den vollständigen primären Seedkontrast nach Seitenmittel.
**Unbekannte Rollenstreuung**: die folgenden SDs sind Annahmen, keine Übernahme
der kleinen P1B-Faktor-SDs als gemessene Rollenvarianz.

| Variante | Seeds/Gegner | Unabhängige Blöcke | Hauptmatches | Technik separat | Grobe Child-Zeit / vorgeschlagener harter Cap |
|---|---:|---:|---:|---:|---|
| Klein, zuerst empfohlen |32|64|512|32+1Negativprobe|300–400s /900s|
| Größer, separat entscheiden |64|128|1024|32+1Negativprobe|550–700s /1200s|

Zeitanker aus echten zentralen Budgets: P1B1071,884s/2048 und P1C295,818s/512
Hauptmatches, etwa0,52–0,58s/Match bei vier Workern. Neue Rollen-/Auditkosten
können abweichen. Global≤4Worker,90s ohne Fortschritt,2GiB Artefakte,
20GiB Diskreserve; dauerhafte Child-Zähler und fixe UTC-Frist1800s/2400s.
Keine parallelen nativen Agentenserien oder Budgetneustarts.

| Angenommene SD | Volle95-%-Breite klein | Power für0,30 klein | Volle95-%-Breite groß | Power für0,30 groß |
|---:|---:|---:|---:|---:|
|0,8|0,400|84,0%|0,280|98,8%|
|1,2|0,600|50,4%|0,420|80,1%|
|1,8|0,900|25,9%|0,630|46,5%|

Offline berechnet mit nichtzentraler t-Verteilung, df=2n−2,
SE=SD/√(2n), gleiche SD pro Kontext nur als Rechenannahme.
`research.stats.required_n(.30,sd)` ergibt77/171/381 Gesamtblöcke für90%:
gleichmäßig gerundet78/172/382 =624/1376/3056 Matches. Diese Power gilt
nur für den ST-Haupteffekt, nicht für anders streuende DoD/Holm7-Familie.
Später tatsächliche Kontext-SDs und Obergrenzen einsetzen; keine Garantie.

Pro1000Matches: ungefähr125 unabhängige Achtmatchblöcke für einen primären
und zwei weitere vorab benannte xGD-Kontraste. Bei SD0,8/1,2: SE≈0,072/0,107,
volle95-%-Breite≈0,284/0,425. Drei Kontraste sind keine drei unabhängigen
Stichproben. Ein Zweiarm-Paket liefert250Blöcke/1000Matches, isoliert aber
nicht ST/AMC/Interaktion. Mehr Mechanismenwissen, kein behaupteter kostenloser
Präzisionsgewinn. Der erste kleine Pilot schließt die fehlende Rollenvarianz.

## Unabhängige D15-Bestätigung – bewusst zurückgestellt

Keine sofortige neue D15-Serie empfohlen. Schon bei den bekannten P1C-
Streuungen kostet90% Power für+0,15Punkte gegen Null3384 neue Matches,
mit gemeinsamen Normalmodell-SD-Obergrenzen4960. Neue Kontexte können
variabler sein. Diese Opportunitätskosten sprechen zunächst für Rollen/OOP.

Nur bei späterem separatem Auftrag: unverändertes D15 gegen D00, neue Seeds,
unbenutzte Gegner und Stärken, beide Seiten. Zwei gehaltene Gegner×drei
vorab definierte Stärken =sechs feste Kontexte, je1/6; hier wurden keine
vorhandenen Holdoutdaten gelesen. Realistische Profile/Stärken brauchen
VALID-003. Primär Punkte, sekundär xGD/GF/GA/xGF/xGA(Holm5).
Bei bloß angenommener Punkte-SD1,5 benötigt0,15gegen Null etwa1053 Blöcke,
balanciert1056 =4224Matches. Erst separaten Varianzpilot neuer Kontexte und
Nutzen gegenüber neuen Fragen bewerten; P1C-SD ist keine Transfergarantie.
Kein Poolen mit P1B-Auswahldaten, kein D09-Ersatz bei Enttäuschung.

Positive95-%-Untergrenze belegt nicht einen Mindestgewinn0,15. Für letzteren
muss sie>0,15 liegen; Power braucht eine angenommene wahre Verbesserung
oberhalb dieser Schwelle. Power0,15gegen0 darf nicht als90% Power für den
Nachweis mindestens0,15 ausgegeben werden.

## Implementierungs-/Teststatus, Unsicherheiten, nächste Schritte

**Implementiert:** nur dieser Bericht.32 reine Offline-Katalogassertions und
obige Power-/Präzisionsrechnungen ausgeführt. Kein neuer Validator/Runner,
keine Registrierung und keine neue native Rollenfreigabe. Native Starts0.
Die erste Ausgabeinspektion musste wegen UTF8-Lesecodierung wiederholt werden;
die Assertions liefen danach erfolgreich. Keine Engineaktion betroffen.

**Offen:** effektive rolleninterne PI, neue Flag-/Slotbindung, realistische
positionsabhängige Profile, Familiarity und Karriere. Universelle synthetische
Positionseignung kann echte Kaderanforderungen verdecken. Runtime-Normalisierung
setzt kontrollierte Startzustände erneut: JSON-Fitness-/Schärfeänderung ist
ohne Audit keine wirksame Intervention. OOP-Mapping braucht eigenes Gate.

**Konkrete nächste Schritte, nicht gestartet:** unabhängiges Review der
Kontraste/Holm7/Power; mit Agent VALID Rollenmanifest-/Policy-/Recorddiff-
Check spezifizieren;16 vollständige Zellen samt Code/Hashes/neuen Seeds vor
Technik publizieren und33Versuchsplätze zentral freigeben. Erst danach kleiner
512-Match-Rollenpilot als neuer Auftrag. Kein automatischer großer Plan,
keine weitere D15-Serie, Holdoutausführung oder Karrierefortschreibung.

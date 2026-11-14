# Agent 7 – unabhängiges Review von TACT-001-P1C

14.11.2026. **Zur Veröffentlichung als unabhängiger Seed-/Präzisionspilot
freigegeben; kein statistischer oder dokumentierter technischer Blocker gefunden.**
Diese Freigabe ist keine Bestätigung einer optimalen Taktik oder allgemeiner
Karriereübertragbarkeit und keine Freigabe weiterer Simulationen.

## Unabhängigkeit und geprüfter Stand

Dieser Codex-Subagent hat die numerischen Resultate direkt aus öffentlichen
`main.jsonl`-Zeilen und dem Manifest neu aufgebaut. Kein Import des vorhandenen
Analysers, Verifiers, Runners oder gemeinsamer `research.stats`-Funktionen.
Eigene skalare Paarbildung, SciPy-t-Verteilung und eigene vollständige
Bootstrapindexmatrix; Power-/Präzisionsminima mit **linearer** Ganzzahlsuche
statt der im Produktcode verwendeten binären Suche. Keine native Ausführung,
keine Registry-/Seedänderung und keine Nutzung gehaltener Daten.

Quellstand für Vorregistrierung/Code/Seedplan:
`bd3d9baa04b0a66ce8b80d37eb0b3c8f305849a5`.
Technische Publikation:
`44d6a97fcff612ed785e75786301051128647a79`.
Die Ergebnisdateien wurden vor ihrer abschließenden Publikation geprüft.

Git-Status war ein gemeinsamer, erwartbar veränderter Checkout; ausschließlich
Reviewdateien dieses Agenten wurden geschrieben. Remote-main stand beim Review
auf44d6a97. DLL-Version rein lesend27.0.1/27.0.1+2503222, tatsächlicher SHA256
`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`.
Kein erneuter nativer Enginecheck oder Matchstart durch den Reviewer.

## Primärer Endpunkt und Entscheidung

Alle512 erwarteten Kombinationen aus128 neuen Seedblöcken, beiden Seiten und
D00/D15 genau einmal vorhanden. Vollständige Seiten- und Armpaare,64 unabhängige
Blöcke je festem Gegnerkontext. Keine nachträgliche Wahl zwischen D15 und D09.

Punkte3/1/0 aus den tatsächlichen Endständen, D15−D00 pro Seite, Seitenmittel
im Seed, anschließend beide Gegner je½:

| Größe | Unabhängig nachgerechnet |
|---|---:|
| Punkte/Match | +0,0976562500 |
| high_press Mittel / SD | +0,0703125000 /1,4388796002 |
| deep_block Mittel / SD | +0,1250000000 /1,2408394496 |
| SE |0,1187509382|
| Welch-Satterthwaite-df |123,3347235668|
| Zweiseitiges95-%-t-KI |[−0,1373976138;+0,3327101138]|
| p |0,4124579966|
| Stratifiziertes20.000-Block-Bootstrap95-%-KI |[−0,1328125000;+0,3242187500]|

Numerische Übereinstimmung aller sechs Endpunkte einschließlich t-/Bootstrap-
Intervallen innerhalb1e−12. Die volle Primärintervallbreite0,4701077275 überschreitet
das vorab gesetzte Ziel0,30. Schätzer<0,15 und Untergrenze<0; nur die positiven
Kontextmittel erfüllen das entsprechende Kriterium. Die eingefrorene gemeinsame
Hinweisregel ist **nicht erfüllt**. Empfehlung Rollen/OOP statt unbegrenzter
D15-Wiederholung entspricht der Vorregistrierung. Nichtsignifikanz ist kein
Äquivalenznachweis und kein Beweis fehlender Verbesserung.

## Sekundäre Familie unabhängig nachgerechnet

| Endpunkt | D15−D00 | Marginales95-%-t-KI | Roh-p | Holm5-p |
|---|---:|---|---:|---:|
| xGD |+0,196039837|[+0,027102953;+0,364976720]|0,023303839|0,093215355|
| GF |−0,027343750|[−0,217914347;+0,163226847]|0,776914512|1,000000000|
| GA |−0,179687500|[−0,387038528;+0,027663528]|0,088811227|0,266433680|
| xGF |+0,035418038|[−0,074425084;+0,145261159]|0,524561581|1,000000000|
| xGA |−0,160621799|[−0,273065711;−0,048177887]|0,005470004|0,027350020|

Nur xGA unterschreitet die Holm5-Schwelle. Das ist ein sekundärer Hinweis auf
weniger erwartete Gegentore im getesteten Kontext. Es darf weder die primäre
Punktefrage ersetzen noch nachträglich zum Auswahlkriterium werden. Das positive
marginale xGD-Intervall ist kein Holm-korrigierter xGD-Nachweis.

## Power und Präzision

Eigene lineare Ganzzahlsuche bestätigt sämtliche im Archiv angegebenen Minima:

| Feste Verbesserung gegen Null | Beobachtete SD: neue Seeds/Gegner / Matches | Gemeinsame Normalmodell-SD-Obergrenzen: neue Seeds/Gegner / Matches |
|---|---|---|
|0,10 Punkte|950 /7600|1392 /11136|
|0,15 Punkte|423 /3384|620 /4960|
|0,20 Punkte|239 /1912|349 /2792|

Volle95-%-Breiten0,20/0,30 verlangen bei beobachteter SD348/156 neue Seeds je
Gegner (2784/1248 Matches), mit oberen SDs510/228 (4080/1824 Matches).
Auch die SD3-Sensitivitätsminima stimmen. Diese Zahlen sind bedingt auf feste
Streuung, Kontextgewichte und nichtzentrale Welch-t-Näherung. Sie sind kein
Ausführungsauftrag und keine90-%-Garantie in neuen Gegner-/Kaderkontexten.

Die beiden einseitigen97,5-%-χ²-SD-Grenzen ergeben unter dem Normalmodell über
Bonferroni mindestens95-%-gemeinsame Abdeckung. Punktekontraste sind diskret;
dieses Modell ist hier keine exakte Verteilung. SD3 ist eine gültige theoretische
Range-Schranke für einen Kontrast in[−3,+3], garantiert aber keine exakte t-Power.
Keine Posthoc-Power aus dem beobachteten kleinen Punkteeffekt wird als neue
Evidenz ausgegeben. Ein Nachweis **mindestens**+0,15 hätte eine andere Nullhypothese;
Power für einen wahren Effekt0,15 gegen0 bedeutet nicht90% Power für eine
Intervalluntergrenze>0,15.

## Technischer und zeitlicher Audit

- 529 eindeutige Versuchsplätze:512 Hauptmatches und16 technische Matches ok,
 eine erwartete Negativabweisung, keine fehlenden/ersetzten Jobs.
- Acht technische Kontext×Seite×Arm-Paare jeweils zweimal; Scores, vollständige
 Teamstatistik, Endtick, Seed und Setuphash exakt gleich.
- Die acht D00/D15-Setuphashes stimmen mit P1B überein. Öffentliche Hauptzeilen
 tragen passende Identitäts-, Konfigurations- und Setupprovenienz sowie vollständige
 Native-Auditflags. Keine nachträgliche Taktikänderung im Pilot.
- 13 eingefrorene Codequelldateien und Inputs/Seedplan/Designmatrix stimmen
 sowohl zum Manifesthash als auch zu den tatsächlich gelesenen Gitblobs des
 Vorregistrierungscommits überein, nach einheitlicher CRLF/LF-Normalisierung.
- Alle151 historischen Archivdateien stimmen sowohl mit dem Archivhash als auch
 den tatsächlichen Gitblobs des Ausgangscommits317dec75 überein.
- Kumulierte beaufsichtigte Child-Zeit320,4412158s<900s, Summe der drei
 Phasenoperationen. Studienfenster661,419055s<1800s; keine Budgetneustarts,
 keine gescheiterten/zeitüberschrittenen Operationen im öffentlichen Budget.

[Vorregistrierungs-CI43604285753](https://github.com/Matchekk/FM-27-Research/actions/runs/43604285753)
war fehlgeschlagen; der Bericht verschweigt dies nicht. Der Fehler betraf einen
neuen Test mit privater Pfadabhängigkeit. Wissenschaftlicher Code blieb gehasht
identisch. [Freigabe-CI43604561092](https://github.com/Matchekk/FM-27-Research/actions/runs/43604561092)
ist success und wurde14:24:06UTC abgeschlossen, **vor** Hauptstart14:24:22,445UTC.
Vorregistrierungs-Pushereignis14:19:48UTC liegt vor Technikstart14:20:08,095UTC.
Frühere Vorbereitung enthielt Kompatibilitäts-/Kodierungsarbeit, keine
vorregistrierten Vollmatches. Die UTC-Deadline blieb unverändert.

Grenze dieses Audits: Öffentliche JSONL und Hashbelege erlauben eine unabhängige
Statistik-/Provenienzprüfung, aber keine erneute Prüfung des privaten kompletten
Spielmaterials oder einen unabhängigen Game-in-Game-Vergleich. Der Reviewer hat
keine native Serie wiederholt; dies ist **keine externe Replikation**. Geschütztes
Material bleibt privat. Die technische Freigabe gilt weiterhin ausschließlich
für das bekannte gebündelte synthetische Fixture.

## Reproduzierbarer unabhängiger Rechenkern

Ab Repositorywurzel mit der vorhandenen Pythonumgebung; nur Standardbibliothek,
NumPy und SciPy. Kein Import der Projektanalyse:

```python
import json, hashlib
from pathlib import Path
import numpy as np
from scipy.stats import t, nct
p = Path('data/tact-001-p1c')
r = json.loads((p/'manifest.json').read_text(encoding='utf8'))
rows = [json.loads(s) for s in (p/'main.jsonl').read_text(encoding='utf8').splitlines()]
contexts = ['high_press', 'deep_block']
by = {(x['scenario'], x['seed'], x['tested_side'], x['arm']): x for x in rows}
assert len(rows) == len(by) == 512

def endpoint(x):
    s = x['tested_side']; gf, ga = x['score'][s], x['score'][1-s]
    a, b = x['team_statistics'][s]['xg'], x['team_statistics'][1-s]['xg']
    return np.array([3 if gf > ga else int(gf == ga), a-b, gf, ga, a, b])

v = np.array([[
    sum((endpoint(by[h,seed,s,'D15'])-endpoint(by[h,seed,s,'D00']))
        for s in [0,1])/2
    for seed in r['seeds'][j*64:(j+1)*64]] for j,h in enumerate(contexts)])
mu = v.mean(axis=(0,1)); sd = v.std(axis=1, ddof=1)
parts = sd**2/(4*64); se = np.sqrt(parts.sum(axis=0))
df = parts.sum(axis=0)**2/(parts**2/63).sum(axis=0)
half = t.ppf(.975,df)*se; prob = 2*t.sf(abs(mu/se),df)
print(mu, sd, np.column_stack([mu-half,mu+half]), prob)
seed = int.from_bytes(hashlib.sha256(b'TACT-001-P1C/bootstrap-v1').digest()[:8],'little')
rng = np.random.default_rng(seed)
indices = [rng.integers(64,size=(20000,64)) for _ in contexts]
boot = (v[0][indices[0]].mean(axis=1)+v[1][indices[1]].mean(axis=1))/2
print(np.quantile(boot,[.025,.975],axis=0))
order = np.argsort(prob[1:]); adjusted = np.empty(5); prior = 0
for rank,k in enumerate(order):
    prior = max(prior, min(1., (5-rank)*prob[k+1])); adjusted[k] = prior
print(adjusted)

def planned_power(n, effect, sigma):
    pieces = np.asarray(sigma)**2/(4*n)
    q = np.sqrt(pieces.sum())
    df = pieces.sum()**2/(pieces**2/(n-1)).sum()
    cut = t.ppf(.975,df)
    return nct.cdf(-cut,df,effect/q)+nct.sf(cut,df,effect/q)
for effect in [.10,.15,.20]:
    n = next(n for n in range(2,10000) if planned_power(n,effect,sd[:,0]) >= .9)
    print(effect, n, 8*n)
```

Verwendete Bibliotheken: NumPy 2.3.5, SciPy 1.16.3.
Gelesene öffentliche Hauptdaten SHA256(LF): `24d9b96cbd0521372e5a78caed6ce38b238a29f0b755393369218bc258143627`.
Manifest SHA256(LF): `d15095cf36584258a0b63108c3baa179ed00d4c7bd67be641a483953d11ee35c`.

## Abschluss

Der öffentliche Ergebnisbericht kann mit seinen negativen/unklaren primären
Schlüssen, der sekundären xGA-Evidenz und expliziten Transfergrenzen veröffentlicht
werden. Director führt finalen Diff-/Datei-/Geheimnischeck und CI nach Integration
aus. Keine neue native Studie oder Kandidatenwahl durch dieses Review autorisiert.

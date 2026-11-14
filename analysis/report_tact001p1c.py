"""Render complete P1C pilot and its resource summary; never invokes native code."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.native import read,rows,write,require
PUBLIC=ROOT/'data/tact-001-p1c';LOCAL=ROOT/'local/tact-001-p1c'
def num(x):return f'{x:+.3f}'.replace('.',',')
def ci(z,key='ci'):return '['+'; '.join(num(x) for x in z[key])+']'
def report():
    status=read(PUBLIC/'run-summary.json');require(status['scientific_series_complete'],'Incomplete: technical status only')
    z=read(PUBLIC/'effects.json');b=read(PUBLIC/'budget.json');p=z['primary'];gate=read(PUBLIC/'technical-gate.json')
    resources=[]
    for kind in ('technical','main'):
        sessions=[s for f in (LOCAL/kind).glob('part-*/sessions.json') for s in read(f)]
        resources.append(dict(kind=kind,warm_worker_processes=len(sessions),completed_matches=sum(s['completed'] for s in sessions),all_returncodes_zero=all(s['returncode']==0 for s in sessions),all_cleanup_ok=all(s.get('steam_session_cleanup',{}).get('ok') for s in sessions)))
    write(PUBLIC/'resource-summary.json',dict(sessions=resources,raw_private_bytes=sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file()),supervised_operations=len(b['operations']),non_match_native_probes=len(b['operations'])+2,probe_basis='One image check per NativeLab child, one capability cache miss per technical/main child; within supervised budget',negative_processes=1,maximum_workers=4,progress_timeout_seconds=90,charged_native_seconds=b['charged_seconds'],study_window_seconds=b['elapsed_study_window_seconds']))
    fig,ax=plt.subplots(figsize=(8,3.6),layout='constrained')
    values=[]
    for h in ('high_press','deep_block'):
        c=p['context'][h];half=t.isf(.025,63)*c['sd']/8;values.append((h,c['mean'],c['mean']-half,c['mean']+half))
    values.append(('Gleichgewichtetes Mittel',p['mean'],*p['ci']))
    for i,(label,mean,lo,hi) in enumerate(values):ax.errorbar(mean,i,xerr=[[mean-lo],[hi-mean]],fmt='o',capsize=4,color='#245a81')
    ax.axvline(0,color='#888');ax.axvline(.15,color='#ba752d',linestyle='--',label='Praktische Schwelle +0,15')
    ax.set_yticks(range(3),[v[0] for v in values]);ax.invert_yaxis();ax.set_xlabel('D15 minus D00: tatsächliche Punkte pro Match; marginales 95-%-KI');ax.set_title('TACT-001-P1C · unabhängiger Seedpilot · 128 Seedblöcke');ax.legend(fontsize=9);ax.spines[['top','right']].set_visible(False);fig.savefig(ROOT/'docs/tact001p1c-points.png',dpi=160);plt.close(fig)
    secondary='\n'.join(f"| {m} | {num(v['mean'])} | {ci(v)} | {ci(v,'bootstrap_ci')} | {v['p_holm']:.5f} |" for m,v in z['secondary'].items())
    context='\n'.join(f"| {h} | {num(v['mean'])} | {v['sd']:.3f} | {num(v['home_mean'])} | {num(v['away_mean'])} | {v['side_covariance']:.3f} |" for h,v in p['context'].items())
    arm='\n'.join(f"| {h} | {a} | "+' | '.join(f"{v[m]:.3f}" for m in ('points','gf','ga','xgf','xga'))+' |' for h,by in z['actual_arm_means'].items() for a,v in by.items())
    plans=[]
    for name,case in z['planning']['cases'].items():
        for r in case['power90']:plans.append(f"| {name} | +{r['effect']:.2f} | {r['n_per_context']} | {r['independent_blocks']} | {r['matches']} |")
    precision=[]
    for name,case in z['planning']['cases'].items():
        for r in case['precision']:precision.append(f"| {name} | {r['full_width']:.2f} | {r['n_per_context']} | {r['matches']} |")
    decision='Alle Kriterien für einen hinreichenden Pilothinweis erfüllt; externe Bestätigung separat planen.' if z['adequate_preregistered_signal'] else '**Die vorregistrierte Hinweisschwelle ist nicht erfüllt. Wir empfehlen ausdrücklich den Wechsel zu neuen Rollen und OOP-Strukturen statt unbegrenzter Wiederholung dieses Instruktionspakets.**'
    text=f'''# TACT-001-P1C – unabhängiger D15-Kandidatenpilot

**14.11.2026 · FM27 27.0.1+2503222 · unabhängige neue Seeds im bisherigen synthetischen Kontext.**

**512/512 Hauptmatches, 128 vollständige unabhängige Seedblöcke**,64 je Gegner.
16/16 technische Vollmatches,8 exakte A/A-Wiederholungen und eine erwartete
Exit108-Abweisung. Keine Ausfälle, Ausschlüsse, Retries, Ersatzseeds,
Holdoutmatches oder Karriereausführung. Alle529 Versuchsplätze abgerechnet.

## Primär: tatsächliche Punkte pro Match

D15−D00: **{num(p['mean'])} Punkte/Match**,95-%-t-KI **{ci(p)}**,
Bootstrap95-%-KI {ci(p,'bootstrap_ci')}, zweiseitiges p={p['p']:.5f}.
SE={p['se']:.4f}, Welch-df={p['df']:.2f}, gepoolte innerhalb-Kontext-SD={p['pooled_within_context_sd']:.3f}.
Volle t-KI-Breite={p['ci'][1]-p['ci'][0]:.3f}; Ziel≤0,30.

{decision}

Die Regel war vorab eingefroren: Mittel≥+0,15, untere95-%-Grenze>0,
Breite≤0,30 und positives Mittel in beiden Kontexten. Nichtsignifikanz beweist
keine Äquivalenz. Keine Kandidatenneuwahl; D09 bleibt unverändert archiviert.
Keine finale Sieger-, Optimalitäts- oder Karrierebehauptung.

![Punkte und Unsicherheit](../docs/tact001p1c-points.png)

| Kontext | Punkteffekt | Kontrast-SD | Seite0-Mittel | Seite1-Mittel | Seitenkovarianz |
|---|---:|---:|---:|---:|---:|
{context}

Seitenmittel im vollständigen Seedblock, dann Gegnergewichte je½.
512 Matches sind keine512 unabhängigen Replikate. Seiten sind native Fixtureplätze,
kein isolierter Heimvorteil. Kontexte sind feste Stilbündel, keine Stichprobe aller Gegner.
Leave-one-seed-out-Bereich {p['leave_one_out']['range']}, maximale Verschiebung
{p['leave_one_out']['max_change']:.4f}; keine Löschung aus der Hauptanalyse.

## Sekundäre Endpunkte

Genau fünf sekundäre Tests, Holm5; marginale Intervalle. GA positiv heißt mehr
Gegentore. xGD ersetzt weder Tore noch tatsächlichen Punktgewinn.

| Endpunkt | Effekt | 95-%-t-KI | Bootstrap95-%-KI | Holm-p |
|---|---:|---|---|---:|
{secondary}

| Kontext | Arm | Punkte/Match | GF | GA | xGF | xGA |
|---|---|---:|---:|---:|---:|---:|
{arm}

Vollständige Endstände und native Schüsse/SOT/Besitz bleiben im Messarchiv;
zusätzliche Leistungs-p-Werte wurden nicht erzeugt.

## Spätere neue Bestätigung: bedingte Power- und Präzisionsplanung

Feste Zielverbesserungen0,10/0,15/0,20 Punkte,90% Power, zweiseitigα0,05.
Gleiche neue n pro Kontext;128 hier beobachtete Blöcke werden nicht wiederverwendet.
Vier Matches pro Seed, insgesamt8n. Diese Zahlen sind **kein Ausführungsauftrag**.
Nichtzentrale Welch-t-Näherung bei unveränderter Streuung, keine beobachtete Power
für den ausgewählten Effektschätzer. In neuen Kontexten muss die SD neu pilotiert werden.

| SD-Annahme | Zielpunkteffekt | Neue Seeds/Gegner | Neue unabhängige Blöcke | Neue Hauptmatches |
|---|---:|---:|---:|---:|
{chr(10).join(plans)}

| SD-Annahme | Gewünschte volle95-%-Breite | Neue Seeds/Gegner | Neue Hauptmatches |
|---|---:|---:|---:|
{chr(10).join(precision)}

`simultaneous95_normal_model_upper`: Bonferroni für zwei einseitige97,5-%-SD-Grenzen,
Normalmodell/χ² mit63df. Diskrete Punktekontraste sind nicht exakt normal; diese
Grenzen und t-Power sind Näherungen, keine Verteilungsgarantie.
`bounded_points_sd3`: Varianzgrenze aus Kontrastbereich[−3,+3], konservative
Streuungssensitivität, weiterhin modellbasierte t-Power. Keine künstliche Präzision.
Vorab aus P1B prognostiziert: SD1,317/1,587, Breite0,510 und21,1% Power für+0,15.
Der neue Pilot war ausdrücklich nicht für90% Power dimensioniert.

## Technische Freigabe, Provenienz und Ressourcen

Vorregistrierung/Code/131Seedreservierungen vor dem ersten Vollmatch auf GitHub:
`{status['preregistration_commit']}`. Technischer Gate vor jedem Hauptmatch:
`{gate['published_commit']}`. D15/D00 sämtlicher acht Kontexte/Seiten bytegleich
zu P1B, vollständige native Audits nach Originalvorbereitung für jedes Match.
Phasen/Positionen/Rollen/Duties/PI, alle69 Attribute,1.058 Profilfelder,
sämtliche Instruktionsgruppen, effektiver Seed, Naturabschluss/Statistik geprüft.
Engine/Host/Fixture/Ressourcen/Adapter/Katalog/Runtimequellen entsprechen VALID-002/P1B.
Alle SHA256 im öffentlichen Eingabe-/Registrymanifest; Rohspielmaterial bleibt privat.

Kumulierte beaufsichtigte Child-Wall-Time **{b['charged_seconds']:.3f}/900s**;
festes Studienzeitfenster **{b['elapsed_study_window_seconds']:.3f}/1800s**,
UTC-Deadline `{b['wall_deadline_utc']}`. Zähler nie zurückgesetzt,
maximal4Worker und90s ohne Fortschritt. Probes/Audits/Publikationspausen im
jeweiligen Budget enthalten. Native Rohartefakte bleiben unter2GiB.

## Gültigkeitsbereich und nächste Forschungsrichtung

Neue Seedblöcke beseitigen die Wiederverwendung der P1B-Selektionsdaten, erweitern
aber weder Gegnerdiversität noch Profilrealismus. Ein Fixture, gleiche synthetische
Kaderstärke, konstante Rollen/PI/Management. Allgemeine Karriereübertragbarkeit
bleibt unbestätigt. D09 wird unabhängig vom Ergebnis nicht als Ersatz nachgeschoben.

[VALID-003](VALID-003-plan.md) plant positionsabhängige Profile, getrennte
Stärkekontexte und kapazitätsgerechte Karriere-PKM-Adapter. Keine dieser Gates
wurde hier ausgeführt. Karriere-Replays bleiben bis separater Abnahme gesperrt.
Neue Rollen-/OOP-Fragen brauchen neue native Readbacks, eigene Vorregistrierung,
neue Discoveryseeds und später unabhängige Bestätigung. Keine weitere automatische
Simulation, Holdoutstudie oder Optimierungsrunde. **Nach P1C gestoppt.**

## Reproduktion und Archivschutz

48 Plattformtests plus5 historische Analysetests, unabhängige P0/P1B/P1C-Verifier.
Der unabhängige P1C-Verifier rekonstruiert sechs Kontraste/t-/Bootstrapintervalle,
Holm5, SD-/Fallzahlminima,128 Seedkontraste und529 Versuchsplätze.
Alle151 historischen versionierten Analyse-/Daten-/Experiment-/Vertragsdateien
bleiben gegenüber Ausgangscommit317dec75 unverändert. Code/Vertrag/Eingaben und
Seedplan seit Vorregistrierung unverändert; nur zulässige Whitelist-JSONL publiziert.

[Vorregistrierung](TACT-001-P1C-preregistration.md) ·
[Freigabe](TACT-001-P1C-validation.md) · [Daten](../data/tact-001-p1c/README.md) ·
[Effekte/Planung](../data/tact-001-p1c/effects.json) ·
[Rohmessungen](../data/tact-001-p1c/main.jsonl) ·
[Abrechnung](../data/tact-001-p1c/job-accounting.jsonl).
'''
    (ROOT/'experiments/TACT-001-P1C-results.md').write_text(text,encoding='utf8')
if __name__=='__main__':report()

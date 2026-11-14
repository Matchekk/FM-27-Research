"""Render only a complete R0 study; private game material never exported."""
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.native import read,write,require
PUBLIC=ROOT/'data/tact-002-r0';LOCAL=ROOT/'local/tact-002-r0'
def num(v):return f'{v:+.3f}'.replace('.',',')
def ci(v,key='ci'):return '['+'; '.join(num(x) for x in v[key])+']'
def report():
    status=read(PUBLIC/'run-summary.json');require(status['scientific_series_complete'],'Incomplete series: technical status only')
    r=read(PUBLIC/'effects.json');p=r['primary'];budget=read(PUBLIC/'budget.json');gate=read(PUBLIC/'technical-gate.json')
    records=[('ST: DLF minus CF',p),('AMC: SecondStriker minus AttackingMidfielder',r['secondary']['AMC:xgd']),('ST x AMC: physische DoD',r['secondary']['STxAMC:xgd'])]
    fig,ax=plt.subplots(figsize=(9,4),layout='constrained')
    for i,(_,v) in enumerate(records):
        mean=v['mean'];lo,hi=v['ci'];ax.errorbar(mean,i,xerr=[[mean-lo],[hi-mean]],fmt='o',capsize=4,color='#245a81')
    ax.axvline(0,color='#888');ax.set_yticks(range(3),[a for a,_ in records]);ax.invert_yaxis();ax.set_xlabel('xGD pro Match; marginales95-%-t-KI');ax.set_title('TACT-002-R0: Rollenvarianzpilot,64 unabhaengige Seedbloecke');ax.spines[['top','right']].set_visible(False)
    fig.savefig(ROOT/'docs/tact002r0-effects.png',dpi=160);plt.close(fig)
    sessions=[]
    for kind in ('technical','main'):
        entries=[s for f in (LOCAL/kind).glob('part-*/sessions.json') for s in read(f)]
        sessions.append(dict(kind=kind,warm_worker_processes=len(entries),completed_matches=sum(s['completed'] for s in entries),all_returncodes_zero=all(s['returncode']==0 for s in entries),all_cleanup_ok=all(s.get('steam_session_cleanup',{}).get('ok') for s in entries)))
    resources=dict(supervised_operations=len(budget['operations']),coordination_leases=budget['coordination_leases'],sessions=sessions,non_match_native_probe_processes=len(budget['operations'])+2,probe_basis='One image check per supervised NativeLab initialization plus one capability-cache miss in each technical/main child',negative_processes=1,private_raw_bytes=sum(p.stat().st_size for p in LOCAL.rglob('*') if p.is_file()),maximum_workers=4,progress_timeout_seconds=90)
    write(PUBLIC/'resource-summary.json',resources)
    sec='\n'.join(f"| {a} | {num(v['mean'])} | {ci(v)} | {ci(v,'bootstrap_ci')} | {v['p_holm']:.5f} |" for a,v in r['secondary'].items())
    contexts='\n'.join(f"| {h} | {num(v['mean'])} | {v['sd']:.3f} | {num(v['side0_mean'])} | {num(v['side1_mean'])} | {v['side_covariance']:.3f} |" for h,v in p['context'].items())
    arms='\n'.join(f"| {h} | {a} | "+' | '.join(f"{v[m]:.3f}" for m in ('xgd','points','gf','ga','xgf','xga'))+' |' for h,by in r['actual_arm_means'].items() for a,v in by.items())
    plan='\n'.join(f"| {label} | {row['effect']:.2f} | {row['seeds_per_context']} | {row['independent_blocks']} | {row['matches']} |" for label,case in r['planning']['cases'].items() for row in case['power90'])
    text=f'''# TACT-002-R0 – Ergebnis des ST/AMC-Rollenvarianzpiloten

**FM27 27.0.1+2503222 · vorregistrierter synthetischer Discoverykontext.**
Alle512Hauptmatches und32technischen Vollmatches akzeptiert,16exakteA/A-Paare
und eine erwarteteExit108-Negativabweisung.64vollständige unabhängige Seedblöcke,
32je Gegner. Alle545Versuchsplätze abgerechnet; keine Ausfälle/Ausschlüsse,
Retries,Ersatzseeds,Holdoutmatches oder Karriereausführung.

## Primär: marginaler ST-Rolleneffekt

DeepLyingForward minus CentreForward, gemittelt über die zwei eingefrorenen
AMC-Rollen: **{num(p['mean'])}xGD**,95-%-t-KI **{ci(p)}**,
Bootstrap95-%-KI{ci(p,'bootstrap_ci')},zweiseitigp={p['p']:.5f}.
SE={p['se']:.4f}; volle95-%-Breite={p['ci'][1]-p['ci'][0]:.3f},Pilotziel≤0,50.
Praktische Screeninggröße0,30xGD,keine garantierte90-%-Power.

R00=CentreForward/AttackingMidfielder,R10=DeepLyingForward/AttackingMidfielder,
R01=CentreForward/SecondStriker,R11=DeepLyingForward/SecondStriker.
R00ist für jeden Gegner und jede Seite bytegleich D00 aus P1B; sämtliche
Team Instructions,Profile,OOP-Phasen,Rollen der anderen Spieler,Duties und
expliziten PI bleiben konstant. Rolleninterne Vorgaben sind Teil der Rollenwirkung;
PI0 behauptet nicht die Abwesenheit intrinsischen Rollenverhaltens.

Physische Primärkoeffizienten(−½,+½,−½,+½),Seitenmittel im Seed,dann beide
Gegner je½. Welch-Satterthwaite und20000stratifizierte vollständige Seedblöcke.
512Matches sind keine512unabhängigen Replikate. Keine Äquivalenzbehauptung bei
unklarem Intervall und keine universelle Rollengewichtung.

![Rollenwirkungen](../docs/tact002r0-effects.png)

| Primärkontext | xGD-Effekt | Kontrast-SD | Seite0 | Seite1 | Seitenkovarianz |
|---|---:|---:|---:|---:|---:|
{contexts}

LOO-Bereich{p['leave_one_out']['range']},maximale Verschiebung
{p['leave_one_out']['max_change']:.4f};keine Ergebnisexklusion.

## Sieben vorab vollständig benannte Sekundärtests

Eine gemeinsame Holm7-Familie;marginale95-%-Intervalle. STxAMCist physische
DoD(+1,−1,−1,+1),kein Faktor2-Fehler. Punkte3/1/0aus tatsächlichem Endstand.
GA/xGApositiv bedeutet mehr Gegentore/Chancenabgabe.

| Kontrast:Endpunkt | Effekt |95-%-t-KI|Bootstrap95-%-KI|Holm7-p|
|---|---:|---|---|---:|
{sec}

## Tatsächliche Armmittel, rein deskriptiv

| Gegner | Arm | xGD | Punkte | GF | GA | xGF | xGA |
|---|---|---:|---:|---:|---:|---:|---:|
{arms}

Keine neue Kandidatenauswahl oder optimale Taktik aus diesen Daten. Keine
D15-Optimierung. Die32techMatches gehen nicht in diese Leistungsanalyse ein.

## Bedingte neue Bestätigungsplanung

Zweiseitigα0,05,90%Power gegen Null,gleiche neue n je Kontext. Kein Poolen
mit diesen Daten,keine automatische weitere Ausführung. Die Normalmodell-
Obergrenzen sind je97,5-%-einseitigeχ²-SD-Grenzen;gemeinsame nominelle95-%-
Abdeckung nur unter Normalannahme. Andere Rollen/Gegner/Kader können anders streuen.

| SD-Annahme | ZielxGD | Neue Seeds/Gegner | Neue unabhängige Blöcke | Neue Vollmatches |
|---|---:|---:|---:|---:|
{plan}

Die Fallzahlen beziehen sich auf den gleichen marginalen ST-Kontrast im vollen
2×2,keine Garantie für Interaktions-/Holm7-Nachweise oder Karriereübertragung.

## Technische Provenienz und Ressourcen

Vorregistrierung/Code/Seeds vor Vollmatches:`{status['preregistration_commit']}`.
Technische Freigabe vor Hauptmatches:`{gate['published_commit']}`.
Native Readbacks für alle kodierten Records,beide Teams/Phasen,44Rollen-/Duty-
Zellen,748PI-Gruppen/Targets,69Attribute und1058Profilfelder sowie effektiven
Seed und natürlichen Abschluss bestanden. Nur deklarierte IP-ST/AMC-Rollenrecords
weichen von D00ab. Version/Katalog/Runtimequellen stimmen mit VALID-002/P1B überein.

Ein zentraler NativeLease-Supervisor,je höchstens4Engine-Worker,90s ohne
Fortschritt. Kumulierte Child-Wall-Time **{budget['charged_seconds']:.3f}/900s**,
festes Studienfenster **{budget['elapsed_study_window_seconds']:.3f}/1800s**,
unverrückbareUTC-Deadline`{budget['wall_deadline_utc']}`. Keine Zählerneustarts.
Die zusätzliche Exklusivlease ist in diesem neuen Runner integriert;historische
Runner unverändert. Vollständige Sanitized-Lease-/Budget-/Jobbelege im Datenarchiv.

## Grenzen und Abschluss

Ein gebündeltes Fixture,zwei bekannte synthetische Gegner,gleiche omnipotente
Profile und feste Managementpolitik. Rollen können über intrinsische Vorgaben,
Laufwege und Kontextinteraktionen wirken;dieser Pilot isoliert keine einzelne
solche Komponente. Kein allgemeiner Karriere- oder echter Kadernachweis.
Historische Daten und Vorregistrierungen unverändert,geschütztes Rohspielmaterial
privat. Offline-Verifier rekonstruiert achtKontraste,Holm7,192Blockwerte und545Jobs.
Nach diesem512-Match-Pilot gestoppt;keine1024-Erweiterung,Holdouts oder weitere
Optimierungsrunde.

[Vorregistrierung](TACT-002-R0-preregistration.md) ·
[Vertrag](../research/specs/TACT-002-R0.json) ·
[Rohmessungen](../data/tact-002-r0/main.jsonl) ·
[Effekte](../data/tact-002-r0/effects.json) ·
[Jobabrechnung](../data/tact-002-r0/job-accounting.jsonl).
'''
    (ROOT/'experiments/TACT-002-R0-results.md').write_text(text,encoding='utf8')
if __name__=='__main__':report()

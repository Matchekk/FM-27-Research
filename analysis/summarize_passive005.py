"""Descriptive state summary of the four unique completed technical seed cells.

Reads only retained native JSONL plus frozen configurations. No native imports,
save access, new seeds or causal effect estimate. Repeats are deliberately omitted.
"""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from research.native import read,rows,digest,require,write
from research.core import config_hash

PUBLIC=ROOT/'data/valid-005-observer-v1'
STAGES=('prepared','first_advance','finished')


def build(private):
    private=Path(private);frozen=read(PUBLIC/'inputs.json');configs=read(private/'configs.json')
    require(config_hash(configs)==frozen['configs_sha256'],'Frozen configuration changed')
    chosen=[r for r in rows(PUBLIC/'measurements.jsonl') if r['kind']=='full' and r['mode']=='observer_on']
    require(len(chosen)==4 and all(r['status']=='ok' for r in chosen),'Exactly four unique technical cells required')
    cells=[]
    for result in chosen:
        path=private/'technical'/(result['key']+'.jsonl')
        require(digest(path)==result['raw_log_sha256'],'Retained raw log differs')
        captures=[r for r in rows(path) if r.get('event')=='native_passive_state']
        require([r['stage'] for r in captures]==list(STAGES),'Stage order changed')
        config=configs[f"{result['context']}-{result['side']}"]
        starters={(s,i) for s,t in enumerate(config['teams']) for i in t['lineup'][1:]}
        require(len(starters)==20,'Twenty actual starting outfield actors required')
        stage_rows=[]
        for capture in captures:
            require(len(capture['players'])==46,'Actor coverage differs')
            players=[p for p in capture['players'] if (p['side'],p['roster_index']) in starters]
            require(len(players)==20 and all(p['statistics_cache_region_hex'] is not None for p in players),
                    'Starting outfield cache missing; never impute zero')
            def summary(values):return dict(min=min(values),mean=sum(values)/len(values),max=max(values),n=len(values))
            stage_rows.append(dict(stage=capture['stage'],
                starting_outfield_condition_storage=summary([p['condition_raw'] for p in players]),
                starting_outfield_accumulator=summary([p['condition_accumulator_raw'] for p in players]),
                starting_outfield_cache89=summary([bytes.fromhex(p['statistics_cache_region_hex'])[9] for p in players]),
                starting_outfield_cache8a=summary([bytes.fromhex(p['statistics_cache_region_hex'])[10] for p in players]),
                all_actor_nonzero_raw33=sum(any(bytes.fromhex(p['effectiveness_region_hex'])) for p in capture['players']),
                all_actor_count=46,
                missing_cache_actors=sum(p['statistics_cache_region_hex'] is None for p in capture['players'])))
        cells.append(dict(context=result['context'],side=result['side'],seed=result['seed'],
                          raw_log_sha256=result['raw_log_sha256'],stages=stage_rows))
    return dict(schema='valid005.descriptive-passive-state.v1',unique_seed_cells=4,
        repeat_runs_used_as_additional_observations=False,cells=cells,
        scope='descriptive technical observations; different raw memory sources; no UI or consumer calibration',
        causal_effect_estimate=None,new_native_matches=0)


def plot(report):
    import matplotlib
    matplotlib.use('Agg')
    matplotlib.rcParams['svg.hashsalt']='VALID-005-PASSIVE-STATE-V1'
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,3,figsize=(12,3.6))
    names=['Vorbereitung','Schritt 1','Ende'];x=range(3)
    for cell in report['cells']:
        stages=cell['stages'];label=f"{cell['context']} / Seite {cell['side']}"
        axes[0].plot(x,[r['starting_outfield_condition_storage']['mean'] for r in stages],marker='o',label=label)
        axes[1].plot(x,[r['starting_outfield_cache89']['mean'] for r in stages],marker='o',label=label)
        axes[2].plot(x,[r['all_actor_nonzero_raw33'] for r in stages],marker='o')
    for ax in axes:
        ax.set_xticks(list(x),names);ax.spines[['top','right']].set_visible(False)
        ax.grid(axis='y',alpha=.2)
    axes[0].set(title='Konditions-Profilstorage',ylabel='Rohwert (20 Feldstarter)',ylim=(9500,10500))
    axes[1].set(title='Separater Runtime-Cache 0x89',ylabel='Cache-Rohbyte (20 Feldstarter)',ylim=(0,105))
    axes[1].legend(loc='lower left',fontsize=8,frameon=False)
    axes[2].set(title='Beobachtete 33-Byte-Region',ylabel='Nichtnull-Regionen (von 46 Actors)',ylim=(0,46))
    fig.suptitle('Vier technische Seedzellen: statische Eingabe und dynamische Runtimequellen',fontsize=12)
    fig.text(.5,.01,'Deskriptiv; keine UI-Skala, kein Nachweis eines bestimmten Consumers, keine Wirkungsschätzung.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.04,1,.94));fig.savefig(PUBLIC/'passive-state.svg',metadata={'Date':None})
    preview=ROOT/'local/night-001/passive-state.png';preview.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(preview,dpi=150);plt.close(fig)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__);parser.add_argument('--private',type=Path)
    parser.add_argument('--plot-only',action='store_true');args=parser.parse_args()
    target=PUBLIC/'passive-state.json'
    if args.plot_only:report=read(target)
    else:
        require(args.private is not None,'Explicit retained private evidence directory required')
        report=build(args.private);write(target,report)
    plot(report);print(json.dumps(dict(unique_seed_cells=report['unique_seed_cells'],new_native_matches=0)))

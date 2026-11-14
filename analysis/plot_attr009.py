"""Plot published estimates only; no new inference, native calls or selection."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / 'data/attr-009-bridge'
    z = json.loads((folder / 'effects.json').read_text(encoding='utf8'))
    values = {'xgd': z['primary'], **z['secondary']}
    groups = [('xG-Kontraste', ('xgd', 'xgf', 'xga'), 'xG / Match'),
              ('Tore', ('gf', 'ga'), 'Tore / Match'),
              ('Punkte', ('points',), 'Punkte / Match')]
    labels = {'xgd': 'xGD · primär', 'xgf': 'xGF', 'xga': 'xGA',
              'gf': 'Tore', 'ga': 'Gegentore', 'points': 'Punkte'}
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 4), layout='constrained')
    for ax, (title, metrics, unit) in zip(axes, groups, strict=True):
        for y, metric in enumerate(metrics):
            v = values[metric]
            ax.errorbar(v['mean'], y, xerr=[[v['mean']-v['ci'][0]], [v['ci'][1]-v['mean']]],
                        fmt='o', capsize=4, color='#1d537a' if metric == 'xgd' else '#59636b')
        ax.axvline(0, color='#91979c', linewidth=1, linestyle='--')
        ax.set_yticks(range(len(metrics)), [labels[m] for m in metrics])
        ax.set_ylim(len(metrics)-.5, -.5)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel(unit)
        ax.spines[['top', 'right']].set_visible(False)
        ax.grid(axis='x', alpha=.15)
    fig.suptitle('ATTR-009: Positionsspezialisierung × relativer Rohattributnutzen', fontsize=13)
    fig.supxlabel('S[J − (A+P)/2] − O[J − (A+P)/2] · 384 Matches / 32 Seedblöcke\n'
                  'Marginale 95-%-t-KI; sekundäre Tests Holm5. Keine simultanen Intervalle.', fontsize=9)
    fig.savefig(folder / 'contrast-intervals.png', dpi=160)
    plt.close(fig)


if __name__ == '__main__':
    main()

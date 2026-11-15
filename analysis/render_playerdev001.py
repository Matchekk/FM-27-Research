"""Standalone scientific figure from completed public estimates; no simulation."""
from hashlib import sha256
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/player-development-001-role/effects.json'
OUT=ROOT/'docs/player-development-001'

def main():
    effects=json.loads(DATA.read_text(encoding='utf8'))
    if effects['n_matches']!=4096:raise ValueError('Full scientific sample required')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.hashsalt':'PD-ROLE-001'})
    fig,axes=plt.subplots(2,1,figsize=(9,5.4),gridspec_kw={'height_ratios':[1,1.6]},layout='constrained')
    fig.suptitle('CF / DLF × Sprunghöhe beim selben Stürmer',fontsize=16,fontweight='bold')
    axes[0].axvspan(-.15,.15,color='#ecefee',zorder=0)
    sets=[[(0,effects['primary'],'Interaktion: DLF minus CF')],
          [(1,effects['descriptive_only']['JR_CF']['xgd'],'JR-Effekt unter CF'),
           (0,effects['descriptive_only']['JR_DLF']['xgd'],'JR-Effekt unter DLF')]]
    for ax,cells in zip(axes,sets):
        for y,estimate,label in cells:
            mean=estimate['mean'];low,high=estimate['ci']
            ax.errorbar(mean,y,xerr=[[mean-low],[high-mean]],fmt='o',color='#0b625b',capsize=4,linewidth=2,markersize=6)
            ax.annotate(f'{mean:+.3f} [{low:+.3f}; {high:+.3f}]',(mean,y),xytext=(0,14),textcoords='offset points',ha='center',fontsize=10)
        ax.set_yticks([c[0] for c in cells],[c[2] for c in cells]);ax.set_ylim(-.6,max(c[0] for c in cells)+.7)
        ax.axvline(0,color='#707773',linestyle='--',linewidth=.8);ax.grid(axis='x',alpha=.15)
        ax.spines[['top','right','left']].set_visible(False);ax.set_xlabel('xGD pro Match · Rohsprunghöhe 60 → 80')
        ax.tick_params(axis='y',length=0)
    axes[0].set_title('Vorregistrierter Primärkontrast · grau: praktische Referenz ±0,15',fontsize=10,loc='left')
    axes[1].set_title('Bedingte Effekte: deskriptiv, keine separaten Bestätigungstests',fontsize=10,loc='left')
    fig.supxlabel('FM27 27.0.1+2503222 · 4.096 Matches / 512 Seedblöcke · marginale 95-%-Welch-Intervalle',fontsize=9)
    for ext in ('svg','png'):fig.savefig(OUT/('role-contrasts.'+ext),dpi=160,metadata={'Date':None} if ext=='svg' else {})
    plt.close(fig)
    svg=OUT/'role-contrasts.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\n',encoding='utf8',newline='\n')
    provenance=dict(measurement='data/player-development-001-role/effects.json',source_sha256=sha256(DATA.read_bytes()).hexdigest(),
        renderer_sha256=sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        files={ext:sha256((OUT/('role-contrasts.'+ext)).read_bytes()).hexdigest() for ext in ('svg','png')},
        warning='Conditional effects share blocks and are descriptive; no player-outcome or CA calibration.')
    (OUT/'figure-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':main()

"""Render the released IP/OOP interaction without additional statistical tests."""
from hashlib import sha256
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'data/night-002-stless003'


def main():
    data=json.loads((PUBLIC/'effects.json').read_text(encoding='utf8'))
    assert data['n_matches']==512 and data['independent_seed_blocks']==64
    assert json.loads((PUBLIC/'main-summary.json').read_text())['passed'] is True
    matplotlib.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.hashsalt':'TACT-003-STLESS-R0'})
    contexts=('high_press','deep_block')
    means={arm:sum(data['arm_means'][h][arm]['xgd'] for h in contexts)/2
           for arm in ('I0-O0','I1-O0','I0-O1','I1-O1')}
    fig,axis=plt.subplots(figsize=(8.2,5.1))
    for arms,label,color in [(('I0-O0','I1-O0'),'OOP4411 unverändert','#68747d'),
                              (('I0-O1','I1-O1'),'OOP4420-Paket','#174e70')]:
        values=[means[a] for a in arms]
        axis.plot([0,1],values,'o-',color=color,linewidth=2,markersize=7,label=label)
        for x,value in enumerate(values):
            axis.annotate(f'{value:+.3f}',(x,value),xytext=(0,9 if x==0 else -19),
                          textcoords='offset points',ha='center',color=color,fontsize=10)
    axis.axhline(0,color='#c7cdd0',linewidth=.8,zorder=0)
    axis.set_xticks([0,1],['IP4231 unverändert','IP4240-Paket'])
    axis.set_xlim(-.18,1.18)
    low,high=min(means.values()),max(means.values());padding=max(.12,(high-low)*.35)
    axis.set_ylim(low-padding,high+padding)
    axis.set_ylabel('xGD pro Match · deskriptives Armmittel')
    axis.spines[['top','right']].set_visible(False)
    axis.legend(frameon=False,loc='best')
    primary=data['primary'];lo,hi=primary['ci']
    fig.suptitle('Verändert das OOP-Paket den Effekt des IP-Pakets?',x=.11,ha='left',fontsize=14)
    fig.text(.11,.89,f"Primär: IP×OOP {primary['mean']:+.3f} xGD-DoD · 95-%-KI [{lo:+.3f}; {hi:+.3f}]",fontsize=11)
    fig.text(.11,.04,'512 Matches · 64 neue Seedblöcke · Seiten im Seed gemittelt · zwei feste Kontexte\n'
             'FM27 27.0.1+2503222 · Rollen-/Positionspakete; keine allgemeine Karriereprognose',fontsize=9,color='#4c565c')
    fig.subplots_adjust(left=.11,right=.96,bottom=.20,top=.80)
    fig.savefig(PUBLIC/'interaction.png',dpi=180,metadata={'Software':'FM27 Research'})
    fig.savefig(PUBLIC/'interaction.svg',metadata={'Date':None,'Creator':'FM27 Research'})
    svg=PUBLIC/'interaction.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf8').splitlines())+'\n',
                   encoding='utf8',newline='\n')
    plt.close(fig)
    proof=dict(experiment_id='TACT-003-STLESS-R0',command='python -B analysis/render_stless003.py',
        source_sha256=sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        effects_sha256=sha256((PUBLIC/'effects.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inference='Only the preregistered primary interval is shown; four arm means are descriptive.',
        matplotlib_version=matplotlib.__version__)
    (PUBLIC/'figure-provenance.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf8')
    print('Rendered released interaction figure; no new tests or native calls')


if __name__=='__main__':main()

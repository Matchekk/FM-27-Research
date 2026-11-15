"""Publication figure of the two complete, preregistered NIGHT-003 contrasts."""
from pathlib import Path
from hashlib import sha256
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
STUDIES=(('night-003-sharpstruct','Schärfe × IP-Struktur',512,.20),
         ('night-003-sharppos','Schärfenutzen: AMC/ST relativ zu CB',1024,.15))

def lf_hash(p):return sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest()

def render():
    data=[]
    for folder,label,n,reference in STUDIES:
        p=ROOT/'data'/folder;effect=json.loads((p/'effects.json').read_text(encoding='utf8'))
        review=json.loads((p/'independent-statistics-review.json').read_text(encoding='utf8'))
        if effect['n_matches']!=4096 or review['passed'] is not True or review['independent_blocks']!=n:
            raise ValueError('Only complete, independently reconstructed studies may be plotted')
        data.append((effect['primary'],label,n,reference))
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.hashsalt':'night003-results-v1'})
    fig,axes=plt.subplots(2,1,figsize=(9,4.7),sharex=True)
    extent=max(.26,max(max(abs(x) for x in e['ci']) for e,_,_,_ in data)+.04)
    for ax,(effect,label,n,reference) in zip(axes,data,strict=True):
        mean=effect['mean'];lo,hi=effect['ci']
        ax.axvspan(-reference,reference,color='#eef0ed',zorder=0)
        ax.axvline(0,color='#5a625c',linewidth=.8,zorder=1)
        ax.errorbar(mean,0,xerr=[[mean-lo],[hi-mean]],fmt='o',markersize=8,
                    color='#1d534a',elinewidth=2.4,capsize=5,zorder=3)
        ax.set_title(f'{label}  ·  4.096 Matches / {n:,} Blöcke'.replace('1,024','1.024'),loc='left',fontsize=11,pad=9)
        ax.text(.99,.78,f'{mean:+.3f}  [{lo:+.3f}; {hi:+.3f}]'.replace('.',','),
                transform=ax.transAxes,ha='right',fontsize=10,color='#1d534a')
        ax.set(yticks=[],ylim=(-.6,.6),xlim=(-extent,extent))
        for spine in ('left','right','top'):ax.spines[spine].set_visible(False)
        ax.spines['bottom'].set_color('#b9beba');ax.tick_params(axis='x',length=3,color='#b9beba')
    axes[1].set_xlabel('Primärer Kontrast in xGD pro Match · marginales 95-%-Welch-Intervall')
    fig.suptitle('FM27 · Zwei getrennte Schärfefragen',x=.055,y=.98,ha='left',fontsize=15,fontweight='bold')
    fig.text(.055,.025,'Grau: vorab definierte praktische Referenz (oben ±0,20; unten ±0,15). Zwei feste Gegner; synthetische Profile.',fontsize=8,color='#525c55')
    fig.subplots_adjust(left=.055,right=.98,top=.82,bottom=.16,hspace=.65)
    output=ROOT/'docs/night-003';fig.savefig(output/'primary-contrasts.svg',metadata={'Date':None})
    fig.savefig(output/'primary-contrasts.png',dpi=160);plt.close(fig)
    provenance=dict(source_lf_sha256=lf_hash(Path(__file__)),matplotlib=matplotlib.__version__,
        inputs={folder:lf_hash(ROOT/'data'/folder/'effects.json') for folder,_,_,_ in STUDIES},
        svg_sha256=sha256((output/'primary-contrasts.svg').read_bytes()).hexdigest())
    (output/'figure-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':render()

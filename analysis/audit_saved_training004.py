"""Offline audit of saved calendar slots, never an exposure/attendance estimator."""
from collections import Counter
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from research.native import read,require,write

# Public API facts from the frozen official 0.12.4 TrainingSession enum. These
# are reader labels; no local FM UI verification is inferred from their names.
LABELS={0:'PASSING_STYLE',1:'BUILD_UP',2:'CHANCE_CREATION',5:'PRESSING_INTENSITY',
        6:'PRESSING_TRAP',300:'REST',301:'RECOVERY',302:'LIGHT_CONDITIONING',
        303:'CONDITIONING',402:'TRAVEL',500:'MATCH'}
SOURCE='https://github.com/rhiever/fmsave/blob/e0704bc5d7e6bf687fecf85cd48b28c497bdef68/src/fmsave/models/training.py'
SOURCE_SHA='d15d0d10430cb1b0e4d8f25721e81ea1e941dec6d8ec9a293277839597fd5fc4'


def audit(report):
    require(report['profile']=='R2' and report['snapshot_stable'] is True,'Stable R2 snapshot required')
    probes={p['probe']:p for p in report['probes']}
    training=probes['training']
    require(training['status']=='observed','Missing training cannot become zero exposure')
    calendar=training['coverage'];require(calendar['rows']==len(calendar['teams'])>0,'Calendar denominator missing')
    current=date.fromisoformat(probes['open']['coverage']['game_date_claim'])
    result=[];total=Counter();weeks=days=0
    for team in calendar['teams']:
        counts={int(k):v for k,v in team['raw_session_counts'].items()}
        require(len(counts)==len(team['raw_session_counts']) and
                all(type(v) is int and v>=0 for v in counts.values()),'Invalid saved code counts')
        slots=sum(counts.values())
        require(type(team['days']) is int and type(team['weeks']) is int and
                slots==3*team['days'] and team['days']==7*team['weeks'],
                'Saved slot/day/week accounting mismatch')
        known=sum(v for k,v in counts.items() if k in LABELS)
        result.append(dict(team_code=team['team_code'],saved_weeks=team['weeks'],saved_days=team['days'],
            saved_slots=slots,reader_labelled_slots=known,unknown_label_slots=slots-known,
            reader_label_coverage=known/slots if slots else None,
            last_saved_week_after_parser_save_date=date.fromisoformat(team['last_week'])>current))
        total.update(counts);weeks+=team['weeks'];days+=team['days']
    slots=sum(total.values());known=sum(v for k,v in total.items() if k in LABELS)
    return dict(schema='valid004.saved-calendar-label-audit.v1',source=SOURCE,source_file_sha256=SOURCE_SHA,
        reader_labels={str(k):v for k,v in LABELS.items()},teams=result,
        total=dict(saved_weeks=weeks,saved_days=days,saved_slots=slots,reader_labelled_slots=known,
                   unknown_label_slots=slots-known,reader_label_coverage=known/slots),
        unknown_code_counts={str(k):v for k,v in sorted(total.items()) if k not in LABELS},
        scope='same saved calendar; descriptive offline audit; no new save read',
        completed_session_exposure=None,individual_attendance=None,training_effect_estimate=None,
        ui_label_verified=False,native_semantics_verified=False)


def main():
    folder=ROOT/'data/night-001-career-r1';path=folder/'R2/coverage.json'
    report=audit(read(path));report['input_sha256']=sha256(path.read_bytes().replace(b'\r\n',b'\n')).hexdigest()
    write(folder/'training-code-coverage.json',report)
    print(json.dumps(report['total']))


if __name__=='__main__':main()

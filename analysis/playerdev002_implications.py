"""Conditional index arithmetic on source means; no match gain or CA efficiency."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def analyse():
    source = json.loads((ROOT/'data/player-development-002-training/source-table-audit.json').read_text())
    model_path = ROOT/'research/meta_score_v01_weights.json'
    model = json.loads(model_path.read_text())
    contrasts = {}
    for name in ('prespecified_46_minus_38', 'postinspection_exploratory_1_minus_0'):
        changes = source[name]['attribute_gain_differences']
        contrasts[name] = {p: sum(w*changes[k] for k, w in cfg['weights_pct'].items())/19
                          for p, cfg in model['positions'].items() if p != 'GK'}
    return dict(status='POSTINSPECTION_CONDITIONAL_INDEX_ARITHMETIC',
        condition='Source attribute-change units must equal visible1..20 units; not independently verified',
        source_sha256=source['source_sha256'],
        baseline_weights_sha256=hashlib.sha256(model_path.read_text().encode()).hexdigest(),
        baseline_hash_encoding='UTF-8 LF normalized',
        index_gain_differences=contrasts, actual_match_gain=None,
        actual_ca_efficiency=None, pa_feasibility=None,
        weights_changed=False, prediction_improvement_validated=False)


if __name__ == '__main__':
    path = ROOT/'data/player-development-002-training/conditional-index.json'
    path.write_text(json.dumps(analyse(), indent=2, allow_nan=False)+'\n', encoding='utf8', newline='\n')

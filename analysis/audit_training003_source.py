"""Read-only audit of the pinned Harvestgreen FM27 training workbook.

Does not execute Excel formulas, open saves, or infer independent replicates.
Only compact derived summaries are exported, never the full source table.
"""
import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

EXPECTED_SHA256 = '005a704ed0f9205b8003c150ab182f0944d7cea2f8c8745078344eac612c3552'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
ATTRS = {'acceleration': 'AM', 'pace': 'AS', 'jumping_reach': 'AN',
         'stamina': 'AP', 'anticipation': 'AK', 'finishing': 'U',
         'strength': 'AR', 'agility': 'AO', 'balance': 'AQ',
         'concentration': 'AB', 'dribbling': 'R'}


def extract(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError('Source SHA256 mismatch; do not silently accept a new workbook')
    with zipfile.ZipFile(path) as archive:
        strings = [''.join(e.itertext()) for e in ET.fromstring(
            archive.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
        values = {}
        for cell in sheet.findall('.//s:c', NS):
            value = cell.find('s:v', NS)
            if value is not None:
                values[cell.get('r')] = strings[int(value.text)] if cell.get('t') == 's' else float(value.text)
        formulas = len(sheet.findall('.//s:f', NS))
    return raw, sheet, values, formulas


def analyse(path):
    raw, sheet, values, formulas = extract(path)
    plans = {}
    for row in sheet.findall('s:sheetData/s:row', NS):
        r = int(row.get('r'))
        plan_id = values.get(f'A{r}')
        if isinstance(plan_id, float) and plan_id.is_integer():
            if int(plan_id) in plans:
                raise ValueError('Duplicate plan ID')
            plans[int(plan_id)] = r
    if set(plans) != set(range(51)):
        raise ValueError('Expected all 51 source plans, IDs 0..50')
    columns = [c for c in values if c.endswith('12') and c not in {'B12', 'E12'}]
    missing = [f'{c[:-2]}{r}' for c in columns for r in plans.values()
               if not isinstance(values.get(f'{c[:-2]}{r}'), float)]
    def profile(plan):
        r = plans[plan]
        return {'plan_id': plan, 'source_row': r,
                'additional_focus': values.get(f'I{r}').strip(),
                'ca_gain': values.get(f'J{r}'),
                'attribute_gains': {a: values.get(f'{c}{r}') for a, c in ATTRS.items()}}
    profiles = {p: profile(p) for p in (0, 1, 38, 46)}
    def contrast(a, b):
        aa, bb = profiles[a], profiles[b]
        return {'intervention_plan': a, 'comparator_plan': b,
                'ca_gain_difference': aa['ca_gain'] - bb['ca_gain'],
                'attribute_gain_differences': {k: aa['attribute_gains'][k] - bb['attribute_gains'][k] for k in ATTRS},
                'quickness_mean_gain_difference': sum(aa['attribute_gains'][k] - bb['attribute_gains'][k] for k in ('acceleration', 'pace')) / 2,
                'confidence_interval': None, 'p_value': None,
                'independent_career_pairs': None}
    return {'schema': 'train003.original-workbook-audit.v1',
            'source_url': 'https://pixeldrain.com/api/file/92NJyBDb',
            'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_bytes': len(raw),
            'source_sheet': 'Sheet1', 'source_plan_count': len(plans),
            'source_endpoint_columns': len(columns), 'source_numeric_endpoints': len(columns) * len(plans),
            'missing_endpoint_cells': missing, 'formula_cells': formulas,
            'author_reported_player_sample_range': [20, 30], 'sample_locator': 'A10',
            'author_reported_months': 12, 'author_reported_matches': 100,
            'pa_claim_conflict': {'chinese_A1': 130, 'english_A2': 150},
            'game_build': None, 'independent_career_replicates': None,
            'profiles': list(profiles.values()), 'prespecified_46_minus_38': contrast(46, 38),
            'postinspection_exploratory_1_minus_0': contrast(1, 0),
            'endpoint_units': 'author-reported mean season attribute changes; display/raw scale not independently calibrated',
            'native_measurements': False, 'causal_effect_identified': False,
            'new_career_arms': 0, 'new_calendar_advances': 0}


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('workbook', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = json.dumps(analyse(args.workbook), indent=2, ensure_ascii=False, allow_nan=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding='utf-8', newline='\n')
    else:
        print(report)


if __name__ == '__main__':
    main()

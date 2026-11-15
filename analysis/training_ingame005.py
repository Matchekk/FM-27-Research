"""Descriptive analysis of the single-career FM27 in-game pilot. No game access."""
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.native import require, rows, write

START = date(2027, 1, 16)
NUMBERS = {
    'acceleration_ui': (1, 20), 'pace_ui': (1, 20),
    'stored_ca': (0, 200), 'stored_pa': (0, 200),
    'condition_ui': (0, 100), 'sharpness_ui': (0, 100),
    'minutes_current_season': (0, 100000), 'pilot_injury_days': (0, 56),
}


def summarize(data):
    require(bool(data), 'No measured observations')
    observed = {}
    for row in data:
        require(row['experiment'] == 'TRAIN-005-INGAME', 'Different experiment')
        require(row['career_cluster'] == 'C001' and row['player'] == 'P001',
                'Single shared career/player required; no invented replication')
        require(row['identity_verified'] is True, 'Player identity was not verified')
        require(row['ca_measure'] == 'STORED_CA', 'CA and RCA must remain separate')
        require(row['attribute_resolution'] == 'ROUNDED_UI', 'Mixed attribute units')
        arm, day = row['arm'], row['elapsed_days']
        require(arm in ('A', 'B') and type(day) is int and 0 <= day <= 56,
                'Invalid arm or follow-up')
        require((date.fromisoformat(row['game_date']) - START).days == day,
                'Calendar date and follow-up disagree')
        require((arm, day) not in observed, 'Duplicate arm/time endpoint')
        for key, (low, high) in NUMBERS.items():
            value = row[key]
            require(value is None or type(value) is int and low <= value <= high,
                    f'Invalid measured value: {key}')
        require(bool(re.fullmatch('[0-9a-f]{64}', row['profile_sha256'])),
                'Profile provenance hash missing')
        require(row['stored_ca'] is None or bool(re.fullmatch(
            '[0-9a-f]{64}', row['native_inventory_sha256'] or '')),
            'Stored CA requires native measurement provenance')
        observed[arm, day] = row

    result = {'experiment': 'TRAIN-005-INGAME', 'independent_career_clusters': 1,
              'players': 1, 'planned_arms': 2, 'completed_arms': 0,
              'complete_career_pairs': 0, 'primary_contrast_B_minus_A': None,
              'confidence_interval': None, 'p_value': None, 'arms': {}}
    gains = {}
    for arm in ('A', 'B'):
        points = sorted(day for a, day in observed if a == arm)
        if not points:
            result['arms'][arm] = {'status': 'NOT_YET_MEASURED'}
            continue
        require(points[0] == 0, 'Follow-up without the same-player baseline')
        baseline, last = observed[arm, 0], observed[arm, points[-1]]
        require(baseline['focus_code'] == (-1 if arm == 'A' else 9),
                'Control/intervention assignment swapped or unverified')
        def delta(key):
            before, after = baseline[key], last[key]
            return after - before if before is not None and after is not None else None
        acc, pace = delta('acceleration_ui'), delta('pace_ui')
        quickness = (acc + pace) / 2 if acc is not None and pace is not None else None
        complete = points[-1] == 56
        result['completed_arms'] += complete
        result['arms'][arm] = {
            'status': 'COMPLETED_56_DAYS' if complete else 'INCOMPLETE',
            'observations': len(points), 'last_elapsed_days': points[-1],
            'last_game_date': last['game_date'],
            'delta_acceleration_ui': acc, 'delta_pace_ui': pace,
            'delta_quickness_ui_at_last_observation': quickness,
            'delta_stored_ca': delta('stored_ca'), 'delta_stored_pa': delta('stored_pa'),
            'delta_minutes_current_season': delta('minutes_current_season'),
            'pilot_injury_days': last['pilot_injury_days'],
            'observed_focus_codes': sorted({observed[arm, d]['focus_code'] for d in points
                                            if observed[arm, d]['focus_code'] is not None}),
        }
        if complete:
            gains[arm] = quickness
    if result['completed_arms'] == 2:
        for key in ('acceleration_ui', 'pace_ui', 'stored_ca', 'stored_pa'):
            require(observed['A', 0][key] == observed['B', 0][key],
                    'Paired baseline profiles differ')
        result['complete_career_pairs'] = 1
        if all(gains[a] is not None for a in ('A', 'B')):
            result['primary_contrast_B_minus_A'] = gains['B'] - gains['A']
    result['status'] = ('SINGLE_PAIR_DESCRIPTIVE' if result['complete_career_pairs']
                        else 'INCOMPLETE_NO_PRIMARY_CONTRAST')
    return result


if __name__ == '__main__':
    folder = ROOT / 'data/player-development-004'
    result = summarize(rows(folder / 'observations.jsonl'))
    write(folder / 'analysis.json', result)
    print(json.dumps(result, ensure_ascii=False))

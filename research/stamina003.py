"""Own MECH-003 intentions and strict input audits, never a native launcher."""
from copy import deepcopy
import struct

from .core import config_hash
from .native import event, read, require, rows
from .validation003 import validate_attributes

EXPERIMENT = 'MECH-003-STAMINA-R0'
CONTEXTS = ('high_press', 'deep_block')
ARMS = ('R00', 'R10', 'R01', 'R11')
STAMINA_INDEX = 52
PRESS_GROUP = 10
PRESS_IDS = (1313689463, 2000905329)
PRESS_BITS = (0, 66)
LEVELS = ((-1, -1), (1, -1), (-1, 1), (1, 1))
COEFFICIENTS = {'STAMINA': (-.5, .5, -.5, .5),
                'PRESS': (-.5, -.5, .5, .5),
                'STAMINAxPRESS': (1., -1., -1., 1.)}
SECONDARY = ('points', 'gf', 'ga', 'xgf', 'xga')
SECONDARY_PAIRS = (*(('STAMINA', m) for m in SECONDARY),
                   ('PRESS', 'xgd'), ('STAMINAxPRESS', 'xgd'))


def matrix():
    return [dict(id=arm, levels={'STAMINA': sta, 'PRESS': press},
                 stamina_raw=80 if sta == 1 else 40,
                 pressing_id=PRESS_IDS[int(press == 1)], pressing_bit=PRESS_BITS[int(press == 1)])
            for arm, (sta, press) in zip(ARMS, LEVELS, strict=True)]


def treatment(arm):
    require(arm in ARMS, 'Unknown arm')
    return matrix()[ARMS.index(arm)]


def apply_arm(base, side, arm):
    require(type(side) is int and side in (0, 1), 'Invalid tested side')
    t = treatment(arm)
    require(base.get('rules') == 'game' and base.get('fixture') == 'bundled_match_pkm', 'Rules/fixture drift')
    require('experimental_execution' not in base and 'away_tactic_pool' not in base,
            'Execution and uniform normalization forbidden, including disabled keys')
    result = deepcopy(base)
    team = result['teams'][side]
    require(team['roster_size'] == 23 and len(team['players']) >= 23, 'Active roster drift')
    lineup = team['lineup']
    require(len(lineup) == len(set(lineup)) == 11 and all(type(i) is int and 0 <= i < 23 for i in lineup),
            'Starting roster binding invalid')
    require(len(team['phases']) == 2 and all(len(p) == 11 for p in team['phases']) and
            team['phases'][0][0]['position'] == 'GK' and team['phases'][1][0]['position'] == 'GK',
            'D00 goalkeeper/phase binding missing')
    require(team['instructions'][str(PRESS_GROUP)] == PRESS_IDS[0], 'D00 Standard pressing differs')
    changes = []
    for roster_slot in lineup[1:]:
        values = team['players'][roster_slot]['attributes']
        validate_attributes(values)
        require(values[15:] == [60]*54, 'Frozen raw60 ability baseline differs')
        values[STAMINA_INDEX] = t['stamina_raw']
        changes.append(dict(side=side, roster_slot=roster_slot, attribute=STAMINA_INDEX,
                            before=60, after=t['stamina_raw']))
    team['instructions'][str(PRESS_GROUP)] = t['pressing_id']
    return result, changes


def audit_binary(before, after, side, arm, changes):
    require(before[:8] == after[:8] == b'FM27CFG1' and before[:12] == after[:12] and
            len(before) == len(after) and (len(before)-12) % 20 == 0, 'Binary header/count drift')
    a, b = (list(struct.iter_unpack('<5I', payload[12:])) for payload in (before, after))
    wanted = {((1, side, c['roster_slot'], STAMINA_INDEX, 60),
               (1, side, c['roster_slot'], STAMINA_INDEX, c['after'])) for c in changes}
    t = treatment(arm)
    if t['pressing_id'] != PRESS_IDS[0]:
        wanted.add(((2, side, PRESS_GROUP, 0, PRESS_IDS[0]), (2, side, PRESS_GROUP, 0, t['pressing_id'])))
    actual = {(x, y) for x, y in zip(a, b, strict=True) if x != y}
    require(actual == wanted and len(changes) == len(wanted)-int(t['pressing_bit'] != 0) == 10,
            'Undeclared/missing Stamina/pressing change')
    return dict(changed_records=len(actual), undeclared_changes=0,
                records=[dict(before=list(x), after=list(y)) for x, y in zip(a, b, strict=True) if x != y])


def audit_contract(lab, row, job, task, log):
    evidence = rows(log)
    require(event(evidence, 'native_profile_bindings_verified')['fields'] == 1058, 'Profile readbacks incomplete')
    binding = event(evidence, 'native_player_tactic_bindings_verified')
    require(binding['players'] == 22 and binding['phases'] == 2, 'Actual player phase bindings incomplete')
    dump, config = read(task['dump']), job['config']
    role_cells = pi_cells = pi_groups = 0
    for side, team in enumerate(config['teams']):
        flags = int.from_bytes(bytes.fromhex(dump['teams'][side]['creator_hex'])[:16], 'little')
        for group, choice in team['instructions'].items():
            options = lab.server.GROUPS[int(group)]['options']
            bit = next(o['native_bit'] for o in options if o['id'] == choice)
            active = {o['native_bit'] for o in options if o['native_bit'] and flags >> o['native_bit'] & 1}
            require(active == ({bit} if bit else set()), 'Native team instruction drift')
        for phase, cells in enumerate(team['phases']):
            for index, cell in enumerate(cells):
                slot = lab.server.OOP_MAP[side][index] if phase else index
                raw = bytes.fromhex(dump['teams'][side]['tactical_slots'][phase][slot])
                require(struct.unpack_from('<I', raw)[0] == lab.server.POSITIONS[cell['position']]['mask'], 'Position drift')
                require(struct.unpack_from('<Q', raw, 64)[0] == int(lab.server.ROLES[cell['role']]['flags']) | int(cell['duty']), 'Role/duty drift')
                role_cells += 1
                pi = dump['teams'][side]['personal_instructions'][phase][slot]
                require(pi['target_player'] == cell['target_player'] and pi['target_position'] == cell['target_position'], 'PI targets drift')
                require(set(cell['instructions']) == {str(k) for k in lab.server.PIS}, 'PI groups missing')
                for group, definition in lab.server.PIS.items():
                    options = {o['id'] for o in definition['options'] if o['id']}
                    active = {v for v in options if int(pi['flags']) >> v & 1}
                    choice = cell['instructions'][str(group)]
                    require(active == ({choice} if choice else set()), 'PI drift')
                    pi_groups += 1
                pi_cells += 1
    require((role_cells, pi_cells, pi_groups) == (44, 44, 748), 'Native cell coverage incomplete')
    t = treatment(job['arm'])
    values = [dump['teams'][job['side']]['players'][i]['attributes'][STAMINA_INDEX]
              for i in config['teams'][job['side']]['lineup'][1:]]
    require(values == [t['stamina_raw']]*10, 'Stamina raw dose not native')
    # NativeLab additionally compares every attribute/active identity after original preparation.
    return dict(input_contract_verified=True, profile_fields_verified=1058, native_roles_verified=44,
                native_pi_cells_verified=44, native_pi_groups_verified=748,
                native_attribute_values_verified=3174, native_stamina_values=values,
                native_pressing_bit=t['pressing_bit'], factor_levels=t['levels'],
                design_matrix_sha256=config_hash(matrix()))

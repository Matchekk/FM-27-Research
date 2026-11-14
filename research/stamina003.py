"""Own MECH-003 intentions and strict input audits, never a native launcher."""
from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import re
import struct
from threading import Lock

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
PROCESS_CAPS = {'technical':36,'main':514}


def probe_jobs():
    return [dict(key=f'loader-check-image-{p}',kind='main' if p=='main' else 'technical',phase=p,probe='loader')
            for p in ('prepare','technical','main')]+[
        dict(key=f'worker-capabilities-{p}',kind='main' if p=='main' else 'technical',phase=p,probe='capabilities')
        for p in ('technical','main')]


def parse_popen_event(args):
    """CPython Windows emits executable=None and one quoted commandline string."""
    executable,argv,_,_=args
    if isinstance(argv,str):
        require(os.name=='nt' and argv and '\0' not in argv,'Invalid Windows Popen commandline')
        import ctypes
        from ctypes import wintypes
        shell=ctypes.WinDLL('shell32',use_last_error=True);kernel=ctypes.WinDLL('kernel32',use_last_error=True)
        shell.CommandLineToArgvW.argtypes=[wintypes.LPCWSTR,ctypes.POINTER(ctypes.c_int)]
        shell.CommandLineToArgvW.restype=ctypes.POINTER(wintypes.LPWSTR)
        kernel.LocalFree.argtypes=[ctypes.c_void_p];kernel.LocalFree.restype=ctypes.c_void_p
        count=ctypes.c_int();pointer=shell.CommandLineToArgvW(argv,ctypes.byref(count))
        if not pointer:raise ctypes.WinError(ctypes.get_last_error())
        try:values=[pointer[i] for i in range(count.value)]
        finally:kernel.LocalFree(ctypes.cast(pointer,ctypes.c_void_p))
    else:
        require(type(argv) in (list,tuple),'Unknown Popen argument representation')
        values=list(argv)
    require(values and all(type(v) is str and '\0' not in v for v in values),'Invalid Popen argument vector')
    return Path(os.fsdecode(executable) if executable is not None else values[0]),values


class HostLaunchAudit:
    """Opt-in audit hook installed in the contained study child before server import.

    Records intent before every Python-created native host. Match slots and warm
    process starts are deliberately separate dimensions. Unknown launches fail
    before Popen; a launch exception remains a started attempt, never a zero.
    """
    def __init__(self,phase,host,ledger,admission,engine_dll=None):
        require(phase in ('prepare','technical','main'),'Unknown host-audit phase')
        self.phase,self.host,self.ledger,self.admission=phase,Path(host).resolve(),Path(ledger),admission
        self.engine_dll=Path(engine_dll).resolve() if engine_dll is not None else None
        self.counts={};self.lock=Lock();self.control_python=None

    @contextmanager
    def negative_capsule(self,python):
        require(self.phase=='technical' and self.control_python is None,'Negative capsule phase differs')
        self.control_python=Path(python).resolve()
        try:yield
        finally:self.control_python=None

    def __call__(self,event,args):
        if event!='subprocess.Popen':return
        path,argv=parse_popen_event(args)
        if path.name.lower() in ('git','git.exe','gh','gh.exe'):return
        if path.resolve()!=self.host:
            require(self.control_python is not None and path.resolve()==self.control_python,
                    'Unexpected executable in contained study')
            require(len(argv)==4 and argv[1]=='-I' and
                    Path(argv[2]).resolve()==Path(__file__).with_name('native_process005.py').resolve() and
                    argv[3]=='--capsule','Unknown containment launcher grammar')
            with self.lock:
                require(self.counts.get('negative_capsule',0)==0,'Repeated negative capsule launcher')
                self.counts['negative_capsule']=1
            return
        require(Path(argv[0]).resolve()==self.host,'Native executable/argv0 mismatch')
        if len(argv)==3 and argv[1]=='--check-image':
            require(self.engine_dll is None or Path(argv[2]).resolve()==self.engine_dll,'Loader DLL path differs')
            kind='loader';key=f'loader-check-image-{self.phase}';limit=1
        elif argv[1:]==['--worker-capabilities']:
            require(self.phase!='prepare','Capabilities in prepare forbidden')
            kind='capabilities';key=f'worker-capabilities-{self.phase}';limit=1
        elif len(argv)==9 and argv[1]=='--worker-manifest' and argv[3]=='--output' and argv[5:8]==['--tick-step','1','--cancel-event']:
            require(self.phase!='prepare','Warmworker in prepare forbidden')
            require(Path(argv[2]).resolve().is_relative_to(self.ledger.parent.resolve()) and
                    Path(argv[4]).resolve().is_relative_to(self.ledger.parent.resolve()) and
                    re.fullmatch(r'Local\\FM27MatchCancel_[0-9]+_[0-9a-f]{32}',argv[8]),
                    'Warmworker paths or cancellation identity differ')
            kind='worker_start';key=None;limit=4 if self.phase=='technical' else 64
        else:raise ValueError('Unregistered native command; negative uses contained_call separately')
        with self.lock:
            self.admission()
            count=self.counts.get(kind,0)+1
            require(count<=limit,'Unexpected/repeated native host launch')
            self.counts[kind]=count
            row=dict(phase=self.phase,kind=kind,key=key or f'worker-start-{self.phase}-{count:03d}',
                     status='started',ordinal=count,utc=datetime.now(timezone.utc).isoformat())
            with self.ledger.open('a',encoding='utf8') as stream:
                stream.write(json.dumps(row)+'\n');stream.flush();os.fsync(stream.fileno())

    def negative_permission(self):
        with self.lock:
            self.admission()
            require(self.phase=='technical' and self.counts.get('negative_permission',0)==0,'Repeated negative host permission')
            self.counts['negative_permission']=1
            with self.ledger.open('a',encoding='utf8') as stream:
                stream.write(json.dumps(dict(phase=self.phase,kind='negative',key='negative-binary',
                    status='start_permission_sent',ordinal=1,utc=datetime.now(timezone.utc).isoformat()))+'\n')
                stream.flush();os.fsync(stream.fileno())

    def require_complete(self):
        expected={'loader':1} if self.phase=='prepare' else {'loader':1,'capabilities':1,'worker_start':4 if self.phase=='technical' else 64}
        if self.phase=='technical':expected.update(negative_capsule=1,negative_permission=1)
        require(self.counts==expected,'Incomplete/extra native host launch inventory')
        return self.counts.copy()


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

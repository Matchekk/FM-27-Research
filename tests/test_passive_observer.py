"""Own synthetic observer fixtures; no native processes or game files."""
from copy import deepcopy
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch

from research.passive_observer import (FIELDS, VERSION, audit_trace, equivalence,
    instrument_source, read_rows, snapshot)


def fixture():
    dump = dict(teams=[]); players=[]
    for side in (0,1):
        team=dict(side=side,count=23,players=[])
        for slot in range(23):
            identity=1+100*side+slot;tail=bytearray(0x81b)
            for key,offset in FIELDS.items():struct.pack_into('<H',tail,offset-0x4c5,0 if key=='fatigue_raw' else 10000)
            tail[0xcba-0x4c5:0xcba-0x4c5+33]=bytes([slot+1])*33
            team['players'].append(dict(index=slot,id=identity,input_tail_hex=tail.hex()))
            players.append(dict(side=side,roster_index=slot,id=identity,
                **{k:0 if k=='fatigue_raw' else 10000 for k in FIELDS},
                condition_accumulator_raw=10000,sharpness_penalty_raw=0,
                effectiveness_region_hex=(bytes([slot+1])*33).hex(),runtime_near_morale_region_hex='00'*0x70,
                statistics_cache_region_hex='00'*0x10 if slot<11 else None))
        dump['teams'].append(team)
    captures=[]
    for stage,ordinal,tick,before,target in [('prepared',0,0,0,0),('first_advance',1,1,0,1),('finished',22000,22000,22000,22000)]:
        captures.append(dict(event='native_passive_state',schema=VERSION,stage=stage,advance_ordinal=ordinal,
            tick=tick,tick_before=before,requested_target=target,clock=tick,seed=123,
            match_version_raw=0x1b000000,players=deepcopy(players)))
    evidence=[dict(event='native_input_seed',override=True,effective_seed=123),
        dict(event='native_profile_bindings_verified',fields=1058),
        dict(event='native_player_tactic_bindings_verified',players=22,phases=2),
        dict(event='native_scenario_readback_verified',records=5557,after_original_preparation=True),
        *captures,dict(event='natural_match_finished',full_match_completed=True,tick=22000,clock=22000,score=[1,0]),
        dict(event='native_match_statistics',source='original_team_statistics',teams=[dict(side=s,xg=1.,shots=10,
             shots_on_target=4,passes=100,completed_passes=80,possession=.5,possession_ticks=100)for s in(0,1)])]
    return dump,evidence


class ObserverTests(unittest.TestCase):
    def test_three_real_stage_contract_and_dump_cross_binding(self):
        dump,rows=fixture();result=audit_trace(rows,dump,123)
        self.assertTrue(result['structurally_verified'])
        self.assertEqual([s['profile_values']for s in result['captures']],[184]*3)
        self.assertFalse(result['native_release_granted']);self.assertFalse(result['startpolicy_released'])
        self.assertFalse(result['consumer_semantics_validated']);self.assertNotIn("'id':",str(result))

    def test_missing_reordered_duplicate_or_falsely_first_progress_fails(self):
        dump,evidence=fixture()
        for edit in ('missing','duplicate','reordered','ordinal','target','before','no_progress'):
            rows=deepcopy(evidence)
            if edit=='missing':rows.pop(5)
            elif edit=='duplicate':rows.insert(5,deepcopy(rows[4]))
            elif edit=='reordered':rows[4],rows[5]=rows[5],rows[4]
            elif edit=='ordinal':rows[5]['advance_ordinal']=0
            elif edit=='target':rows[5]['requested_target']=2
            elif edit=='before':rows[5]['tick_before']=1
            else:rows[5]['tick']=0
            with self.subTest(edit=edit),self.assertRaises(ValueError):audit_trace(rows,dump,123)

    def test_raw_profiles_hex_ids_counts_types_and_seed_are_strict(self):
        dump,evidence=fixture()
        for edit in ('bool','range','hex','duplicate_id','roster_slot','side','seed','dump'):
            rows=deepcopy(evidence);native=deepcopy(dump)
            if edit=='bool':rows[4]['players'][0]['condition_raw']=True
            elif edit=='range':rows[4]['players'][0]['condition_raw']=65536
            elif edit=='hex':rows[4]['players'][0]['effectiveness_region_hex']='0'*65
            elif edit=='duplicate_id':rows[4]['players'][1]['id']=rows[4]['players'][0]['id']
            elif edit=='roster_slot':rows[4]['players'][1]['roster_index']=0
            elif edit=='side':rows[5]['players'][0]['side']=1
            elif edit=='seed':rows[5]['seed']=456
            else:native['teams'][0]['players'][0]['input_tail_hex']='00'*0x81b
            with self.subTest(edit=edit),self.assertRaises(ValueError):audit_trace(rows,native,123)

    def test_forbidden_execution_and_missing_native_receipts_fail(self):
        dump,evidence=fixture()
        for name in ('experimental_engine_version','native_execution_probe','native_execution_context_bound'):
            with self.assertRaises(ValueError):audit_trace(evidence+[dict(event=name)],dump,123)
        for index in (0,1,2,3,7):
            rows=deepcopy(evidence);rows.pop(index)
            with self.assertRaises(ValueError):audit_trace(rows,dump,123)

    def test_natural_finish_version_and_prepared_bytes_cannot_be_forged(self):
        dump,evidence=fixture()
        for edit in ('finish','version','raw','future'):
            rows=deepcopy(evidence)
            if edit=='finish':rows[7]['tick']-=1
            elif edit=='version':rows[5]['match_version_raw']+=1
            elif edit=='raw':rows[4]['players'][0]['effectiveness_region_hex']='00'*33
            else:rows[6]['tick']=0
            with self.assertRaises(ValueError):audit_trace(rows,dump,123)

    def test_four_mode_exact_results_and_no_silent_observer_off(self):
        _,evidence=fixture();plain=[r for r in evidence if r['event']!='native_passive_state']
        modes=dict(reference=deepcopy(plain),observer_off=deepcopy(plain),observer_on=deepcopy(evidence),observer_on_repeat=deepcopy(evidence))
        self.assertTrue(equivalence(modes,123)['result_equivalence_verified'])
        modes['observer_on_repeat'][-2]['score']=[0,0]
        with self.assertRaises(ValueError):equivalence(modes,123)

    def test_runtime_cache_missing_is_not_zero_and_repeat_state_is_bound(self):
        dump,rows=fixture();rows[4]['players'][0]['statistics_cache_region_hex']=None
        with self.assertRaises(ValueError):audit_trace(rows,dump,123)
        dump,rows=fixture();result=audit_trace(rows,dump,123)
        self.assertEqual(result['captures'][0]['runtime_cache_players'],22)
        plain=[r for r in rows if r['event']!='native_passive_state']
        modes=dict(reference=deepcopy(plain),observer_off=deepcopy(plain),observer_on=deepcopy(rows),observer_on_repeat=deepcopy(rows))
        modes['observer_on_repeat'][4]['players'][0]['statistics_cache_region_hex']='00'*9+'01'+'00'*6
        with self.assertRaises(ValueError):equivalence(modes,123)
        modes['observer_on_repeat']=deepcopy(rows);modes['observer_off']=deepcopy(rows)
        with self.assertRaises(ValueError):equivalence(modes,123)

    def test_json_duplicate_nonfinite_and_invalid_snapshots_reject(self):
        with tempfile.TemporaryDirectory()as tmp:
            path=Path(tmp)/'own.jsonl'
            for value in ('{"a":1,"a":2}\n','{"a":NaN}\n'):
                path.write_text(value,encoding='utf8')
                with self.assertRaises(ValueError):read_rows(path)
        _,evidence=fixture();row=deepcopy(evidence[4]);row['native_released']=True
        with self.assertRaises(ValueError):snapshot(row)

    def test_disabled_source_identity_and_five_exact_insertion_sites(self):
        source=('// own synthetic source fixture\n#include "native_execution_experiment.h"\n'
                '    source_generation_install(match);\n    desktop_initial_state_snapshot(match);\n'
                '        if(flags&4){\n'
                '        if(after==tick){fprintf(log_file,"{\\"event\\":\\"native_match_stalled\\",\\"tick\\":%d}\\n",tick);fflush(log_file);desktop_finish_and_exit(91);}\n')
        self.assertEqual(instrument_source(source,False).encode(),source.encode())
        changed=instrument_source(source)
        self.assertEqual(changed.count('passive_observer_snapshot('),3)
        self.assertEqual(changed.count('passive_observer_options();'),1)
        self.assertLess(changed.index('passive_observer_options();'),changed.index('source_generation_install'))
        self.assertGreater(changed.index('"first_advance"'),changed.index('desktop_finish_and_exit(91)'))
        with self.assertRaises(ValueError):instrument_source(changed)
        with self.assertRaises(ValueError):instrument_source(source.replace('if(flags&4)','if(flags&8)'))

    def test_header_is_read_only_not_an_execution_hook(self):
        root=Path(__file__).resolve().parents[1];header=(root/'adapters/passive_observer_v1.h').read_text(encoding='utf8')
        for prohibited in ('VirtualProtect','WriteProcessMemory','SetThreadContext','execution_apply(',
                           'execution_install(','memset(','memcpy(','at('):
            self.assertNotIn(prohibited,header)
        self.assertIn('GetEnvironmentVariableW',header)
        self.assertIn('VirtualQuery',header)
        self.assertIn('actor+0xcba,33',header)
        self.assertIn('actor+0x1df0,0x70',header)

    def test_private_builder_rejects_foreign_trees_before_git_or_compiler(self):
        from analysis.build_passive_observer import build
        with tempfile.TemporaryDirectory()as tmp:
            base=Path(tmp);upstream=base/'upstream';game=base/'game'
            with patch('analysis.build_passive_observer.subprocess.check_output',side_effect=AssertionError('No process allowed')):
                for output in (upstream/'local/new',game/'local/new',base/'public'):
                    with self.assertRaises(ValueError):build(upstream,game,output,base/'compiler',base/'sdk')


if __name__=='__main__':unittest.main()

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

from research.career_diag004r3 import (TARGET_MESSAGE,STAGES,declared_markers,full_ledger,
    marker_evidence,model_fields,observe_final_call,source_hash)


class ReaderCheckError(Exception):pass


def selection(section,block_start,block_end,layout,error):
    cursor=block_start+2
    raise error


class PassiveDiagnosticTests(unittest.TestCase):
    def invoke_failure(self,section_bytes=b'..XYZ......',start=0,end=10,markers=(b'abc',b'def')):
        error=ReaderCheckError('PRIVATE_PATH: '+TARGET_MESSAGE)
        receipt={};layout=SimpleNamespace(taker_markers=markers)
        with self.assertRaises(ReaderCheckError) as caught:
            observe_final_call(selection,selection,receipt,section_bytes,start,end,layout,error)
        self.assertIs(caught.exception,error)
        return receipt,error

    def test_same_exception_and_only_bounded_private_offsets_and_booleans(self):
        receipt,_=self.invoke_failure()
        self.assertEqual(receipt['status'],'captured_final_target_failure')
        self.assertEqual((receipt['block_start'],receipt['block_end'],receipt['cursor']),(0,10,2))
        self.assertTrue(receipt['failure_consistent_with_expected_marker_tests'])
        self.assertTrue(all(not r['equals_expected_at_cursor'] for r in receipt['marker_checks']))
        self.assertNotIn('PRIVATE_PATH',str(receipt));self.assertNotIn('XYZ',str(receipt))
        self.assertFalse(receipt['scan_performed']);self.assertFalse(receipt['grammar_changed'])

    def test_return_and_arguments_untouched_and_internal_candidate_error_not_captured(self):
        token=object();original=ReaderCheckError(TARGET_MESSAGE);receipt={}
        def outer(arg,*,key):
            self.assertIs(arg,token);self.assertIs(key,token)
            try:selection(b'...ZZZ',0,6,SimpleNamespace(taker_markers=(b'abc',)),original)
            except ReaderCheckError:pass
            return token
        self.assertIs(observe_final_call(outer,selection,receipt,token,key=token),token)
        self.assertEqual(receipt,dict(status='no_final_exception',target_frame_observed=False))

    def test_unrelated_error_identity_and_no_target_frame(self):
        error=ValueError('PRIVATE_PATH');receipt={}
        def operation():raise error
        with self.assertRaises(ValueError) as caught:observe_final_call(operation,selection,receipt)
        self.assertIs(caught.exception,error)
        self.assertEqual(receipt['status'],'non_target_error')

    def test_invalid_frame_and_marker_shape_rejected_without_recovery(self):
        receipt,_=self.invoke_failure(start=5,end=4)
        self.assertEqual(receipt['status'],'observer_rejected_frame')
        receipt,_=self.invoke_failure(markers=(b'A'*17,))
        self.assertEqual(receipt['status'],'observer_rejected_frame')
        receipt,_=self.invoke_failure(markers=())
        self.assertEqual(receipt['status'],'observer_rejected_frame')

    def test_no_scan_even_if_expected_marker_exists_nearby(self):
        receipt,_=self.invoke_failure(section_bytes=b'..XYZabc...',markers=(b'abc',))
        self.assertFalse(receipt['marker_checks'][0]['equals_expected_at_cursor'])
        self.assertEqual(receipt['cursor'],2)

    def test_failed_marker_near_end_records_incomplete_range(self):
        receipt,_=self.invoke_failure(section_bytes=b'..X',end=3,markers=(b'abc',))
        self.assertFalse(receipt['marker_checks'][0]['fully_inside_block'])
        self.assertEqual(receipt['bytes_remaining_in_block'],1)

    def test_existing_receipt_refused_before_operation(self):
        operation=unittest.mock.Mock()
        with self.assertRaises(ValueError):observe_final_call(operation,selection,{'already':'retained'})
        operation.assert_not_called()

    def test_preparation_and_failed_missing_ledgers_do_not_release_anything(self):
        receipt=full_ledger([dict(stage='tactics_final_call',status='failed',error_type='ReaderCheckError',private='PRIVATE')])
        self.assertEqual(len(receipt['stages']),len(STAGES))
        self.assertEqual(sum(x['status']=='not_started' for x in receipt['stages']),4)
        self.assertNotIn('PRIVATE',str(receipt));self.assertIsNone(receipt['reader_processes_started'])
        self.assertEqual(full_ledger()['reader_processes_started'],0)
        self.assertFalse(receipt['tactics_released']);self.assertFalse(receipt['career_advance_released'])
        unresolved=full_ledger([dict(stage='open',status='started')])
        self.assertEqual(unresolved['stages'][2]['status'],'started_unresolved')
        with self.assertRaises(ValueError):full_ledger([dict(stage='unknown',status='observed')])

    def test_source_reader_cannot_open_save_extension(self):
        with patch.object(Path,'read_bytes') as read_bytes:
            with self.assertRaises(ValueError):source_hash('approved.fm')
            read_bytes.assert_not_called()

    def test_layout_and_model_inventory_is_static_not_python_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'_layouts').mkdir()
            (root/'_layouts/fm26_26_3_2.py').write_text("raise RuntimeError('must never execute')\nTACTICS = TacticsLayout(taker_markers=(bytes.fromhex('010203'),b'abc'))\n")
            (root/'_layouts/fm27_27_0_0.py').write_text("TACTICS=replace(FM26_TACTICS,selection_end_marker=b'xx')\n")
            self.assertEqual(declared_markers(root),(b'\1\2\3',b'abc'))
            (root/'models.py').write_text("raise RuntimeError('must never execute')\nclass Example:\n team_id:int\n sessions:tuple\n UNKNOWN_KEYS:tuple=()\n")
            self.assertEqual(model_fields(root,'models.py',('Example',)),{'Example':['team_id','sessions']})
            (root/'_layouts/fm27_27_0_0.py').write_text("TACTICS=replace(FM26_TACTICS,taker_markers=(b'new',))\n")
            with self.assertRaises(ValueError):declared_markers(root)


if __name__=='__main__':unittest.main()

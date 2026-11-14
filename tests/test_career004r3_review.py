"""Independent adversarial outer-boundary tests; all inputs are synthetic."""
from types import SimpleNamespace
import unittest

from research.career_diag004r3 import TARGET_MESSAGE,observe_final_call


class ReaderCheckError(Exception):pass


def selection(section,block_start,block_end,layout,error):
    cursor=block_start+1
    raise error


class IndependentDiagnosticTests(unittest.TestCase):
    def test_discarded_candidate_does_not_replace_later_unrelated_error(self):
        discarded=ReaderCheckError(TARGET_MESSAGE);final=ReaderCheckError('different final error');receipt={}
        def operation():
            try:selection(b'xxx',0,3,SimpleNamespace(taker_markers=(b'a',)),discarded)
            except ReaderCheckError:pass
            raise final
        with self.assertRaises(ReaderCheckError) as caught:observe_final_call(operation,selection,receipt)
        self.assertIs(caught.exception,final)
        self.assertEqual(receipt,dict(status='non_target_error',target_frame_observed=False))

    def test_same_named_target_error_without_exact_code_frame_is_not_claimed(self):
        final=ReaderCheckError(TARGET_MESSAGE);receipt={}
        def operation():raise final
        with self.assertRaises(ReaderCheckError) as caught:observe_final_call(operation,selection,receipt)
        self.assertIs(caught.exception,final)
        self.assertEqual(receipt['status'],'observer_rejected_frame')

    def test_observer_failure_preserves_original_exception_and_arguments(self):
        final=ReaderCheckError(TARGET_MESSAGE);receipt={};token=object()
        def operation(value,*,other):
            self.assertIs(value,token);self.assertIs(other,token)
            raise final
        with self.assertRaises(ReaderCheckError) as caught:
            observe_final_call(operation,object(),receipt,token,other=token)
        self.assertIs(caught.exception,final)
        self.assertEqual(receipt['status'],'observer_rejected_frame')
        self.assertEqual(receipt['observer_error_type'],'AttributeError')

    def test_excess_traceback_is_rejected_without_masking_original(self):
        final=ReaderCheckError(TARGET_MESSAGE);receipt={}
        def recurse(n):
            if n:return recurse(n-1)
            return selection(b'xxx',0,3,SimpleNamespace(taker_markers=(b'a',)),final)
        with self.assertRaises(ReaderCheckError) as caught:observe_final_call(recurse,selection,receipt,70)
        self.assertIs(caught.exception,final)
        self.assertEqual(receipt['status'],'observer_rejected_frame')

    def test_baseexception_is_not_swallowed_or_misclassified_as_parser_failure(self):
        final=KeyboardInterrupt();receipt={}
        def operation():raise final
        with self.assertRaises(KeyboardInterrupt) as caught:observe_final_call(operation,selection,receipt)
        self.assertIs(caught.exception,final);self.assertEqual(receipt,{})

    def test_maximum_width_marker_comparison_stays_at_original_cursor(self):
        final=ReaderCheckError(TARGET_MESSAGE);receipt={}
        layout=SimpleNamespace(taker_markers=(b'A'*16,))
        with self.assertRaises(ReaderCheckError):
            observe_final_call(selection,selection,receipt,b'Z'+b'B'*16+b'A'*16,0,33,layout,final)
        self.assertEqual(receipt['cursor'],1)
        self.assertFalse(receipt['marker_checks'][0]['equals_expected_at_cursor'])
        self.assertFalse(receipt['scan_performed'])


if __name__=='__main__':unittest.main()

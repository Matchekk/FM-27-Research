"""Public arithmetic/identity regressions; no network or external execution."""
from copy import deepcopy
from hashlib import sha1
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from analysis import review_external_replication001 as reviewer


class ExternalReplicationReviewTests(unittest.TestCase):
    def test_real_register_arithmetic_and_nonreplication_scope(self):
        result=reviewer.audit()
        self.assertEqual(result['sd_approximations_verified'],9)
        self.assertEqual(result['pinned_blob_entries'],18)
        self.assertFalse(result['raw_data_reproduced'])

    def test_wrong_sd_or_invented_raw_replication_is_rejected(self):
        original=json.loads(reviewer.REGISTER.read_text(encoding='utf8'))
        with tempfile.TemporaryDirectory(prefix='fm27-source-review-') as temporary:
            path=Path(temporary)/'own-register.json'
            for kind in ('sd','replication'):
                value=deepcopy(original)
                if kind=='sd':value['summary_arithmetic']['observations'][0]['approximate_contrast_SD']+=.1
                else:value['sources'][0]['independently_reproduced']=True
                path.write_text(json.dumps(value),encoding='utf8')
                with patch.object(reviewer,'REGISTER',path),self.assertRaises(ValueError):reviewer.audit()

    def test_blob_header_hash_is_actual_git_identity(self):
        payload=b'Own harmless source fixture\n'
        url='https://github.com/own/fixture/blob/'+'a'*40+'/own.txt'
        expected=sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
        with patch.object(reviewer,'get',return_value=payload):
            self.assertEqual(reviewer.verify_blob((url,expected))['git_blob_sha1'],expected)
            with self.assertRaises(ValueError):reviewer.verify_blob((url,'0'*40))


if __name__=='__main__':unittest.main()

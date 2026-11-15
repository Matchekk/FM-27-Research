import tempfile
from pathlib import Path
import unittest
from analysis.ca_profile001 import parse_profiles,split,fit,predict

class CAProfileTest(unittest.TestCase):
    def test_known_regression_and_identity_split(self):
        model=fit([1,2,3],[5,7,9]);self.assertEqual(model,dict(intercept=3.,slope=2.))
        self.assertEqual(list(predict(model,[4,5])),[11,13])
        records=[dict(split_key=f'{i:064x}') for i in range(109)]
        train,test=split(list(reversed(records)))
        self.assertEqual((len(train),len(test)),(80,29))
        self.assertFalse({p['split_key'] for p in train}&{p['split_key'] for p in test})
        with self.assertRaises(ValueError):split(records[:-1])
        with self.assertRaises(ValueError):split(records[:-1]+[records[0]])

    def test_missing_values_and_duplicates_remain_visible(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'input.csv'
            p.write_text('Unique ID,Position,CA,Pace\na,GK,100,12\nb,GK,,12\nc,GK,90,\n',encoding='utf8')
            records,quality=parse_profiles(p,{'Pace':3})
            self.assertEqual(len(records),1);self.assertEqual(len(quality['failures']),2)
            self.assertEqual(quality['rows'],3)
            p.write_text('Unique ID,Position,CA,Pace\na,GK,100,12\na,GK,90,10\n',encoding='utf8')
            with self.assertRaises(ValueError):parse_profiles(p,{'Pace':3})

if __name__=='__main__':unittest.main()

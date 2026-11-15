import itertools
import tempfile
from pathlib import Path
import unittest
from analysis.ca_efficiency001 import load_table,optimize_increments

class CAEfficiency001Test(unittest.TestCase):
    def test_solver_matches_exhaustive_search(self):
        weights={'a':2,'b':3,'c':5};values={'a':1.,'b':2.4,'c':4.1};room={'a':3,'b':2,'c':2}
        for budget in range(25):
            result=optimize_increments(weights,values,room,budget)
            brute=max(sum(n*values[a] for a,n in zip(weights,counts)) for counts in itertools.product(range(4),range(3),range(3)) if sum(n*weights[a] for a,n in zip(weights,counts))<=budget)
            self.assertAlmostEqual(result['proxy_gain'],brute)
            self.assertLessEqual(result['spent_reference_units'],budget)
            self.assertIsNone(result['actual_ca_spent'])
            self.assertIsNone(result['expected_match_gain'])

    def test_missing_cost_is_not_free(self):
        with self.assertRaises(ValueError):optimize_increments({'a':2},{'a':1,'b':2},{'a':1,'b':1},10)
        with self.assertRaises(ValueError):optimize_increments({'a':0},{'a':1},{'a':1},10)
        with self.assertRaises(ValueError):optimize_increments({'a':2},{'a':float('nan')},{'a':1},10)
        with self.assertRaises(ValueError):optimize_increments({'a':2},{'a':1},{'a':1},True)

    def test_table_duplicates_and_missing_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'table.csv'
            path.write_text('Position,Attribute,CA cost\nST,Pace,7\n',encoding='utf8')
            table,_=load_table(path);self.assertEqual(table,{'ST':{'Pace':7}})
            self.assertNotIn('Finishing',table['ST'])
            for content in ('Position,Attribute,CA cost\nST,Pace,7\nST,Pace,7\n','Position,Attribute,CA cost\nST,Pace,NaN\n','Position,Attribute,CA cost\nST,Pace,0\n'):
                path.write_text(content,encoding='utf8')
                with self.assertRaises(ValueError):load_table(path)

if __name__=='__main__':unittest.main()

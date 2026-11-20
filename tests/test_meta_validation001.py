from copy import deepcopy
import unittest

from analysis.review_meta_validation001 import DOC, audit, curvature, goals, lines, load, pair_value


class Validation001Tests(unittest.TestCase):
    def setUp(self):
        self.plan = load(DOC/'technical-plan.json')
        self.rows = lines(DOC/'technical-matches.jsonl')

    def test_actual_technical_rows_have_one_seed_and_zero_selection_pairs(self):
        result = audit(self.plan, self.rows)
        self.assertEqual((16,8,1,0), (result['technical_matches'],result['exact_aa_pairs'],
                         result['independent_technical_seeds'],result['scientific_pairs']))

    def test_identity_position_seed_fixture_and_purpose_bound_to_plan(self):
        for field,value in [('actor_token','another'),('position','CB'),('slot',2),
                            ('position_rating',20),('seed',12),('fixture_sha256','different'),
                            ('setup_sha256','other'),('kind','scientific')]:
            with self.subTest(field=field):
                rows = deepcopy(self.rows)
                rows[0][field] = value
                with self.assertRaises(ValueError):
                    audit(self.plan, rows)

    def test_repeated_or_missing_measurements_never_create_pairs(self):
        for rows in (self.rows[:-1], self.rows + self.rows[:1], [self.rows[0]] * len(self.rows)):
            with self.assertRaises(ValueError):
                audit(self.plan,rows)

    def test_chosen_gain_and_signed_utility_on_both_sides(self):
        home, away = ('fixture',0,42), ('fixture',1,42)
        a, b = {home:[2,0],away:[0,2]}, {home:[1,0],away:[0,1]}
        scores = {'v2.0':[9,10],'v2.1':[10,9]}
        self.assertEqual(pair_value(a,b,scores),dict(D=1,V=2,G=1))
        self.assertEqual(pair_value(a,b,{'v2.0':scores['v2.1'],'v2.1':scores['v2.0']})['G'],-1)
        self.assertEqual(pair_value(a,b,{'v2.0':[9,10],'v2.1':[9,10]})['G'],0)
        self.assertEqual(pair_value(a,b,{'v2.0':[9,9],'v2.1':[10,9]})['G'],0.5)
        with self.assertRaises(ValueError):
            pair_value(a,{home:b[home]},scores)
        with self.assertRaises(ValueError):
            pair_value(a,b,{'v2.1':[10,9],'v2.2':[9,10]})

    def test_null_results_and_incomplete_doses_remain_missing(self):
        for score in (None,[None,0],[],[True,0]):
            with self.assertRaises(ValueError):
                goals(score,0)
        with self.assertRaises(ValueError):
            curvature({7:0,9:0,16:1})
        self.assertEqual(curvature({7:0,9:2,16:3,19:9}),1)

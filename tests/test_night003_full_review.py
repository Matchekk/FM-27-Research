import unittest,json
from pathlib import Path
from analysis.review_night003_results import review,CONFIG
ROOT=Path(__file__).resolve().parents[1]
class FullScalarReviewTest(unittest.TestCase):
    def test_published_scalar_reviews_are_reproducible(self):
        checked=0
        for study,config in CONFIG.items():
            path=ROOT/'data'/config[0]/'independent-statistics-review.json'
            if path.exists():
                self.assertEqual(review(study),json.loads(path.read_text(encoding='utf8')));checked+=1
        self.assertGreater(checked,0)

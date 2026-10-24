import unittest
import sys
from pathlib import Path

# Add the backend folder to Python's import path
BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from services.decision_engine import classify_ai_score, build_analysis_result


class TestDecisionEngine(unittest.TestCase):

    def test_high_ai_score(self):
        self.assertEqual(classify_ai_score(0.99), "Likely AI-generated")

    def test_low_ai_score(self):
        self.assertEqual(classify_ai_score(0.05), "Likely natural")

    def test_uncertain_ai_score(self):
        self.assertEqual(classify_ai_score(0.50), "Uncertain")

    def test_result_contains_required_fields(self):
        result = build_analysis_result(0.99)

        self.assertIn("ai_score", result)
        self.assertIn("classification", result)
        self.assertIn("confidence", result)
        self.assertIn("disclaimer", result)

    def test_result_preserves_ai_score(self):
        result = build_analysis_result(0.99)

        self.assertEqual(result["ai_score"], 0.99)

    def test_ai_score_at_high_threshold(self):
        result = build_analysis_result(0.85)

        self.assertEqual(
            result["classification"],
            "Likely AI-generated"
        )
        self.assertEqual(result["confidence"], "High")


if __name__ == "__main__":
    unittest.main()
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Add the backend folder to Python's import path
BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from app import app


class TestMediaTruthAPI(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")

    def test_analyze_without_file(self):
        response = self.client.post("/analyze")

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_analyze_with_empty_filename(self):
        response = self.client.post(
            "/analyze",
            data={"file": (None, "")},
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    @patch("app.analyze_media")
    def test_analyze_handles_detector_error(self, mock_analyze):
        mock_analyze.side_effect = RuntimeError(
            "Sightengine request timed out."
        )

        response = self.client.post(
            "/analyze",
            data={
                "file": (
                    __import__("io").BytesIO(b"fake image content"),
                    "test.jpg"
                )
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 502)
        self.assertIn("error", response.get_json())
        mock_analyze.assert_called_once()


if __name__ == "__main__":
    unittest.main()
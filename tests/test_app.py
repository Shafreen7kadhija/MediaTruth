import sys
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

# Add the backend folder to Python's import path
BACKEND_PATH = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND_PATH))

from app import app


def make_test_png():
    """Create a small, valid PNG image for API tests."""
    image_buffer = io.BytesIO()
    Image.new("RGB", (1, 1), color="red").save(
        image_buffer,
        format="PNG"
    )
    image_buffer.seek(0)
    return image_buffer


class TestMediaTruthAPI(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "healthy")
        self.assertIn("application/json", response.content_type)

    def test_health_endpoint_rejects_post(self):
        response = self.client.post("/health")
        self.assertEqual(response.status_code, 405)

    def test_health_endpoint_returns_json(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
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

    def test_analyze_rejects_get_request(self):
        response = self.client.get("/analyze")
        self.assertEqual(response.status_code, 405)

    @patch("app.analyze_media")
    def test_analyze_handles_detector_error(self, mock_analyze):
        mock_analyze.side_effect = RuntimeError(
            "Sightengine request timed out."
        )
        response = self.client.post(
            "/analyze",
            data={"file": (make_test_png(), "test.png")},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 502)
        self.assertIn("error", response.get_json())
        mock_analyze.assert_called_once()

    def test_rejects_unsupported_file_type(self):
        response = self.client.post(
            "/analyze",
            data={
                "file": (io.BytesIO(b"some text"), "document.txt")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Unsupported file type",
            response.get_json()["error"]
        )

    @patch("app.analyze_media")
    def test_rejects_empty_file(self, mock_analyze):
        response = self.client.post(
            "/analyze",
            data={
                "file": (io.BytesIO(b""), "empty.jpg")
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("empty", response.get_json()["error"].lower())
        mock_analyze.assert_not_called()

    def test_rejects_file_over_10_mb(self):
        response = self.client.post(
            "/analyze",
            data={
                "file": (
                    io.BytesIO(b"x" * (10 * 1024 * 1024 + 1)),
                    "large.jpg"
                )
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 413)
        self.assertIn(
            "too large",
            response.get_json()["error"].lower()
        )

    @patch("app.analyze_media")
    def test_rejects_invalid_image_content(self, mock_analyze):
        response = self.client.post(
            "/analyze",
            data={
                "file": (
                    io.BytesIO(b"this is not a real image"),
                    "fake.jpg"
                )
            },
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Invalid image content",
            response.get_json()["error"]
        )
        mock_analyze.assert_not_called()


if __name__ == "__main__":
    unittest.main()

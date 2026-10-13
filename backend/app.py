from flask import Flask, request
from services.detector import analyze_media
from services.decision_engine import build_analysis_result
import os
import tempfile

app = Flask(__name__)

# Upload security settings
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}


def is_allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.get("/")
def home():
    return {"message": "MediaTruth backend is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MediaTruth backend"
    }


@app.errorhandler(413)
def file_too_large(error):
    return {"error": "File is too large. Maximum allowed size is 10 MB."}, 413


@app.post("/analyze")
def analyze():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return {"error": "No file selected"}, 400

    if not is_allowed_file(uploaded_file.filename):
        return {
            "error": "Unsupported file type. Upload JPG, JPEG, PNG, or WEBP."
        }, 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            uploaded_file.save(temp_file)
            temp_path = temp_file.name

        if os.path.getsize(temp_path) == 0:
            return {"error": "The uploaded file is empty."}, 400

        try:
            result = analyze_media(temp_path)
            ai_score = result["type"]["ai_generated"]
            return build_analysis_result(ai_score)

        except RuntimeError as exc:
            return {"error": str(exc)}, 502

        except (KeyError, TypeError, ValueError):
            return {
                "error": "Invalid response from the analysis service."
            }, 502

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    def test_rejects_unsupported_file_type(self):
        response = self.client.post(
            "/analyze",
            data={
                "file": (
                    __import__("io").BytesIO(b"some text"),
                    "document.txt"
                )
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported file type", response.get_json()["error"])

    def test_rejects_empty_file(self):
        with patch("app.analyze_media") as mock_analyze:
            response = self.client.post(
                "/analyze",
                data={
                    "file": (
                        __import__("io").BytesIO(b""),
                        "empty.jpg"
                    )
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
                    __import__("io").BytesIO(b"x" * (10 * 1024 * 1024 + 1)),
                    "large.jpg"
                )
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 413)
        self.assertIn("too large", response.get_json()["error"].lower())

if __name__ == "__main__":
    app.run(debug=True)
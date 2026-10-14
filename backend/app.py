from flask import Flask, request
from services.detector import analyze_media
from services.decision_engine import build_analysis_result
from PIL import Image, UnidentifiedImageError
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
    return {
        "error": "File is too large. Maximum allowed size is 10 MB."
    }, 413


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

        # Validate actual image content.
        try:
            with Image.open(temp_path) as image:
                if image.format not in {"JPEG", "PNG", "WEBP"}:
                    return {
                        "error": "Unsupported image format. Upload JPG, JPEG, PNG, or WEBP."
                    }, 400

                image.verify()

        except (UnidentifiedImageError, OSError, ValueError):
            return {
                "error": "Invalid image content. Please upload a valid image."
            }, 400

        # Analyze the validated image.
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
        # Remove the temporary file even if analysis fails.
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True)
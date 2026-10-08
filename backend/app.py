from flask import Flask, request
from services.detector import analyze_media
from services.decision_engine import build_analysis_result
import os
import tempfile

app = Flask(__name__)


@app.get("/")
def home():
    return {"message": "MediaTruth backend is running"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "MediaTruth backend"
    }


@app.post("/analyze")
def analyze():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":
        return {"error": "No file selected"}, 400

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            uploaded_file.save(temp_file)
            temp_path = temp_file.name

        result = analyze_media(temp_path)

        ai_score = result["type"]["ai_generated"]

        return build_analysis_result(ai_score)

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True)
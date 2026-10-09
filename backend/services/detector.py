import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_USER = os.getenv("SIGHTENGINE_API_USER")
API_SECRET = os.getenv("SIGHTENGINE_API_SECRET")

SIGHTENGINE_URL = "https://api.sightengine.com/1.0/check.json"


def analyze_media(file_path):
    if not API_USER or not API_SECRET:
        raise RuntimeError("Sightengine API credentials are not configured.")

    params = {
        "models": "genai",
        "api_user": API_USER,
        "api_secret": API_SECRET
    }

    try:
        with open(file_path, "rb") as media_file:
            files = {"media": media_file}

            response = requests.post(
                SIGHTENGINE_URL,
                files=files,
                data=params,
                timeout=30
            )

        response.raise_for_status()
        result = response.json()

    except requests.Timeout as exc:
        raise RuntimeError("Sightengine request timed out.") from exc

    except requests.RequestException as exc:
        raise RuntimeError("Could not connect to Sightengine.") from exc

    except ValueError as exc:
        raise RuntimeError("Sightengine returned an invalid response.") from exc

    if result.get("status") != "success":
        raise RuntimeError("Sightengine could not analyze this media.")

    if not isinstance(result.get("type"), dict):
        raise RuntimeError("Sightengine response is missing the AI detection result.")

    ai_score = result["type"].get("ai_generated")

    if (
        isinstance(ai_score, bool)
        or not isinstance(ai_score, (int, float))
        or not 0 <= ai_score <= 1
    ):
        raise RuntimeError("Sightengine returned an invalid AI score.")

    return result
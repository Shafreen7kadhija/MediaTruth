import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_USER = os.getenv("SIGHTENGINE_API_USER")
API_SECRET = os.getenv("SIGHTENGINE_API_SECRET")

SIGHTENGINE_URL = "https://api.sightengine.com/1.0/check.json"


def analyze_media(file_path):
    params = {
        "models": "genai",
        "api_user": API_USER,
        "api_secret": API_SECRET
    }

    with open(file_path, "rb") as media_file:
        files = {
            "media": media_file
        }

        response = requests.post(
            SIGHTENGINE_URL,
            files=files,
            data=params
        )

    return response.json()
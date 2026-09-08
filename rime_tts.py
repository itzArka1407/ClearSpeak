import os
import requests
from dotenv import load_dotenv


# Load the API key from .env
load_dotenv()

RIME_API_KEY = os.getenv("RIME_API_KEY")

RIME_URL = "https://users.rime.ai/v1/rime-tts"


def generate_speech(text):

    if not RIME_API_KEY:
        raise ValueError(
            "RIME_API_KEY not found. Check your .env file."
        )

    headers = {
        "Accept": "audio/mpeg",
        "Authorization": f"Bearer {RIME_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "modelId": "mistv2",
        "speaker": "astra",
        "lang": "eng",
        "samplingRate": 22050,
        "speedAlpha": 1.0
    }

    response = requests.post(
        RIME_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(
            f"Rime API Error {response.status_code}: {response.text}"
        )

    return response.content
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def list_available_models():
    base_url = os.getenv("LLM_API_BASE", "http://localhost:3001").rstrip("/")
    api_key = os.getenv("LLM_API_KEY", "")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print("--- List of available models from 9router ---")
    try:
        response = requests.get(f"{base_url}/v1/models", headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        for model in data.get("data", []):
            print(f"Model Name: {model.get('id')}")
            print(f"Owned By: {model.get('owned_by', 'unknown')}")
            print("-" * 30)
    except Exception as e:
        print(f"Error calling 9router API: {e}")


if __name__ == "__main__":
    list_available_models()

import os

import requests
from dotenv import load_dotenv

load_dotenv()


def list_my_models():
    base_url = os.getenv("LLM_API_BASE", "http://localhost:3001").rstrip("/")
    api_key = os.getenv("LLM_API_KEY", "")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print("--- CAC MODEL 9ROUTER DANG CO ---")
    try:
        response = requests.get(f"{base_url}/v1/models", headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        models = data.get("data", [])

        if not models:
            print("[?] Khong tim thay model nao.")
            return

        for model in models:
            print(f"> {model.get('id', 'unknown')}")
    except Exception as e:
        print(f"[!] Loi khi goi 9router: {e}")


if __name__ == "__main__":
    list_my_models()

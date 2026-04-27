import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY not found in .env")
        return

    client = genai.Client(api_key=api_key)
    
    print("--- List of available models for your API Key ---")
    try:
        # Liệt kê các model
        for model in client.models.list():
            print(f"Model Name: {model.name}")
            print(f"Supported Actions: {model.supported_actions}")
            print("-" * 30)
    except Exception as e:
        print(f"Error calling Google API: {e}")

if __name__ == "__main__":
    list_available_models()

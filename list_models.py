import google.generativeai as genai
import os
from dotenv import load_dotenv

# load môi trường để lấy api key
load_dotenv()
api_key = os.getenv("LLM_API_KEY")

def list_my_models():
    if not api_key:
        print("[!] Lỗi: Không tìm thấy LLM_API_KEY trong file .env")
        return

    genai.configure(api_key=api_key)
    print("--- CÁC MODEL GEMINI BẠN CÓ QUYỀN TRUY CẬP ---")
    try:
        found = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"> {m.name}")
                found = True
        
        if not found:
            print("[?] Không tìm thấy model nào hỗ trợ generateContent.")
            
    except Exception as e:
        print(f"[!] Lỗi khi gọi API: {str(e)}")

if __name__ == "__main__":
    list_my_models()

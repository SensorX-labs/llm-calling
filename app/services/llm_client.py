from google import genai
from google.genai import types
from typing import Optional

from app.core.config import settings

class LLMClient:
    def __init__(self):
        # Khởi tạo client với API Key
        self.client = genai.Client(api_key=settings.LLM_API_KEY)
        self.default_model_name = settings.LLM_MODEL

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        model_name = model or self.default_model_name
        temp = temperature if temperature is not None else settings.TEMPERATURE

        try:
            # Gemma models often don't support response_mime_type="application/json"
            mime_type = "application/json" if "gemma" not in model_name.lower() else None
            
            response = await self.client.aio.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temp,
                    response_mime_type=mime_type,
                    max_output_tokens=max_tokens or settings.MAX_TOKENS
                )
            )

            if not response.text:
                return {"status": "error", "message": "Gemini không trả về nội dung"}

            return {
                "status": "success",
                "content": response.text,
                "model": model_name
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": model_name
            }

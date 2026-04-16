import google.generativeai as genai
from typing import Optional

from app.core.config import settings


class LLMClient:
    """Client for communicating with LLM APIs (Gemini)."""

    def __init__(self):
        """Initialize Gemini client."""
        genai.configure(api_key=settings.LLM_API_KEY)
        self.default_model_name = settings.LLM_MODEL

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        """
        Call Gemini API with given prompt.
        """
        model_name = model or self.default_model_name
        temp = temperature if temperature is not None else settings.TEMPERATURE

        try:
            # Sử dụng các tham số trực tiếp và bật JSON mode
            model_instance = genai.GenerativeModel(model_name)
            
            response = await model_instance.generate_content_async(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temp,
                    response_mime_type="application/json",
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

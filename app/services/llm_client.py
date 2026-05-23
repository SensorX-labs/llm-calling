from typing import Optional

import httpx

from app.core.config import settings


class LLMClient:
    def __init__(self):
        self.default_model_name = settings.LLM_MODEL
        self.base_url = settings.LLM_API_BASE.rstrip("/")
        self.timeout = settings.LLM_TIMEOUT

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        model_name = model or self.default_model_name
        temp = temperature if temperature is not None else settings.TEMPERATURE
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": temp,
            "max_tokens": max_tokens or settings.MAX_TOKENS,
            "stream": False,
        }

        headers = {"Content-Type": "application/json"}
        if settings.LLM_API_KEY:
            headers["Authorization"] = f"Bearer {settings.LLM_API_KEY}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json=payload,
                    headers=headers,
                )
                if response.is_error:
                    message = self._extract_error_message(response)
                    return {
                        "status": "error",
                        "message": message,
                        "model": model_name,
                    }

            data = response.json()
            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content:
                return {"status": "error", "message": "9router khong tra ve noi dung", "model": model_name}

            return {
                "status": "success",
                "content": content,
                "model": model_name,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "model": model_name,
            }

    @staticmethod
    def _extract_error_message(response: httpx.Response) -> str:
        try:
            data = response.json()
            error = data.get("error")
            if isinstance(error, dict):
                detail = error.get("message") or error.get("code") or str(error)
                return f"{response.status_code} {response.reason_phrase}: {detail}"
            if error:
                return f"{response.status_code} {response.reason_phrase}: {error}"
        except Exception:
            pass

        body = response.text.strip()
        if body:
            return f"{response.status_code} {response.reason_phrase}: {body}"
        return f"{response.status_code} {response.reason_phrase}"

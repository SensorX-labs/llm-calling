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
        endpoint = f"{self.base_url}/v1/chat/completions"
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
                    endpoint,
                    json=payload,
                    headers=headers,
                )
                if response.is_error:
                    message = self._extract_error_message(response)
                    return {
                        "status": "error",
                        "message": f"9router HTTP error at {endpoint} with model {model_name}: {message}",
                        "model": model_name,
                    }

            try:
                data = response.json()
            except ValueError:
                body_preview = self._preview_text(response.text)
                return {
                    "status": "error",
                    "message": (
                        f"9router returned non-JSON response from {endpoint} "
                        f"with model {model_name}: {body_preview}"
                    ),
                    "model": model_name,
                }

            content = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content:
                return {
                    "status": "error",
                    "message": (
                        f"9router returned empty content from {endpoint} "
                        f"with model {model_name}"
                    ),
                    "model": model_name,
                }

            return {
                "status": "success",
                "content": content,
                "model": model_name,
            }
        except httpx.TimeoutException as e:
            return {
                "status": "error",
                "message": (
                    f"Timeout when calling 9router at {endpoint} with model {model_name} "
                    f"(timeout={self.timeout}s): {self._format_exception_message(e)}"
                ),
                "model": model_name,
            }
        except httpx.ConnectError as e:
            return {
                "status": "error",
                "message": (
                    f"Cannot connect to 9router at {endpoint} with model {model_name}: "
                    f"{self._format_exception_message(e)}"
                ),
                "model": model_name,
            }
        except httpx.HTTPError as e:
            return {
                "status": "error",
                "message": (
                    f"HTTP client error when calling 9router at {endpoint} with model {model_name}: "
                    f"{self._format_exception_message(e)}"
                ),
                "model": model_name,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": (
                    f"Unexpected error when calling 9router at {endpoint} with model {model_name}: "
                    f"{self._format_exception_message(e)}"
                ),
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

    @staticmethod
    def _format_exception_message(error: Exception) -> str:
        message = str(error).strip()
        if message:
            return message
        return error.__class__.__name__

    @staticmethod
    def _preview_text(text: str, limit: int = 300) -> str:
        flattened = " ".join(text.split())
        if not flattened:
            return "<empty body>"
        if len(flattened) <= limit:
            return flattened
        return flattened[:limit] + "...(truncated)"

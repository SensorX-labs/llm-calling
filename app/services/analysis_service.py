import json
from json import JSONDecodeError

from app.repositories.analysis_repository import AnalysisRepository
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder


class AnalysisService:
    REQUIRED_KEYS = ("deal_status", "reasoning", "strategy")

    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.repository = AnalysisRepository()

    async def process_quotation(self, data: dict):
        quote_id = data.get("quoteId")
        print(f"[*] Start analysis for quote id: {quote_id}")

        try:
            prompt = self.prompt_builder.build_quotation_prompt(data)
            print("[*] Prompt prepared")

            result = await self.llm_client.complete(prompt=prompt, temperature=0.2)
            if result.get("status") == "error":
                print(f"[!] 9router request failed: {result.get('message')}")
                return result
            print("[*] Received response from 9router")

            content = result.get("content", "{}")
            analysis = await self._parse_analysis_content(content, quote_id)
            print("[*] Parsed analysis JSON successfully")

            self.repository.upsert_analysis(quote_id, analysis)
            print(f"[ok] Saved analysis to postgres for quote id: {quote_id}")

            return {"status": "success", "quote_id": quote_id, "analysis": analysis}
        except Exception as e:
            print(f"[x] Fatal analysis error: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_existing_analysis(self, quote_id: str):
        return self.repository.find_by_id(quote_id)

    async def _parse_analysis_content(self, content: str, quote_id: str) -> dict:
        cleaned_content = self._strip_markdown_fence(content)

        try:
            analysis = self._loads_analysis(cleaned_content)
            return self._validate_analysis(analysis)
        except (JSONDecodeError, ValueError) as parse_error:
            print(
                f"[!] Invalid JSON from 9router for quote {quote_id}: {parse_error}. "
                f"Raw content: {self._preview_text(cleaned_content)}"
            )

        repaired_content = await self._repair_invalid_json(cleaned_content, quote_id)
        analysis = self._loads_analysis(repaired_content)
        return self._validate_analysis(analysis)

    def _loads_analysis(self, content: str) -> dict:
        try:
            return json.loads(content)
        except JSONDecodeError:
            extracted_json = self._extract_first_json_object(content)
            return json.loads(extracted_json)

    async def _repair_invalid_json(self, broken_content: str, quote_id: str) -> str:
        repair_prompt = f"""
You are fixing malformed JSON produced by another model.

Requirements:
- Return exactly one valid JSON object.
- Do not include markdown fences.
- Do not include explanations.
- The JSON must contain exactly these keys:
  "deal_status", "reasoning", "strategy"
- Keep the original meaning if possible.
- If any field is missing, fill it with a short fallback string.

Malformed JSON:
{broken_content}
""".strip()

        repair_result = await self.llm_client.complete(prompt=repair_prompt, temperature=0)
        if repair_result.get("status") == "error":
            raise ValueError(
                f"Unable to repair malformed JSON for quote {quote_id}: {repair_result.get('message')}"
            )

        repaired_content = self._strip_markdown_fence(repair_result.get("content", ""))
        print(f"[*] Received repaired JSON for quote {quote_id}: {self._preview_text(repaired_content)}")
        return repaired_content

    def _validate_analysis(self, analysis: dict) -> dict:
        if not isinstance(analysis, dict):
            raise ValueError("Analysis payload is not a JSON object")

        normalized = {
            "deal_status": str(analysis.get("deal_status", "")).strip(),
            "reasoning": str(analysis.get("reasoning", "")).strip(),
            "strategy": str(analysis.get("strategy", "")).strip(),
        }

        missing_keys = [key for key in self.REQUIRED_KEYS if not normalized[key]]
        if missing_keys:
            raise ValueError(f"Analysis JSON is missing fields: {', '.join(missing_keys)}")

        return normalized

    @staticmethod
    def _strip_markdown_fence(content: str) -> str:
        if not isinstance(content, str):
            return ""

        cleaned = content.strip()
        if "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) >= 3:
                cleaned = parts[1]
            else:
                cleaned = cleaned.replace("```", "")

        cleaned = cleaned.strip()
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

        return cleaned

    @staticmethod
    def _extract_first_json_object(content: str) -> str:
        start = content.find("{")
        if start == -1:
            raise JSONDecodeError("No JSON object found", content, 0)

        depth = 0
        in_string = False
        escape = False

        for index in range(start, len(content)):
            char = content[index]

            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return content[start:index + 1]

        raise JSONDecodeError("JSON object is not closed", content, start)

    @staticmethod
    def _preview_text(content: str, limit: int = 400) -> str:
        flattened = " ".join(content.split())
        if len(flattened) <= limit:
            return flattened
        return flattened[:limit] + "...(truncated)"

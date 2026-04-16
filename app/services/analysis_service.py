import json
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.repositories.analysis_repository import AnalysisRepository

class AnalysisService:
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.repository = AnalysisRepository()

    async def process_quotation(self, data: dict):
        """
        Giao tiếp với LLM và lưu kết quả thông qua Repository.
        """
        quote_id = data.get("quoteId")
        if not quote_id:
            return {"status": "error", "message": "Missing quoteId"}

        # build promt cho ai
        prompt = self.prompt_builder.build_quotation_prompt(data)

        # gọi api
        result = await self.llm_client.complete(prompt=prompt, temperature=0.2)
        if result.get("status") == "error":
            return result

        # parse json
        content = result.get("content", "{}")
        try:
            analysis = json.loads(content)
            # lưu vào db
            self.repository.upsert_analysis(quote_id, analysis)
            return {"status": "success", "quote_id": quote_id, "analysis": analysis}
        except Exception as e:
            return {"status": "error", "message": f"JSON Parse Error: {str(e)}", "raw": content}

    def get_existing_analysis(self, quote_id: str):
        """
        Lấy kết quả phân tích đã có từ Repository.
        """
        return self.repository.find_by_id(quote_id)

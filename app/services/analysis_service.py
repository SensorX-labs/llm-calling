import json
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.repositories.analysis_repository import AnalysisRepository

# service phân tích báo giá
class AnalysisService:

    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.repository = AnalysisRepository()

    # xử lý phân tích báo giá
    async def process_quotation(self, data: dict):
        quote_id = data.get("quoteId")
        try:
            #  xây dựng promt theo mẫu
            prompt = self.prompt_builder.build_quotation_prompt(data)

            # gọi gemini lấy kết quả
            result = await self.llm_client.complete(prompt=prompt, temperature=0.2)
            if result.get("status") == "error":
                return result

            # parse json từ nội dung ai trả về
            content = result.get("content", "{}")
            analysis = json.loads(content)
            
            # lưu kết quả vào postgres
            self.repository.upsert_analysis(quote_id, analysis)
            return {"status": "success", "quote_id": quote_id, "analysis": analysis}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # lấy kết quả phân tích theo quote id
    def get_existing_analysis(self, quote_id: str):
        return self.repository.find_by_id(quote_id)

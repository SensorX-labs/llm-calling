import json
from app.services.llm_client import LLMClient
from app.services.prompt_builder import PromptBuilder
from app.repositories.analysis_repository import AnalysisRepository

class AnalysisService:
    # dịch vụ điều phối phân tích báo giá

    def __init__(self):
        # khởi tạo client ai, prompt bộ xây dựng và kho dữ liệu
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.repository = AnalysisRepository()

    async def process_quotation(self, data: dict):
        # quy trình xử lý chính: build prompt -> gọi ai -> parse json -> lưu db
        quote_id = data.get("quoteId")
        print(f"[*] bắt đầu phân tích: {quote_id}")

        try:
            # xây dựng prompt chuyên sâu
            prompt = self.prompt_builder.build_quotation_prompt(data)

            # gọi gemini lấy kết quả
            result = await self.llm_client.complete(prompt=prompt, temperature=0.2)
            if result.get("status") == "error":
                print(f"[!] lỗi gọi gemini: {result.get('message')}")
                return result

            # parse json từ nội dung ai trả về
            content = result.get("content", "{}")
            analysis = json.loads(content)
            
            # lưu kết quả vào postgres
            self.repository.upsert_analysis(quote_id, analysis)
            print(f"[ok] đã lưu db cho id: {quote_id}")
            
            return {"status": "success", "quote_id": quote_id, "analysis": analysis}
            
        except Exception as e:
            print(f"[x] lỗi phân tích id {quote_id}: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_existing_analysis(self, quote_id: str):
        # tìm kết quả cũ trong database
        return self.repository.find_by_id(quote_id)

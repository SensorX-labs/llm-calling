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
        print(f"[*] bắt đầu phân tích cho id: {quote_id}")

        try:
            # 1. xây dựng prompt
            prompt = self.prompt_builder.build_quotation_prompt(data)
            print("[*] đã dựng xong prompt cho ai")

            # 2. gọi gemini
            result = await self.llm_client.complete(prompt=prompt, temperature=0.2)
            if result.get("status") == "error":
                print(f"[!] lỗi kết nối gemini: {result.get('message')}")
                return result
            print("[*] đã nhận phản hồi từ gemini")

            # 3. parse nội dung json
            content = result.get("content", "{}")
            
            # Làm sạch chuỗi nếu AI trả về kèm markdown backticks
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            
            analysis = json.loads(content)
            print("[*] giải mã json thành công")
            
            # 4. lưu vào database
            self.repository.upsert_analysis(quote_id, analysis)
            print(f"[ok] đã lưu vào postgres thành công cho id: {quote_id}")

            return {"status": "success", "quote_id": quote_id, "analysis": analysis}
        except Exception as e:
            print(f"[x] lỗi nghiêm trọng: {str(e)}")
            return {"status": "error", "message": str(e)}

    # lấy kết quả phân tích theo quote id
    def get_existing_analysis(self, quote_id: str):
        return self.repository.find_by_id(quote_id)

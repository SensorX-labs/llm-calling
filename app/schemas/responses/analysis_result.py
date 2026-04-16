from pydantic import BaseModel

class AnalysisContent(BaseModel):
    # mốc trạng thái: An toàn | Rủi ro | Lỗ | Tiềm năng Upsell
    deal_status: str 
    # lập luận tại sao chọn trạng thái này
    reasoning: str
    # chiến lược đàm phán và cơ hội upsell
    strategy: str

class AnalysisResponse(BaseModel):
    status: str
    analysis: AnalysisContent

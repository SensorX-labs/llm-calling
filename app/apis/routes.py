from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.core.config import settings
from app.schemas.requests.quotation_analysis_request import QuotationAnalysisRequest
from app.services.analysis_service import AnalysisService

router = APIRouter()

# khởi tạo service phân tích
analysis_service = AnalysisService()

@router.get("/analysis/{quote_id}")
async def get_quote_analysis(quote_id: str):
    # lấy kết quả từ db
    analysis = analysis_service.get_existing_analysis(quote_id)
    if not analysis:
        return {
            "status": "pending",
            "message": "đang xử lý hoặc chưa có dữ liệu"
        }
    return {"status": "success", "analysis": analysis}

@router.post("/analyze-quote")
async def analyze_quote(request: QuotationAnalysisRequest, background_tasks: BackgroundTasks):
    # đẩy việc phân tích vào hàng đợi chạy ngầm
    background_tasks.add_task(analysis_service.process_quotation, request.model_dump())
    
    return {
        "status": "processing",
        "quote_id": request.quoteId,
        "message": "đã nhận và đang xử lý"
    }

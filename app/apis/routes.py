from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.core.config import settings
from app.schemas.responses.health_response import HealthResponse
from app.schemas.requests.quotation_analysis_request import QuotationAnalysisRequest
from app.services.analysis_service import AnalysisService

router = APIRouter()

# khởi tạo service 
analysis_service = AnalysisService()

@router.get("/analysis/{quote_id}")
async def get_quote_analysis(quote_id: str):
    # lấy kết quả từ db
    analysis = analysis_service.get_existing_analysis(quote_id)
    if not analysis:
        return {
            "status": "pending",
            "message": "đang xử lý hoặc id không tồn tại"
        }
    return {"status": "success", "analysis": analysis}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    # kiểm tra server
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
    }

@router.post("/analyze-quote")
async def analyze_quote(request: QuotationAnalysisRequest, background_tasks: BackgroundTasks):
    # nhận data, xử lý ngầm
    background_tasks.add_task(analysis_service.process_quotation, request.model_dump())
    
    return {
        "status": "processing",
        "quote_id": request.quoteId,
        "message": "đã nhận, đang xử lý ngầm"
    }

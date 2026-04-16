from fastapi import APIRouter, HTTPException, BackgroundTasks

from app.core.config import settings
from app.schemas.response import HealthResponse
from app.schemas.quotation import QuotationAnalysisRequest
from app.services.analysis_service import AnalysisService

router = APIRouter()

# Khởi tạo Service (Lớp này sẽ tự gọi sang Repository bên dưới)
analysis_service = AnalysisService()

@router.get("/analysis/{quote_id}")
async def get_quote_analysis(quote_id: str):
    """
    Next.js gọi API này để lấy kết quả từ DB.
    """
    analysis = analysis_service.get_existing_analysis(quote_id)
    if not analysis:
        return {
            "status": "pending",
            "message": "AI đang phân tích hoặc chưa có dữ liệu cho Quote ID này."
        }
    return {"status": "success", "analysis": analysis}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
    }

@router.post("/analyze-quote")
async def analyze_quote(request: QuotationAnalysisRequest, background_tasks: BackgroundTasks):
    """
    Hệ thống C# gọi API này để đẩy dữ liệu báo giá sang.
    """
    # Giao việc cho AI làm ngầm
    background_tasks.add_task(analysis_service.process_quotation, request.model_dump())
    
    return {
        "status": "processing",
        "quote_id": request.quoteId,
        "message": "Yêu cầu đã được tiếp nhận và đang xử lý ngầm."
    }

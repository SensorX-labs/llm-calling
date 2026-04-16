from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class CustomerData(BaseModel):
    # hồ sơ khách hàng
    isExisting: bool      # khách cũ?
    totalOrders: int      # tổng đơn
    lastOrderDaysAgo: int # ngày đơn cuối
    avgOrderValue: float  # giá trị trung bình
    paymentBehavior: str  # thanh toán: on_time | late | bad
    relationshipLevel: str # thân thiết: low | medium | high

class PriceTier(BaseModel):
    # giá theo lô
    quantity: int # mốc số lượng
    price: float # giá tương ứng

class PricingData(BaseModel):
    # thông tin giá báo
    totalAmount: float
    suggestedPrice: float       # giá đề xuất
    floorPrice: float           # giá sàn
    priceTiers: Optional[List[PriceTier]] = [] # bảng giá lô
    discountPercent: float
    avgMargin: float            # biên lợi nhuận
    priceCompetitiveness: str

class QuoteStructure(BaseModel):
    # cấu trúc báo giá
    itemCount: int
    totalItemCount: Optional[int] = 0 # tổng số lượng sp
    hasAlternativeOptions: bool
    hasBundle: bool
    complexity: str

class ContextData(BaseModel):
    # ngữ cảnh chốt đơn
    urgency: str # độ gấp
    competition: bool # có đối thủ?
    customerRequestedQuote: bool
    deadlineDays: int

class SalesData(BaseModel):
    # năng lực sales
    experienceYears: int
    winRate: float
    recentPerformance: str

class QuotationAnalysisRequest(BaseModel):
    # yêu cầu phân tích tổng thể
    quoteId: str = Field(..., description="id duy nhất báo giá")
    customer: CustomerData
    pricing: PricingData
    quote: QuoteStructure
    context: ContextData
    sales: SalesData
    signals: Optional[Dict[str, Any]] = None
    customerMessage: Optional[str] = None

from typing import Dict, Optional, Any
from pydantic import BaseModel, Field

class CustomerData(BaseModel):
    isExisting: bool
    totalOrders: int
    lastOrderDaysAgo: int
    avgOrderValue: float
    paymentBehavior: str  # on_time | late | bad
    relationshipLevel: str  # low | medium | high

class PriceTier(BaseModel):
    quantity: int
    price: float

class PricingData(BaseModel):
    totalAmount: float
    suggestedPrice: float
    floorPrice: float
    priceTiers: Optional[list[PriceTier]] = []  # Danh sách các mức giá theo số lượng
    discountPercent: float
    avgMargin: float
    priceCompetitiveness: str

class QuoteStructure(BaseModel):
    itemCount: int
    hasAlternativeOptions: bool
    hasBundle: bool
    complexity: str  # low | medium | high

class ContextData(BaseModel):
    urgency: str  # low | medium | high
    competition: bool
    customerRequestedQuote: bool
    deadlineDays: int

class SalesData(BaseModel):
    experienceYears: int
    winRate: float
    recentPerformance: str  # up | stable | down

class QuotationAnalysisRequest(BaseModel):
    quoteId: str = Field(..., description="ID định danh báo giá từ hệ thống C#")
    customer: CustomerData
    pricing: PricingData
    quote: QuoteStructure
    context: ContextData
    sales: SalesData
    signals: Optional[Dict[str, Any]] = None
    customerMessage: Optional[str] = None

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.schemas.requests.customer_data import CustomerData
from app.schemas.requests.pricing_data import PricingData
from app.schemas.requests.quote_structure import QuoteStructure
from app.schemas.requests.context_data import ContextData
from app.schemas.requests.sales_data import SalesData

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

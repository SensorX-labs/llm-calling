from pydantic import BaseModel
from typing import List, Optional
from app.schemas.requests.price_tier import PriceTier

class PricingData(BaseModel):
    # thông tin giá báo
    totalAmount: float
    suggestedPrice: float
    floorPrice: float
    priceTiers: Optional[List[PriceTier]] = []
    discountPercent: float
    avgMargin: float
    priceCompetitiveness: str

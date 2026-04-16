from pydantic import BaseModel
from typing import Optional

class QuoteStructure(BaseModel):
    # cấu trúc báo giá
    itemCount: int
    totalItemCount: Optional[int] = 0
    hasAlternativeOptions: bool
    hasBundle: bool
    complexity: str

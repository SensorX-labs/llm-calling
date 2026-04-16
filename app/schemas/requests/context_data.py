from pydantic import BaseModel

class ContextData(BaseModel):
    # ngữ cảnh chốt đơn
    urgency: str
    competition: bool
    customerRequestedQuote: bool
    deadlineDays: int

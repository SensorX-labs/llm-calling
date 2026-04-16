from pydantic import BaseModel

class CustomerData(BaseModel):
    # hồ sơ khách hàng
    isExisting: bool
    totalOrders: int
    lastOrderDaysAgo: int
    avgOrderValue: float
    paymentBehavior: str
    relationshipLevel: str

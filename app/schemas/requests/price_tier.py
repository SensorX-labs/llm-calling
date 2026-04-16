from pydantic import BaseModel

class PriceTier(BaseModel):
    # giá theo lô
    quantity: int
    price: float

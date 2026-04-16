from pydantic import BaseModel

class HealthResponse(BaseModel):
    # trạng thái hệ thống
    status: str
    version: str

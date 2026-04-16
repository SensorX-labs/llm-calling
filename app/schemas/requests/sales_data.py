from pydantic import BaseModel

class SalesData(BaseModel):
    # năng lực sales
    experienceYears: int
    winRate: float
    recentPerformance: str

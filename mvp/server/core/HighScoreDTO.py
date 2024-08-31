from datetime import datetime

from pydantic import BaseModel


class HighScoreDTO(BaseModel):
    nickname: str
    score: int
    level_reached: int
    cash_balance: float
    timestamp: datetime

    class Config:
        from_attributes = True

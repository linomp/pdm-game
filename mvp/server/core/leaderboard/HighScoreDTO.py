from datetime import datetime

from pydantic import BaseModel


class HighScoreDTO(BaseModel):
    nickname: str
    score: float
    timestamp: datetime

    class Config:
        from_attributes = True

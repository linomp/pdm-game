import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime

from mvp.server.persistence.database import Base


class HighScoreModel(Base):
    __tablename__ = "highscores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    level_reached = Column(Integer, nullable=False)
    cash_balance = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<HighScore(id={self.id}, nickname={self.nickname}, score={self.score}, timestamp={self.timestamp})>"

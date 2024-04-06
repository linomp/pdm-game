from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mvp.server.core.leaderboard.HighScoreDTO import HighScoreDTO
from mvp.server.core.leaderboard.HighScoreModel import HighScoreModel
from mvp.server.persistence.database import get_db

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[HighScoreDTO])
async def get_leaderboard(db: Session = Depends(get_db)):
    result = db.query(HighScoreModel).all()

    return result


@router.post("/test")
async def test_leaderboard_post(db: Session = Depends(get_db)):
    dummy_entries = [
        HighScoreModel(nickname="Player1", score=1000.5, timestamp=datetime(2024, 4, 6, 10, 0, 0)),
        HighScoreModel(nickname="Player2", score=750.3, timestamp=datetime(2024, 4, 6, 11, 30, 0)),
        HighScoreModel(nickname="Player3", score=1200.8, timestamp=datetime(2024, 4, 6, 14, 45, 0)),
        HighScoreModel(nickname="Player4", score=850.9, timestamp=datetime(2024, 4, 6, 16, 20, 0)),
        HighScoreModel(nickname="Player5", score=1100.2, timestamp=datetime(2024, 4, 6, 18, 0, 0))
    ]

    db.add_all(dummy_entries)
    db.commit()


@router.delete("/test")
async def test_leaderboard_delete(db: Session = Depends(get_db)):
    db.query(HighScoreModel).delete()
    db.commit()

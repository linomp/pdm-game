from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.leaderboard.HighScoreDTO import HighScoreDTO
from mvp.server.core.leaderboard.HighScoreModel import HighScoreModel
from mvp.server.core.leaderboard.ScoreCreateRequest import ScoreCreateRequest
from mvp.server.persistence.database import get_db
from mvp.server.routers.sessions import get_session_dependency

router = APIRouter(
    prefix="/leaderboard",
    tags=["Leaderboard"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[HighScoreDTO])
async def get_leaderboard(db: Session = Depends(get_db)):
    result = db.query(HighScoreModel).order_by(desc(HighScoreModel.score)).limit(10).all()

    return result


@router.post("/score")
async def post_score(request: ScoreCreateRequest, session: GameSession = Depends(get_session_dependency),
                     db: Session = Depends(get_db)):
    if session.is_game_over is False:
        raise HTTPException(status_code=400, detail="Game is not over yet")
    db.add(HighScoreModel(nickname=request.nickname, score=session.get_score(), timestamp=datetime.now()))
    db.commit()

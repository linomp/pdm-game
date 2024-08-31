from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from mvp.server.core.GameSession import GameSession
from mvp.server.core.HighScoreDTO import HighScoreDTO
from mvp.server.core.ScoreCreateRequest import ScoreCreateRequest
from mvp.server.persistence.database import get_db
from mvp.server.persistence.models.HighScoreModel import HighScoreModel
from mvp.server.routers.sessions import get_session_dependency, cleanup_session

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

    # TODO 74: clean up this hack made just for load test...
    score = session.get_score()
    if request.nickname == "LOCUST":
        score = 0

    db.add(
        HighScoreModel(
            nickname=request.nickname,
            score=score,
            level_reached=session.current_step,
            cash_balance=session.available_funds,
            timestamp=datetime.now()
        )
    )
    db.commit()

    cleanup_session(session.id)

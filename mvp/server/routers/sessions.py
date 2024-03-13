import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utilities import repeat_every

from mvp.server.core.game.GameMetrics import GameMetrics
from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.game.GameSessionDTO import GameSessionDTO

sessions: dict[str, GameSession] = {}
game_metrics = GameMetrics()

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    responses={404: {"description": "Not found"}},
)


def get_session_dependency(session_id: str) -> GameSession:
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@router.on_event("startup")
@repeat_every(seconds=3600, wait_first=False)
async def cleanup_inactive_sessions():
    print(f"{datetime.now()}: Cleaning up sessions...")

    for session_id, session in list(sessions.items()):
        must_be_dropped = False

        if session.is_game_over:
            must_be_dropped = True
        if session.is_abandoned():
            must_be_dropped = True
            game_metrics.update_on_game_abandoned()

        if must_be_dropped:
            print(f"{datetime.now()}: Session '{session_id}' will be dropped")
            sessions.pop(session_id)


@router.on_event("shutdown")
async def cleanup_all_sessions():
    sessions.clear()


@router.post("/", response_model=GameSessionDTO)
async def create_session() -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        session = GameSession.new_game_session(_id=new_session_id)
        sessions[new_session_id] = session

    game_metrics.update_on_game_started()

    return GameSessionDTO.from_session(sessions[new_session_id])


@router.get("/metrics", response_model=GameMetrics)
async def get_metrics() -> GameMetrics:
    return game_metrics


@router.get("/", response_model=GameSessionDTO)
async def get_session(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    return GameSessionDTO.from_session(session)


@router.put("/turns", response_model=GameSessionDTO)
async def advance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    await session.advance_one_turn()

    if session.check_if_game_over():
        game_metrics.update_on_game_ended(session.get_total_duration())

    return GameSessionDTO.from_session(session)

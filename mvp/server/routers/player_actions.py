from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from mvp.server.core.game.GameSession import GameSessionDTO, GameSession
from mvp.server.routers.sessions import get_session_dependency

router = APIRouter(
    prefix="/player-actions",
    tags=["Player actions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/maintenance-interventions", response_model=GameSessionDTO)
async def do_maintenance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO | JSONResponse:
    success = session.do_maintenance()

    if not success:
        return JSONResponse(status_code=400, content={"message": "Not enough funds to do maintenance"})

    return GameSessionDTO.from_session(session)

import uuid

from fastapi import APIRouter, Depends, HTTPException

from mvp.server.core.game.GameSession import GameSessionDTO, GameSession

sessions: dict[str, GameSession] = {}


def get_session_dependency(session_id: str) -> GameSession:
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=GameSessionDTO)
async def create_session() -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        session = GameSession.new_game_session(_id=new_session_id)
        sessions[new_session_id] = session

    return GameSessionDTO.from_session(sessions[new_session_id])


@router.get("/", response_model=GameSessionDTO)
async def get_session(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    return GameSessionDTO.from_session(session)


@router.put("/turns", response_model=GameSessionDTO)
async def advance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    # TODO: do something with the returned list of MachineState. May be useful for prediction functionality.
    await session.advance_one_turn()

    return GameSessionDTO.from_session(session)

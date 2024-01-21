import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from mvp.server.data_models.GameSession import GameSession, GameSessionDTO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, GameSession] = {}


@app.on_event("shutdown")
async def cleanup_sessions():
    sessions.clear()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/session", response_model=GameSessionDTO, tags=["Sessions"])
async def create_session() -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        session = GameSession.new_game_session(_id=new_session_id)
        sessions[new_session_id] = session

    return GameSessionDTO.from_session(sessions[new_session_id])


@app.get("/session", response_model=GameSessionDTO, tags=["Sessions"])
async def get_session(session_id: str) -> GameSessionDTO | JSONResponse:
    if session_id not in sessions:
        return JSONResponse(status_code=404, content={"message": "Session not found"})

    session = sessions[session_id]

    return GameSessionDTO.from_session(session)


@app.put("/session/turns", response_model=GameSessionDTO, tags=["Sessions"])
async def advance(session_id: str) -> GameSessionDTO | JSONResponse:
    if session_id not in sessions:
        return JSONResponse(status_code=404, content={"message": "Session not found"})

    session = sessions[session_id]

    # TODO: do something with the returned list of MachineState. May be useful for prediction functionality.
    await session.advance_one_turn()

    return GameSessionDTO.from_session(session)

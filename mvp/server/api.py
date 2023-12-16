import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from mvp.server.constants import DEFAULT_SESSION_ID
from mvp.server.data_models import GameSession, GameSessionDTO

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, GameSession] = {DEFAULT_SESSION_ID: GameSession(id=DEFAULT_SESSION_ID)}


@app.on_event("shutdown")
async def cleanup_sessions():
    for session in sessions.values():
        session.stop_incrementing()

    sessions.clear()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/session", response_model=GameSessionDTO, tags=["Sessions"])
async def start_session() -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        session = GameSession(id=new_session_id)
        sessions[new_session_id] = session

    return GameSessionDTO.from_session(sessions[new_session_id])


@app.get("/session", response_model=GameSessionDTO, tags=["Sessions"])
async def get_session(session_id: str) -> GameSessionDTO | JSONResponse:
    if session_id not in sessions:
        return JSONResponse(status_code=404, content={"message": "Session not found"})

    session = sessions[session_id]

    return GameSessionDTO.from_session(session)

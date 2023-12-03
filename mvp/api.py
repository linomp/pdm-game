import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse

from mvp.constants import MACHINE_STATS_ENDPOINT
from mvp.data_models import MachineStats, GameSession

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

default_session_id = "test"
sessions: dict[str, GameSession] = {default_session_id: GameSession(id=default_session_id)}


@app.on_event("shutdown")
async def cleanup_sessions():
    for session in sessions.values():
        session.stop_incrementing()

    sessions.clear()


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/session", response_model=GameSession, tags=["Sessions"])
async def start_session() -> GameSession:
    new_session_id = uuid.uuid4().hex
    if new_session_id not in sessions:
        session = GameSession(id=new_session_id)
        sessions[new_session_id] = session
    return sessions[new_session_id]


@app.get(MACHINE_STATS_ENDPOINT, tags=["Machine stats"], response_model=MachineStats)
async def get_machine_stats(session_id: str = default_session_id) -> JSONResponse | MachineStats:
    if session_id not in sessions:
        return JSONResponse(status_code=404, content={"message": "Session not found"})

    session: GameSession = sessions[session_id]

    return session.machine_stats

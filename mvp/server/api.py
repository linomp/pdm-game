import os
from contextlib import asynccontextmanager

import logfire
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from mvp.server.core.GameParametersDTO import GameParametersDTO
from mvp.server.persistence.database import init_db
from mvp.server.routers.leaderboard import router as leaderboard_router
from mvp.server.routers.player_actions import router as player_actions_router
from mvp.server.routers.sessions import router as sessions_router, cleanup_inactive_sessions, \
    publish_mqtt_client_heartbeat


@asynccontextmanager
async def lifespan(app: FastAPI):
    await cleanup_inactive_sessions()
    await publish_mqtt_client_heartbeat()
    yield


app = FastAPI(lifespan=lifespan)

logfire_token = os.getenv("LOGFIRE_TOKEN", None)
if logfire_token is not None:
    logfire.configure(token=logfire_token)
    logfire.instrument_fastapi(app)
    logfire.instrument_sqlalchemy()  # TODO: why it doesn't log the SQL query when a highscore is added?

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(player_actions_router)
app.include_router(leaderboard_router)

init_db()


@app.exception_handler(HTTPException)
async def http_exception_handler(_, e):
    return JSONResponse(status_code=e.status_code, content={"message": e.detail})


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/game-parameters", tags=["Game Parameters"])
async def get_parameters() -> GameParametersDTO:
    return GameParametersDTO()

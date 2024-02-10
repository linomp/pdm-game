from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse

from mvp.server.core.game.GameParametersDTO import GameParametersDTO
from mvp.server.routers.player_actions import router as player_actions_router
from mvp.server.routers.sessions import router as sessions_router, sessions

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)
app.include_router(player_actions_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.on_event("shutdown")
async def cleanup_sessions():
    sessions.clear()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/game-parameters", tags=["Game Parameters"])
async def get_parameters() -> GameParametersDTO:
    return GameParametersDTO()

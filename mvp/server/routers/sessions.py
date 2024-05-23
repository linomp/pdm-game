import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utilities import repeat_every

from mvp.server.core.constants import SESSION_CLEANUP_INTERVAL_SECONDS
from mvp.server.core.game.GameMetrics import GameMetrics
from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.game.GameSessionDTO import GameSessionDTO
from mvp.server.messaging.MqttFrontendConnectionDetails import MqttFrontendConnectionDetails
from mvp.server.messaging.mqtt_client import get_mqtt_client

sessions: dict[str, GameSession] = {}
game_metrics = GameMetrics()
mqtt_client = get_mqtt_client()

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
    responses={404: {"description": "Not found"}},
)


def end_player_session(session_id: str):
    session = sessions.get(session_id)
    if session is not None:
        print(f"{datetime.now()}: Session '{session_id}' will be dropped")
        session.ended_at = datetime.now()
        sessions.pop(session_id)
        game_metrics.update_on_game_abandoned(len(sessions))


def get_session_dependency(session_id: str) -> GameSession:
    session = sessions.get(session_id)

    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    return session


@repeat_every(seconds=SESSION_CLEANUP_INTERVAL_SECONDS, wait_first=False)
async def cleanup_inactive_sessions():
    print(f"{datetime.now()}: Cleaning up sessions...")

    sessions_to_drop = []

    for session_id, session in list(sessions.items()):
        is_abandoned = session.is_abandoned()
        if session.is_game_over or is_abandoned:
            print(f"{datetime.now()}: Session '{session_id}' will be dropped")
            sessions_to_drop.append((session_id, is_abandoned))

    for session_id, is_abandoned in sessions_to_drop:
        sessions.pop(session_id)
        if is_abandoned:
            game_metrics.update_on_game_abandoned(len(sessions))


@router.get("/", response_model=GameSessionDTO)
async def get_session(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    return GameSessionDTO.from_session(session)


@router.post("/", response_model=GameSessionDTO)
async def create_session() -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        def publishing_func(game_session: GameSession) -> None:
            mqtt_client.publish_session_state(game_session.id, GameSessionDTO.from_session(game_session))

        session = GameSession.new_game_session(_id=new_session_id, _state_publish_function=publishing_func)
        sessions[new_session_id] = session

        game_metrics.update_on_game_started(len(sessions))

    return GameSessionDTO.from_session(sessions[new_session_id])


@router.get("/metrics", response_model=GameMetrics)
async def get_metrics() -> GameMetrics:
    return game_metrics


@router.get("/mqtt-connection-details", response_model=MqttFrontendConnectionDetails)
async def get_mqtt_connection_details(session_id: str) -> MqttFrontendConnectionDetails:
    session = sessions.get(session_id)

    if session.is_abandoned() or session.is_game_over:
        raise HTTPException(status_code=412, detail="Session has already been terminated")

    return MqttFrontendConnectionDetails(session_id)


@router.put("/turns", response_model=GameSessionDTO)
async def advance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    await session.advance_one_turn()

    if session.is_game_over:
        game_metrics.update_on_game_ended(session.get_total_duration())

    return GameSessionDTO.from_session(session)

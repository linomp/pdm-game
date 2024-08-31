import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utilities import repeat_every

from mvp.server.core.GameSession import GameSession
from mvp.server.core.GameSessionDTO import GameSessionDTO
from mvp.server.core.constants import SESSION_CLEANUP_INTERVAL_SECONDS
from mvp.server.core.shared import sessions
from mvp.server.messaging.MqttFrontendConnectionDetails import MqttFrontendConnectionDetails
from mvp.server.messaging.mqtt_client import get_mqtt_client, MqttClientBase

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


def cleanup_session(session_id: str):
    session = sessions.get(session_id)
    if session is not None:
        print(f"{datetime.now()}: Session '{session_id}' will be dropped")
        sessions.pop(session_id)


@repeat_every(seconds=600, wait_first=False)
async def publish_mqtt_client_heartbeat(mqtt_client: MqttClientBase = Depends(get_mqtt_client)):
    mqtt_client.publish_heartbeat()


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


@router.get("/", response_model=GameSessionDTO)
async def get_session(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    return GameSessionDTO.from_session(session)


@router.post("/", response_model=GameSessionDTO)
async def create_session(mqtt_client: MqttClientBase = Depends(get_mqtt_client)) -> GameSessionDTO:
    new_session_id = uuid.uuid4().hex

    if new_session_id not in sessions:
        def publishing_func(game_session: GameSession) -> None:
            mqtt_client.publish_session_state(game_session.id, GameSessionDTO.from_session(game_session))

        session = GameSession.new_game_session(_id=new_session_id, _state_publish_function=publishing_func)
        sessions[new_session_id] = session

    return GameSessionDTO.from_session(sessions[new_session_id])


@router.post("/mqtt-heartbeat")
async def send_mqtt_heartbeat(mqtt_client: MqttClientBase = Depends(get_mqtt_client)) -> JSONResponse:
    error = mqtt_client.publish_heartbeat()
    if error is None:
        return JSONResponse(status_code=200, content={"message": "Heartbeat sent"})
    return JSONResponse(status_code=500, content={"message": error})


@router.get("/mqtt-connection-details", response_model=MqttFrontendConnectionDetails)
async def get_mqtt_connection_details(session_id: str) -> MqttFrontendConnectionDetails:
    session = sessions.get(session_id)

    if session.is_abandoned() or session.is_game_over:
        raise HTTPException(status_code=412, detail="Session has already been terminated")

    return MqttFrontendConnectionDetails(session_id)


@router.put("/turns", response_model=GameSessionDTO)
async def advance(session: GameSession = Depends(get_session_dependency)) -> GameSessionDTO:
    await session.advance_one_turn()

    return GameSessionDTO.from_session(session)

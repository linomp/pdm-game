from typing import Any

from pydantic import BaseModel

from mvp.server.core.constants import *
from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.game.MachineStateDTO import MachineStateDTO
from mvp.server.core.game.UserMessage import UserMessage


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_state: MachineStateDTO
    available_funds: float
    is_game_over: bool
    game_over_reason: str | None = None
    final_score: float | None = None
    user_messages: dict[str, UserMessage] = {}
    cash_multiplier: int = 1

    @staticmethod
    def from_session(session: GameSession) -> "GameSessionDTO":
        dto = GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            available_funds=session.available_funds,
            is_game_over=session.is_game_over,
            machine_state=MachineStateDTO.from_machine_state(session.machine_state),
            final_score=None,
            user_messages=session.user_messages,
            cash_multiplier=session.cash_multiplier
        )

        if session.is_game_over:
            dto.game_over_reason = GAME_OVER_MESSAGE_MACHINE_BREAKDOWN if session.machine_state.is_broken() else GAME_OVER_MESSAGE_NO_MONEY
            dto.final_score = session.get_score()

        # Filter out sensor data & predictions that the player has not purchased
        dto.machine_state = MachineStateDTO.from_machine_state(session.machine_state)

        for sensor, purchased in session.available_sensors.items():
            if not purchased:
                dto.machine_state.hide_sensor_data(sensor)

        for prediction, purchased in session.available_predictions.items():
            if not purchased:
                dto.machine_state.hide_prediction(prediction)

        return dto

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "GameSessionDTO":
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_state=MachineStateDTO.from_dict(json.get("machine_state", {})),
            available_funds=json.get("available_funds", 0.),
            is_game_over=json.get("is_game_over", False),
            user_messages=json.get("user_messages", {}),
            cash_multiplier=json.get("current_step", 1),
        )

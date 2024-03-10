from typing import Any

from pydantic import BaseModel

from mvp.server.core.constants import *
from mvp.server.core.game.GameSession import GameSession
from mvp.server.core.machine.MachineState import MachineState
from mvp.server.core.machine.MachineStateDTO import MachineStateDTO


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_state: MachineStateDTO
    available_funds: float
    is_game_over: bool
    game_over_reason: str | None = None

    @staticmethod
    def from_session(session: GameSession):
        dto = GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            available_funds=session.available_funds,
            is_game_over=session.is_game_over,
            machine_state=MachineStateDTO.from_machine_state(session.machine_state)
        )

        if session.is_game_over:
            dto.game_over_reason = GAME_OVER_MESSAGE_MACHINE_BREAKDOWN if session.machine_state.is_broken() else GAME_OVER_MESSAGE_NO_MONEY

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
    def from_dict(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_state=MachineState.from_dict(json.get("machine_state", {})),
            available_funds=json.get("available_funds", 0.),
            is_game_over=json.get("is_game_over", False),
        )

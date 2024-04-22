import asyncio
import math
import os
from datetime import datetime
from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseModel

from mvp.server.core.analysis.rul_prediction import default_rul_prediction_fn
from mvp.server.core.constants import *
from mvp.server.core.machine.MachineState import MachineState

load_dotenv()


class GameSession(BaseModel):
    id: str
    current_step: int
    machine_state: MachineState
    available_funds: float
    is_game_over: bool = False
    available_sensors: dict[str, bool] = None
    available_predictions: dict[str, bool] = None
    last_updated: datetime = None
    started_at: datetime = None
    ended_at: datetime = None
    machine_state_history: list[tuple[int, MachineState]] = []
    state_publish_function: Callable[["GameSession"], None]
    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(_id: str, _state_publish_function: Callable[["GameSession"], None]) -> "GameSession":
        session = GameSession(
            id=_id,
            current_step=0,
            machine_state=MachineState.new_machine_state(),
            available_funds=INITIAL_CASH,
            started_at=datetime.now(),
            state_publish_function=_state_publish_function
        )
        session.available_sensors = {sensor: False for sensor in session.machine_state.get_purchasable_sensors()}
        session.available_predictions = {prediction: False for prediction in
                                         session.machine_state.get_purchasable_predictions()}
        session.last_updated = datetime.now()

        return session

    def is_abandoned(self) -> bool:
        if self.ended_at is not None:
            return False

        return (datetime.now() - self.last_updated).total_seconds() >= IDLE_SESSION_TTL_SECONDS

    def get_total_duration(self) -> float:
        if self.ended_at is None:
            raise ValueError("Game is not over yet")

        return (self.ended_at - self.started_at).total_seconds()

    def update_game_over_flag(self) -> None:
        self.is_game_over = False

        if os.getenv("DEV_FORCE_QUICK_FINISH", False):
            if self.current_step >= 30:
                self.machine_state.health_percentage = -1

        if self.machine_state.is_broken():
            self.is_game_over = True
            self.ended_at = datetime.now()
            print(
                f"{datetime.now()}: GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_state}"
            )

    async def advance_one_turn(self) -> list[MachineState]:
        collected_machine_states_during_turn = []

        self.last_updated = datetime.now()

        for _ in range(TIMESTEPS_PER_MOVE):
            # collect stats
            collected_machine_states_during_turn.append(self.machine_state)

            self.update_game_over_flag()
            if self.is_game_over:
                break

            self.current_step += 1
            self.machine_state.update_parameters(self.current_step)

            # Player earns money for the production at every timestep
            self.available_funds += math.ceil(REVENUE_PER_DAY / TIMESTEPS_PER_MOVE)

            # Publish state every 2 steps (to reduce the load on the MQTT broker)
            if self.current_step % 2 == 0:
                self.state_publish_function(self)

            await asyncio.sleep(GAME_TICK_INTERVAL)

        self.machine_state.update_prediction(
            self.current_step,
            self.rul_predictor,
            collected_machine_states_during_turn
        )

        self.machine_state_history.extend(
            zip(
                range(self.current_step - TIMESTEPS_PER_MOVE, self.current_step),
                collected_machine_states_during_turn
            )
        )

        return collected_machine_states_during_turn

    def do_maintenance(self) -> bool:
        if self.available_funds < MAINTENANCE_COST:
            return False

        self.available_funds -= MAINTENANCE_COST
        self.machine_state.do_maintenance()
        return True

    def purchase_sensor(self, sensor: str) -> bool:
        if self.available_funds < SENSOR_COST:
            return False

        self.available_funds -= SENSOR_COST
        self.available_sensors[sensor] = True
        return True

    def purchase_prediction(self, prediction: str) -> bool:
        if self.available_funds < PREDICTION_MODEL_COST:
            return False

        self.available_funds -= PREDICTION_MODEL_COST
        self.available_predictions[prediction] = True
        return True

    def get_score(self) -> float:
        # TODO: review this score calculation, decide if needs to be more complex
        return (self.current_step * self.available_funds) / 100

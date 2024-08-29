import asyncio
import os
import random
from datetime import datetime
from typing import Callable

from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.concurrency import run_in_threadpool

from mvp.server.core.analysis.rul_prediction import default_rul_prediction_fn, svr_rul_prediction_fn
from mvp.server.core.constants import *
from mvp.server.core.game.MachineState import MachineState, OperationalParameters, get_purchasable_sensors, \
    get_purchasable_predictions
from mvp.server.core.game.UserMessage import UserMessage

load_dotenv()

FORCE_DEMAND_PEAK_EVENT = os.getenv("DEV_FORCE_DEMAND_PEAK_EVENT", False)
FORCE_QUICK_FINISH = os.getenv("DEV_FORCE_QUICK_FINISH", False)
COLLECT_MACHINE_HISTORY = os.getenv("COLLECT_MACHINE_HISTORY", False)


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
    rul_predictor: Callable[[int, OperationalParameters, list[str]], int | None] = default_rul_prediction_fn
    user_messages: dict[str, UserMessage] = {}
    cash_multiplier: int = 1

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
        session.available_sensors = {sensor: False for sensor in get_purchasable_sensors()}
        session.available_predictions = {prediction: False for prediction in
                                         get_purchasable_predictions()}
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

        if FORCE_QUICK_FINISH and self.current_step >= TIMESTEPS_PER_MOVE:
            self.machine_state.health_percentage = -1

        if self.machine_state.is_broken():
            self.is_game_over = True
            self.ended_at = datetime.now()
            print(
                f"{datetime.now()}: GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_state}"
            )

    async def advance_one_turn(self) -> tuple[MachineState, list[MachineState]]:
        collected_machine_states_during_turn = []

        self.last_updated = datetime.now()

        # if there is a demand peak bonus up to this point, multiply the player cash for this turn!
        if "demand_peak_bonus" in self.user_messages:
            self.cash_multiplier = DEMAND_PEAK_BONUS_MULTIPLIER
            self.user_messages.pop("demand_peak_bonus", None)

        for s in range(TIMESTEPS_PER_MOVE - 1):

            if COLLECT_MACHINE_HISTORY:
                collected_machine_states_during_turn.append(self.machine_state)

            self.update_game_over_flag()
            if self.is_game_over:
                return self.machine_state, collected_machine_states_during_turn

            self.current_step += 1
            self.machine_state.update_parameters(self.current_step)

            # Player earns money for the production at every timestep
            self.available_funds += self.cash_multiplier * REVENUE_PER_DAY / TIMESTEPS_PER_MOVE

            # Publish state every 3 steps (to reduce the load on the MQTT broker)
            if s == 0 or self.current_step % 4 == 0:
                await run_in_threadpool(lambda: self.state_publish_function(self))

            await asyncio.sleep(GAME_TICK_INTERVAL)

        self.update_rul_prediction()
        self.cash_multiplier = 1
        self.current_step += 1

        # 😈 probability of bonus multiplier increases with time, when it is also most risky for the player to skip maintenance!
        # TODO: organize this better, there are too many things mixed here...  probably won't remember what this code does in 1 week!
        r = 100 * random.random() / (0.5 * self.current_step)
        if (r < DEMAND_PEAK_EVENT_PROBABILITY) or FORCE_DEMAND_PEAK_EVENT:
            self.user_messages["demand_peak_bonus"] = UserMessage(
                type="INFO",
                content=f"Demand Peak! - Skip maintenance and earn {DEMAND_PEAK_BONUS_MULTIPLIER}x cash in the next turn!"
            )

        if COLLECT_MACHINE_HISTORY:
            self.machine_state_history.extend(
                zip(
                    range(self.current_step - TIMESTEPS_PER_MOVE, self.current_step),
                    collected_machine_states_during_turn
                )
            )

        return self.machine_state, collected_machine_states_during_turn

    def do_maintenance(self) -> bool:
        if self.available_funds < MAINTENANCE_COST:
            return False

        # if there was a demand peak bonus and player does maintenance, it gets cleared
        self.user_messages.pop("demand_peak_bonus", None)

        self.available_funds -= MAINTENANCE_COST
        self.machine_state.do_maintenance()
        self.update_rul_prediction()

        return True

    def purchase_sensor(self, sensor: str) -> bool:
        if self.available_funds < SENSOR_COST:
            return False

        self.available_funds -= SENSOR_COST
        self.available_sensors[sensor] = True
        self.update_rul_prediction()

        return True

    def purchase_prediction(self, prediction: str) -> bool:
        if self.available_funds < PREDICTION_MODEL_COST:
            return False

        self.available_funds -= PREDICTION_MODEL_COST
        self.available_predictions[prediction] = True
        self.rul_predictor = svr_rul_prediction_fn
        self.update_rul_prediction()

        return True

    def update_rul_prediction(self) -> None:
        self.user_messages.pop("rul_accuracy_warning", None)

        for prediction, purchased in self.available_predictions.items():
            if prediction == 'predicted_rul' and purchased:

                if not all(self.available_sensors.values()):
                    self.user_messages["rul_accuracy_warning"] = UserMessage(
                        type="WARNING",
                        content="Some sensor(s) are missing. RUL prediction may not be accurate!"
                    )

                self.machine_state.update_prediction(
                    self.current_step,
                    self.rul_predictor,
                    [s for s in self.available_sensors.keys() if self.available_sensors[s]]
                )

    def get_score(self) -> int:
        raw_score = self.current_step * self.available_funds
        return round(raw_score / 70)

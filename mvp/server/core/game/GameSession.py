import asyncio
from typing import Callable

from pydantic import BaseModel

from mvp.server.core.analysis.rul_prediction import default_rul_prediction_fn
from mvp.server.core.constants import *
from mvp.server.core.machine.MachineState import MachineState


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_state: MachineState
    available_funds: float = 0.
    is_game_over: bool = False
    available_sensors: dict[str, bool] = None
    available_predictions: dict[str, bool] = None

    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(_id: str):
        session = GameSession(
            id=_id,
            current_step=0,
            machine_state=MachineState.new_machine_state(),
            available_funds=INITIAL_CASH
        )
        session.available_sensors = {sensor: False for sensor in session.machine_state.get_purchasable_sensors()}
        session.available_predictions = {prediction: False for prediction in
                                         session.machine_state.get_purchasable_predictions()}
        return session

    def check_if_game_over(self):
        self.is_game_over = True

        if self.machine_state.is_broken():
            print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_state}")
        # TODO: decide if to allow for slightly negative overshoot (player debt)
        # TODO: decide if to bring back this rule. While testing it turned out frustrating for the player.
        # elif self.available_funds <= 0:
        #     print(
        #         f"GameSession '{self.id}' - player ran out of money at step {self.current_step} - {self.machine_state}")
        else:
            self.is_game_over = False

        return self.is_game_over

    async def advance_one_turn(self) -> list[MachineState]:
        collected_machine_states_during_turn = []

        for _ in range(TIMESTEPS_PER_MOVE):
            # collect stats
            collected_machine_states_during_turn.append(self.machine_state)

            self.check_if_game_over()
            if self.is_game_over:
                break

            self.current_step += 1
            self.machine_state.update_parameters(self.current_step)
            # Player earns money for the production at every timestep
            self.available_funds += REVENUE_PER_DAY / TIMESTEPS_PER_MOVE
            self._log()

            await asyncio.sleep(0.5)

        self.machine_state.update_prediction(
            self.current_step,
            self.rul_predictor,
            collected_machine_states_during_turn
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

    def _log(self, multiple=5):
        if self.current_step % multiple == 0:
            print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_state}")

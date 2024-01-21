import asyncio
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.core.analysis.rul_prediction import default_rul_prediction_fn
from mvp.server.core.constants import TIMESTEPS_PER_MOVE
from mvp.server.core.machine.MachineState import MachineState


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_state: MachineState

    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(_id: str):
        return GameSession(
            id=_id,
            current_step=0,
            machine_state=MachineState.new_machine_state()
        )

    def is_game_over(self) -> bool:
        if self.machine_state.is_broken():
            print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_state}")
            return True
        # TODO: add other game over conditions, i.e. player ran out of money
        return False

    async def advance_one_turn(self) -> list[MachineState]:
        collected_machine_states_during_turn = []

        for _ in range(TIMESTEPS_PER_MOVE):
            # collect stats
            collected_machine_states_during_turn.append(self.machine_state)

            if self.is_game_over():
                break

            self.current_step += 1
            self.machine_state.update(self.current_step, self.rul_predictor)
            self._log()

            await asyncio.sleep(0.5)

        return collected_machine_states_during_turn

    def do_maintenance(self):
        # TODO - add a cost for maintenance, reject if player doesn't have enough money
        self.machine_state.do_maintenance()

    def _log(self, multiple=5):
        if self.current_step % multiple == 0:
            print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_state}")


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_state: MachineState | None = None

    # TODO: define MachineStateDTO to hide some fields from the player, e.g. health_percentage

    @staticmethod
    def from_session(session: 'GameSession'):
        return GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            machine_state=session.machine_state,
        )

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_state=MachineState.from_dict(json.get("machine_state", {}))
        )

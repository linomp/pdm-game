import asyncio
from typing import Any, Callable

from pydantic import BaseModel

from mvp.server.analysis import default_rul_prediction_fn
from mvp.server.constants import TIMESTEPS_PER_MOVE
from mvp.server.data_models.MachineStats import MachineStats


class GameSession(BaseModel):
    id: str
    current_step: int = 0
    machine_stats: MachineStats

    # TODO: Update this function in-game, to simulate a change in the model (an "upgrade" for the player)
    rul_predictor: Callable[[int], int | None] = default_rul_prediction_fn

    @staticmethod
    def new_game_session(id: str, current_step: int = 0):
        return GameSession(
            id=id,
            current_step=0,
            machine_stats=MachineStats.new_machine_stats(current_step)
        )

    async def advance_one_turn(self) -> list[MachineStats]:
        collected_machine_stats_during_turn = []

        for _ in range(TIMESTEPS_PER_MOVE):
            # collect stats
            collected_machine_stats_during_turn.append(self.machine_stats)

            # check if game over
            if self.machine_stats.is_broken():
                print(f"GameSession '{self.id}' - machine failed at step {self.current_step} - {self.machine_stats}")
                break

            self.current_step += 1
            self.machine_stats.update_stats_and_parameters(self.current_step, self.rul_predictor)
            self._log()

            await asyncio.sleep(0.5)

        return collected_machine_stats_during_turn

    def _log(self, multiple=5):
        if self.current_step % multiple == 0:
            print(f"GameSession '{self.id}' - step: {self.current_step} - {self.machine_stats}")


class GameSessionDTO(BaseModel):
    id: str
    current_step: int
    machine_stats: MachineStats | None = None

    @staticmethod
    def from_session(session: 'GameSession'):
        return GameSessionDTO(
            id=session.id,
            current_step=session.current_step,
            machine_stats=session.machine_stats,
        )

    @staticmethod
    def from_dict(json: dict[str, Any]):
        return GameSessionDTO(
            id=json.get("id", ""),
            current_step=json.get("current_step", 0),
            machine_stats=MachineStats.from_dict(json.get("machine_stats", {}))
        )
